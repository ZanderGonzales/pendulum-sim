from __future__ import annotations

import copy
import csv
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, Sampler, TensorDataset

from pendulum_sim.data import SimulationDataset
from model_residual.model import ResidualStateNetwork, Standardizer


@dataclass(frozen=True)
class ResidualTrajectorySplit:
    train: np.ndarray
    validation: np.ndarray
    test: np.ndarray


@dataclass
class ResidualTrainingResult:
    model: ResidualStateNetwork
    input_scaler: Standardizer
    target_scaler: Standardizer
    split: ResidualTrajectorySplit
    history: dict[str, list[float]]
    optimizer_state: dict
    seed: int
    training_config: dict[str, float | int | None]
    best_epoch: int
    best_validation_loss: float
    scheduler_state: dict


class ShuffledBalancedBatchSampler(Sampler[list[int]]):
    """Create an exact number of shuffled, near-equal batches without dropping samples."""

    def __init__(self, sample_count: int, batch_count: int, seed: int) -> None:
        if sample_count <= 0:
            raise ValueError("sample_count must be positive")
        if batch_count <= 0 or batch_count > sample_count:
            raise ValueError("batch_count must be positive and no greater than sample_count")
        self.sample_count = sample_count
        self.batch_count = batch_count
        self.seed = seed
        self.epoch = 0

    def __iter__(self):
        generator = torch.Generator()
        generator.manual_seed(self.seed + self.epoch)
        self.epoch += 1
        shuffled_indices = torch.randperm(self.sample_count, generator=generator).tolist()
        base_size, extra = divmod(self.sample_count, self.batch_count)
        start = 0
        for batch_index in range(self.batch_count):
            batch_size = base_size + int(batch_index < extra)
            end = start + batch_size
            yield shuffled_indices[start:end]
            start = end

    def __len__(self) -> int:
        return self.batch_count


def make_training_loader(
    inputs: torch.Tensor,
    targets: torch.Tensor,
    batch_size: int | None = 256,
    batches_per_epoch: int | None = None,
    seed: int = 0,
) -> DataLoader:
    """Return a shuffled DataLoader that either uses a fixed batch size or an exact batch count."""
    if inputs.shape[0] != targets.shape[0]:
        raise ValueError("inputs and targets must contain the same number of samples")
    if batches_per_epoch is None:
        if batch_size is None or batch_size <= 0:
            raise ValueError("batch_size must be positive when batches_per_epoch is not set")
    elif batch_size is not None:
        raise ValueError("set either batch_size or batches_per_epoch, not both")

    dataset = TensorDataset(inputs, targets)
    if batches_per_epoch is not None:
        sampler = ShuffledBalancedBatchSampler(
            sample_count=len(dataset),
            batch_count=batches_per_epoch,
            seed=seed,
        )
        return DataLoader(dataset, batch_sampler=sampler)

    generator = torch.Generator()
    generator.manual_seed(seed)
    return DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=True,
        drop_last=False,
        generator=generator,
    )


def build_residual_step_dataset(
    dataset: SimulationDataset,
    trajectory_indices: np.ndarray,
) -> tuple[torch.Tensor, torch.Tensor]:
    """Build residual-step inputs and targets for the selected trajectories."""
    num_trajectories = len(trajectory_indices)
    if num_trajectories == 0:
        raise ValueError("at least one trajectory is required")

    theta = dataset.theta[trajectory_indices]
    omega = dataset.omega[trajectory_indices]
    torque = dataset.torque[trajectory_indices]

    step_count = theta.shape[1] - 1
    inputs = np.empty((num_trajectories * step_count, 5), dtype=np.float32)
    targets = np.empty((num_trajectories * step_count, 2), dtype=np.float32)
    offset = 0
    for step in range(step_count):
        for i in range(num_trajectories):
            current_theta = theta[i, step]
            current_omega = omega[i, step]
            current_torque = torque[i, step]
            next_torque = torque[i, step + 1]
            inputs[offset] = np.array(
                [
                    current_theta,
                    current_omega,
                    current_torque,
                    0.5 * (current_torque + next_torque),
                    next_torque,
                ],
                dtype=np.float32,
            )
            targets[offset] = np.array(
                [
                    theta[i, step + 1] - theta[i, step],
                    omega[i, step + 1] - omega[i, step],
                ],
                dtype=np.float32,
            )
            offset += 1

    return torch.from_numpy(inputs), torch.from_numpy(targets)


def residual_train_supervised(
    dataset: SimulationDataset,
    model: ResidualStateNetwork | None = None,
    max_epochs: int = 100,
    batch_size: int | None = 256,
    batches_per_epoch: int | None = None,
    max_optimizer_steps: int = 20000,
    learning_rate: float = 1e-3,
    scheduler_factor: float = 0.5,
    scheduler_patience: int = 10,
    min_learning_rate: float = 1e-6,
    train_fraction: float = 0.6,
    validation_fraction: float = 0.2,
    seed: int = 0,
    split: ResidualTrajectorySplit | None = None,
) -> ResidualTrainingResult:
    """Train a residual model on one-step state increments with trajectory-level splits."""
    if max_epochs <= 0:
        raise ValueError("max_epochs must be positive")
    if max_optimizer_steps <= 0:
        raise ValueError("max_optimizer_steps must be positive")
    if not 0.0 < scheduler_factor < 1.0:
        raise ValueError("scheduler_factor must be between zero and one")
    if scheduler_patience < 0:
        raise ValueError("scheduler_patience must be nonnegative")
    if min_learning_rate < 0.0 or min_learning_rate > learning_rate:
        raise ValueError("min_learning_rate must be between zero and learning_rate")

    torch.manual_seed(seed)
    if split is None:
        num_trajectories = dataset.theta.shape[0]
        generator = np.random.default_rng(seed)
        shuffled = generator.permutation(num_trajectories)
        train_count = max(1, int(num_trajectories * train_fraction))
        validation_count = max(1, int(num_trajectories * validation_fraction))
        if train_count + validation_count >= num_trajectories:
            validation_count = num_trajectories - train_count - 1
        split = ResidualTrajectorySplit(
            train=np.sort(shuffled[:train_count]),
            validation=np.sort(shuffled[train_count : train_count + validation_count]),
            test=np.sort(shuffled[train_count + validation_count :]),
        )
    else:
        selected = np.concatenate([split.train, split.validation, split.test])
        if np.any(selected < 0) or np.any(selected >= dataset.theta.shape[0]):
            raise ValueError("split indices are out of bounds")
        if np.unique(selected).size != selected.size:
            raise ValueError("trajectory splits must not overlap")

    train_inputs, train_targets = build_residual_step_dataset(dataset, split.train)
    validation_inputs, validation_targets = build_residual_step_dataset(dataset, split.validation)

    input_scaler = Standardizer.fit(train_inputs)
    target_scaler = Standardizer.fit(train_targets)
    train_inputs = input_scaler.transform(train_inputs)
    train_targets = target_scaler.transform(train_targets)
    validation_inputs = input_scaler.transform(validation_inputs)
    validation_targets = target_scaler.transform(validation_targets)
    training_loader = make_training_loader(
        train_inputs,
        train_targets,
        batch_size=batch_size,
        batches_per_epoch=batches_per_epoch,
        seed=seed,
    )

    if model is None:
        model = ResidualStateNetwork()

    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer,
        mode="min",
        factor=scheduler_factor,
        patience=scheduler_patience,
        min_lr=min_learning_rate,
    )
    loss_function = nn.MSELoss()
    history = {
        "epoch": [],
        "optimizer_step": [],
        "samples_seen": [],
        "learning_rate": [],
        "train_loss": [],
        "validation_loss": [],
    }
    best_validation_loss = float("inf")
    best_epoch = 0
    best_model_state = None
    best_optimizer_state = None
    best_scheduler_state = None
    optimizer_step = 0
    samples_seen = 0

    for epoch in range(max_epochs):
        model.train()
        epoch_loss_sum = 0.0
        epoch_sample_count = 0
        for batch_inputs, batch_targets in training_loader:
            optimizer.zero_grad()
            predictions = model(batch_inputs)
            batch_loss = loss_function(predictions, batch_targets)
            batch_loss.backward()
            optimizer.step()

            batch_sample_count = batch_inputs.shape[0]
            epoch_loss_sum += float(batch_loss.item()) * batch_sample_count
            epoch_sample_count += batch_sample_count
            optimizer_step += 1
            samples_seen += batch_sample_count

        epoch_train_loss = epoch_loss_sum / epoch_sample_count

        model.eval()
        with torch.no_grad():
            validation_predictions = model(validation_inputs)
            validation_loss = loss_function(validation_predictions, validation_targets)

        validation_loss_value = float(validation_loss.item())
        scheduler.step(validation_loss_value)
        current_learning_rate = float(optimizer.param_groups[0]["lr"])

        history["epoch"].append(float(epoch + 1))
        history["optimizer_step"].append(float(optimizer_step))
        history["samples_seen"].append(float(samples_seen))
        history["learning_rate"].append(current_learning_rate)
        history["train_loss"].append(epoch_train_loss)
        history["validation_loss"].append(validation_loss_value)

        if validation_loss_value < best_validation_loss:
            best_validation_loss = validation_loss_value
            best_epoch = epoch + 1
            best_model_state = {name: value.detach().clone() for name, value in model.state_dict().items()}
            best_optimizer_state = copy.deepcopy(optimizer.state_dict())
            best_scheduler_state = copy.deepcopy(scheduler.state_dict())

        if optimizer_step >= max_optimizer_steps:
            break

    model.load_state_dict(best_model_state)
    if batches_per_epoch is not None:
        minimum_batch_size, extra = divmod(train_inputs.shape[0], batches_per_epoch)
        maximum_batch_size = minimum_batch_size + int(extra > 0)
    else:
        minimum_batch_size = min(int(batch_size), train_inputs.shape[0])
        maximum_batch_size = minimum_batch_size

    return ResidualTrainingResult(
        model=model,
        input_scaler=input_scaler,
        target_scaler=target_scaler,
        split=split,
        history=history,
        optimizer_state=best_optimizer_state,
        seed=seed,
        training_config={
            "batch_size": batch_size,
            "batches_per_epoch": batches_per_epoch,
            "minimum_batch_size": minimum_batch_size,
            "maximum_batch_size": maximum_batch_size,
            "max_epochs": max_epochs,
            "max_optimizer_steps": max_optimizer_steps,
            "learning_rate": learning_rate,
            "scheduler_factor": scheduler_factor,
            "scheduler_patience": scheduler_patience,
            "min_learning_rate": min_learning_rate,
        },
        best_epoch=best_epoch,
        best_validation_loss=best_validation_loss,
        scheduler_state=best_scheduler_state,
    )


def save_residual_checkpoint(result: ResidualTrainingResult, path: str | Path) -> None:
    """Save residual model, optimizer, preprocessing, split, and training metadata."""
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        {
            "model_state_dict": result.model.state_dict(),
            "optimizer_state_dict": result.optimizer_state,
            "scheduler_state_dict": result.scheduler_state,
            "input_mean": result.input_scaler.mean,
            "input_std": result.input_scaler.std,
            "target_mean": result.target_scaler.mean,
            "target_std": result.target_scaler.std,
            "train_indices": result.split.train,
            "validation_indices": result.split.validation,
            "test_indices": result.split.test,
            "history": result.history,
            "seed": result.seed,
            "training_config": result.training_config,
            "best_epoch": result.best_epoch,
            "best_validation_loss": result.best_validation_loss,
        },
        output,
    )


def save_residual_training_log(result: ResidualTrainingResult, path: str | Path) -> None:
    """Save epoch, optimizer-step, sample-count, and loss checkpoints as CSV."""
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "epoch",
        "optimizer_step",
        "samples_seen",
        "learning_rate",
        "training_loss",
        "validation_loss",
    ]
    with output.open("w", newline="", encoding="utf-8") as log_file:
        writer = csv.DictWriter(log_file, fieldnames=fields)
        writer.writeheader()
        for index in range(len(result.history["epoch"])):
            writer.writerow(
                {
                    "epoch": int(result.history["epoch"][index]),
                    "optimizer_step": int(result.history["optimizer_step"][index]),
                    "samples_seen": int(result.history["samples_seen"][index]),
                    "learning_rate": result.history["learning_rate"][index],
                    "training_loss": result.history["train_loss"][index],
                    "validation_loss": result.history["validation_loss"][index],
                }
            )

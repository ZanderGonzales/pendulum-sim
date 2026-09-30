from __future__ import annotations

import copy
import csv
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

from pendulum_sim.data import SimulationDataset
from model_baseline.model import PendulumStateNetwork, Standardizer


@dataclass(frozen=True)
class TrajectorySplit:
    train: np.ndarray
    validation: np.ndarray
    test: np.ndarray


@dataclass
class TrainingResult:
    model: PendulumStateNetwork
    input_scaler: Standardizer
    target_scaler: Standardizer
    split: TrajectorySplit
    history: dict[str, list[float]]
    optimizer_state: dict
    seed: int
    training_config: dict[str, float | int]
    best_epoch: int
    best_validation_loss: float
    scheduler_state: dict


def make_training_loader(
    inputs: torch.Tensor,
    targets: torch.Tensor,
    batch_size: int,
    seed: int = 0,
) -> DataLoader:
    """Create shuffled batches without separating inputs from their targets."""
    if batch_size <= 0:
        raise ValueError("batch_size must be positive")
    if inputs.shape[0] != targets.shape[0]:
        raise ValueError("inputs and targets must contain the same number of samples")

    generator = torch.Generator()
    generator.manual_seed(seed)
    return DataLoader(
        TensorDataset(inputs, targets),
        batch_size=batch_size,
        shuffle=True,
        drop_last=False,
        generator=generator,
    )


def split_trajectory_indices(
    num_trajectories: int,
    train_fraction: float = 0.6,
    validation_fraction: float = 0.2,
    seed: int = 0,
) -> TrajectorySplit:
    """Split complete trajectory IDs into train, validation, and test groups."""
    if num_trajectories < 3:
        raise ValueError("at least three trajectories are required for three splits")
    if train_fraction <= 0 or validation_fraction <= 0 or train_fraction + validation_fraction >= 1:
        raise ValueError("fractions must be positive and leave data for the test split")

    generator = np.random.default_rng(seed)
    shuffled = generator.permutation(num_trajectories)
    train_count = max(1, int(num_trajectories * train_fraction))
    validation_count = max(1, int(num_trajectories * validation_fraction))
    if train_count + validation_count >= num_trajectories:
        validation_count = num_trajectories - train_count - 1

    return TrajectorySplit(
        train=np.sort(shuffled[:train_count]),
        validation=np.sort(shuffled[train_count : train_count + validation_count]),
        test=np.sort(shuffled[train_count + validation_count :]),
    )


def tensors_for_trajectories(
    dataset: SimulationDataset,
    trajectory_indices: np.ndarray,
) -> tuple[torch.Tensor, torch.Tensor]:
    """Convert selected complete trajectories into flattened input/target tensors."""
    all_inputs, all_targets = dataset.as_tensors()
    num_times = dataset.theta.shape[1]
    row_indices = np.concatenate(
        [np.arange(index * num_times, (index + 1) * num_times) for index in trajectory_indices]
    )
    rows = torch.from_numpy(row_indices).long()
    return all_inputs[rows], all_targets[rows]


def train_supervised(
    dataset: SimulationDataset,
    model: PendulumStateNetwork | None = None,
    max_epochs: int = 100,
    batch_size: int = 256,
    max_optimizer_steps: int = 5000,
    learning_rate: float = 1e-3,
    scheduler_factor: float = 0.5,
    scheduler_patience: int = 10,
    min_learning_rate: float = 1e-6,
    train_fraction: float = 0.6,
    validation_fraction: float = 0.2,
    seed: int = 0,
    split: TrajectorySplit | None = None,
) -> TrainingResult:
    """Train in shuffled mini-batches and stop at a complete epoch boundary."""
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
        split = split_trajectory_indices(
            dataset.theta.shape[0], train_fraction, validation_fraction, seed
        )
    else:
        if split.train.size == 0 or split.validation.size == 0:
            raise ValueError("explicit splits must include training and validation trajectories")
        selected = np.concatenate([split.train, split.validation, split.test])
        if np.any(selected < 0) or np.any(selected >= dataset.theta.shape[0]):
            raise ValueError("split indices must refer to trajectories in the dataset")
        if np.unique(selected).size != selected.size:
            raise ValueError("trajectory splits must not overlap")

    train_inputs, train_targets = tensors_for_trajectories(dataset, split.train)
    validation_inputs, validation_targets = tensors_for_trajectories(dataset, split.validation)

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
        seed=seed,
    )

    if model is None:
        model = PendulumStateNetwork()
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
            train_predictions = model(batch_inputs)
            batch_loss = loss_function(train_predictions, batch_targets)
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
            best_model_state = {
                name: value.detach().clone()
                for name, value in model.state_dict().items()
            }
            best_optimizer_state = copy.deepcopy(optimizer.state_dict())
            best_scheduler_state = copy.deepcopy(scheduler.state_dict())

        if optimizer_step >= max_optimizer_steps:
            break

    model.load_state_dict(best_model_state)

    training_config = {
        "batch_size": batch_size,
        "max_epochs": max_epochs,
        "max_optimizer_steps": max_optimizer_steps,
        "learning_rate": learning_rate,
        "scheduler_factor": scheduler_factor,
        "scheduler_patience": scheduler_patience,
        "min_learning_rate": min_learning_rate,
        "steps_per_epoch": len(training_loader),
        "train_fraction": train_fraction,
        "validation_fraction": validation_fraction,
    }
    return TrainingResult(
        model,
        input_scaler,
        target_scaler,
        split,
        history,
        best_optimizer_state,
        seed,
        training_config,
        best_epoch,
        best_validation_loss,
        best_scheduler_state,
    )


def save_checkpoint(result: TrainingResult, path: str | Path) -> None:
    """Save model, optimizer, preprocessing, split, and loss-history state."""
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


def save_training_log(result: TrainingResult, path: str | Path) -> None:
    """Save the per-epoch update budget, learning rate, and loss history as CSV."""
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

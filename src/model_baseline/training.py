from __future__ import annotations

import copy
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import torch
from torch import nn

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
    training_config: dict[str, float]
    best_epoch: int
    best_validation_loss: float


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
    epochs: int = 200,
    learning_rate: float = 1e-3,
    train_fraction: float = 0.6,
    validation_fraction: float = 0.2,
    seed: int = 0,
    split: TrajectorySplit | None = None,
) -> TrainingResult:
    """Train a full-state model using MSE and trajectory-level data splits."""
    if epochs <= 0:
        raise ValueError("epochs must be positive")

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

    if model is None:
        model = PendulumStateNetwork()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    loss_function = nn.MSELoss()
    history = {"train_loss": [], "validation_loss": []}
    best_validation_loss = float("inf")
    best_epoch = 0
    best_model_state = None
    best_optimizer_state = None

    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        train_predictions = model(train_inputs)
        train_loss = loss_function(train_predictions, train_targets)
        train_loss.backward()
        optimizer.step()

        model.eval()
        with torch.no_grad():
            validation_predictions = model(validation_inputs)
            validation_loss = loss_function(validation_predictions, validation_targets)

        history["train_loss"].append(float(train_loss.item()))
        validation_loss_value = float(validation_loss.item())
        history["validation_loss"].append(validation_loss_value)
        if validation_loss_value < best_validation_loss:
            best_validation_loss = validation_loss_value
            best_epoch = epoch + 1
            best_model_state = {
                name: value.detach().clone()
                for name, value in model.state_dict().items()
            }
            best_optimizer_state = copy.deepcopy(optimizer.state_dict())

    model.load_state_dict(best_model_state)

    training_config = {
        "epochs": epochs,
        "learning_rate": learning_rate,
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
    )


def save_checkpoint(result: TrainingResult, path: str | Path) -> None:
    """Save model, optimizer, preprocessing, split, and loss-history state."""
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        {
            "model_state_dict": result.model.state_dict(),
            "optimizer_state_dict": result.optimizer_state,
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

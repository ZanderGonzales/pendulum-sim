from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import torch

from pendulum_sim.data import SimulationDataset
from model_baseline.training import tensors_for_trajectories


def evaluate_model(
    dataset: SimulationDataset,
    model: torch.nn.Module,
    trajectory_indices: np.ndarray,
    input_scaler,
    target_scaler,
) -> dict[str, float]:
    """Evaluate predictions in physical units on complete trajectories."""
    inputs, targets = tensors_for_trajectories(dataset, trajectory_indices)
    model.eval()
    with torch.no_grad():
        predictions = target_scaler.inverse_transform(
            model(input_scaler.transform(inputs))
        )

    absolute_error = (predictions - targets).abs()
    squared_error = (predictions - targets).square()
    return {
        "mae": float(absolute_error.mean().item()),
        "rmse": float(squared_error.mean().sqrt().item()),
        "max_absolute_error": float(absolute_error.max().item()),
    }


def evaluate_trajectory_metrics(
    dataset: SimulationDataset,
    model: torch.nn.Module,
    trajectory_indices: np.ndarray,
    input_scaler,
    target_scaler,
) -> list[dict[str, float | int]]:
    """Return separate angle and angular-velocity metrics for each trajectory."""
    metrics = []
    model.eval()
    with torch.no_grad():
        for trajectory_index in trajectory_indices:
            inputs, targets = tensors_for_trajectories(
                dataset,
                np.asarray([trajectory_index], dtype=int),
            )
            predictions = target_scaler.inverse_transform(
                model(input_scaler.transform(inputs))
            )
            error = (predictions - targets).abs()
            metrics.append(
                {
                    "trajectory_index": int(trajectory_index),
                    "theta_mae": float(error[:, 0].mean().item()),
                    "theta_rmse": float(error[:, 0].square().mean().sqrt().item()),
                    "omega_mae": float(error[:, 1].mean().item()),
                    "omega_rmse": float(error[:, 1].square().mean().sqrt().item()),
                }
            )
    return metrics


def plot_training_history(history: dict[str, list[float]], save_path: str | Path) -> None:
    """Save training and validation loss versus epoch."""
    output = Path(save_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    figure, axis = plt.subplots(figsize=(8, 5))
    axis.plot(history["train_loss"], label="Training loss")
    axis.plot(history["validation_loss"], label="Validation loss")
    axis.set_xlabel("Epoch")
    axis.set_ylabel("MSE loss")
    axis.set_title("Supervised training history")
    axis.grid(True, alpha=0.3)
    axis.legend()
    figure.tight_layout()
    figure.savefig(output, dpi=200)
    plt.close(figure)


def plot_trajectory_prediction(
    dataset: SimulationDataset,
    model: torch.nn.Module,
    trajectory_index: int,
    input_scaler,
    target_scaler,
    save_path: str | Path,
) -> None:
    """Save predicted and simulator states for one complete trajectory."""
    inputs, targets = tensors_for_trajectories(
        dataset, np.asarray([trajectory_index], dtype=int)
    )
    model.eval()
    with torch.no_grad():
        predictions = target_scaler.inverse_transform(
            model(input_scaler.transform(inputs))
        ).numpy()

    reference = targets.numpy()
    output = Path(save_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    figure, axes = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
    axes[0].plot(dataset.time, reference[:, 0], label="Simulator")
    axes[0].plot(dataset.time, predictions[:, 0], "--", label="Model")
    axes[0].set_ylabel("Angle (rad)")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    axes[1].plot(dataset.time, reference[:, 1], label="Simulator")
    axes[1].plot(dataset.time, predictions[:, 1], "--", label="Model")
    axes[1].set_xlabel("Time (s)")
    axes[1].set_ylabel("Angular velocity (rad/s)")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    figure.tight_layout()
    figure.savefig(output, dpi=200)
    plt.close(figure)

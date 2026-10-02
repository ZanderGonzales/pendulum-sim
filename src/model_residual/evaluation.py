from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import torch

from pendulum_sim.data import SimulationDataset
from model_residual.training import build_residual_step_dataset


def _rollout_residual_prediction(
    dataset: SimulationDataset,
    model: torch.nn.Module,
    trajectory_index: int,
    input_scaler,
    target_scaler,
) -> tuple[np.ndarray, np.ndarray]:
    """Roll out a residual model through one complete trajectory."""
    theta_true = dataset.theta[trajectory_index].copy()
    omega_true = dataset.omega[trajectory_index].copy()
    torque = dataset.torque[trajectory_index]

    predicted_theta = [float(theta_true[0])]
    predicted_omega = [float(omega_true[0])]
    theta = float(theta_true[0])
    omega = float(omega_true[0])

    model.eval()
    with torch.no_grad():
        for step in range(len(torque) - 1):
            residual_input = np.array(
                [
                    [theta, omega, torque[step], 0.5 * (torque[step] + torque[step + 1]), torque[step + 1]],
                ],
                dtype=np.float32,
            )
            delta = model(input_scaler.transform(torch.from_numpy(residual_input))).numpy()[0]
            delta = target_scaler.inverse_transform(torch.from_numpy(delta[None, :])).numpy()[0]
            theta += float(delta[0])
            omega += float(delta[1])
            predicted_theta.append(theta)
            predicted_omega.append(omega)

    return np.asarray(predicted_theta, dtype=float), np.asarray(predicted_omega, dtype=float)


def evaluate_residual_trajectory_metrics(
    dataset: SimulationDataset,
    model: torch.nn.Module,
    trajectory_indices: np.ndarray,
    input_scaler,
    target_scaler,
) -> list[dict[str, float | int]]:
    """Return per-trajectory angle and angular-velocity MAE/RMSE for residual predictions."""
    metrics: list[dict[str, float | int]] = []
    for trajectory_index in trajectory_indices:
        theta_pred, omega_pred = _rollout_residual_prediction(
            dataset,
            model,
            int(trajectory_index),
            input_scaler,
            target_scaler,
        )
        theta_target = dataset.theta[int(trajectory_index)]
        omega_target = dataset.omega[int(trajectory_index)]

        theta_error = np.abs(theta_pred - theta_target)
        omega_error = np.abs(omega_pred - omega_target)
        metrics.append(
            {
                "trajectory_index": int(trajectory_index),
                "theta_mae": float(theta_error.mean()),
                "theta_rmse": float(np.sqrt(np.mean(theta_error**2))),
                "omega_mae": float(omega_error.mean()),
                "omega_rmse": float(np.sqrt(np.mean(omega_error**2))),
            }
        )
    return metrics


def plot_residual_training_history(history: dict[str, list[float]], save_path: str | Path) -> None:
    """Save training and validation loss versus epoch."""
    output = Path(save_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    figure, axis = plt.subplots(figsize=(8, 5))
    axis.plot(history["train_loss"], label="Training loss")
    axis.plot(history["validation_loss"], label="Validation loss")
    axis.set_xlabel("Epoch")
    axis.set_ylabel("MSE loss")
    axis.set_title("Residual training history")
    axis.grid(True, alpha=0.3)
    axis.legend()
    figure.tight_layout()
    figure.savefig(output, dpi=200)
    plt.close(figure)


def plot_residual_trajectory_prediction(
    dataset: SimulationDataset,
    model: torch.nn.Module,
    trajectory_index: int,
    input_scaler,
    target_scaler,
    save_path: str | Path,
) -> None:
    """Save predicted and simulator states for one residual-model trajectory."""
    theta_pred, omega_pred = _rollout_residual_prediction(
        dataset,
        model,
        trajectory_index,
        input_scaler,
        target_scaler,
    )
    theta_target = dataset.theta[trajectory_index]
    omega_target = dataset.omega[trajectory_index]

    output = Path(save_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    figure, axes = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
    axes[0].plot(dataset.time, theta_target, label="Simulator")
    axes[0].plot(dataset.time, theta_pred, "--", label="Residual model")
    axes[0].set_ylabel("Angle (rad)")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    axes[1].plot(dataset.time, omega_target, label="Simulator")
    axes[1].plot(dataset.time, omega_pred, "--", label="Residual model")
    axes[1].set_xlabel("Time (s)")
    axes[1].set_ylabel("Angular velocity (rad/s)")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    figure.tight_layout()
    figure.savefig(output, dpi=200)
    plt.close(figure)

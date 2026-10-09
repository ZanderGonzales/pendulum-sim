"""Checkpoint loading and recursive inertial-frame unicycle evaluation."""

from __future__ import annotations

import csv
import json
from pathlib import Path
import shutil

import numpy as np
import torch

from model_unicycle_residual.model import UnicycleResidualMLP
from unicycle_sim.dataset import UnicycleDataset
from unicycle_sim.frames import body_to_inertial, angle_difference


def load_checkpoint(path: str | Path, device: str = "cpu") -> tuple[UnicycleResidualMLP, dict]:
    """Load a U3 checkpoint and its frozen input/target standardizers."""
    checkpoint = torch.load(Path(path), map_location=device, weights_only=True)
    config = checkpoint["training_config"]
    model = UnicycleResidualMLP(hidden_size=config["hidden_size"], hidden_layers=config["hidden_layers"])
    model.load_state_dict(checkpoint["model_state_dict"])
    model.to(device).eval()
    return model, checkpoint


def predict_body_increments(model: UnicycleResidualMLP, checkpoint: dict, controls: np.ndarray, dt: float,
                            device: str = "cpu") -> np.ndarray:
    """Predict physical body increments from [v, omega] controls and fixed dt."""
    inputs = np.column_stack((controls, np.full(len(controls), dt))).astype(np.float32)
    x = torch.as_tensor(inputs, device=device)
    mean = checkpoint["input_mean"].to(device)
    scale = checkpoint["input_scale"].to(device)
    target_mean = checkpoint["target_mean"].to(device)
    target_scale = checkpoint["target_scale"].to(device)
    with torch.no_grad():
        prediction = model((x - mean) / scale) * target_scale + target_mean
    return prediction.cpu().numpy()


def recursive_rollout(model: UnicycleResidualMLP, checkpoint: dict, initial_state: np.ndarray,
                      controls: np.ndarray, dt: float, device: str = "cpu") -> tuple[np.ndarray, np.ndarray]:
    """Roll out local increments recursively using the predicted heading each step."""
    body = predict_body_increments(model, checkpoint, controls, dt, device)
    predicted = np.empty((len(controls) + 1, 3), dtype=float)
    predicted[0] = initial_state
    for k, local in enumerate(body):
        predicted[k + 1, :2] = predicted[k, :2] + body_to_inertial(local[:2], predicted[k, 2])
        predicted[k + 1, 2] = predicted[k, 2] + local[2]
    return predicted, body


def _trajectory_metrics(true_states: np.ndarray, predicted_states: np.ndarray) -> dict[str, float]:
    position_error = np.linalg.norm(predicted_states[:, :2] - true_states[:, :2], axis=1)
    heading_unwrapped = predicted_states[:, 2] - true_states[:, 2]
    heading_wrapped = np.asarray(angle_difference(predicted_states[:, 2], true_states[:, 2]))
    true_length = float(np.linalg.norm(np.diff(true_states[:, :2], axis=0), axis=1).sum())
    predicted_length = float(np.linalg.norm(np.diff(predicted_states[:, :2], axis=0), axis=1).sum())
    return {
        "position_mae": float(position_error.mean()),
        "position_rmse": float(np.sqrt(np.mean(position_error ** 2))),
        "final_position_error": float(position_error[-1]),
        "maximum_position_error": float(position_error.max()),
        "heading_mae": float(np.mean(np.abs(heading_wrapped))),
        "heading_rmse": float(np.sqrt(np.mean(heading_wrapped ** 2))),
        "heading_unwrapped_mae": float(np.mean(np.abs(heading_unwrapped))),
        "heading_unwrapped_rmse": float(np.sqrt(np.mean(heading_unwrapped ** 2))),
        "path_length_error": predicted_length - true_length,
        "true_path_length": true_length,
        "predicted_path_length": predicted_length,
    }


def _teacher_forced_metrics(true_states: np.ndarray, predicted_body: np.ndarray,
                            true_body: np.ndarray) -> dict[str, float]:
    local_error = predicted_body - true_body
    inertial_pred = np.stack([
        body_to_inertial(predicted_body[k, :2], true_states[k, 2])
        for k in range(len(predicted_body))
    ])
    true_inertial = np.diff(true_states, axis=0)
    inertial_error = np.column_stack((inertial_pred, predicted_body[:, 2])) - true_inertial
    return {
        "body_dx_mae": float(np.mean(np.abs(local_error[:, 0]))),
        "body_dy_mae": float(np.mean(np.abs(local_error[:, 1]))),
        "body_dtheta_mae": float(np.mean(np.abs(local_error[:, 2]))),
        "inertial_dx_rmse": float(np.sqrt(np.mean(inertial_error[:, 0] ** 2))),
        "inertial_dy_rmse": float(np.sqrt(np.mean(inertial_error[:, 1] ** 2))),
        "inertial_dtheta_rmse": float(np.sqrt(np.mean(inertial_error[:, 2] ** 2))),
    }


def evaluate_test_set(model: UnicycleResidualMLP, checkpoint: dict, dataset: UnicycleDataset,
                      output_dir: str | Path, device: str = "cpu",
                      training_curve_path: str | Path | None = None) -> dict:
    """Save per-trajectory predictions, plots, and free-running test metrics."""
    root = Path(output_dir)
    predictions_dir, plots_dir = root / "predictions", root / "plots"
    predictions_dir.mkdir(parents=True, exist_ok=True)
    plots_dir.mkdir(parents=True, exist_ok=True)
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    test_ids = np.flatnonzero(dataset.split == "test")
    if not len(test_ids):
        raise ValueError("dataset has no test trajectories")
    dt = float(dataset.metadata["dt"])
    trajectory_results, summary_rows, overlay = {}, [], []
    for trajectory_id in test_ids:
        true = dataset.states[trajectory_id]
        controls = dataset.controls[trajectory_id]
        initial = true[0]
        predicted, predicted_body = recursive_rollout(model, checkpoint, initial, controls, dt, device)
        true_body = dataset.delta_body_target[trajectory_id]
        metrics = _trajectory_metrics(true, predicted)
        metrics.update(_teacher_forced_metrics(true, predicted_body, true_body))
        trajectory_results[str(int(trajectory_id))] = metrics
        summary_rows.append({"trajectory_id": int(trajectory_id), **metrics})
        np.savez_compressed(
            predictions_dir / f"trajectory_{trajectory_id:03d}.npz",
            trajectory_id=np.asarray(trajectory_id), dt=np.asarray(dt),
            true_states=true, predicted_states=predicted, controls=controls,
            true_body_increments=true_body, predicted_body_increments=predicted_body,
        )
        time = np.arange(len(true)) * dt
        position_error = np.linalg.norm(predicted[:, :2] - true[:, :2], axis=1)
        heading_error = np.asarray(angle_difference(predicted[:, 2], true[:, 2]))
        fig, ax = plt.subplots(figsize=(6.5, 5.5))
        ax.plot(true[:, 0], true[:, 1], label="True", linewidth=2)
        ax.plot(predicted[:, 0], predicted[:, 1], "--", label="Predicted", linewidth=1.8)
        ax.scatter(true[0, 0], true[0, 1], marker="o", color="black", zorder=3, label="Start")
        ax.set(xlabel="Inertial x (distance units)", ylabel="Inertial y (distance units)",
               title=f"Trajectory {trajectory_id} · U4 recursive rollout")
        ax.axis("equal")
        ax.margins(0.08)
        ax.grid(True, alpha=0.3)
        ax.legend()
        fig.tight_layout()
        fig.savefig(plots_dir / f"path_comparison_{trajectory_id:03d}.png", dpi=150)
        plt.close(fig)
        for name, errors, ylabel in (
            ("position", position_error, "Position error (distance units)"),
            ("heading", heading_error, "Wrapped heading error (rad)"),
        ):
            fig, ax = plt.subplots(figsize=(7, 4))
            ax.plot(time, errors)
            ax.set(xlabel="Time (s)", ylabel=ylabel, title=f"Trajectory {trajectory_id}: {name} error")
            ax.grid(True, alpha=0.3)
            fig.tight_layout()
            fig.savefig(plots_dir / f"{name}_error_vs_time_{trajectory_id:03d}.png", dpi=150)
            plt.close(fig)
        overlay.append((int(trajectory_id), true, predicted))

    fig, ax = plt.subplots(figsize=(8, 6))
    for trajectory_id, true, predicted in overlay:
        ax.plot(true[:, 0], true[:, 1], label=f"True {trajectory_id}")
        ax.plot(predicted[:, 0], predicted[:, 1], "--", label=f"Predicted {trajectory_id}")
        ax.scatter(true[0, 0], true[0, 1], marker="o", s=20)
    ax.set(xlabel="Inertial x (distance units)", ylabel="Inertial y (distance units)",
           title="U4 test trajectories: true and recursive predictions")
    ax.axis("equal")
    ax.margins(0.08)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize="small", ncol=2)
    fig.tight_layout()
    fig.savefig(plots_dir / "path_comparison_summary.png", dpi=160)
    plt.close(fig)

    fields = list(summary_rows[0])
    with (root / "rollout_metrics.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(summary_rows)
    aggregate = {
        metric: float(np.mean([row[metric] for row in summary_rows]))
        for metric in summary_rows[0] if metric != "trajectory_id"
    }
    result = {"per_trajectory": trajectory_results, "mean_across_test_trajectories": aggregate}
    (root / "rollout_metrics.json").write_text(json.dumps(result, indent=2), encoding="utf-8")

    # Include the controls and learning curve that define this checkpoint's experiment.
    all_controls = dataset.controls.reshape(-1, 2)
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.scatter(all_controls[:, 0], all_controls[:, 1], s=6, alpha=0.25)
    ax.set(xlabel="Forward speed v", ylabel="Turn rate omega (rad/s)", title="Dataset control coverage")
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    fig.savefig(plots_dir / "control_coverage.png", dpi=150)
    plt.close(fig)
    training_plot = Path(training_curve_path) if training_curve_path is not None else None
    if training_plot is not None and training_plot.exists():
        shutil.copyfile(training_plot, plots_dir / "training_curves.png")
    return result

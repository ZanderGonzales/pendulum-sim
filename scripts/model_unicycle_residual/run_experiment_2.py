"""Run Experiment 2 with aggressive training maneuvers and a figure-eight test path."""

import argparse
from dataclasses import asdict, replace
import json
from pathlib import Path
import shlex
import subprocess
import sys

import numpy as np

from model_unicycle_residual.evaluation import evaluate_test_set
from model_unicycle_residual.training import TrainingConfig, save_training_outputs, train_model
from unicycle_sim.dataset import DatasetConfig, generate_dataset
from unicycle_sim.dynamics import body_increment, simulate_trajectory
from unicycle_sim.types import UnicycleControl, UnicycleState


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("runs/unicycle_run_2"))
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--dataset-seed", type=int, default=2029)
    args = parser.parse_args()

    # Match Experiment 1's number of transitions and trajectory split so that
    # balanced mini-batch sizes and all optimizer counts remain identical.
    dataset_config = DatasetConfig(
        num_trajectories=64, num_steps=60, dt=0.05,
        speed_range=(0.0, 3.0), omega_range=(-7.0, 7.0),
        control_hold_steps=(1, 3), split_fractions=(0.75, 0.125, 0.125),
        initial_heading_range=(-np.pi, np.pi), seed=args.dataset_seed,
    )
    dataset = generate_dataset(dataset_config)
    train_ids = np.flatnonzero(dataset.split == "train")
    test_ids = np.flatnonzero(dataset.split == "test")
    if len(train_ids) != 48 or len(test_ids) != 8:
        raise ValueError(f"expected 48 training and 8 test trajectories; got {len(train_ids)} and {len(test_ids)}")

    # Sample a Gerono lemniscate x=A sin(t), y=B sin(2t). Midpoint speed and
    # curvature determine the piecewise-constant controls over each interval.
    dt = dataset_config.dt
    steps_per_lobe = 30
    shape_a, shape_b = 0.8, 0.4
    phase_rate = 2.0 * np.pi / (2 * steps_per_lobe * dt)
    figure8_controls_list = []
    for step_index in range(2 * steps_per_lobe):
        phase = (step_index + 0.5) * 2.0 * np.pi / (2 * steps_per_lobe)
        dx_dphase = shape_a * np.cos(phase)
        dy_dphase = 2.0 * shape_b * np.cos(2.0 * phase)
        ddx_dphase = -shape_a * np.sin(phase)
        ddy_dphase = -4.0 * shape_b * np.sin(2.0 * phase)
        speed_squared = dx_dphase ** 2 + dy_dphase ** 2
        speed = np.sqrt(speed_squared) * phase_rate
        omega = (dx_dphase * ddy_dphase - dy_dphase * ddx_dphase) / speed_squared * phase_rate
        figure8_controls_list.append(UnicycleControl(float(speed), float(omega)))
    figure8_controls = tuple(figure8_controls_list)
    initial_heading = float(np.arctan2(2.0 * shape_b, shape_a))
    figure8 = simulate_trajectory(UnicycleState(0.0, 0.0, initial_heading), figure8_controls, dt)
    figure8_states = np.asarray([[state.x, state.y, state.theta] for state in figure8.states])
    closure_error = float(np.linalg.norm(figure8_states[-1, :2] - figure8_states[0, :2]))
    heading_closure_error = abs(float(figure8_states[-1, 2] - figure8_states[0, 2]))
    if closure_error > 0.05 or heading_closure_error > 0.05:
        raise RuntimeError("constructed figure-eight trajectory did not approximately close")

    figure8_id = int(test_ids[0])
    states, controls = dataset.states.copy(), dataset.controls.copy()
    body_targets, inertial_deltas = dataset.delta_body_target.copy(), dataset.delta_inertial_true.copy()
    states[figure8_id] = figure8_states
    controls[figure8_id] = np.asarray([[control.v, control.omega] for control in figure8_controls])
    body_targets[figure8_id] = np.asarray([body_increment(control, dt) for control in figure8_controls])
    inertial_deltas[figure8_id] = np.diff(figure8_states, axis=0)
    metadata = dict(dataset.metadata)
    metadata["figure_eight_test"] = {
        "trajectory_id": figure8_id, "steps_per_lobe": steps_per_lobe,
        "shape_a": shape_a, "shape_b": shape_b,
        "maximum_speed": float(max(control.v for control in figure8_controls)),
        "maximum_absolute_turn_rate": float(max(abs(control.omega) for control in figure8_controls)),
        "dt": dt, "closed_position_error": closure_error,
        "heading_closure_error": heading_closure_error,
        "description": "60-step sampled Gerono lemniscate with a transverse crossing at the origin.",
    }
    dataset = replace(dataset, states=states, controls=controls,
                      delta_body_target=body_targets, delta_inertial_true=inertial_deltas,
                      metadata=metadata)

    # Keep every optimizer setting from Experiment 1 unchanged.
    config = TrainingConfig(
        seed=args.seed, epochs=15, batch_size=None, batches_per_epoch=100,
        max_optimizer_updates=1500, learning_rate=1e-3, hidden_size=64, hidden_layers=2,
    )
    result = train_model(dataset, config)
    if result.optimizer_updates != 1500 or len(result.history) != 15:
        raise RuntimeError("training did not complete 15 epochs x 100 batches = 1500 updates")
    save_training_outputs(result, args.output, summary_filename=None)
    rollout = evaluate_test_set(
        result.model,
        {
            "input_mean": result.input_scaler.mean, "input_scale": result.input_scaler.scale,
            "target_mean": result.target_scaler.mean, "target_scale": result.target_scaler.scale,
        },
        dataset, args.output, training_curve_path=args.output / "loss_curves.png",
    )
    free = rollout["mean_across_test_trajectories"]
    train_samples = len(train_ids) * dataset_config.num_steps
    samples_min, remainder = divmod(train_samples, config.batches_per_epoch)
    samples_max = samples_min + int(remainder > 0)
    epoch_batches = [int(row["batches_per_epoch"]) for row in result.history]
    split_counts = {name: int(np.count_nonzero(dataset.split == name))
                    for name in ("train", "validation", "test")}
    try:
        revision = subprocess.run(["git", "rev-parse", "--short", "HEAD"], check=True,
                                  capture_output=True, text=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        revision = "unknown"
    metadata = {
        "experiment": "Experiment 2",
        "description": "More aggressive training controls; one held-out test trajectory is a closed figure eight.",
        "command": shlex.join([sys.executable, *sys.argv]), "code_version": revision,
        "training_seed": args.seed, "dataset_seed": args.dataset_seed,
        "dataset_config": asdict(dataset_config), "split_counts": split_counts,
        "split_trajectory_ids": {name: np.flatnonzero(dataset.split == name).tolist()
                                  for name in ("train", "validation", "test")},
        "training_config": asdict(config), "optimizer_updates": result.optimizer_updates,
        "epochs_completed": len(result.history),
        "batches_per_epoch": {"typical": max(set(epoch_batches), key=epoch_batches.count),
                               "first_epoch": epoch_batches[0], "last_epoch": epoch_batches[-1]},
        "samples_per_batch": {"minimum": samples_min, "maximum": samples_max,
                               "samples_per_epoch": train_samples},
        "figure_eight_test": metadata["figure_eight_test"],
        "best_epoch": result.best_epoch,
        "best_validation_mse_standardized": result.best_validation_loss,
        "one_step_test_metrics_body_frame": result.test_metrics,
        "free_running_test_metrics": free,
        "mean_x_mae": free["x_mae"], "mean_y_mae": free["y_mae"],
        "mean_theta_mae": free["theta_mae"],
    }
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "run_metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    summary = (
        "# Experiment 2: Aggressive maneuvers and figure-eight test\n\n"
        "**Difference from Experiment 1:** training controls use v=0-3 and omega=-7 to 7, with a new control every 1-3 steps rather than v=0-2, omega=-1.5 to 1.5, and 3-10 steps. One test trajectory is a closed Gerono figure eight with a transverse crossing. The model, optimizer, split sizes, training transitions per epoch, and update schedule match Experiment 1.\n\n"
        f"- Number of trajectories: total 64 (train {split_counts['train']}, validation {split_counts['validation']}, test {split_counts['test']})\n"
        f"- Epochs: {len(result.history)}\n- Batches per epoch: {epoch_batches[0]}\n"
        f"- Samples per batch: {samples_min}-{samples_max} (balanced; {train_samples} training samples per epoch)\n"
        f"- Optimizer updates: {result.optimizer_updates}\n"
        f"- Figure-eight test trajectory ID: {figure8_id} (60 steps, max speed {metadata['figure_eight_test']['maximum_speed']:.4f}, max |omega| {metadata['figure_eight_test']['maximum_absolute_turn_rate']:.4f} rad/s)\n"
        f"- Mean X MAE: {free['x_mae']:.8g}\n- Mean Y MAE: {free['y_mae']:.8g}\n"
        f"- Mean Theta MAE: {free['theta_mae']:.8g} rad\n"
        f"- One-step body-frame RMSE: {result.test_metrics['overall_rmse']:.8g}\n"
        f"- Free-running position RMSE: {free['position_rmse']:.8g}\n"
        f"- Best validation MSE (standardized): {result.best_validation_loss:.8g}\n"
        "- Path comparisons and per-trajectory predictions: `plots/` and `predictions/`.\n"
    )
    (args.output / "Experiment 2 Data.md").write_text(summary, encoding="utf-8")
    print(f"Saved {args.output}")
    print(f"Completed {len(result.history)} epochs x {epoch_batches[0]} batches = {result.optimizer_updates} updates")
    print(f"Figure-eight held-out trajectory: {figure8_id}; closure error: {closure_error:.3e}")
    print(f"Test MAE: X={free['x_mae']:.6g}, Y={free['y_mae']:.6g}, Theta={free['theta_mae']:.6g} rad")


if __name__ == "__main__":
    main()

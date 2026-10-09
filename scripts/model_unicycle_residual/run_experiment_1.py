"""Run numbered Experiment 1 with 48 training trajectories and 100 batches/epoch."""

import argparse
from dataclasses import asdict
import json
from pathlib import Path
import shlex
import subprocess
import sys

import numpy as np

from model_unicycle_residual.evaluation import evaluate_test_set
from model_unicycle_residual.training import TrainingConfig, save_training_outputs, train_model
from unicycle_sim.dataset import DatasetConfig, generate_dataset


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("runs/unicycle_u5/Experiment 1 - 100 Batches 15 Epochs"))
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--dataset-seed", type=int, default=2028)
    parser.add_argument("--steps", type=int, default=60)
    args = parser.parse_args()

    dataset_config = DatasetConfig(
        num_trajectories=64, num_steps=args.steps, dt=0.05,
        speed_range=(0.0, 2.0), omega_range=(-1.5, 1.5),
        control_hold_steps=(3, 10), split_fractions=(0.75, 0.125, 0.125),
        seed=args.dataset_seed,
    )
    dataset = generate_dataset(dataset_config)
    train_count = int(np.count_nonzero(dataset.split == "train"))
    if train_count != 48:
        raise ValueError(f"expected 48 training trajectories, got {train_count}")

    config = TrainingConfig(
        seed=args.seed, epochs=15, batch_size=None, batches_per_epoch=100,
        max_optimizer_updates=1500, learning_rate=1e-3, hidden_size=64, hidden_layers=2,
    )
    result = train_model(dataset, config)
    if result.optimizer_updates != 1500 or len(result.history) != 15:
        raise RuntimeError("training did not complete the requested 15 x 100 optimizer updates")
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
    train_samples = train_count * args.steps
    samples_min, remainder = divmod(train_samples, config.batches_per_epoch)
    samples_max = samples_min + int(remainder > 0)
    epoch_batches = [int(row["batches_per_epoch"]) for row in result.history]
    split_counts = {key: int(np.count_nonzero(dataset.split == key)) for key in ("train", "validation", "test")}
    try:
        revision = subprocess.run(["git", "rev-parse", "--short", "HEAD"], check=True,
                                  capture_output=True, text=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        revision = "unknown"
    metadata = {
        "experiment": "Experiment 1",
        "description": "48 training trajectories, 100 balanced mini-batches per epoch, 15 epochs, 1500 optimizer updates.",
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
        "# Experiment 1: 100 batches per epoch, 15 epochs\n\n"
        "**Difference from the previous update-budget experiments:** uses the same broad-control dataset seed and "
        "48/8/8 trajectory split as U5 Experiments D/F, while setting a smaller balanced batch size through exactly "
        "100 batches per epoch for 15 epochs (1500 updates). This extends the update budget beyond the prior 900-update run.\n\n"
        f"- Number of trajectories: total 64 (train {split_counts['train']}, validation {split_counts['validation']}, test {split_counts['test']})\n"
        f"- Epochs: {len(result.history)}\n- Batches per epoch: {epoch_batches[0]}\n"
        f"- Samples per batch: {samples_min}-{samples_max} (balanced; {train_samples} training samples per epoch)\n"
        f"- Optimizer updates: {result.optimizer_updates}\n"
        f"- Mean X MAE: {free['x_mae']:.8g}\n- Mean Y MAE: {free['y_mae']:.8g}\n"
        f"- Mean Theta MAE: {free['theta_mae']:.8g} rad\n"
        f"- One-step body-frame RMSE: {result.test_metrics['overall_rmse']:.8g}\n"
        f"- Free-running position RMSE: {free['position_rmse']:.8g}\n"
        f"- Best validation MSE (standardized): {result.best_validation_loss:.8g}\n"
        "- Path comparison plots and per-trajectory predictions: `plots/` and `predictions/`.\n"
    )
    (args.output / "Experiment 1 Data.md").write_text(summary, encoding="utf-8")
    print(f"Saved {args.output}")
    print(f"Completed {len(result.history)} epochs x {epoch_batches[0]} batches = {result.optimizer_updates} updates")
    print(f"Test MAE: X={free['x_mae']:.6g}, Y={free['y_mae']:.6g}, Theta={free['theta_mae']:.6g} rad")


if __name__ == "__main__":
    main()

"""Run U4 free-running evaluation from a U3 checkpoint and U2 dataset."""

import argparse
import json
from pathlib import Path
import shlex
import subprocess
import sys

import numpy as np

from model_unicycle_residual.evaluation import evaluate_test_set, load_checkpoint
from unicycle_sim.dataset import load_dataset


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", type=Path, default=Path("runs/unicycle_u3/checkpoint_best.pt"))
    parser.add_argument("--dataset", type=Path, default=Path("runs/unicycle_u2/dataset.npz"))
    parser.add_argument("--output", type=Path, default=Path("runs/unicycle_u4"))
    parser.add_argument("--device", default="cpu")
    args = parser.parse_args()

    model, checkpoint = load_checkpoint(args.checkpoint, args.device)
    dataset = load_dataset(args.dataset)
    metrics = evaluate_test_set(
        model, checkpoint, dataset, args.output, args.device,
        training_curve_path=args.checkpoint.parent / "loss_curves.png",
    )
    try:
        code_version = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"], check=True,
            capture_output=True, text=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        code_version = "unknown"
    metadata = {
        "command": shlex.join([sys.executable, *sys.argv]),
        "code_version": code_version,
        "checkpoint": str(args.checkpoint), "dataset": str(args.dataset),
        "device": args.device, "test_trajectory_ids": [int(i) for i in np.flatnonzero(dataset.split == "test")],
        "dt": dataset.metadata["dt"], "dataset_seed": dataset.metadata["seed"],
        "rollout_mode": "free_running; predicted inertial state recursively feeds the next step",
    }
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "run_metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    mean_metrics = metrics["mean_across_test_trajectories"]
    readme = (
        "# Unicycle U4 recursive rollout\n\n"
        "Predicted local body increments are rotated by the current predicted heading before updating position. "
        "The resulting predicted state is fed into the next step; test states are not substituted during rollout.\n\n"
        f"- Command: `{metadata['command']}`\n- Code version: {code_version}\n"
        f"- Checkpoint: `{args.checkpoint}`\n- Dataset: `{args.dataset}`\n"
        f"- Test trajectories: {metadata['test_trajectory_ids']}\n- Dataset seed: {metadata['dataset_seed']}\n"
        f"- Mean test position RMSE: {mean_metrics['position_rmse']:.8g}\n"
        f"- Mean test final position error: {mean_metrics['final_position_error']:.8g}\n"
        f"- Mean test wrapped heading RMSE: {mean_metrics['heading_rmse']:.8g} rad\n"
        f"- Mean test path-length error: {mean_metrics['path_length_error']:.8g}\n"
    )
    (args.output / "U4_Data.md").write_text(readme, encoding="utf-8")
    print(f"Saved U4 evaluation to {args.output}")
    print(f"Mean free-running metrics: {mean_metrics}")


if __name__ == "__main__":
    main()

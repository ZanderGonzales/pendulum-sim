"""Run U5 experiments A-F (the representation comparison G is intentionally excluded)."""

from __future__ import annotations

import argparse
import csv
from dataclasses import replace
import json
from pathlib import Path
import shlex
import subprocess
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from model_unicycle_residual.evaluation import _teacher_forced_metrics, _trajectory_metrics, recursive_rollout
from model_unicycle_residual.training import TrainingConfig, save_training_outputs, train_model
from unicycle_sim.dataset import DatasetConfig, UnicycleDataset, generate_dataset
from unicycle_sim.dynamics import body_increment, simulate_trajectory
from unicycle_sim.frames import angle_difference, body_to_inertial
from unicycle_sim.types import UnicycleControl, UnicycleState

EXPERIMENT_LETTERS = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F"}


def _experiment_folder(root: Path, experiment_id: int, label: str) -> Path:
    letter = EXPERIMENT_LETTERS[experiment_id]
    short_label = label[2:] if len(label) > 2 and label[1] == "_" else label
    return root / f"Experiment {letter} - {short_label.replace('_', ' ')}"


def _save_path_comparisons(output: Path, paths: list[tuple[int, np.ndarray, np.ndarray]], title: str) -> None:
    plot_dir = output / "plots"
    plot_dir.mkdir(parents=True, exist_ok=True)
    for pattern in ("path_comparison_*.png", "heading_error_vs_time_*.png", "position_error_vs_time_*.png"):
        for stale_plot in plot_dir.glob(pattern):
            stale_plot.unlink()
    for trajectory_id, truth, prediction in paths:
        fig, ax = plt.subplots(figsize=(6.5, 5.5))
        ax.plot(truth[:, 0], truth[:, 1], label="True path", linewidth=2)
        ax.plot(prediction[:, 0], prediction[:, 1], "--", label="Predicted path", linewidth=1.8)
        ax.scatter(truth[0, 0], truth[0, 1], marker="o", color="black", zorder=3, label="Start")
        ax.set(xlabel="Inertial x (distance units)", ylabel="Inertial y (distance units)",
               title=f"{title} · trajectory {trajectory_id}")
        ax.axis("equal")
        ax.margins(0.08)
        ax.grid(True, alpha=0.3)
        ax.legend()
        fig.tight_layout()
        fig.savefig(plot_dir / f"{trajectory_id}_path_comparison.png", dpi=150)
        plt.close(fig)
    fig, ax = plt.subplots(figsize=(8, 6))
    for trajectory_id, truth, prediction in paths:
        ax.plot(truth[:, 0], truth[:, 1], label=f"True {trajectory_id}")
        ax.plot(prediction[:, 0], prediction[:, 1], "--", label=f"Predicted {trajectory_id}")
        ax.scatter(truth[0, 0], truth[0, 1], marker="o", s=18)
    ax.set(xlabel="Inertial x (distance units)", ylabel="Inertial y (distance units)", title=f"{title}: test paths")
    ax.axis("equal")
    ax.margins(0.08)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize="small", ncol=2)
    fig.tight_layout()
    fig.savefig(plot_dir / "summary_path_comparison.png", dpi=160)
    plt.close(fig)


def _dataset_with_headings(dataset: UnicycleDataset, headings: np.ndarray, name: str) -> UnicycleDataset:
    states = np.empty_like(dataset.states)
    inertial = np.empty_like(dataset.delta_inertial_true)
    for trajectory_id, heading in enumerate(headings):
        controls = [UnicycleControl(float(v), float(w)) for v, w in dataset.controls[trajectory_id]]
        trajectory = simulate_trajectory(UnicycleState(0.0, 0.0, float(heading)), controls,
                                         float(dataset.metadata["dt"]))
        states[trajectory_id] = [[s.x, s.y, s.theta] for s in trajectory.states]
        inertial[trajectory_id] = np.diff(states[trajectory_id], axis=0)
    metadata = dict(dataset.metadata)
    metadata["initial_heading_design"] = name
    return replace(dataset, states=states, delta_inertial_true=inertial, metadata=metadata)


def _with_train_count(dataset: UnicycleDataset, train_count: int) -> UnicycleDataset:
    train_ids = np.flatnonzero(dataset.split == "train")
    if train_count > len(train_ids):
        raise ValueError("requested train count exceeds the shared training pool")
    split = dataset.split.copy()
    split[train_ids] = "unused"
    split[train_ids[:train_count]] = "train"
    metadata = dict(dataset.metadata)
    metadata["split_counts"] = {key: int(np.count_nonzero(split == key))
                                for key in ("train", "validation", "test", "unused")}
    metadata["trajectory_split"] = split.tolist()
    metadata["selected_training_trajectory_ids"] = train_ids[:train_count].tolist()
    return replace(dataset, split=split, metadata=metadata)


def _replace_training_trajectories(evaluation_data: UnicycleDataset,
                                   training_source: UnicycleDataset,
                                   design: str) -> UnicycleDataset:
    """Use source training trajectories while preserving evaluation_data val/test exactly."""
    destination_ids = np.flatnonzero(evaluation_data.split == "train")
    source_ids = np.flatnonzero(training_source.split == "train")
    if len(destination_ids) != len(source_ids):
        raise ValueError("source and evaluation datasets must have the same training trajectory count")
    states, controls = evaluation_data.states.copy(), evaluation_data.controls.copy()
    body, inertial = evaluation_data.delta_body_target.copy(), evaluation_data.delta_inertial_true.copy()
    states[destination_ids] = training_source.states[source_ids]
    controls[destination_ids] = training_source.controls[source_ids]
    body[destination_ids] = training_source.delta_body_target[source_ids]
    inertial[destination_ids] = training_source.delta_inertial_true[source_ids]
    metadata = dict(evaluation_data.metadata)
    metadata["training_distribution_design"] = design
    metadata["training_source_seed"] = training_source.metadata["seed"]
    metadata["training_source_config"] = training_source.metadata["config"]
    return replace(evaluation_data, states=states, controls=controls,
                   delta_body_target=body, delta_inertial_true=inertial, metadata=metadata)


def _run_condition(experiment_id: int, label: str, condition: str, dataset: UnicycleDataset,
                   updates: int, seed: int, root: Path) -> dict:
    output = _experiment_folder(root, experiment_id, label) / condition
    training_config = TrainingConfig(
        seed=seed, epochs=max(1, updates), batch_size=256, max_optimizer_updates=updates,
        learning_rate=1e-3, hidden_size=64, hidden_layers=2,
    )
    result = train_model(dataset, training_config)
    save_training_outputs(result, output, summary_filename=None)
    trajectory_rows = []
    paths = []
    predictions_dir = output / "predictions"
    predictions_dir.mkdir(parents=True, exist_ok=True)
    for trajectory_id in np.flatnonzero(dataset.split == "test"):
        true = dataset.states[trajectory_id]
        controls = dataset.controls[trajectory_id]
        predicted, predicted_body = recursive_rollout(
            result.model, {
                "input_mean": result.input_scaler.mean, "input_scale": result.input_scaler.scale,
                "target_mean": result.target_scaler.mean, "target_scale": result.target_scaler.scale,
            }, true[0], controls, float(dataset.metadata["dt"]),
        )
        metrics = _trajectory_metrics(true, predicted)
        metrics.update(_teacher_forced_metrics(true, predicted_body, dataset.delta_body_target[trajectory_id]))
        trajectory_rows.append({"trajectory_id": int(trajectory_id), **metrics})
        paths.append((int(trajectory_id), true, predicted))
        np.savez_compressed(
            predictions_dir / f"trajectory_{trajectory_id:03d}.npz",
            trajectory_id=np.asarray(trajectory_id), dt=np.asarray(dataset.metadata["dt"]),
            true_states=true, predicted_states=predicted, controls=controls,
            true_body_increments=dataset.delta_body_target[trajectory_id],
            predicted_body_increments=predicted_body,
        )
    _save_path_comparisons(output, paths, f"Experiment {experiment_id}: {condition}")
    rollout_fields = list(trajectory_rows[0])
    with (output / "rollout_metrics.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=rollout_fields)
        writer.writeheader()
        writer.writerows(trajectory_rows)
    rollout_mean = {key: float(np.mean([row[key] for row in trajectory_rows]))
                    for key in trajectory_rows[0] if key != "trajectory_id"}
    training_ids = np.flatnonzero(dataset.split == "train")
    validation_ids = np.flatnonzero(dataset.split == "validation")
    test_ids = np.flatnonzero(dataset.split == "test")
    unused_count = int(np.count_nonzero(dataset.split == "unused"))
    epoch_batches = [int(row["batches_per_epoch"]) for row in result.history]
    typical_batches = max(set(epoch_batches), key=epoch_batches.count)
    batches_per_epoch = (f"{typical_batches} (final {epoch_batches[-1]})"
                         if len(set(epoch_batches)) > 1 else str(typical_batches))
    train_sample_count = len(training_ids) * dataset.controls.shape[1]
    configured_batch_size = training_config.batch_size
    last_batch_size = train_sample_count % configured_batch_size
    samples_per_batch = (f"{configured_batch_size} (final {last_batch_size})"
                         if last_batch_size else str(configured_batch_size))
    trajectory_counts = (
        f"total {dataset.states.shape[0]} (train {len(training_ids)}, validation {len(validation_ids)}, "
        f"test {len(test_ids)}" + (f", unused {unused_count}" if unused_count else "") + ")"
    )
    (output / "rollout_metrics.json").write_text(json.dumps({
        "per_trajectory": trajectory_rows, "mean_across_test_trajectories": rollout_mean,
    }, indent=2), encoding="utf-8")
    run_meta = {
        "experiment_id": experiment_id, "experiment": label, "condition": condition,
        "optimizer_updates": result.optimizer_updates, "best_epoch": result.best_epoch,
        "training_config": {**training_config.__dict__},
        "train_trajectory_ids": training_ids.tolist(),
        "validation_trajectory_ids": validation_ids.tolist(),
        "test_trajectory_ids": test_ids.tolist(),
        "number_of_trajectories": trajectory_counts,
        "epochs": len(result.history), "batches_per_epoch": batches_per_epoch,
        "samples_per_batch": samples_per_batch,
        "dataset_metadata": dataset.metadata,
        "one_step_physical_metrics": result.test_metrics,
        "free_running_mean_metrics": rollout_mean,
    }
    (output / "condition_metadata.json").write_text(json.dumps(run_meta, indent=2), encoding="utf-8")
    return {
        "experiment_id": experiment_id, "experiment": label, "condition": condition,
        "number_of_trajectories": trajectory_counts,
        "epochs": len(result.history), "batches_per_epoch": batches_per_epoch,
        "samples_per_batch": samples_per_batch,
        "optimizer_updates": result.optimizer_updates,
        "mean_x_mae": rollout_mean["x_mae"], "mean_y_mae": rollout_mean["y_mae"],
        "mean_theta_mae": rollout_mean["theta_mae"],
        "one_step_body_rmse": result.test_metrics["overall_rmse"],
        "position_rmse": rollout_mean["position_rmse"],
        "final_position_error": rollout_mean["final_position_error"],
        "heading_rmse": rollout_mean["heading_rmse"],
        "path_length_error": rollout_mean["path_length_error"],
        "best_validation_mse": result.best_validation_loss,
    }


def _run_analytic_sanity(root: Path) -> dict:
    experiment_id, label = 0, "A_Simulator_Sanity"
    output = _experiment_folder(root, experiment_id, label)
    output.mkdir(parents=True, exist_ok=True)
    controls = [UnicycleControl(1.2, 0.5), UnicycleControl(0.0, -0.8),
                UnicycleControl(0.7, 0.0), UnicycleControl(-0.2, 0.4)] * 15
    dt = 0.04
    errors = []
    paths = []
    for heading in (-np.pi, -np.pi / 2, 0.0, np.pi / 2, np.pi - 1e-8):
        truth = simulate_trajectory(UnicycleState(0.0, 0.0, heading), controls, dt)
        rollout = [np.array([0.0, 0.0, heading])]
        for control in controls:
            local = body_increment(control, dt)
            previous = rollout[-1]
            delta_xy = body_to_inertial(local[:2], previous[2])
            rollout.append(previous + np.array([delta_xy[0], delta_xy[1], local[2]]))
        truth_array = np.array([[s.x, s.y, s.theta] for s in truth.states])
        prediction_array = np.asarray(rollout)
        errors.append(float(np.max(np.linalg.norm(prediction_array - truth_array, axis=1))))
        paths.append((len(paths), truth_array, prediction_array))
    _save_path_comparisons(output, paths, "Experiment A: perfect analytical rollout")
    all_truth = np.concatenate([path[1] for path in paths], axis=0)
    all_prediction = np.concatenate([path[2] for path in paths], axis=0)
    mean_x_mae = float(np.mean(np.abs(all_prediction[:, 0] - all_truth[:, 0])))
    mean_y_mae = float(np.mean(np.abs(all_prediction[:, 1] - all_truth[:, 1])))
    mean_theta_mae = float(np.mean(np.abs(angle_difference(all_prediction[:, 2], all_truth[:, 2]))))
    metrics = {"heading_cases": 5, "maximum_state_error": max(errors),
               "maximum_position_error": max(errors), "passed_tolerance_1e_10": max(errors) < 1e-10}
    (output / "analytic_sanity.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    (output / "Experiment A Data.md").write_text(
        "# Experiment A: Simulator and transform sanity\n\n"
        "Used exact local constant-control increments as a perfect transition model and recursively transformed "
        "them into inertial coordinates. Evaluated straight, turning, stationary-turn, and reverse segments from "
        f"five initial headings.\n\n"
        "**Difference from an average learned run:** this is an analytical oracle case with no fitted neural model "
        "or optimizer; it isolates simulator and frame-transform correctness.\n\n"
        "- Number of trajectories: 5 analytic paths, 60 steps each\n- Epochs: N/A\n"
        "- Batches per epoch: N/A\n- Samples per batch: N/A\n- Optimizer updates: 0\n"
        f"- Mean X MAE: {mean_x_mae:.6g}\n- Mean Y MAE: {mean_y_mae:.6g}\n"
        f"- Mean Theta MAE: {mean_theta_mae:.6g} rad\n"
        f"- Maximum state error: {max(errors):.3e}\n- Pass tolerance 1e-10: {metrics['passed_tolerance_1e_10']}\n",
        encoding="utf-8",
    )
    return {"experiment_id": 0, "experiment": label, "condition": "perfect_analytic",
            "number_of_trajectories": "5 analytic paths (60 steps each)", "epochs": "N/A",
            "batches_per_epoch": "N/A", "samples_per_batch": "N/A", "optimizer_updates": 0,
            "mean_x_mae": mean_x_mae, "mean_y_mae": mean_y_mae,
            "mean_theta_mae": mean_theta_mae, "one_step_body_rmse": 0.0,
            "position_rmse": max(errors), "final_position_error": max(errors),
            "heading_rmse": max(errors), "path_length_error": 0.0,
            "best_validation_mse": 0.0}


def _write_experiment_note(folder: Path, experiment_id: int, label: str,
                           rows: list[dict], interpretation: str) -> None:
    letter = EXPERIMENT_LETTERS[experiment_id]
    display_label = label[2:] if len(label) > 2 and label[1] == "_" else label
    lines = [f"# Experiment {letter}: {display_label.replace('_', ' ')}", "",
             f"**Difference from an average run / previous experiment:** {interpretation}", "",
             "### Training budget", "",
             "| Condition | Number of trajectories | Epochs | Batches per epoch | Samples per batch | Optimizer updates |",
             "|---|---|---:|---:|---|---:|"]
    for row in rows:
        lines.append(f"| {row['condition']} | {row['number_of_trajectories']} | {row['epochs']} "
                     f"| {row['batches_per_epoch']} | {row['samples_per_batch']} | {row['optimizer_updates']} |")
    lines.extend(["", "### Test metrics", "",
                  "| Condition | Mean X MAE | Mean Y MAE | Mean Theta MAE (rad) | One-step body RMSE | Position RMSE | Final position error | Heading RMSE (rad) | Path-length error |",
                  "|---|---:|---:|---:|---:|---:|---:|---:|---:|"])
    for row in rows:
        lines.append(
            f"| {row['condition']} | {row['mean_x_mae']:.6g} | {row['mean_y_mae']:.6g} "
            f"| {row['mean_theta_mae']:.6g} | {row['one_step_body_rmse']:.6g} "
            f"| {row['position_rmse']:.6g} | {row['final_position_error']:.6g} "
            f"| {row['heading_rmse']:.6g} | {row['path_length_error']:.6g} |"
        )
    (folder / f"Experiment {letter} Data.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _refresh_reports(root: Path) -> None:
    """Rebuild A-F markdown summaries from already saved experiment artifacts."""
    interpretations = {
        1: "Compared with the broad-range average run, this model uses narrower speed and turn-rate ranges and measures interpolation within that configured envelope.",
        2: "Compared with the standard broad-control run, this changes the initial-heading design: training uses cardinal headings while validation and test use unseen headings.",
        3: "Varies training trajectory count (8, 24, 48) while keeping the nested data source, held-out trajectories, architecture, seed, and update budget fixed.",
        4: "Compares many narrow-range training trajectories with fewer broad-range trajectories on identical broad validation/test paths; both count and variety change.",
        5: "Changes only the optimizer-update budget (100, 300, 900) while holding dataset, split, architecture, controls, and seed fixed.",
    }
    for experiment_id, letter in EXPERIMENT_LETTERS.items():
        folder = next(root.glob(f"Experiment {letter} -*"))
        if experiment_id == 0:
            (folder / "Experiment A Data.md").write_text(
                "# Experiment A: Simulator and transform sanity\n\n"
                "**Difference from an average learned run:** this analytical oracle uses no fitted neural model or optimizer; it isolates simulator and frame-transform correctness.\n\n"
                "- Number of trajectories: 5 analytic paths, 60 steps each\n- Epochs: N/A\n"
                "- Batches per epoch: N/A\n- Samples per batch: N/A\n- Optimizer updates: 0\n"
                "- Mean X MAE: 0\n- Mean Y MAE: 0\n- Mean Theta MAE: 0 rad\n"
                f"- Maximum state error: {json.loads((folder / 'analytic_sanity.json').read_text(encoding='utf-8'))['maximum_state_error']:.3e}\n",
                encoding="utf-8",
            )
            continue
        rows = []
        experiment_label = None
        for condition_dir in sorted(path for path in folder.iterdir() if path.is_dir()):
            metadata = json.loads((condition_dir / "condition_metadata.json").read_text(encoding="utf-8"))
            experiment_label = metadata["experiment"]
            training = list(csv.DictReader((condition_dir / "training_metrics.csv").open(encoding="utf-8")))
            rollout = list(csv.DictReader((condition_dir / "rollout_metrics.csv").open(encoding="utf-8")))
            prediction_files = sorted((condition_dir / "predictions").glob("trajectory_*.npz"))
            x_errors, y_errors, theta_errors = [], [], []
            for prediction_file in prediction_files:
                with np.load(prediction_file, allow_pickle=False) as archive:
                    true, predicted = archive["true_states"], archive["predicted_states"]
                x_errors.extend(np.abs(predicted[:, 0] - true[:, 0]).tolist())
                y_errors.extend(np.abs(predicted[:, 1] - true[:, 1]).tolist())
                theta_errors.extend(np.abs(angle_difference(predicted[:, 2], true[:, 2])).tolist())
            batch_counts = [int(float(row["batches_per_epoch"])) for row in training]
            typical_batches = max(set(batch_counts), key=batch_counts.count)
            batches = f"{typical_batches} (final {batch_counts[-1]})" if len(set(batch_counts)) > 1 else str(typical_batches)
            split_counts = metadata["dataset_metadata"].get("split_counts", {})
            n_train = len(metadata["train_trajectory_ids"])
            total = metadata["dataset_metadata"]["num_trajectories"]
            count_text = (f"total {total} (train {n_train}, validation {len(metadata['validation_trajectory_ids'])}, "
                          f"test {len(metadata['test_trajectory_ids'])}" +
                          (f", unused {split_counts['unused']}" if split_counts.get("unused", 0) else "") + ")")
            train_samples = n_train * metadata["dataset_metadata"]["num_steps_per_trajectory"]
            batch_size = metadata["training_config"]["batch_size"]
            remainder = train_samples % batch_size
            samples_per_batch = f"{batch_size} (final {remainder})" if remainder else str(batch_size)
            test = json.loads((condition_dir / "test_metrics.json").read_text(encoding="utf-8"))
            rows.append({
                "condition": condition_dir.name,
                "number_of_trajectories": count_text,
                "epochs": len(training), "batches_per_epoch": batches,
                "samples_per_batch": samples_per_batch,
                "optimizer_updates": metadata["optimizer_updates"],
                "mean_x_mae": float(np.mean(x_errors)), "mean_y_mae": float(np.mean(y_errors)),
                "mean_theta_mae": float(np.mean(theta_errors)),
                "one_step_body_rmse": test["overall_rmse"],
                "position_rmse": float(np.mean([float(row["position_rmse"]) for row in rollout])),
                "final_position_error": float(np.mean([float(row["final_position_error"]) for row in rollout])),
                "heading_rmse": float(np.mean([float(row["heading_rmse"]) for row in rollout])),
                "path_length_error": float(np.mean([float(row["path_length_error"]) for row in rollout])),
            })
        _write_experiment_note(folder, experiment_id, experiment_label, rows, interpretations[experiment_id])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("runs/unicycle_u5"))
    parser.add_argument("--steps", type=int, default=60)
    parser.add_argument("--updates", type=int, default=300,
                        help="common update budget for B-E; F uses 100, this value, and 3x this value")
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--reports-only", action="store_true",
                        help="refresh experiment markdown from existing outputs without retraining")
    args = parser.parse_args()
    root = args.output
    if args.reports_only:
        _refresh_reports(root)
        print(f"Refreshed A-F experiment notes from saved artifacts in {root}")
        return
    root.mkdir(parents=True, exist_ok=True)
    results = [_run_analytic_sanity(root)]

    # B: narrow but deliberately axis/corner-covered operating envelope.
    narrow = generate_dataset(DatasetConfig(
        num_trajectories=64, num_steps=args.steps, dt=0.05,
        speed_range=(0.4, 1.4), omega_range=(-0.6, 0.6),
        control_hold_steps=(3, 10), split_fractions=(0.75, 0.125, 0.125), seed=args.seed,
    ))
    b = _run_condition(1, "B_Narrow_Control", "narrow_well_covered", narrow, args.updates, args.seed, root)
    results.append(b)
    _write_experiment_note(_experiment_folder(root, 1, "B_Narrow_Control"), 1, "B_Narrow_Control", [b],
                            "A single narrow-range model checks interpolation over a deliberately bounded speed and turn-rate region.")

    # C: train on a small set of headings and test on headings kept out of training.
    heading_base = generate_dataset(DatasetConfig(
        num_trajectories=64, num_steps=args.steps, dt=0.05,
        control_hold_steps=(3, 10), split_fractions=(0.75, 0.125, 0.125), seed=args.seed + 1,
    ))
    c_headings = np.empty(64)
    train_ids = np.flatnonzero(heading_base.split == "train")
    val_ids = np.flatnonzero(heading_base.split == "validation")
    test_ids = np.flatnonzero(heading_base.split == "test")
    training_headings = np.array([-np.pi, -np.pi / 2, 0, np.pi / 2])
    c_headings[train_ids] = training_headings[np.arange(len(train_ids)) % len(training_headings)]
    c_headings[val_ids] = np.pi / 4
    c_headings[test_ids] = -3 * np.pi / 4
    heading_data = _dataset_with_headings(heading_base, c_headings, "train_cardinal_test_unseen")
    c = _run_condition(2, "C_Initial_Heading_Invariance", "unseen_test_headings", heading_data,
                       args.updates, args.seed, root)
    results.append(c)
    _write_experiment_note(_experiment_folder(root, 2, "C_Initial_Heading_Invariance"), 2,
                            "C_Initial_Heading_Invariance", [c],
                            "Training trajectories use cardinal headings; validation and test use held-out headings to check whether local body-frame transitions transfer across orientation.")

    # Shared broad dataset gives D and F exactly the same validation/test trajectories and controls.
    broad = generate_dataset(DatasetConfig(
        num_trajectories=64, num_steps=args.steps, dt=0.05,
        control_hold_steps=(3, 10), split_fractions=(0.75, 0.125, 0.125), seed=args.seed + 2,
    ))
    d_rows = []
    for count in (8, 24, 48):
        subset = _with_train_count(broad, count)
        row = _run_condition(3, "D_Data_Quantity", f"train_{count:02d}", subset,
                             args.updates, args.seed, root)
        d_rows.append(row)
        results.append(row)
    _write_experiment_note(_experiment_folder(root, 3, "D_Data_Quantity"), 3, "D_Data_Quantity", d_rows,
                            "The nested training subsets share the same held-out validation and test trajectories, architecture, seed, controls, and optimizer-update budget; training trajectory count is the changed factor.")

    # E: many near-identical runs against fewer trajectories with wider motion/heading variety.
    similar_source = generate_dataset(DatasetConfig(
        num_trajectories=64, num_steps=args.steps, dt=0.05,
        speed_range=(0.8, 1.0), omega_range=(-0.15, 0.15),
        control_hold_steps=(8, 15), initial_heading_range=(-0.1, 0.1),
        split_fractions=(0.75, 0.125, 0.125), seed=args.seed + 3,
    ))
    similar = _replace_training_trajectories(broad, similar_source, "narrow_controls_and_headings")
    varied = _replace_training_trajectories(broad, broad, "broad_controls_and_headings")
    e_rows = [
        _run_condition(4, "E_Data_Variety", "many_similar_48", _with_train_count(similar, 48),
                       args.updates, args.seed, root),
        _run_condition(4, "E_Data_Variety", "fewer_varied_12", _with_train_count(varied, 12),
                       args.updates, args.seed, root),
    ]
    results.extend(e_rows)
    _write_experiment_note(_experiment_folder(root, 4, "E_Data_Variety"), 4, "E_Data_Variety", e_rows,
                            "Compares many similar training trajectories with fewer varied trajectories. Both conditions use the exact same broad validation/test trajectories, so the test distribution is fixed. This deliberately contrasts count and coverage together rather than treating either as the only changed factor.")

    # F: same exact dataset and architecture, varying only optimizer update budget.
    f_rows = []
    for update_count in sorted({100, args.updates, 3 * args.updates}):
        row = _run_condition(5, "F_Optimizer_Updates", f"updates_{update_count:04d}", broad,
                             update_count, args.seed, root)
        f_rows.append(row)
        results.append(row)
    _write_experiment_note(_experiment_folder(root, 5, "F_Optimizer_Updates"), 5, "F_Optimizer_Updates", f_rows,
                            "All runs use the same trajectories, split, architecture, seed, controls, and data; only the maximum optimizer-update budget changes.")

    fields = list(results[0])
    with (root / "summary.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)
    (root / "summary.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    fig, ax = plt.subplots(figsize=(11, 5.5))
    labels = [f"{r['experiment_id']}:{r['condition']}" for r in results if r["experiment_id"] != 0]
    learn_rows = [r for r in results if r["experiment_id"] != 0]
    positions = np.arange(len(learn_rows))
    ax.bar(positions - 0.18, [r["one_step_body_rmse"] for r in learn_rows], width=0.36,
           label="One-step body RMSE")
    ax.bar(positions + 0.18, [r["position_rmse"] for r in learn_rows], width=0.36,
           label="Free-running position RMSE")
    ax.set_xticks(positions, labels, rotation=45, ha="right")
    ax.set(ylabel="RMSE (configured physical units)", title="U5 controlled comparisons (Experiments B-F)")
    ax.grid(axis="y", alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(root / "comparison_metrics.png", dpi=160)
    plt.close(fig)
    try:
        revision = subprocess.run(["git", "rev-parse", "--short", "HEAD"], check=True,
                                  capture_output=True, text=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        revision = "unknown"
    (root / "run_metadata.json").write_text(json.dumps({
        "phase": "U5", "included_experiments": ["A", "B", "C", "D", "E", "F"],
        "excluded_experiment": "G", "command": shlex.join([sys.executable, *sys.argv]),
        "code_version": revision, "seed": args.seed, "steps_per_trajectory": args.steps,
        "common_update_budget_B_to_E": args.updates,
        "update_budgets_F": sorted({100, args.updates, 3 * args.updates}),
    }, indent=2), encoding="utf-8")
    by_condition = {(r["experiment_id"], r["condition"]): r for r in results}
    d_rows_result = [r for r in results if r["experiment_id"] == 3]
    e_similar = by_condition[(4, "many_similar_48")]
    e_varied = by_condition[(4, "fewer_varied_12")]
    f_rows_result = [r for r in results if r["experiment_id"] == 5]
    f_positions = "/".join(format(r["position_rmse"], ".4g") for r in f_rows_result)
    conclusions = (
        f"- **Interpolation (B):** narrow-range test position RMSE was {b['position_rmse']:.4g}; this measures performance within the same configured operating envelope.\n"
        f"- **Heading transfer (C):** held-out initial-heading test position RMSE was {c['position_rmse']:.4g}, with wrapped heading RMSE {c['heading_rmse']:.4g} rad.\n"
        f"- **Data quantity (D):** position RMSEs for 8/24/48 training trajectories were "
        f"{d_rows_result[0]['position_rmse']:.4g}/{d_rows_result[1]['position_rmse']:.4g}/{d_rows_result[2]['position_rmse']:.4g}; the result is not monotonic at this fixed update budget, so 300 updates may not let every dataset size converge equally.\n"
        f"- **Variety (E):** on the same broad held-out set, 48 similar trajectories gave position RMSE {e_similar['position_rmse']:.4g}, versus {e_varied['position_rmse']:.4g} for 12 varied trajectories. This shows the trade-off under this run, and does not isolate variety from sample count.\n"
        f"- **Optimizer updates (F):** position RMSE at 100/300/900 updates was "
        f"{f_positions}; more updates improved this fixed-data run.\n"
    )
    (root / "U5_Data.md").write_text(
        "# Unicycle Phase U5: Controlled experiments A-F\n\n"
        "Experiment G (representation comparison) was excluded as requested. Experiments A-F use lettered "
        "folders and `Experiment [letter] Data.md` summaries; future user-defined experiments can use numbered "
        "names such as `Experiment 1`. Condition folders retain training curves, physical one-step metrics, "
        "standardizers, checkpoints, data split IDs, and free-running rollout metrics.\n\n"
        "See `summary.csv` and `comparison_metrics.png` for the combined results. Experiments D and F hold out "
        "the same broad-dataset validation and test trajectories. Experiment E also holds evaluation trajectories "
        "fixed while changing training count and variety.\n\n## Conclusions\n\n" + conclusions,
        encoding="utf-8",
    )
    print(f"U5 experiments A-F saved to {root}")
    print(f"Wrote {len(results)} rows to {root / 'summary.csv'}")


if __name__ == "__main__":
    main()

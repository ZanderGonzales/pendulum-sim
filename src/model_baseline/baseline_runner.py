from __future__ import annotations

import csv
from pathlib import Path

import numpy as np

from model_baseline.evaluation import (
    evaluate_trajectory_metrics,
    plot_training_history,
    plot_trajectory_prediction,
)
from model_baseline.experiments import build_baseline_experiment_case
from model_baseline.training import TrajectorySplit, save_checkpoint, train_supervised
from pendulum_sim.data import generate_dataset, save_dataset


def next_run_directory(runs_dir: Path = Path("runs")) -> Path:
    """Return the next monotonically numbered baseline run directory."""
    prefix = "baseline_runs_"
    run_numbers = [
        int(path.name.removeprefix(prefix))
        for path in runs_dir.glob(f"{prefix}*")
        if path.is_dir() and path.name.removeprefix(prefix).isdigit()
    ]
    return runs_dir / f"{prefix}{max(run_numbers, default=-1) + 1}"


def save_test_error_table(
    dataset,
    split: TrajectorySplit,
    result,
    output_path: Path,
) -> None:
    """Save per-trajectory state errors and across-trajectory summaries."""
    metrics = evaluate_trajectory_metrics(
        dataset,
        result.model,
        split.test,
        result.input_scaler,
        result.target_scaler,
    )
    fields = [
        "trajectory",
        "theta0_rad",
        "omega0_rad_per_s",
        "torque_name",
        "torque_parameters",
        "theta_mae_rad",
        "theta_rmse_rad",
        "omega_mae_rad_per_s",
        "omega_rmse_rad_per_s",
    ]
    rows = []
    for item in metrics:
        index = item["trajectory_index"]
        theta0, omega0 = dataset.metadata["initial_conditions"][index]
        torque = dataset.metadata["torque_functions"][index]
        rows.append(
            {
                "trajectory": f"trajectory_{index + 1}",
                "theta0_rad": theta0,
                "omega0_rad_per_s": omega0,
                "torque_name": torque["name"],
                "torque_parameters": str(torque["parameters"]),
                "theta_mae_rad": item["theta_mae"],
                "theta_rmse_rad": item["theta_rmse"],
                "omega_mae_rad_per_s": item["omega_mae"],
                "omega_rmse_rad_per_s": item["omega_rmse"],
            }
        )

    metric_fields = fields[5:]
    for label, function in (
        ("mean", np.mean),
        ("standard_deviation", np.std),
    ):
        summary = {field: float(function([row[field] for row in rows])) for field in metric_fields}
        rows.append({"trajectory": label, **summary})

    with output_path.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def save_experiment_data_note(case: dict, output_dir: Path) -> None:
    """Write a compact description of the generated experiment and outputs."""
    run_number = output_dir.name.removeprefix("baseline_runs_")
    train_configs = case["train_configs"]
    validation_configs = case["validation_configs"]
    test_configs = case["test_configs"]
    theta_values = sorted({config.theta0 for config in train_configs})
    omega_values = sorted({config.omega0 for config in train_configs})
    torque_slopes = sorted(
        {config.torque_parameters["slope"] for config in train_configs}
    )

    def describe_conditions(configs: list) -> str:
        return "; ".join(
            f"(theta0={config.theta0:.2f}, omega0={config.omega0:.2f}, "
            f"slope={config.torque_parameters['slope']:.2f})"
            for config in configs
        )

    params = train_configs[0].params
    lines = [
        f"# Experiment {run_number} Data",
        "",
        "## Dataset",
        "",
        f"- Trajectories: {len(train_configs)} training, "
        f"{len(validation_configs)} validation, {len(test_configs)} test.",
        "- Split unit: complete trajectories.",
        "- Simulation duration: 10 seconds.",
        "- Time step: 0.01 seconds; 1001 samples per trajectory, including the initial state.",
        f"- Physical parameters: mass={params.mass} kg, length={params.length} m, "
        f"gravity={params.gravity} m/s^2, damping={params.damping}.",
        "- Training initial angles (rad): " + ", ".join(f"{value:.4f}" for value in theta_values) + ".",
        "- Training initial angular velocities (rad/s): " + ", ".join(f"{value:.4f}" for value in omega_values) + ".",
        "- Training initial conditions use every angle/velocity pair in the Cartesian product of those values.",
        "- Torque family: linear ramp, tau(t) = slope * t.",
        "- Training torque slopes (N m/s): " + ", ".join(f"{value:.2f}" for value in torque_slopes) + ".",
        "- Validation cases (theta0 rad, omega0 rad/s, slope N m/s): "
        + describe_conditions(validation_configs)
        + ".",
        "- Test cases (theta0 rad, omega0 rad/s, slope N m/s): "
        + describe_conditions(test_configs)
        + ".",
        "- Model inputs: time, initial angle, initial angular velocity, and applied torque; targets: angle and angular velocity.",
        "",
        f"## Changes From Experiment {int(run_number) - 1}",
        "",
        *[f"- {change}" for change in case["changes_from_previous"]],
        "",
        "## Files",
        "",
        "- `simulation_dataset.npz`: all generated trajectories and simulation metadata.",
        "- `baseline_checkpoint.pt`: model checkpoint selected by lowest validation MSE.",
        "- `baseline_learning_curves.png`: training and validation MSE versus epoch.",
        "- `baseline_training_comparison.png`: prediction versus simulator on a validation trajectory.",
        "- `baseline_test_comparison.png`: prediction versus simulator on the preselected first test trajectory.",
        "- `baseline_test_error_data.csv`: per-test-trajectory state errors and aggregate mean/standard deviation.",
        "",
    ]
    (output_dir / f"Experiment {run_number} Data.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def run_baseline_case(
    case: dict,
    *,
    epochs: int = 300,
    learning_rate: float = 1e-3,
    seed: int = 7,
    duration: float = 10.0,
    time_step: float = 0.01,
) -> None:
    num_steps = int(duration / time_step)

    configs = (
        case["train_configs"]
        + case["validation_configs"]
        + case["test_configs"]
    )
    train_count = len(case["train_configs"])
    validation_count = len(case["validation_configs"])
    test_count = len(case["test_configs"])
    dataset = generate_dataset(configs, duration=duration, num_steps=num_steps)
    split = TrajectorySplit(
        train=np.arange(0, train_count, dtype=int),
        validation=np.arange(train_count, train_count + validation_count, dtype=int),
        test=np.arange(train_count + validation_count, len(configs), dtype=int),
    )
    result = train_supervised(
        dataset,
        epochs=epochs,
        learning_rate=learning_rate,
        train_fraction=0.8,
        validation_fraction=0.1,
        seed=seed,
        split=split,
    )

    output_dir = next_run_directory()
    output_dir.mkdir(parents=True, exist_ok=False)
    save_dataset(dataset, output_dir / "simulation_dataset.npz")
    save_checkpoint(result, output_dir / "baseline_checkpoint.pt")
    plot_training_history(
        result.history,
        output_dir / "baseline_learning_curves.png",
    )
    plot_trajectory_prediction(
        dataset,
        result.model,
        int(split.validation[0]),
        result.input_scaler,
        result.target_scaler,
        output_dir / "baseline_training_comparison.png",
    )
    plot_trajectory_prediction(
        dataset,
        result.model,
        int(split.test[0]),
        result.input_scaler,
        result.target_scaler,
        output_dir / "baseline_test_comparison.png",
    )
    save_test_error_table(
        dataset,
        split,
        result,
        output_dir / "baseline_test_error_data.csv",
    )
    save_experiment_data_note(case, output_dir)

    print(f"Run directory: {output_dir}")
    print(
        f"Trajectories: {len(configs)} "
        f"({train_count} train, {validation_count} validation, {test_count} test)"
    )
    print(f"Samples per trajectory: {num_steps + 1}")
    print(f"Best validation MSE: {result.best_validation_loss:.6f} at epoch {result.best_epoch}")
    print("Saved dataset, checkpoint, comparison plots, learning curves, and test error table.")


def main() -> None:
    seed = 7
    case = build_baseline_experiment_case(seed=seed)
    run_baseline_case(case, seed=seed)


if __name__ == "__main__":
    main()

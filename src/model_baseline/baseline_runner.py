from __future__ import annotations

import csv
import argparse
from pathlib import Path

import numpy as np

from model_baseline.evaluation import (
    evaluate_trajectory_metrics,
    plot_training_history,
    plot_trajectory_prediction,
)
from model_baseline.experiments import build_baseline_experiment_case
from model_baseline.training import (
    TrajectorySplit,
    save_checkpoint,
    save_training_log,
    train_supervised,
)
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


def save_experiment_data_note(case: dict, result, output_dir: Path) -> None:
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
        f"- Training configuration: batch_size={result.training_config['batch_size']}, "
        f"max_epochs={result.training_config['max_epochs']}, "
        f"max_optimizer_steps={result.training_config['max_optimizer_steps']}, "
        f"learning_rate={result.training_config['learning_rate']}, "
        f"scheduler=ReduceLROnPlateau(factor={result.training_config['scheduler_factor']}, "
        f"patience={result.training_config['scheduler_patience']}, "
        f"min_lr={result.training_config['min_learning_rate']}).",
        f"- Actual training: {int(result.history['optimizer_step'][-1])} optimizer updates, "
        f"{int(result.history['samples_seen'][-1])} training samples processed.",
        "",
        f"## {case['changes_heading']}",
        "",
        *[f"- {change}" for change in case["changes_from_previous"]],
        "",
        "## Training Procedure",
        "",
        "- Training uses shuffled, non-dropping mini-batches; validation is evaluated in its original order after each epoch.",
        f"- The optimizer-step target was {result.training_config['max_optimizer_steps']}; this run completed "
        f"{int(result.history['optimizer_step'][-1])} updates over {len(result.history['epoch'])} complete epochs, "
        f"processing {int(result.history['samples_seen'][-1])} training samples.",
        "- ReduceLROnPlateau monitors validation MSE once per epoch and applies the configured factor, patience, and minimum learning rate.",
        "",
        "## Files",
        "",
        "- `simulation_dataset.npz`: all generated trajectories and simulation metadata.",
        "- `baseline_checkpoint.pt`: model checkpoint selected by lowest validation MSE.",
        "- `baseline_training_log.csv`: per-epoch update count, samples seen, learning rate, training loss, and validation loss.",
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
    max_epochs: int = 100,
    max_optimizer_steps: int = 5000,
    batch_size: int = 256,
    learning_rate: float = 1e-3,
    scheduler_factor: float = 0.5,
    scheduler_patience: int = 10,
    min_learning_rate: float = 1e-6,
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
        max_epochs=max_epochs,
        max_optimizer_steps=max_optimizer_steps,
        batch_size=batch_size,
        learning_rate=learning_rate,
        scheduler_factor=scheduler_factor,
        scheduler_patience=scheduler_patience,
        min_learning_rate=min_learning_rate,
        train_fraction=0.8,
        validation_fraction=0.1,
        seed=seed,
        split=split,
    )

    output_dir = next_run_directory()
    output_dir.mkdir(parents=True, exist_ok=False)
    save_dataset(dataset, output_dir / "simulation_dataset.npz")
    save_checkpoint(result, output_dir / "baseline_checkpoint.pt")
    save_training_log(result, output_dir / "baseline_training_log.csv")
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
    save_experiment_data_note(case, result, output_dir)

    print(f"Run directory: {output_dir}")
    print(
        f"Trajectories: {len(configs)} "
        f"({train_count} train, {validation_count} validation, {test_count} test)"
    )
    print(f"Samples per trajectory: {num_steps + 1}")
    print(f"Best validation MSE: {result.best_validation_loss:.6f} at epoch {result.best_epoch}")
    print(f"Optimizer updates: {int(result.history['optimizer_step'][-1])}")
    print(f"Training samples seen: {int(result.history['samples_seen'][-1])}")
    print("Saved dataset, checkpoint, comparison plots, learning curves, and test error table.")


def add_training_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--batch-size", type=int, default=256)
    parser.add_argument("--max-epochs", type=int, default=100)
    parser.add_argument("--max-optimizer-steps", type=int, default=5000)
    parser.add_argument("--learning-rate", type=float, default=1e-3)
    parser.add_argument("--scheduler-factor", type=float, default=0.5)
    parser.add_argument("--scheduler-patience", type=int, default=10)
    parser.add_argument("--min-learning-rate", type=float, default=1e-6)


def main() -> None:
    parser = argparse.ArgumentParser(description="Train the baseline pendulum model.")
    add_training_arguments(parser)
    options = parser.parse_args()
    seed = 7
    case = build_baseline_experiment_case(seed=seed)
    run_baseline_case(
        case,
        max_epochs=options.max_epochs,
        max_optimizer_steps=options.max_optimizer_steps,
        batch_size=options.batch_size,
        learning_rate=options.learning_rate,
        scheduler_factor=options.scheduler_factor,
        scheduler_patience=options.scheduler_patience,
        min_learning_rate=options.min_learning_rate,
        seed=seed,
    )


if __name__ == "__main__":
    main()

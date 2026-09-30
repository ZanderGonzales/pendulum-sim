from __future__ import annotations

import json
from itertools import product
import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import torch

from pendulum_sim.data import SimulationConfig, generate_dataset
from model_baseline.evaluation import evaluate_model
from model_baseline.model import PendulumStateNetwork
from pendulum_sim.simulator import PendulumParameters
from model_baseline.training import (
    TrajectorySplit,
    train_supervised,
    tensors_for_trajectories,
)


def _linear_torque_factory(slope: float):
    """Return a linear torque function with the specified slope."""

    def torque_fn(time: float, slope: float = slope) -> float:
        return slope * time

    return torque_fn


def _sinusoidal_torque_factory(amplitude: float, frequency: float):
    """Return a sinusoidal torque function."""

    def torque_fn(time: float, amplitude: float = amplitude, frequency: float = frequency) -> float:
        return amplitude * np.sin(frequency * time)

    return torque_fn


def _build_configs(
    params: PendulumParameters,
    theta_values: list[float],
    omega_values: list[float],
    torque_slopes: list[float],
    torque_name: str = "linear",
) -> list[SimulationConfig]:
    configs: list[SimulationConfig] = []
    for index, (theta0, omega0) in enumerate(zip(theta_values, omega_values)):
        slope = torque_slopes[index % len(torque_slopes)]
        torque_fn = _linear_torque_factory(slope)
        configs.append(
            SimulationConfig(
                theta0=theta0,
                omega0=omega0,
                params=params,
                torque_fn=torque_fn,
                torque_name=torque_name,
                torque_parameters={"slope": slope},
            )
        )
    return configs


def build_experiment_cases() -> list[dict]:
    """Create a small set of data-size and generalization regimes."""
    params = PendulumParameters(mass=1.0, length=1.0, gravity=9.81, damping=0.1)

    small_train = _build_configs(
        params,
        theta_values=[0.15, 0.30, 0.45, 0.60],
        omega_values=[0.10, 0.15, 0.20, 0.25],
        torque_slopes=[0.05, 0.10, 0.15, 0.20],
    )
    large_train = _build_configs(
        params,
        theta_values=[0.05 * i for i in range(1, 10)],
        omega_values=[0.05 * i for i in range(1, 10)],
        torque_slopes=[0.02 * i for i in range(1, 10)],
    )
    held_out_initial = _build_configs(
        params,
        theta_values=[-0.20, -0.10, 0.10, 0.20],
        omega_values=[-0.10, -0.05, 0.05, 0.10],
        torque_slopes=[0.05, 0.08, 0.05, 0.08],
    )
    held_out_torque = _build_configs(
        params,
        theta_values=[0.15, 0.25, 0.35, 0.45],
        omega_values=[0.08, 0.12, 0.18, 0.21],
        torque_slopes=[0.08, 0.12, 0.08, 0.12],
    )

    test_small = _build_configs(
        params,
        theta_values=[0.22, 0.58],
        omega_values=[0.16, 0.23],
        torque_slopes=[0.12, 0.17],
    )
    test_large = _build_configs(
        params,
        theta_values=[0.42, 0.81, 0.90],
        omega_values=[0.18, 0.30, 0.32],
        torque_slopes=[0.09, 0.13, 0.16],
    )
    test_initial = _build_configs(
        params,
        theta_values=[0.55, 0.75],
        omega_values=[0.15, 0.18],
        torque_slopes=[0.10, 0.10],
    )
    test_torque = _build_configs(
        params,
        theta_values=[0.32, 0.60],
        omega_values=[0.10, 0.15],
        torque_slopes=[0.22, 0.28],
    )

    return [
        {
            "name": "small_dataset",
            "description": "Only a small number of trajectories are used for training.",
            "train_configs": small_train,
            "test_configs": test_small,
        },
        {
            "name": "large_dataset",
            "description": "A broader training set covers more trajectory combinations.",
            "train_configs": large_train,
            "test_configs": test_large,
        },
        {
            "name": "held_out_initial_conditions",
            "description": "The test trajectories use initial conditions beyond the training range.",
            "train_configs": held_out_initial,
            "test_configs": test_initial,
        },
        {
            "name": "held_out_torque",
            "description": "The test trajectories use torque levels or trends not seen during training.",
            "train_configs": held_out_torque,
            "test_configs": test_torque,
        },
    ]


def build_data_quantity_cases(
    train_sizes: tuple[int, ...] = (4, 8, 16, 32),
) -> list[dict]:
    """Create nested training sets with identical validation and test conditions."""
    if not train_sizes or any(size <= 0 for size in train_sizes):
        raise ValueError("train_sizes must contain positive trajectory counts")
    if tuple(sorted(set(train_sizes))) != train_sizes:
        raise ValueError("train_sizes must be unique and in increasing order")

    params = PendulumParameters(mass=1.0, length=1.0, gravity=9.81, damping=0.1)
    max_train_size = train_sizes[-1]
    train_pool = _build_configs(
        params,
        theta_values=np.linspace(-0.7, 0.7, max_train_size).tolist(),
        omega_values=np.linspace(-0.4, 0.4, max_train_size).tolist(),
        torque_slopes=[(-0.12, 0.0, 0.12)[index % 3] for index in range(max_train_size)],
    )
    validation_configs = _build_configs(
        params,
        theta_values=[-0.63, -0.21, 0.21, 0.63],
        omega_values=[0.20, -0.20, 0.10, -0.10],
        torque_slopes=[0.07, -0.07, 0.11, -0.11],
    )
    test_configs = _build_configs(
        params,
        theta_values=[-0.50, -0.15, 0.25, 0.55],
        omega_values=[0.13, -0.28, 0.31, -0.08],
        torque_slopes=[0.04, -0.08, 0.10, -0.03],
    )

    return [
        {
            "name": f"{size}_training_trajectories",
            "train_configs": train_pool[:size],
            "validation_configs": validation_configs,
            "test_configs": test_configs,
        }
        for size in train_sizes
    ]


def build_baseline_experiment_case(seed: int = 7) -> dict:
    """Create a baseline case with independent, grid-spread initial conditions."""
    params = PendulumParameters(mass=1.0, length=1.0, gravity=9.81, damping=0.1)
    theta_values = np.linspace(-0.7, 0.7, 8).tolist()
    omega_values = np.linspace(-0.4, 0.4, 4).tolist()
    initial_condition_pairs = list(product(theta_values, omega_values))

    torque_slopes = np.resize(np.asarray([-0.12, 0.0, 0.12]), len(initial_condition_pairs))
    np.random.default_rng(seed).shuffle(torque_slopes)
    train_configs = _build_configs(
        params,
        theta_values=[pair[0] for pair in initial_condition_pairs],
        omega_values=[pair[1] for pair in initial_condition_pairs],
        torque_slopes=[float(slope) for slope in torque_slopes],
    )

    prior_case = build_data_quantity_cases(train_sizes=(32,))[0]
    return {
        "name": "baseline_grid",
        "changes_heading": "Changes From Experiment 0",
        "train_configs": train_configs,
        "validation_configs": prior_case["validation_configs"],
        "test_configs": prior_case["test_configs"],
        "changes_from_previous": [
            "Experiment 0 paired 32 angle values with 32 velocity values by matching list index, so its training conditions followed a single diagonal through the angle/velocity space.",
            "Experiment 1 uses the Cartesian product of 8 angle values and 4 velocity values, giving 32 combinations across the two-dimensional initial-condition space.",
            "The linear torque family and the balanced slope values (-0.12, 0.0, and 0.12 N m/s) are unchanged; Experiment 1 assigns them in a reproducible seeded shuffle instead of the prior cyclic order.",
            "The validation and test conditions, physical parameters, duration, time step, network, epoch count, learning rate, and training seed are unchanged.",
            "The purpose of this change is to test whether broader combinations of initial conditions help the model reproduce trajectories it did not train on.",
        ],
    }


def build_extended_baseline_experiment_case(seed: int = 7) -> dict:
    """Create Experiment 2 with more trajectories and wider initial conditions."""
    params = PendulumParameters(mass=1.0, length=1.0, gravity=9.81, damping=0.1)
    theta_values = np.linspace(-1.4, 1.4, 10).tolist()
    omega_values = np.linspace(-1.0, 1.0, 8).tolist()
    initial_condition_pairs = list(product(theta_values, omega_values))

    torque_slopes = np.resize(np.asarray([-0.12, 0.0, 0.12]), len(initial_condition_pairs))
    np.random.default_rng(seed).shuffle(torque_slopes)
    train_configs = _build_configs(
        params,
        theta_values=[pair[0] for pair in initial_condition_pairs],
        omega_values=[pair[1] for pair in initial_condition_pairs],
        torque_slopes=[float(slope) for slope in torque_slopes],
    )

    experiment_one = build_baseline_experiment_case(seed=seed)
    validation_configs = experiment_one["validation_configs"] + _build_configs(
        params,
        theta_values=[-1.25, -0.95, -0.65, -0.25, 0.35, 1.25],
        omega_values=[0.75, -0.65, 0.85, -0.85, 0.55, -0.55],
        torque_slopes=[0.06, -0.10, 0.02, 0.09, -0.04, 0.12],
    )
    test_configs = experiment_one["test_configs"] + _build_configs(
        params,
        theta_values=[-1.25, -0.95, -0.35, 0.35, 0.95, 1.25],
        omega_values=[0.75, -0.65, 0.85, -0.85, 0.55, -0.55],
        torque_slopes=[0.10, -0.10, 0.08, -0.09, 0.06, -0.11],
    )

    return {
        "name": "baseline_wide_grid",
        "changes_heading": "Changes From Experiment 1",
        "train_configs": train_configs,
        "validation_configs": validation_configs,
        "test_configs": test_configs,
        "changes_from_previous": [
            "Training trajectories increased from 32 to 80; validation and test trajectories increased from 4 each to 10 each.",
            "Training initial angles widened from -0.7 to 0.7 rad to -1.4 to 1.4 rad, and initial angular velocities widened from -0.4 to 0.4 rad/s to -1.0 to 1.0 rad/s.",
            "Training initial conditions use a 10-by-8 Cartesian grid; the linear torque family and balanced slope values are retained.",
            "The first four test trajectories are unchanged from Experiment 1; six additional validation and six additional test conditions cover the wider range.",
            "Physical parameters, duration, time step, model, epoch count, learning rate, and seed are unchanged.",
        ],
    }


def summarize_case_metrics(
    *,
    train_loss: float,
    validation_loss: float,
    mae: float,
    rmse: float,
    max_absolute_error: float,
) -> dict[str, float]:
    """Return a compact dictionary of experiment metrics."""
    return {
        "train_loss": float(train_loss),
        "validation_loss": float(validation_loss),
        "mae": float(mae),
        "rmse": float(rmse),
        "max_absolute_error": float(max_absolute_error),
    }


def evaluate_dataset(
    dataset,
    model: torch.nn.Module,
    input_scaler,
    target_scaler,
    trajectory_indices: np.ndarray | None = None,
) -> dict[str, float]:
    """Evaluate the model across an entire dataset or a selected subset of trajectories."""
    if trajectory_indices is None:
        trajectory_indices = np.arange(dataset.theta.shape[0], dtype=int)

    inputs, targets = tensors_for_trajectories(dataset, np.asarray(trajectory_indices, dtype=int))
    model.eval()
    with torch.no_grad():
        predictions = target_scaler.inverse_transform(model(input_scaler.transform(inputs)))

    absolute_error = (predictions - targets).abs()
    squared_error = (predictions - targets).square()
    return {
        "mae": float(absolute_error.mean().item()),
        "rmse": float(squared_error.mean().sqrt().item()),
        "max_absolute_error": float(absolute_error.max().item()),
    }


def evaluate_errors_over_time(
    dataset,
    model: torch.nn.Module,
    input_scaler,
    target_scaler,
) -> dict[str, list[float]]:
    """Return test-set MAE at each simulation time for both predicted states."""
    trajectory_indices = np.arange(dataset.theta.shape[0], dtype=int)
    inputs, targets = tensors_for_trajectories(dataset, trajectory_indices)
    model.eval()
    with torch.no_grad():
        predictions = target_scaler.inverse_transform(
            model(input_scaler.transform(inputs))
        )

    num_trajectories, num_times = dataset.theta.shape
    errors = (predictions - targets).abs().reshape(num_trajectories, num_times, 2)
    mean_error = errors.mean(dim=0)
    return {
        "angle_mae": mean_error[:, 0].tolist(),
        "angular_velocity_mae": mean_error[:, 1].tolist(),
    }


def plot_data_quantity_error_over_time(
    time: np.ndarray,
    results: list[dict],
    save_path: str | Path,
) -> None:
    """Plot fixed-test-set state error against simulation time for each data size."""
    output = Path(save_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    figure, axes = plt.subplots(2, 1, figsize=(9, 7), sharex=True)
    for result in results:
        errors = result["test_error_over_time"]
        axes[0].plot(time, errors["angle_mae"], label=result["name"])
        axes[1].plot(time, errors["angular_velocity_mae"], label=result["name"])

    axes[0].set_ylabel("Angle MAE (rad)")
    axes[1].set_ylabel("Angular velocity MAE (rad/s)")
    axes[1].set_xlabel("Simulation time (s)")
    for axis in axes:
        axis.grid(True, alpha=0.3)
        axis.legend()
    figure.suptitle("Prediction error over time on the same held-out trajectories")
    figure.tight_layout()
    figure.savefig(output, dpi=200)
    plt.close(figure)


def plot_data_quantity_learning_curves(
    results: list[dict],
    save_path: str | Path,
) -> None:
    """Plot training progress over epochs for each training-set size."""
    output = Path(save_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    figure, axes = plt.subplots(2, 1, figsize=(9, 7), sharex=True)
    for result in results:
        axes[0].plot(result["history"]["train_loss"], label=result["name"])
        axes[1].plot(result["history"]["validation_loss"], label=result["name"])

    axes[0].set_ylabel("Training MSE")
    axes[1].set_ylabel("Validation MSE")
    axes[1].set_xlabel("Training epoch")
    for axis in axes:
        axis.grid(True, alpha=0.3)
        axis.legend()
    figure.suptitle("Learning curves by amount of training data")
    figure.tight_layout()
    figure.savefig(output, dpi=200)
    plt.close(figure)


def run_data_quantity_comparison(
    train_sizes: tuple[int, ...] = (4, 8, 16, 32),
    *,
    duration: float = 2.0,
    num_steps: int = 80,
    max_epochs: int = 100,
    max_optimizer_steps: int = 5000,
    batch_size: int = 256,
    learning_rate: float = 1e-3,
    seed: int = 17,
) -> list[dict]:
    """Compare nested training-set sizes using fixed validation and test trajectories."""
    cases = build_data_quantity_cases(train_sizes)
    test_dataset = generate_dataset(
        cases[0]["test_configs"], duration=duration, num_steps=num_steps
    )
    results: list[dict] = []

    for case in cases:
        num_train = len(case["train_configs"])
        num_validation = len(case["validation_configs"])
        training_dataset = generate_dataset(
            case["train_configs"] + case["validation_configs"],
            duration=duration,
            num_steps=num_steps,
        )
        split = TrajectorySplit(
            train=np.arange(num_train, dtype=int),
            validation=np.arange(num_train, num_train + num_validation, dtype=int),
            test=np.asarray([], dtype=int),
        )
        fit_started = time.perf_counter()
        trained = train_supervised(
            training_dataset,
            max_epochs=max_epochs,
            max_optimizer_steps=max_optimizer_steps,
            batch_size=batch_size,
            learning_rate=learning_rate,
            seed=seed,
            split=split,
        )
        training_seconds = time.perf_counter() - fit_started
        metrics = evaluate_dataset(
            test_dataset,
            trained.model,
            trained.input_scaler,
            trained.target_scaler,
        )
        results.append(
            {
                "name": case["name"],
                "training_trajectories": num_train,
                "validation_trajectories": num_validation,
                "test_trajectories": len(case["test_configs"]),
                "max_epochs": max_epochs,
                "max_optimizer_steps": max_optimizer_steps,
                "batch_size": batch_size,
                "learning_rate": learning_rate,
                "seed": seed,
                "training_seconds": training_seconds,
                "summary": metrics,
                "history": trained.history,
                "test_error_over_time": evaluate_errors_over_time(
                    test_dataset,
                    trained.model,
                    trained.input_scaler,
                    trained.target_scaler,
                ),
            }
        )

    output_dir = Path("runs")
    output_dir.mkdir(parents=True, exist_ok=True)
    summary_path = output_dir / "phase6_matched_data_quantity.json"
    summary_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    plot_data_quantity_error_over_time(
        test_dataset.time,
        results,
        output_dir / "phase6_error_vs_time.png",
    )
    plot_data_quantity_learning_curves(
        results,
        output_dir / "phase6_learning_curves.png",
    )
    return results


def run_experiment_case(
    case: dict,
    *,
    duration: float = 2.0,
    num_steps: int = 80,
    max_epochs: int = 60,
    max_optimizer_steps: int = 5000,
    batch_size: int = 256,
    learning_rate: float = 1e-3,
    seed: int = 7,
) -> dict:
    """Train a model on one regime and evaluate its held-out performance."""
    train_dataset = generate_dataset(case["train_configs"], duration=duration, num_steps=num_steps)
    test_dataset = generate_dataset(case["test_configs"], duration=duration, num_steps=num_steps)
    result = train_supervised(
        train_dataset,
        max_epochs=max_epochs,
        max_optimizer_steps=max_optimizer_steps,
        batch_size=batch_size,
        learning_rate=learning_rate,
        seed=seed,
    )
    metrics = evaluate_dataset(
        test_dataset,
        result.model,
        result.input_scaler,
        result.target_scaler,
    )
    summary = summarize_case_metrics(
        train_loss=result.history["train_loss"][-1],
        validation_loss=result.history["validation_loss"][-1],
        mae=metrics["mae"],
        rmse=metrics["rmse"],
        max_absolute_error=metrics["max_absolute_error"],
    )
    return {
        "name": case["name"],
        "description": case["description"],
        "train_dataset_size": len(train_dataset.theta),
        "test_dataset_size": len(test_dataset.theta),
        "summary": summary,
        "history": result.history,
        "trajectory_split": {
            "train": result.split.train.tolist(),
            "validation": result.split.validation.tolist(),
            "test": result.split.test.tolist(),
        },
    }


def plot_experiment_summary(results: list[dict], save_path: str | Path) -> None:
    """Save a compact comparison of MAE and RMSE across regimes."""
    output = Path(save_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    labels = [entry["name"] for entry in results]
    mae_values = [entry["summary"]["mae"] for entry in results]
    rmse_values = [entry["summary"]["rmse"] for entry in results]

    figure, axis = plt.subplots(figsize=(9, 5))
    x = np.arange(len(labels))
    width = 0.35
    axis.bar(x - width / 2, mae_values, width=width, label="MAE")
    axis.bar(x + width / 2, rmse_values, width=width, label="RMSE")
    axis.set_xticks(x)
    axis.set_xticklabels(labels, rotation=15, ha="right")
    axis.set_ylabel("Error")
    axis.set_title("Pendulum prediction error across experimental regimes")
    axis.grid(True, axis="y", alpha=0.3)
    axis.legend()
    figure.tight_layout()
    figure.savefig(output, dpi=200)
    plt.close(figure)


def run_experiment_suite() -> list[dict]:
    """Run a lightweight experiment sweep and return structured summaries."""
    results = [run_experiment_case(case) for case in build_experiment_cases()]
    summary_path = Path("runs/phase6_experiment_summary.json")
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    plot_experiment_summary(results, "runs/phase6_experiment_summary.png")
    return results

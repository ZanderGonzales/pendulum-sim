from __future__ import annotations

from dataclasses import replace

import numpy as np

from model_baseline.experiments import _sinusoidal_torque_factory, build_baseline_experiment_case
from model_residual.residual_runner import run_residual_case


def replace_with_sinusoidal_torques(case: dict) -> dict:
    """Preserve Run 0 trajectories while replacing their torque inputs."""
    configs = (
        case["train_configs"]
        + case["validation_configs"]
        + case["test_configs"]
    )
    amplitudes = np.linspace(5.0, 10.0, len(configs))
    frequencies = np.linspace(0.0, 2.0 * np.pi, len(configs))
    sinusoidal_configs = []
    for config, amplitude, frequency in zip(configs, amplitudes, frequencies):
        sinusoidal_configs.append(
            replace(
                config,
                torque_fn=_sinusoidal_torque_factory(float(amplitude), float(frequency)),
                torque_name="sinusoidal",
                torque_parameters={
                    "amplitude": float(amplitude),
                    "frequency": float(frequency),
                },
            )
        )

    train_count = len(case["train_configs"])
    validation_count = len(case["validation_configs"])
    return {
        **case,
        "name": "residual_exp_3",
        "train_configs": sinusoidal_configs[:train_count],
        "validation_configs": sinusoidal_configs[train_count : train_count + validation_count],
        "test_configs": sinusoidal_configs[train_count + validation_count :],
        "changes_heading": "Changes From Residual Experiment 0",
        "changes_from_previous": [
            "The training, validation, and test initial conditions use the exact same trajectory split as Residual Experiment 0.",
            "Linear torque ramps were replaced with sinusoidal torques, tau(t) = amplitude * sin(frequency * t).",
            "Torque amplitudes range from 5 to 10 N m and frequencies range from 0 to 2 pi rad/s across the 40 trajectories.",
            "The optimizer budget, model architecture, physical parameters, time step, and training seed are unchanged from Residual Experiment 0.",
        ],
    }


def main() -> None:
    seed = 7
    case = replace_with_sinusoidal_torques(build_baseline_experiment_case(seed=seed))
    run_residual_case(
        case,
        max_epochs=100,
        max_optimizer_steps=20000,
        batch_size=None,
        batches_per_epoch=200,
        learning_rate=1e-3,
        scheduler_factor=0.5,
        scheduler_patience=10,
        min_learning_rate=1e-6,
        seed=seed,
    )


if __name__ == "__main__":
    main()
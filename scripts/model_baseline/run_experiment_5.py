from __future__ import annotations

from model_baseline.baseline_runner import run_baseline_case
from model_baseline.experiments import build_baseline_experiment_case


def main() -> None:
    seed = 7
    case = build_baseline_experiment_case(seed=seed)
    case["name"] = "baseline_200_batches_per_epoch"
    case["changes_heading"] = "Changes From Experiment 4"
    case["changes_from_previous"] = [
        "The training, validation, and test trajectories, model, seed, initial learning rate, scheduler settings, physical parameters, duration, and time step match Experiment 4.",
        "Each epoch uses exactly 200 shuffled, near-equal batches instead of 126 batches of 256 samples. With 32032 training samples, batches contain 160 or 161 samples, and every sample is used exactly once per epoch.",
        "The optimizer-step target increases from 15000 to 20000; the epoch ceiling remains 150. The target is reached exactly after 100 epochs because 200 updates per epoch divides 20000 evenly.",
        "This experiment changes batch organization and update count together, while leaving the dataset and other training settings unchanged.",
    ]
    run_baseline_case(
        case,
        max_epochs=150,
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

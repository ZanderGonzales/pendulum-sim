from __future__ import annotations

from model_baseline.baseline_runner import run_baseline_case
from model_baseline.experiments import build_baseline_experiment_case


def main() -> None:
    seed = 7
    case = build_baseline_experiment_case(seed=seed)
    case["name"] = "baseline_longer_optimization"
    case["changes_heading"] = "Changes From Experiment 3"
    case["changes_from_previous"] = [
        "The training, validation, and test trajectories, model, batch size, initial learning rate, scheduler, physical parameters, duration, time step, and seed match Experiment 3.",
        "The optimizer-step target increases from 5000 to 15000; the epoch ceiling increases from 100 to 150 so the run can reach that target.",
        "The target is checked after each complete epoch. With 126 batches per epoch, this run is expected to stop after 120 epochs and 15120 optimizer updates.",
        "This experiment tests whether additional optimization updates improve validation and test predictions while keeping the training data and batch configuration fixed.",
    ]
    run_baseline_case(
        case,
        max_epochs=150,
        max_optimizer_steps=15000,
        batch_size=256,
        learning_rate=1e-3,
        scheduler_factor=0.5,
        scheduler_patience=10,
        min_learning_rate=1e-6,
        seed=seed,
    )


if __name__ == "__main__":
    main()

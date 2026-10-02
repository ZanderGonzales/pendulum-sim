from __future__ import annotations

from model_baseline.experiments import build_baseline_experiment_case
from model_residual.residual_runner import run_residual_case


def main() -> None:
    seed = 7
    source_case = build_baseline_experiment_case(seed=seed)
    case = {
        "name": "residual_small_data",
        "changes_heading": "Changes From Residual Experiment 1",
        "train_configs": source_case["train_configs"][:24],
        "validation_configs": source_case["validation_configs"][:3],
        "test_configs": source_case["test_configs"][:3],
        "changes_from_previous": [
            "This residual run keeps the same architecture, optimizer schedule, and batch schedule as residual Experiment 1.",
            "The total dataset size is reduced from 40 trajectories to 30 trajectories: 24 training, 3 validation, and 3 test.",
            "The reduced dataset tests how much performance degrades when the residual model sees fewer training trajectories while preserving the same validation/test family.",
        ],
    }
    run_residual_case(
        case,
        max_epochs=10,
        max_optimizer_steps=2000,
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

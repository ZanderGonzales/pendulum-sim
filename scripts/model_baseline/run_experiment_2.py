from __future__ import annotations

import argparse

from model_baseline.baseline_runner import add_training_arguments, run_baseline_case
from model_baseline.experiments import build_extended_baseline_experiment_case


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the 100-trajectory baseline experiment.")
    add_training_arguments(parser)
    options = parser.parse_args()
    seed = 7
    case = build_extended_baseline_experiment_case(seed=seed)
    run_baseline_case(
        case,
        max_epochs=options.max_epochs,
        max_optimizer_steps=options.max_optimizer_steps,
        batch_size=options.batch_size if options.batches_per_epoch is None else None,
        batches_per_epoch=options.batches_per_epoch,
        learning_rate=options.learning_rate,
        scheduler_factor=options.scheduler_factor,
        scheduler_patience=options.scheduler_patience,
        min_learning_rate=options.min_learning_rate,
        seed=seed,
    )


if __name__ == "__main__":
    main()

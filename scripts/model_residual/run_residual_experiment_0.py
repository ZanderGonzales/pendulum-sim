from __future__ import annotations

from model_baseline.experiments import build_baseline_experiment_case
from model_residual.residual_runner import run_residual_case


def main() -> None:
    seed = 7
    case = build_baseline_experiment_case(seed=seed)
    case["name"] = "residual_exp_0"
    case["changes_heading"] = "Changes From Baseline Experiment 5"
    case["changes_from_previous"] = [
        "This residual model uses the exact same training, validation, and test trajectories as the baseline Experiment 5 split.",
        "The only intended change is the residual formulation: the model predicts one-step state increments, not the full next state.",
        "The target optimizer budget is 20000 updates across 100 epochs, using 200 balanced batches per epoch.",
        "This run is meant to be the direct residual comparison against the baseline model run at the same trajectory split.",
    ]
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

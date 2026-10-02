from __future__ import annotations

from model_baseline.experiments import build_baseline_experiment_case
from model_residual.training import residual_train_supervised


def main() -> None:
    seed = 7
    case = build_baseline_experiment_case(seed=seed)
    dataset = __import__("pendulum_sim.data", fromlist=["generate_dataset"]).generate_dataset(
        case["train_configs"] + case["validation_configs"] + case["test_configs"],
        duration=10.0,
        num_steps=1000,
    )
    split = __import__("model_baseline.training", fromlist=["TrajectorySplit"]).TrajectorySplit(
        train=__import__("numpy").arange(0, len(case["train_configs"]), dtype=int),
        validation=__import__("numpy").arange(
            len(case["train_configs"]),
            len(case["train_configs"]) + len(case["validation_configs"]),
            dtype=int,
        ),
        test=__import__("numpy").arange(
            len(case["train_configs"]) + len(case["validation_configs"]),
            len(case["train_configs"]) + len(case["validation_configs"]) + len(case["test_configs"]),
            dtype=int,
        ),
    )
    result = residual_train_supervised(dataset, epochs=10, learning_rate=1e-3, seed=seed, split=split)
    print(f"Best validation MSE: {result.best_validation_loss:.6f} at epoch {result.best_epoch}")


if __name__ == "__main__":
    main()

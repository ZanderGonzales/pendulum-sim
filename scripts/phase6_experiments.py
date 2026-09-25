from __future__ import annotations

from pendulum_sim.experiments import run_experiment_suite


def main() -> None:
    results = run_experiment_suite()

    print("Phase 6 experiment summary")
    print("-" * 80)
    for entry in results:
        print(f"{entry['name']}:")
        print(f"  description: {entry['description']}")
        print(f"  train trajectories: {entry['train_dataset_size']}")
        print(f"  test trajectories: {entry['test_dataset_size']}")
        summary = entry["summary"]
        print(
            "  metrics: "
            f"train_loss={summary['train_loss']:.6f}, "
            f"validation_loss={summary['validation_loss']:.6f}, "
            f"mae={summary['mae']:.6f}, "
            f"rmse={summary['rmse']:.6f}, "
            f"max_error={summary['max_absolute_error']:.6f}"
        )
        print()

    print("Saved experiment summaries to runs/phase6_experiment_summary.json and runs/phase6_experiment_summary.png")


if __name__ == "__main__":
    main()

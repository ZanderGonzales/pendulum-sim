from __future__ import annotations

from model_baseline.experiments import run_data_quantity_comparison


def main() -> None:
    results = run_data_quantity_comparison()

    print("Phase 6: matched training-data quantity comparison")
    print("All runs use the same validation and test trajectories.")
    print("Training trajectories | Test MAE | Test RMSE | Max error | Fit seconds")
    for result in results:
        metrics = result["summary"]
        print(
            f"{result['training_trajectories']:>20} | "
            f"{metrics['mae']:>8.4f} | "
            f"{metrics['rmse']:>9.4f} | "
            f"{metrics['max_absolute_error']:>9.4f} | "
            f"{result['training_seconds']:>11.3f}"
        )

    print("Saved runs/phase6_matched_data_quantity.json")
    print("Saved runs/phase6_error_vs_time.png")
    print("Saved runs/phase6_learning_curves.png")


if __name__ == "__main__":
    main()

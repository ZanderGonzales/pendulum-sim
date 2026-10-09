"""Train the U3 body-frame residual model on a saved U2 dataset."""

import argparse
from pathlib import Path

from model_unicycle_residual import TrainingConfig, save_training_outputs, train_model
from unicycle_sim.dataset import load_dataset


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=Path("runs/unicycle_u2/dataset.npz"))
    parser.add_argument("--output", type=Path, default=Path("runs/unicycle_u3"))
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--epochs", type=int, default=300)
    parser.add_argument("--batch-size", type=int, default=256)
    parser.add_argument("--max-updates", type=int, default=5000)
    parser.add_argument("--learning-rate", type=float, default=1e-3)
    parser.add_argument("--hidden-size", type=int, default=64)
    parser.add_argument("--hidden-layers", type=int, default=2)
    args = parser.parse_args()
    dataset = load_dataset(args.dataset)
    config = TrainingConfig(
        seed=args.seed, epochs=args.epochs, batch_size=args.batch_size,
        max_optimizer_updates=args.max_updates, learning_rate=args.learning_rate,
        hidden_size=args.hidden_size, hidden_layers=args.hidden_layers,
    )
    result = train_model(dataset, config)
    save_training_outputs(result, args.output)
    print(f"Saved U3 run to {args.output}")
    print(f"Optimizer updates: {result.optimizer_updates}; best epoch: {result.best_epoch}")
    print(f"Test physical-unit metrics: {result.test_metrics}")


if __name__ == "__main__":
    main()

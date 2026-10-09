"""Generate a seeded unicycle dataset and a control coverage plot."""

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from unicycle_sim.dataset import DatasetConfig, generate_dataset, save_dataset


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("runs/unicycle_u2/dataset.npz"))
    parser.add_argument("--trajectories", type=int, default=100)
    parser.add_argument("--steps", type=int, default=100)
    parser.add_argument("--dt", type=float, default=0.05)
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--min-speed", type=float, default=0.0)
    parser.add_argument("--max-speed", type=float, default=2.0)
    parser.add_argument("--min-omega", type=float, default=-1.5)
    parser.add_argument("--max-omega", type=float, default=1.5)
    parser.add_argument("--min-hold", type=int, default=5)
    parser.add_argument("--max-hold", type=int, default=20)
    parser.add_argument("--no-boundaries", action="store_true", help="disable injected range-axis/corner controls")
    args = parser.parse_args()

    config = DatasetConfig(
        num_trajectories=args.trajectories, num_steps=args.steps, dt=args.dt,
        speed_range=(args.min_speed, args.max_speed), omega_range=(args.min_omega, args.max_omega),
        control_hold_steps=(args.min_hold, args.max_hold), seed=args.seed,
        include_boundary_controls=not args.no_boundaries,
    )
    dataset = generate_dataset(config)
    save_dataset(dataset, args.output)

    flat_controls = dataset.controls.reshape(-1, 2)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    axes[0].scatter(flat_controls[:, 0], flat_controls[:, 1], s=7, alpha=0.28)
    axes[0].set(xlabel="Forward speed v", ylabel="Turn rate omega (rad/s)", title="Control coverage")
    axes[0].grid(True, alpha=0.25)
    axes[1].hist(flat_controls[:, 0], bins=30, alpha=0.65, label="v")
    axes[1].hist(flat_controls[:, 1], bins=30, alpha=0.65, label="omega")
    axes[1].set(title="Marginal distributions", xlabel="Value", ylabel="Count")
    axes[1].legend()
    fig.tight_layout()
    plot_path = args.output.with_name("control_coverage.png")
    fig.savefig(plot_path, dpi=160)
    plt.close(fig)
    print(f"Saved {args.output}")
    print(f"Saved {plot_path}")
    print(f"Trajectory split counts: {dataset.metadata['split_counts']}")


if __name__ == "__main__":
    main()

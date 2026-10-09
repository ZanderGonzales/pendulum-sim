"""Plot a few exact unicycle paths to inspect the documented sign convention."""

from pathlib import Path
import argparse

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from unicycle_sim import UnicycleControl, UnicycleState, simulate_trajectory


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("runs/unicycle_u1_paths.png"))
    args = parser.parse_args()

    cases = [
        ("straight", UnicycleControl(1.0, 0.0)),
        ("left turn", UnicycleControl(1.0, 0.8)),
        ("right turn", UnicycleControl(1.0, -0.8)),
        ("stationary turn", UnicycleControl(0.0, 0.8)),
    ]
    fig, ax = plt.subplots(figsize=(7, 6))
    for label, control in cases:
        trajectory = simulate_trajectory(UnicycleState(0.0, 0.0, 0.0), [control] * 40, 0.05)
        ax.plot([s.x for s in trajectory.states], [s.y for s in trajectory.states], label=label)
    ax.set(xlabel="Inertial x", ylabel="Inertial y", title="Exact unicycle paths (CCW turn is positive)")
    ax.axis("equal")
    ax.grid(True, alpha=0.3)
    ax.legend()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, dpi=160, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {args.output}")


if __name__ == "__main__":
    main()

"""Plots of real MuJoCo reference flights; no learned predictions in Phase 1."""

from pathlib import Path
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def plot_flight(trajectory, output: Path, family: str) -> None:
    """Plot state, tracking error, and actual applied wrench on one time grid."""
    output.mkdir(parents=True, exist_ok=True)
    states, time = trajectory.states, trajectory.time
    fig, axes = plt.subplots(4, 1, figsize=(10, 11), sharex=True, constrained_layout=True)
    colors = ("tab:blue", "tab:orange", "tab:green")
    for axis, label, color in zip(range(3), ("x", "y", "z"), colors):
        axes[0].plot(time, states[:, axis], color=color, label=f"{label} simulated")
        axes[0].plot(time, trajectory.reference_positions[:, axis], "--", color=color, alpha=.65,
                     label=f"{label} reference")
        axes[1].plot(time, states[:, 7+axis], color=color, label=f"v{label}")
        if len(trajectory.controls):
            axes[3].plot(time[:-1], trajectory.controls[:, 1+axis]*1e6, color=color, label=f"moment {label}")
    axes[2].plot(time, np.linalg.norm(states[:, :3] - trajectory.reference_positions, axis=1), color="tab:red")
    axes[0].set_ylabel("Position [m]")
    axes[1].set_ylabel("Velocity [m/s]")
    axes[2].set_ylabel("Tracking distance [m]")
    axes[3].set(ylabel="Applied moment [micro N m]", xlabel="Time [s]")
    for ax in axes:
        ax.grid(alpha=.25)
    axes[0].legend(ncol=3, fontsize=8)
    axes[1].legend(ncol=3)
    axes[3].legend(ncol=3)
    fig.suptitle(f"Crazyflie reference flight: {family} | {'valid' if trajectory.valid_for_learning else 'rejected'}")
    fig.savefig(output / f"{family}_state_comparison.png", dpi=150)
    plt.close(fig)


def plot_path_summary(trajectories: dict, output: Path) -> None:
    fig = plt.figure(figsize=(14, 8), constrained_layout=True)
    for index, (family, flight) in enumerate(trajectories.items(), start=1):
        ax = fig.add_subplot(2, 3, index, projection="3d")
        ax.plot(*flight.reference_positions.T, "--", color="tab:orange", label="Controller reference")
        ax.plot(*flight.states[:, :3].T, color="tab:blue", label="MuJoCo flight")
        ax.scatter(*flight.states[0, :3], color="black", s=15)
        points = np.vstack((flight.states[:, :3], flight.reference_positions))
        center = (points.max(axis=0) + points.min(axis=0))/2
        half = max(.05, float(np.ptp(points, axis=0).max())/2) * 1.15
        ax.set(xlim=(center[0]-half, center[0]+half), ylim=(center[1]-half, center[1]+half),
               zlim=(center[2]-half, center[2]+half), xlabel="x [m]", ylabel="y [m]", zlabel="z [m]",
               title=family.replace("_", " "))
        ax.set_box_aspect((1, 1, 1))
        ax.legend(fontsize=7, loc="upper left")
    fig.suptitle("Crazyflie Phase 1: six controlled MuJoCo flight families")
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=160)
    plt.close(fig)

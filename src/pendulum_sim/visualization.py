from __future__ import annotations

from pathlib import Path
from typing import Iterable

import matplotlib
matplotlib.use("Agg")
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

from pendulum_sim.simulator import PendulumParameters


def plot_trajectories(
    time: np.ndarray,
    theta: np.ndarray,
    omega: np.ndarray,
    torque: np.ndarray,
    save_path: str | None = None,
) -> None:
    """Create a multi-panel plot of angle, angular velocity, and torque."""
    fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

    axes[0].plot(time, theta, label="theta(t)", color="tab:blue")
    axes[0].set_ylabel("Angle (rad)")
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()

    axes[1].plot(time, omega, label="omega(t)", color="tab:orange")
    axes[1].set_ylabel("Angular velocity (rad/s)")
    axes[1].grid(True, alpha=0.3)
    axes[1].legend()

    axes[2].plot(time, torque, label="tau(t)", color="tab:green")
    axes[2].set_xlabel("Time (s)")
    axes[2].set_ylabel("Torque (N·m)")
    axes[2].grid(True, alpha=0.3)
    axes[2].legend()

    fig.tight_layout()

    if save_path is not None:
        output = Path(save_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output, dpi=200)

    plt.close(fig)


def animate_pendulum(
    time: np.ndarray,
    theta: np.ndarray,
    params: PendulumParameters,
    save_path: str | None = None,
    interval: int = 30,
) -> None:
    """Create a pendulum animation GIF using the simulated angle history."""
    x = params.length * np.sin(theta)
    y = -params.length * np.cos(theta)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(-(params.length + 0.5), params.length + 0.5)
    ax.set_ylim(-(params.length + 0.5), params.length + 0.5)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_facecolor("white")

    pivot, = ax.plot([0], [0], marker="o", markersize=10, color="black")
    rod, = ax.plot([], [], color="black", linewidth=2)
    bob, = ax.plot([], [], marker="o", markersize=12, color="tab:blue")
    time_text = ax.text(0.02, 0.95, "", transform=ax.transAxes, fontsize=10)

    def update(frame: int):
        rod.set_data([0, x[frame]], [0, y[frame]])
        bob.set_data([x[frame]], [y[frame]])
        time_text.set_text(f"t = {time[frame]:.2f} s")
        return rod, bob, time_text

    anim = animation.FuncAnimation(
        fig,
        update,
        frames=len(time),
        interval=interval,
        blit=True,
    )

    if save_path is not None:
        output = Path(save_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        anim.save(output, writer="pillow", fps=30)

    plt.close(fig)

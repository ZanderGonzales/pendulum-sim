from pathlib import Path

import numpy as np

from pendulum_sim.simulator import PendulumParameters, simulate_pendulum
from pendulum_sim.visualization import animate_pendulum, plot_trajectories


def test_plot_trajectories_creates_png(tmp_path: Path) -> None:
    params = PendulumParameters(mass=1.0, length=1.0, gravity=9.81, damping=0.1)
    data = simulate_pendulum(
        duration=1.0,
        num_steps=50,
        theta0=0.3,
        omega0=0.0,
        params=params,
        torque_fn=lambda t: 0.2 * t,
    )

    output_path = tmp_path / "trajectory_plot.png"
    plot_trajectories(
        data["time"],
        data["theta"],
        data["omega"],
        data["torque"],
        save_path=str(output_path),
    )

    assert output_path.exists()
    assert output_path.stat().st_size > 0


def test_animate_pendulum_creates_gif(tmp_path: Path) -> None:
    params = PendulumParameters(mass=1.0, length=1.0, gravity=9.81, damping=0.1)
    data = simulate_pendulum(
        duration=1.0,
        num_steps=50,
        theta0=0.3,
        omega0=0.0,
        params=params,
        torque_fn=lambda t: 0.1 * np.sin(2 * t),
    )

    output_path = tmp_path / "pendulum_animation.gif"
    animate_pendulum(
        data["time"],
        data["theta"],
        params,
        save_path=str(output_path),
    )

    assert output_path.exists()
    assert output_path.stat().st_size > 0

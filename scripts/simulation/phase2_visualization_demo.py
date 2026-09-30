from pendulum_sim.simulator import PendulumParameters, simulate_pendulum
from pendulum_sim.visualization import animate_pendulum, plot_trajectories


def main() -> None:
    params = PendulumParameters(mass=1.0, length=1.0, gravity=9.81, damping=0.1)
    result = simulate_pendulum(
        duration=12.0,
        num_steps=1200,
        theta0=0.5,
        omega0=0.0,
        params=params,
        torque_fn=lambda t: 0.2 * t,
    )

    plot_trajectories(
        result["time"],
        result["theta"],
        result["omega"],
        result["torque"],
        save_path="runs/phase2_trajectory_plot.png",
    )
    animate_pendulum(
        result["time"],
        result["theta"],
        params,
        save_path="runs/phase2_pendulum_animation.gif",
    )

    print("Saved trajectory plot and pendulum animation to runs/")


if __name__ == "__main__":
    main()

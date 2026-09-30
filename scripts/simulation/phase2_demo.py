from pendulum_sim.simulator import PendulumParameters, simulate_pendulum


def main() -> None:
    params = PendulumParameters(mass=1.0, length=1.0, gravity=9.81, damping=0.1)
    result = simulate_pendulum(
        duration=2.0,
        num_steps=200,
        theta0=0.5,
        omega0=0.0,
        params=params,
        torque_fn=lambda t: 0.0,
    )

    print(f"time points: {len(result['time'])}")
    print(f"theta start: {result['theta'][0]:.4f}")
    print(f"theta end: {result['theta'][-1]:.4f}")
    print(f"omega start: {result['omega'][0]:.4f}")
    print(f"omega end: {result['omega'][-1]:.4f}")


if __name__ == "__main__":
    main()

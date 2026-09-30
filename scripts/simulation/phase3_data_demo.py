from pendulum_sim.data import SimulationConfig, generate_dataset, save_dataset
from pendulum_sim.simulator import PendulumParameters


def main() -> None:
    params = PendulumParameters(mass=1.0, length=1.0, gravity=9.81, damping=0.1)
    configs = [
        SimulationConfig(
            theta0=0.2,
            omega0=0.0,
            params=params,
            torque_fn=lambda t: 0.0,
            torque_name="zero",
            torque_parameters={},
        ),
        SimulationConfig(
            theta0=-0.3,
            omega0=0.4,
            params=params,
            torque_fn=lambda t: 0.2 * t,
            torque_name="linear",
            torque_parameters={"slope": 0.2},
        ),
    ]

    dataset = generate_dataset(configs, duration=2.0, num_steps=200)
    path = "data/phase3_example.npz"
    save_dataset(dataset, path)
    inputs, targets = dataset.as_tensors()

    print(f"Saved dataset: {path}")
    print(f"Trajectories: {dataset.theta.shape[0]}")
    print(f"Time samples per trajectory: {dataset.theta.shape[1]}")
    print(f"Model input tensor shape: {tuple(inputs.shape)}")
    print(f"Model target tensor shape: {tuple(targets.shape)}")


if __name__ == "__main__":
    main()

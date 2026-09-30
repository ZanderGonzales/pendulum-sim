import torch

from pendulum_sim.data import SimulationConfig, generate_dataset
from model_baseline.model import PendulumStateNetwork, Standardizer
from pendulum_sim.simulator import PendulumParameters


def main() -> None:
    params = PendulumParameters(mass=1.0, length=1.0, gravity=9.81, damping=0.1)
    config = SimulationConfig(
        theta0=0.2,
        omega0=0.0,
        params=params,
        torque_fn=lambda t: 0.0,
        torque_name="zero",
        torque_parameters={},
    )
    dataset = generate_dataset([config], duration=2.0, num_steps=100)
    inputs, targets = dataset.as_tensors()

    input_scaler = Standardizer.fit(inputs)
    target_scaler = Standardizer.fit(targets)
    model = PendulumStateNetwork()
    predictions = target_scaler.inverse_transform(model(input_scaler.transform(inputs)))

    print(f"Normalized input shape: {tuple(inputs.shape)}")
    print(f"Model output shape: {tuple(predictions.shape)}")
    print(f"First predicted state: {predictions[0].tolist()}")


if __name__ == "__main__":
    main()

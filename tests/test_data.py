import numpy as np
import torch

from pendulum_sim.data import (
    SimulationConfig,
    generate_dataset,
    load_dataset,
    save_dataset,
)
from pendulum_sim.simulator import PendulumParameters


def make_configs() -> list[SimulationConfig]:
    params = PendulumParameters(mass=1.0, length=1.0, gravity=9.81, damping=0.1)
    return [
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


def test_dataset_generation_contains_full_state_and_metadata() -> None:
    dataset = generate_dataset(make_configs(), duration=1.0, num_steps=20)

    assert dataset.time.shape == (21,)
    assert dataset.theta.shape == (2, 21)
    assert dataset.omega.shape == (2, 21)
    assert dataset.torque.shape == (2, 21)
    assert dataset.metadata["torque_functions"][1]["name"] == "linear"


def test_dataset_round_trip_and_tensor_conversion(tmp_path) -> None:
    dataset = generate_dataset(make_configs(), duration=1.0, num_steps=20)
    path = tmp_path / "pendulum_dataset.npz"

    save_dataset(dataset, path)
    loaded = load_dataset(path)
    inputs, targets = loaded.as_tensors()

    assert np.array_equal(loaded.theta, dataset.theta)
    assert loaded.metadata == dataset.metadata
    assert inputs.shape == (42, 4)
    assert targets.shape == (42, 2)
    assert inputs.dtype == torch.float32
    assert targets.dtype == torch.float32

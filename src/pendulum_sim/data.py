from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable, Sequence

import numpy as np
import torch

from pendulum_sim.simulator import PendulumParameters, simulate_pendulum


@dataclass(frozen=True)
class SimulationConfig:
    """Configuration for one trajectory in a shared-grid dataset."""

    theta0: float
    omega0: float
    params: PendulumParameters
    torque_fn: Callable[[float], float]
    torque_name: str
    torque_parameters: dict[str, float]


@dataclass
class SimulationDataset:
    """A batch of simulator trajectories and the metadata that describes them."""

    time: np.ndarray
    torque: np.ndarray
    theta: np.ndarray
    omega: np.ndarray
    metadata: dict

    def as_tensors(self) -> tuple[torch.Tensor, torch.Tensor]:
        """Return flattened model inputs and full-state targets as float32 tensors."""
        num_trajectories, num_times = self.theta.shape
        time = np.broadcast_to(self.time, (num_trajectories, num_times))
        theta0 = np.asarray(self.metadata["initial_conditions"])[:, 0, None]
        omega0 = np.asarray(self.metadata["initial_conditions"])[:, 1, None]

        inputs = np.stack(
            [
                time,
                np.broadcast_to(theta0, time.shape),
                np.broadcast_to(omega0, time.shape),
                self.torque,
            ],
            axis=-1,
        ).reshape(-1, 4)
        targets = np.stack([self.theta, self.omega], axis=-1).reshape(-1, 2)

        return torch.from_numpy(inputs.astype(np.float32)), torch.from_numpy(targets.astype(np.float32))


def generate_dataset(configs: Sequence[SimulationConfig], duration: float, num_steps: int) -> SimulationDataset:
    """Generate a batch of trajectories sharing duration and sampling settings."""
    if not configs:
        raise ValueError("configs must contain at least one simulation")

    results = [
        simulate_pendulum(
            duration=duration,
            num_steps=num_steps,
            theta0=config.theta0,
            omega0=config.omega0,
            params=config.params,
            torque_fn=config.torque_fn,
        )
        for config in configs
    ]

    metadata = {
        "duration": duration,
        "num_steps": num_steps,
        "initial_conditions": [[config.theta0, config.omega0] for config in configs],
        "physical_parameters": [asdict(config.params) for config in configs],
        "torque_functions": [
            {
                "name": config.torque_name,
                "parameters": config.torque_parameters,
            }
            for config in configs
        ],
    }

    return SimulationDataset(
        time=results[0]["time"],
        torque=np.stack([result["torque"] for result in results]),
        theta=np.stack([result["theta"] for result in results]),
        omega=np.stack([result["omega"] for result in results]),
        metadata=metadata,
    )


def save_dataset(dataset: SimulationDataset, path: str | Path) -> None:
    """Save arrays and inspectable JSON metadata in a compressed NumPy archive."""
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        output,
        time=dataset.time,
        torque=dataset.torque,
        theta=dataset.theta,
        omega=dataset.omega,
        metadata_json=json.dumps(dataset.metadata),
    )


def load_dataset(path: str | Path) -> SimulationDataset:
    """Load a dataset previously saved with :func:`save_dataset`."""
    with np.load(path, allow_pickle=False) as archive:
        return SimulationDataset(
            time=archive["time"],
            torque=archive["torque"],
            theta=archive["theta"],
            omega=archive["omega"],
            metadata=json.loads(str(archive["metadata_json"])),
        )

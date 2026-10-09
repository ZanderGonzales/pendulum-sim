"""Seeded piecewise-constant trajectory generation and serialization.

Splits are assigned to whole trajectories. Each saved transition includes the
current/next inertial states, controls, local body target, and inertial delta.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Literal

import numpy as np

from unicycle_sim.dynamics import body_increment, simulate_trajectory
from unicycle_sim.types import UnicycleControl, UnicycleState


@dataclass(frozen=True)
class DatasetConfig:
    num_trajectories: int = 100
    num_steps: int = 100
    dt: float = 0.05
    speed_range: tuple[float, float] = (0.0, 2.0)
    omega_range: tuple[float, float] = (-1.5, 1.5)
    speed_distribution: Literal["uniform"] = "uniform"
    omega_distribution: Literal["uniform"] = "uniform"
    control_hold_steps: tuple[int, int] = (5, 20)
    initial_position_range: tuple[float, float] = (0.0, 0.0)
    initial_heading_range: tuple[float, float] = (-np.pi, np.pi)
    split_fractions: tuple[float, float, float] = (0.75, 0.125, 0.125)
    include_boundary_controls: bool = True
    seed: int = 0

    def __post_init__(self) -> None:
        if self.num_trajectories < 3 or self.num_steps <= 0 or self.dt <= 0:
            raise ValueError("need at least 3 trajectories, positive steps, and positive dt")
        if self.speed_range[0] > self.speed_range[1] or self.omega_range[0] > self.omega_range[1]:
            raise ValueError("control ranges must be ordered")
        if self.control_hold_steps[0] <= 0 or self.control_hold_steps[0] > self.control_hold_steps[1]:
            raise ValueError("control_hold_steps must be an ordered positive range")
        if self.initial_position_range[0] > self.initial_position_range[1]:
            raise ValueError("initial_position_range must be ordered")
        if self.initial_heading_range[0] > self.initial_heading_range[1]:
            raise ValueError("initial_heading_range must be ordered")
        if len(self.split_fractions) != 3 or not np.isclose(sum(self.split_fractions), 1.0):
            raise ValueError("split_fractions must be three values summing to 1")
        if min(self.split_fractions) <= 0:
            raise ValueError("each split must receive a positive fraction")
        if self.speed_distribution != "uniform" or self.omega_distribution != "uniform":
            raise ValueError("only uniform control sampling is currently supported")


@dataclass(frozen=True)
class UnicycleDataset:
    states: np.ndarray  # (trajectories, steps + 1, 3)
    controls: np.ndarray  # (trajectories, steps, 2)
    delta_body_target: np.ndarray  # (trajectories, steps, 3)
    delta_inertial_true: np.ndarray  # (trajectories, steps, 3)
    split: np.ndarray  # (trajectories,), train/validation/test
    metadata: dict

    def __post_init__(self) -> None:
        n, steps_plus_one, state_dim = self.states.shape
        if state_dim != 3 or self.controls.shape != (n, steps_plus_one - 1, 2):
            raise ValueError("states and controls have incompatible schemas")
        expected = (n, steps_plus_one - 1, 3)
        if self.delta_body_target.shape != expected or self.delta_inertial_true.shape != expected:
            raise ValueError("target arrays have incompatible schemas")
        if self.split.shape != (n,):
            raise ValueError("split must contain one label per trajectory")

    def samples(self, split_name: str | None = None) -> dict[str, np.ndarray]:
        """Return flattened transition records, optionally for one trajectory split."""
        trajectory_ids = np.arange(len(self.states))
        if split_name is not None:
            trajectory_ids = trajectory_ids[self.split == split_name]
            if len(trajectory_ids) == 0:
                raise ValueError(f"split {split_name!r} contains no trajectories")
        num_steps = self.controls.shape[1]
        current = self.states[trajectory_ids, :-1]
        following = self.states[trajectory_ids, 1:]
        tids = np.broadcast_to(trajectory_ids[:, None], (len(trajectory_ids), num_steps))
        steps = np.broadcast_to(np.arange(num_steps)[None, :], tids.shape)
        dts = np.full(tids.shape, self.metadata["dt"], dtype=float)
        return {
            "state_current": current.reshape(-1, 3),
            "control_current": self.controls[trajectory_ids].reshape(-1, 2),
            "state_next": following.reshape(-1, 3),
            "delta_body_target": self.delta_body_target[trajectory_ids].reshape(-1, 3),
            "delta_inertial_true": self.delta_inertial_true[trajectory_ids].reshape(-1, 3),
            "trajectory_id": tids.reshape(-1),
            "step_index": steps.reshape(-1),
            "dt": dts.reshape(-1),
        }


def _sample_control(rng: np.random.Generator, config: DatasetConfig) -> UnicycleControl:
    return UnicycleControl(
        float(rng.uniform(*config.speed_range)),
        float(rng.uniform(*config.omega_range)),
    )


def _boundary_controls(config: DatasetConfig) -> tuple[UnicycleControl, ...]:
    """Representative range corners/axes, clipped to configured ranges."""
    v0, v1 = config.speed_range
    w0, w1 = config.omega_range
    vz = float(np.clip(0.0, v0, v1))
    wz = float(np.clip(0.0, w0, w1))
    candidates = [
        (vz, wz), (v0, wz), (v1, wz), (vz, w0), (vz, w1),
        (v0, w0), (v0, w1), (v1, w0), (v1, w1),
    ]
    return tuple(UnicycleControl(v, w) for v, w in dict.fromkeys(candidates))


def generate_dataset(config: DatasetConfig) -> UnicycleDataset:
    """Generate reproducible piecewise-constant trajectories and group splits."""
    rng = np.random.default_rng(config.seed)
    states = np.empty((config.num_trajectories, config.num_steps + 1, 3), dtype=float)
    controls = np.empty((config.num_trajectories, config.num_steps, 2), dtype=float)
    body_targets = np.empty((config.num_trajectories, config.num_steps, 3), dtype=float)
    inertial_deltas = np.empty_like(body_targets)
    boundary = _boundary_controls(config) if config.include_boundary_controls else ()

    for trajectory_id in range(config.num_trajectories):
        x0 = float(rng.uniform(*config.initial_position_range))
        y0 = float(rng.uniform(*config.initial_position_range))
        heading = float(rng.uniform(*config.initial_heading_range))
        initial = UnicycleState(x0, y0, heading)
        control_sequence: list[UnicycleControl] = []
        while len(control_sequence) < config.num_steps:
            if boundary and trajectory_id < len(boundary) and not control_sequence:
                control = boundary[trajectory_id]
            else:
                control = _sample_control(rng, config)
            hold = int(rng.integers(config.control_hold_steps[0], config.control_hold_steps[1] + 1))
            control_sequence.extend([control] * min(hold, config.num_steps - len(control_sequence)))

        trajectory = simulate_trajectory(initial, control_sequence, config.dt)
        states[trajectory_id] = np.array([[s.x, s.y, s.theta] for s in trajectory.states])
        controls[trajectory_id] = np.array([[u.v, u.omega] for u in trajectory.controls])
        for step_index, (state, control) in enumerate(zip(trajectory.states, trajectory.controls)):
            body_targets[trajectory_id, step_index] = body_increment(control, config.dt)
            inertial_deltas[trajectory_id, step_index] = (
                trajectory.states[step_index + 1].x - state.x,
                trajectory.states[step_index + 1].y - state.y,
                trajectory.states[step_index + 1].theta - state.theta,
            )

    permutation = rng.permutation(config.num_trajectories)
    raw_counts = np.asarray(config.split_fractions) * config.num_trajectories
    counts = np.maximum(np.floor(raw_counts).astype(int), 1)
    while counts.sum() > config.num_trajectories:
        reducible = np.flatnonzero(counts > 1)
        counts[reducible[np.argmin(raw_counts[reducible] - counts[reducible])]] -= 1
    for index in np.argsort(-(raw_counts - np.floor(raw_counts))):
        if counts.sum() == config.num_trajectories:
            break
        counts[index] += 1
    n_train, n_val = int(counts[0]), int(counts[1])
    split = np.empty(config.num_trajectories, dtype="U10")
    split[permutation[:n_train]] = "train"
    split[permutation[n_train:n_train + n_val]] = "validation"
    split[permutation[n_train + n_val:]] = "test"

    metadata = {
        "schema_version": 1,
        # JSON-normalize tuples and NumPy scalar defaults for exact round-trips.
        "config": json.loads(json.dumps(asdict(config))),
        "seed": config.seed,
        "dt": config.dt,
        "duration": config.num_steps * config.dt,
        "num_trajectories": config.num_trajectories,
        "num_steps_per_trajectory": config.num_steps,
        "state_order": ["x", "y", "theta"],
        "control_order": ["v", "omega"],
        "delta_body_target_order": ["delta_x_body", "delta_y_body", "delta_theta"],
        "delta_inertial_true_order": ["delta_x", "delta_y", "delta_theta"],
        "units": {"position": "configured distance units", "theta": "radians", "v": "distance/second", "omega": "radians/second"},
        "sampling": {"mode": "piecewise_constant", "speed": config.speed_distribution,
                     "omega": config.omega_distribution, "control_hold_steps": list(config.control_hold_steps),
                     "speed_range": list(config.speed_range), "omega_range": list(config.omega_range),
                     "initial_position_range_per_axis": list(config.initial_position_range),
                     "initial_heading_range": list(config.initial_heading_range),
                     "boundary_controls_injected": len(boundary)},
        "split_counts": {name: int(np.count_nonzero(split == name)) for name in ("train", "validation", "test")},
        "trajectory_split": split.tolist(),
    }
    return UnicycleDataset(states, controls, body_targets, inertial_deltas, split, metadata)


def save_dataset(dataset: UnicycleDataset, path: str | Path) -> None:
    """Write named arrays and JSON metadata into a compressed NPZ archive."""
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        output, states=dataset.states, controls=dataset.controls,
        delta_body_target=dataset.delta_body_target,
        delta_inertial_true=dataset.delta_inertial_true,
        split=dataset.split, metadata_json=np.asarray(json.dumps(dataset.metadata)),
    )


def load_dataset(path: str | Path) -> UnicycleDataset:
    """Load a dataset archive without enabling pickle deserialization."""
    with np.load(Path(path), allow_pickle=False) as archive:
        return UnicycleDataset(
            states=archive["states"], controls=archive["controls"],
            delta_body_target=archive["delta_body_target"],
            delta_inertial_true=archive["delta_inertial_true"],
            split=archive["split"], metadata=json.loads(str(archive["metadata_json"])),
        )

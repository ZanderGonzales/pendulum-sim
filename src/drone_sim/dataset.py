"""Seeded complete-flight datasets, stable trajectory splits, and NPZ storage.

All data remain in physical units. No NN features, residual targets, or fitted
normalizers are introduced here. Future normalizers must use samples('train')
only; benchmark data are stored separately and have no training split.
"""

from collections.abc import Callable
from dataclasses import asdict, dataclass
import json
from pathlib import Path

import numpy as np

from drone_sim.controls import ControllerConfig, FLIGHT_FAMILIES, FlightReference
from drone_sim.dynamics import DroneSimulator
from drone_sim.flight import simulate_flight
from drone_sim.frames import roll_pitch_yaw_quaternion
from drone_sim.types import DroneState, DroneTrajectory, SimulationConfig


SPLIT_CODES = {"train": 0, "validation": 1, "test": 2, "benchmark": 3}
ARRAY_NAMES = ("time", "states", "controls", "requested_controls", "actuator_controls", "contacts",
               "reference_positions", "reference_yaw", "trajectory_ids", "families", "split")


@dataclass(frozen=True)
class DatasetConfig:
    train_count: int = 80
    validation_count: int = 10
    test_count: int = 10
    benchmark_count: int = 10
    held_out_family: str = "waypoints"
    seed: int = 2026
    simulation: SimulationConfig = SimulationConfig()
    controller: ControllerConfig = ControllerConfig()
    horizontal_position_range: tuple = (-.5, .5)
    height_range: tuple = (.8, 1.2)
    yaw_range: tuple = (-np.pi, np.pi)
    motion_scale_range: tuple = (.6, 1.)
    cycles_range: tuple = (.6, 1.)
    initial_tilt_range: tuple = (-.025, .025)
    initial_velocity_range: tuple = (-.03, .03)
    initial_angular_velocity_range: tuple = (-.02, .02)
    max_attempts_per_trajectory: int = 5

    def __post_init__(self):
        for name in ("train_count", "validation_count", "test_count", "benchmark_count", "max_attempts_per_trajectory"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int) or value < 1:
                raise ValueError(f"{name} must be a positive integer")
        if isinstance(self.seed, bool) or not isinstance(self.seed, int) or self.seed < 0:
            raise ValueError("seed must be a nonnegative integer")
        if self.held_out_family not in FLIGHT_FAMILIES:
            raise ValueError(f"held_out_family must be one of {FLIGHT_FAMILIES}")
        for name in ("horizontal_position_range", "height_range", "yaw_range", "motion_scale_range", "cycles_range",
                     "initial_tilt_range", "initial_velocity_range", "initial_angular_velocity_range"):
            bounds = np.asarray(getattr(self, name), dtype=float)
            if bounds.shape != (2,) or not np.isfinite(bounds).all() or bounds[0] > bounds[1]:
                raise ValueError(f"{name} must be an ordered pair of finite values")
        if min(self.motion_scale_range[0], self.cycles_range[0]) <= 0:
            raise ValueError("motion scale and cycle bounds must be positive")

    @property
    def main_families(self) -> tuple:
        return tuple(family for family in FLIGHT_FAMILIES if family != self.held_out_family)


class DatasetGenerationError(RuntimeError):
    def __init__(self, message: str, failures: list):
        super().__init__(message)
        self.failures = failures


@dataclass(frozen=True)
class DroneDataset:
    time: np.ndarray                       # (steps+1,), shared grid in seconds
    states: np.ndarray                     # (trajectories, steps+1, 13)
    controls: np.ndarray                   # (trajectories, steps, 4), actual physical wrench
    requested_controls: np.ndarray
    actuator_controls: np.ndarray
    contacts: np.ndarray
    reference_positions: np.ndarray
    reference_yaw: np.ndarray
    trajectory_ids: np.ndarray             # stable string IDs, independent of dataset size
    families: np.ndarray
    split: np.ndarray
    metadata: dict

    def __post_init__(self):
        if self.metadata.get("schema_version") != 1:
            raise ValueError("unsupported drone dataset schema_version")
        if self.states.ndim != 3 or self.states.shape[2] != 13 or self.states.shape[0] < 1:
            raise ValueError("states must have shape (trajectories, steps+1, 13)")
        n, times, _ = self.states.shape
        shapes = {"time": (times,), "controls": (n, times-1, 4), "requested_controls": (n, times-1, 4),
                  "actuator_controls": (n, times-1, 4), "contacts": (n, times-1),
                  "reference_positions": (n, times, 3), "reference_yaw": (n, times),
                  "trajectory_ids": (n,), "families": (n,), "split": (n,)}
        for name, shape in shapes.items():
            if getattr(self, name).shape != shape:
                raise ValueError(f"{name} must have shape {shape}")
        for name in ("time", "states", "controls", "requested_controls", "actuator_controls", "reference_positions", "reference_yaw"):
            if not np.isfinite(getattr(self, name)).all():
                raise ValueError(f"{name} must be finite")
        dt = self.metadata.get("dt", 0.)
        if times < 2 or not np.isfinite(dt) or dt <= 0 or not np.allclose(self.time, np.arange(times)*dt, rtol=0, atol=1e-9):
            raise ValueError("time must match the complete shared fixed-step grid")
        if self.contacts.dtype.kind != "b" or self.contacts.any():
            raise ValueError("learning datasets must contain only contact-free trajectories")
        if not np.allclose(np.linalg.norm(self.states[:, :, 3:7], axis=-1), 1., rtol=0, atol=1e-8):
            raise ValueError("saved orientations must be normalized wxyz quaternions")
        for name in ("trajectory_ids", "families", "split"):
            if getattr(self, name).dtype.kind != "U":
                raise ValueError(f"{name} must contain Unicode strings")
        if len(np.unique(self.trajectory_ids)) != n:
            raise ValueError("trajectory IDs must be unique; a trajectory cannot appear in multiple splits")
        labels = set(self.split.tolist())
        if not labels <= set(SPLIT_CODES) or ("benchmark" in labels and labels != {"benchmark"}):
            raise ValueError("benchmark trajectories must be kept separate from train/validation/test")
        held_out = self.metadata["held_out_family"]
        if labels == {"benchmark"}:
            if set(self.families.tolist()) != {held_out}:
                raise ValueError("benchmark must contain only the held-out family")
        elif held_out in self.families or not set(self.families.tolist()) <= set(FLIGHT_FAMILIES):
            raise ValueError("main dataset must exclude the held-out family")
        records = self.metadata.get("trajectories", [])
        if len(records) != n or [row["trajectory_id"] for row in records] != self.trajectory_ids.tolist():
            raise ValueError("trajectory metadata must match saved trajectory IDs in order")
        for row, label, family in zip(records, self.split, self.families):
            if row["split"] != label or row["family"] != family or not row["valid_for_learning"]:
                raise ValueError("trajectory metadata has invalid split, family, or validity")
        simulation = self.metadata["simulation"]
        gears = np.asarray(simulation["actuator_gears"])
        limits = np.asarray(simulation["actuator_ctrlrange"])
        if np.any(self.actuator_controls < limits[:, 0]-1e-12) or np.any(self.actuator_controls > limits[:, 1]+1e-12):
            raise ValueError("actuator controls exceed recorded limits")
        if not np.allclose(self.controls, self.actuator_controls*gears, rtol=0, atol=1e-12):
            raise ValueError("applied physical controls do not match actuator controls and gears")

    def samples(self, split_name: str) -> dict:
        """Expose transitions from one explicit split, retaining flight/step IDs."""
        selected = np.flatnonzero(self.split == split_name)
        if len(selected) == 0:
            raise ValueError(f"dataset has no trajectories in split {split_name!r}")
        steps = self.controls.shape[1]
        return {"state_current": self.states[selected, :-1].reshape(-1, 13),
                "state_next": self.states[selected, 1:].reshape(-1, 13),
                "control_current": self.controls[selected].reshape(-1, 4),
                "trajectory_id": np.repeat(self.trajectory_ids[selected], steps),
                "step_index": np.tile(np.arange(steps), len(selected)),
                "dt": np.full(len(selected)*steps, self.metadata["dt"])}

    def trajectory(self, index: int) -> DroneTrajectory:
        if not 0 <= index < len(self.trajectory_ids):
            raise IndexError("trajectory index out of range")
        return DroneTrajectory(self.states[index], self.requested_controls[index], self.controls[index],
                               self.actuator_controls[index], self.time, self.contacts[index],
                               self.reference_positions[index], self.reference_yaw[index],
                               self.metadata["trajectories"][index].copy())


def _trajectory_seed(root_seed: int, split: str, index: int, attempt: int) -> int:
    words = np.random.SeedSequence([root_seed, SPLIT_CODES[split], index, attempt]).generate_state(4)
    return sum(int(word) << (32*i) for i, word in enumerate(words))


def _generate(config: DatasetConfig, split_names: tuple, progress: Callable | None) -> DroneDataset:
    simulator = DroneSimulator(config.simulation)
    flights, ids, labels, families, failures = [], [], [], [], []
    for label in split_names:
        count = getattr(config, f"{label}_count")
        pool = (config.held_out_family,) if label == "benchmark" else config.main_families
        # One stable family permutation per split, then cycle it. Extending a
        # split preserves its earlier flights and approximately balances families.
        order = np.random.default_rng(np.random.SeedSequence([config.seed, SPLIT_CODES[label], 999])).permutation(pool)
        for index in range(count):
            family = str(order[index % len(order)])
            trajectory_id = f"{label}_{index:06d}"
            for attempt in range(config.max_attempts_per_trajectory):
                seed = _trajectory_seed(config.seed, label, index, attempt)
                rng = np.random.default_rng(seed)
                origin = (*rng.uniform(*config.horizontal_position_range, size=2), rng.uniform(*config.height_range))
                yaw = float(rng.uniform(*config.yaw_range))
                reference = FlightReference(family, config.simulation.duration, seed, origin=origin, yaw_offset=yaw,
                                            motion_scale=float(rng.uniform(*config.motion_scale_range)),
                                            cycles=float(rng.uniform(*config.cycles_range)))
                roll, pitch = rng.uniform(*config.initial_tilt_range, size=2)
                initial = DroneState(origin, roll_pitch_yaw_quaternion(roll, pitch, yaw),
                                     rng.uniform(*config.initial_velocity_range, size=3),
                                     rng.uniform(*config.initial_angular_velocity_range, size=3))
                flight = simulate_flight(simulator, reference, config.controller, initial)
                flight.metadata.update({"trajectory_id": trajectory_id, "split": label, "attempt": attempt,
                                        "valid_for_learning": flight.valid_for_learning,
                                        "failure_reason": flight.failure_reason})
                complete = len(flight.controls) == config.simulation.num_steps
                if flight.valid_for_learning and complete:
                    flights.append(flight)
                    ids.append(trajectory_id)
                    labels.append(label)
                    families.append(family)
                    if progress is not None:
                        progress({"trajectory_id": trajectory_id, "family": family, "accepted": True,
                                  "completed": len(flights), "attempt": attempt})
                    break
                failure = {"trajectory_id": trajectory_id, "split": label, "family": family, "attempt": attempt,
                           "seed": seed, "failure_reason": flight.failure_reason or "incomplete trajectory",
                           "completed_steps": len(flight.controls), "initial_state": initial.as_array().tolist(),
                           "reference_parameters": reference.parameters()}
                failures.append(failure)
                if progress is not None:
                    progress({**failure, "accepted": False})
            else:
                raise DatasetGenerationError(f"Could not collect {trajectory_id} after {config.max_attempts_per_trajectory} attempts", failures)
    simulation = simulator.metadata()
    metadata = {"schema_version": 1, "dataset_kind": "held_out_family_benchmark" if split_names == ("benchmark",) else "main",
                "dt": config.simulation.dt, "duration": config.simulation.duration,
                "state_order": simulation["state_order"], "control_order": simulation["control_order"],
                "held_out_family": config.held_out_family, "main_families": list(config.main_families),
                "config": json.loads(json.dumps(asdict(config))), "simulation": simulation,
                "seed_policy": "SeedSequence([root_seed, split_code, within_split_index, attempt]); 128-bit derived seed",
                "split_codes": SPLIT_CODES, "split_counts": {label: labels.count(label) for label in split_names},
                "trajectories": [flight.metadata for flight in flights], "failed_trajectories": failures,
                "normalization": "physical units; fit later NN feature/target normalizers on train trajectories only"}
    return DroneDataset(np.arange(config.simulation.num_steps+1)*config.simulation.dt,
                        np.stack([f.states for f in flights]), np.stack([f.controls for f in flights]),
                        np.stack([f.requested_controls for f in flights]), np.stack([f.actuator_controls for f in flights]),
                        np.stack([f.contacts for f in flights]), np.stack([f.reference_positions for f in flights]),
                        np.stack([f.reference_yaw for f in flights]), np.asarray(ids), np.asarray(families), np.asarray(labels), metadata)


def generate_dataset(config: DatasetConfig = DatasetConfig(), progress: Callable | None = None) -> DroneDataset:
    return _generate(config, ("train", "validation", "test"), progress)


def generate_benchmark_dataset(config: DatasetConfig = DatasetConfig(), progress: Callable | None = None) -> DroneDataset:
    return _generate(config, ("benchmark",), progress)


def save_dataset(dataset: DroneDataset, path: str | Path) -> None:
    path = Path(path)
    if path.suffix.lower() != ".npz":
        raise ValueError("dataset path must end in .npz")
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(path, **{name: getattr(dataset, name) for name in ARRAY_NAMES},
                        metadata_json=json.dumps(dataset.metadata))


def load_dataset(path: str | Path) -> DroneDataset:
    with np.load(path, allow_pickle=False) as archive:
        required = set(ARRAY_NAMES) | {"metadata_json"}
        if not required <= set(archive.files):
            raise ValueError(f"dataset is missing arrays: {sorted(required-set(archive.files))}")
        metadata = json.loads(str(archive["metadata_json"].item()))
        if not isinstance(metadata, dict):
            raise ValueError("dataset metadata must be a JSON object")
        return DroneDataset(**{name: archive[name] for name in ARRAY_NAMES}, metadata=metadata)


def export_trajectory(dataset: DroneDataset, index: int, path: str | Path) -> None:
    """Export the existing single-flight NPZ schema for the playback script."""
    flight = dataset.trajectory(index)
    path = Path(path)
    if path.suffix.lower() != ".npz":
        raise ValueError("flight path must end in .npz")
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(path, time=flight.time, states=flight.states, controls=flight.controls,
                        requested_controls=flight.requested_controls, actuator_controls=flight.actuator_controls,
                        contacts=flight.contacts, reference_positions=flight.reference_positions,
                        reference_yaw=flight.reference_yaw, metadata_json=json.dumps(flight.metadata))


def dataset_summary(dataset: DroneDataset) -> dict:
    """Physical-unit coverage and counts, never fitted NN normalization values."""
    result = {}
    for label in dict.fromkeys(dataset.split.tolist()):
        mask = dataset.split == label
        states, controls = dataset.states[mask], dataset.controls[mask]
        saturated = np.any(np.abs(controls-dataset.requested_controls[mask]) > 1e-12, axis=-1)
        result[label] = {"trajectories": int(mask.sum()), "transitions": int(mask.sum()*dataset.controls.shape[1]),
                         "family_counts": {f: int(np.count_nonzero(dataset.families[mask] == f)) for f in FLIGHT_FAMILIES},
                         "state_min": states.min(axis=(0, 1)).tolist(), "state_max": states.max(axis=(0, 1)).tolist(),
                         "control_min": controls.min(axis=(0, 1)).tolist(), "control_max": controls.max(axis=(0, 1)).tolist(),
                         "saturated_transition_fraction": float(saturated.mean())}
    return result

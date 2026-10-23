"""Controlled drone training designs, fixed flight selection, and sample reuse."""

from collections import Counter
from dataclasses import asdict, dataclass, fields, replace
import copy

import numpy as np

from drone_sim.dataset import ARRAY_NAMES, DroneDataset
from model_drone_residual.training import ResidualSamples


EXPERIMENT_NAMES = {
    "A": "Trajectory Quantity", "B": "Trajectory Variety", "C": "Optimizer Updates",
    "D": "Neural Network Size", "E": "Refresh Frequency",
}
REFRESH_INTERVALS = (None, 1, 5, 10, 25, 50, 100, 200, 500)


@dataclass(frozen=True)
class ExperimentCase:
    name: str
    label: str
    train_count: int = 80
    requested_updates: int = 10000
    hidden_size: int = 64
    hidden_layers: int = 2
    restricted_families: tuple = ()


def experiment_designs():
    """Identical baseline conditions share training, never different seeds."""
    cases = [ExperimentCase(f"broad_{n}", f"{n} broad trajectories", train_count=n) for n in (10, 20, 40, 80)]
    cases += [ExperimentCase("restricted_20", "20 restricted trajectories", train_count=20,
                             restricted_families=("circle", "figure_eight"))]
    cases += [ExperimentCase(f"updates_{n}", f"{n:,} requested optimizer updates", requested_updates=n)
              for n in (5000, 15000, 20000)]
    cases += [ExperimentCase(f"layers_{depth}_width_{width}", f"{depth} hidden layers x {width} neurons",
                             hidden_size=width, hidden_layers=depth)
              for depth, width in ((2, 32), (2, 128), (1, 64), (4, 64))]
    groups = {"A": [f"broad_{n}" for n in (10, 20, 40, 80)],
              "B": ["restricted_20", "broad_20"],
              "C": ["updates_5000", "broad_80", "updates_15000", "updates_20000"],
              "D": ["layers_2_width_32", "broad_80", "layers_2_width_128", "layers_1_width_64", "layers_4_width_64"]}
    return {case.name: case for case in cases}, groups


def training_indices(dataset: DroneDataset, case: ExperimentCase) -> np.ndarray:
    available = np.flatnonzero(dataset.split == "train")
    if case.restricted_families:
        if case.train_count % len(case.restricted_families):
            raise ValueError("restricted training count must balance the selected families")
        count = case.train_count//len(case.restricted_families)
        chosen = []
        for family in case.restricted_families:
            pool = available[dataset.families[available] == family]
            if len(pool) < count:
                raise ValueError(f"insufficient training trajectories for family {family}")
            chosen.extend(pool[:count])
        return np.array(sorted(chosen), dtype=int)
    if len(available) < case.train_count:
        raise ValueError("insufficient training trajectories")
    # The phase-2 generator cycles a fixed family permutation. Prefixes are
    # nested and balanced, without any accuracy-based or seed-based selection.
    return available[:case.train_count]


def select_training_dataset(dataset: DroneDataset, case: ExperimentCase) -> DroneDataset:
    chosen = training_indices(dataset, case)
    held_out = np.flatnonzero(dataset.split != "train")
    indices = np.sort(np.concatenate((chosen, held_out)))
    metadata = copy.deepcopy(dataset.metadata)
    metadata["trajectories"] = [metadata["trajectories"][i] for i in indices]
    metadata["split_counts"] = dict(Counter(dataset.split[indices].tolist()))
    metadata["config"]["train_count"] = case.train_count
    metadata["experiment_training_selection"] = {
        **asdict(case), "trajectory_ids": dataset.trajectory_ids[chosen].tolist(),
        "family_counts": dict(Counter(dataset.families[chosen].tolist())),
        "source_training_pool_count": int(np.count_nonzero(dataset.split == "train")),
        "rule": "fixed source-order prefix per selected family" if case.restricted_families else "fixed source-order prefix",
    }
    arrays = {name: getattr(dataset, name)[indices].copy() for name in ARRAY_NAMES if name != "time"}
    return DroneDataset(time=dataset.time.copy(), metadata=metadata, **arrays)


def select_prepared_samples(source: ResidualSamples, trajectory_ids) -> ResidualSamples:
    mask = np.isin(source.trajectory_ids, trajectory_ids)
    if set(source.trajectory_ids[mask].tolist()) != set(trajectory_ids):
        raise ValueError("cached samples do not contain the selected training trajectories")
    return replace(source, **{field.name: getattr(source, field.name)[mask]
                              for field in fields(source) if field.name != "split"})


def percent_reduction(candidate: float, reference: float) -> float | None:
    """Positive means less error; a zero-error reference has no percent ratio."""
    if not np.isfinite((candidate, reference)).all() or candidate < 0 or reference < 0:
        raise ValueError("errors must be finite and nonnegative")
    return 100*(1-candidate/reference) if reference > 0 else None

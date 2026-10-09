import numpy as np

from unicycle_sim.dataset import DatasetConfig, generate_dataset, load_dataset, save_dataset


def small_config(seed=12):
    return DatasetConfig(
        num_trajectories=12, num_steps=17, dt=0.1,
        speed_range=(0.0, 2.0), omega_range=(-1.0, 1.0),
        control_hold_steps=(2, 4), seed=seed,
    )


def test_seed_reproduces_arrays_and_other_seed_changes_data():
    first = generate_dataset(small_config())
    same = generate_dataset(small_config())
    different = generate_dataset(small_config(seed=13))
    assert np.array_equal(first.controls, same.controls)
    assert np.array_equal(first.states, same.states)
    assert np.array_equal(first.split, same.split)
    assert not np.array_equal(first.controls, different.controls)


def test_boundaries_appear_and_splits_are_complete_trajectory_groups():
    dataset = generate_dataset(small_config())
    flat = dataset.controls.reshape(-1, 2)
    assert np.any(np.all(flat == [0.0, 0.0], axis=1))
    assert np.any(np.all(flat == [2.0, 0.0], axis=1))
    assert np.any(np.all(flat == [0.0, -1.0], axis=1))
    assert set(dataset.split) == {"train", "validation", "test"}
    for label in ("train", "validation", "test"):
        records = dataset.samples(label)
        assert set(records["trajectory_id"]) == set(np.flatnonzero(dataset.split == label))
    split_trajectory_ids = [set(np.flatnonzero(dataset.split == label)) for label in ("train", "validation", "test")]
    assert not (split_trajectory_ids[0] & split_trajectory_ids[1])
    assert not (split_trajectory_ids[0] & split_trajectory_ids[2])
    assert not (split_trajectory_ids[1] & split_trajectory_ids[2])


def test_transition_schema_metadata_and_round_trip(tmp_path):
    dataset = generate_dataset(small_config())
    records = dataset.samples()
    total = 12 * 17
    assert records["state_current"].shape == (total, 3)
    assert records["control_current"].shape == (total, 2)
    assert records["delta_body_target"].shape == (total, 3)
    assert records["dt"].shape == (total,)
    assert dataset.metadata["state_order"] == ["x", "y", "theta"]
    assert sum(dataset.metadata["split_counts"].values()) == 12
    path = tmp_path / "data.npz"
    save_dataset(dataset, path)
    restored = load_dataset(path)
    assert restored.metadata == dataset.metadata
    assert np.array_equal(restored.states, dataset.states)
    assert np.array_equal(restored.controls, dataset.controls)
    assert np.array_equal(restored.delta_body_target, dataset.delta_body_target)

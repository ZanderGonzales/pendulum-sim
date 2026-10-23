"""Dataset isolation, reproducibility, alignment, validation, and flight export."""

from dataclasses import replace
import json

import numpy as np
import pytest

from drone_sim import DroneControl, DroneSimulator, DroneState, FlightReference, SimulationConfig, simulate_flight
from drone_sim.artifacts import next_run
from drone_sim.dataset import (DatasetConfig, DatasetGenerationError, dataset_summary, export_trajectory,
                               generate_benchmark_dataset, generate_dataset, load_dataset, save_dataset)
from drone_sim.frames import roll_pitch_yaw_quaternion, rotation_matrix
from drone_sim.playback import load_flight


@pytest.fixture(scope="module")
def config():
    return DatasetConfig(train_count=3, validation_count=2, test_count=2, benchmark_count=2,
                         simulation=SimulationConfig(duration=.1))


@pytest.fixture(scope="module")
def dataset(config):
    return generate_dataset(config)


@pytest.fixture(scope="module")
def benchmark(config):
    return generate_benchmark_dataset(config)


def test_default_counts_and_separate_family_policy():
    config = DatasetConfig()
    assert (config.train_count, config.validation_count, config.test_count, config.benchmark_count) == (80, 10, 10, 10)
    assert config.held_out_family == "waypoints"
    assert "waypoints" not in config.main_families
    assert len(config.main_families) == 5


def test_complete_shapes_split_ids_and_one_step_alignment(dataset, config):
    assert dataset.states.shape == (7, 11, 13)
    assert dataset.controls.shape == (7, 10, 4)
    assert dataset.metadata["split_counts"] == {"train": 3, "validation": 2, "test": 2}
    assert len(np.unique(dataset.trajectory_ids)) == 7
    assert not dataset.contacts.any()
    samples = dataset.samples("train")
    assert samples["state_current"].shape == (30, 13)
    assert samples["control_current"].shape == (30, 4)
    for sample_index in (0, 9, 10, 29):
        trajectory_id = samples["trajectory_id"][sample_index]
        index = int(np.flatnonzero(dataset.trajectory_ids == trajectory_id)[0])
        step = samples["step_index"][sample_index]
        np.testing.assert_array_equal(samples["state_current"][sample_index], dataset.states[index, step])
        np.testing.assert_array_equal(samples["state_next"][sample_index], dataset.states[index, step+1])
        np.testing.assert_array_equal(samples["control_current"][sample_index], dataset.controls[index, step])
    np.testing.assert_array_equal(samples["dt"], config.simulation.dt)
    assert set(samples["trajectory_id"]) == set(dataset.trajectory_ids[dataset.split == "train"])
    assert not set(samples["trajectory_id"]) & set(dataset.trajectory_ids[dataset.split == "test"])


def test_benchmark_has_no_training_data_or_main_family_overlap(dataset, benchmark):
    assert set(benchmark.split) == {"benchmark"}
    assert set(benchmark.families) == {"waypoints"}
    assert "waypoints" not in dataset.families
    assert not set(dataset.trajectory_ids) & set(benchmark.trajectory_ids)
    with pytest.raises(ValueError, match="no trajectories"):
        benchmark.samples("train")


def test_round_trip_preserves_every_saved_array_and_metadata(tmp_path, dataset, benchmark):
    from drone_sim.dataset import ARRAY_NAMES
    for name, source in (("dataset", dataset), ("benchmark", benchmark)):
        path = tmp_path / f"{name}.npz"
        save_dataset(source, path)
        loaded = load_dataset(path)
        for field in ARRAY_NAMES:
            np.testing.assert_array_equal(getattr(source, field), getattr(loaded, field))
        assert loaded.metadata == source.metadata
    with pytest.raises(ValueError, match="npz"):
        save_dataset(dataset, tmp_path / "wrong.npy")


def test_count_changes_preserve_nested_training_and_all_held_out_data(config, dataset, benchmark):
    expanded = generate_dataset(replace(config, train_count=5))
    for label in ("train", "validation", "test"):
        original_ids = dataset.trajectory_ids[dataset.split == label]
        for trajectory_id in original_ids:
            first = int(np.flatnonzero(dataset.trajectory_ids == trajectory_id)[0])
            second = int(np.flatnonzero(expanded.trajectory_ids == trajectory_id)[0])
            np.testing.assert_array_equal(dataset.states[first], expanded.states[second])
            np.testing.assert_array_equal(dataset.controls[first], expanded.controls[second])
            assert dataset.metadata["trajectories"][first] == expanded.metadata["trajectories"][second]
    other_benchmark = generate_benchmark_dataset(replace(config, train_count=5))
    np.testing.assert_array_equal(other_benchmark.states, benchmark.states)
    changed = generate_dataset(replace(config, seed=config.seed+1))
    assert not np.array_equal(changed.states, dataset.states)


def test_replaying_actual_controls_reproduces_dataset_states(config, dataset):
    simulator = DroneSimulator(config.simulation)
    simulator.reset(DroneState.from_array(dataset.states[0, 0]))
    for index, command in enumerate(dataset.controls[0]):
        result = simulator.step(DroneControl(command[0], command[1:]))
        np.testing.assert_allclose(result.state.as_array(), dataset.states[0, index+1], atol=1e-12, rtol=0)


def test_saved_reference_and_initial_state_reproduce_the_whole_flight(config, dataset):
    record = dataset.metadata["trajectories"][0]
    parameters = record["reference_parameters"]
    reference = FlightReference(**{key: parameters[key] for key in (
        "family", "duration", "seed", "origin", "yaw_offset", "motion_scale", "cycles")})
    flight = simulate_flight(DroneSimulator(config.simulation), reference, config.controller,
                             DroneState.from_array(record["initial_state"]))
    np.testing.assert_array_equal(flight.states, dataset.states[0])
    np.testing.assert_array_equal(flight.controls, dataset.controls[0])


def test_export_is_compatible_with_existing_playback(tmp_path, dataset):
    path = tmp_path / "flight.npz"
    export_trajectory(dataset, 2, path)
    track = load_flight(path)
    np.testing.assert_array_equal(track.time, dataset.time)
    np.testing.assert_allclose(track.states, dataset.states[2], atol=1e-15)
    assert track.metadata["trajectory_id"] == dataset.trajectory_ids[2]
    assert track.metadata["valid_for_learning"]
    with pytest.raises(IndexError):
        dataset.trajectory(-1)


def test_randomized_flights_and_geometric_transforms(dataset):
    assert len(np.unique(dataset.states[:, 0, :], axis=0)) == len(dataset.states)
    records = dataset.metadata["trajectories"]
    assert len({row["seed"] for row in records}) == len(records)
    parameters = dict(origin=(.2, -.3, 1.1), yaw_offset=.7, motion_scale=.8)
    reference = FlightReference("figure_eight", **parameters)
    base = FlightReference("figure_eight")
    at = reference.sample(3.)
    baseline = base.sample(3.)
    rotation = rotation_matrix(roll_pitch_yaw_quaternion(0, 0, .7))
    np.testing.assert_allclose(at.position, np.array(parameters["origin"])+.8*(rotation @ (baseline.position-base.origin)))
    np.testing.assert_allclose(at.velocity, .8*(rotation @ baseline.velocity))
    np.testing.assert_allclose(at.acceleration, .8*(rotation @ baseline.acceleration))
    assert at.yaw == pytest.approx(baseline.yaw+.7)


def test_rejected_flight_is_logged_and_retried_with_a_new_seed(config, monkeypatch):
    import drone_sim.dataset as module
    original = module.simulate_flight
    calls = []
    def reject_first(*args):
        flight = original(*args)
        calls.append(args[1].seed)
        if len(calls) == 1:
            flight.failure_reason = "injected contact failure"
            flight.contacts[0] = True
        return flight
    monkeypatch.setattr(module, "simulate_flight", reject_first)
    result = generate_dataset(replace(config, train_count=1, validation_count=1, test_count=1))
    assert len(result.states) == 3 and not result.contacts.any()
    assert calls[0] != calls[1]
    failures = result.metadata["failed_trajectories"]
    assert len(failures) == 1
    assert failures[0]["trajectory_id"] == "train_000000"
    assert failures[0]["failure_reason"] == "injected contact failure"
    assert result.metadata["trajectories"][0]["attempt"] == 1


def test_exhausted_retries_raise_instead_of_returning_partial_data(config, monkeypatch):
    import drone_sim.dataset as module
    original = module.simulate_flight
    def reject(*args):
        flight = original(*args)
        flight.failure_reason = "injected unstable flight"
        return flight
    monkeypatch.setattr(module, "simulate_flight", reject)
    with pytest.raises(DatasetGenerationError) as raised:
        generate_dataset(replace(config, max_attempts_per_trajectory=2))
    assert len(raised.value.failures) == 2
    assert raised.value.failures[0]["seed"] != raised.value.failures[1]["seed"]


def test_invalid_dataset_content_is_rejected(dataset):
    contacts = dataset.contacts.copy()
    contacts[0, 0] = True
    with pytest.raises(ValueError, match="contact-free"):
        replace(dataset, contacts=contacts)
    duplicate_ids = dataset.trajectory_ids.copy()
    duplicate_ids[1] = duplicate_ids[0]
    with pytest.raises(ValueError, match="unique"):
        replace(dataset, trajectory_ids=duplicate_ids)
    states = dataset.states.copy()
    states[0, 0, 3:7] *= 2
    with pytest.raises(ValueError, match="normalized"):
        replace(dataset, states=states)
    with pytest.raises(ValueError, match="shape"):
        replace(dataset, controls=dataset.controls[:, :-1])
    with pytest.raises(ValueError, match="applied"):
        replace(dataset, controls=dataset.controls+1.)
    with pytest.raises(ValueError, match="schema"):
        replace(dataset, metadata={**dataset.metadata, "schema_version": 999})
    with pytest.raises(ValueError, match="grid"):
        replace(dataset, time=dataset.time+1.)
    families = dataset.families.copy()
    families[0] = "waypoints"
    with pytest.raises(ValueError, match="exclude"):
        replace(dataset, families=families)


def test_missing_schema_fields_and_object_archives_are_rejected(tmp_path, dataset):
    path = tmp_path / "bad.npz"
    np.savez(path, states=np.zeros((1, 2, 13)))
    with pytest.raises(ValueError, match="missing arrays"):
        load_dataset(path)
    from drone_sim.dataset import ARRAY_NAMES
    arrays = {name: getattr(dataset, name) for name in ARRAY_NAMES}
    arrays["states"] = dataset.states.astype(object)
    np.savez(path, **arrays, metadata_json=json.dumps(dataset.metadata))
    with pytest.raises(ValueError, match="Object arrays"):
        load_dataset(path)


@pytest.mark.parametrize("options", [dict(train_count=0), dict(test_count=1.5), dict(seed=-1),
                                     dict(held_out_family="invalid"), dict(height_range=(2, 1)),
                                     dict(motion_scale_range=(0, 1)), dict(cycles_range=(np.nan, 1))])
def test_invalid_generation_settings(options):
    with pytest.raises(ValueError):
        DatasetConfig(**options)


def test_summary_counts_and_numbered_outputs(tmp_path, dataset, benchmark):
    summary = dataset_summary(dataset)
    assert summary["train"]["trajectories"] == 3
    assert summary["train"]["transitions"] == 30
    assert sum(summary["train"]["family_counts"].values()) == 3
    assert dataset_summary(benchmark)["benchmark"]["family_counts"]["waypoints"] == 2
    first, number = next_run(tmp_path)
    second, next_number = next_run(tmp_path)
    assert first.name == "drone_run_1" and number == 1
    assert second.name == "drone_run_2" and next_number == 2

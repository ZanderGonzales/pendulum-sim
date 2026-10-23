"""Exact-update learning, leakage prevention, checkpoint selection, and rollout scoring."""

from dataclasses import replace
import inspect
import json

import numpy as np
import pytest
import torch

from drone_sim import (DatasetConfig, DroneState, RigidBodyPhysics, SimulationConfig,
                       generate_dataset, generate_benchmark_dataset)
from drone_sim.evaluation import trajectory_metrics
from drone_sim.playback import load_flight
from model_drone_residual import (DroneResidualMLP, HybridPredictor, TrainingConfig, fit_standardizers,
                                  load_checkpoint, prepare_samples, save_training_outputs, train_model)
from model_drone_residual.evaluation import evaluate_test_set, save_evaluation_summaries


@pytest.fixture(scope="module")
def dataset_config():
    return DatasetConfig(train_count=3, validation_count=2, test_count=2, benchmark_count=2,
                         seed=512, simulation=SimulationConfig(duration=.05))


@pytest.fixture(scope="module")
def data(dataset_config):
    return generate_dataset(dataset_config)


@pytest.fixture(scope="module")
def benchmark(dataset_config):
    return generate_benchmark_dataset(dataset_config)


@pytest.fixture(scope="module")
def result(data):
    return train_model(data, TrainingConfig(optimizer_updates=6, batch_size=4, validation_interval=4,
                                          hidden_size=8, hidden_layers=1, seed=7))


def test_default_10000_updates_when_already_at_epoch_boundary(data, monkeypatch):
    original = torch.optim.Adam.step
    calls = 0

    def count_step(self, *args, **kwargs):
        nonlocal calls
        calls += 1
        return original(self, *args, **kwargs)

    monkeypatch.setattr(torch.optim.Adam, "step", count_step)
    fitted = train_model(data, TrainingConfig(hidden_size=4, hidden_layers=1))
    assert calls == 10000 == fitted.summary["optimizer_updates"]
    assert fitted.config.batch_size == 256 and fitted.config.learning_rate == .001
    assert [row["optimizer_updates"] for row in fitted.history] == list(range(0, 10001, 100))
    assert fitted.final_checkpoint["optimizer_updates"] == 10000
    assert fitted.summary["samples_processed"] == 150000  # One complete 15-sample batch per epoch.
    assert fitted.summary["completed_epochs"] == 10000
    assert all(int(state["step"]) == 10000 for state in fitted.final_checkpoint["optimizer_state_dict"]["state"].values())


def test_complete_final_epoch_validation_schedule_and_best_selection(result):
    assert result.summary["requested_optimizer_updates"] == 6
    assert result.summary["optimizer_updates"] == 8
    assert result.summary["epochs_started"] == 2 and result.summary["completed_epochs"] == 2
    assert result.summary["samples_processed"] == 30
    assert result.summary["epoch_fraction"] == 2
    assert [row["optimizer_updates"] for row in result.history] == [0, 4, 8]
    best = min(result.history, key=lambda row: row["validation_loss"])
    assert result.best_checkpoint["optimizer_updates"] == best["optimizer_updates"]
    assert result.summary["best_validation_residual_mse"] == best["validation_loss"]
    assert result.final_checkpoint["training_progress"]["samples_in_current_epoch"] == 15
    assert result.final_checkpoint["next_sample_offset"] == 15
    assert len(result.final_checkpoint["current_epoch_permutation"]) == 15
    for name, value in result.model.state_dict().items():
        torch.testing.assert_close(value, result.best_checkpoint["model_state_dict"][name], rtol=0, atol=0)


@pytest.mark.parametrize("updates,expected", [(1, [0, 1]), (4, [0, 4]), (5, [0, 4, 5])])
def test_final_validation_occurs_once_even_between_intervals(data, updates, expected):
    fitted = train_model(data, TrainingConfig(optimizer_updates=updates, validation_interval=4, hidden_size=4, hidden_layers=1))
    assert [row["optimizer_updates"] for row in fitted.history] == expected


def test_training_never_requests_test_data_and_repeats_deterministically(data, monkeypatch):
    requested = []
    original = type(data).samples

    def guarded(self, label):
        requested.append(label)
        assert label in ("train", "validation")
        return original(self, label)

    monkeypatch.setattr(type(data), "samples", guarded)
    config = TrainingConfig(optimizer_updates=9, batch_size=4, validation_interval=4, hidden_size=8, hidden_layers=1, seed=5)
    first, second = train_model(data, config), train_model(data, config)
    assert requested == ["train", "validation", "train", "validation"]
    for a, b in zip(first.history, second.history):
        assert a["train_loss"] == b["train_loss"] and a["validation_loss"] == b["validation_loss"]
    for name, value in first.final_checkpoint["model_state_dict"].items():
        torch.testing.assert_close(value, second.final_checkpoint["model_state_dict"][name], rtol=0, atol=0)


def test_saved_best_and_final_checkpoints_keep_optimizer_accounting_and_scalers(tmp_path, result):
    save_training_outputs(result, tmp_path, provenance={"dataset_hash": "example"})
    for kind, expected in (("best", result.best_checkpoint), ("final", result.final_checkpoint)):
        predictor, checkpoint = load_checkpoint(tmp_path/f"checkpoint_{kind}.pt")
        assert checkpoint["optimizer_updates"] == expected["optimizer_updates"]
        assert checkpoint["training_run_summary"]["optimizer_updates"] == 8
        assert checkpoint["provenance"] == {"dataset_hash": "example"}
        assert checkpoint["standardizers"] == json.loads((tmp_path/"standardizers.json").read_text())
        assert predictor.physics.config.duration == .05
        assert checkpoint["optimizer_state_dict"]["param_groups"][0]["lr"] == .001
        assert checkpoint["training_config"]["seed"] == 7


def test_recursive_rollout_uses_each_preceding_prediction_and_has_no_truth_argument(data):
    training = prepare_samples(data, "train")
    predictor = HybridPredictor(DroneResidualMLP(8, 1), fit_standardizers(training),
                                RigidBodyPhysics(config=SimulationConfig(duration=.05)))
    initial = data.states[0, 0]
    controls = data.controls[0]
    manual = [initial]
    for control in controls:
        manual.append(predictor.step_array(manual[-1], control))
    prediction = predictor.rollout(initial, controls)
    np.testing.assert_allclose(prediction, manual, atol=1e-15)
    assert list(inspect.signature(predictor.rollout).parameters) == ["initial_states", "applied_controls"]
    np.testing.assert_allclose(np.linalg.norm(prediction[:, 3:7], axis=-1), 1., atol=1e-15)
    # Altering future truth cannot affect the inputs supplied to rollout.
    altered = data.states[0].copy()
    altered[1:] += 20
    np.testing.assert_array_equal(predictor.rollout(altered[0], controls), prediction)


def test_batched_and_single_recursive_predictions_agree(result, data):
    predictor = HybridPredictor(result.model, result.standardizers, result.physics)
    initial, controls = data.states[:2, 0], data.controls[:2]
    batched = predictor.rollout(initial, controls)
    individual = np.stack([predictor.rollout(x, u) for x, u in zip(initial, controls)])
    np.testing.assert_allclose(batched, individual, rtol=0, atol=1e-13)
    with pytest.raises(ValueError):
        predictor.rollout(initial, controls[0])
    with pytest.raises(ValueError):
        predictor.rollout(initial, np.full_like(controls, np.nan))


def test_complete_final_evaluation_separates_modes_predictors_and_family_benchmark(tmp_path, data, benchmark, result):
    predictor = HybridPredictor(result.model, result.standardizers, result.physics)
    first = evaluate_test_set(predictor, data, tmp_path, save_plots=False)
    second = evaluate_test_set(predictor, benchmark, tmp_path, split="benchmark", save_plots=False)
    summary = save_evaluation_summaries([first, second], tmp_path)
    assert set(summary) == {"test", "benchmark"}
    assert len(first["rows"]) == 8  # Two trajectories, two modes, two predictors.
    for split, source in (("test", data), ("benchmark", benchmark)):
        for mode in ("one_step", "recursive"):
            assert set(summary[split][mode]) == {"physics_only", "hybrid"}
            with np.load(tmp_path/f"predictions/{split}_{mode}.npz", allow_pickle=False) as archive:
                assert archive["hybrid_states"].shape == (2, 6, 13)
                np.testing.assert_array_equal(archive["controls"], source.controls[source.split == split])
                for name, key in (("physics_only", "physics_states"), ("hybrid", "hybrid_states")):
                    values = [trajectory_metrics(a, b) for a, b in zip(archive[key], archive["truth_states"])]
                    for metric in ("position_mae_m", "orientation_mae_rad"):
                        assert summary[split][mode][name]["mean_"+metric] == np.mean([row[metric] for row in values])
        identifier = source.trajectory_ids[np.flatnonzero(source.split == split)[0]]
        track = load_flight(tmp_path/f"predictions/{identifier}_hybrid_recursive.npz")
        assert track.states.shape == (6, 13)
    assert json.loads((tmp_path/"test_metrics.json").read_text()) == summary
    with pytest.raises(ValueError, match="test or benchmark"):
        evaluate_test_set(predictor, data, tmp_path, split="train", save_plots=False)


@pytest.mark.parametrize("kwargs", [dict(optimizer_updates=0), dict(optimizer_updates=True), dict(batch_size=0),
                                     dict(validation_interval=0), dict(seed=-1), dict(learning_rate=np.nan), dict(num_threads=0)])
def test_invalid_training_settings(kwargs):
    with pytest.raises(ValueError):
        TrainingConfig(**kwargs)

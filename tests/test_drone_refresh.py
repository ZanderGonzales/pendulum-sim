"""Truth access, refresh timing, full-state resets, drift visibility, and schedules."""

import csv
import json

import numpy as np
import pytest
import torch

from drone_sim import DatasetConfig, RigidBodyPhysics, SimulationConfig, generate_dataset
from drone_sim.evaluation import one_step_predictions, trajectory_metrics
from drone_sim.playback import load_comparison
from model_drone_residual import (DroneResidualMLP, HybridPredictor, RefreshSchedule, fit_standardizers,
                                  prepare_samples, rollout_with_refresh)
from model_drone_residual.refresh_evaluation import (PRIMARY_VIEW, POST_VIEW, evaluate_refresh_schedule,
                                                     save_refresh_summaries)


@pytest.fixture(scope="module")
def data():
    return generate_dataset(DatasetConfig(train_count=3, validation_count=2, test_count=2,
                                          seed=71, simulation=SimulationConfig(duration=.1)))


@pytest.fixture(scope="module")
def predictor(data):
    training = prepare_samples(data, "train")
    return HybridPredictor(DroneResidualMLP(8, 1), fit_standardizers(training),
                           RigidBodyPhysics(config=SimulationConfig(duration=.1)))


def held_out(data):
    mask = data.split == "test"
    return data.states[mask], data.controls[mask]


def test_default_no_refresh_never_reads_future_truth_and_matches_both_existing_rollouts(data, predictor):
    truth, controls = held_out(data)
    def forbidden(step):
        pytest.fail(f"unexpected truth access at step {step}")
    for model in (predictor.physics, predictor):
        result = rollout_with_refresh(model, truth[:, 0], controls, truth_provider=forbidden)
        np.testing.assert_array_equal(result.states, model.rollout(truth[:, 0], controls))
        np.testing.assert_array_equal(result.forecast_states, result.states)
        assert result.refresh_steps.shape == (0,)
        assert result.pre_refresh_states.shape == result.corrected_refresh_states.shape == (2, 0, 13)
    assert not RefreshSchedule(interval_steps=100).resolve(10, .01)


@pytest.mark.parametrize("schedule,expected", [
    (RefreshSchedule(interval_steps=2), (2, 4, 6, 8, 10)),
    (RefreshSchedule(interval_seconds=.02), (2, 4, 6, 8, 10)),
    (RefreshSchedule(steps=(10, 2, 7)), (2, 7, 10)),
    (RefreshSchedule(times=(.1, .02, .07)), (2, 7, 10)),
    (RefreshSchedule(interval_seconds=.03), (3, 6, 9)),
    (RefreshSchedule(times=(.1+.2,)), (30,)),
])
def test_step_and_grid_time_schedules_resolve_consistently(schedule, expected):
    assert schedule.resolve(100, .01) == expected if expected == (30,) else schedule.resolve(10, .01) == expected


def test_selected_step_replaces_all_13_values_after_predicting_and_then_uses_next_control(data, predictor):
    truth, controls = held_out(data)
    calls = []
    def provider(step):
        calls.append(step)
        return truth[:, step]
    result = rollout_with_refresh(predictor.physics, truth[:, 0], controls,
                                 schedule=RefreshSchedule(steps=(2, 7)), truth_provider=provider)
    assert calls == [2, 7]
    np.testing.assert_array_equal(result.states[:, [2, 7]], truth[:, [2, 7]])
    np.testing.assert_array_equal(result.corrected_refresh_states, truth[:, [2, 7]])
    np.testing.assert_array_equal(result.pre_refresh_states, result.forecast_states[:, [2, 7]])
    expected_second = predictor.physics.step_array(result.states[:, 1], controls[:, 1])
    expected_third = predictor.physics.step_array(truth[:, 2], controls[:, 2])
    np.testing.assert_array_equal(result.forecast_states[:, 2], expected_second)
    np.testing.assert_array_equal(result.forecast_states[:, 3], expected_third)
    assert np.max(np.abs(result.pre_refresh_states-result.corrected_refresh_states)) > 0


def test_every_step_refresh_has_nonzero_forecast_errors_and_exact_post_states(data, predictor):
    truth, controls = held_out(data)
    for model in (predictor.physics, predictor):
        result = rollout_with_refresh(model, truth[:, 0], controls,
                       schedule=RefreshSchedule(interval_steps=1), truth_provider=lambda step: truth[:, step])
        expected = one_step_predictions(model, truth, controls)
        np.testing.assert_allclose(result.forecast_states, expected, rtol=0, atol=1e-13)
        np.testing.assert_array_equal(result.states[:, 1:], truth[:, 1:])
        for actual, pre, post in zip(truth, result.forecast_states, result.states):
            assert trajectory_metrics(pre, actual)["position_mae_m"] > 0
            assert trajectory_metrics(post, actual)["position_mae_m"] == 0


def test_final_step_refresh_cannot_improve_any_forecast_and_scalar_rollouts_work(data, predictor):
    truth, controls = held_out(data)
    baseline = predictor.physics.rollout(truth[0, 0], controls[0])
    result = rollout_with_refresh(predictor.physics, truth[0, 0], controls[0],
                 schedule=RefreshSchedule(steps=(10,)), truth_provider=lambda step: truth[0, step])
    np.testing.assert_array_equal(result.forecast_states, baseline)
    np.testing.assert_array_equal(result.states[-1], truth[0, -1])
    assert result.pre_refresh_states.shape == (1, 13)
    assert result.schedule_metadata["includes_final_step"]
    assert trajectory_metrics(result.forecast_states, truth[0])["final_position_error_m"] > 0
    assert trajectory_metrics(result.states, truth[0])["final_position_error_m"] == 0


def test_refreshes_leave_weights_normalization_and_source_arrays_unchanged(data, predictor):
    truth, controls = held_out(data)
    previous_truth, previous_controls = truth.copy(), controls.copy()
    weights = {name: value.clone() for name, value in predictor.model.state_dict().items()}
    scales = json.dumps(predictor.standardizers.to_dict(), sort_keys=True)
    rollout_with_refresh(predictor, truth[:, 0], controls, schedule=RefreshSchedule(interval_steps=2),
                         truth_provider=lambda step: truth[:, step])
    np.testing.assert_array_equal(truth, previous_truth)
    np.testing.assert_array_equal(controls, previous_controls)
    assert json.dumps(predictor.standardizers.to_dict(), sort_keys=True) == scales
    for name, value in predictor.model.state_dict().items():
        torch.testing.assert_close(value, weights[name], rtol=0, atol=0)


def test_saved_metrics_events_segments_and_playback_do_not_hide_replacement(tmp_path, data, predictor):
    schedule = RefreshSchedule(interval_steps=3)
    result = evaluate_refresh_schedule(predictor, data, tmp_path/"case", schedule=schedule, label="every_3_steps", save_plots=False)
    summary = save_refresh_summaries([result], tmp_path)
    events = list(csv.DictReader((tmp_path/"case/refresh_events_test.csv").open()))
    segments = list(csv.DictReader((tmp_path/"case/segments_test.csv").open()))
    assert result["refresh_events"] == len(events) == 12  # 2 models * 2 flights * 3 refreshes.
    assert result["segments"] == len(segments) == 16
    selected = [row for row in segments if row["trajectory_id"] == "test_000000" and row["predictor"] == "hybrid"]
    assert [(int(row["start_step"]), int(row["end_step"])) for row in selected] == [(0, 3), (3, 6), (6, 9), (9, 10)]
    assert selected[-1]["ends_in_refresh"] == "False"
    assert all(float(row["post_position_error_m"]) == 0 for row in events)
    for name in ("physics_only", "hybrid"):
        rows = [row for row in result["trajectory_rows"] if row["predictor"] == name and row["metric_view"] == PRIMARY_VIEW]
        assert summary["every_3_steps"]["test"][PRIMARY_VIEW][name]["mean_position_mae_m"] == np.mean([row["position_mae_m"] for row in rows])
    with np.load(tmp_path/"case/predictions/test_recursive.npz", allow_pickle=False) as archive:
        np.testing.assert_array_equal(archive["hybrid_pre_refresh_states"], archive["hybrid_forecast_states"][:, [3, 6, 9]])
        np.testing.assert_array_equal(archive["hybrid_corrected_refresh_states"], archive["truth_states"][:, [3, 6, 9]])
        np.testing.assert_array_equal(archive["hybrid_states"][:, [3, 6, 9]], archive["truth_states"][:, [3, 6, 9]])
    tracks = load_comparison(tmp_path/"case/predictions/test_recursive.npz")
    assert tracks.reference.metadata["truth_refresh"]["resolved_steps"] == [3, 6, 9]
    zero = evaluate_refresh_schedule(predictor, data, tmp_path/"none", save_plots=False)
    assert zero["refresh_events"] == 0 and zero["segments"] == 4
    assert zero["summaries"][PRIMARY_VIEW] == zero["summaries"][POST_VIEW]


@pytest.mark.parametrize("kwargs", [dict(interval_steps=0), dict(interval_steps=True), dict(steps=(0,)),
    dict(steps=(1.5,)), dict(steps=(1, 1)), dict(interval_seconds=np.nan), dict(times=(0.,)),
    dict(times=(.1, .1)), dict(interval_steps=2, times=(.1,))])
def test_invalid_schedule_configuration(kwargs):
    with pytest.raises(ValueError):
        RefreshSchedule(**kwargs)


@pytest.mark.parametrize("schedule", [RefreshSchedule(interval_seconds=.015), RefreshSchedule(times=(.021,)),
                                        RefreshSchedule(steps=(11,)), RefreshSchedule(times=(.11,))])
def test_off_grid_or_out_of_horizon_schedules_are_rejected(schedule):
    with pytest.raises(ValueError):
        schedule.resolve(10, .01)


def test_bad_truth_provider_and_missing_provider_are_rejected(data, predictor):
    truth, controls = held_out(data)
    schedule = RefreshSchedule(interval_steps=1)
    with pytest.raises(ValueError, match="truth_provider"):
        rollout_with_refresh(predictor, truth[:, 0], controls, schedule=schedule)
    for value in (np.zeros((2, 3)), np.zeros((2, 13)), np.full((2, 13), np.nan)):
        with pytest.raises(ValueError, match="truth_provider"):
            rollout_with_refresh(predictor, truth[:, 0], controls, schedule=schedule, truth_provider=lambda step: value)

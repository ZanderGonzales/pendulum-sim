"""Residual geometry, tiny-target precision, train-only scaling, and NN interfaces."""

from dataclasses import replace
import json

import numpy as np
import pytest
import torch
from torch import nn

from drone_sim import DatasetConfig, DroneState, RigidBodyPhysics, SimulationConfig, generate_dataset, generate_benchmark_dataset
from drone_sim.evaluation import one_step_residuals, state_errors
from drone_sim.frames import (compose_quaternions, rotate_vectors, rotation_matrix,
                              rotation_vector_quaternion, roll_pitch_yaw_quaternion, yaw_quaternion)
from model_drone_residual import (DroneResidualMLP, FEATURE_ORDER, TARGET_ORDER, HybridPredictor,
                                  ResidualStandardizers, Standardizer, apply_residual, residual_features,
                                  fit_standardizers, gradient_check, prepare_samples, standardized_tensors,
                                  save_initial_checkpoint, load_checkpoint)


@pytest.fixture(scope="module")
def data():
    return generate_dataset(DatasetConfig(train_count=3, validation_count=2, test_count=2,
                                          simulation=SimulationConfig(duration=.05), seed=31))


@pytest.fixture(scope="module")
def training(data):
    return prepare_samples(data, "train")


@pytest.fixture(scope="module")
def scalers(training):
    return fit_standardizers(training)


@pytest.mark.parametrize("width,depth,count", [(32, 2, 1932), (64, 2, 5900), (128, 2, 19980),
                                               (64, 1, 1740), (64, 4, 14220)])
def test_architectures_have_correct_depth_width_activation_and_parameter_counts(width, depth, count):
    model = DroneResidualMLP(width, depth)
    assert model.parameter_count == count
    linear = [layer for layer in model.network if isinstance(layer, nn.Linear)]
    assert len(linear) == depth+1
    assert [(layer.in_features, layer.out_features) for layer in linear] == [(14, width)]+[(width, width)]*(depth-1)+[(width, 12)]
    assert sum(isinstance(layer, nn.Tanh) for layer in model.network) == depth
    assert model(torch.zeros(2, 3, 14)).shape == (2, 3, 12)


def test_feature_order_body_velocity_and_body_gravity():
    q = roll_pitch_yaw_quaternion(.2, .3, .7)
    state = DroneState(quaternion=q, linear_velocity=(.3, -.2, .1), angular_velocity=(.1, .2, .3)).as_array()
    controls = [.26, 1e-6, -2e-6, 3e-6]
    features = residual_features(state, controls, .01)
    assert len(FEATURE_ORDER) == 14 and len(TARGET_ORDER) == 12
    np.testing.assert_allclose(features[:3], rotation_matrix(q).T@state[7:10])
    np.testing.assert_array_equal(features[3:6], state[10:13])
    np.testing.assert_allclose(features[6:9], rotation_matrix(q).T@[0, 0, -9.81])
    np.testing.assert_array_equal(features[9:13], controls)
    assert features[13] == .01
    level = residual_features(DroneState(quaternion=yaw_quaternion(1.4)).as_array(), controls, .01)
    np.testing.assert_allclose(level[6:9], [0, 0, -9.81])


def test_features_are_translation_heading_and_quaternion_sign_invariant():
    x = DroneState(quaternion=roll_pitch_yaw_quaternion(.2, -.3, .5), linear_velocity=(.3, -.1, .2),
                   angular_velocity=(.2, -.1, .1)).as_array()
    controls = [.26, 0, 1e-6, 0]
    original = residual_features(x, controls, .01)
    transformed = x.copy()
    heading = yaw_quaternion(2.3)
    transformed[:3] = rotation_matrix(heading)@x[:3]+[2, -3, 1]
    transformed[7:10] = rotation_matrix(heading)@x[7:10]
    transformed[3:7] = compose_quaternions(heading, x[3:7])
    np.testing.assert_allclose(residual_features(transformed, controls, .01), original, atol=3e-15)
    transformed[3:7] *= -1
    np.testing.assert_allclose(residual_features(transformed, controls, .01), original, atol=3e-15)


def test_batched_vector_rotation_and_quaternion_exponential():
    vectors = np.array([[1., 2., 3.], [.2, -.4, .1]])
    quaternions = np.array([yaw_quaternion(.7), roll_pitch_yaw_quaternion(.2, -.3, .4)])
    rotated = rotate_vectors(vectors, quaternions)
    expected = np.stack([rotation_matrix(q)@v for q, v in zip(quaternions, vectors)])
    np.testing.assert_allclose(rotated, expected, atol=1e-15)
    np.testing.assert_allclose(rotate_vectors(rotated, quaternions, inverse=True), vectors, atol=1e-15)
    np.testing.assert_array_equal(rotation_vector_quaternion([0, 0, 0]), [1, 0, 0, 0])
    np.testing.assert_allclose(rotation_vector_quaternion([0, 0, 1e-12]), [1, 0, 0, 5e-13], atol=1e-28)
    np.testing.assert_allclose(rotation_vector_quaternion([0, 0, .8]), yaw_quaternion(.8))


def test_arbitrary_residual_round_trip_and_noncommuting_orientation_composition():
    rng = np.random.default_rng(42)
    states = rng.normal(size=(3, 5, 13))
    states[..., 3:7] /= np.linalg.norm(states[..., 3:7], axis=-1, keepdims=True)
    predicted = rng.normal(size=(3, 5, 13))
    predicted[..., 3:7] /= np.linalg.norm(predicted[..., 3:7], axis=-1, keepdims=True)
    corrections = rng.normal(scale=.2, size=(3, 5, 12))
    truth = apply_residual(states, predicted, corrections)
    residual = one_step_residuals(states, predicted, truth)
    np.testing.assert_allclose(residual, corrections, atol=1e-15)
    recovered = apply_residual(states, predicted, residual)
    for error in state_errors(recovered, truth).values():
        assert np.max(error) < 2e-15
    # Right-composition in predicted NEXT axes; not left-composition or current axes.
    expected = rotation_matrix(predicted[0, 0, 3:7])@rotation_matrix(rotation_vector_quaternion(corrections[0, 0, 6:9]))
    np.testing.assert_allclose(rotation_matrix(truth[0, 0, 3:7]), expected, atol=1e-15)
    negated = predicted.copy()
    negated[..., 3:7] *= -1
    np.testing.assert_allclose(state_errors(apply_residual(states, negated, corrections), truth)["orientation_rad"], 0, atol=1e-15)


def test_real_simulator_targets_reconstruct_next_states_and_zero_residual_preserves_physics(training):
    rebuilt = apply_residual(training.current_states, training.physics_next, training.targets)
    zero = apply_residual(training.current_states, training.physics_next, np.zeros_like(training.targets))
    for error in state_errors(rebuilt, training.next_states).values():
        assert np.max(error) < 1e-14
    for error in state_errors(zero, training.physics_next).values():
        assert np.max(error) < 1e-14
    assert np.max(np.abs(training.targets)) > 0
    np.testing.assert_allclose(np.linalg.norm(rebuilt[:, 3:7], axis=-1), 1, atol=1e-15)


def test_sample_alignment_is_complete_trajectory_local(data, training):
    selected = data.samples("train")
    np.testing.assert_array_equal(training.current_states, selected["state_current"])
    np.testing.assert_array_equal(training.next_states, selected["state_next"])
    np.testing.assert_array_equal(training.trajectory_ids, selected["trajectory_id"])
    np.testing.assert_array_equal(training.step_indices, selected["step_index"])
    assert training.features.shape == (15, 14) and training.targets.shape == (15, 12)
    expected = RigidBodyPhysics(config=SimulationConfig(duration=.05)).step_array(selected["state_current"], selected["control_current"])
    np.testing.assert_array_equal(training.physics_next, expected)
    with pytest.raises(ValueError, match="timing"):
        prepare_samples(data, "train", RigidBodyPhysics())


def test_standardizers_preserve_small_signal_and_constant_columns():
    values = np.array([[.01, 2e-12], [.01, -2e-12], [.01, 0.]])
    scaler = Standardizer.fit(values)
    assert scaler.scale[0] == 1
    assert 0 < scaler.scale[1] < 1e-8
    np.testing.assert_array_equal(scaler.transform(values)[:, 0], 0)
    np.testing.assert_allclose(scaler.transform(values).std(axis=0)[1], 1.)
    np.testing.assert_allclose(scaler.inverse_transform(scaler.transform(values)), values, atol=1e-27)
    assert scaler.mean.dtype == np.float64 and scaler.scale.dtype == np.float64
    assert not scaler.mean.flags.writeable


def test_residual_subtraction_precedes_float32_conversion():
    current = DroneState().as_array()
    predicted = current.copy()
    truth = current.copy()
    truth[0] = 1e-9
    predicted[0] = 1.
    truth[0] += 1.
    residual = one_step_residuals(current, predicted, truth)
    assert residual[0] != 0.
    assert np.float32(truth[0])-np.float32(predicted[0]) == 0.
    assert residual.dtype == np.float64


def test_scalers_use_training_only_and_reject_other_splits(data, training, scalers):
    expected = Standardizer.fit(training.features)
    np.testing.assert_array_equal(scalers.inputs.mean, expected.mean)
    assert scalers.training_sample_count == 15 and len(scalers.training_trajectory_ids) == 3
    before = json.dumps(scalers.to_dict(), sort_keys=True)
    for split in ("validation", "test"):
        samples = prepare_samples(data, split)
        with pytest.raises(ValueError, match="train split"):
            fit_standardizers(samples)
        standardized_tensors(samples, scalers)
    benchmark = generate_benchmark_dataset(DatasetConfig(benchmark_count=1, simulation=SimulationConfig(duration=.05)))
    held_out = prepare_samples(benchmark, "benchmark")
    with pytest.raises(ValueError, match="train split"):
        fit_standardizers(held_out)
    assert json.dumps(scalers.to_dict(), sort_keys=True) == before
    train_x, train_y = standardized_tensors(training, scalers)
    assert train_x.dtype == torch.float32 and train_y.dtype == torch.float32
    assert training.targets.dtype == np.float64
    np.testing.assert_array_equal(train_x[:, -1].numpy(), 0)


def test_gradient_check_connects_all_parameters_without_updating_weights(training, scalers):
    torch.manual_seed(4)
    model = DroneResidualMLP()
    original = {name: value.clone() for name, value in model.state_dict().items()}
    result = gradient_check(model, training, scalers)
    assert result["passed"] and result["optimizer_updates"] == 0
    assert all(result["parameter_gradients_finite"].values())
    for name, value in model.state_dict().items():
        torch.testing.assert_close(value, original[name], rtol=0, atol=0)
    assert all(parameter.grad is None for parameter in model.parameters())
    with pytest.raises(ValueError, match="training data"):
        gradient_check(model, replace(training, split="test"), scalers)


@pytest.mark.parametrize("dtype", [torch.float32, torch.float64])
def test_checkpoint_and_json_round_trips_preserve_one_step_inference(tmp_path, training, scalers, dtype):
    physics = RigidBodyPhysics(config=SimulationConfig(duration=.05))
    model = DroneResidualMLP(hidden_size=8, hidden_layers=1).to(dtype)
    predictor = HybridPredictor(model, scalers, physics)
    x = training.current_states[:4]
    controls = np.tile([.26, 0, 0, 0], (4, 1))
    expected = predictor.step_array(x, controls)
    path = tmp_path/"checkpoint_initial.pt"
    save_initial_checkpoint(path, predictor, seed=12)
    loaded, metadata = load_checkpoint(path)
    assert metadata["training_status"] == "untrained" and metadata["optimizer_updates"] == 0
    assert next(loaded.model.parameters()).dtype == dtype
    np.testing.assert_array_equal(loaded.step_array(x, controls), expected)
    restored = ResidualStandardizers.from_dict(json.loads(json.dumps(scalers.to_dict())))
    np.testing.assert_array_equal(restored.targets.scale, scalers.targets.scale)
    assert expected.dtype == np.float64
    assert np.isfinite(expected).all()


def test_zero_standardized_network_output_means_target_mean_not_zero_physical_residual(training, scalers):
    model = DroneResidualMLP(8, 1)
    for parameter in model.parameters():
        nn.init.zeros_(parameter)
    predictor = HybridPredictor(model, scalers, RigidBodyPhysics(config=SimulationConfig(duration=.05)))
    residual = predictor.predict_residuals(training.current_states[0], [.26, 0, 0, 0])
    np.testing.assert_array_equal(residual, scalers.targets.mean)
    assert np.max(np.abs(residual)) > 0


@pytest.mark.parametrize("operation", [
    lambda: DroneResidualMLP(0, 2), lambda: DroneResidualMLP(64, True),
    lambda: Standardizer.fit(np.empty((0, 3))), lambda: Standardizer([0], [0]),
    lambda: Standardizer.fit([[np.nan]]), lambda: Standardizer([0], [1]).transform([0, 1]),
    lambda: rotation_vector_quaternion([0, np.inf, 0]),
    lambda: rotate_vectors([0, 0, 0], [[1, 0, 0, 0]]),
    lambda: compose_quaternions([1, 0, 0, 0], [[1, 0, 0, 0]]),
    lambda: apply_residual(np.zeros(13), np.zeros(13), np.zeros(11)),
    lambda: residual_features(DroneState().as_array(), [.26, 0, 0, 0], 0),
    lambda: residual_features(np.stack([DroneState().as_array()]*2), np.zeros((2, 4)), [.01, .01, .01]),
])
def test_invalid_model_scaling_geometry_and_feature_inputs(operation):
    with pytest.raises(ValueError):
        operation()


def test_standardizer_contract_rejects_wrong_order_and_fitting_split(scalers):
    payload = scalers.to_dict()
    for update in ({"schema_version": 9}, {"fit_split": "test"}, {"target_order": list(reversed(TARGET_ORDER))}):
        with pytest.raises(ValueError):
            ResidualStandardizers.from_dict({**payload, **update})

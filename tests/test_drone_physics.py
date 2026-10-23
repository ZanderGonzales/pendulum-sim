"""Analytic dynamics, fluid isolation, quaternion geometry, and baseline scoring."""

import numpy as np
import pytest

from drone_sim import DroneControl, DroneSimulator, DroneState, RigidBodyParameters, RigidBodyPhysics, SimulationConfig
from drone_sim.artifacts import next_phase
from drone_sim.evaluation import (one_step_predictions, one_step_residuals, state_errors,
                                  summarize_metrics, trajectory_metrics)
from drone_sim.frames import orientation_difference, roll_pitch_yaw_quaternion, rotation_matrix, yaw_quaternion
from drone_sim.verification import compare_without_fluid, verify_analytic_motion


def test_analytic_motion_and_free_fall_over_many_steps():
    physics = RigidBodyPhysics()
    assert verify_analytic_motion(physics)["passed"]
    initial = DroneState(position=(0, 0, 10), linear_velocity=(.1, -.2, .3))
    result = physics.rollout(initial.as_array(), np.zeros((100, 4)))
    time = np.arange(101)*.01
    expected = initial.position + time[:, None]*initial.linear_velocity + .5*time[:, None]**2*np.array([0, 0, -9.81])
    np.testing.assert_allclose(result[:, :3], expected, atol=3e-13)
    np.testing.assert_allclose(np.linalg.norm(result[:, 3:7], axis=-1), 1., atol=1e-15)


@pytest.mark.parametrize("axis", range(3))
@pytest.mark.parametrize("sign", [-1, 1])
def test_moment_signs_angular_acceleration_and_thrust_axes(axis, sign):
    physics = RigidBodyPhysics()
    control = DroneControl(.26487, tuple(sign*1e-6*np.eye(3)[axis]))
    predicted = physics.step(DroneState(), control)
    assert predicted.angular_velocity[axis]*sign > 0
    assert predicted.quaternion[axis+1]*sign > 0
    assert predicted.angular_velocity[axis] == pytest.approx(sign*.01e-6/physics.parameters.inertia[axis])


def test_rotational_coupling_and_torque_free_invariants():
    physics = RigidBodyPhysics()
    state = DroneState(angular_velocity=(1.2, -.8, .6))
    x = state.as_array()
    inertia = np.array(physics.parameters.inertia)
    expected = -np.cross(x[10:], inertia*x[10:])/inertia
    np.testing.assert_allclose(physics.derivative(x, np.zeros(4))[10:], expected)
    result = physics.rollout(x, np.zeros((100, 4)))
    omega = result[:, 10:]
    energy = .5*np.sum(inertia*omega**2, axis=-1)
    momentum = np.linalg.norm(inertia*omega, axis=-1)
    np.testing.assert_allclose(energy, energy[0], rtol=1e-11)
    np.testing.assert_allclose(momentum, momentum[0], rtol=1e-11)


@pytest.mark.parametrize("fluid", [False, True])
def test_fluid_switch_and_reference_independence(fluid):
    simulator = DroneSimulator(fluid_forces=fluid)
    assert simulator.model.opt.density == pytest.approx(1.225 if fluid else 0.)
    assert simulator.model.opt.viscosity == pytest.approx(1.8e-5 if fluid else 0.)
    assert DroneSimulator().model.opt.density == pytest.approx(1.225)


def test_arbitrary_attitude_rotation_and_actual_controls_against_fluid_free_mujoco():
    simulator = DroneSimulator(fluid_forces=False)
    physics = RigidBodyPhysics(RigidBodyParameters.from_metadata(simulator.metadata()))
    initial = DroneState(quaternion=roll_pitch_yaw_quaternion(.3, -.4, 2.1),
                         linear_velocity=(.5, -.3, .2), angular_velocity=(.4, -.3, .2))
    simulator.reset(initial)
    requested = DroneControl(1., (2e-5, -3e-5, 4e-5))
    actual = simulator.step(requested)
    prediction = physics.step(initial, actual.applied_control)
    errors = state_errors(prediction.as_array(), actual.state.as_array())
    assert errors["position_m"] < 1e-10
    assert errors["orientation_rad"] < 1e-8
    assert errors["linear_velocity_m_s"] < 1e-8
    assert errors["angular_velocity_rad_s"] < 1e-12
    # This check also catches raw actuator commands being mistaken for moments.
    assert actual.applied_control.thrust == .35


def test_drag_is_omitted_and_normal_reference_has_nonzero_residual():
    physics = RigidBodyPhysics()
    state = DroneState(linear_velocity=(.4, -.3, .2), angular_velocity=(.2, -.1, .3))
    control = DroneControl(physics.parameters.mass*9.81)
    no_fluid, normal = DroneSimulator(fluid_forces=False), DroneSimulator()
    for simulator in (normal, no_fluid):
        simulator.reset(state)
    predicted = physics.step(state, control).as_array()
    normal_next = normal.step(control).state.as_array()
    no_fluid_next = no_fluid.step(control).state.as_array()
    assert np.linalg.norm(predicted[7:10]-normal_next[7:10]) > 1e-6
    assert np.linalg.norm(predicted[7:10]-no_fluid_next[7:10]) < 1e-9
    np.testing.assert_allclose(physics.derivative(state.as_array(), control.as_array())[7:10], 0.)


def test_batch_scalar_quaternion_sign_and_no_input_mutation():
    physics = RigidBodyPhysics()
    state = DroneState(quaternion=roll_pitch_yaw_quaternion(.2, -.3, .4), angular_velocity=(.2, .1, -.2))
    states = np.stack([state.as_array()]*6).reshape(2, 3, 13)
    controls = np.tile([.26, 1e-6, -2e-6, 3e-6], (2, 3, 1))
    before = states.copy()
    expected = physics.step_array(states[0, 0], controls[0, 0])
    result = physics.step_array(states, controls)
    np.testing.assert_allclose(result, np.broadcast_to(expected, states.shape))
    np.testing.assert_array_equal(before, states)
    states[..., 3:7] *= -1
    negated = physics.step_array(states, controls)
    np.testing.assert_allclose(negated[..., :3], result[..., :3])
    np.testing.assert_allclose(negated[..., 3:7], -result[..., 3:7])
    np.testing.assert_allclose(state_errors(negated, result)["orientation_rad"], 0., atol=1e-15)


def test_one_step_and_rollout_use_correct_current_states_and_control_intervals():
    physics = RigidBodyPhysics()
    controls = np.tile([.26, 1e-6, -2e-6, 0.], (2, 10, 1))
    initial = np.stack([DroneState().as_array()]*2)
    rollout = physics.rollout(initial, controls)
    # The one-step and recursive paths agree on self-generated data.
    np.testing.assert_allclose(one_step_predictions(physics, rollout, controls, chunk_size=3), rollout, atol=1e-14)
    changed = rollout.copy()
    changed[:, 5, 7] += 1.
    one_step = one_step_predictions(physics, changed, controls)
    assert np.max(np.abs(one_step[:, 6]-rollout[:, 6])) > .5
    np.testing.assert_allclose(one_step[:, 7:], rollout[:, 7:], atol=1e-14)
    # Recursive interface has only the initial state and controls.
    np.testing.assert_array_equal(physics.rollout(changed[:, 0], controls), rollout)


def test_rotation_difference_small_angles_signs_pi_and_composition():
    assert np.linalg.norm(orientation_difference([1, 0, 0, 0], yaw_quaternion(1e-12))) == pytest.approx(1e-12)
    np.testing.assert_allclose(orientation_difference([1, 0, 0, 0], [0, -1, 0, 0]), [np.pi, 0, 0])
    predicted = roll_pitch_yaw_quaternion(.7, -.4, 1.)
    truth = roll_pitch_yaw_quaternion(-.2, .3, -.5)
    vector = orientation_difference(predicted, truth)
    angle = np.linalg.norm(vector)
    axis = vector/angle
    skew = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
    correction = np.eye(3)+np.sin(angle)*skew+(1-np.cos(angle))*(skew@skew)
    np.testing.assert_allclose(rotation_matrix(predicted)@correction, rotation_matrix(truth), atol=1e-14)
    np.testing.assert_allclose(orientation_difference(-predicted, truth), vector)
    np.testing.assert_allclose(orientation_difference(predicted, -truth), vector)


def test_residual_coordinates_reconstruct_translations_and_velocities():
    current = DroneState(quaternion=yaw_quaternion(np.pi/2)).as_array()
    predicted = DroneState(quaternion=yaw_quaternion(.3)).as_array()
    truth = predicted.copy()
    truth[:3] += [1., 2., 3.]
    truth[7:10] += [-.2, .3, -.4]
    truth[3:7] = yaw_quaternion(.5)
    truth[10:] += [.1, .2, .3]
    residual = one_step_residuals(current, predicted, truth)
    np.testing.assert_allclose(predicted[:3]+rotation_matrix(current[3:7])@residual[:3], truth[:3])
    np.testing.assert_allclose(predicted[7:10]+rotation_matrix(current[3:7])@residual[3:6], truth[7:10])
    np.testing.assert_allclose(residual[6:9], [0, 0, .2], atol=1e-15)
    np.testing.assert_allclose(predicted[10:]+residual[9:12], truth[10:])
    np.testing.assert_allclose(one_step_residuals(current, truth, truth), 0., atol=1e-15)


def test_metrics_use_euclidean_distance_rotation_angle_and_equal_flight_weights():
    truth = np.stack([DroneState().as_array()]*4)
    predicted = truth.copy()
    predicted[1:, :3] += [3, 4, 0]
    predicted[1:, 3:7] = yaw_quaternion(.2)
    row = trajectory_metrics(predicted, truth)
    assert row["position_mae_m"] == 5
    assert row["position_rmse_m"] == 5
    assert row["orientation_mae_rad"] == pytest.approx(.2)
    assert row["orientation_mae_deg"] == pytest.approx(np.degrees(.2))
    shorter = trajectory_metrics(predicted[:2], truth[:2])
    shorter["position_mae_m"] = 9.
    summary = summarize_metrics([row, shorter])
    assert summary["mean_position_mae_m"] == 7.
    assert summary["std_position_mae_m"] == 2.


@pytest.mark.parametrize("kwargs", [dict(mass=0), dict(mass=np.nan), dict(inertia=(1, 1, 3)),
                                     dict(inertia=(0, 1, 1)), dict(gravity=(0, 0, np.inf))])
def test_invalid_physical_properties(kwargs):
    with pytest.raises(ValueError):
        RigidBodyParameters(**kwargs)


def test_invalid_inputs_and_inertial_frame_contract():
    physics = RigidBodyPhysics()
    x = DroneState().as_array()
    for states, control in ((x, [-1, 0, 0, 0]), (x[:-1], np.zeros(4)),
                            (np.full(13, np.nan), np.zeros(4)), (np.zeros(13), np.zeros(4)),
                            (np.tile(x, (2, 1)), np.zeros(4))):
        with pytest.raises(ValueError):
            physics.step_array(states, control)
    metadata = DroneSimulator().metadata()
    for change in ({"inertial_position_body_m": [.1, 0, 0]}, {"inertial_quaternion_wxyz": [.7, .7, 0, 0]}):
        with pytest.raises(ValueError):
            RigidBodyParameters.from_metadata({**metadata, **change})
    with pytest.raises(ValueError):
        physics.rollout(x, np.zeros((2, 3, 4)))
    with pytest.raises(ValueError):
        one_step_predictions(physics, np.tile(x, (2, 1)), np.zeros((1, 4)), chunk_size=0)


def test_phase_directories_preserve_past_outputs(tmp_path):
    target, number = next_phase(tmp_path, 3)
    assert target == tmp_path/"phase_3" and number == 3
    (target/"Phase 3 Data.md").write_text("preserved")
    repeat, number = next_phase(tmp_path, 3)
    assert repeat == target/"repeat_1" and number == 3
    assert (target/"Phase 3 Data.md").read_text() == "preserved"
    assert next_phase(tmp_path, 3)[0] == target/"repeat_2"


def test_matched_fluid_diagnostics_sample_training_only_and_preserve_data():
    from drone_sim import DatasetConfig, generate_dataset

    timing = SimulationConfig(duration=.02)
    dataset = generate_dataset(DatasetConfig(train_count=2, validation_count=1, test_count=1, simulation=timing))
    before = dataset.states.copy()
    summary, arrays = compare_without_fluid(RigidBodyPhysics(config=timing), dataset, samples_per_trajectory=2)
    assert summary["samples"] == 4 and summary["source_split"] == "train"
    assert all(label.startswith("train_") for label in arrays["trajectory_ids"])
    np.testing.assert_array_equal(arrays["step_indices"], [0, 1, 0, 1])
    np.testing.assert_array_equal(dataset.states, before)
    assert summary["comparisons"]["fluid_off"]["max_position_m"] < 1e-9
    assert summary["comparisons"]["normal_reference"]["mean_linear_velocity_m_s"] > 1e-8

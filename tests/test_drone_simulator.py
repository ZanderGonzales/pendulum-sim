"""Phase 1 checks exercise the pinned MuJoCo model, not a substitute simulator."""

import hashlib
import json

import mujoco
import numpy as np
import pytest

from drone_sim import (
    DroneControl, DroneSimulator, DroneState, FLIGHT_FAMILIES, FlightReference,
    SimulationConfig, simulate_flight,
)
from drone_sim.dynamics import MODEL_DIRECTORY, MUJOCO_VERSION
from drone_sim.frames import body_to_inertial, inertial_to_body, rotation_matrix, yaw_quaternion


@pytest.fixture
def simulator():
    return DroneSimulator()


def test_pinned_assets_and_physical_properties(simulator):
    provenance = json.loads((MODEL_DIRECTORY / "provenance.json").read_text())
    assert mujoco.__version__ == MUJOCO_VERSION
    assert provenance["revision"] == "71f066ad0be9cd271f7ed58c030243ef157af9f4"
    for relative, expected in provenance["sha256"].items():
        assert hashlib.sha256((MODEL_DIRECTORY / relative).read_bytes()).hexdigest() == expected
    assert simulator.mass == pytest.approx(.027)
    np.testing.assert_allclose(simulator.inertia, [2.3951e-5, 2.3951e-5, 3.2347e-5])
    assert simulator.model.opt.integrator == mujoco.mjtIntegrator.mjINT_RK4
    assert simulator.model.opt.density == pytest.approx(1.225)
    assert simulator.model.opt.viscosity == pytest.approx(1.8e-5)
    np.testing.assert_array_equal(simulator.model.opt.wind, 0.)


def test_full_state_reset_and_frame_conventions(simulator):
    state = DroneState((.2, -.3, 1.2), (2., 0., 0., 2.), (.1, .2, -.1), (.05, -.02, .03))
    simulator.reset(state)
    np.testing.assert_allclose(simulator.state().as_array(), state.as_array())
    np.testing.assert_allclose(simulator.data.qvel[:3], state.linear_velocity)
    gyro = simulator.data.sensor("body_gyro").data
    np.testing.assert_allclose(gyro, state.angular_velocity)
    q = state.quaternion
    np.testing.assert_allclose(rotation_matrix(q), rotation_matrix(-np.array(q)))
    vector = [.2, -.5, .9]
    np.testing.assert_allclose(inertial_to_body(body_to_inertial(vector, q), q), vector)
    np.testing.assert_allclose(body_to_inertial([1, 0, 0], yaw_quaternion(np.pi/2)), [0, 1, 0], atol=1e-14)


def test_control_saturation_and_negative_stock_gears(simulator):
    raw, applied = simulator.convert_control(DroneControl(1., (1., -1., 1.)))
    np.testing.assert_allclose(raw, [.35, -1., 1., -1.])
    np.testing.assert_allclose(applied.as_array(), [.35, 1e-5, -1e-5, 1e-5])
    _, applied = simulator.convert_control(DroneControl(-1.))
    assert applied.thrust == 0.


@pytest.mark.parametrize("axis", [0, 1, 2])
@pytest.mark.parametrize("sign", [-1, 1])
def test_physical_moments_obey_right_hand_rule(simulator, axis, sign):
    moment = np.zeros(3)
    moment[axis] = sign*1e-6
    result = simulator.step(DroneControl(simulator.hover_control().thrust, moment))
    assert result.state.angular_velocity[axis]*sign > 0
    assert result.state.quaternion[axis+1]*sign > 0
    assert result.actuator_control[axis+1]*sign < 0


def test_thrust_points_along_rotated_body_z_and_free_fall(simulator):
    pitch = .2
    simulator.reset(DroneState(quaternion=(np.cos(pitch/2), 0, np.sin(pitch/2), 0)))
    result = simulator.step(simulator.hover_control())
    assert result.state.linear_velocity[0] > 0
    assert result.state.linear_velocity[2] < 0
    simulator.reset()
    falling = simulator.step(DroneControl(0.))
    assert falling.state.position[2] < 1.
    assert falling.state.linear_velocity[2] == pytest.approx(-.0981, rel=.01)


def test_hover_timing_and_reset_reproducibility(simulator):
    initial = simulator.state().as_array()
    for _ in range(1000):
        result = simulator.step(simulator.hover_control())
        assert not result.contact and result.failure_reason is None
    assert simulator.data.time == pytest.approx(10.)
    np.testing.assert_allclose(simulator.state().as_array(), initial, atol=1e-12)
    simulator.reset()
    assert simulator.data.time == 0.
    assert not simulator.data.ctrl.any()
    np.testing.assert_allclose(simulator.state().as_array(), initial)


@pytest.mark.parametrize("family", FLIGHT_FAMILIES)
def test_complete_controlled_flight_families(simulator, family):
    flight = simulate_flight(simulator, FlightReference(family, seed=0))
    assert flight.valid_for_learning, flight.failure_reason
    assert flight.states.shape == (1001, 13)
    assert flight.controls.shape == flight.requested_controls.shape == flight.actuator_controls.shape == (1000, 4)
    assert flight.contacts.shape == (1000,)
    assert flight.reference_positions.shape == (1001, 3)
    assert np.isfinite(flight.states).all()
    np.testing.assert_allclose(np.linalg.norm(flight.states[:, 3:7], axis=1), 1., atol=1e-12)
    np.testing.assert_allclose(flight.controls, flight.actuator_controls*simulator.gears)
    assert flight.metadata["controller_config"]["attitude_gain"] == 64.
    if family == "straight":
        assert flight.states[400, 0] > .2
        assert abs(flight.states[-1, 0]) < flight.states[400, 0]
    elif family == "climb_descent":
        assert flight.states[:, 2].max() > 1.2
        assert flight.states[-1, 2] < 1.
    elif family in ("circle", "figure_eight", "waypoints"):
        assert np.ptp(flight.states[:, 0]) > .1
        assert np.ptp(flight.states[:, 1]) > .1


def test_applied_control_replay_and_independent_simulators(simulator):
    config = SimulationConfig(duration=.5)
    first = DroneSimulator(config)
    flight = simulate_flight(first, FlightReference("hover", .5), initial_state=DroneState(position=(.05, 0., 1.)))
    replay = DroneSimulator(config)
    replay.reset(DroneState.from_array(flight.states[0]))
    states = [replay.state().as_array()]
    for control in flight.controls:
        result = replay.step(DroneControl(control[0], control[1:]))
        states.append(result.state.as_array())
    np.testing.assert_allclose(states, flight.states, atol=1e-12)
    assert simulator.data.time == 0.


def test_seeded_reference_and_simulation_are_repeatable():
    a, b = FlightReference("waypoints", seed=42), FlightReference("waypoints", seed=42)
    c = FlightReference("waypoints", seed=43)
    np.testing.assert_array_equal(a.points, b.points)
    assert not np.array_equal(a.points, c.points)
    simulator = DroneSimulator(SimulationConfig(duration=1.))
    a = simulate_flight(simulator, FlightReference("hover", 1.), initial_state=DroneState(position=(.03, -.01, 1.)))
    b = simulate_flight(simulator, FlightReference("hover", 1.), initial_state=DroneState(position=(.03, -.01, 1.)))
    np.testing.assert_array_equal(a.states, b.states)
    np.testing.assert_array_equal(a.controls, b.controls)


def test_contact_and_flight_envelope_reject_collection(simulator):
    result = simulate_flight(simulator, FlightReference("hover"), initial_state=DroneState(position=(0, 0, 0)))
    assert not result.valid_for_learning
    assert "contact" in result.failure_reason
    assert result.metadata["initial_contact"]
    simulator.reset(DroneState(position=(0, 0, .04), linear_velocity=(0, 0, -5)))
    step = simulator.step(DroneControl(0.))
    assert step.contact
    result = simulate_flight(simulator, FlightReference("hover"), initial_state=DroneState(position=(11, 0, 1)))
    assert not result.valid_for_learning
    assert "flight envelope" in result.failure_reason
    assert len(result.controls) < 1000


def test_numerical_warning_is_rejected_without_fabricating_state(simulator, monkeypatch):
    last_valid = simulator.state().as_array()
    def unstable_step(model, data):
        data.warning[mujoco.mjtWarning.mjWARN_BADQPOS].number += 1
    monkeypatch.setattr(mujoco, "mj_step", unstable_step)
    result = simulator.step(simulator.hover_control())
    assert result.failure_reason == "MuJoCo numerical instability"
    np.testing.assert_allclose(result.state.as_array(), last_valid)


@pytest.mark.parametrize("kwargs", [dict(dt=0), dict(duration=np.nan), dict(internal_dt=.003), dict(duration=.015)])
def test_invalid_timing(kwargs):
    with pytest.raises(ValueError):
        SimulationConfig(**kwargs)


def test_invalid_states_and_references(simulator):
    for kwargs in (dict(quaternion=(0, 0, 0, 0)), dict(position=(1, 2)), dict(linear_velocity=(np.inf, 0, 0))):
        with pytest.raises(ValueError):
            DroneState(**kwargs)
    with pytest.raises(ValueError):
        DroneControl(np.nan)
    with pytest.raises(ValueError):
        FlightReference("unsupported")
    with pytest.raises(ValueError):
        simulate_flight(simulator, FlightReference("hover", 5.))

import numpy as np
import pytest

from unicycle_sim import (
    UnicycleControl, UnicycleState, angle_difference, body_to_inertial,
    inertial_to_body, simulate_trajectory, step, wrap_angle,
)


def test_stationary_and_straight_motion():
    start = UnicycleState(2.0, -1.0, 0.0)
    assert step(start, UnicycleControl(0.0, 0.0), 0.5) == start
    assert step(start, UnicycleControl(2.0, 0.0), 0.5) == UnicycleState(3.0, -1.0, 0.0)


def test_heading_rotates_forward_motion_and_turn_sign():
    north = step(UnicycleState(0.0, 0.0, np.pi / 2), UnicycleControl(1.0, 0.0), 0.25)
    assert north.x == pytest.approx(0.0, abs=1e-14)
    assert north.y == pytest.approx(0.25)
    left = step(UnicycleState(0.0, 0.0, 0.0), UnicycleControl(1.0, 1.0), 0.2)
    right = step(UnicycleState(0.0, 0.0, 0.0), UnicycleControl(1.0, -1.0), 0.2)
    assert left.y > 0 > right.y


def test_stationary_turn_and_small_omega_limit():
    turned = step(UnicycleState(1.0, 2.0, 0.3), UnicycleControl(0.0, -2.0), 0.4)
    assert (turned.x, turned.y) == (1.0, 2.0)
    assert turned.theta == pytest.approx(-0.5)
    tiny = step(UnicycleState(0.0, 0.0, 0.0), UnicycleControl(3.0, 1e-14), 0.2)
    assert tiny.x == pytest.approx(0.6)
    assert tiny.y == pytest.approx(0.0, abs=1e-14)


def test_frame_round_trip_and_heading_wrap():
    vectors = np.array([[1.0, 2.0], [-0.5, 0.25]])
    assert np.allclose(inertial_to_body(body_to_inertial(vectors, 0.7), 0.7), vectors)
    assert wrap_angle(np.pi) == pytest.approx(-np.pi)
    assert angle_difference(-np.pi + 0.01, np.pi - 0.01) == pytest.approx(0.02)


def test_trajectory_repeats_exact_steps_and_validates_lengths():
    controls = [UnicycleControl(1.0, 0.4), UnicycleControl(0.5, -0.2)]
    trajectory = simulate_trajectory(UnicycleState(0.0, 0.0, 0.2), controls, 0.1)
    assert len(trajectory.states) == 3
    assert trajectory.states[-1] == step(step(trajectory.states[0], controls[0], 0.1), controls[1], 0.1)
    with pytest.raises(ValueError):
        simulate_trajectory(UnicycleState(0.0, 0.0, 0.0), [], 0.0)

"""Exact unicycle dynamics for piecewise-constant controls."""

from collections.abc import Iterable

import numpy as np

from unicycle_sim.frames import body_to_inertial
from unicycle_sim.types import UnicycleControl, UnicycleState, UnicycleTrajectory


def continuous_dynamics(state: UnicycleState, control: UnicycleControl) -> np.ndarray:
    """Return [x_dot, y_dot, theta_dot] in inertial coordinates."""
    return np.array([control.v * np.cos(state.theta), control.v * np.sin(state.theta), control.omega])


def body_increment(control: UnicycleControl, dt: float) -> np.ndarray:
    """Exact local [dx, dy, dtheta] for a constant control over positive dt."""
    if dt <= 0:
        raise ValueError("dt must be positive")
    alpha = control.omega * dt
    # np.sinc(z) = sin(pi*z)/(pi*z); these forms retain the straight-line
    # limit and avoid cancellation/division near zero turn rate.
    dx = control.v * dt * np.sinc(alpha / np.pi)
    dy = control.v * dt * (alpha / 2.0) * np.sinc(alpha / (2.0 * np.pi)) ** 2
    return np.array([dx, dy, alpha], dtype=float)


def step(state: UnicycleState, control: UnicycleControl, dt: float) -> UnicycleState:
    """Advance one exact constant-control interval, retaining unwrapped theta."""
    local = body_increment(control, dt)
    displacement = body_to_inertial(local[:2], state.theta)
    return UnicycleState(state.x + displacement[0], state.y + displacement[1], state.theta + local[2])


def simulate_trajectory(
    initial_state: UnicycleState, controls: Iterable[UnicycleControl], dt: float
) -> UnicycleTrajectory:
    """Simulate a sequence of piecewise-constant controls using exact steps."""
    control_sequence = tuple(controls)
    if dt <= 0:
        raise ValueError("dt must be positive")
    states = [initial_state]
    for control in control_sequence:
        states.append(step(states[-1], control, dt))
    return UnicycleTrajectory(tuple(states), control_sequence, dt)

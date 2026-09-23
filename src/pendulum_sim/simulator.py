from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np


@dataclass(frozen=True)
class PendulumParameters:
    mass: float
    length: float
    gravity: float
    damping: float


def _state_derivative(
    state: np.ndarray,
    t: float,
    params: PendulumParameters,
    torque_fn: Callable[[float], float],
) -> np.ndarray:
    theta, omega = state

    theta_ddot = (
        -params.gravity / params.length * np.sin(theta)
        - params.damping / (params.mass * params.length**2) * omega
        + torque_fn(t) / (params.mass * params.length**2)
    )

    return np.array([omega, theta_ddot], dtype=float)


def simulate_pendulum(
    duration: float,
    num_steps: int,
    theta0: float,
    omega0: float,
    params: PendulumParameters,
    torque_fn: Callable[[float], float],
) -> dict[str, np.ndarray]:
    """Simulate a damped pendulum with applied torque using RK4.

    Returns a dictionary containing time, theta, omega, and torque arrays.
    """
    if num_steps <= 0:
        raise ValueError("num_steps must be positive")
    if duration <= 0:
        raise ValueError("duration must be positive")

    dt = duration / num_steps
    times = np.linspace(0.0, duration, num_steps + 1)
    theta = np.zeros_like(times)
    omega = np.zeros_like(times)

    theta[0] = theta0
    omega[0] = omega0

    state = np.array([theta0, omega0], dtype=float)
    for i in range(num_steps):
        t = times[i]

        k1 = _state_derivative(state, t, params, torque_fn)
        k2 = _state_derivative(state + 0.5 * dt * k1, t + 0.5 * dt, params, torque_fn)
        k3 = _state_derivative(state + 0.5 * dt * k2, t + 0.5 * dt, params, torque_fn)
        k4 = _state_derivative(state + dt * k3, t + dt, params, torque_fn)

        state = state + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)

        theta[i + 1] = state[0]
        omega[i + 1] = state[1]

    torque = np.array([torque_fn(t) for t in times], dtype=float)

    return {
        "time": times,
        "theta": theta,
        "omega": omega,
        "torque": torque,
    }

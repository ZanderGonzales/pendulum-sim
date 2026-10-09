"""Planar frame transforms and angle helpers.

Body +x points forward, body +y points left. Inertial +x/+y share the same
counter-clockwise orientation, and theta=0 points along inertial +x.
"""

import numpy as np


def wrap_angle(angle: float | np.ndarray) -> float | np.ndarray:
    """Wrap radians to [-pi, pi), preserving array inputs as arrays."""
    wrapped = (np.asarray(angle) + np.pi) % (2.0 * np.pi) - np.pi
    return float(wrapped) if wrapped.ndim == 0 else wrapped


def angle_difference(target: float | np.ndarray, source: float | np.ndarray) -> float | np.ndarray:
    """Return the shortest signed angular displacement target - source."""
    return wrap_angle(np.asarray(target) - np.asarray(source))


def body_to_inertial(vector: np.ndarray, theta: float) -> np.ndarray:
    """Rotate one or more body-frame 2-vectors into inertial coordinates."""
    vector = np.asarray(vector, dtype=float)
    if vector.shape[-1:] != (2,):
        raise ValueError("vector's last dimension must be 2")
    c, s = np.cos(theta), np.sin(theta)
    x, y = vector[..., 0], vector[..., 1]
    return np.stack((c * x - s * y, s * x + c * y), axis=-1)


def inertial_to_body(vector: np.ndarray, theta: float) -> np.ndarray:
    """Rotate one or more inertial-frame 2-vectors into body coordinates."""
    vector = np.asarray(vector, dtype=float)
    if vector.shape[-1:] != (2,):
        raise ValueError("vector's last dimension must be 2")
    c, s = np.cos(theta), np.sin(theta)
    x, y = vector[..., 0], vector[..., 1]
    return np.stack((c * x + s * y, -s * x + c * y), axis=-1)

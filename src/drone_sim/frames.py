"""Right-handed frames: world +z up; body +x forward, +y left, +z up.

Quaternions are scalar-first [w, x, y, z], rotating body vectors into world
coordinates. Linear velocity is world-frame; angular velocity is body-frame.
"""

import numpy as np


def normalize_quaternion(quaternion) -> np.ndarray:
    q = np.asarray(quaternion, dtype=float)
    if q.shape != (4,) or not np.isfinite(q).all():
        raise ValueError("quaternion must contain four finite values [w, x, y, z]")
    length = np.linalg.norm(q)
    if length < 1e-12:
        raise ValueError("quaternion must have nonzero norm")
    return q / length


def rotation_matrix(quaternion) -> np.ndarray:
    """Return R such that vector_world = R @ vector_body."""
    w, x, y, z = normalize_quaternion(quaternion)
    return np.array([
        [1 - 2*(y*y + z*z), 2*(x*y - w*z), 2*(x*z + w*y)],
        [2*(x*y + w*z), 1 - 2*(x*x + z*z), 2*(y*z - w*x)],
        [2*(x*z - w*y), 2*(y*z + w*x), 1 - 2*(x*x + y*y)],
    ])


def body_to_inertial(vector, quaternion) -> np.ndarray:
    return rotation_matrix(quaternion) @ np.asarray(vector, dtype=float)


def inertial_to_body(vector, quaternion) -> np.ndarray:
    return rotation_matrix(quaternion).T @ np.asarray(vector, dtype=float)


def yaw_quaternion(yaw: float) -> np.ndarray:
    return np.array([np.cos(yaw / 2), 0., 0., np.sin(yaw / 2)])

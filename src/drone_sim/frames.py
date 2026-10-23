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


def roll_pitch_yaw_quaternion(roll: float, pitch: float, yaw: float) -> np.ndarray:
    """Body-to-world quaternion for Rz(yaw) @ Ry(pitch) @ Rx(roll)."""
    if not np.isfinite([roll, pitch, yaw]).all():
        raise ValueError("roll, pitch, and yaw must be finite")
    cr, cp, cy = np.cos(np.array([roll, pitch, yaw])/2)
    sr, sp, sy = np.sin(np.array([roll, pitch, yaw])/2)
    return normalize_quaternion([cr*cp*cy + sr*sp*sy, sr*cp*cy - cr*sp*sy,
                                 cr*sp*cy + sr*cp*sy, cr*cp*sy - sr*sp*cy])


def unit_quaternions(values) -> np.ndarray:
    """Normalize scalar-first quaternions with any leading batch dimensions."""
    q = np.asarray(values, dtype=float)
    if q.ndim < 1 or q.shape[-1] != 4 or not np.isfinite(q).all():
        raise ValueError("quaternions must be finite with shape (...,4)")
    norm = np.linalg.norm(q, axis=-1, keepdims=True)
    if np.any(norm < 1e-12):
        raise ValueError("quaternions must have nonzero norm")
    return q/norm


def orientation_difference(predicted, truth) -> np.ndarray:
    """Shortest rotation vector for R_pred.T @ R_truth, in predicted body axes.

    Uses composition, not quaternion subtraction. Its norm is in [0,pi];
    quaternion sign changes leave the represented rotation unchanged.
    """
    p, t = unit_quaternions(predicted), unit_quaternions(truth)
    if p.shape != t.shape:
        raise ValueError("orientation pairs must have matching shapes")
    scalar = np.sum(p*t, axis=-1, keepdims=True)
    vector = p[..., :1]*t[..., 1:] - t[..., :1]*p[..., 1:] - np.cross(p[..., 1:], t[..., 1:])
    # Resolve the exact-pi ambiguity deterministically using the largest component.
    dominant = np.take_along_axis(vector, np.argmax(np.abs(vector), axis=-1)[..., None], axis=-1)
    sign = np.where((scalar < 0) | ((scalar == 0) & (dominant < 0)), -1., 1.)
    scalar, vector = scalar*sign, vector*sign
    length = np.linalg.norm(vector, axis=-1, keepdims=True)
    angle = 2*np.arctan2(length, scalar)
    factor = np.divide(angle, length, out=np.full_like(length, 2.), where=length > 1e-15)
    return vector*factor


def rotate_vectors(vectors, quaternions, *, inverse: bool = False) -> np.ndarray:
    """Rotate matching (...,3) vectors using (...,4) body-to-world orientations."""
    values, q = np.asarray(vectors, dtype=float), unit_quaternions(quaternions)
    if values.shape != (*q.shape[:-1], 3) or not np.isfinite(values).all():
        raise ValueError("finite vectors (...,3) must match quaternion leading shapes")
    axis = -q[..., 1:] if inverse else q[..., 1:]
    twice_cross = 2*np.cross(axis, values)
    return values + q[..., :1]*twice_cross + np.cross(axis, twice_cross)


def rotation_vector_quaternion(rotation_vectors) -> np.ndarray:
    """Exponential map, including a stable limit at zero rotation."""
    vectors = np.asarray(rotation_vectors, dtype=float)
    if vectors.ndim < 1 or vectors.shape[-1] != 3 or not np.isfinite(vectors).all():
        raise ValueError("rotation vectors must be finite with shape (...,3)")
    angle = np.linalg.norm(vectors, axis=-1, keepdims=True)
    return unit_quaternions(np.concatenate((np.cos(angle/2), .5*np.sinc(angle/(2*np.pi))*vectors), axis=-1))


def compose_quaternions(left, right) -> np.ndarray:
    """Hamilton product representing R(left) @ R(right), with matching shapes."""
    left, right = unit_quaternions(left), unit_quaternions(right)
    if left.shape != right.shape:
        raise ValueError("quaternion compositions require matching shapes")
    scalar = left[..., :1]*right[..., :1] - np.sum(left[..., 1:]*right[..., 1:], axis=-1, keepdims=True)
    vector = left[..., :1]*right[..., 1:] + right[..., :1]*left[..., 1:] + np.cross(left[..., 1:], right[..., 1:])
    return unit_quaternions(np.concatenate((scalar, vector), axis=-1))

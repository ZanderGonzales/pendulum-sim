"""Explicit feature frames and finite-step residual correction contract."""

import numpy as np

from drone_sim.frames import compose_quaternions, rotate_vectors, rotation_vector_quaternion
from drone_sim.physics import RigidBodyPhysics
from drone_sim.types import finite_tuple


FEATURE_ORDER = (
    "velocity_body_x", "velocity_body_y", "velocity_body_z",
    "angular_velocity_body_x", "angular_velocity_body_y", "angular_velocity_body_z",
    "gravity_body_x", "gravity_body_y", "gravity_body_z",
    "thrust_N", "moment_x_Nm", "moment_y_Nm", "moment_z_Nm", "dt_s",
)
TARGET_ORDER = (
    "delta_position_current_body_x", "delta_position_current_body_y", "delta_position_current_body_z",
    "delta_velocity_current_body_x", "delta_velocity_current_body_y", "delta_velocity_current_body_z",
    "delta_rotation_predicted_next_body_x", "delta_rotation_predicted_next_body_y", "delta_rotation_predicted_next_body_z",
    "delta_angular_velocity_body_x", "delta_angular_velocity_body_y", "delta_angular_velocity_body_z",
)
RESIDUAL_CONVENTION = {
    "position_velocity_frame": "current body",
    "orientation": "Log(R_physics_next.T @ R_sim_next), right-composed in predicted next body axes",
    "angular_velocity": "simulator minus physics body-coordinate state components",
    "units_by_group": ["m", "m/s", "rad", "rad/s"],
}


def residual_features(states, applied_controls, dt, gravity=(0., 0., -9.81)) -> np.ndarray:
    """14 features, independent of world position and global heading in still air.

    Body-frame gravity is the WORLD gravity vector expressed along the drone's
    CURRENT axes: R(q).T @ gravity_world. It encodes tilt, not a second force.
    dt may be a positive scalar or one value per matching state/control pair.
    """
    states, controls = RigidBodyPhysics._validate(states, applied_controls)
    gravity = np.asarray(finite_tuple(gravity, 3, "gravity"))
    timestep = np.asarray(dt, dtype=float)
    if timestep.shape not in ((), states.shape[:-1]) or not np.isfinite(timestep).all() or np.any(timestep <= 0):
        raise ValueError("dt must be positive and finite: scalar or matching state leading shape")
    timesteps = np.broadcast_to(timestep, states.shape[:-1])[..., None]
    q = states[..., 3:7]
    body_velocity = rotate_vectors(states[..., 7:10], q, inverse=True)
    body_gravity = rotate_vectors(np.broadcast_to(gravity, (*states.shape[:-1], 3)), q, inverse=True)
    return np.concatenate((body_velocity, states[..., 10:13], body_gravity, controls, timesteps), axis=-1)


def apply_residual(current_states, physics_next, residuals) -> np.ndarray:
    """Compose 12 physical corrections with a physics next state in float64.

    Translation corrections rotate using CURRENT attitude. Orientation uses
    q_next = q_physics_next (Hamilton product) quaternion_from_rotvec(delta_rotation).
    Angular-velocity components are corrected additively in body coordinates.
    """
    current, predicted = np.asarray(current_states, dtype=float), np.asarray(physics_next, dtype=float)
    residual = np.asarray(residuals, dtype=float)
    if current.ndim < 1 or current.shape[-1] != 13 or current.shape != predicted.shape:
        raise ValueError("current and physics-next states must have matching (...,13) shapes")
    if residual.shape != (*current.shape[:-1], 12):
        raise ValueError("residuals must have matching (...,12) shape")
    if not np.isfinite(current).all() or not np.isfinite(predicted).all() or not np.isfinite(residual).all():
        raise ValueError("states and residuals must be finite")
    result = predicted.copy()
    result[..., :3] += rotate_vectors(residual[..., :3], current[..., 3:7])
    result[..., 7:10] += rotate_vectors(residual[..., 3:6], current[..., 3:7])
    result[..., 3:7] = compose_quaternions(predicted[..., 3:7], rotation_vector_quaternion(residual[..., 6:9]))
    result[..., 10:13] += residual[..., 9:12]
    return result

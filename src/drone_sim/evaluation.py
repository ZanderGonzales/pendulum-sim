"""Physics prediction diagnostics in physical units, with equal-flight summaries."""

import numpy as np

from drone_sim.frames import orientation_difference, unit_quaternions
from drone_sim.physics import RigidBodyPhysics


def state_errors(predicted, truth) -> dict[str, np.ndarray]:
    """Vector norms and shortest rotation angle; never subtract quaternions."""
    predicted, truth = np.asarray(predicted, dtype=float), np.asarray(truth, dtype=float)
    if predicted.shape != truth.shape or predicted.ndim < 1 or predicted.shape[-1] != 13:
        raise ValueError("prediction and truth must have matching (...,13) shapes")
    if not np.isfinite(predicted).all() or not np.isfinite(truth).all():
        raise ValueError("prediction and truth must be finite")
    return {
        "position_m": np.linalg.norm(predicted[..., :3]-truth[..., :3], axis=-1),
        "orientation_rad": np.linalg.norm(orientation_difference(predicted[..., 3:7], truth[..., 3:7]), axis=-1),
        "linear_velocity_m_s": np.linalg.norm(predicted[..., 7:10]-truth[..., 7:10], axis=-1),
        "angular_velocity_rad_s": np.linalg.norm(predicted[..., 10:13]-truth[..., 10:13], axis=-1),
    }


def trajectory_metrics(predicted, truth) -> dict:
    """Average over predicted times only: exclude the exact initial condition."""
    if np.ndim(predicted) != 2 or len(predicted) < 2:
        raise ValueError("a trajectory needs at least one predicted transition")
    errors = state_errors(predicted, truth)
    row = {}
    for name, values in errors.items():
        quantity, unit = {"position_m": ("position", "m"),
                          "orientation_rad": ("orientation", "rad"),
                          "linear_velocity_m_s": ("linear_velocity", "m_s"),
                          "angular_velocity_rad_s": ("angular_velocity", "rad_s")}[name]
        row[f"{quantity}_mae_{unit}"] = float(values[1:].mean())
        row[f"{quantity}_rmse_{unit}"] = float(np.sqrt(np.mean(values[1:]**2)))
    row.update(orientation_mae_deg=float(np.degrees(row["orientation_mae_rad"])),
               orientation_rmse_deg=float(np.degrees(row["orientation_rmse_rad"])),
               final_position_error_m=float(errors["position_m"][-1]),
               maximum_position_error_m=float(errors["position_m"][1:].max()))
    return row


def summarize_metrics(rows: list[dict]) -> dict:
    """Equal weight per trajectory; population standard deviation (ddof=0)."""
    if not rows:
        raise ValueError("at least one trajectory is required")
    keys = [key for key, value in rows[0].items()
            if isinstance(value, (int, float)) and not isinstance(value, bool)]
    summary = {"trajectories": len(rows), "weighting": "equal per trajectory", "std_ddof": 0}
    for key in keys:
        values = np.array([row[key] for row in rows], dtype=float)
        if not np.isfinite(values).all():
            raise ValueError("metrics must be finite")
        summary[f"mean_{key}"] = float(values.mean())
        summary[f"std_{key}"] = float(values.std())
    return summary


def one_step_predictions(physics: RigidBodyPhysics, states, controls, *, chunk_size: int = 8192) -> np.ndarray:
    """Predict each next state from its true current state; preserve flight layout."""
    states, controls = np.asarray(states, dtype=float), np.asarray(controls, dtype=float)
    if (states.ndim < 2 or states.shape[-1] != 13 or
            controls.shape != (*states.shape[:-2], states.shape[-2]-1, 4)):
        raise ValueError("states (...,steps+1,13) and controls (...,steps,4) must align")
    if isinstance(chunk_size, bool) or not isinstance(chunk_size, int) or chunk_size <= 0:
        raise ValueError("chunk_size must be a positive integer")
    current = states[..., :-1, :].reshape(-1, 13)
    applied = controls.reshape(-1, 4)
    result = np.empty_like(current)
    for start in range(0, len(current), chunk_size):
        end = start+chunk_size
        result[start:end] = physics.step_array(current[start:end], applied[start:end])
    initial = states[..., :1, :].copy()
    initial[..., 3:7] = unit_quaternions(initial[..., 3:7])
    return np.concatenate((initial, result.reshape(*controls.shape[:-1], 13)), axis=-2)


def one_step_residuals(current, predicted_next, true_next) -> np.ndarray:
    """12 diagnostic coordinates: dp_body, dv_body, dtheta, domega_body.

    Translational differences use the CURRENT body axes. dtheta is the shortest
    right-composed correction in PREDICTED NEXT body axes. Angular velocity is
    the difference between state components in their respective body axes.
    These are finite-step errors, not derivatives or raw quaternion differences.
    """
    current = np.asarray(current, dtype=float)
    predicted_next, true_next = np.asarray(predicted_next), np.asarray(true_next)
    if current.shape != predicted_next.shape:
        raise ValueError("current and next states must have matching shapes")
    state_errors(predicted_next, true_next)  # shape, finite and orientation checks
    q = unit_quaternions(current[..., 3:7])
    vector = -q[..., 1:]  # conjugate rotates world differences into current body

    def to_body(value):
        cross = 2*np.cross(vector, value)
        return value + q[..., :1]*cross + np.cross(vector, cross)

    return np.concatenate((to_body(true_next[..., :3]-predicted_next[..., :3]),
                           to_body(true_next[..., 7:10]-predicted_next[..., 7:10]),
                           orientation_difference(predicted_next[..., 3:7], true_next[..., 3:7]),
                           true_next[..., 10:13]-predicted_next[..., 10:13]), axis=-1)

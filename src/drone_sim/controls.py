"""Gentle reference paths and an explicit position/attitude PD controller.

This controller generates simulator data. Future predictor rollouts will replay
its recorded applied controls instead of querying this controller with truth.
"""

from dataclasses import dataclass
import numpy as np

from drone_sim.frames import rotation_matrix, yaw_quaternion
from drone_sim.types import DroneControl


FLIGHT_FAMILIES = ("hover", "straight", "climb_descent", "circle", "figure_eight", "waypoints")


@dataclass(frozen=True)
class ReferenceState:
    position: np.ndarray
    velocity: np.ndarray
    acceleration: np.ndarray
    yaw: float = 0.


def smooth_step(t: float, duration: float) -> tuple[float, float, float]:
    """Quintic interpolation, with zero velocity/acceleration at both ends."""
    s = np.clip(t / duration, 0., 1.)
    return (10*s**3 - 15*s**4 + 6*s**5,
            (30*s**2 - 60*s**3 + 30*s**4) / duration,
            (60*s - 180*s**2 + 120*s**3) / duration**2)


class FlightReference:
    def __init__(self, family: str, duration: float = 10., seed: int = 0, *,
                 origin=(0., 0., 1.), yaw_offset: float = 0., motion_scale: float = 1.,
                 cycles: float = 1.):
        if family not in FLIGHT_FAMILIES:
            raise ValueError(f"family must be one of {FLIGHT_FAMILIES}")
        if not np.isfinite(duration) or duration <= 0:
            raise ValueError("duration must be positive and finite")
        self.family, self.duration, self.seed = family, duration, seed
        self.origin = np.asarray(origin, dtype=float).copy()
        if self.origin.shape != (3,) or not np.isfinite(self.origin).all():
            raise ValueError("origin must contain three finite values")
        if not np.isfinite([yaw_offset, motion_scale, cycles]).all() or min(motion_scale, cycles) <= 0:
            raise ValueError("yaw must be finite; motion scale and cycles must be positive and finite")
        self.yaw_offset, self.motion_scale, self.cycles = float(yaw_offset), float(motion_scale), float(cycles)
        self.path_rotation = rotation_matrix(yaw_quaternion(yaw_offset))
        self.knots = np.array([0., .35, .55, .9, 1.]) * duration
        if family == "straight":
            self.points = self.origin + np.array([[0, 0, 0], [.3, 0, 0], [.3, 0, 0], [0, 0, 0], [0, 0, 0]])
        elif family == "climb_descent":
            self.points = self.origin + np.array([[0, 0, 0], [0, 0, .25], [0, 0, .25], [0, 0, -.1], [0, 0, -.1]])
        else:
            rng = np.random.default_rng(seed)
            offsets = rng.uniform([-.18, -.18, -.1], [.18, .18, .15], size=(5, 3))
            offsets[0] = offsets[-1] = 0.
            self.points = self.origin + offsets
            self.knots = np.linspace(0, duration, 5)
        self.points = self.origin + self.motion_scale * ((self.points-self.origin) @ self.path_rotation.T)

    def parameters(self) -> dict:
        """Record enough settings to recreate this path, including its placement."""
        return {"family": self.family, "duration": self.duration, "seed": self.seed,
                "origin": self.origin.tolist(), "yaw_offset": self.yaw_offset,
                "motion_scale": self.motion_scale, "cycles": self.cycles,
                "knots": self.knots.tolist(), "points": self.points.tolist()}

    def sample(self, time: float) -> ReferenceState:
        if not np.isfinite(time):
            raise ValueError("reference time must be finite")
        t = float(np.clip(time, 0., self.duration))
        if self.family == "hover":
            return ReferenceState(self.origin.copy(), np.zeros(3), np.zeros(3), self.yaw_offset)
        if self.family in ("straight", "climb_descent", "waypoints"):
            i = min(int(np.searchsorted(self.knots, t, side="right")) - 1, len(self.knots) - 2)
            s, ds, dds = smooth_step(t - self.knots[i], self.knots[i+1] - self.knots[i])
            delta = self.points[i+1] - self.points[i]
            return ReferenceState(self.points[i] + s*delta, ds*delta, dds*delta, self.yaw_offset)
        s, ds, dds = smooth_step(t, self.duration)
        phase, rate, acceleration = 2*np.pi*self.cycles*np.array([s, ds, dds])
        if self.family == "circle":
            p = [.18*(1-np.cos(phase)), .18*np.sin(phase), 0.]
            v = [.18*np.sin(phase)*rate, .18*np.cos(phase)*rate, 0.]
            a = [.18*(np.cos(phase)*rate**2 + np.sin(phase)*acceleration),
                 .18*(-np.sin(phase)*rate**2 + np.cos(phase)*acceleration), 0.]
        else:
            p = [.22*np.sin(phase), .1*np.sin(2*phase), 0.]
            v = [.22*np.cos(phase)*rate, .2*np.cos(2*phase)*rate, 0.]
            a = [.22*(-np.sin(phase)*rate**2 + np.cos(phase)*acceleration),
                 .2*(-2*np.sin(2*phase)*rate**2 + np.cos(2*phase)*acceleration), 0.]
        return ReferenceState(self.origin + self.motion_scale*(self.path_rotation @ p),
                              self.motion_scale*(self.path_rotation @ v),
                              self.motion_scale*(self.path_rotation @ a),
                              self.yaw_offset + .12*np.sin(phase))


@dataclass(frozen=True)
class ControllerConfig:
    position_gain: float = 1.2
    velocity_gain: float = 2.0
    attitude_gain: float = 64.0
    angular_velocity_gain: float = 16.0
    max_tilt_radians: float = np.deg2rad(12.)

    def __post_init__(self):
        for value in (self.position_gain, self.velocity_gain, self.attitude_gain, self.angular_velocity_gain):
            if not np.isfinite(value) or value <= 0:
                raise ValueError("controller gains must be positive and finite")
        if not np.isfinite(self.max_tilt_radians) or not 0 < self.max_tilt_radians < np.pi / 2:
            raise ValueError("max tilt must be between zero and pi/2")


class FlightController:
    """Position PD plus acceleration feedforward, followed by attitude/rate PD.

    F_world = m * (a_ref + Kp*(p_ref-p) + Kd*(v_ref-v) - gravity).
    Desired body +z aligns with F_world; desired heading comes from ref.yaw.
    tau_body = I*(-Kr*e_rotation - Kw*omega) + omega cross (I*omega).
    Saturation is performed by DroneSimulator and recorded in the trajectory.
    """

    def __init__(self, simulator, config: ControllerConfig = ControllerConfig()):
        self.mass, self.inertia = simulator.mass, simulator.inertia.copy()
        self.gravity = simulator.model.opt.gravity.copy()
        self.config = config

    def command(self, state, reference: ReferenceState) -> DroneControl:
        cfg = self.config
        force = self.mass * (reference.acceleration
                            + cfg.position_gain*(reference.position - state.position)
                            + cfg.velocity_gain*(reference.velocity - state.linear_velocity)
                            - self.gravity)
        force[2] = max(force[2], .1*self.mass*np.linalg.norm(self.gravity))
        horizontal = np.linalg.norm(force[:2])
        limit = force[2] * np.tan(cfg.max_tilt_radians)
        if horizontal > limit:
            force[:2] *= limit / horizontal
        desired_z = force / np.linalg.norm(force)
        heading = np.array([np.cos(reference.yaw), np.sin(reference.yaw), 0.])
        desired_y = np.cross(desired_z, heading)
        desired_y /= np.linalg.norm(desired_y)
        desired_x = np.cross(desired_y, desired_z)
        desired_rotation = np.column_stack((desired_x, desired_y, desired_z))
        current_rotation = rotation_matrix(state.quaternion)
        skew_error = desired_rotation.T @ current_rotation - current_rotation.T @ desired_rotation
        error = .5*np.array([skew_error[2, 1], skew_error[0, 2], skew_error[1, 0]])
        omega = np.asarray(state.angular_velocity)
        moments = self.inertia * (-cfg.attitude_gain*error - cfg.angular_velocity_gain*omega)
        moments += np.cross(omega, self.inertia*omega)
        thrust = max(0., float(force @ current_rotation[:, 2]))
        return DroneControl(thrust, moments)

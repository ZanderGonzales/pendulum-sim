"""Independent Newton/Euler flight predictor; no MuJoCo stepping or aerodynamics.

The body origin is its centre of mass and its axes are principal inertia axes,
as in the pinned Crazyflie model. Controls are already applied physical wrenches.
"""

from dataclasses import dataclass

import numpy as np

from drone_sim.types import DroneControl, DroneState, SimulationConfig, finite_tuple


@dataclass(frozen=True)
class RigidBodyParameters:
    mass: float = .027
    inertia: tuple = (2.3951e-5, 2.3951e-5, 3.2347e-5)
    gravity: tuple = (0., 0., -9.81)

    def __post_init__(self):
        if not np.isfinite(self.mass) or self.mass <= 0:
            raise ValueError("mass must be positive and finite")
        object.__setattr__(self, "mass", float(self.mass))
        object.__setattr__(self, "inertia", finite_tuple(self.inertia, 3, "inertia"))
        object.__setattr__(self, "gravity", finite_tuple(self.gravity, 3, "gravity"))
        if min(self.inertia) <= 0 or 2*max(self.inertia) > sum(self.inertia):
            raise ValueError("principal inertias must be positive and obey the triangle inequality")

    @classmethod
    def from_metadata(cls, simulation: dict) -> "RigidBodyParameters":
        """Copy constants, never infer parameters from observed future motion."""
        if not np.allclose(simulation.get("inertial_position_body_m", [0, 0, 0]), 0., atol=1e-14):
            raise ValueError("physics predictor requires body origin at centre of mass")
        q = np.asarray(simulation.get("inertial_quaternion_wxyz", [1, 0, 0, 0]))
        if q.shape != (4,) or not np.allclose(np.abs(q), [1, 0, 0, 0], atol=1e-14):
            raise ValueError("physics predictor requires principal inertia axes aligned with body")
        return cls(simulation["mass_kg"], tuple(simulation["inertia_kg_m2"]),
                   tuple(simulation["gravity_world_m_s2"]))


class RigidBodyPhysics:
    """Pure one-step transition, with optional leading batch dimensions.

    State: [p_world(3), q_wxyz_body_to_world(4), v_world(3), omega_body(3)].
    Control: [body +z thrust N, right-hand body moments N m]. No re-clipping.
    """

    def __init__(self, parameters: RigidBodyParameters = RigidBodyParameters(),
                 config: SimulationConfig = SimulationConfig()):
        self.parameters = parameters
        self.config = config
        self._inertia = np.asarray(parameters.inertia)

    @staticmethod
    def _validate(states, controls):
        states, controls = np.asarray(states, dtype=float), np.asarray(controls, dtype=float)
        if states.ndim < 1 or states.shape[-1] != 13 or controls.shape != (*states.shape[:-1], 4):
            raise ValueError("states (...,13) and applied controls (...,4) need matching leading shapes")
        if not np.isfinite(states).all() or not np.isfinite(controls).all():
            raise ValueError("states and applied controls must be finite")
        if np.any(np.linalg.norm(states[..., 3:7], axis=-1) < 1e-12):
            raise ValueError("state quaternion must have nonzero norm")
        if np.any(controls[..., 0] < 0):
            raise ValueError("applied thrust must be nonnegative")
        return states, controls

    def _derivative(self, x, u):
        q = x[..., 3:7]
        unit = q / np.linalg.norm(q, axis=-1, keepdims=True)
        w, a, b, c = np.moveaxis(unit, -1, 0)
        # R(q) @ e_z: the third column of the body-to-world rotation matrix.
        thrust_direction = np.stack((2*(a*c+w*b), 2*(b*c-w*a), 1-2*(a*a+b*b)), axis=-1)
        omega = x[..., 10:13]
        derivative = np.empty_like(x)
        derivative[..., :3] = x[..., 7:10]
        derivative[..., 7:10] = self.parameters.gravity + u[..., :1]*thrust_direction/self.parameters.mass
        # q_dot = 1/2 q (Hamilton product) [0, omega_body].
        derivative[..., 3:4] = -.5*np.sum(q[..., 1:]*omega, axis=-1, keepdims=True)
        derivative[..., 4:7] = .5*(q[..., :1]*omega + np.cross(q[..., 1:], omega))
        derivative[..., 10:13] = (u[..., 1:] - np.cross(omega, self._inertia*omega))/self._inertia
        return derivative

    def derivative(self, states, applied_controls) -> np.ndarray:
        """Continuous-time equations, exposed for analytic checks."""
        return self._derivative(*self._validate(states, applied_controls))

    def step_array(self, states, applied_controls) -> np.ndarray:
        """Classical RK4, dt/internal_dt substeps, constant applied control."""
        x, u = self._validate(states, applied_controls)
        x = x.copy()
        x[..., 3:7] /= np.linalg.norm(x[..., 3:7], axis=-1, keepdims=True)
        h = self.config.internal_dt
        for _ in range(self.config.substeps):
            k1 = self._derivative(x, u)
            k2 = self._derivative(x+h*k1/2, u)
            k3 = self._derivative(x+h*k2/2, u)
            k4 = self._derivative(x+h*k3, u)
            x += h*(k1+2*k2+2*k3+k4)/6
            x[..., 3:7] /= np.linalg.norm(x[..., 3:7], axis=-1, keepdims=True)
        if not np.isfinite(x).all():
            raise FloatingPointError("non-finite rigid-body prediction")
        return x

    def step(self, state: DroneState, applied_control: DroneControl) -> DroneState:
        return DroneState.from_array(self.step_array(state.as_array(), applied_control.as_array()))

    def rollout(self, initial_states, applied_controls) -> np.ndarray:
        """Recursive prediction; the interface accepts no future true states.

        Inputs: (...,13), (...,steps,4). Output: (...,steps+1,13).
        """
        initial = np.asarray(initial_states, dtype=float)
        controls = np.asarray(applied_controls, dtype=float)
        if controls.ndim < 2 or controls.shape[:-2] != initial.shape[:-1] or controls.shape[-1] != 4:
            raise ValueError("rollout controls must have shape (...,steps,4) matching initial states")
        self._validate(initial, np.zeros((*initial.shape[:-1], 4)))
        if not np.isfinite(controls).all() or np.any(controls[..., 0] < 0):
            raise ValueError("rollout requires finite applied controls and nonnegative thrust")
        result = np.empty((*initial.shape[:-1], controls.shape[-2]+1, 13))
        result[..., 0, :] = initial
        result[..., 0, 3:7] /= np.linalg.norm(initial[..., 3:7], axis=-1, keepdims=True)
        for k in range(controls.shape[-2]):
            result[..., k+1, :] = self.step_array(result[..., k, :], controls[..., k, :])
        return result

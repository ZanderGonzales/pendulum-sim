"""Explicit state, physical control, timing, and simulation trajectory types."""

from dataclasses import dataclass, field
import numpy as np

from drone_sim.frames import normalize_quaternion


def finite_tuple(value, size: int, name: str) -> tuple:
    array = np.asarray(value, dtype=float)
    if array.shape != (size,) or not np.isfinite(array).all():
        raise ValueError(f"{name} must contain {size} finite values")
    return tuple(float(x) for x in array)


@dataclass(frozen=True)
class DroneState:
    """13 values: p_world(3), q_wxyz(4), v_world(3), omega_body(3), in SI."""

    position: tuple = (0., 0., 1.)
    quaternion: tuple = (1., 0., 0., 0.)
    linear_velocity: tuple = (0., 0., 0.)
    angular_velocity: tuple = (0., 0., 0.)

    def __post_init__(self):
        for name in ("position", "linear_velocity", "angular_velocity"):
            object.__setattr__(self, name, finite_tuple(getattr(self, name), 3, name))
        object.__setattr__(self, "quaternion", tuple(normalize_quaternion(self.quaternion)))

    def as_array(self) -> np.ndarray:
        return np.array((*self.position, *self.quaternion, *self.linear_velocity, *self.angular_velocity))

    @classmethod
    def from_array(cls, values) -> "DroneState":
        a = finite_tuple(values, 13, "state")
        return cls(a[:3], a[3:7], a[7:10], a[10:13])


@dataclass(frozen=True)
class DroneControl:
    """Total body +z thrust [N] and right-hand body moments [N m].

    This is a physical wrench, not raw MuJoCo ctrl and not four rotor speeds.
    The simulator converts it using the stock XML actuator gear factors.
    """

    thrust: float
    moments: tuple = (0., 0., 0.)

    def __post_init__(self):
        if not np.isfinite(self.thrust):
            raise ValueError("thrust must be finite")
        object.__setattr__(self, "thrust", float(self.thrust))
        object.__setattr__(self, "moments", finite_tuple(self.moments, 3, "moments"))

    def as_array(self) -> np.ndarray:
        return np.array((self.thrust, *self.moments))


@dataclass(frozen=True)
class SimulationConfig:
    dt: float = 0.01
    internal_dt: float = 0.002
    duration: float = 10.

    def __post_init__(self):
        for name in ("dt", "internal_dt", "duration"):
            if not np.isfinite(getattr(self, name)) or getattr(self, name) <= 0:
                raise ValueError(f"{name} must be positive and finite")
        for ratio in (self.dt / self.internal_dt, self.duration / self.dt):
            if not np.isclose(ratio, round(ratio), rtol=0, atol=1e-9) or round(ratio) < 1:
                raise ValueError("dt/internal_dt and duration/dt must be positive integers")

    @property
    def substeps(self) -> int:
        return round(self.dt / self.internal_dt)

    @property
    def num_steps(self) -> int:
        return round(self.duration / self.dt)


@dataclass(frozen=True)
class StepResult:
    state: DroneState
    applied_control: DroneControl
    actuator_control: tuple
    contact: bool
    failure_reason: str | None = None


@dataclass
class DroneTrajectory:
    """N controls and N+1 states; requested and saturated inputs are both kept."""

    states: np.ndarray
    requested_controls: np.ndarray
    controls: np.ndarray
    actuator_controls: np.ndarray
    time: np.ndarray
    contacts: np.ndarray
    reference_positions: np.ndarray
    reference_yaw: np.ndarray
    metadata: dict = field(default_factory=dict)
    failure_reason: str | None = None

    @property
    def valid_for_learning(self) -> bool:
        return self.failure_reason is None and not self.contacts.any()

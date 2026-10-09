"""Typed state and control values for the planar unicycle model.

Coordinates are right-handed: body +x is forward, body +y is left, and
positive heading/turn rate are counter-clockwise in the inertial x-y plane.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class UnicycleState:
    x: float
    y: float
    theta: float  # Unwrapped heading in radians.


@dataclass(frozen=True)
class UnicycleControl:
    v: float  # Signed forward speed.
    omega: float  # Signed counter-clockwise angular speed, radians/second.


@dataclass(frozen=True)
class UnicycleTrajectory:
    """States has length N+1; controls has length N, one per interval."""

    states: tuple[UnicycleState, ...]
    controls: tuple[UnicycleControl, ...]
    dt: float

    def __post_init__(self) -> None:
        if self.dt <= 0:
            raise ValueError("dt must be positive")
        if len(self.states) != len(self.controls) + 1:
            raise ValueError("states must have exactly one more item than controls")

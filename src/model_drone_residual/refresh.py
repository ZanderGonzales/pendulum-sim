"""Optional full-state truth refreshes with explicit before/after records."""

from dataclasses import asdict, dataclass
from collections.abc import Callable
from numbers import Integral

import numpy as np

from drone_sim.physics import RigidBodyPhysics


@dataclass(frozen=True)
class RefreshSchedule:
    """Choose at most one schedule; the default has no truth refreshes.

    Step k is the state at t=k*dt, after controls[k-1]. Step 0 initializes the
    prediction and is not a refresh. The final prediction step may be refreshed.
    Time values are seconds relative to the initial state, on the same grid.
    """

    interval_steps: int | None = None
    steps: tuple = ()
    interval_seconds: float | None = None
    times: tuple = ()

    def __post_init__(self):
        object.__setattr__(self, "steps", tuple(self.steps))
        object.__setattr__(self, "times", tuple(self.times))
        if sum((self.interval_steps is not None, bool(self.steps), self.interval_seconds is not None, bool(self.times))) > 1:
            raise ValueError("choose one periodic or explicit refresh schedule, in steps or seconds")
        for value in ((self.interval_steps,) if self.interval_steps is not None else ()) + self.steps:
            if isinstance(value, bool) or not isinstance(value, Integral) or value < 1:
                raise ValueError("refresh steps and intervals must be positive integers; step 0 is initialization")
        for value in ((self.interval_seconds,) if self.interval_seconds is not None else ()) + self.times:
            if isinstance(value, bool) or not np.isfinite(value) or value <= 0:
                raise ValueError("refresh times and intervals must be positive finite seconds")
        if len(set(self.steps)) != len(self.steps) or len(set(self.times)) != len(self.times):
            raise ValueError("explicit refresh steps/times must not contain duplicates")
        object.__setattr__(self, "steps", tuple(int(step) for step in self.steps))
        object.__setattr__(self, "times", tuple(float(value) for value in self.times))
        if self.interval_steps is not None:
            object.__setattr__(self, "interval_steps", int(self.interval_steps))
        if self.interval_seconds is not None:
            object.__setattr__(self, "interval_seconds", float(self.interval_seconds))

    def resolve(self, num_steps: int, dt: float) -> tuple[int, ...]:
        if isinstance(num_steps, bool) or not isinstance(num_steps, int) or num_steps < 1:
            raise ValueError("num_steps must be a positive integer")
        if not np.isfinite(dt) or dt <= 0:
            raise ValueError("dt must be positive and finite")

        def on_grid(value):
            ratio = value/dt
            step = round(ratio)
            if step < 1 or not np.isclose(ratio, step, rtol=0, atol=1e-9):
                raise ValueError(f"refresh time {value:g} must lie on the {dt:g} s prediction grid")
            return step

        interval = self.interval_steps
        if self.interval_seconds is not None:
            interval = on_grid(self.interval_seconds)
        if interval is not None:
            return tuple(range(interval, num_steps+1, interval))
        explicit = self.steps or tuple(on_grid(value) for value in self.times)
        if any(step > num_steps for step in explicit):
            raise ValueError("explicit refresh step/time exceeds the trajectory horizon")
        if len(set(explicit)) != len(explicit):
            raise ValueError("refresh times resolve to duplicate prediction steps")
        return tuple(sorted(explicit))

    def metadata(self, num_steps: int, dt: float) -> dict:
        resolved = self.resolve(num_steps, dt)
        return {"requested": asdict(self), "resolved_steps": list(resolved),
                "resolved_times_s": [step*dt for step in resolved], "refresh_count": len(resolved),
                "dt_s": dt, "num_steps": num_steps, "includes_final_step": num_steps in resolved,
                "replacement": "full position, quaternion orientation, world velocity, body angular velocity",
                "timing": "after predicting step k, replace state at the same k; then continue with control[k]"}


@dataclass(frozen=True)
class RefreshRollout:
    forecast_states: np.ndarray         # (...,steps+1,13), before any replacement at each timestamp
    states: np.ndarray                  # (...,steps+1,13), post-replacement state used for the next step
    refresh_steps: np.ndarray           # (refresh_count,)
    pre_refresh_states: np.ndarray      # (...,refresh_count,13), explicitly retained event snapshots
    corrected_refresh_states: np.ndarray
    schedule_metadata: dict


def rollout_with_refresh(predictor, initial_states, applied_controls, *,
                         schedule: RefreshSchedule = RefreshSchedule(),
                         truth_provider: Callable[[int], np.ndarray] | None = None) -> RefreshRollout:
    """Propagate recursively; truth_provider is called ONLY at selected steps.

    With the default empty schedule, no future truth is required or accessed.
    The provider returns a complete state/batch at the requested step index.
    This function never trains a model, fits normalization, or runs a controller.
    """
    initial, controls = np.asarray(initial_states, dtype=np.float64), np.asarray(applied_controls, dtype=np.float64)
    if controls.ndim < 2 or controls.shape[:-2] != initial.shape[:-1] or controls.shape[-1] != 4:
        raise ValueError("controls (...,steps,4) must match initial states (...,13)")
    RigidBodyPhysics._validate(initial, np.zeros((*initial.shape[:-1], 4)))
    if not np.isfinite(controls).all() or np.any(controls[..., 0] < 0):
        raise ValueError("controls must be finite applied wrenches with nonnegative thrust")
    steps = controls.shape[-2]
    physics = predictor.physics if hasattr(predictor, "physics") else predictor
    dt = physics.config.dt
    resolved = schedule.resolve(steps, dt)
    if resolved and not callable(truth_provider):
        raise ValueError("a truth_provider is required for a nonempty refresh schedule")
    shape = (*initial.shape[:-1], steps+1, 13)
    forecasts, states = np.empty(shape), np.empty(shape)
    states[..., 0, :] = initial
    states[..., 0, 3:7] /= np.linalg.norm(initial[..., 3:7], axis=-1, keepdims=True)
    forecasts[..., 0, :] = states[..., 0, :]
    event_index = {step: index for index, step in enumerate(resolved)}
    event_shape = (*initial.shape[:-1], len(resolved), 13)
    before, corrected = np.empty(event_shape), np.empty(event_shape)
    for step in range(1, steps+1):
        prediction = predictor.step_array(states[..., step-1, :], controls[..., step-1, :])
        forecasts[..., step, :] = prediction
        states[..., step, :] = prediction
        if step in event_index:
            truth = np.asarray(truth_provider(step), dtype=np.float64)
            if truth.shape != initial.shape or not np.isfinite(truth).all():
                raise ValueError("truth_provider must return a finite full state matching initial-state shape")
            if not np.allclose(np.linalg.norm(truth[..., 3:7], axis=-1), 1., rtol=0, atol=1e-8):
                raise ValueError("truth_provider must return normalized quaternion orientations")
            index = event_index[step]
            before[..., index, :] = prediction
            corrected[..., index, :] = truth
            states[..., step, :] = truth
    return RefreshRollout(forecasts, states, np.asarray(resolved, dtype=np.int64), before, corrected,
                          schedule.metadata(steps, dt))

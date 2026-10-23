"""MuJoCo comparisons used to verify the independent phase-3 predictor."""

import numpy as np

from drone_sim.dynamics import DroneSimulator
from drone_sim.evaluation import state_errors
from drone_sim.frames import roll_pitch_yaw_quaternion
from drone_sim.physics import RigidBodyPhysics
from drone_sim.types import DroneControl, DroneState


def verify_analytic_motion(physics: RigidBodyPhysics) -> dict:
    """Check closed-form cases without using MuJoCo as the answer."""
    dt, p = physics.config.dt, physics.parameters
    initial = DroneState(position=(0, 0, 5), linear_velocity=(.2, -.1, .3))
    falling = physics.step(initial, DroneControl(0)).as_array()
    g = np.asarray(p.gravity)
    expected_p = np.array(initial.position) + dt*np.array(initial.linear_velocity) + .5*g*dt**2
    expected_v = np.array(initial.linear_velocity) + g*dt
    hover = physics.step(DroneState(), DroneControl(-p.mass*g[2])).as_array()
    tilted = DroneState(quaternion=roll_pitch_yaw_quaternion(0, .3, 0))
    thrust = -p.mass*g[2]
    derivative = physics.derivative(tilted.as_array(), [thrust, 0, 0, 0])
    expected_a = g + thrust/p.mass*np.array([np.sin(.3), 0, np.cos(.3)])
    moments = np.array([1e-6, -1e-6, 1e-6])
    resting = physics.derivative(DroneState().as_array(), np.r_[thrust, moments])
    single_axis_error = []
    for axis in range(3):
        torque = np.zeros(3)
        torque[axis] = moments[axis]
        rotated = physics.step(DroneState(), DroneControl(thrust, torque)).as_array()
        expected_omega = dt*torque/np.asarray(p.inertia)
        angle = .5*dt**2*torque[axis]/p.inertia[axis]
        expected_q = np.zeros(4)
        expected_q[0], expected_q[axis+1] = np.cos(angle/2), np.sin(angle/2)
        single_axis_error.append(float(np.max(np.abs(rotated[10:]-expected_omega))))
        single_axis_error.append(float(np.max(np.abs(rotated[3:7]-expected_q))))
    checks = {
        "free_fall_position_max_abs_error_m": float(np.max(np.abs(falling[:3]-expected_p))),
        "free_fall_velocity_max_abs_error_m_s": float(np.max(np.abs(falling[7:10]-expected_v))),
        "hover_state_max_abs_error": float(np.max(np.abs(hover-DroneState().as_array()))),
        "tilted_thrust_acceleration_max_abs_error_m_s2": float(np.max(np.abs(derivative[7:10]-expected_a))),
        "resting_angular_acceleration_max_abs_error_rad_s2": float(np.max(np.abs(resting[10:]-moments/p.inertia))),
        "single_axis_rotation_max_abs_error": max(single_axis_error),
    }
    if any(value > 1e-10 for value in checks.values()):
        raise AssertionError(f"analytic rigid-body check failed: {checks}")
    return {"passed": True, "checks": checks}


def compare_without_fluid(physics: RigidBodyPhysics, dataset, *, samples_per_trajectory: int = 10):
    """Reset an isolated fluid-free simulator at sampled TRAINING states only.

    Compare both fluid-on archived next states and fluid-off fresh next states
    on exactly the same initial states and applied controls. No model fitting.
    """
    if (isinstance(samples_per_trajectory, bool) or not isinstance(samples_per_trajectory, int)
            or samples_per_trajectory < 1):
        raise ValueError("samples_per_trajectory must be a positive integer")
    indices = np.flatnonzero(dataset.split == "train")
    if not len(indices):
        raise ValueError("fluid-isolation diagnostics require a training split")
    steps = dataset.controls.shape[1]
    if samples_per_trajectory > steps:
        raise ValueError("samples_per_trajectory exceeds available transitions")
    selected_steps = np.linspace(0, steps-1, samples_per_trajectory, dtype=int)
    flight_index = np.repeat(indices, len(selected_steps))
    step_index = np.tile(selected_steps, len(indices))
    current = dataset.states[flight_index, step_index]
    applied = dataset.controls[flight_index, step_index]
    normal_next = dataset.states[flight_index, step_index+1]
    predicted = physics.step_array(current, applied)
    simulator = DroneSimulator(physics.config, fluid_forces=False)
    no_fluid = []
    for state, control in zip(current, applied):
        simulator.reset(DroneState.from_array(state))
        result = simulator.step(DroneControl(control[0], control[1:]))
        if result.failure_reason or result.contact:
            raise RuntimeError("invalid flight in fluid-isolation diagnostic")
        no_fluid.append(result.state.as_array())
    no_fluid = np.asarray(no_fluid)
    comparisons = {}
    for label, reference in (("fluid_off", no_fluid), ("normal_reference", normal_next)):
        errors = state_errors(predicted, reference)
        comparisons[label] = {f"{stat}_{name}": float(getattr(np, stat)(value))
                              for name, value in errors.items() for stat in ("mean", "max")}
    summary = {"samples": len(current), "source_split": "train",
               "samples_per_trajectory": samples_per_trajectory,
               "fluid_off_simulation": simulator.metadata(), "comparisons": comparisons}
    arrays = {"current_states": current, "controls": applied, "physics_next": predicted,
              "normal_next": normal_next, "fluid_off_next": no_fluid,
              "trajectory_ids": dataset.trajectory_ids[flight_index], "step_indices": step_index}
    return summary, arrays

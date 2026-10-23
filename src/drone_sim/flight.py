"""Run a single controlled reference flight for inspection or dataset generation."""

from dataclasses import asdict
import numpy as np

from drone_sim.controls import ControllerConfig, FlightController, FlightReference
from drone_sim.dynamics import DroneSimulator
from drone_sim.frames import rotation_matrix, yaw_quaternion
from drone_sim.types import DroneState, DroneTrajectory


def simulate_flight(
    simulator: DroneSimulator,
    reference: FlightReference,
    controller_config: ControllerConfig = ControllerConfig(),
    initial_state: DroneState | None = None,
) -> DroneTrajectory:
    """Log requested/applied controls, full states, contacts, and failure reason.

    Contact or flight-envelope failures stop collection and invalidate the entire
    flight. Dataset generation uses valid_for_learning to reject it.
    """
    config = simulator.config
    if not np.isclose(reference.duration, config.duration):
        raise ValueError("reference and simulation durations must match")
    first = reference.sample(0.)
    simulator.reset(initial_state if initial_state is not None else DroneState(
        first.position, yaw_quaternion(first.yaw), first.velocity))
    controller = FlightController(simulator, controller_config)
    states = [simulator.state().as_array()]
    requested, applied, actuator, contacts = [], [], [], []
    failure = "initial state in contact" if simulator.data.ncon else None
    for k in range(config.num_steps):
        if failure:
            break
        command = controller.command(simulator.state(), reference.sample(k*config.dt))
        result = simulator.step(command)
        requested.append(command.as_array())
        applied.append(result.applied_control.as_array())
        actuator.append(result.actuator_control)
        contacts.append(result.contact)
        states.append(result.state.as_array())
        failure = result.failure_reason
        if result.contact:
            failure = failure or f"contact during prediction step {k+1}"
        p = np.asarray(result.state.position)
        if failure is None and (not .05 <= p[2] <= 5. or np.linalg.norm(p[:2]) > 10.
                                or np.linalg.norm(result.state.linear_velocity) > 10.
                                or rotation_matrix(result.state.quaternion)[2, 2] < .5):
            failure = f"outside flight envelope during prediction step {k+1}"
    time = np.arange(len(states))*config.dt
    targets = [reference.sample(t) for t in time]
    metadata = simulator.metadata()
    metadata.update({"family": reference.family, "seed": reference.seed,
                     "controller_config": asdict(controller_config),
                     "reference_definition": "drone_sim.controls.FlightReference",
                     "reference_parameters": reference.parameters(),
                     "reference_knots": reference.knots.tolist(), "reference_points": reference.points.tolist(),
                     "initial_state": states[0].tolist(), "requested_steps": config.num_steps,
                     "completed_steps": len(applied),
                     "flight_envelope": {"height_m": [.05, 5.], "horizontal_radius_m": 10.,
                                         "max_speed_m_s": 10., "max_tilt_degrees": 60.}})
    # Initial contact must remain visible even when no transition is attempted.
    if failure == "initial state in contact":
        metadata["initial_contact"] = True
    return DroneTrajectory(
        np.asarray(states), np.asarray(requested).reshape(-1, 4), np.asarray(applied).reshape(-1, 4),
        np.asarray(actuator).reshape(-1, 4), time, np.asarray(contacts, dtype=bool),
        np.array([r.position for r in targets]), np.array([r.yaw for r in targets]), metadata, failure,
    )

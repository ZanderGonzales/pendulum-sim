"""MuJoCo reference simulator; independent rigid-body prediction is in physics.py.

MuJoCo free-joint qpos is [p_world, q_wxyz], qvel is [v_world, omega_body].
Positive moments use the right-hand rule; stock moment gears are NEGATIVE.
"""

from dataclasses import asdict
import json
from pathlib import Path

import mujoco
import numpy as np

from drone_sim.types import DroneControl, DroneState, SimulationConfig, StepResult


MODEL_DIRECTORY = Path(__file__).parent / "assets" / "bitcraze_crazyflie_2"
MUJOCO_VERSION = "3.16.0"


class DroneSimulator:
    """Own one independent MjModel/MjData pair; no viewer or network required."""

    def __init__(self, config: SimulationConfig = SimulationConfig(), *, fluid_forces: bool = True):
        if mujoco.__version__ != MUJOCO_VERSION:
            raise RuntimeError(f"Install mujoco=={MUJOCO_VERSION}; found {mujoco.__version__}")
        self.config = config
        self.model = mujoco.MjModel.from_xml_path(str(MODEL_DIRECTORY / "scene.xml"))
        self.model.opt.timestep = config.internal_dt
        if not fluid_forces:
            # Diagnostic model instance only; the normal reference stays unchanged.
            self.model.opt.density = 0.
            self.model.opt.viscosity = 0.
        self.data = mujoco.MjData(self.model)
        self.body_id = mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_BODY, "cf2")
        names = ("body_thrust", "x_moment", "y_moment", "z_moment")
        self.actuator_ids = np.array([mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_ACTUATOR, n) for n in names])
        if (self.actuator_ids < 0).any() or (self.model.nq, self.model.nv, self.model.nu) != (7, 6, 4):
            raise RuntimeError("Unexpected Crazyflie state/actuator layout")
        self.gears = np.array([self.model.actuator_gear[i, axis] for i, axis in zip(self.actuator_ids, (2, 3, 4, 5))])
        self.control_limits = self.model.actuator_ctrlrange[self.actuator_ids].copy()
        self.mass = float(self.model.body_mass[self.body_id])
        self.inertia = self.model.body_inertia[self.body_id].copy()
        self.provenance = json.loads((MODEL_DIRECTORY / "provenance.json").read_text(encoding="utf-8"))
        self.reset()

    def reset(self, state: DroneState = DroneState()) -> DroneState:
        """Reset time, contacts, controls, and state, then recompute derived data."""
        mujoco.mj_resetData(self.model, self.data)
        self.data.qpos[:] = (*state.position, *state.quaternion)
        self.data.qvel[:] = (*state.linear_velocity, *state.angular_velocity)
        mujoco.mj_forward(self.model, self.data)
        return self.state()

    def state(self) -> DroneState:
        return DroneState.from_array(np.concatenate((self.data.qpos, self.data.qvel)))

    def hover_control(self) -> DroneControl:
        return DroneControl(self.mass * np.linalg.norm(self.model.opt.gravity))

    def convert_control(self, requested: DroneControl) -> tuple[np.ndarray, DroneControl]:
        """Convert physical wrench to stock ctrl, clip, reconstruct actual wrench."""
        ctrl = np.clip(requested.as_array() / self.gears, self.control_limits[:, 0], self.control_limits[:, 1])
        applied = ctrl * self.gears
        return ctrl, DroneControl(applied[0], applied[1:])

    def step(self, requested: DroneControl) -> StepResult:
        ctrl, applied = self.convert_control(requested)
        self.data.ctrl[self.actuator_ids] = ctrl
        contact = self.data.ncon > 0
        # Observe every internal step: a transient contact must not disappear
        # between the 100 Hz samples. MuJoCo can reset unstable state silently;
        # changed warning counters or unexpected time are treated as failures.
        warnings_before = self.data.warning.number.copy()
        start_time = self.data.time
        for index in range(self.config.substeps):
            last_valid_state = self.state()
            mujoco.mj_step(self.model, self.data)
            contact = contact or self.data.ncon > 0
            expected = start_time + (index + 1) * self.config.internal_dt
            finite = np.isfinite(self.data.qpos).all() and np.isfinite(self.data.qvel).all()
            warned = np.any(self.data.warning.number != warnings_before)
            if not finite or warned or not np.isclose(self.data.time, expected, rtol=0, atol=1e-8):
                # Return the last valid state through the caller's failure log.
                return StepResult(last_valid_state, applied, tuple(ctrl), bool(contact), "MuJoCo numerical instability")
        return StepResult(self.state(), applied, tuple(ctrl), bool(contact))

    def metadata(self) -> dict:
        return {
            "mujoco_version": mujoco.__version__, "model_repository": self.provenance["repository"],
            "model_revision": self.provenance["revision"], "model_license": self.provenance["license"],
            "simulation_config": asdict(self.config), "mass_kg": self.mass,
            "inertia_kg_m2": self.inertia.tolist(), "gravity_world_m_s2": self.model.opt.gravity.tolist(),
            "inertial_position_body_m": self.model.body_ipos[self.body_id].tolist(),
            "inertial_quaternion_wxyz": self.model.body_iquat[self.body_id].tolist(),
            "density_kg_m3": float(self.model.opt.density), "viscosity_pa_s": float(self.model.opt.viscosity),
            "wind_world_m_s": self.model.opt.wind.tolist(), "integrator": "RK4",
            "actuator_gears": self.gears.tolist(), "actuator_ctrlrange": self.control_limits.tolist(),
            "state_order": ["x", "y", "z", "qw", "qx", "qy", "qz", "vx", "vy", "vz", "wx", "wy", "wz"],
            "control_order": ["thrust_N", "moment_x_Nm", "moment_y_Nm", "moment_z_Nm"],
            "frames": "world +z up; quaternion wxyz body-to-world; velocity world; angular velocity body",
        }

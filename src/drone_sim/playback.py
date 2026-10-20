"""Replay saved Crazyflie states in MuJoCo without running the physics again.

FlightTrack is independent of file layout and rendering. A future NN adapter can
construct the same track from full-state predictions and render a transparent
copy at the actual flight's playback time. The nn_prediction argument reserves
that extension explicitly; prediction loading/rendering is not implemented yet.
"""

from dataclasses import dataclass, field
import json
from pathlib import Path
from queue import Empty, SimpleQueue
import time

import mujoco
import numpy as np

from drone_sim.dynamics import DroneSimulator


MIN_SPEED = .125
MAX_SPEED = 8.
CONTROL_HELP = "Space: play/pause | R: restart | A/D: previous/next frame | +/-: speed | L: loop | Q: quit"


@dataclass(frozen=True)
class FlightTrack:
    """One full-state track on an explicit clock, usable by recorded or NN data.

    States are [p_world(3), q_wxyz(4), v_world(3), omega_body(3)]. Arrays are
    copied and read-only so normalizing quaternions never changes the source.
    Sample times may be nonuniform and may start at a nonzero timestamp.
    """

    time: np.ndarray
    states: np.ndarray
    label: str = "Simulator flight"
    metadata: dict = field(default_factory=dict)

    def __post_init__(self):
        times = np.array(self.time, dtype=float, copy=True)
        states = np.array(self.states, dtype=float, copy=True)
        if times.ndim != 1 or len(times) == 0 or not np.isfinite(times).all():
            raise ValueError("time must be a nonempty finite one-dimensional array")
        if np.any(np.diff(times) <= 0):
            raise ValueError("time values must be strictly increasing")
        if states.shape != (len(times), 13) or not np.isfinite(states).all():
            raise ValueError("states must be a finite array of shape (number of times, 13)")
        norms = np.linalg.norm(states[:, 3:7], axis=1)
        if np.any(norms < 1e-12) or not np.isfinite(norms).all():
            raise ValueError("every state needs a nonzero finite quaternion [w, x, y, z]")
        states[:, 3:7] /= norms[:, None]
        times.setflags(write=False)
        states.setflags(write=False)
        object.__setattr__(self, "time", times)
        object.__setattr__(self, "states", states)
        object.__setattr__(self, "metadata", dict(self.metadata))

    @property
    def duration(self) -> float:
        return float(self.time[-1] - self.time[0])

    def frame_at(self, timestamp: float) -> int:
        """Show the last recorded frame at/before time; do not invent new poses."""
        return int(np.clip(np.searchsorted(self.time, timestamp, side="right") - 1, 0, len(self.time) - 1))


def load_flight(path: str | Path) -> FlightTrack:
    """Load one existing *_flight.npz trace; never enable NumPy pickle loading."""
    path = Path(path)
    if path.suffix.lower() != ".npz":
        raise ValueError("choose a saved *_flight.npz file")
    with np.load(path, allow_pickle=False) as archive:
        missing = {"time", "states"} - set(archive.files)
        if missing:
            raise ValueError(f"flight file is missing required arrays: {', '.join(sorted(missing))}")
        metadata = {}
        if "metadata_json" in archive:
            try:
                metadata = json.loads(str(archive["metadata_json"].item()))
            except (ValueError, TypeError) as error:
                raise ValueError("metadata_json must be one JSON object") from error
            if not isinstance(metadata, dict):
                raise ValueError("metadata_json must contain a JSON object")
        return FlightTrack(archive["time"], archive["states"], path.stem, metadata)


class PlaybackController:
    """Deterministic playback clock; no GUI, sleeping, or simulator dependence.

    Advance using elapsed monotonic wall time. The same timestamp will drive an
    actual and optional NN track later; rendering never advances its own clock.
    """

    def __init__(self, track: FlightTrack, *, speed: float = 1., paused: bool = False, loop: bool = False):
        if not np.isfinite(speed) or not MIN_SPEED <= speed <= MAX_SPEED:
            raise ValueError(f"speed must be between {MIN_SPEED} and {MAX_SPEED}")
        self.track = track
        self.speed = float(speed)
        self.paused = bool(paused) or track.duration == 0
        self.loop = bool(loop)
        self.timestamp = float(track.time[0])

    @property
    def frame(self) -> int:
        return self.track.frame_at(self.timestamp)

    def advance(self, elapsed_seconds: float) -> None:
        if not np.isfinite(elapsed_seconds) or elapsed_seconds < 0:
            raise ValueError("elapsed time must be finite and nonnegative")
        if self.paused or self.track.duration == 0 or elapsed_seconds == 0:
            return
        timestamp = self.timestamp + elapsed_seconds * self.speed
        if timestamp >= self.track.time[-1]:
            if self.loop:
                timestamp = self.track.time[0] + (timestamp - self.track.time[0]) % self.track.duration
            else:
                timestamp = self.track.time[-1]
                self.paused = True
        self.timestamp = float(timestamp)

    def action(self, action: str) -> None:
        if action == "toggle_pause":
            if self.paused and self.timestamp >= self.track.time[-1]:
                self.timestamp = float(self.track.time[0])
            self.paused = not self.paused if self.track.duration else True
        elif action == "restart":
            self.timestamp = float(self.track.time[0])
        elif action in ("previous", "next"):
            frame = int(np.clip(self.frame + (-1 if action == "previous" else 1), 0, len(self.track.time)-1))
            self.timestamp = float(self.track.time[frame])
            self.paused = True
        elif action == "faster":
            self.speed = min(MAX_SPEED, self.speed*2)
        elif action == "slower":
            self.speed = max(MIN_SPEED, self.speed/2)
        elif action == "toggle_loop":
            self.loop = not self.loop
        else:
            raise ValueError(f"unknown playback action: {action}")


def apply_frame(model, data, track: FlightTrack, frame: int) -> None:
    """Assign a recorded full state and update geometry; never call mj_step."""
    if not 0 <= frame < len(track.time):
        raise IndexError("playback frame is out of range")
    state = track.states[frame]
    data.qpos[:] = state[:7]
    data.qvel[:] = state[7:]
    data.time = float(track.time[frame])
    mujoco.mj_forward(model, data)


def add_path(scene, track: FlightTrack) -> None:
    """Add a small visual-only line of the recorded path, capped at 250 edges.

    Future transparent NN meshes can share the custom visualization scene.
    This does not create another physical drone or alter reference-model XML.
    """
    indices = np.unique(np.linspace(0, len(track.time)-1, min(len(track.time), 251), dtype=int))
    scene.ngeom = 0
    for left, right in zip(indices[:-1], indices[1:]):
        start, end = track.states[left, :3], track.states[right, :3]
        if np.linalg.norm(end-start) < 1e-9:
            continue
        if scene.ngeom >= scene.maxgeom:
            break
        geom = scene.geoms[scene.ngeom]
        mujoco.mjv_initGeom(geom, mujoco.mjtGeom.mjGEOM_CAPSULE, np.zeros(3), np.zeros(3),
                           np.eye(3).ravel(), np.array([.15, .6, 1., .65]))
        mujoco.mjv_connector(geom, mujoco.mjtGeom.mjGEOM_CAPSULE, .0007, start, end)
        scene.ngeom += 1


def playback_flight(
    flight: str | Path | FlightTrack,
    *, speed: float = 1., paused: bool = False, loop: bool = False,
    follow: bool = False, show_path: bool = True,
    nn_prediction: FlightTrack | None = None,
) -> None:
    """Open a viewer until the user closes it; pause on the final saved frame.

    nn_prediction reserves a future transparent NN prediction of THIS actual
    flight. Passing it currently raises NotImplementedError; no second drone is
    drawn. A future implementation must align its timestamps/world frame with
    flight and sample it using this same PlaybackController, not another clock.
    """
    if nn_prediction is not None:
        raise NotImplementedError("Transparent NN-prediction playback is reserved for a future update")
    track = load_flight(flight) if isinstance(flight, (str, Path)) else flight
    controller = PlaybackController(track, speed=speed, paused=paused, loop=loop)
    simulator = DroneSimulator()
    revision = track.metadata.get("model_revision")
    if revision is not None and revision != simulator.provenance["revision"]:
        raise ValueError("saved flight uses a different Crazyflie model revision")
    apply_frame(simulator.model, simulator.data, track, controller.frame)
    # Import viewer/GLFW only at the GUI boundary; tracks and timing are testable
    # without creating a native window or OpenGL context.
    import glfw
    import mujoco.viewer

    keys = SimpleQueue()
    actions = {glfw.KEY_SPACE: "toggle_pause", glfw.KEY_R: "restart",
               glfw.KEY_LEFT: "previous", glfw.KEY_RIGHT: "next",
               glfw.KEY_A: "previous", glfw.KEY_D: "next",
               glfw.KEY_UP: "faster", glfw.KEY_DOWN: "slower", glfw.KEY_L: "toggle_loop",
               glfw.KEY_EQUAL: "faster", glfw.KEY_MINUS: "slower",
               glfw.KEY_KP_ADD: "faster", glfw.KEY_KP_SUBTRACT: "slower"}
    print(f"Playback: {track.label} ({len(track.time)} frames, {track.duration:g} s)", flush=True)
    print(CONTROL_HELP, flush=True)
    print("Drag the mouse to orbit/pan; scroll to zoom. Playback pauses at the end.", flush=True)
    with mujoco.viewer.launch_passive(simulator.model, simulator.data, key_callback=keys.put,
                                     show_left_ui=False, show_right_ui=False) as viewer:
        with viewer.lock():
            positions = track.states[:, :3]
            viewer.cam.lookat[:] = (positions.min(axis=0) + positions.max(axis=0))/2
            viewer.cam.distance = max(.45, float(np.ptp(positions, axis=0).max())*1.8)
            viewer.cam.azimuth, viewer.cam.elevation = 135., -25.
            if follow:
                viewer.cam.type = mujoco.mjtCamera.mjCAMERA_TRACKING
                viewer.cam.trackbodyid = simulator.body_id
            if show_path:
                add_path(viewer.user_scn, track)
            # MuJoCo also binds A/D to visual flags and R/L to render flags,
            # even with side panels hidden. Preserve those settings when our
            # playback shortcuts reuse the same keys.
            saved_visual_flags = {key: (flag, int(viewer.opt.flags[flag])) for key, flag in (
                (glfw.KEY_A, mujoco.mjtVisFlag.mjVIS_AUTOCONNECT),
                (glfw.KEY_D, mujoco.mjtVisFlag.mjVIS_STATIC))}
            saved_render_flags = {key: (flag, int(viewer.user_scn.flags[flag])) for key, flag in (
                (glfw.KEY_R, mujoco.mjtRndFlag.mjRND_REFLECTION),
                (glfw.KEY_L, mujoco.mjtRndFlag.mjRND_ADDITIVE))}
        last_wall_time = time.perf_counter()
        while viewer.is_running():
            started = time.perf_counter()
            controller.advance(started-last_wall_time)
            last_wall_time = started
            quit_requested = False
            restore_visual, restore_render = [], []
            while True:
                try:
                    key = keys.get_nowait()
                except Empty:
                    break
                if key == glfw.KEY_Q:
                    quit_requested = True
                elif key in actions:
                    controller.action(actions[key])
                    if key in saved_visual_flags:
                        restore_visual.append(saved_visual_flags[key])
                    if key in saved_render_flags:
                        restore_render.append(saved_render_flags[key])
            if quit_requested:
                break
            if restore_render:
                # First collect the native GUI change, then override it through
                # the public custom-scene flags on the regular sync below.
                viewer.sync(state_only=True)
            with viewer.lock():
                for flag, value in restore_visual:
                    viewer.opt.flags[flag] = value
                for flag, value in restore_render:
                    viewer.user_scn.flags[flag] = value
                apply_frame(simulator.model, simulator.data, track, controller.frame)
            state = "PAUSED" if controller.paused else "PLAYING"
            viewer.set_texts((mujoco.mjtFontScale.mjFONTSCALE_100, mujoco.mjtGridPos.mjGRID_BOTTOMLEFT,
                              f"{track.label}\n{state} | {controller.speed:g}x | loop {'ON' if controller.loop else 'OFF'}\n"
                              f"Time {controller.timestamp-track.time[0]:.2f} / {track.duration:.2f} s | frame {controller.frame+1}/{len(track.time)}\n"
                              "Space play/pause | R restart | A/D frame\n+/- speed | L loop | Q quit", ""))
            viewer.sync(state_only=True)
            time.sleep(max(0., 1/60 - (time.perf_counter()-started)))

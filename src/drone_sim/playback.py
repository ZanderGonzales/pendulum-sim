"""Replay saved Crazyflie states in MuJoCo without running the physics again.

Reference, physics, and hybrid tracks share one playback clock. Predictions are
visual-only colored mesh copies; no second physical drone is simulated.
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
PREDICTION_OPACITY = .55
PHYSICS_RGBA = (.1216, .4667, .7059, PREDICTION_OPACITY)
HYBRID_RGBA = (1., .498, .0549, PREDICTION_OPACITY)
REFERENCE_PATH_RGBA = (.7, .7, .7, .65)
CONTROL_HELP = ("Space: play/pause | R: restart | A/D: previous/next frame | +/-: speed | L: loop | "
                "1: physics | 2: physics+NN | 3: both | 0: MuJoCo only | Q: quit")


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


@dataclass(frozen=True)
class ComparisonTracks:
    """One reference plus optional predictions of that same flight on its grid."""

    reference: FlightTrack
    physics: FlightTrack | None = None
    hybrid: FlightTrack | None = None

    def __post_init__(self):
        for prediction in (self.physics, self.hybrid):
            if prediction is None:
                continue
            if (prediction.time.shape != self.reference.time.shape or
                    not np.allclose(prediction.time, self.reference.time, rtol=0, atol=1e-9)):
                raise ValueError("prediction and reference must share the same timestamp grid")
            expected, actual = self.reference.metadata.get("trajectory_id"), prediction.metadata.get("trajectory_id")
            if expected is not None and actual is not None and expected != actual:
                raise ValueError("prediction belongs to a different trajectory")

    @property
    def default_mode(self) -> str:
        if self.physics is not None and self.hybrid is not None:
            return "both"
        return "physics" if self.physics is not None else "hybrid" if self.hybrid is not None else "reference"

    def visible_predictions(self, mode: str) -> dict[str, FlightTrack]:
        if mode not in ("reference", "physics", "hybrid", "both"):
            raise ValueError("comparison must be reference, physics, hybrid, or both")
        selected = {name: track for name, track in (("physics", self.physics), ("hybrid", self.hybrid))
                    if mode == name or mode == "both"}
        if any(track is None for track in selected.values()):
            raise ValueError(f"comparison '{mode}' requires prediction tracks that were not loaded")
        return selected


def load_comparison(path: str | Path, *, trajectory_id: str | None = None) -> ComparisonTracks:
    """Load a phase-5 comparison archive or a legacy individual flight.

    Phase-5 archives contain truth_states, physics_states, hybrid_states with
    shape (trajectories,times,13). Select by saved ID; default to the first ID.
    One-step and recursive archives are both supported and labeled explicitly.
    """
    path = Path(path)
    if path.suffix.lower() != ".npz":
        raise ValueError("choose a saved .npz flight or comparison archive")
    with np.load(path, allow_pickle=False) as archive:
        if "truth_states" not in archive:
            track = load_flight(path)
            if trajectory_id is not None and track.metadata.get("trajectory_id") != trajectory_id:
                raise ValueError("trajectory ID does not match the individual flight")
            return ComparisonTracks(track)
        required = {"time", "trajectory_ids", "truth_states", "physics_states", "hybrid_states"}
        missing = required-set(archive.files)
        if missing:
            raise ValueError(f"comparison archive is missing: {', '.join(sorted(missing))}")
        ids = archive["trajectory_ids"]
        if ids.ndim != 1 or not len(ids) or ids.dtype.kind != "U" or len(set(ids.tolist())) != len(ids):
            raise ValueError("comparison trajectory_ids must be nonempty unique Unicode IDs")
        index = 0
        if trajectory_id is not None:
            found = np.flatnonzero(ids == trajectory_id)
            if not len(found):
                raise ValueError(f"unknown trajectory ID {trajectory_id!r}; available: {', '.join(ids.tolist())}")
            index = int(found[0])
        times = archive["time"]
        if times.ndim != 1:
            raise ValueError("comparison time must be a shared one-dimensional grid")
        metadata = json.loads(str(archive["metadata_json"].item())) if "metadata_json" in archive else {}
        if not isinstance(metadata, dict):
            raise ValueError("metadata_json must contain a JSON object")
        metadata = {**metadata, "trajectory_id": str(ids[index])}
        if "families" in archive:
            families = archive["families"]
            if families.shape != ids.shape or families.dtype.kind != "U":
                raise ValueError("comparison families must match trajectory IDs")
            metadata["family"] = str(families[index])
        tracks = []
        for name in ("truth_states", "physics_states", "hybrid_states"):
            states = archive[name]
            if states.shape != (len(ids), len(times), 13):
                raise ValueError(f"{name} must have shape (trajectories,times,13)")
            role = {"truth_states": "MuJoCo", "physics_states": "Physics only", "hybrid_states": "Physics+NN"}[name]
            tracks.append(FlightTrack(times, states[index], f"{ids[index]} | {role}", {**metadata, "role": role}))
        return ComparisonTracks(*tracks)


class PlaybackController:
    """Deterministic playback clock; no GUI, sleeping, or simulator dependence.

    Advance using elapsed monotonic wall time. Reference and predictions use
    this same timestamp; rendering never advances an independent clock.
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


def add_path(scene, track: FlightTrack, *, rgba=REFERENCE_PATH_RGBA, reset: bool = True, limit: int | None = None) -> None:
    """Add a small visual-only line of the recorded path, capped at 250 edges.

    This does not create another physical drone or alter reference-model XML.
    """
    indices = np.unique(np.linspace(0, len(track.time)-1, min(len(track.time), 251), dtype=int))
    if reset:
        scene.ngeom = 0
    maximum = scene.maxgeom if limit is None else min(scene.maxgeom, limit)
    for left, right in zip(indices[:-1], indices[1:]):
        start, end = track.states[left, :3], track.states[right, :3]
        if np.linalg.norm(end-start) < 1e-9:
            continue
        if scene.ngeom >= maximum:
            break
        geom = scene.geoms[scene.ngeom]
        mujoco.mjv_initGeom(geom, mujoco.mjtGeom.mjGEOM_CAPSULE, np.zeros(3), np.zeros(3),
                           np.eye(3).ravel(), np.asarray(rgba))
        mujoco.mjv_connector(geom, mujoco.mjtGeom.mjGEOM_CAPSULE, .0007, start, end)
        scene.ngeom += 1


class PredictionRenderer:
    """Append blue/orange visual mesh copies without altering reference state/materials."""

    def __init__(self, model, tracks: ComparisonTracks, *, opacity: float = PREDICTION_OPACITY):
        if not np.isfinite(opacity) or not 0 < opacity < 1:
            raise ValueError("prediction opacity must be strictly between 0 and 1")
        self.model, self.tracks = model, tracks
        self.colors = {"physics": (*PHYSICS_RGBA[:3], opacity), "hybrid": (*HYBRID_RGBA[:3], opacity)}
        self.data = {name: mujoco.MjData(model) for name, track in (("physics", tracks.physics), ("hybrid", tracks.hybrid)) if track is not None}
        self.option = mujoco.MjvOption()
        self.option.geomgroup[:] = 0
        self.option.geomgroup[2] = 1  # Stock visual meshes only, no collision hulls.
        self.option.flags[:] = 0
        self.camera = mujoco.MjvCamera()
        self.scratch = mujoco.MjvScene(model, maxgeom=max(64, model.ngeom+1))
        body = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, "cf2")
        self.visual_ids = set(np.flatnonzero((model.geom_bodyid == body) & (model.geom_group == 2)).tolist())
        self._scene, self._path_key, self._path_count = None, None, 0

    def update(self, scene, timestamp: float, mode: str, *, show_path: bool = True) -> None:
        selected = self.tracks.visible_predictions(mode)
        required = len(selected)*len(self.visual_ids)
        if required > scene.maxgeom:
            raise RuntimeError("custom scene has insufficient capacity for prediction meshes")
        path_key = (mode, show_path)
        if scene is not self._scene or path_key != self._path_key:
            scene.ngeom = 0
            if show_path:
                limit = scene.maxgeom-required
                add_path(scene, self.tracks.reference, reset=False, limit=limit)
                for name, track in selected.items():
                    add_path(scene, track, rgba=self.colors[name], reset=False, limit=limit)
            self._scene, self._path_key, self._path_count = scene, path_key, scene.ngeom
        scene.ngeom = self._path_count
        for name, track in selected.items():
            data = self.data[name]
            # Shared validated grid, shared clock, no interpolation or mj_step.
            apply_frame(self.model, data, track, self.tracks.reference.frame_at(timestamp))
            mujoco.mjv_updateScene(self.model, data, self.option, None, self.camera,
                                  mujoco.mjtCatBit.mjCAT_DYNAMIC, self.scratch)
            for source in self.scratch.geoms[:self.scratch.ngeom]:
                if source.objtype != mujoco.mjtObj.mjOBJ_GEOM or source.objid not in self.visual_ids:
                    continue
                destination = scene.geoms[scene.ngeom]
                mujoco.mjv_initGeom(destination, source.type, source.size, source.pos, source.mat.ravel(), np.asarray(self.colors[name]))
                destination.dataid = source.dataid  # Same model: existing GPU mesh buffers.
                destination.matid, destination.texid = -1, -1  # Use the overlay RGBA, not original materials.
                destination.objtype, destination.objid = mujoco.mjtObj.mjOBJ_UNKNOWN, -1
                destination.category, destination.segid = mujoco.mjtCatBit.mjCAT_DECOR, -1
                destination.modelrbound = source.modelrbound
                destination.transparent = 1
                scene.ngeom += 1


def playback_flight(
    flight: str | Path | FlightTrack | ComparisonTracks,
    *, speed: float = 1., paused: bool = False, loop: bool = False,
    follow: bool = False, show_path: bool = True,
    nn_prediction: FlightTrack | None = None,
    physics_prediction: FlightTrack | None = None,
    trajectory_id: str | None = None, comparison: str | None = None,
    prediction_opacity: float = PREDICTION_OPACITY,
) -> None:
    """Open a viewer until the user closes it; pause on the final saved frame.

    Phase-5 comparison archives provide all three tracks. Alternatively pass
    individual reference/prediction FlightTracks on the same timestamp grid.
    """
    if isinstance(flight, (str, Path)):
        tracks = load_comparison(flight, trajectory_id=trajectory_id)
    else:
        tracks = flight if isinstance(flight, ComparisonTracks) else ComparisonTracks(flight)
    if (physics_prediction is not None and tracks.physics is not None) or (nn_prediction is not None and tracks.hybrid is not None):
        raise ValueError("prediction supplied twice: choose a comparison archive or explicit prediction tracks")
    tracks = ComparisonTracks(tracks.reference, physics_prediction if physics_prediction is not None else tracks.physics,
                              nn_prediction if nn_prediction is not None else tracks.hybrid)
    mode = comparison if comparison is not None else tracks.default_mode
    tracks.visible_predictions(mode)
    track = tracks.reference
    controller = PlaybackController(track, speed=speed, paused=paused, loop=loop)
    simulator = DroneSimulator()
    renderer = PredictionRenderer(simulator.model, tracks, opacity=prediction_opacity)
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
    if tracks.default_mode != "reference":
        print(f"MuJoCo: original appearance | Physics only: BLUE | Physics+NN: ORANGE | "
              f"prediction opacity {prediction_opacity:g} | mode {mode}", flush=True)
    print("Drag the mouse to orbit/pan; scroll to zoom. Playback pauses at the end.", flush=True)
    with mujoco.viewer.launch_passive(simulator.model, simulator.data, key_callback=keys.put,
                                     show_left_ui=False, show_right_ui=False) as viewer:
        with viewer.lock():
            positions = np.concatenate([item.states[:, :3] for item in (tracks.reference, tracks.physics, tracks.hybrid) if item is not None])
            viewer.cam.lookat[:] = (positions.min(axis=0) + positions.max(axis=0))/2
            viewer.cam.distance = max(.45, float(np.ptp(positions, axis=0).max())*1.8)
            viewer.cam.azimuth, viewer.cam.elevation = 135., -25.
            if follow:
                viewer.cam.type = mujoco.mjtCamera.mjCAMERA_TRACKING
                viewer.cam.trackbodyid = simulator.body_id
            renderer.update(viewer.user_scn, controller.timestamp, mode, show_path=show_path)
            # MuJoCo also binds A/D to visual flags and R/L to render flags,
            # even with side panels hidden. Preserve those settings when our
            # playback shortcuts reuse the same keys.
            saved_visual_flags = {key: (flag, int(viewer.opt.flags[flag])) for key, flag in (
                (glfw.KEY_A, mujoco.mjtVisFlag.mjVIS_AUTOCONNECT),
                (glfw.KEY_D, mujoco.mjtVisFlag.mjVIS_STATIC))}
            saved_render_flags = {key: (flag, int(viewer.user_scn.flags[flag])) for key, flag in (
                (glfw.KEY_R, mujoco.mjtRndFlag.mjRND_REFLECTION),
                (glfw.KEY_L, mujoco.mjtRndFlag.mjRND_ADDITIVE))}
            # Native 0-3 keys toggle geom groups, including the reference drone.
            saved_geom_groups = {getattr(glfw, f"KEY_{i}"): (i, int(viewer.opt.geomgroup[i])) for i in range(4)}
            mode_keys = {glfw.KEY_0: "reference", glfw.KEY_1: "physics", glfw.KEY_2: "hybrid", glfw.KEY_3: "both"}
        last_wall_time = time.perf_counter()
        while viewer.is_running():
            started = time.perf_counter()
            controller.advance(started-last_wall_time)
            last_wall_time = started
            quit_requested = False
            restore_visual, restore_render, restore_groups = [], [], []
            while True:
                try:
                    key = keys.get_nowait()
                except Empty:
                    break
                if key == glfw.KEY_Q:
                    quit_requested = True
                elif key in mode_keys:
                    requested = mode_keys[key]
                    try:
                        tracks.visible_predictions(requested)
                    except ValueError as error:
                        print(str(error), flush=True)
                    else:
                        mode = requested
                    restore_groups.append(saved_geom_groups[key])
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
                for group, value in restore_groups:
                    viewer.opt.geomgroup[group] = value
                apply_frame(simulator.model, simulator.data, track, controller.frame)
                renderer.update(viewer.user_scn, controller.timestamp, mode, show_path=show_path)
            state = "PAUSED" if controller.paused else "PLAYING"
            viewer.set_texts((mujoco.mjtFontScale.mjFONTSCALE_100, mujoco.mjtGridPos.mjGRID_BOTTOMLEFT,
                              f"{track.label}\n{state} | {controller.speed:g}x | loop {'ON' if controller.loop else 'OFF'} | {mode}\n"
                              f"Time {controller.timestamp-track.time[0]:.2f} / {track.duration:.2f} s | frame {controller.frame+1}/{len(track.time)}\n"
                              "Space play/pause | R restart | A/D frame\n+/- speed | L loop | Q quit\n"
                              "1 Physics (blue) | 2 Physics+NN (orange) | 3 Both | 0 MuJoCo only\n"
                              f"Prediction opacity {prediction_opacity:g} | {track.metadata.get('mode', 'recorded flight')}", ""))
            viewer.sync(state_only=True)
            time.sleep(max(0., 1/60 - (time.perf_counter()-started)))

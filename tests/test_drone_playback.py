"""Playback timing, recorded-state fidelity, validation, and viewer integration."""

from itertools import count
from pathlib import Path

import mujoco
import numpy as np
import pytest

from drone_sim import DroneSimulator
from drone_sim.playback import (
    FlightTrack, MAX_SPEED, MIN_SPEED, PlaybackController, add_path,
    apply_frame, load_flight, playback_flight,
)


@pytest.fixture
def track():
    states = np.zeros((4, 13))
    states[:, 0] = [0., .1, .2, .3]
    states[:, 2] = 1.
    states[:, 3] = 1.
    states[:, 7] = .5
    return FlightTrack(np.array([2., 2.1, 2.4, 3.]), states, "Recorded flight")


def test_load_existing_trace_schema_without_modifying_source(tmp_path, track):
    path = tmp_path / "circle_flight.npz"
    states = track.states.copy()
    states[:, 3:7] *= 2
    np.savez_compressed(path, states=states, time=track.time, controls=np.zeros((3, 4)),
                        metadata_json='{"family": "circle"}')
    before = path.read_bytes()
    loaded = load_flight(path)
    np.testing.assert_allclose(loaded.states, track.states)
    np.testing.assert_array_equal(loaded.time, track.time)
    assert loaded.metadata == {"family": "circle"}
    assert loaded.label == "circle_flight"
    assert path.read_bytes() == before
    assert not loaded.states.flags.writeable and not loaded.time.flags.writeable
    assert np.all(states[:, 3] == 2.)


def test_playback_clock_uses_recorded_nonuniform_timestamps(track):
    controller = PlaybackController(track)
    assert controller.timestamp == 2. and controller.frame == 0
    controller.advance(.2)
    assert controller.timestamp == pytest.approx(2.2)
    assert controller.frame == 1
    controller.action("faster")
    controller.advance(.2)
    assert controller.timestamp == pytest.approx(2.6)
    assert controller.frame == 2
    controller.action("toggle_pause")
    controller.advance(100.)
    assert controller.timestamp == pytest.approx(2.6)
    controller.action("restart")
    assert controller.timestamp == 2. and controller.paused
    controller.action("toggle_pause")
    controller.advance(.1)
    assert controller.timestamp == pytest.approx(2.2)


def test_frame_stepping_pauses_and_clamps_at_both_ends(track):
    controller = PlaybackController(track)
    controller.action("previous")
    assert controller.frame == 0 and controller.paused
    controller.action("next")
    assert controller.timestamp == 2.1
    controller.action("next")
    assert controller.timestamp == 2.4
    controller.action("next")
    controller.action("next")
    assert controller.frame == 3 and controller.timestamp == 3.
    controller.action("previous")
    assert controller.timestamp == 2.4


def test_end_of_flight_pauses_and_resume_restarts(track):
    controller = PlaybackController(track)
    controller.advance(100.)
    assert controller.timestamp == 3. and controller.paused
    controller.advance(100.)
    assert controller.timestamp == 3.
    controller.action("toggle_pause")
    assert not controller.paused and controller.timestamp == 2.
    controller.action("restart")
    assert not controller.paused


def test_loop_keeps_remainder_and_speed_is_bounded(track):
    controller = PlaybackController(track, loop=True)
    controller.advance(3.25)
    assert controller.timestamp == pytest.approx(2.25)
    assert not controller.paused
    controller.action("toggle_loop")
    controller.advance(2.)
    assert controller.paused and controller.timestamp == 3.
    for _ in range(20):
        controller.action("faster")
    assert controller.speed == MAX_SPEED
    for _ in range(20):
        controller.action("slower")
    assert controller.speed == MIN_SPEED


def test_single_frame_recording_is_viewable_without_modulo_zero(track):
    single = FlightTrack(track.time[:1], track.states[:1])
    controller = PlaybackController(single, loop=True)
    controller.advance(100.)
    controller.action("toggle_pause")
    controller.action("next")
    assert controller.timestamp == 2. and controller.frame == 0 and controller.paused


def test_apply_frame_replays_pose_velocity_time_and_never_integrates(track, monkeypatch):
    simulator = DroneSimulator()
    def forbidden_step(*args):
        pytest.fail("saved-state playback must not advance physics")
    monkeypatch.setattr(mujoco, "mj_step", forbidden_step)
    for frame in (0, 3, 1):
        apply_frame(simulator.model, simulator.data, track, frame)
        np.testing.assert_allclose(simulator.state().as_array(), track.states[frame])
        assert simulator.data.time == track.time[frame]
        np.testing.assert_allclose(simulator.data.xpos[simulator.body_id], track.states[frame, :3])
    with pytest.raises(IndexError):
        apply_frame(simulator.model, simulator.data, track, -1)


def test_visual_path_is_bounded_and_skips_stationary_segments(track):
    simulator = DroneSimulator()
    scene = mujoco.MjvScene(simulator.model, maxgeom=2)
    add_path(scene, track)
    assert scene.ngeom == 2
    stationary = FlightTrack(track.time, np.repeat(track.states[:1], 4, axis=0))
    add_path(scene, stationary)
    assert scene.ngeom == 0


def test_prediction_overlay_is_explicitly_deferred(track):
    with pytest.raises(NotImplementedError, match="NN-prediction"):
        playback_flight(track, nn_prediction=track)


@pytest.mark.parametrize("times,shape", [([], (0, 13)), ([0, 0], (2, 13)), ([1, 0], (2, 13)),
                                        ([0, np.nan], (2, 13)), ([[0, 1]], (2, 13)),
                                        ([0, 1], (2, 7)), ([0, 1], (1, 13))])
def test_invalid_times_and_shapes(times, shape):
    with pytest.raises(ValueError):
        FlightTrack(times, np.zeros(shape))


def test_invalid_states_are_rejected(track):
    for column, value in ((0, np.inf), (3, 0.)):
        states = track.states.copy()
        states[0, column] = value
        with pytest.raises(ValueError):
            FlightTrack(track.time, states)


@pytest.mark.parametrize("speed", [0, -1, np.nan, np.inf, .01, 9])
def test_invalid_speed(track, speed):
    with pytest.raises(ValueError, match="speed"):
        PlaybackController(track, speed=speed)


def test_invalid_clock_actions(track):
    controller = PlaybackController(track)
    for elapsed in (-1, np.nan, np.inf):
        with pytest.raises(ValueError):
            controller.advance(elapsed)
    with pytest.raises(ValueError):
        controller.action("unknown")


def test_missing_or_invalid_archive_data(tmp_path, track):
    with pytest.raises(FileNotFoundError):
        load_flight(tmp_path / "missing.npz")
    with pytest.raises(ValueError):
        load_flight(Path("not-a-recording.csv"))
    path = tmp_path / "flight.npz"
    np.savez(path, position=track.states[:, :3])
    with pytest.raises(ValueError, match="missing required"):
        load_flight(path)
    for metadata in ('[]', 'not JSON'):
        np.savez(path, states=track.states, time=track.time, metadata_json=metadata)
        with pytest.raises(ValueError, match="metadata_json"):
            load_flight(path)
    np.savez(path, states=np.array([object()], dtype=object), time=track.time)
    with pytest.raises(ValueError):
        load_flight(path)


def test_viewer_loop_applies_recorded_frames_and_handles_queued_controls(track, monkeypatch):
    import glfw
    import mujoco.viewer
    import drone_sim.playback as playback

    observed = []
    class Viewer:
        def __init__(self, model, data, key_callback, **kwargs):
            self.model, self.data, self.callback = model, data, key_callback
            self.cam = mujoco.MjvCamera()
            self.opt = mujoco.MjvOption()
            self.user_scn = mujoco.MjvScene(model, maxgeom=300)
        def __enter__(self):
            return self
        def __exit__(self, *args):
            pass
        def lock(self):
            from contextlib import nullcontext
            return nullcontext()
        def is_running(self):
            return len(observed) < 4
        def set_texts(self, text):
            assert "Recorded flight" in text[2]
        def sync(self, **kwargs):
            observed.append(self.data.qpos.copy())
            self.callback(glfw.KEY_RIGHT if len(observed) < 3 else glfw.KEY_Q)

    monkeypatch.setattr(mujoco.viewer, "launch_passive", Viewer)
    monkeypatch.setattr(playback.time, "perf_counter", lambda ticks=count(): next(ticks)*.001)
    monkeypatch.setattr(playback.time, "sleep", lambda _: None)
    monkeypatch.setattr(mujoco, "mj_step", lambda *args: pytest.fail("playback called mj_step"))
    playback_flight(track, paused=True)
    assert len(observed) == 3
    np.testing.assert_allclose(observed, track.states[:3, :7])

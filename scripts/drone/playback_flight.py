"""Watch a saved *_flight.npz file using MuJoCo's interactive viewer."""

import argparse
from pathlib import Path

from drone_sim.playback import CONTROL_HELP, playback_flight


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, epilog=CONTROL_HELP)
    parser.add_argument("flight", type=Path, help="Saved flight, e.g. runs/Drone/drone_run_1/circle_flight.npz")
    parser.add_argument("--speed", type=float, default=1., help="Initial playback speed, 0.125 to 8 (default: 1)")
    parser.add_argument("--paused", action="store_true", help="Start paused at the first frame")
    parser.add_argument("--loop", action="store_true", help="Repeat continuously")
    parser.add_argument("--follow", action="store_true", help="Start with the camera following the drone")
    parser.add_argument("--hide-path", action="store_true", help="Hide the recorded path line")
    args = parser.parse_args()
    try:
        playback_flight(args.flight, speed=args.speed, paused=args.paused, loop=args.loop,
                        follow=args.follow, show_path=not args.hide_path)
    except KeyboardInterrupt:
        pass
    except (OSError, ValueError, RuntimeError) as error:
        parser.exit(2, f"Playback error: {error}\n")


if __name__ == "__main__":
    main()

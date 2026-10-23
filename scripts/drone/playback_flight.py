"""Watch recorded flights or phase-5 reference/physics/NN comparisons in MuJoCo."""

import argparse
from pathlib import Path

from drone_sim.playback import CONTROL_HELP, PREDICTION_OPACITY, playback_flight


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, epilog=CONTROL_HELP)
    parser.add_argument("flight", type=Path, help="Individual flight or comparison archive, e.g. runs/Drone/phase_5/predictions/test_recursive.npz")
    parser.add_argument("--trajectory-id", help="ID inside a comparison archive; default: first saved trajectory")
    parser.add_argument("--compare", choices=("physics", "hybrid", "both", "reference"),
                        help="Show physics only, physics+NN, both, or MuJoCo only alongside the reference; default: all available")
    parser.add_argument("--prediction-opacity", type=float, default=PREDICTION_OPACITY,
                        help="Blue/orange drone opacity, strictly between 0 and 1 (default: 0.55)")
    parser.add_argument("--speed", type=float, default=1., help="Initial playback speed, 0.125 to 8 (default: 1)")
    parser.add_argument("--paused", action="store_true", help="Start paused at the first frame")
    parser.add_argument("--loop", action="store_true", help="Repeat continuously")
    parser.add_argument("--follow", action="store_true", help="Start with the camera following the drone")
    parser.add_argument("--hide-path", action="store_true", help="Hide all path lines while keeping drones visible")
    args = parser.parse_args()
    try:
        playback_flight(args.flight, speed=args.speed, paused=args.paused, loop=args.loop,
                        follow=args.follow, show_path=not args.hide_path, trajectory_id=args.trajectory_id,
                        comparison=args.compare, prediction_opacity=args.prediction_opacity)
    except KeyboardInterrupt:
        pass
    except (OSError, ValueError, RuntimeError) as error:
        parser.exit(2, f"Playback error: {error}\n")


if __name__ == "__main__":
    main()

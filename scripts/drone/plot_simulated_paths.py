"""Demonstrate all Phase 1 flights; save real simulation plots and failure logs.

This is a six-flight demonstration, not the Phase 2 training dataset pipeline.
"""

import argparse
import csv
import json
from pathlib import Path
import subprocess

import numpy as np

from drone_sim import DroneSimulator, FLIGHT_FAMILIES, FlightReference, SimulationConfig, simulate_flight
from drone_sim.plotting import plot_flight, plot_path_summary


def next_run(root: Path) -> tuple[Path, int]:
    root.mkdir(parents=True, exist_ok=True)
    number = 1
    while (root / f"drone_run_{number}").exists():
        number += 1
    target = root / f"drone_run_{number}"
    target.mkdir()
    return target, number


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=Path("runs/Drone"))
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--duration", type=float, default=10.)
    parser.add_argument("--dt", type=float, default=.01)
    parser.add_argument("--internal-dt", type=float, default=.002)
    parser.add_argument("--render", action="store_true", help="Also save an offscreen MuJoCo scene image (requires OpenGL)")
    args = parser.parse_args()
    config = SimulationConfig(args.dt, args.internal_dt, args.duration)
    simulator = DroneSimulator(config)
    output, number = next_run(args.output_root)
    plots = output / "plots"
    plots.mkdir()
    flights, summary, failures = {}, [], []
    for family in FLIGHT_FAMILIES:
        flight = simulate_flight(simulator, FlightReference(family, args.duration, args.seed))
        flights[family] = flight
        error = np.linalg.norm(flight.states[:, :3] - flight.reference_positions, axis=1)
        row = {"family": family, "valid_for_learning": flight.valid_for_learning,
               "completed_steps": len(flight.controls), "contact_steps": int(flight.contacts.sum()),
               "position_tracking_mae_m": float(error.mean()), "maximum_tracking_error_m": float(error.max()),
               "failure_reason": flight.failure_reason}
        summary.append(row)
        if not flight.valid_for_learning:
            failures.append(row)
        # Raw flight traces support inspection/replay, without a train/val/test split.
        np.savez_compressed(output / f"{family}_flight.npz", states=flight.states, time=flight.time,
                            requested_controls=flight.requested_controls, controls=flight.controls,
                            actuator_controls=flight.actuator_controls, contacts=flight.contacts,
                            reference_positions=flight.reference_positions, reference_yaw=flight.reference_yaw,
                            metadata_json=json.dumps({**flight.metadata, "valid_for_learning": flight.valid_for_learning,
                                                      "failure_reason": flight.failure_reason}))
        plot_flight(flight, plots, family)
        print(f"{family}: valid={flight.valid_for_learning}, steps={len(flight.controls)}, "
              f"mean tracking distance={error.mean():.5f} m, max={error.max():.5f} m")
    plot_path_summary(flights, plots / "path_comparison_summary.png")
    with (output / "simulation_metrics.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(summary[0]))
        writer.writeheader()
        writer.writerows(summary)
    (output / "failed_trajectories.json").write_text(json.dumps(failures, indent=2) + "\n", encoding="utf-8")
    revision = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=False)
    dirty = subprocess.run(["git", "status", "--porcelain", "--untracked-files=normal"], capture_output=True, text=True, check=False)
    metadata = {"phase": 1, "experiment": number, "seed": args.seed,
                "code_revision": revision.stdout.strip() or "unavailable", "working_tree_dirty": bool(dirty.stdout.strip()),
                "simulation": simulator.metadata(), "flights": {name: f.metadata for name, f in flights.items()},
                "summary": summary, "training": "Not run: simulation demonstration only"}
    if args.render:
        import mujoco
        with mujoco.Renderer(simulator.model, height=480, width=640) as renderer:
            renderer.update_scene(simulator.data, camera="track")
            import matplotlib.pyplot as plt
            plt.imsave(plots / "crazyflie_scene.png", renderer.render())
        metadata["rendered_scene"] = "plots/crazyflie_scene.png"
    (output / "run_metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    lines = [f"# Experiment {number} Data: Drone Phase 1", "",
             "Six controlled MuJoCo flights; no training, learned model, or train/validation/test split.", "",
             f"- Seed: {args.seed}", f"- Prediction interval: {args.dt} s; internal interval: {args.internal_dt} s",
             f"- Requested duration: {args.duration} s per family; {config.num_steps} transitions each",
             f"- Valid flights: {sum(f.valid_for_learning for f in flights.values())}/6", "",
             "## Artifacts", "",
             "- `plots/path_comparison_summary.png`: controller reference and actual MuJoCo paths.",
             "- `plots/<family>_state_comparison.png`: position, velocity, tracking error, applied moments.",
             "- `<family>_flight.npz`: N+1 full states, N requested/applied physical controls and raw actuator controls, contacts, references, timing, JSON metadata.",
             "- `simulation_metrics.csv`: per-flight validity and reference-tracking errors in metres.",
             "- `failed_trajectories.json`: rejected flights and reasons; empty when all flights are valid.",
             "- `run_metadata.json`: physical parameters, simulator/model versions, controller gains, reference paths, initial states, code revision, and seed.", "",
             "## Interpretation", "",
             "Tracking error measures the flight controller's ability to follow its reference. It is not an NN prediction error. "
             "Interpret curves manually; no model-fidelity acceptance threshold is imposed.", "",
             "## Changes and next phase", "",
             "Phase 1 adds the pinned reference simulator and controller. No earlier drone learning experiment exists. "
             "Phase 2 will add larger seeded datasets, coverage plots, storage/loading, and trajectory splits.", ""]
    (output / f"Experiment {number} Data.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Saved demonstration: {output}")
    if failures:
        raise SystemExit("Some flights failed; inspect failed_trajectories.json")


if __name__ == "__main__":
    main()

"""Generate complete drone trajectories, fixed splits, and a held-out-family benchmark."""

import argparse
from dataclasses import asdict
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import numpy as np

from drone_sim.artifacts import next_phase
from drone_sim.controls import FLIGHT_FAMILIES
from drone_sim.dataset import (DatasetConfig, DatasetGenerationError, dataset_summary, export_trajectory,
                               generate_benchmark_dataset, generate_dataset, save_dataset)
from drone_sim.plotting import plot_dataset_coverage, plot_path_summary
from drone_sim.types import SimulationConfig


def write_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def trajectory_rows(dataset) -> list:
    rows = []
    for i, record in enumerate(dataset.metadata["trajectories"]):
        error = np.linalg.norm(dataset.states[i, :, :3]-dataset.reference_positions[i], axis=1)
        saturated = np.any(np.abs(dataset.controls[i]-dataset.requested_controls[i]) > 1e-12, axis=1)
        rows.append({"trajectory_id": str(dataset.trajectory_ids[i]), "split": str(dataset.split[i]),
                     "family": str(dataset.families[i]), "seed": record["seed"], "attempt": record["attempt"],
                     "transitions": len(dataset.controls[i]), "initial_height_m": float(dataset.states[i, 0, 2]),
                     "motion_scale": record["reference_parameters"]["motion_scale"],
                     "position_tracking_mae_m": float(error.mean()),
                     "position_tracking_rmse_m": float(np.sqrt(np.mean(error**2))),
                     "maximum_tracking_error_m": float(error.max()),
                     "saturated_transition_fraction": float(saturated.mean())})
    return rows


def write_report(output: Path, number: int, config, main, benchmark, metadata, exported: list) -> None:
    lines = [f"# Phase {number} Data: Drone Dataset Generation", "",
             "## Results", "",
             f"- Main dataset: {len(main.states)} complete trajectories, with {main.metadata['split_counts']}.",
             f"- Separate benchmark: {len(benchmark.states)} complete {config.held_out_family} trajectories.",
             f"- Each trajectory: {config.simulation.num_steps} transitions, {len(main.time)} full states, {config.simulation.duration:g} seconds.",
             f"- Prediction/control interval: {config.simulation.dt:g} s; internal RK4 step: {config.simulation.internal_dt:g} s.",
             f"- Rejected attempts: {len(metadata['failed_trajectories'])}; all saved trajectories are complete and contact-free.",
             f"- Root dataset seed: {config.seed}.", "",
             "## How the data are generated", "",
             "Each trajectory is a controlled MuJoCo simulation. Seeded draws vary world placement, height, yaw, path scale, "
             "circle/figure-eight cycle count, initial roll/pitch, linear velocity, and angular velocity. "
             "The five main families are balanced within each split up to integer remainders. "
             "Hover changes placement and initial disturbance, not its reference path shape. "
             "The benchmark family is excluded from training, validation, and the ordinary test set.", "",
             "## Why these splits are used", "",
             "Complete trajectories stay in one split so neighboring timesteps cannot leak into validation or testing. "
             "The ordinary test split contains new trajectories from familiar families. "
             "The separate benchmark tests a family absent from all main splits. "
             "Keep it out of checkpoint selection and hyperparameter tuning when claiming held-out-family generalization.", "",
             "IDs use <split>_<within-split index>. Seeds are derived from the root seed, split code, within-split index, "
             "and retry number. Family ordering is fixed per split. Increasing the training count retains existing "
             "training flights and leaves validation, test, and benchmark flights unchanged when other settings are fixed.", "",
             "## Saved arrays and units", "",
             "- `time`: shared seconds, shape (steps+1,).",
             "- `states`: shape (trajectories, steps+1, 13), ordered [x,y,z,qw,qx,qy,qz,vx,vy,vz,wx,wy,wz].",
             "- Position and linear velocity are world-frame metres and metres/second; angular velocity is body-frame radians/second.",
             "- Orientations are normalized scalar-first wxyz quaternions rotating body vectors to world coordinates.",
             "- `controls`: actual applied [thrust, moment_x, moment_y, moment_z], shape (trajectories, steps, 4), in N and N m.",
             "- `requested_controls` and `actuator_controls`: physical requests before clipping and raw MuJoCo actuator commands.",
             "- `contacts`: shape (trajectories, steps), false for all accepted trajectories.",
             "- `reference_positions` / `reference_yaw`: desired positions and headings at the state sample times.",
             "- `trajectory_ids`, `families`, `split`: one stable ID, family, and split per trajectory.",
             "- `metadata_json`: schema version, model revision, physical and controller settings, randomization ranges, "
             "per-flight initial states, path parameters, seeds, and failed-attempt records.", "",
             "The states at k and k+1 pair with controls[k], held across that prediction interval. "
             "`dataset.samples('train')` exposes those one-step records while keeping trajectory and step IDs. "
             "No residual target is calculated here; that requires the independent physics predictor. "
             "Data remain in physical units. Fit later feature/target normalizers using only the train split, "
             "then freeze them for validation, testing, and the benchmark.", "",
             "## Artifacts", "",
             "- `dataset.npz`: the main train/validation/test dataset; load with drone_sim.dataset.load_dataset.",
             "- `benchmark_dataset.npz`: the held-out-family dataset, labeled benchmark only.",
             "- `trajectory_manifest.csv`: stable IDs, seeds, split/family labels, lengths, tracking errors, and saturation rates.",
             "- `coverage_summary.json`: per-split trajectory/family counts, physical state/control ranges, and saturation fractions.",
             "- `plots/state_coverage.png`, `plots/control_coverage.png`, `plots/trajectory_family_counts.png`: coverage diagnostics.",
             "- `plots/path_comparison_summary.png`: preselected ordinary test examples and one benchmark flight.",
             "- `flights/`: preselected examples in the existing playback-compatible single-flight format.",
             "- `failed_trajectories.json`: deterministic rejected attempts, reasons, and reproduction settings.",
             "- `run_metadata.json`: configuration, code revision/dirty state, source hashes, model settings, and summaries.", "",
             "## Reproduction and inspection", "", "```powershell", metadata["command"], "```", ""]
    if exported:
        lines += ["For example, inspect an exported flight using:", "", "```powershell",
                  f"python scripts/drone/playback_flight.py {exported[0]} --paused", "```", ""]
    lines += ["## Interpretation and limitations", "",
              "Coverage plots show what this dataset contains, not proof of uniform coverage of all possible drone motion. "
              "All flights use one mass/inertia configuration, still air, the same controller, and conservative flight envelopes. "
              "Yaw/position changes add geometric variety; path scale, cycle count, and initial disturbances vary the actual motion. "
              "Retrying failed flights conditions the dataset on valid flight; inspect rejected attempts when comparing datasets.", "",
              "Tracking errors compare the simulated vehicle with the controller reference. They are not learned-model errors. "
              "There is no automatic fidelity threshold and no NN training in this run. "
              "The next model component will predict basic rigid-body motion so one-step physics errors can be formed.", "",
              "## Changes from earlier drone work", "",
              "Earlier outputs contained six individual demonstration flights. This run adds multiple seeded trajectories, "
              "stable splits, a separate family benchmark, validated save/load, transition access, and coverage diagnostics. "
              "Drone_Plan.md and README.md were not edited during this implementation.", ""]
    (output / f"Phase {number} Data.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=Path("runs/Drone"))
    parser.add_argument("--train-trajectories", type=int, default=80)
    parser.add_argument("--validation-trajectories", type=int, default=10)
    parser.add_argument("--test-trajectories", type=int, default=10)
    parser.add_argument("--benchmark-trajectories", type=int, default=10)
    parser.add_argument("--held-out-family", choices=FLIGHT_FAMILIES, default="waypoints")
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--duration", type=float, default=10.)
    parser.add_argument("--dt", type=float, default=.01)
    parser.add_argument("--internal-dt", type=float, default=.002)
    parser.add_argument("--max-attempts", type=int, default=5)
    args = parser.parse_args()
    try:
        config = DatasetConfig(args.train_trajectories, args.validation_trajectories, args.test_trajectories,
                               args.benchmark_trajectories, args.held_out_family, args.seed,
                               SimulationConfig(args.dt, args.internal_dt, args.duration),
                               max_attempts_per_trajectory=args.max_attempts)
    except ValueError as error:
        parser.error(str(error))
    output, number = next_phase(args.output_root, 2)
    root = Path(__file__).resolve().parents[2]
    revision = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True, check=False)
    dirty = subprocess.run(["git", "status", "--porcelain"], cwd=root, capture_output=True, text=True, check=False)
    sources = sorted((root / "src/drone_sim").glob("*.py")) + [Path(__file__).resolve()]
    metadata = {"status": "generating", "phase": number, "dataset_config": asdict(config),
                "command": subprocess.list2cmdline(["python", "scripts/drone/generate_dataset.py", *sys.argv[1:]]),
                "code_revision": revision.stdout.strip(), "working_tree_dirty": bool(dirty.stdout.strip()),
                "source_sha256": {path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest() for path in sources}}
    write_json(output / "run_metadata.json", metadata)
    total = config.train_count + config.validation_count + config.test_count + config.benchmark_count
    completed = 0

    def progress(row):
        nonlocal completed
        if row["accepted"]:
            completed += 1
            if completed % 10 == 0 or completed == total:
                print(f"Accepted {completed}/{total}: {row['trajectory_id']} ({row['family']})", flush=True)
        else:
            print(f"Rejected {row['trajectory_id']}, attempt {row['attempt']}: {row['failure_reason']}", flush=True)

    print(f"Generating {total} complete flights into {output}", flush=True)
    dataset = None
    try:
        dataset = generate_dataset(config, progress)
        benchmark = generate_benchmark_dataset(config, progress)
    except DatasetGenerationError as error:
        failures = ([] if dataset is None else dataset.metadata["failed_trajectories"]) + error.failures
        metadata.update({"status": "failed", "failure_reason": str(error), "failed_trajectories": failures})
        write_json(output / "failed_trajectories.json", failures)
        write_json(output / "run_metadata.json", metadata)
        raise SystemExit(str(error)) from error
    failures = dataset.metadata["failed_trajectories"] + benchmark.metadata["failed_trajectories"]
    save_dataset(dataset, output / "dataset.npz")
    save_dataset(benchmark, output / "benchmark_dataset.npz")
    summary = {"main": dataset_summary(dataset), "benchmark": dataset_summary(benchmark)}
    write_json(output / "coverage_summary.json", summary)
    write_json(output / "failed_trajectories.json", failures)
    rows = trajectory_rows(dataset) + trajectory_rows(benchmark)
    with (output / "trajectory_manifest.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    examples, exported = {}, []
    for family in FLIGHT_FAMILIES:
        source = benchmark if family == config.held_out_family else dataset
        mask = (source.families == family) & (source.split == ("benchmark" if source is benchmark else "test"))
        indices = np.flatnonzero(mask)
        if len(indices):
            index = int(indices[0])
            path = output / "flights" / f"{source.trajectory_ids[index]}.npz"
            export_trajectory(source, index, path)
            exported.append(path.as_posix())
            examples[family] = source.trajectory(index)
    plot_dataset_coverage(dataset, benchmark, output / "plots")
    plot_path_summary(examples, output / "plots/path_comparison_summary.png",
                      title="Drone dataset: preselected test and held-out-family flights")
    metadata.update({"status": "complete", "simulation": dataset.metadata["simulation"], "coverage": summary,
                     "failed_trajectories": failures, "exported_examples": exported,
                     "total_transitions": len(rows)*config.simulation.num_steps})
    write_json(output / "run_metadata.json", metadata)
    write_report(output, number, config, dataset, benchmark, metadata, exported)
    print(f"Saved {len(dataset.states)} main and {len(benchmark.states)} benchmark trajectories; {len(failures)} rejected attempts.", flush=True)
    print(f"Results and theory: {output / f'Phase {number} Data.md'}", flush=True)


if __name__ == "__main__":
    main()

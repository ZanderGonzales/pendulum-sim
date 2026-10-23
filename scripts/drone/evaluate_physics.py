"""Verify phase-3 rigid-body dynamics and evaluate the saved phase-2 flights.

Default outputs: runs/Drone/phase_3/ (repeat_N subfolders preserve prior output).
No training, fitted parameters, truth refreshes, or online flight controller.
"""

import argparse
import csv
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import numpy as np

from drone_sim import DroneSimulator, RigidBodyParameters, RigidBodyPhysics, SimulationConfig, load_dataset
from drone_sim.artifacts import next_phase
from drone_sim.evaluation import (one_step_predictions, one_step_residuals, summarize_metrics, trajectory_metrics)
from drone_sim.plotting import plot_fluid_isolation, plot_physics_errors, plot_physics_flight
from drone_sim.verification import compare_without_fluid, verify_analytic_motion


def write_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, allow_nan=False)+"\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def metric_rows(dataset, prediction, indices, mode: str) -> list[dict]:
    return [{"trajectory_id": str(dataset.trajectory_ids[index]), "split": str(dataset.split[index]),
             "family": str(dataset.families[index]), "predictor": "physics_only", "mode": mode,
             **trajectory_metrics(prediction[i], dataset.states[index])}
            for i, index in enumerate(indices)]


def summarize_by_split(rows):
    return {label: summarize_metrics([row for row in rows if row["split"] == label])
            for label in dict.fromkeys(row["split"] for row in rows)}


def write_report(output: Path, metadata, one_step, recursive, diagnostics):
    p, timing = metadata["physics_parameters"], metadata["prediction_config"]
    lines = ["# Phase 3 Data: Basic Rigid-Body Physics Predictor", "",
             "## Results", "",
             "The independent predictor is implemented and evaluated against the existing phase-2 MuJoCo flights. "
             "No NN was trained, no parameters were fitted, and no artificial model mismatch was introduced.", "",
             f"- Mass: {p['mass']:g} kg; principal inertias: {p['inertia']} kg m^2.",
             f"- World gravity: {p['gravity']} m/s^2.",
             f"- Prediction interval: {timing['dt']:g} s; internal RK4 interval: {timing['internal_dt']:g} s.",
             f"- One-step evaluation: {metadata['one_step_transitions']:,} transitions over all main and benchmark flights.",
             f"- Recursive evaluation: {metadata['recursive_trajectories']} test/benchmark flights, {timing['duration']:g} s each.",
             "- Analytic checks: free fall, hover balance, tilted thrust, and single-axis rotational response passed.", ""]
    for label in recursive:
        lines += [f"### {label.capitalize()} trajectories", ""]
        for mode, summary in (("One-step (true current state)", one_step[label]),
                              ("Recursive (predicted current state, no refresh)", recursive[label])):
            lines += [f"- **{mode}**, {summary['trajectories']} flights: mean position MAE "
                      f"**{summary['mean_position_mae_m']:.9g} m**, std {summary['std_position_mae_m']:.9g} m; "
                      f"mean orientation MAE **{summary['mean_orientation_mae_rad']:.9g} rad "
                      f"({summary['mean_orientation_mae_deg']:.9g} deg)**, std "
                      f"{summary['std_orientation_mae_rad']:.9g} rad.",
                      f"  Mean final position error: {summary['mean_final_position_error_m']:.9g} m; "
                      f"mean maximum position error: {summary['mean_maximum_position_error_m']:.9g} m."]
        lines.append("")
    lines += ["## Fluid-isolation comparison", "",
              f"An isolated MuJoCo instance had density and viscosity set to zero for {diagnostics['samples']} "
              f"one-step samples ({diagnostics['samples_per_trajectory']} evenly spaced transitions per training flight). "
              "Each sample begins at the same true current state and uses the same applied controls as the normal reference. "
              "This isolates frame, sign, inertia, and integration discrepancies without changing the saved dataset.", ""]
    for label, summary in diagnostics["comparisons"].items():
        lines += [f"- **{label}**: mean/max position discrepancy "
                  f"{summary['mean_position_m']:.9g} / {summary['max_position_m']:.9g} m; "
                  f"mean/max orientation discrepancy {summary['mean_orientation_rad']:.9g} / "
                  f"{summary['max_orientation_rad']:.9g} rad; mean linear/angular velocity discrepancy "
                  f"{summary['mean_linear_velocity_m_s']:.9g} m/s / {summary['mean_angular_velocity_rad_s']:.9g} rad/s."]
    lines += ["", "The fluid-free difference is a numerical diagnostic, not a target fidelity threshold. "
              "Classical RK4 integrates the quaternion differential equation here, whereas MuJoCo's RK4 uses "
              "tangent-space quaternion position integration. Small finite-step differences are expected, especially "
              "for changing rotation axes. The normal residual also includes the intentionally omitted fluid forces.", "",
              "## Governing equations and frames", "",
              "Let p and v be world-frame position and velocity, q the scalar-first body-to-world quaternion, "
              "and omega the body-frame angular velocity. The body origin is its centre of mass and body axes "
              "are principal inertia axes in this pinned model. T is applied total thrust, tau applied body moments, "
              "and I the diagonal principal inertia matrix.", "",
              "$$\\dot p=v,\\qquad \\dot v=g_{world}+\\frac{T}{m}R(q)e_z$$", "",
              "$$\\dot\\omega=I^{-1}\\left(\\tau-\\omega\\times(I\\omega)\\right)$$", "",
              "$$\\dot q=\\tfrac12 q\\otimes[0,\\omega]$$", "",
              "`RigidBodyPhysics._derivative` implements these equations directly in NumPy. "
              "The cross product is the gyroscopic coupling from Euler's rotational equation. "
              "Thrust acts along body +z and is rotated into world coordinates; moments use the body-frame right-hand rule. "
              "World gravity is constant. Body-frame gravity would be R(q).T @ g_world; it changes with attitude "
              "but is not an additional force.", "",
              f"`step_array` holds the applied wrench constant while taking {round(timing['dt']/timing['internal_dt'])} "
              f"classical RK4 substeps of {timing['internal_dt']:g} s per {timing['dt']:g} s prediction. "
              "Each substep evaluates four derivative stages and then normalizes "
              "the quaternion. `step` provides the same transition using DroneState and DroneControl. "
              "No MuJoCo dynamics function is called by the predictor. Its properties are copied from recorded "
              "model metadata. Actuator scaling and clipping happen upstream; feeding raw actuator commands here is incorrect.", "",
              "The normal simulator retains density 1.225 kg/m^3 and viscosity 1.8e-5 Pa s in still air. "
              "The stock model uses MuJoCo's inertia-based fluid resistance. The basic predictor omits that "
              "resistance, contact, wind corrections, and rotor dynamics. It does not stop when a predicted flight "
              "crosses the floor: these are contact-free flight equations, not a contact simulator.", "",
              "References: [MuJoCo fluid forces](https://mujoco.readthedocs.io/en/stable/computation/fluid.html), "
              "[pinned MuJoCo 3.16.0 RK4 implementation](https://github.com/google-deepmind/mujoco/blob/3.16.0/src/engine/engine_forward.c).", "",
              "## One-step residual and recursive prediction", "",
              "One-step evaluation starts each transition at the true simulator current state. Its error "
              "measures the correction a future residual NN must learn. Recursive prediction starts with truth "
              "only at t=0 and uses predicted states thereafter. Both replay the saved applied-control sequence; "
              "the flight controller is not rerun or given simulator truth during prediction. "
              "Small one-step errors can accumulate into substantial drift over 1,000 recursive transitions.", "",
              "The saved diagnostic residual has 12 coordinates: position difference (3), linear velocity difference (3), "
              "orientation rotation vector (3), and angular velocity component difference (3), always simulator minus physics. "
              "Position and velocity differences use the current true state's body axes. "
              "The orientation vector is Log(R_physics_next.T @ R_sim_next), a right-composed correction "
              "in the predicted next body axes. Angular velocity differences subtract the state components in "
              "their respective body axes. Orientations are never subtracted as four quaternion components. "
              "q and -q represent the same orientation and give the same angle error.", "",
              "These are finite-step errors, not acceleration targets or a complete state increment. "
              "No features, fitted standardizers, NN, optimizer, or truth-refresh mechanism have been added. "
              "Phase 4 can use these physics transitions and residual measurements when defining the learning pipeline.", "",
              "## Metric definitions", "",
              "Position MAE is the mean Euclidean position distance over predicted timestamps; position RMSE "
              "is the square root of the mean squared distance. Orientation uses the shortest absolute rotation "
              "angle in [0, pi], with MAE/RMSE in radians and degrees. Velocity MAE/RMSE similarly use vector "
              "norms in m/s and rad/s. Angular velocities are compared as body-frame state components. "
              "The shared exact initial state is excluded from means and maxima; final error is at the last timestamp.", "",
              "Each split-level mean averages its per-trajectory metrics with equal flight weight. "
              "Standard deviations describe variation between trajectory metrics, using ddof=0. "
              "One-step and recursive results remain separate, as do ordinary tests and the waypoint benchmark. "
              "All per-trajectory velocity errors, RMSEs, and position/orientation errors are saved in CSV; "
              "all their equal-weight means and standard deviations are saved in JSON and comparison CSV.", "",
              "## Artifacts and interfaces", "",
              "- `one_step_metrics.csv` / `.json`: per-flight and per-split metrics for train, validation, test, benchmark.",
              "- `rollout_metrics.csv` / `.json`: physics-only, no-refresh recursive test and benchmark metrics.",
              "- `test_metrics.json`: one-step and recursive summaries for test and benchmark, including both mean MAEs.",
              "- `comparison_metrics.csv`: split/mode summary rows, including mean MAEs and standard deviations.",
              "- `sanity_checks.json`: analytic check results and numerical discrepancies.",
              "- `fluid_comparison.json` / `predictions/fluid_comparison.npz`: matched fluid-on/fluid-off diagnostics.",
              "- `predictions/one_step_main.npz` and `one_step_benchmark.npz`: predicted full states, 12D residuals, time, IDs, families, splits, residual convention metadata.",
              "- `predictions/recursive_test.npz` and `recursive_benchmark.npz`: predicted full states, time, IDs, families, applied controls, no-refresh metadata.",
              "- `plots/one_step_errors.png`: mean one-step errors by split with one-standard-deviation bands.",
              "- `plots/recursive_errors.png`: mean recursive test/benchmark errors with variability bands.",
              "- `plots/fluid_isolation.png`: matched one-step discrepancies on a logarithmic scale.",
              "- `plots/<split>_<trajectory_id>_physics.png`: first flight of each family, preselected by saved index, not accuracy.",
              "- `run_metadata.json`: source-data hashes, source-code hashes, code revision, model provenance, timing, properties, exact command.", "",
              "The physics API is `RigidBodyPhysics(parameters, config).step(state, applied_control)`; "
              "`step_array` also accepts batches with matching leading shapes. "
              "`rollout(initial_states, applied_controls)` accepts no future truth. "
              "The evaluator loads phase-2 archives without modifying them. "
              "Prediction archives retain trajectory identity and link to source-data paths and hashes in run metadata.", "",
              "## Reproduction", "", "From the repository root, with the project environment installed:", "",
              "```powershell", metadata["command"], "```", "",
              "```powershell", r".\.venv\Scripts\python.exe -m pytest tests/test_drone_physics.py -q", "```", "",
              "Default inputs are `runs/Drone/phase_2/dataset.npz` and `runs/Drone/phase_2/benchmark_dataset.npz`. "
              "Use `--dataset`, `--benchmark`, or `--output-root` to select alternatives. "
              "Repeated executions preserve existing results in `phase_3/repeat_N/`, each with `Phase 3 Data.md`.", "",
              "## Scope and changes", "",
              "Added independent dynamics, quaternion-angle diagnostics, physics scoring, analytic verification, "
              "fluid-isolation checks, and prediction/error plots. Development scripts now write phase_N folders "
              "and Phase N Data.md reports; numbered runs/experiments remain reserved for the formed system. "
              "Past phase outputs were not rewritten. Drone_Plan.md and README.md were not edited.", "",
              "This baseline covers one drone property configuration and the conservative still-air flight envelope "
              "from phase 2. Its drift is evidence for interpreting the upcoming learned correction, not an "
              "automatic model success/failure rule. Held-out waypoint data are reported separately and never "
              "used to fit model parameters. No commit was created.", ""]
    (output/"Phase 3 Data.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=Path("runs/Drone/phase_2/dataset.npz"))
    parser.add_argument("--benchmark", type=Path, default=Path("runs/Drone/phase_2/benchmark_dataset.npz"))
    parser.add_argument("--output-root", type=Path, default=Path("runs/Drone"))
    parser.add_argument("--fluid-samples-per-trajectory", type=int, default=10)
    args = parser.parse_args()
    main_data, benchmark = load_dataset(args.dataset), load_dataset(args.benchmark)
    config = SimulationConfig(**main_data.metadata["simulation"]["simulation_config"])
    simulator = DroneSimulator(config)
    current_settings = simulator.metadata()
    expected_keys = ("model_revision", "mass_kg", "inertia_kg_m2", "gravity_world_m_s2", "density_kg_m3",
                     "viscosity_pa_s", "wind_world_m_s", "simulation_config", "actuator_gears", "actuator_ctrlrange")
    for dataset in (main_data, benchmark):
        for key in expected_keys:
            if dataset.metadata["simulation"][key] != current_settings[key]:
                parser.error(f"source dataset differs from the current reference setting: {key}")
    if set(main_data.split.tolist()) != {"train", "validation", "test"} or set(benchmark.split.tolist()) != {"benchmark"}:
        parser.error("provide a main train/validation/test archive and a separate benchmark archive")
    if (main_data.metadata["held_out_family"] != benchmark.metadata["held_out_family"] or
            main_data.metadata["config"]["seed"] != benchmark.metadata["config"]["seed"]):
        parser.error("main and benchmark must use the same root seed and held-out family")
    if not 1 <= args.fluid_samples_per_trajectory <= config.num_steps:
        parser.error("fluid sample count must be between 1 and the number of transitions")
    physics = RigidBodyPhysics(RigidBodyParameters.from_metadata(current_settings), config)
    sanity = verify_analytic_motion(physics)
    output, _ = next_phase(args.output_root, 3)
    (output/"predictions").mkdir()
    (output/"plots").mkdir()
    root = Path(__file__).resolve().parents[2]
    sources = sorted((root/"src/drone_sim").glob("*.py")) + [Path(__file__).resolve()]
    revision = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True, check=False)
    dirty = subprocess.run(["git", "status", "--porcelain"], cwd=root, capture_output=True, text=True, check=False)
    metadata = {"phase": 3, "status": "evaluating", "predictor": "physics_only", "truth_refresh": None,
                "command": subprocess.list2cmdline(["python", "scripts/drone/evaluate_physics.py", *sys.argv[1:]]),
                "code_revision": revision.stdout.strip(), "working_tree_dirty": bool(dirty.stdout.strip()),
                "source_sha256": {path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest() for path in sources},
                "inputs": {label: {"path": path.as_posix(), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
                           for label, path in (("main", args.dataset), ("benchmark", args.benchmark))},
                "physics_parameters": asdict(physics.parameters), "prediction_config": asdict(config),
                "reference_simulation": current_settings,
                "metric_time_samples": "predicted timestamps only; excludes exact initial state"}
    write_json(output/"run_metadata.json", metadata)
    write_json(output/"sanity_checks.json", sanity)
    print(f"Analytic motion checks passed. Evaluating physics into {output}", flush=True)
    try:
        diagnostics, diagnostic_arrays = compare_without_fluid(physics, main_data,
                                      samples_per_trajectory=args.fluid_samples_per_trajectory)
        write_json(output/"fluid_comparison.json", diagnostics)
        np.savez_compressed(output/"predictions/fluid_comparison.npz", **diagnostic_arrays)
        plot_fluid_isolation(diagnostic_arrays, output/"plots/fluid_isolation.png")
        print(f"Fluid isolation: {diagnostics['samples']} matched training transitions checked.", flush=True)
        all_one_step_rows, all_recursive_rows, one_step_groups, recursive_groups, examples = [], [], {}, {}, []
        transitions = 0
        for source_name, dataset in (("main", main_data), ("benchmark", benchmark)):
            print(f"Computing one-step predictions for {len(dataset.states)} {source_name} flights...", flush=True)
            one_step = one_step_predictions(physics, dataset.states, dataset.controls)
            residual = one_step_residuals(dataset.states[:, :-1], one_step[:, 1:], dataset.states[:, 1:])
            residual_metadata = {"order": ["dp_body_current_3", "dv_body_current_3", "dtheta_predicted_next_body_3", "domega_body_components_3"],
                                 "meaning": "simulator next state minus physics next state; orientation via right composition",
                                 "units": ["m", "m/s", "rad", "rad/s"], "source": source_name}
            np.savez_compressed(output/f"predictions/one_step_{source_name}.npz", states=one_step,
                                residuals=residual, time=dataset.time, trajectory_ids=dataset.trajectory_ids,
                                families=dataset.families, split=dataset.split, metadata_json=json.dumps(residual_metadata))
            all_one_step_rows += metric_rows(dataset, one_step, np.arange(len(dataset.states)), "one_step")
            transitions += dataset.controls.shape[0]*dataset.controls.shape[1]
            for label in dict.fromkeys(dataset.split.tolist()):
                indices = np.flatnonzero(dataset.split == label)
                one_step_groups[label] = (one_step[indices], dataset.states[indices])
                if label not in ("test", "benchmark"):
                    continue
                predicted = physics.rollout(dataset.states[indices, 0], dataset.controls[indices])
                all_recursive_rows += metric_rows(dataset, predicted, indices, "recursive")
                recursive_groups[label] = (predicted, dataset.states[indices])
                np.savez_compressed(output/f"predictions/recursive_{label}.npz", states=predicted,
                                    time=dataset.time, trajectory_ids=dataset.trajectory_ids[indices],
                                    families=dataset.families[indices], controls=dataset.controls[indices],
                                    metadata_json=json.dumps({"predictor": "physics_only", "mode": "recursive", "truth_refresh": None}))
                for family in dict.fromkeys(dataset.families[indices].tolist()):
                    local = int(np.flatnonzero(dataset.families[indices] == family)[0])
                    index = indices[local]
                    name = f"{label}_{dataset.trajectory_ids[index]}_physics.png"
                    plot_physics_flight(dataset.time, dataset.states[index], predicted[local], output/"plots"/name,
                                        f"{label} | {family} | {dataset.trajectory_ids[index]} | no truth refresh")
                    examples.append({"split": label, "family": family, "trajectory_id": str(dataset.trajectory_ids[index]), "plot": f"plots/{name}"})
                print(f"Completed {label}: {len(indices)} recursive flights.", flush=True)
        one_step_summary, recursive_summary = summarize_by_split(all_one_step_rows), summarize_by_split(all_recursive_rows)
        write_csv(output/"one_step_metrics.csv", all_one_step_rows)
        write_json(output/"one_step_metrics.json", one_step_summary)
        write_csv(output/"rollout_metrics.csv", all_recursive_rows)
        write_json(output/"rollout_metrics.json", recursive_summary)
        write_json(output/"test_metrics.json", {label: {"one_step": one_step_summary[label], "recursive": recursive_summary[label]}
                                               for label in recursive_summary})
        comparison = [{"split": label, "predictor": "physics_only", "mode": mode, **summary}
                      for mode, summaries in (("one_step", one_step_summary), ("recursive", recursive_summary))
                      for label, summary in summaries.items()]
        write_csv(output/"comparison_metrics.csv", comparison)
        plot_physics_errors(main_data.time, one_step_groups, output/"plots/one_step_errors.png", "One-step rigid-body prediction errors")
        plot_physics_errors(main_data.time, recursive_groups, output/"plots/recursive_errors.png", "Recursive rigid-body prediction errors; no truth refresh")
        metadata.update(status="complete", one_step_transitions=transitions,
                        recursive_trajectories=len(all_recursive_rows), preselected_examples=examples,
                        one_step_summaries=one_step_summary, recursive_summaries=recursive_summary)
        write_json(output/"run_metadata.json", metadata)
        write_report(output, metadata, one_step_summary, recursive_summary, diagnostics)
    except Exception as error:
        metadata.update(status="failed", failure_reason=str(error))
        write_json(output/"run_metadata.json", metadata)
        raise
    for label, summary in recursive_summary.items():
        print(f"{label}: recursive mean position MAE={summary['mean_position_mae_m']:.6g} m; "
              f"mean orientation MAE={summary['mean_orientation_mae_rad']:.6g} rad "
              f"({summary['mean_orientation_mae_deg']:.6g} deg)", flush=True)
    print(f"Results and theory: {output/'Phase 3 Data.md'}", flush=True)


if __name__ == "__main__":
    main()

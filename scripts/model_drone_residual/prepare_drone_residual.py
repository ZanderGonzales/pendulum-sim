"""Prepare and verify phase-4 residual NN components; no optimizer training yet.

Build true-current-state examples, fit train-only standardizers, verify geometry
and gradients, save an untrained initialization and a Phase 4 Data.md report.
"""

import argparse
import csv
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

import numpy as np
import torch

from drone_sim import RigidBodyParameters, RigidBodyPhysics, SimulationConfig, load_dataset
from drone_sim.artifacts import next_phase
from drone_sim.evaluation import state_errors, summarize_metrics, trajectory_metrics
from drone_sim.plotting import plot_prediction_comparison
from model_drone_residual import (
    DroneResidualMLP, FEATURE_ORDER, TARGET_ORDER, RESIDUAL_CONVENTION, HybridPredictor,
    apply_residual, fit_standardizers, gradient_check, load_checkpoint, prepare_samples,
    save_initial_checkpoint, standardized_tensors,
)


def write_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, allow_nan=False)+"\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def construction_check(samples):
    rebuilt = apply_residual(samples.current_states, samples.physics_next, samples.targets)
    zero = apply_residual(samples.current_states, samples.physics_next, np.zeros_like(samples.targets))
    result = {"samples": len(samples.features), "trajectories": len(set(samples.trajectory_ids.tolist())),
              "raw_features_dtype": str(samples.features.dtype), "raw_targets_dtype": str(samples.targets.dtype)}
    for label, prediction, target in (("exact_residual_reconstruction", rebuilt, samples.next_states),
                                       ("zero_residual_vs_physics", zero, samples.physics_next)):
        errors = state_errors(prediction, target)
        result[label] = {f"maximum_{name}": float(value.max()) for name, value in errors.items()}
        if any(value > 1e-12 for value in result[label].values()):
            raise AssertionError(f"residual composition check failed: {label}")
    return result, rebuilt


def construction_rows(dataset, samples, rebuilt):
    indices = np.flatnonzero(dataset.split == samples.split)
    steps = dataset.controls.shape[1]
    rows = []
    for name, array in (("physics_only", samples.physics_next), ("exact_residual_reconstruction", rebuilt)):
        trajectories = array.reshape(len(indices), steps, 13)
        for local, index in enumerate(indices):
            predicted = np.concatenate((dataset.states[index, :1], trajectories[local]), axis=0)
            rows.append({"trajectory_id": str(dataset.trajectory_ids[index]), "split": samples.split,
                         "family": str(dataset.families[index]), "method": name, "mode": "one_step_construction_check",
                         **trajectory_metrics(predicted, dataset.states[index])})
    return rows


def write_report(output: Path, metadata: dict, standardizers, checks: dict, summaries: dict) -> None:
    lines = ["# Phase 4 Data: One-Step Physics-Residual Neural Network", "", "## Results and scope", "",
             "The residual NN, supervised examples, train-only standardizers, one-step hybrid inference, "
             "and portable initial checkpoint are implemented. This phase verifies the learning problem and "
             "correction geometry. **No optimizer updates were performed and the checkpoint is untrained.** "
             "The full 10,000-update Adam training schedule and learned recursive evaluation remain phase 5.", "",
             f"- Architecture: 14 inputs, {metadata['model_config']['hidden_layers']} hidden layers of "
             f"{metadata['model_config']['hidden_size']} neurons, Tanh hidden activations, 12 linear outputs.",
             f"- Trainable parameters: {metadata['trainable_parameters']:,}.",
             f"- Model initialization seed: {metadata['seed']}; PyTorch: {metadata['torch_version']}.",
             f"- Prepared samples: {metadata['split_sample_counts']}.",
             f"- Standardizer fitting: {standardizers.training_sample_count:,} training samples from "
             f"{len(standardizers.training_trajectory_ids)} complete training trajectories only.",
             f"- Forward/backward check: {checks['gradient_check']['batch_size']} training samples; finite gradients "
             "for every parameter tensor; weights unchanged; zero optimizer updates.",
             f"- Initial checkpoint reload: maximum state-component difference "
             f"{checks['checkpoint_reload_maximum_component_difference']:.9g} on the fixed training-state check batch.", "",
             "## Exact-residual reconstruction checks", "",
             "These checks apply the known simulator-minus-physics residual to verify the coordinate transformations. "
             "They use true next states and are **not learned predictions, generalization scores, or recursive rollouts**. "
             "Zero-residual checks independently verify that applying zero physical correction preserves physics-only prediction.", ""]
    for label, result in checks["splits"].items():
        errors = result["exact_residual_reconstruction"]
        lines += [f"- {label}: {result['samples']:,} transitions; maximum reconstruction position error "
                  f"{errors['maximum_position_m']:.9g} m, orientation error "
                  f"{errors['maximum_orientation_rad']:.9g} rad, linear velocity error "
                  f"{errors['maximum_linear_velocity_m_s']:.9g} m/s, angular velocity error "
                  f"{errors['maximum_angular_velocity_rad_s']:.9g} rad/s."]
    lines += ["", "### Test and benchmark mean MAEs", "",
              "The following are equal-weight means of the per-trajectory one-step MAEs. "
              "The exact-residual values measure reconstruction precision, not NN accuracy.", ""]
    for label in ("test", "benchmark"):
        for name, result in summaries[label].items():
            lines += [f"- {label}, {name}: mean position MAE **{result['mean_position_mae_m']:.9g} m**, "
                      f"std {result['std_position_mae_m']:.9g} m; mean orientation MAE "
                      f"**{result['mean_orientation_mae_rad']:.9g} rad ({result['mean_orientation_mae_deg']:.9g} deg)**, "
                      f"std {result['std_orientation_mae_rad']:.9g} rad."]
    lines += ["", "## What the network learns", "",
              "For a true simulator current state x_k and the actual applied wrench u_k, first compute the "
              "independent physics step. The target is the finite-step error of that prediction:", "",
              "$$x^p_{k+1}=F_{physics}(x_k,u_k,\\Delta t),\\qquad r_k=x^{sim}_{k+1}\\ominus x^p_{k+1}$$", "",
              "$$\\hat x_{k+1}=x^p_{k+1}\\oplus NN(z_k)$$", "",
              "The NN is not asked to relearn gravity, thrust acceleration, or rigid-body rotation. "
              "Those are already present in the independent predictor. The unicycle model learned its entire "
              "one-step body displacement and heading increment; this drone model learns only the discrepancy "
              "between physics and MuJoCo. The residual is not an acceleration and is not divided by the timestep.", "",
              "## The 14 inputs", "",
              "- Current body-frame linear velocity: 3 components, R(q_k).T @ v_world.",
              "- Current body-frame angular velocity: 3 components, already stored in that frame.",
              "- Current body-frame gravity: 3 components, R(q_k).T @ g_world.",
              "- Applied physical control: total thrust in N and three right-hand body moments in N m.",
              "- Prediction interval in seconds: 1 component.", "",
              "**Body-frame gravity is the world gravity vector expressed along the drone's current axes.** "
              "A level drone sees [0, 0, -9.81] regardless of yaw; a tilted drone sees components along its tilted axes. "
              "This is the same gravity used by the physics model, not an additional force. "
              "The features omit absolute position and global yaw: rigid-body motion and still-air resistance "
              "do not require them for this setup. Every input comes from the current state, the known applied "
              "control, and fixed physics settings; the NN receives no next-state truth.", "",
              "The exact feature order is saved in standardizers.json and the initial checkpoint. "
              "The controls are applied SI wrenches after actuator limits, not raw MuJoCo commands or rotor speeds.", "",
              "## The 12 outputs and how they are applied", "",
              "Let R_k be the current body-to-world orientation. Position and velocity corrections are:", "",
              "$$r_p=R_k^T(p^{sim}_{k+1}-p^p_{k+1}),\\quad r_v=R_k^T(v^{sim}_{k+1}-v^p_{k+1})$$", "",
              "$$\\hat p_{k+1}=p^p_{k+1}+R_k\\hat r_p,\\quad \\hat v_{k+1}=v^p_{k+1}+R_k\\hat r_v$$", "",
              "The three orientation outputs form a shortest rotation vector:", "",
              "$$r_\\theta=\\mathrm{Log}((R^p_{k+1})^T R^{sim}_{k+1}),\\quad "
              "\\hat R_{k+1}=R^p_{k+1}\\mathrm{Exp}(\\hat r_\\theta)$$", "",
              "This orientation correction is in predicted-next body axes and composes on the right. "
              "The code converts the vector to a unit quaternion and uses the Hamilton product "
              "q_physics_next * quaternion_from_rotvec(r_theta). Quaternion components are never subtracted. "
              "q and -q yield the same physical correction and error. The remaining three outputs are "
              "simulator-minus-physics angular-velocity state components, added in their respective body-coordinate representation.", "",
              "`apply_residual` explicitly implements these transformations. Its output remains a 13-component "
              "state with a normalized scalar-first body-to-world quaternion. Training targets are built from true "
              "current states; eventual recursive use must compute features and correction frames from predicted current states.", "",
              "## Standardization and numerical precision", "",
              "Physics integration, residual construction, population means, and population standard deviations "
              "use float64. Each feature and target coordinate is standardized independently with statistics from "
              "the train split. Only the standardized values become float32 NN tensors. Network outputs are "
              "converted back to float64 before unstandardization and state correction.", "",
              f"Training target standard deviations span {float(standardizers.targets.scale.min()):.9g} to "
              f"{float(standardizers.targets.scale.max()):.9g} in their respective physical units. "
              "An inherited absolute scale cutoff of 1e-8 would incorrectly stop normalizing some orientation "
              "targets. This implementation uses the measured positive standard deviation for nonconstant columns "
              "and scale=1 only for exactly constant columns. Constant means use their recorded value exactly; "
              "the fixed dt column therefore becomes exactly zero. Very small targets are preserved rather than artificially enlarged.", "",
              "Validation, test, and held-out waypoint samples use the frozen training statistics and cannot be "
              "passed to fit_standardizers. The saved standardizer includes the fitting trajectory IDs and sample count. "
              "The benchmark remains separate and is used here only for algebraic consistency checks, not tuning.", "",
              "A zero standardized NN output unstandardizes to the training target mean. It does not necessarily "
              "mean zero physical residual. The physics-equivalence check therefore applies an explicit physical zero vector.", "",
              "## Architecture and PyTorch", "",
              "The default MLP uses Linear(14,64), Tanh, Linear(64,64), Tanh, Linear(64,12). "
              "The final layer is linear so signed standardized residuals are unrestricted. "
              "Hidden width and hidden-layer count are configurable. Input and output layers are additional "
              "to the hidden-layer count. PyTorch autograd checks backpropagation through the NN's standardized "
              "residual MSE. Physics and target construction happen outside that graph because this is supervised "
              "one-step residual learning, not differentiation through MuJoCo.", "",
              "The architecture variants are constructible (parameter counts include all biases):", ""]
    for name, count in metadata["architecture_parameter_counts"].items():
        lines.append(f"- {name}: {count:,} trainable parameters.")
    lines += ["", "References: [PyTorch Linear](https://docs.pytorch.org/docs/2.14/generated/torch.nn.Linear.html) "
              "and [Tanh](https://docs.pytorch.org/docs/2.14/generated/torch.nn.Tanh.html).", "",
              "## Artifacts and file architecture", "",
              "- `src/model_drone_residual/model.py`: configurable MLP, float64 standardizers, serialized feature/target contract.",
              "- `src/model_drone_residual/residuals.py`: input features, frame definitions, and correction composition.",
              "- `src/model_drone_residual/training.py`: true-state supervised examples, training-only scaler fitting, tensor preparation, backward check. No scheduled fitting loop yet.",
              "- `src/model_drone_residual/evaluation.py`: one-step HybridPredictor and initial checkpoint save/load. No recursive evaluator yet.",
              "- `src/drone_sim/frames.py`: reusable vector rotation, quaternion composition, rotation-vector exponential map.",
              "- `scripts/model_drone_residual/prepare_drone_residual.py`: this reproducible phase-4 entry point.",
              "- `tests/test_drone_residual.py`: geometry, leakage prevention, tiny-target precision, NN variants, gradients, checkpoint tests.",
              "- `standardizers.json`: training-fitted statistics, coordinate ordering, fitting trajectory IDs and count.",
              "- `checkpoint_initial.pt`: UNTRAINED seeded model, frozen standardizers, physics/timing constants, schema and frame contract. It is not checkpoint_best.pt or checkpoint_final.pt.",
              "- `prepared_samples/<split>.npz`: raw float64 features/targets, standardized float32 arrays, per-transition trajectory IDs/step indices, metadata.",
              "- `contract_checks.json`: reconstruction, zero-residual, frozen statistics, gradient, and checkpoint reload results.",
              "- `construction_metrics.csv` / `.json`: per-flight and equal-weight per-split physical metrics for physics-only versus exact-residual reconstruction.",
              "- `comparison_metrics.csv`: split/method summary rows, including mean test position/orientation MAEs and standard deviations.",
              "- `plots/<trajectory_id>_construction.png`: preselected test/benchmark examples with a large 3D path and smaller position/orientation angle error plots. No planar projection or position/velocity component plots.",
              "- `predictions/<trajectory_id>_construction.npz`: the corresponding true, physics-next, and exact-residual reconstructed states; these are construction checks, not NN forecasts.",
              "- `run_metadata.json`: exact command, source/input SHA256s, model/source provenance, architecture, seed, schema, dtype, phase status, and zero optimizer updates.", "",
              "Position MAE uses time-average Euclidean distance, orientation MAE uses shortest absolute rotation "
              "angle in radians/degrees, and the exact initial state is excluded. Means give every flight equal "
              "weight; standard deviations use ddof=0. Velocity MAE/RMSE, position/orientation RMSE, and final/maximum "
              "position errors remain in the CSV/JSON, even though velocity curves are omitted from plots.", "",
              "## Reproduction and interfaces", "", "From the repository root:", "", "```powershell",
              metadata["command"], "```", "", "```powershell",
              r".\.venv\Scripts\python.exe -m pytest tests/test_drone_residual.py -q", "```", "",
              "The entry point accepts `--dataset`, `--benchmark`, `--output-root`, `--seed`, `--hidden-size`, "
              "and `--hidden-layers`. Default output is runs/Drone/phase_4; repeats preserve earlier results under repeat_N.", "",
              "`prepare_samples(dataset, 'train')` builds true-state samples; `fit_standardizers(training_samples)` "
              "fits only train statistics. `HybridPredictor(model, standardizers, physics).step(state, applied_control)` "
              "computes a physics transition and its NN correction. `load_checkpoint(path)` returns that predictor "
              "and its checkpoint metadata. **The saved initialization is not ready for useful forecasting until trained.**", "",
              "## Interpretation and next work", "",
              "Successful reconstruction verifies that targets and correction composition are mutually consistent. "
              "Finite gradients verify that the NN can receive a training signal. Neither proves learned accuracy. "
              "All data use one drone property configuration, still air, conservative flight, and one timestep; "
              "including dt as an input does not establish generalization to other timesteps.", "",
              "Phase 5 will use Adam, learning rate 0.001, batch size 256, exactly 10,000 default optimizer updates, "
              "validation every 100 updates and at the end, best/final checkpoints, and separate physics/hybrid "
              "one-step and fully recursive results. Phase 4 has no optimizer state, trained best/final checkpoints, "
              "loss curves, or learned test-accuracy claims. No truth refresh mechanism was introduced.", "",
              "Drone_Plan.md and README.md were not edited. Prior phase output was not rewritten. No commit was created.", ""]
    (output/"Phase 4 Data.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=Path("runs/Drone/phase_2/dataset.npz"))
    parser.add_argument("--benchmark", type=Path, default=Path("runs/Drone/phase_2/benchmark_dataset.npz"))
    parser.add_argument("--output-root", type=Path, default=Path("runs/Drone"))
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--hidden-size", type=int, default=64)
    parser.add_argument("--hidden-layers", type=int, default=2)
    args = parser.parse_args()
    if args.seed < 0 or args.hidden_size < 1 or args.hidden_layers < 1:
        parser.error("seed must be nonnegative; hidden size and layer count must be positive")
    main_data, benchmark = load_dataset(args.dataset), load_dataset(args.benchmark)
    if set(main_data.split.tolist()) != {"train", "validation", "test"} or set(benchmark.split.tolist()) != {"benchmark"}:
        parser.error("provide main train/validation/test data and a separate benchmark archive")
    if (main_data.metadata["simulation"] != benchmark.metadata["simulation"] or
            main_data.metadata["held_out_family"] != benchmark.metadata["held_out_family"] or
            main_data.metadata["config"]["seed"] != benchmark.metadata["config"]["seed"]):
        parser.error("main and benchmark simulator settings, root seed, and held-out family must match")
    physics = RigidBodyPhysics(RigidBodyParameters.from_metadata(main_data.metadata["simulation"]),
                              SimulationConfig(**main_data.metadata["simulation"]["simulation_config"]))
    torch.manual_seed(args.seed)
    model = DroneResidualMLP(args.hidden_size, args.hidden_layers)
    architectures = {f"{depth}x{width}": sum((previous+1)*following for previous, following in
                     zip([14]+[width]*depth, [width]*depth+[12]))
                     for width, depth in ((32, 2), (64, 2), (128, 2), (64, 1), (64, 4))}
    output, _ = next_phase(args.output_root, 4)
    for directory in ("prepared_samples", "predictions", "plots"):
        (output/directory).mkdir()
    root = Path(__file__).resolve().parents[2]
    sources = sorted((root/"src/drone_sim").glob("*.py")) + sorted((root/"src/model_drone_residual").glob("*.py")) + [Path(__file__).resolve()]
    revision = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True, check=False)
    dirty = subprocess.run(["git", "status", "--porcelain"], cwd=root, capture_output=True, text=True, check=False)
    metadata = {"phase": 4, "status": "preparing", "training_status": "untrained", "optimizer_updates": 0,
                "command": subprocess.list2cmdline(["python", "scripts/model_drone_residual/prepare_drone_residual.py", *sys.argv[1:]]),
                "code_revision": revision.stdout.strip(), "working_tree_dirty": bool(dirty.stdout.strip()),
                "source_sha256": {path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest() for path in sources},
                "inputs": {label: {"path": path.as_posix(), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
                           for label, path in (("main", args.dataset), ("benchmark", args.benchmark))},
                "model_config": {"hidden_size": args.hidden_size, "hidden_layers": args.hidden_layers,
                                 "input_size": 14, "output_size": 12, "activation": "Tanh"},
                "seed": args.seed, "trainable_parameters": model.parameter_count, "torch_version": str(torch.__version__),
                "architecture_parameter_counts": architectures, "feature_order": list(FEATURE_ORDER),
                "target_order": list(TARGET_ORDER), "residual_convention": RESIDUAL_CONVENTION,
                "physics_parameters": asdict(physics.parameters), "prediction_config": asdict(physics.config),
                "reference_simulation": main_data.metadata["simulation"]}
    write_json(output/"run_metadata.json", metadata)
    print(f"Preparing residual NN interfaces into {output}; no optimizer training.", flush=True)
    started = time.perf_counter()
    try:
        training = prepare_samples(main_data, "train", physics)
        standardizers = fit_standardizers(training)
        write_json(output/"standardizers.json", standardizers.to_dict())
        frozen_statistics = json.dumps(standardizers.to_dict(), sort_keys=True)
        checks = {"gradient_check": gradient_check(model, training, standardizers, seed=args.seed), "splits": {}}
        predictor = HybridPredictor(model, standardizers, physics)
        save_initial_checkpoint(output/"checkpoint_initial.pt", predictor, seed=args.seed)
        reloaded, _ = load_checkpoint(output/"checkpoint_initial.pt")
        current = training.current_states[:32]
        controls = main_data.samples("train")["control_current"][:32]
        before, after = predictor.step_array(current, controls), reloaded.step_array(current, controls)
        checks["checkpoint_reload_maximum_component_difference"] = float(np.max(np.abs(before-after)))
        if checks["checkpoint_reload_maximum_component_difference"] != 0:
            raise AssertionError("initial checkpoint round trip changed inference")
        rows, counts, examples = [], {}, []
        for split, dataset in (("train", main_data), ("validation", main_data), ("test", main_data), ("benchmark", benchmark)):
            samples = training if split == "train" else prepare_samples(dataset, split, physics)
            contract, rebuilt = construction_check(samples)
            checks["splits"][split] = contract
            x, y = standardized_tensors(samples, standardizers)
            np.savez_compressed(output/f"prepared_samples/{split}.npz", features=samples.features,
                                targets=samples.targets, standardized_features=x.numpy(), standardized_targets=y.numpy(),
                                trajectory_ids=samples.trajectory_ids, step_indices=samples.step_indices,
                                metadata_json=json.dumps({"split": split, "feature_order": list(FEATURE_ORDER),
                                                          "target_order": list(TARGET_ORDER), "residual_convention": RESIDUAL_CONVENTION}))
            counts[split] = len(samples.features)
            rows += construction_rows(dataset, samples, rebuilt)
            if split in ("test", "benchmark"):
                indices = np.flatnonzero(dataset.split == split)
                steps = dataset.controls.shape[1]
                physics_flights = samples.physics_next.reshape(len(indices), steps, 13)
                rebuilt_flights = rebuilt.reshape(len(indices), steps, 13)
                for family in dict.fromkeys(dataset.families[indices].tolist()):
                    local = int(np.flatnonzero(dataset.families[indices] == family)[0])
                    index, identifier = indices[local], str(dataset.trajectory_ids[indices[local]])
                    truth = dataset.states[index]
                    physics_states = np.concatenate((truth[:1], physics_flights[local]))
                    reconstructed = np.concatenate((truth[:1], rebuilt_flights[local]))
                    plot_prediction_comparison(dataset.time, truth,
                        {"Physics: true current states": physics_states, "Exact residual: uses next-state truth": reconstructed},
                        output/f"plots/{identifier}_construction.png",
                        f"{split} | {family} | {identifier}\nOne-step construction check; no trained NN")
                    np.savez_compressed(output/f"predictions/{identifier}_construction.npz", time=dataset.time,
                                        true_states=truth, physics_next_states=physics_states, reconstructed_states=reconstructed,
                                        metadata_json=json.dumps({"trajectory_id": identifier, "split": split,
                                                                  "purpose": "exact-residual construction check, not learned prediction"}))
                    examples.append(identifier)
            print(f"{split}: {len(samples.features):,} examples; exact-residual and zero-residual checks passed.", flush=True)
        if json.dumps(standardizers.to_dict(), sort_keys=True) != frozen_statistics:
            raise AssertionError("held-out data changed training standardizers")
        checks["standardizers_unchanged_after_held_out_preparation"] = True
        summaries = {split: {name: summarize_metrics([row for row in rows if row["split"] == split and row["method"] == name])
                            for name in ("physics_only", "exact_residual_reconstruction")} for split in counts}
        write_csv(output/"construction_metrics.csv", rows)
        write_json(output/"construction_metrics.json", summaries)
        write_csv(output/"comparison_metrics.csv", [{"split": split, "method": name, "mode": "one_step_construction_check", **summary}
                    for split, methods in summaries.items() for name, summary in methods.items()])
        write_json(output/"contract_checks.json", checks)
        metadata.update(status="complete", split_sample_counts=counts, preselected_examples=examples,
                        elapsed_seconds=time.perf_counter()-started)
        write_json(output/"run_metadata.json", metadata)
        write_report(output, metadata, standardizers, checks, summaries)
    except Exception as error:
        metadata.update(status="failed", failure_reason=str(error))
        write_json(output/"run_metadata.json", metadata)
        raise
    print(f"Saved untrained {model.parameter_count:,}-parameter model and train-only standardizers. Optimizer updates: 0.", flush=True)
    print(f"Results and theory: {output/'Phase 4 Data.md'}", flush=True)


if __name__ == "__main__":
    main()

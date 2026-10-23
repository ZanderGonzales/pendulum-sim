"""Hybrid one-step/recursive inference and portable model checkpoints."""

from dataclasses import asdict
from pathlib import Path

import numpy as np
import torch

from drone_sim.physics import RigidBodyParameters, RigidBodyPhysics
from drone_sim.types import DroneControl, DroneState, SimulationConfig
from model_drone_residual.model import DroneResidualMLP, ResidualStandardizers
from model_drone_residual.residuals import FEATURE_ORDER, TARGET_ORDER, RESIDUAL_CONVENTION, apply_residual, residual_features


class HybridPredictor:
    """Predict a physics step, then compose a learned physical residual.

    Inputs include no next-state truth or future observations. Physics and
    correction remain float64; only standardized features enter the MLP dtype.
    """

    def __init__(self, model: DroneResidualMLP, standardizers: ResidualStandardizers, physics: RigidBodyPhysics):
        self.model, self.standardizers, self.physics = model, standardizers, physics

    def predict_residuals(self, states, applied_controls) -> np.ndarray:
        features = residual_features(states, applied_controls, self.physics.config.dt, self.physics.parameters.gravity)
        standardized = self.standardizers.inputs.transform(features).reshape(-1, len(FEATURE_ORDER))
        parameter = next(self.model.parameters())
        tensor = torch.as_tensor(standardized, dtype=parameter.dtype, device=parameter.device)
        if not torch.isfinite(tensor).all():
            raise ValueError("standardized features overflow model dtype")
        self.model.eval()
        with torch.inference_mode():
            prediction = self.model(tensor).cpu().numpy().astype(np.float64)
        return self.standardizers.targets.inverse_transform(prediction).reshape(*features.shape[:-1], len(TARGET_ORDER))

    def step_array(self, states, applied_controls) -> np.ndarray:
        predicted = self.physics.step_array(states, applied_controls)
        residual = self.predict_residuals(states, applied_controls)
        return apply_residual(states, predicted, residual)

    def step(self, state: DroneState, applied_control: DroneControl) -> DroneState:
        return DroneState.from_array(self.step_array(state.as_array(), applied_control.as_array()))

    def rollout(self, initial_states, applied_controls) -> np.ndarray:
        """Recursive propagation accepts no truth after initialization.

        State shape (...,13), controls (...,steps,4), result (...,steps+1,13).
        Features and correction frames are recomputed from predicted states.
        """
        initial, controls = np.asarray(initial_states, dtype=float), np.asarray(applied_controls, dtype=float)
        if controls.ndim < 2 or controls.shape[:-2] != initial.shape[:-1] or controls.shape[-1] != 4:
            raise ValueError("rollout controls must match initial-state leading dimensions")
        self.physics._validate(initial, np.zeros((*initial.shape[:-1], 4)))
        if not np.isfinite(controls).all() or np.any(controls[..., 0] < 0):
            raise ValueError("rollout controls must be finite with nonnegative thrust")
        result = np.empty((*initial.shape[:-1], controls.shape[-2]+1, 13), dtype=np.float64)
        result[..., 0, :] = initial
        result[..., 0, 3:7] /= np.linalg.norm(initial[..., 3:7], axis=-1, keepdims=True)
        for k in range(controls.shape[-2]):
            result[..., k+1, :] = self.step_array(result[..., k, :], controls[..., k, :])
        return result


def checkpoint_payload(predictor: HybridPredictor, *, seed: int = 0) -> dict:
    """Clone the model and complete inference contract into a portable payload."""
    model = predictor.model
    if next(model.parameters()).dtype not in (torch.float32, torch.float64):
        raise ValueError("checkpoint model dtype must be float32 or float64")
    return {
        "schema_version": 1, "training_status": "untrained", "optimizer_updates": 0, "seed": seed,
        "model_config": {"hidden_size": model.hidden_size, "hidden_layers": model.hidden_layers,
                         "input_size": model.input_size, "output_size": model.output_size, "activation": "Tanh"},
        "model_dtype": str(next(model.parameters()).dtype),
        "model_state_dict": {name: tensor.detach().cpu().clone() for name, tensor in model.state_dict().items()},
        "standardizers": predictor.standardizers.to_dict(),
        "physics_parameters": asdict(predictor.physics.parameters), "prediction_config": asdict(predictor.physics.config),
        "residual_convention": RESIDUAL_CONVENTION, "torch_version": str(torch.__version__),
    }


def save_initial_checkpoint(path: str | Path, predictor: HybridPredictor, *, seed: int = 0) -> None:
    """Save an explicitly UNTRAINED initialization; no best/final training claims."""
    torch.save(checkpoint_payload(predictor, seed=seed), Path(path))


def load_checkpoint(path: str | Path, device: str = "cpu") -> tuple[HybridPredictor, dict]:
    checkpoint = torch.load(Path(path), map_location=device, weights_only=True)
    if checkpoint.get("schema_version") != 1 or checkpoint.get("residual_convention") != RESIDUAL_CONVENTION:
        raise ValueError("unsupported drone checkpoint schema or residual convention")
    config = checkpoint["model_config"]
    if config["input_size"] != len(FEATURE_ORDER) or config["output_size"] != len(TARGET_ORDER) or config["activation"] != "Tanh":
        raise ValueError("checkpoint does not match the 14-input/12-output Tanh model")
    dtypes = {"torch.float32": torch.float32, "torch.float64": torch.float64}
    if checkpoint.get("model_dtype") not in dtypes:
        raise ValueError("unsupported checkpoint model dtype")
    model = DroneResidualMLP(config["hidden_size"], config["hidden_layers"]).to(device=device, dtype=dtypes[checkpoint["model_dtype"]])
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()
    standardizers = ResidualStandardizers.from_dict(checkpoint["standardizers"])
    physics = RigidBodyPhysics(RigidBodyParameters(**checkpoint["physics_parameters"]), SimulationConfig(**checkpoint["prediction_config"]))
    return HybridPredictor(model, standardizers, physics), checkpoint


def evaluate_test_set(predictor: HybridPredictor, dataset, output_dir: str | Path, *, split: str = "test",
                      save_plots: bool = True, checkpoint_info: dict | None = None, progress=None) -> dict:
    """Compare physics/hybrid, one-step/recursive, using identical applied controls.

    Recursive prediction is computed from initial states and controls only.
    True future states are passed separately to scoring and one-step evaluation.
    Per-flight metrics remain separate by split, predictor, and mode.
    """
    import csv
    import json
    from drone_sim.evaluation import one_step_predictions, summarize_metrics, trajectory_metrics

    if split not in ("test", "benchmark"):
        raise ValueError("final evaluation requires test or benchmark split")
    settings = dataset.metadata["simulation"]
    if (predictor.physics.parameters != RigidBodyParameters.from_metadata(settings) or
            predictor.physics.config != SimulationConfig(**settings["simulation_config"])):
        raise ValueError("evaluation physics and timing must match the dataset")
    indices = np.flatnonzero(dataset.split == split)
    if not len(indices):
        raise ValueError(f"dataset has no {split} trajectories")
    output = Path(output_dir)
    (output/"predictions").mkdir(parents=True, exist_ok=True)
    if save_plots:
        (output/"plots").mkdir(exist_ok=True)
    controls = dataset.controls[indices].copy()
    initial = dataset.states[indices, 0].copy()
    recursive = {"physics_only": predictor.physics.rollout(initial, controls),
                 "hybrid": predictor.rollout(initial, controls)}
    truth = dataset.states[indices]
    one_step = {"physics_only": one_step_predictions(predictor.physics, truth, controls),
                "hybrid": one_step_predictions(predictor, truth, controls)}
    rows, summaries, examples = [], {}, []
    families = dataset.families[indices]
    identifiers = dataset.trajectory_ids[indices]
    example_indices = [int(np.flatnonzero(families == family)[0]) for family in dict.fromkeys(families.tolist())]
    for mode, predictions in (("one_step", one_step), ("recursive", recursive)):
        summaries[mode] = {}
        metadata = {"mode": mode, "split": split, "truth_refresh": None, "checkpoint": checkpoint_info or {},
                    "control_source": "recorded applied physical controls", "predictors": ["physics_only", "hybrid"]}
        np.savez_compressed(output/f"predictions/{split}_{mode}.npz", time=dataset.time, controls=controls,
                            trajectory_ids=identifiers, families=families, truth_states=truth,
                            physics_states=predictions["physics_only"], hybrid_states=predictions["hybrid"],
                            metadata_json=json.dumps(metadata))
        for name, states in predictions.items():
            selected = [{"trajectory_id": str(identifiers[i]), "split": split, "family": str(families[i]),
                         "predictor": name, "mode": mode, **trajectory_metrics(states[i], truth[i])}
                        for i in range(len(indices))]
            rows += selected
            summaries[mode][name] = summarize_metrics(selected)
        if save_plots:
            from drone_sim.plotting import plot_prediction_comparison
            for local in example_indices:
                name = f"{identifiers[local]}_{mode}.png"
                label = "Recursive; no truth refresh" if mode == "recursive" else "One step; true current states"
                plot_prediction_comparison(dataset.time, truth[local],
                    {"Physics only": predictions["physics_only"][local], "Physics + NN": predictions["hybrid"][local]},
                    output/"plots"/name, f"{split} | {families[local]} | {identifiers[local]}\n{label}")
                examples.append(f"plots/{name}")
        if progress is not None:
            progress(f"{split}: completed {mode} evaluation for {len(indices)} trajectories")
    # Single NN tracks also load in the existing viewer; no second-drone rendering added.
    for local, identifier in enumerate(identifiers):
        np.savez_compressed(output/f"predictions/{identifier}_hybrid_recursive.npz", time=dataset.time,
                            states=recursive["hybrid"][local], controls=controls[local],
                            metadata_json=json.dumps({"predictor": "hybrid", "mode": "recursive", "truth_refresh": None,
                                                      "trajectory_id": str(identifier), "checkpoint": checkpoint_info or {}}))
    with (output/f"{split}_trajectory_metrics.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    (output/f"{split}_metrics.json").write_text(json.dumps(summaries, indent=2, allow_nan=False)+"\n", encoding="utf-8")
    return {"split": split, "trajectory_count": len(indices), "rows": rows, "summaries": summaries, "examples": examples}


def save_evaluation_summaries(results: list[dict], output_dir: str | Path) -> dict:
    """Consolidate equal-flight means, preserving split/mode/predictor identity."""
    import csv
    import json

    output = Path(output_dir)
    rows = [row for result in results for row in result["rows"]]
    summary = {result["split"]: result["summaries"] for result in results}
    for mode, stem in (("one_step", "one_step_metrics"), ("recursive", "rollout_metrics")):
        selected = [row for row in rows if row["mode"] == mode]
        with (output/f"{stem}.csv").open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(selected[0]))
            writer.writeheader()
            writer.writerows(selected)
        (output/f"{stem}.json").write_text(json.dumps({split: modes[mode] for split, modes in summary.items()},
                                                     indent=2, allow_nan=False)+"\n", encoding="utf-8")
    (output/"test_metrics.json").write_text(json.dumps(summary, indent=2, allow_nan=False)+"\n", encoding="utf-8")
    comparison = [{"split": split, "mode": mode, "predictor": name, **values}
                  for split, modes in summary.items() for mode, predictors in modes.items() for name, values in predictors.items()]
    with (output/"comparison_metrics.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(comparison[0]))
        writer.writeheader()
        writer.writerows(comparison)
    return summary

"""True-state supervised residual training, ending only after complete epochs."""

from dataclasses import asdict, dataclass
import copy
import csv
import json
from pathlib import Path
import time

import numpy as np
import torch

from drone_sim.dataset import DroneDataset
from drone_sim.evaluation import one_step_residuals
from drone_sim.physics import RigidBodyParameters, RigidBodyPhysics
from drone_sim.types import SimulationConfig
from model_drone_residual.model import DroneResidualMLP, ResidualStandardizers, Standardizer
from model_drone_residual.residuals import residual_features


@dataclass(frozen=True)
class ResidualSamples:
    split: str
    current_states: np.ndarray
    next_states: np.ndarray
    physics_next: np.ndarray
    features: np.ndarray
    targets: np.ndarray
    trajectory_ids: np.ndarray
    step_indices: np.ndarray


def prepare_samples(dataset: DroneDataset, split: str, physics: RigidBodyPhysics | None = None) -> ResidualSamples:
    """Build residuals from true current states and the matching applied wrench.

    Physics and subtraction happen in float64. No standardizer is fitted here,
    so validation, test, and benchmark preparation cannot change training scales.
    """
    samples = dataset.samples(split)
    settings = dataset.metadata["simulation"]
    parameters = RigidBodyParameters.from_metadata(settings)
    timing = SimulationConfig(**settings["simulation_config"])
    if physics is None:
        physics = RigidBodyPhysics(parameters, timing)
    if physics.parameters != parameters or physics.config != timing:
        raise ValueError("physics properties and timing must match the source dataset")
    current, following = samples["state_current"], samples["state_next"]
    controls = samples["control_current"]
    predicted = physics.step_array(current, controls)
    features = residual_features(current, controls, samples["dt"], physics.parameters.gravity)
    targets = one_step_residuals(current, predicted, following)
    return ResidualSamples(split, current, following, predicted, features, targets,
                           samples["trajectory_id"], samples["step_index"])


def fit_standardizers(training: ResidualSamples) -> ResidualStandardizers:
    """Require an explicit training split and record every trajectory used."""
    if training.split != "train":
        raise ValueError("standardizers may only be fitted on the train split")
    return ResidualStandardizers(Standardizer.fit(training.features), Standardizer.fit(training.targets),
                                 tuple(dict.fromkeys(training.trajectory_ids.tolist())), len(training.features))


def standardized_tensors(samples: ResidualSamples, standardizers: ResidualStandardizers):
    """Convert only standardized values to float32 for the MLP."""
    features = standardizers.inputs.transform(samples.features)
    targets = standardizers.targets.transform(samples.targets)
    x, y = torch.from_numpy(features.astype(np.float32)), torch.from_numpy(targets.astype(np.float32))
    if not torch.isfinite(x).all() or not torch.isfinite(y).all():
        raise ValueError("standardized samples overflow float32")
    return x, y


def gradient_check(model: DroneResidualMLP, training: ResidualSamples,
                   standardizers: ResidualStandardizers, *, seed: int = 0, batch_size: int = 256) -> dict:
    """One forward/backward check on training data; ZERO optimizer updates.

    This verifies that the loss connects to every parameter. It is not training
    or a performance measurement, and model weights are not modified.
    """
    if training.split != "train":
        raise ValueError("gradient check requires training data")
    if isinstance(batch_size, bool) or not isinstance(batch_size, int) or batch_size <= 0:
        raise ValueError("batch_size must be a positive integer")
    if isinstance(seed, bool) or not isinstance(seed, int) or seed < 0:
        raise ValueError("seed must be a nonnegative integer")
    x, y = standardized_tensors(training, standardizers)
    indices = np.random.default_rng(seed).choice(len(x), min(batch_size, len(x)), replace=False)
    reference = next(model.parameters())
    model.zero_grad(set_to_none=True)
    loss = torch.mean((model(x[indices].to(reference))-y[indices].to(reference))**2)
    loss.backward()
    checks = {name: bool(parameter.grad is not None and torch.isfinite(parameter.grad).all())
              for name, parameter in model.named_parameters()}
    nonzero = sum(int(torch.count_nonzero(parameter.grad)) for parameter in model.parameters() if parameter.grad is not None)
    if not torch.isfinite(loss) or not all(checks.values()) or nonzero == 0:
        raise RuntimeError("nonfinite or disconnected residual NN gradient")
    result = {"passed": True, "source_split": "train", "batch_size": len(indices),
              "initial_batch_standardized_mse": float(loss.detach()), "parameter_gradients_finite": checks,
              "nonzero_gradient_entries": nonzero, "optimizer_updates": 0}
    model.zero_grad(set_to_none=True)
    return result


@dataclass(frozen=True)
class TrainingConfig:
    optimizer_updates: int = 10000
    batch_size: int = 256
    learning_rate: float = .001
    validation_interval: int = 100
    seed: int = 0
    hidden_size: int = 64
    hidden_layers: int = 2
    evaluation_batch_size: int = 4096
    num_threads: int = 1

    def __post_init__(self):
        for name in ("optimizer_updates", "batch_size", "validation_interval", "hidden_size", "hidden_layers",
                     "evaluation_batch_size", "num_threads"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int) or value < 1:
                raise ValueError(f"{name} must be a positive integer")
        if isinstance(self.seed, bool) or not isinstance(self.seed, int) or self.seed < 0:
            raise ValueError("seed must be a nonnegative integer")
        if not np.isfinite(self.learning_rate) or self.learning_rate <= 0:
            raise ValueError("learning_rate must be positive and finite")


@dataclass
class TrainingResult:
    model: DroneResidualMLP
    standardizers: ResidualStandardizers
    physics: RigidBodyPhysics
    config: TrainingConfig
    history: list[dict]
    best_checkpoint: dict
    final_checkpoint: dict
    summary: dict


@torch.inference_mode()
def residual_mse(model, inputs, targets, batch_size: int = 4096) -> float:
    """Full-split standardized residual MSE, weighted by all samples/coordinates."""
    model.eval()
    total = 0.
    for start in range(0, len(inputs), batch_size):
        difference = model(inputs[start:start+batch_size])-targets[start:start+batch_size]
        total += float(torch.sum(difference**2, dtype=torch.float64))
    value = total/targets.numel()
    if not np.isfinite(value):
        raise FloatingPointError("nonfinite residual MSE")
    return value


def epoch_budget(sample_count: int, batch_size: int, requested_updates: int) -> dict:
    """Requested updates are a minimum; include the last short batch each epoch."""
    for value in (sample_count, batch_size, requested_updates):
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            raise ValueError("sample count, batch size, and requested updates must be positive integers")
    batches = (sample_count+batch_size-1)//batch_size
    epochs = (requested_updates+batches-1)//batches
    return {"requested_optimizer_updates": requested_updates, "batches_per_complete_epoch": batches,
            "planned_complete_epochs": epochs, "planned_optimizer_updates": epochs*batches,
            "extra_updates_for_complete_epoch": epochs*batches-requested_updates}


def train_model(dataset: DroneDataset, config: TrainingConfig = TrainingConfig(), progress=None, *,
                prepared_samples: tuple[ResidualSamples, ResidualSamples] | None = None) -> TrainingResult:
    """Train on train/validation ONLY; never request test or benchmark samples."""
    previous_threads = torch.get_num_threads()
    torch.set_num_threads(config.num_threads)
    try:
        return _train_model(dataset, config, progress, prepared_samples)
    finally:
        torch.set_num_threads(previous_threads)


def _train_model(dataset, config, progress, prepared_samples=None):
    from model_drone_residual.evaluation import HybridPredictor, checkpoint_payload

    preparation_started = time.perf_counter()
    settings = dataset.metadata["simulation"]
    physics = RigidBodyPhysics(RigidBodyParameters.from_metadata(settings), SimulationConfig(**settings["simulation_config"]))
    if prepared_samples is None:
        training, validation = prepare_samples(dataset, "train", physics), prepare_samples(dataset, "validation", physics)
    else:
        training, validation = prepared_samples
        for label, samples in (("train", training), ("validation", validation)):
            expected = dataset.samples(label)
            if (samples.split != label or
                    not np.array_equal(samples.trajectory_ids, expected["trajectory_id"]) or
                    not np.array_equal(samples.step_indices, expected["step_index"]) or
                    not np.array_equal(samples.current_states, expected["state_current"]) or
                    not np.array_equal(samples.next_states, expected["state_next"]) or
                    not np.array_equal(samples.features, residual_features(expected["state_current"], expected["control_current"],
                                                                         expected["dt"], physics.parameters.gravity))):
                raise ValueError("cached residual samples must match the selected source split exactly")
    standardizers = fit_standardizers(training)
    train_x, train_y = standardized_tensors(training, standardizers)
    budget = epoch_budget(len(train_x), config.batch_size, config.optimizer_updates)
    target_updates = budget["planned_optimizer_updates"]
    val_x, val_y = standardized_tensors(validation, standardizers)
    torch.manual_seed(config.seed)
    model = DroneResidualMLP(config.hidden_size, config.hidden_layers).float()
    optimizer = torch.optim.Adam(model.parameters(), lr=config.learning_rate)
    generator = torch.Generator().manual_seed(config.seed)
    predictor = HybridPredictor(model, standardizers, physics)
    preparation_seconds = time.perf_counter()-preparation_started
    started = time.perf_counter()
    updates, epoch, samples_processed, epoch_offset = 0, 0, 0, 0
    permutation = torch.empty(0, dtype=torch.int64)
    history, best_checkpoint = [], None
    best_loss, best_update = float("inf"), 0

    def record():
        nonlocal best_loss, best_update, best_checkpoint
        row = {"optimizer_updates": updates, "epoch": epoch,
               "completed_epochs": epoch if epoch_offset == len(train_x) else max(epoch-1, 0),
               "epoch_fraction": max(epoch-1, 0)+epoch_offset/len(train_x),
               "samples_processed": samples_processed, "samples_in_current_epoch": epoch_offset,
               "train_loss": residual_mse(model, train_x, train_y, config.evaluation_batch_size),
               "validation_loss": residual_mse(model, val_x, val_y, config.evaluation_batch_size),
               "learning_rate": optimizer.param_groups[0]["lr"], "elapsed_seconds": time.perf_counter()-started}
        history.append(row)
        if row["validation_loss"] < best_loss:
            best_loss, best_update = row["validation_loss"], updates
            best_checkpoint = snapshot("best", row)
        if progress is not None:
            progress(dict(row))

    def snapshot(kind, row):
        payload = checkpoint_payload(predictor, seed=config.seed)
        payload.update(training_status="trained" if updates else "untrained", checkpoint_kind=kind,
                       optimizer_updates=updates, training_config=asdict(config), training_progress=dict(row),
                       best_update=best_update, best_validation_loss=best_loss,
                       optimizer_state_dict=copy.deepcopy(optimizer.state_dict()),
                       optimizer_name="Adam", training_history=copy.deepcopy(history),
                       sampler_generator_state=generator.get_state().clone(),
                       current_epoch_permutation=permutation.clone(), next_sample_offset=epoch_offset,
                       torch_rng_state=torch.get_rng_state().clone(), device="cpu")
        return payload

    record()  # Initialization loss is recorded and eligible for validation selection.
    while updates < target_updates:
        epoch += 1
        permutation = torch.randperm(len(train_x), generator=generator)
        for start in range(0, len(train_x), config.batch_size):
            end = min(start+config.batch_size, len(train_x))
            indices = permutation[start:end]
            model.train()
            optimizer.zero_grad(set_to_none=True)
            loss = torch.mean((model(train_x[indices])-train_y[indices])**2)
            if not torch.isfinite(loss):
                raise FloatingPointError("nonfinite training loss")
            loss.backward()
            optimizer.step()
            updates += 1
            samples_processed += end-start
            epoch_offset = end
            if updates % config.validation_interval == 0 or updates == target_updates:
                record()
    final_checkpoint = snapshot("final", history[-1])
    assert best_checkpoint is not None
    model.load_state_dict(best_checkpoint["model_state_dict"])
    model.eval()
    summary = {**budget, "optimizer_updates": updates, "epochs_started": epoch,
               "completed_epochs": history[-1]["completed_epochs"], "epoch_fraction": history[-1]["epoch_fraction"],
               "samples_processed": samples_processed, "train_samples": len(train_x), "validation_samples": len(val_x),
               "batches_per_complete_epoch": (len(train_x)+config.batch_size-1)//config.batch_size,
               "best_update": best_update, "best_validation_residual_mse": best_loss,
               "initial_validation_residual_mse": history[0]["validation_loss"],
               "final_train_residual_mse": history[-1]["train_loss"],
               "final_validation_residual_mse": history[-1]["validation_loss"],
               "training_seconds": time.perf_counter()-started, "preparation_seconds": preparation_seconds,
               "trainable_parameters": model.parameter_count, "device": "cpu", "num_threads": config.num_threads,
               "selection": "lowest full validation standardized residual MSE, including initialization",
               "test_data_used_for_training_or_selection": False}
    assert updates == target_updates and samples_processed == epoch*len(train_x)
    return TrainingResult(model, standardizers, physics, config, history, best_checkpoint, final_checkpoint, summary)


def save_training_outputs(result: TrainingResult, output_dir: str | Path, *, provenance: dict | None = None) -> None:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    for kind, checkpoint in (("best", result.best_checkpoint), ("final", result.final_checkpoint)):
        payload = {**checkpoint, "training_run_summary": result.summary, "provenance": provenance or {}}
        torch.save(payload, output/f"checkpoint_{kind}.pt")
    (output/"standardizers.json").write_text(json.dumps(result.standardizers.to_dict(), indent=2, allow_nan=False)+"\n", encoding="utf-8")
    (output/"training_summary.json").write_text(json.dumps(result.summary, indent=2, allow_nan=False)+"\n", encoding="utf-8")
    with (output/"training_metrics.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(result.history[0]))
        writer.writeheader()
        writer.writerows(result.history)

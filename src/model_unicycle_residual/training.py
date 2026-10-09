"""Training and physical-unit evaluation for the unicycle residual MLP."""

from __future__ import annotations

import csv
from dataclasses import asdict, dataclass
import json
from pathlib import Path
import shlex
import subprocess
import sys
import time

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

from model_unicycle_residual.model import Standardizer, UnicycleResidualMLP
from unicycle_sim.dataset import UnicycleDataset
from unicycle_sim.frames import inertial_to_body


@dataclass(frozen=True)
class TrainingConfig:
    seed: int = 0
    epochs: int = 300
    batch_size: int = 256
    max_optimizer_updates: int = 5000
    learning_rate: float = 1e-3
    hidden_size: int = 64
    hidden_layers: int = 2

    def __post_init__(self) -> None:
        if min(self.epochs, self.batch_size, self.max_optimizer_updates, self.hidden_size, self.hidden_layers) <= 0:
            raise ValueError("epochs, batch size, update limit, and architecture sizes must be positive")
        if self.learning_rate <= 0:
            raise ValueError("learning_rate must be positive")


@dataclass
class TrainingResult:
    model: UnicycleResidualMLP
    input_scaler: Standardizer
    target_scaler: Standardizer
    history: list[dict]
    config: TrainingConfig
    optimizer_updates: int
    best_epoch: int
    best_validation_loss: float
    best_model_state: dict[str, torch.Tensor]
    final_model_state: dict[str, torch.Tensor]
    test_metrics: dict[str, float]
    data_metadata: dict


def _split_arrays(dataset: UnicycleDataset, label: str) -> tuple[torch.Tensor, torch.Tensor]:
    samples = dataset.samples(label)
    controls_dt = np.column_stack((samples["control_current"], samples["dt"]))
    inputs = torch.as_tensor(controls_dt, dtype=torch.float32)
    inertial_xy = samples["delta_inertial_true"][:, :2]
    headings = samples["state_current"][:, 2]
    reconstructed = np.column_stack((
        inertial_to_body(inertial_xy, headings),
        samples["delta_inertial_true"][:, 2],
    ))
    if not np.allclose(reconstructed, samples["delta_body_target"], rtol=1e-10, atol=1e-10):
        raise ValueError("saved body targets do not agree with targets reconstructed from inertial states")
    targets = torch.as_tensor(reconstructed, dtype=torch.float32)
    return inputs, targets


def _physical_metrics(predicted: torch.Tensor, target: torch.Tensor) -> dict[str, float]:
    error = predicted - target
    names = ("dx_body", "dy_body", "dtheta")
    result = {}
    for index, name in enumerate(names):
        result[f"{name}_mae"] = float(error[:, index].abs().mean())
        result[f"{name}_rmse"] = float(torch.sqrt(torch.mean(error[:, index] ** 2)))
    result["overall_rmse"] = float(torch.sqrt(torch.mean(error ** 2)))
    return result


def train_model(dataset: UnicycleDataset, config: TrainingConfig = TrainingConfig()) -> TrainingResult:
    """Train with dataset-provided trajectory splits and training-only scaling."""
    torch.manual_seed(config.seed)
    np.random.seed(config.seed)
    train_x, train_y = _split_arrays(dataset, "train")
    val_x, val_y = _split_arrays(dataset, "validation")
    test_x, test_y = _split_arrays(dataset, "test")
    input_scaler = Standardizer.fit(train_x)
    target_scaler = Standardizer.fit(train_y)
    train_xs, train_ys = input_scaler.transform(train_x), target_scaler.transform(train_y)
    val_xs, val_ys = input_scaler.transform(val_x), target_scaler.transform(val_y)
    test_xs = input_scaler.transform(test_x)

    loader = DataLoader(
        TensorDataset(train_xs, train_ys), batch_size=config.batch_size, shuffle=True,
        drop_last=False, generator=torch.Generator().manual_seed(config.seed),
    )
    model = UnicycleResidualMLP(hidden_size=config.hidden_size, hidden_layers=config.hidden_layers)
    optimizer = torch.optim.Adam(model.parameters(), lr=config.learning_rate)
    loss_fn = nn.MSELoss()
    history: list[dict] = []
    best_loss, best_epoch, best_state = float("inf"), 0, None
    updates, epoch = 0, 0

    while epoch < config.epochs and updates < config.max_optimizer_updates:
        epoch += 1
        started = time.perf_counter()
        model.train()
        weighted_loss, seen, batches = 0.0, 0, 0
        for batch_x, batch_y in loader:
            if updates >= config.max_optimizer_updates:
                break
            optimizer.zero_grad(set_to_none=True)
            loss = loss_fn(model(batch_x), batch_y)
            loss.backward()
            optimizer.step()
            weighted_loss += float(loss.detach()) * len(batch_x)
            seen += len(batch_x)
            batches += 1
            updates += 1

        model.eval()
        with torch.no_grad():
            val_loss = float(loss_fn(model(val_xs), val_ys))
        train_loss = weighted_loss / seen
        row = {
            "epoch": epoch, "optimizer_updates": updates, "batch_size": config.batch_size,
            "batches_per_epoch": batches, "train_loss": train_loss,
            "validation_loss": val_loss, "learning_rate": optimizer.param_groups[0]["lr"],
            "epoch_seconds": time.perf_counter() - started,
        }
        history.append(row)
        if val_loss < best_loss:
            best_loss, best_epoch = val_loss, epoch
            best_state = {key: value.detach().cpu().clone() for key, value in model.state_dict().items()}

    final_state = {key: value.detach().cpu().clone() for key, value in model.state_dict().items()}
    assert best_state is not None
    model.load_state_dict(best_state)
    model.eval()
    with torch.no_grad():
        test_prediction = target_scaler.inverse_transform(model(test_xs))
    metrics = _physical_metrics(test_prediction, test_y)
    return TrainingResult(
        model=model, input_scaler=input_scaler, target_scaler=target_scaler,
        history=history, config=config, optimizer_updates=updates,
        best_epoch=best_epoch, best_validation_loss=best_loss,
        best_model_state=best_state, final_model_state=final_state,
        test_metrics=metrics, data_metadata=dataset.metadata,
    )


def save_training_outputs(result: TrainingResult, output_dir: str | Path) -> None:
    """Save logs, standardizers, checkpoints, metrics, and a run README."""
    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    repo_root = Path(__file__).resolve().parents[2]
    try:
        revision = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"], cwd=repo_root,
            check=True, capture_output=True, text=True,
        ).stdout.strip()
        dirty = bool(subprocess.run(
            ["git", "status", "--porcelain"], cwd=repo_root,
            check=True, capture_output=True, text=True,
        ).stdout.strip())
        code_version = f"{revision} (working tree {'dirty' if dirty else 'clean'})"
    except (OSError, subprocess.CalledProcessError):
        code_version = "unknown"
    fields = list(result.history[0])
    with (root / "training_metrics.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(result.history)

    standardizers = {
        "feature_order": ["v", "omega", "dt"],
        "target_order": ["delta_x_body", "delta_y_body", "delta_theta"],
        "input_mean": result.input_scaler.mean.tolist(),
        "input_scale": result.input_scaler.scale.tolist(),
        "target_mean": result.target_scaler.mean.tolist(),
        "target_scale": result.target_scaler.scale.tolist(),
        "scale_handling": "population standard deviation; scales <= 1e-8 replaced by 1",
        "fit_split": "train only",
    }
    (root / "standardizers.json").write_text(json.dumps(standardizers, indent=2), encoding="utf-8")
    metadata = {
        "command": shlex.join([sys.executable, *sys.argv]),
        "code_version": code_version,
        "training_config": asdict(result.config),
        "optimizer": "Adam",
        "optimizer_updates": result.optimizer_updates,
        "best_epoch": result.best_epoch,
        "best_validation_loss_standardized": result.best_validation_loss,
        "test_metrics_physical_units": result.test_metrics,
        "dataset": result.data_metadata,
        "architecture": {"input_size": 3, "hidden_size": result.config.hidden_size,
                         "hidden_layers": result.config.hidden_layers, "output_size": 3,
                         "activation": "Tanh"},
    }
    (root / "run_metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    (root / "test_metrics.json").write_text(json.dumps(result.test_metrics, indent=2), encoding="utf-8")
    common = {
        "input_mean": result.input_scaler.mean, "input_scale": result.input_scaler.scale,
        "target_mean": result.target_scaler.mean, "target_scale": result.target_scaler.scale,
        "training_config": asdict(result.config), "feature_order": standardizers["feature_order"],
        "target_order": standardizers["target_order"],
    }
    torch.save({**common, "model_state_dict": result.best_model_state,
                "checkpoint_type": "best_validation", "best_epoch": result.best_epoch}, root / "checkpoint_best.pt")
    torch.save({**common, "model_state_dict": result.final_model_state,
                "checkpoint_type": "final_optimizer_update", "optimizer_updates": result.optimizer_updates}, root / "checkpoint_final.pt")
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    epochs = [row["epoch"] for row in result.history]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(epochs, [row["train_loss"] for row in result.history], label="train")
    ax.plot(epochs, [row["validation_loss"] for row in result.history], label="validation")
    ax.set(xlabel="Epoch", ylabel="Standardized MSE", title="Unicycle one-step training")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(root / "loss_curves.png", dpi=160)
    plt.close(fig)
    readme = (
        "# Unicycle U3 residual model run\n\n"
        "The MLP maps standardized [v, omega, dt] to standardized body-frame "
        "[delta_x_body, delta_y_body, delta_theta]. Standardizers were fit on training trajectories only.\n\n"
        "Coordinate convention: right-handed inertial x-y plane; body +x forward, body +y left, "
        "theta=0 along inertial +x, positive omega counter-clockwise.\n\n"
        f"- Command: `{shlex.join([sys.executable, *sys.argv])}`\n"
        f"- Code version: {code_version}\n"
        f"- Seed: {result.config.seed}\n- Optimizer updates: {result.optimizer_updates}\n"
        f"- Best validation epoch: {result.best_epoch}\n- Best standardized validation MSE: {result.best_validation_loss:.8g}\n"
        f"- Test physical-unit metrics: `{json.dumps(result.test_metrics, sort_keys=True)}`\n"
    )
    (root / "README.md").write_text(readme, encoding="utf-8")

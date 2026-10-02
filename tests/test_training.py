import csv

import numpy as np
import torch

from pendulum_sim.data import SimulationConfig, generate_dataset
from model_baseline.evaluation import (
    evaluate_model,
    evaluate_trajectory_metrics,
    plot_trajectory_prediction,
)
from pendulum_sim.simulator import PendulumParameters
from model_baseline.training import (
    make_training_loader,
    save_checkpoint,
    save_training_log,
    split_trajectory_indices,
    train_supervised,
)


def make_dataset():
    params = PendulumParameters(mass=1.0, length=1.0, gravity=9.81, damping=0.1)
    configs = [
        SimulationConfig(
            theta0=0.1 * index,
            omega0=0.05 * index,
            params=params,
            torque_fn=lambda t, index=index: 0.02 * index * t,
            torque_name="linear",
            torque_parameters={"slope": 0.02 * index},
        )
        for index in range(5)
    ]
    return generate_dataset(configs, duration=1.0, num_steps=20)


def test_split_uses_disjoint_complete_trajectories() -> None:
    split = split_trajectory_indices(5, seed=3)
    groups = [set(split.train), set(split.validation), set(split.test)]

    assert sum(len(group) for group in groups) == 5
    assert not (groups[0] & groups[1] or groups[0] & groups[2] or groups[1] & groups[2])


def test_training_records_losses_and_evaluates_physical_units(tmp_path) -> None:
    dataset = make_dataset()
    result = train_supervised(dataset, max_epochs=3, seed=4)
    metrics = evaluate_model(
        dataset,
        result.model,
        result.split.test,
        result.input_scaler,
        result.target_scaler,
    )

    assert len(result.history["train_loss"]) == 3
    assert len(result.history["validation_loss"]) == 3
    assert np.isfinite(metrics["rmse"])
    assert metrics["mae"] >= 0.0

    checkpoint_path = tmp_path / "model.pt"
    prediction_plot_path = tmp_path / "prediction.png"
    save_checkpoint(result, checkpoint_path)
    plot_trajectory_prediction(
        dataset,
        result.model,
        int(result.split.test[0]),
        result.input_scaler,
        result.target_scaler,
        prediction_plot_path,
    )

    assert checkpoint_path.exists()
    checkpoint = torch.load(checkpoint_path, weights_only=False)
    assert checkpoint["seed"] == 4
    assert checkpoint["training_config"]["max_epochs"] == 3
    assert prediction_plot_path.exists()
    assert prediction_plot_path.stat().st_size > 0


def test_training_returns_lowest_validation_loss_checkpoint() -> None:
    dataset = make_dataset()
    result = train_supervised(dataset, max_epochs=8, seed=4)
    inputs, targets = dataset.as_tensors()
    trajectory_indices = result.split.validation
    num_times = dataset.theta.shape[1]
    row_indices = np.concatenate(
        [np.arange(index * num_times, (index + 1) * num_times) for index in trajectory_indices]
    )
    rows = torch.as_tensor(row_indices, dtype=torch.long)
    validation_inputs = result.input_scaler.transform(inputs[rows])
    validation_targets = result.target_scaler.transform(targets[rows])
    result.model.eval()
    with torch.no_grad():
        final_validation_loss = torch.nn.functional.mse_loss(
            result.model(validation_inputs), validation_targets
        ).item()

    assert np.isclose(final_validation_loss, min(result.history["validation_loss"]), atol=1e-6)


def test_evaluate_trajectory_metrics_reports_both_states_separately() -> None:
    dataset = make_dataset()
    result = train_supervised(dataset, max_epochs=2, seed=4)
    metrics = evaluate_trajectory_metrics(
        dataset,
        result.model,
        result.split.test,
        result.input_scaler,
        result.target_scaler,
    )

    assert len(metrics) == len(result.split.test)
    assert {"theta_mae", "theta_rmse", "omega_mae", "omega_rmse"} <= metrics[0].keys()


def test_training_loader_shuffles_aligned_samples_and_keeps_final_batch() -> None:
    inputs = torch.arange(32, dtype=torch.float32).reshape(-1, 1)
    targets = torch.cat([inputs, inputs * 3.0], dim=1)
    loader = make_training_loader(inputs, targets, batch_size=7, seed=11)
    observed_inputs = []
    observed_targets = []
    batch_sizes = []

    for batch_inputs, batch_targets in loader:
        observed_inputs.append(batch_inputs)
        observed_targets.append(batch_targets)
        batch_sizes.append(batch_inputs.shape[0])

    shuffled_inputs = torch.cat(observed_inputs)
    shuffled_targets = torch.cat(observed_targets)
    assert batch_sizes == [7, 7, 7, 7, 4]
    assert sorted(shuffled_inputs[:, 0].tolist()) == list(range(32))
    assert torch.equal(shuffled_targets[:, 0], shuffled_inputs[:, 0])
    assert torch.equal(shuffled_targets[:, 1], shuffled_inputs[:, 0] * 3.0)
    assert not torch.equal(shuffled_inputs[:, 0], inputs[:, 0])


def test_training_loader_can_create_exact_number_of_balanced_batches() -> None:
    inputs = torch.arange(32, dtype=torch.float32).reshape(-1, 1)
    targets = torch.cat([inputs, inputs * 3.0], dim=1)
    loader = make_training_loader(
        inputs,
        targets,
        batch_size=None,
        batches_per_epoch=10,
        seed=11,
    )
    batches = list(loader)
    batch_sizes = [batch_inputs.shape[0] for batch_inputs, _ in batches]
    shuffled_inputs = torch.cat([batch_inputs for batch_inputs, _ in batches])
    shuffled_targets = torch.cat([batch_targets for _, batch_targets in batches])

    assert len(batches) == 10
    assert sorted(batch_sizes) == [3] * 8 + [4] * 2
    assert sorted(shuffled_inputs[:, 0].tolist()) == list(range(32))
    assert torch.equal(shuffled_targets[:, 0], shuffled_inputs[:, 0])
    assert torch.equal(shuffled_targets[:, 1], shuffled_inputs[:, 0] * 3.0)
    next_epoch_inputs = torch.cat([batch_inputs for batch_inputs, _ in loader])
    assert not torch.equal(shuffled_inputs, next_epoch_inputs)


def test_training_records_updates_samples_learning_rate_and_losses() -> None:
    dataset = make_dataset()
    result = train_supervised(
        dataset,
        max_epochs=5,
        max_optimizer_steps=4,
        batch_size=16,
        seed=4,
    )
    training_sample_count = len(result.split.train) * dataset.theta.shape[1]

    assert result.history["epoch"] == [1.0]
    assert result.history["optimizer_step"] == [4.0]
    assert result.history["samples_seen"] == [float(training_sample_count)]
    assert len(result.history["learning_rate"]) == 1
    assert len(result.history["train_loss"]) == 1
    assert len(result.history["validation_loss"]) == 1
    assert result.training_config["batch_size"] == 16
    assert result.training_config["max_optimizer_steps"] == 4
    assert result.training_config["scheduler_factor"] == 0.5
    assert result.training_config["scheduler_patience"] == 10
    assert result.training_config["min_learning_rate"] == 1e-6


def test_training_with_batches_per_epoch_logs_balanced_batch_config() -> None:
    dataset = make_dataset()
    result = train_supervised(
        dataset,
        max_epochs=5,
        max_optimizer_steps=3,
        batch_size=None,
        batches_per_epoch=2,
        seed=4,
    )
    training_sample_count = len(result.split.train) * dataset.theta.shape[1]

    assert result.training_config["batch_size"] is None
    assert result.training_config["batches_per_epoch"] == 2
    assert result.training_config["minimum_batch_size"] == training_sample_count // 2
    assert result.training_config["maximum_batch_size"] == (training_sample_count + 1) // 2
    assert result.history["optimizer_step"][-1] == 4.0
    assert result.history["samples_seen"][-1] == float(training_sample_count * 2)


def test_training_log_saves_required_budget_fields(tmp_path) -> None:
    result = train_supervised(make_dataset(), max_epochs=1, batch_size=16, seed=4)
    log_path = tmp_path / "training_log.csv"

    save_training_log(result, log_path)

    with log_path.open(newline="", encoding="utf-8") as log_file:
        rows = list(csv.DictReader(log_file))
    assert set(rows[0]) == {
        "epoch",
        "optimizer_step",
        "samples_seen",
        "learning_rate",
        "training_loss",
        "validation_loss",
    }
    assert int(rows[0]["optimizer_step"]) == result.history["optimizer_step"][-1]

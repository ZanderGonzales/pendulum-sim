import numpy as np
import torch

from pendulum_sim.data import SimulationConfig, generate_dataset
from model_baseline.evaluation import (
    evaluate_model,
    evaluate_trajectory_metrics,
    plot_trajectory_prediction,
)
from pendulum_sim.simulator import PendulumParameters
from model_baseline.training import save_checkpoint, split_trajectory_indices, train_supervised


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
    result = train_supervised(dataset, epochs=3, seed=4)
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
    assert checkpoint["training_config"]["epochs"] == 3
    assert prediction_plot_path.exists()
    assert prediction_plot_path.stat().st_size > 0


def test_training_returns_lowest_validation_loss_checkpoint() -> None:
    dataset = make_dataset()
    result = train_supervised(dataset, epochs=8, seed=4)
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
    result = train_supervised(dataset, epochs=2, seed=4)
    metrics = evaluate_trajectory_metrics(
        dataset,
        result.model,
        result.split.test,
        result.input_scaler,
        result.target_scaler,
    )

    assert len(metrics) == len(result.split.test)
    assert {"theta_mae", "theta_rmse", "omega_mae", "omega_rmse"} <= metrics[0].keys()

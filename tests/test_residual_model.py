import numpy as np
import torch

from model_residual.model import ResidualStateNetwork
from model_residual.training import build_residual_step_dataset


def test_residual_network_predicts_delta_state_shape_and_backprop() -> None:
    model = ResidualStateNetwork(hidden_size=16)
    inputs = torch.randn(12, 5, requires_grad=True)

    outputs = model(inputs)
    loss = outputs.square().mean()
    loss.backward()

    assert outputs.shape == (12, 2)
    assert inputs.grad is not None
    assert all(parameter.grad is not None for parameter in model.parameters())


def test_residual_step_dataset_preserves_time_step_and_state_relationship() -> None:
    theta = np.array([[0.0, 0.1, 0.2], [0.5, 0.6, 0.7]], dtype=float)
    omega = np.array([[0.0, 0.2, 0.4], [0.1, 0.3, 0.5]], dtype=float)
    torque = np.array([[0.0, 0.4, 0.8], [1.0, 1.4, 1.8]], dtype=float)
    dataset = type(
        "DummyDataset",
        (),
        {
            "theta": theta,
            "omega": omega,
            "torque": torque,
        },
    )()

    inputs, targets = build_residual_step_dataset(dataset, np.asarray([0, 1]))

    assert inputs.shape == (4, 5)
    assert targets.shape == (4, 2)
    np.testing.assert_allclose(inputs[:, 0], np.array([0.0, 0.5, 0.1, 0.6]))
    np.testing.assert_allclose(inputs[:, 1], np.array([0.0, 0.1, 0.2, 0.3]))
    np.testing.assert_allclose(inputs[:, 2], np.array([0.0, 1.0, 0.4, 1.4]))
    np.testing.assert_allclose(inputs[:, 3], np.array([0.2, 1.2, 0.6, 1.6]))
    np.testing.assert_allclose(inputs[:, 4], np.array([0.4, 1.4, 0.8, 1.8]))
    np.testing.assert_allclose(targets[:, 0], np.array([0.1, 0.1, 0.1, 0.1]))
    np.testing.assert_allclose(targets[:, 1], np.array([0.2, 0.2, 0.2, 0.2]))

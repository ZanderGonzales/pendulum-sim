import numpy as np
import torch

from model_unicycle_residual import TrainingConfig, UnicycleResidualMLP, train_model
from unicycle_sim.dataset import DatasetConfig, generate_dataset
from unicycle_sim.frames import body_to_inertial, inertial_to_body


def test_standardizer_zero_scale_and_model_shape():
    from model_unicycle_residual import Standardizer

    values = torch.tensor([[2.0, 1.0], [2.0, 3.0]])
    scaler = Standardizer.fit(values)
    assert torch.equal(scaler.scale, torch.tensor([1.0, 1.0]))
    assert torch.allclose(scaler.inverse_transform(scaler.transform(values)), values)
    assert UnicycleResidualMLP()(torch.zeros(4, 3)).shape == (4, 3)


def test_batched_frame_transforms_support_per_sample_heading():
    vectors = np.array([[1.0, 0.0], [1.0, 0.0]])
    headings = np.array([0.0, np.pi / 2])
    rotated = body_to_inertial(vectors, headings)
    assert np.allclose(rotated, [[1.0, 0.0], [0.0, 1.0]], atol=1e-14)
    assert np.allclose(inertial_to_body(rotated, headings), vectors)


def test_training_uses_trajectory_splits_and_saves_physical_metrics():
    data = generate_dataset(DatasetConfig(
        num_trajectories=24, num_steps=12, dt=0.1,
        speed_range=(0.2, 1.5), omega_range=(-0.8, 0.8),
        control_hold_steps=(1, 3), seed=31,
    ))
    result = train_model(data, TrainingConfig(
        seed=32, epochs=3, batch_size=32, max_optimizer_updates=8,
        hidden_size=16, hidden_layers=1,
    ))
    assert result.optimizer_updates == 8
    assert result.best_epoch >= 1
    assert result.input_scaler.mean.shape == (3,)
    training = data.samples("train")["control_current"]
    expected_mean = np.r_[training.mean(axis=0), data.metadata["dt"]]
    assert np.allclose(result.input_scaler.mean.numpy(), expected_mean, atol=1e-7)
    assert set(result.test_metrics) == {
        "dx_body_mae", "dx_body_rmse", "dy_body_mae", "dy_body_rmse",
        "dtheta_mae", "dtheta_rmse", "overall_rmse",
    }

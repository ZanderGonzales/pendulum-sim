import numpy as np
import torch
from torch import nn

from model_unicycle_residual.evaluation import recursive_rollout


class FixedIncrementModel(nn.Module):
    def __init__(self, increment):
        super().__init__()
        self.register_buffer("increment", torch.tensor(increment, dtype=torch.float32))

    def forward(self, inputs):
        return self.increment.expand(inputs.shape[0], -1)


def test_recursive_rollout_rotates_with_predicted_heading():
    model = FixedIncrementModel([1.0, 0.0, np.pi / 2])
    checkpoint = {
        "input_mean": torch.zeros(3), "input_scale": torch.ones(3),
        "target_mean": torch.zeros(3), "target_scale": torch.ones(3),
    }
    predicted, body = recursive_rollout(
        model, checkpoint, np.array([0.0, 0.0, 0.0]),
        np.array([[1.0, 0.2], [1.0, 0.2]]), 0.1,
    )
    assert np.allclose(body[:, :2], [[1.0, 0.0], [1.0, 0.0]])
    assert np.allclose(predicted, [[0, 0, 0], [1, 0, np.pi / 2], [1, 1, np.pi]], atol=1e-6)

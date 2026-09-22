"""Phase 1 environment checks."""

import numpy as np
import torch


def test_numpy_and_torch_are_available() -> None:
    values = torch.tensor(np.array([1.0, 2.0, 3.0]))

    assert values.shape == (3,)
    expected_sum = torch.tensor(6.0, dtype=values.dtype)
    assert torch.isclose(values.sum(), expected_sum)

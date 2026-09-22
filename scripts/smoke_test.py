"""Run a minimal Phase 1 environment check."""

import numpy as np
import torch


def main() -> None:
    values = torch.tensor(np.array([1.0, 2.0, 3.0]))
    print(f"PyTorch version: {torch.__version__}")
    print(f"NumPy version: {np.__version__}")
    print(f"Tensor values: {values.tolist()}")
    print(f"Tensor sum: {values.sum().item():.1f}")


if __name__ == "__main__":
    main()

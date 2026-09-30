from __future__ import annotations

from dataclasses import dataclass

import torch
from torch import nn


@dataclass
class Standardizer:
    """Feature-wise standardization values for reproducible preprocessing."""

    mean: torch.Tensor
    std: torch.Tensor

    @classmethod
    def fit(cls, values: torch.Tensor) -> Standardizer:
        if values.ndim != 2:
            raise ValueError("values must have shape (samples, features)")

        mean = values.mean(dim=0)
        std = values.std(dim=0, unbiased=False)
        safe_std = torch.where(std > 0, std, torch.ones_like(std))
        return cls(mean=mean, std=safe_std)

    def transform(self, values: torch.Tensor) -> torch.Tensor:
        return (values - self.mean) / self.std

    def inverse_transform(self, values: torch.Tensor) -> torch.Tensor:
        return values * self.std + self.mean


class PendulumStateNetwork(nn.Module):
    """Small MLP mapping trajectory inputs to angle and angular velocity."""

    def __init__(
        self,
        input_size: int = 4,
        hidden_size: int = 64,
        output_size: int = 2,
    ) -> None:
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.Tanh(),
            nn.Linear(hidden_size, hidden_size),
            nn.Tanh(),
            nn.Linear(hidden_size, output_size),
        )

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        if inputs.shape[-1] != 4:
            raise ValueError("inputs must have four features: t, theta0, omega0, and torque")
        return self.network(inputs)

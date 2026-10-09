"""Small MLP that predicts one-step body-frame unicycle increments."""

from dataclasses import dataclass

import torch
from torch import nn


@dataclass
class Standardizer:
    """Feature-wise standardizer fitted from training samples only."""

    mean: torch.Tensor
    scale: torch.Tensor

    @classmethod
    def fit(cls, values: torch.Tensor, minimum_scale: float = 1e-8) -> "Standardizer":
        if values.ndim != 2 or values.shape[0] == 0:
            raise ValueError("values must be a nonempty (samples, features) tensor")
        mean = values.mean(dim=0)
        scale = values.std(dim=0, unbiased=False)
        scale = torch.where(scale > minimum_scale, scale, torch.ones_like(scale))
        return cls(mean=mean, scale=scale)

    def transform(self, values: torch.Tensor) -> torch.Tensor:
        return (values - self.mean) / self.scale

    def inverse_transform(self, values: torch.Tensor) -> torch.Tensor:
        return values * self.scale + self.mean


class UnicycleResidualMLP(nn.Module):
    """Map [v, omega, dt] to standardized [dx_body, dy_body, dtheta]."""

    def __init__(self, input_size: int = 3, hidden_size: int = 64, hidden_layers: int = 2, output_size: int = 3):
        super().__init__()
        if input_size <= 0 or hidden_size <= 0 or hidden_layers <= 0 or output_size != 3:
            raise ValueError("input/hidden sizes and layers must be positive; output_size must be 3")
        layers: list[nn.Module] = [nn.Linear(input_size, hidden_size), nn.Tanh()]
        for _ in range(hidden_layers - 1):
            layers.extend([nn.Linear(hidden_size, hidden_size), nn.Tanh()])
        layers.append(nn.Linear(hidden_size, output_size))
        self.network = nn.Sequential(*layers)
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.hidden_layers = hidden_layers
        self.output_size = output_size

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        if inputs.shape[-1] != self.input_size:
            raise ValueError(f"inputs must have {self.input_size} features")
        return self.network(inputs)

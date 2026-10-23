"""Configurable residual MLP and precision-preserving train-only standardizers."""

from dataclasses import dataclass

import numpy as np
import torch
from torch import nn

from model_drone_residual.residuals import FEATURE_ORDER, TARGET_ORDER


@dataclass(frozen=True)
class Standardizer:
    """Population statistics in float64; only truly constant columns use scale 1.

    An absolute floor such as 1e-8 would discard the natural scale of the drone's
    small residual targets. Standardize BEFORE converting to NN float32 tensors.
    """

    mean: np.ndarray
    scale: np.ndarray

    def __post_init__(self):
        mean, scale = np.array(self.mean, dtype=np.float64, copy=True), np.array(self.scale, dtype=np.float64, copy=True)
        if (mean.ndim != 1 or len(mean) < 1 or scale.shape != mean.shape or
                not np.isfinite(mean).all() or not np.isfinite(scale).all() or np.any(scale <= 0)):
            raise ValueError("standardizer needs finite matching 1D mean and positive scale")
        mean.setflags(write=False)
        scale.setflags(write=False)
        object.__setattr__(self, "mean", mean)
        object.__setattr__(self, "scale", scale)

    @classmethod
    def fit(cls, values) -> "Standardizer":
        values = np.asarray(values, dtype=np.float64)
        if values.ndim != 2 or min(values.shape) < 1 or not np.isfinite(values).all():
            raise ValueError("fit values must be a nonempty finite (samples,features) array")
        constant = np.min(values, axis=0) == np.max(values, axis=0)
        mean, scale = values.mean(axis=0), values.std(axis=0, ddof=0)
        mean[constant], scale[constant] = values[0, constant], 1.
        return cls(mean, scale)

    def _values(self, values):
        values = np.asarray(values, dtype=np.float64)
        if values.ndim < 1 or values.shape[-1] != len(self.mean) or not np.isfinite(values).all():
            raise ValueError(f"values must be finite with {len(self.mean)} features")
        return values

    def transform(self, values) -> np.ndarray:
        return (self._values(values)-self.mean)/self.scale

    def inverse_transform(self, values) -> np.ndarray:
        return self._values(values)*self.scale+self.mean


class DroneResidualMLP(nn.Module):
    """14 standardized features -> 12 standardized physics residual coordinates."""

    def __init__(self, hidden_size: int = 64, hidden_layers: int = 2):
        super().__init__()
        for name, value in (("hidden_size", hidden_size), ("hidden_layers", hidden_layers)):
            if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                raise ValueError(f"{name} must be a positive integer")
        self.input_size, self.output_size = len(FEATURE_ORDER), len(TARGET_ORDER)
        self.hidden_size, self.hidden_layers = hidden_size, hidden_layers
        layers = []
        previous = self.input_size
        for _ in range(hidden_layers):
            layers.extend((nn.Linear(previous, hidden_size), nn.Tanh()))
            previous = hidden_size
        layers.append(nn.Linear(previous, self.output_size))
        self.network = nn.Sequential(*layers)

    @property
    def parameter_count(self) -> int:
        return sum(parameter.numel() for parameter in self.parameters() if parameter.requires_grad)

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        if inputs.ndim < 1 or inputs.shape[-1] != self.input_size:
            raise ValueError(f"inputs must have {self.input_size} features")
        return self.network(inputs)


@dataclass(frozen=True)
class ResidualStandardizers:
    inputs: Standardizer
    targets: Standardizer
    training_trajectory_ids: tuple
    training_sample_count: int

    def __post_init__(self):
        if len(self.inputs.mean) != len(FEATURE_ORDER) or len(self.targets.mean) != len(TARGET_ORDER):
            raise ValueError("standardizers must match the 14-input/12-target residual contract")
        ids = tuple(self.training_trajectory_ids)
        if not ids or any(not isinstance(value, str) or not value for value in ids) or len(set(ids)) != len(ids):
            raise ValueError("training trajectory IDs must be nonempty unique strings")
        count = self.training_sample_count
        if isinstance(count, bool) or not isinstance(count, int) or count < len(ids):
            raise ValueError("training sample count must cover every fitting trajectory")
        object.__setattr__(self, "training_trajectory_ids", ids)

    def to_dict(self) -> dict:
        return {"schema_version": 1, "feature_order": list(FEATURE_ORDER), "target_order": list(TARGET_ORDER),
                "input_mean": self.inputs.mean.tolist(), "input_scale": self.inputs.scale.tolist(),
                "target_mean": self.targets.mean.tolist(), "target_scale": self.targets.scale.tolist(),
                "fit_split": "train", "training_trajectory_ids": list(self.training_trajectory_ids),
                "training_sample_count": self.training_sample_count, "statistics_dtype": "float64",
                "scale_handling": "population std; exactly constant columns use mean=first value, scale=1; no absolute scale floor"}

    @classmethod
    def from_dict(cls, value: dict) -> "ResidualStandardizers":
        if (value.get("schema_version") != 1 or value.get("feature_order") != list(FEATURE_ORDER) or
                value.get("target_order") != list(TARGET_ORDER) or value.get("fit_split") != "train"):
            raise ValueError("invalid residual standardizer schema, feature/target order, or fit split")
        return cls(Standardizer(value["input_mean"], value["input_scale"]),
                   Standardizer(value["target_mean"], value["target_scale"]),
                   tuple(value["training_trajectory_ids"]), value["training_sample_count"])

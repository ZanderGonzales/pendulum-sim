"""Ideal planar unicycle simulator with explicit body/inertial conventions."""

from unicycle_sim.dataset import DatasetConfig, UnicycleDataset, generate_dataset, load_dataset, save_dataset
from unicycle_sim.dynamics import body_increment, continuous_dynamics, simulate_trajectory, step
from unicycle_sim.frames import angle_difference, body_to_inertial, inertial_to_body, wrap_angle
from unicycle_sim.types import UnicycleControl, UnicycleState, UnicycleTrajectory

__all__ = [
    "DatasetConfig", "UnicycleControl", "UnicycleDataset", "UnicycleState", "UnicycleTrajectory", "angle_difference",
    "body_increment", "body_to_inertial", "continuous_dynamics", "inertial_to_body",
    "generate_dataset", "load_dataset", "save_dataset", "simulate_trajectory", "step", "wrap_angle",
]

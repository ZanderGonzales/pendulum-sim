from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import torch

from pendulum_sim.data import generate_dataset
from model_baseline.experiments import build_data_quantity_cases
from model_baseline.training import (
    TrajectorySplit,
    save_checkpoint,
    tensors_for_trajectories,
    train_supervised,
)


def main() -> None:
    epochs = 90
    seed = 17
    duration = 2.0
    num_steps = 80
    learning_rate = 1e-3
    case = build_data_quantity_cases(train_sizes=(32,))[0]

    training_configs = case["train_configs"] + case["validation_configs"]
    training_dataset = generate_dataset(
        training_configs,
        duration=duration,
        num_steps=num_steps,
    )
    test_dataset = generate_dataset(
        case["test_configs"],
        duration=duration,
        num_steps=num_steps,
    )
    split = TrajectorySplit(
        train=np.arange(len(case["train_configs"]), dtype=int),
        validation=np.arange(
            len(case["train_configs"]),
            len(training_configs),
            dtype=int,
        ),
        test=np.asarray([], dtype=int),
    )
    result = train_supervised(
        training_dataset,
        max_epochs=epochs,
        learning_rate=learning_rate,
        seed=seed,
        split=split,
    )

    output_dir = Path("runs/phase6_32_trajectories_90_epochs")
    output_dir.mkdir(parents=True, exist_ok=True)
    save_checkpoint(result, output_dir / "checkpoint.pt")

    state_predictions: list[np.ndarray] = []
    for trajectory_index in range(test_dataset.theta.shape[0]):
        inputs, _ = tensors_for_trajectories(
            test_dataset,
            np.asarray([trajectory_index], dtype=int),
        )
        result.model.eval()
        with torch.no_grad():
            prediction = result.target_scaler.inverse_transform(
                result.model(result.input_scaler.transform(inputs))
            )
        state_predictions.append(prediction.numpy())

    state_labels = ["Angle, theta (rad)", "Angular velocity, theta dot (rad/s)"]
    state_arrays = [test_dataset.theta, test_dataset.omega]
    output_names = ["theta_vs_time.png", "theta_dot_vs_time.png"]

    for state_index, (state_label, true_values, output_name) in enumerate(
        zip(state_labels, state_arrays, output_names)
    ):
        figure, axes = plt.subplots(
            len(case["test_configs"]),
            1,
            figsize=(9, 9),
            sharex=True,
            squeeze=False,
        )
        for trajectory_index, axis_row in enumerate(axes):
            axis = axis_row[0]
            initial_condition = case["test_configs"][trajectory_index]
            true_state = true_values[trajectory_index]
            predicted_state = state_predictions[trajectory_index][:, state_index]
            axis.plot(
                test_dataset.time,
                true_state,
                color="red",
                label="Simulator truth",
            )
            axis.plot(
                test_dataset.time,
                predicted_state,
                color="blue",
                linestyle="--",
                label="Model prediction",
            )
            axis.set_ylabel(state_label)
            axis.set_title(
                f"Test trajectory {trajectory_index + 1}: "
                f"theta0={initial_condition.theta0:.2f} rad, "
                f"theta-dot0={initial_condition.omega0:.2f} rad/s"
            )
            axis.grid(True, alpha=0.3)
            axis.legend(loc="best")

        axes[-1, 0].set_xlabel("Time (s)")
        figure.suptitle(f"32 training trajectories, {epochs} epochs: {state_label}")
        figure.tight_layout()
        figure.savefig(output_dir / output_name, dpi=200)
        plt.close(figure)

    print(f"Final training loss: {result.history['train_loss'][-1]:.6f}")
    print(f"Final validation loss: {result.history['validation_loss'][-1]:.6f}")
    print(f"Saved plots and checkpoint in {output_dir}")


if __name__ == "__main__":
    main()

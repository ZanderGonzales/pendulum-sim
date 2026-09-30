from pendulum_sim.data import SimulationConfig, generate_dataset
from model_baseline.evaluation import evaluate_model, plot_training_history, plot_trajectory_prediction
from pendulum_sim.simulator import PendulumParameters
from model_baseline.training import save_checkpoint, train_supervised


def main() -> None:
    params = PendulumParameters(mass=1.0, length=1.0, gravity=9.81, damping=0.1)
    configs = [
        SimulationConfig(
            theta0=0.1 * index,
            omega0=0.05 * index,
            params=params,
            torque_fn=lambda t, index=index: 0.02 * index * t,
            torque_name="linear",
            torque_parameters={"slope": 0.02 * index},
        )
        for index in range(10)
    ]
    dataset = generate_dataset(configs, duration=2.0, num_steps=100)
    result = train_supervised(dataset, epochs=300, seed=7)
    metrics = evaluate_model(
        dataset,
        result.model,
        result.split.test,
        result.input_scaler,
        result.target_scaler,
    )
    plot_training_history(result.history, "runs/phase5_training_history.png")
    plot_trajectory_prediction(
        dataset,
        result.model,
        int(result.split.test[0]),
        result.input_scaler,
        result.target_scaler,
        "runs/phase5_prediction.png",
    )
    save_checkpoint(result, "runs/phase5_checkpoint.pt")

    print(f"Final training loss: {result.history['train_loss'][-1]:.6f}")
    print(f"Final validation loss: {result.history['validation_loss'][-1]:.6f}")
    print(f"Test metrics: {metrics}")
    print("Saved checkpoint and plots to runs/")


if __name__ == "__main__":
    main()

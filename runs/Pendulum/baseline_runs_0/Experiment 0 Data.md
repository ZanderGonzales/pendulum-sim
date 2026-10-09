## Data and Run Map

The Phase 7 baseline runner creates one reproducible dataset and saves it with the model outputs.

* Dataset: `runs/baseline_runs_N/simulation_dataset.npz` contains 40 pendulum trajectories: 32 training, 4 validation, and 4 test trajectories. The split is by complete trajectory, not by time sample.
* Sampling: every trajectory covers 10 seconds with a 0.01-second time step, giving 1001 time points including the initial state.
* Physical parameters: mass 1 kg, length 1 m, gravity 9.81 m/s^2, and damping 0.1.
* Torque: all trajectories use the linear ramp `tau(t) = slope * t`. Training slopes cycle through -0.12, 0.0, and 0.12; validation slopes are 0.07, -0.07, 0.11, and -0.11; test slopes are 0.04, -0.08, 0.10, and -0.03.
* Model inputs and targets: each time point uses time, initial angle, initial angular velocity, and torque; the target is angle and angular velocity.
* Run folder: `runs/baseline_runs_N/` contains the dataset, selected model checkpoint, learning-curve graph, validation and test trajectory graphs, and test-error CSV. `N` starts at 0 and increases for each run.
* Test error table: one row per test trajectory reports angle and angular-velocity MAE/RMSE; final rows report the mean and standard deviation across test trajectories.

The data flow is: pendulum simulation creates the trajectories, the baseline trainer fits on the training trajectories and selects the checkpoint with the lowest validation MSE, then the test trajectories are evaluated once for the final per-trajectory metrics and example graph. The current baseline run uses 300 epochs, learning rate `0.001`, and random seed `7`.

## Code Layout

* `src/pendulum_sim/` contains the physical simulator, simulation data generation/storage, and physical visualization.
* `src/model_baseline/` contains the full-state network, training, evaluation, and baseline experiment helpers.
* `scripts/simulation/` contains simulation and data-generation demonstrations.
* `scripts/model_baseline/` contains model demonstrations and training/experiment runners.
* `tests/` contains automated checks for both packages.
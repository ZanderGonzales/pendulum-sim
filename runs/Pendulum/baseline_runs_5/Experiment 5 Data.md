# Experiment 5 Data

## Dataset

- Trajectories: 32 training, 4 validation, 4 test.
- Split unit: complete trajectories.
- Simulation duration: 10 seconds.
- Time step: 0.01 seconds; 1001 samples per trajectory, including the initial state.
- Physical parameters: mass=1.0 kg, length=1.0 m, gravity=9.81 m/s^2, damping=0.1.
- Training initial angles (rad): -0.7000, -0.5000, -0.3000, -0.1000, 0.1000, 0.3000, 0.5000, 0.7000.
- Training initial angular velocities (rad/s): -0.4000, -0.1333, 0.1333, 0.4000.
- Training initial conditions use every angle/velocity pair in the Cartesian product of those values.
- Torque family: linear ramp, tau(t) = slope * t.
- Training torque slopes (N m/s): -0.12, 0.00, 0.12.
- Validation cases (theta0 rad, omega0 rad/s, slope N m/s): (theta0=-0.63, omega0=0.20, slope=0.07); (theta0=-0.21, omega0=-0.20, slope=-0.07); (theta0=0.21, omega0=0.10, slope=0.11); (theta0=0.63, omega0=-0.10, slope=-0.11).
- Test cases (theta0 rad, omega0 rad/s, slope N m/s): (theta0=-0.50, omega0=0.13, slope=0.04); (theta0=-0.15, omega0=-0.28, slope=-0.08); (theta0=0.25, omega0=0.31, slope=0.10); (theta0=0.55, omega0=-0.08, slope=-0.03).
- Model inputs: time, initial angle, initial angular velocity, and applied torque; targets: angle and angular velocity.
- Training configuration: batch_size=None, batches_per_epoch=200, batch_size_range=160-161, max_epochs=150, max_optimizer_steps=20000, learning_rate=0.001, scheduler=ReduceLROnPlateau(factor=0.5, patience=10, min_lr=1e-06).
- Actual training: 20000 optimizer updates, 3203200 training samples processed.

## Changes From Experiment 4

- The training, validation, and test trajectories, model, seed, initial learning rate, scheduler settings, physical parameters, duration, and time step match Experiment 4.
- Each epoch uses exactly 200 shuffled, near-equal batches instead of 126 batches of 256 samples. With 32032 training samples, batches contain 160 or 161 samples, and every sample is used exactly once per epoch.
- The optimizer-step target increases from 15000 to 20000; the epoch ceiling remains 150. The target is reached exactly after 100 epochs because 200 updates per epoch divides 20000 evenly.
- This experiment changes batch organization and update count together, while leaving the dataset and other training settings unchanged.

## Training Procedure

- Training uses shuffled, non-dropping mini-batches; validation is evaluated in its original order after each epoch.
- The optimizer-step target was 20000; this run completed 20000 updates over 100 complete epochs, processing 3203200 training samples.
- ReduceLROnPlateau monitors validation MSE once per epoch and applies the configured factor, patience, and minimum learning rate.

## Files

- `simulation_dataset.npz`: all generated trajectories and simulation metadata.
- `baseline_checkpoint.pt`: model checkpoint selected by lowest validation MSE.
- `baseline_training_log.csv`: per-epoch update count, samples seen, learning rate, training loss, and validation loss.
- `baseline_learning_curves.png`: training and validation MSE versus epoch.
- `baseline_training_comparison.png`: prediction versus simulator on a validation trajectory.
- `baseline_test_comparison.png`: prediction versus simulator on the preselected first test trajectory.
- `baseline_test_error_data.csv`: per-test-trajectory state errors and aggregate mean/standard deviation.

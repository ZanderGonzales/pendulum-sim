# Experiment 4 Data

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
- Training configuration: batch_size=256, max_epochs=150, max_optimizer_steps=15000, learning_rate=0.001, scheduler=ReduceLROnPlateau(factor=0.5, patience=10, min_lr=1e-06).
- Actual training: 15120 optimizer updates, 3843840 training samples processed.

## Changes From Experiment 3

- The training, validation, and test trajectories, model, batch size, initial learning rate, scheduler, physical parameters, duration, time step, and seed match Experiment 3.
- The optimizer-step target increases from 5000 to 15000; the epoch ceiling increases from 100 to 150 so the run can reach that target.
- The target is checked after each complete epoch. With 126 batches per epoch, this run is expected to stop after 120 epochs and 15120 optimizer updates.
- This experiment tests whether additional optimization updates improve validation and test predictions while keeping the training data and batch configuration fixed.

## Training Procedure

- Training uses shuffled, non-dropping mini-batches; validation is evaluated in its original order after each epoch.
- The optimizer-step target was 15000; this run completed 15120 updates over 120 complete epochs, processing 3843840 training samples.
- ReduceLROnPlateau monitors validation MSE once per epoch and applies the configured factor, patience, and minimum learning rate.

## Files

- `simulation_dataset.npz`: all generated trajectories and simulation metadata.
- `baseline_checkpoint.pt`: model checkpoint selected by lowest validation MSE.
- `baseline_training_log.csv`: per-epoch update count, samples seen, learning rate, training loss, and validation loss.
- `baseline_learning_curves.png`: training and validation MSE versus epoch.
- `baseline_training_comparison.png`: prediction versus simulator on a validation trajectory.
- `baseline_test_comparison.png`: prediction versus simulator on the preselected first test trajectory.
- `baseline_test_error_data.csv`: per-test-trajectory state errors and aggregate mean/standard deviation.

# Experiment 1 Data

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
- Model inputs: current theta, current omega, torque at the current step, midpoint torque, and next-step torque; targets: residual angle change and residual angular-velocity change.
- Training configuration: batch_size=None, batches_per_epoch=200, batch_size_range=160-160, max_epochs=10, max_optimizer_steps=2000, learning_rate=0.001, scheduler=ReduceLROnPlateau(factor=0.5, patience=10, min_lr=1e-06).
- Actual training: 2000 optimizer updates, 320000 training samples processed.

## Changes From Residual Experiment 0

- This residual run uses the exact same trajectories as residual Experiment 0.
- The optimizer target is reduced from 20000 to 2000 updates and the epoch cap is lowered from 100 to 10 while keeping the 200-batch-per-epoch schedule fixed.
- This experiment tests how quickly the residual model reaches a good fit when training is much shorter.

## Training Procedure

- Training uses shuffled, non-dropping mini-batches; validation is evaluated in its original order after each epoch.
- The optimizer-step target was 2000; this run completed 2000 updates over 10 complete epochs, processing 320000 training samples.
- ReduceLROnPlateau monitors validation MSE once per epoch and applies the configured factor, patience, and minimum learning rate.

## Files

- `simulation_dataset.npz`: all generated trajectories and simulation metadata.
- `residual_checkpoint.pt`: model checkpoint selected by lowest validation MSE.
- `residual_training_log.csv`: per-epoch update count, samples seen, learning rate, training loss, and validation loss.
- `residual_learning_curves.png`: training and validation MSE versus epoch.
- `residual_training_comparison.png`: prediction versus simulator on a validation trajectory.
- `residual_test_comparison.png`: prediction versus simulator on the preselected first test trajectory.
- `residual_test_error_data.csv`: per-test-trajectory state errors and aggregate mean/standard deviation.

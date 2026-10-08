# Experiment 3 Data

## Dataset

- Trajectories: 32 training, 4 validation, 4 test.
- Split unit: complete trajectories.
- Simulation duration: 10 seconds.
- Time step: 0.01 seconds; 1001 samples per trajectory, including the initial state.
- Physical parameters: mass=1.0 kg, length=1.0 m, gravity=9.81 m/s^2, damping=0.1.
- Training initial angles (rad): -0.7000, -0.5000, -0.3000, -0.1000, 0.1000, 0.3000, 0.5000, 0.7000.
- Training initial angular velocities (rad/s): -0.4000, -0.1333, 0.1333, 0.4000.
- Training initial conditions use every angle/velocity pair in the Cartesian product of those values.
- Torque family: sinusoidal.
- Training cases (theta0 rad, omega0 rad/s, torque parameters): (theta0=-0.70, omega0=-0.40, amplitude=5, frequency=0); (theta0=-0.70, omega0=-0.13, amplitude=5.128, frequency=0.1611); (theta0=-0.70, omega0=0.13, amplitude=5.256, frequency=0.3222); (theta0=-0.70, omega0=0.40, amplitude=5.385, frequency=0.4833); (theta0=-0.50, omega0=-0.40, amplitude=5.513, frequency=0.6444); (theta0=-0.50, omega0=-0.13, amplitude=5.641, frequency=0.8055); (theta0=-0.50, omega0=0.13, amplitude=5.769, frequency=0.9666); (theta0=-0.50, omega0=0.40, amplitude=5.897, frequency=1.128); (theta0=-0.30, omega0=-0.40, amplitude=6.026, frequency=1.289); (theta0=-0.30, omega0=-0.13, amplitude=6.154, frequency=1.45); (theta0=-0.30, omega0=0.13, amplitude=6.282, frequency=1.611); (theta0=-0.30, omega0=0.40, amplitude=6.41, frequency=1.772); (theta0=-0.10, omega0=-0.40, amplitude=6.538, frequency=1.933); (theta0=-0.10, omega0=-0.13, amplitude=6.667, frequency=2.094); (theta0=-0.10, omega0=0.13, amplitude=6.795, frequency=2.256); (theta0=-0.10, omega0=0.40, amplitude=6.923, frequency=2.417); (theta0=0.10, omega0=-0.40, amplitude=7.051, frequency=2.578); (theta0=0.10, omega0=-0.13, amplitude=7.179, frequency=2.739); (theta0=0.10, omega0=0.13, amplitude=7.308, frequency=2.9); (theta0=0.10, omega0=0.40, amplitude=7.436, frequency=3.061); (theta0=0.30, omega0=-0.40, amplitude=7.564, frequency=3.222); (theta0=0.30, omega0=-0.13, amplitude=7.692, frequency=3.383); (theta0=0.30, omega0=0.13, amplitude=7.821, frequency=3.544); (theta0=0.30, omega0=0.40, amplitude=7.949, frequency=3.705); (theta0=0.50, omega0=-0.40, amplitude=8.077, frequency=3.867); (theta0=0.50, omega0=-0.13, amplitude=8.205, frequency=4.028); (theta0=0.50, omega0=0.13, amplitude=8.333, frequency=4.189); (theta0=0.50, omega0=0.40, amplitude=8.462, frequency=4.35); (theta0=0.70, omega0=-0.40, amplitude=8.59, frequency=4.511); (theta0=0.70, omega0=-0.13, amplitude=8.718, frequency=4.672); (theta0=0.70, omega0=0.13, amplitude=8.846, frequency=4.833); (theta0=0.70, omega0=0.40, amplitude=8.974, frequency=4.994).
- Validation cases (theta0 rad, omega0 rad/s, torque parameters): (theta0=-0.63, omega0=0.20, amplitude=9.103, frequency=5.155); (theta0=-0.21, omega0=-0.20, amplitude=9.231, frequency=5.317); (theta0=0.21, omega0=0.10, amplitude=9.359, frequency=5.478); (theta0=0.63, omega0=-0.10, amplitude=9.487, frequency=5.639).
- Test cases (theta0 rad, omega0 rad/s, torque parameters): (theta0=-0.50, omega0=0.13, amplitude=9.615, frequency=5.8); (theta0=-0.15, omega0=-0.28, amplitude=9.744, frequency=5.961); (theta0=0.25, omega0=0.31, amplitude=9.872, frequency=6.122); (theta0=0.55, omega0=-0.08, amplitude=10, frequency=6.283).
- Model inputs: current theta, current omega, torque at the current step, midpoint torque, and next-step torque; targets: residual angle change and residual angular-velocity change.
- Training configuration: batch_size=None, batches_per_epoch=200, batch_size_range=160-160, max_epochs=100, max_optimizer_steps=20000, learning_rate=0.001, scheduler=ReduceLROnPlateau(factor=0.5, patience=10, min_lr=1e-06).
- Actual training: 20000 optimizer updates, 3200000 training samples processed.

## Changes From Residual Experiment 0

- The training, validation, and test initial conditions use the exact same trajectory split as Residual Experiment 0.
- Linear torque ramps were replaced with sinusoidal torques, tau(t) = amplitude * sin(frequency * t).
- Torque amplitudes range from 5 to 10 N m and frequencies range from 0 to 2 pi rad/s across the 40 trajectories.
- The optimizer budget, model architecture, physical parameters, time step, and training seed are unchanged from Residual Experiment 0.

## Training Procedure

- Training uses shuffled, non-dropping mini-batches; validation is evaluated in its original order after each epoch.
- The optimizer-step target was 20000; this run completed 20000 updates over 100 complete epochs, processing 3200000 training samples.
- ReduceLROnPlateau monitors validation MSE once per epoch and applies the configured factor, patience, and minimum learning rate.

## Files

- `simulation_dataset.npz`: all generated trajectories and simulation metadata.
- `residual_checkpoint.pt`: model checkpoint selected by lowest validation MSE.
- `residual_training_log.csv`: per-epoch update count, samples seen, learning rate, training loss, and validation loss.
- `residual_learning_curves.png`: training and validation MSE versus epoch.
- `residual_training_comparison.png`: prediction versus simulator on a validation trajectory.
- `residual_test_comparison.png`: prediction versus simulator on the preselected first test trajectory.
- `residual_test_error_data.csv`: per-test-trajectory state errors and aggregate mean/standard deviation.

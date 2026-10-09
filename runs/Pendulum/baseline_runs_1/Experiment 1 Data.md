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
- Model inputs: time, initial angle, initial angular velocity, and applied torque; targets: angle and angular velocity.

## Changes From Experiment 0

- Experiment 0 paired 32 angle values with 32 velocity values by matching list index, so its training conditions followed a single diagonal through the angle/velocity space.
- Experiment 1 uses the Cartesian product of 8 angle values and 4 velocity values, giving 32 combinations across the two-dimensional initial-condition space.
- The linear torque family and the balanced slope values (-0.12, 0.0, and 0.12 N m/s) are unchanged; Experiment 1 assigns them in a reproducible seeded shuffle instead of the prior cyclic order.
- The validation and test conditions, physical parameters, duration, time step, network, epoch count, learning rate, and training seed are unchanged.
- The purpose of this change is to test whether broader combinations of initial conditions help the model reproduce trajectories it did not train on.

## Files

- `simulation_dataset.npz`: all generated trajectories and simulation metadata.
- `baseline_checkpoint.pt`: model checkpoint selected by lowest validation MSE.
- `baseline_learning_curves.png`: training and validation MSE versus epoch.
- `baseline_training_comparison.png`: prediction versus simulator on a validation trajectory.
- `baseline_test_comparison.png`: prediction versus simulator on the preselected first test trajectory.
- `baseline_test_error_data.csv`: per-test-trajectory state errors and aggregate mean/standard deviation.

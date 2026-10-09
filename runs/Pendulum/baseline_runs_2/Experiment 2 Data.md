# Experiment 2 Data

## Dataset

- Trajectories: 80 training, 10 validation, 10 test.
- Split unit: complete trajectories.
- Simulation duration: 10 seconds.
- Time step: 0.01 seconds; 1001 samples per trajectory, including the initial state.
- Physical parameters: mass=1.0 kg, length=1.0 m, gravity=9.81 m/s^2, damping=0.1.
- Training initial angles (rad): -1.4000, -1.0889, -0.7778, -0.4667, -0.1556, 0.1556, 0.4667, 0.7778, 1.0889, 1.4000.
- Training initial angular velocities (rad/s): -1.0000, -0.7143, -0.4286, -0.1429, 0.1429, 0.4286, 0.7143, 1.0000.
- Training initial conditions use every angle/velocity pair in the Cartesian product of those values.
- Torque family: linear ramp, tau(t) = slope * t.
- Training torque slopes (N m/s): -0.12, 0.00, 0.12.
- Validation cases (theta0 rad, omega0 rad/s, slope N m/s): (theta0=-0.63, omega0=0.20, slope=0.07); (theta0=-0.21, omega0=-0.20, slope=-0.07); (theta0=0.21, omega0=0.10, slope=0.11); (theta0=0.63, omega0=-0.10, slope=-0.11); (theta0=-1.25, omega0=0.75, slope=0.06); (theta0=-0.95, omega0=-0.65, slope=-0.10); (theta0=-0.65, omega0=0.85, slope=0.02); (theta0=-0.25, omega0=-0.85, slope=0.09); (theta0=0.35, omega0=0.55, slope=-0.04); (theta0=1.25, omega0=-0.55, slope=0.12).
- Test cases (theta0 rad, omega0 rad/s, slope N m/s): (theta0=-0.50, omega0=0.13, slope=0.04); (theta0=-0.15, omega0=-0.28, slope=-0.08); (theta0=0.25, omega0=0.31, slope=0.10); (theta0=0.55, omega0=-0.08, slope=-0.03); (theta0=-1.25, omega0=0.75, slope=0.10); (theta0=-0.95, omega0=-0.65, slope=-0.10); (theta0=-0.35, omega0=0.85, slope=0.08); (theta0=0.35, omega0=-0.85, slope=-0.09); (theta0=0.95, omega0=0.55, slope=0.06); (theta0=1.25, omega0=-0.55, slope=-0.11).
- Model inputs: time, initial angle, initial angular velocity, and applied torque; targets: angle and angular velocity.

## Changes From Experiment 1

- Training trajectories increased from 32 to 80; validation and test trajectories increased from 4 each to 10 each.
- Training initial angles widened from -0.7 to 0.7 rad to -1.4 to 1.4 rad, and initial angular velocities widened from -0.4 to 0.4 rad/s to -1.0 to 1.0 rad/s.
- Training initial conditions use a 10-by-8 Cartesian grid; the linear torque family and balanced slope values are retained.
- The first four test trajectories are unchanged from Experiment 1; six additional validation and six additional test conditions cover the wider range.
- Physical parameters, duration, time step, model, epoch count, learning rate, and seed are unchanged.

## Files

- `simulation_dataset.npz`: all generated trajectories and simulation metadata.
- `baseline_checkpoint.pt`: model checkpoint selected by lowest validation MSE.
- `baseline_learning_curves.png`: training and validation MSE versus epoch.
- `baseline_training_comparison.png`: prediction versus simulator on a validation trajectory.
- `baseline_test_comparison.png`: prediction versus simulator on the preselected first test trajectory.
- `baseline_test_error_data.csv`: per-test-trajectory state errors and aggregate mean/standard deviation.

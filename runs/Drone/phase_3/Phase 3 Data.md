# Phase 3 Data: Basic Rigid-Body Physics Predictor

## Results

The independent predictor is implemented and evaluated against the existing phase-2 MuJoCo flights. No NN was trained, no parameters were fitted, and no artificial model mismatch was introduced.

- Mass: 0.027 kg; principal inertias: (2.3951e-05, 2.3951e-05, 3.2347e-05) kg m^2.
- World gravity: (0.0, 0.0, -9.81) m/s^2.
- Prediction interval: 0.01 s; internal RK4 interval: 0.002 s.
- One-step evaluation: 110,000 transitions over all main and benchmark flights.
- Recursive evaluation: 20 test/benchmark flights, 10 s each.
- Analytic checks: free fall, hover balance, tilted thrust, and single-axis rotational response passed.

### Test trajectories

- **One-step (true current state)**, 10 flights: mean position MAE **4.19603804e-08 m**, std 2.8284042e-08 m; mean orientation MAE **1.24415934e-09 rad (7.12850792e-08 deg)**, std 1.0248782e-09 rad.
  Mean final position error: 1.76875091e-10 m; mean maximum position error: 1.60043329e-07 m.
- **Recursive (predicted current state, no refresh)**, 10 flights: mean position MAE **0.0143260365 m**, std 0.00579547429 m; mean orientation MAE **0.000171113069 rad (0.00980405669 deg)**, std 6.29730519e-05 rad.
  Mean final position error: 0.0512667036 m; mean maximum position error: 0.0512667036 m.

### Benchmark trajectories

- **One-step (true current state)**, 10 flights: mean position MAE **4.29712985e-08 m**, std 1.90215184e-08 m; mean orientation MAE **1.56173415e-09 rad (8.94807754e-08 deg)**, std 4.29757267e-10 rad.
  Mean final position error: 1.67331365e-09 m; mean maximum position error: 2.01678114e-07 m.
- **Recursive (predicted current state, no refresh)**, 10 flights: mean position MAE **0.0121544784 m**, std 0.00491539226 m; mean orientation MAE **0.000127819033 rad (0.00732349112 deg)**, std 4.9017943e-05 rad.
  Mean final position error: 0.0440691331 m; mean maximum position error: 0.0440691331 m.

## Fluid-isolation comparison

An isolated MuJoCo instance had density and viscosity set to zero for 800 one-step samples (10 evenly spaced transitions per training flight). Each sample begins at the same true current state and uses the same applied controls as the normal reference. This isolates frame, sign, inertia, and integration discrepancies without changing the saved dataset.

- **fluid_off**: mean/max position discrepancy 6.01114398e-16 / 1.20587036e-14 m; mean/max orientation discrepancy 5.18012878e-12 / 8.93243651e-11 rad; mean linear/angular velocity discrepancy 1.86200503e-13 m/s / 8.64065526e-19 rad/s.
- **normal_reference**: mean/max position discrepancy 3.78285047e-08 / 5.89513477e-07 m; mean/max orientation discrepancy 1.14835017e-09 / 1.45846493e-08 rad; mean linear/angular velocity discrepancy 7.56519495e-06 m/s / 2.29496003e-07 rad/s.

The fluid-free difference is a numerical diagnostic, not a target fidelity threshold. Classical RK4 integrates the quaternion differential equation here, whereas MuJoCo's RK4 uses tangent-space quaternion position integration. Small finite-step differences are expected, especially for changing rotation axes. The normal residual also includes the intentionally omitted fluid forces.

## Governing equations and frames

Let p and v be world-frame position and velocity, q the scalar-first body-to-world quaternion, and omega the body-frame angular velocity. The body origin is its centre of mass and body axes are principal inertia axes in this pinned model. T is applied total thrust, tau applied body moments, and I the diagonal principal inertia matrix.

$$\dot p=v,\qquad \dot v=g_{world}+\frac{T}{m}R(q)e_z$$

$$\dot\omega=I^{-1}\left(\tau-\omega\times(I\omega)\right)$$

$$\dot q=\tfrac12 q\otimes[0,\omega]$$

`RigidBodyPhysics._derivative` implements these equations directly in NumPy. The cross product is the gyroscopic coupling from Euler's rotational equation. Thrust acts along body +z and is rotated into world coordinates; moments use the body-frame right-hand rule. World gravity is constant. Body-frame gravity would be R(q).T @ g_world; it changes with attitude but is not an additional force.

`step_array` holds the applied wrench constant while taking 5 classical RK4 substeps of 0.002 s per 0.01 s prediction. Each substep evaluates four derivative stages and then normalizes the quaternion. `step` provides the same transition using DroneState and DroneControl. No MuJoCo dynamics function is called by the predictor. Its properties are copied from recorded model metadata. Actuator scaling and clipping happen upstream; feeding raw actuator commands here is incorrect.

The normal simulator retains density 1.225 kg/m^3 and viscosity 1.8e-5 Pa s in still air. The stock model uses MuJoCo's inertia-based fluid resistance. The basic predictor omits that resistance, contact, wind corrections, and rotor dynamics. It does not stop when a predicted flight crosses the floor: these are contact-free flight equations, not a contact simulator.

References: [MuJoCo fluid forces](https://mujoco.readthedocs.io/en/stable/computation/fluid.html), [pinned MuJoCo 3.16.0 RK4 implementation](https://github.com/google-deepmind/mujoco/blob/3.16.0/src/engine/engine_forward.c).

## One-step residual and recursive prediction

One-step evaluation starts each transition at the true simulator current state. Its error measures the correction a future residual NN must learn. Recursive prediction starts with truth only at t=0 and uses predicted states thereafter. Both replay the saved applied-control sequence; the flight controller is not rerun or given simulator truth during prediction. Small one-step errors can accumulate into substantial drift over 1,000 recursive transitions.

The saved diagnostic residual has 12 coordinates: position difference (3), linear velocity difference (3), orientation rotation vector (3), and angular velocity component difference (3), always simulator minus physics. Position and velocity differences use the current true state's body axes. The orientation vector is Log(R_physics_next.T @ R_sim_next), a right-composed correction in the predicted next body axes. Angular velocity differences subtract the state components in their respective body axes. Orientations are never subtracted as four quaternion components. q and -q represent the same orientation and give the same angle error.

These are finite-step errors, not acceleration targets or a complete state increment. No features, fitted standardizers, NN, optimizer, or truth-refresh mechanism have been added. Phase 4 can use these physics transitions and residual measurements when defining the learning pipeline.

## Metric definitions

Position MAE is the mean Euclidean position distance over predicted timestamps; position RMSE is the square root of the mean squared distance. Orientation uses the shortest absolute rotation angle in [0, pi], with MAE/RMSE in radians and degrees. Velocity MAE/RMSE similarly use vector norms in m/s and rad/s. Angular velocities are compared as body-frame state components. The shared exact initial state is excluded from means and maxima; final error is at the last timestamp.

Each split-level mean averages its per-trajectory metrics with equal flight weight. Standard deviations describe variation between trajectory metrics, using ddof=0. One-step and recursive results remain separate, as do ordinary tests and the waypoint benchmark. All per-trajectory velocity errors, RMSEs, and position/orientation errors are saved in CSV; all their equal-weight means and standard deviations are saved in JSON and comparison CSV.

## Artifacts and interfaces

- `one_step_metrics.csv` / `.json`: per-flight and per-split metrics for train, validation, test, benchmark.
- `rollout_metrics.csv` / `.json`: physics-only, no-refresh recursive test and benchmark metrics.
- `test_metrics.json`: one-step and recursive summaries for test and benchmark, including both mean MAEs.
- `comparison_metrics.csv`: split/mode summary rows, including mean MAEs and standard deviations.
- `sanity_checks.json`: analytic check results and numerical discrepancies.
- `fluid_comparison.json` / `predictions/fluid_comparison.npz`: matched fluid-on/fluid-off diagnostics.
- `predictions/one_step_main.npz` and `one_step_benchmark.npz`: predicted full states, 12D residuals, time, IDs, families, splits, residual convention metadata.
- `predictions/recursive_test.npz` and `recursive_benchmark.npz`: predicted full states, time, IDs, families, applied controls, no-refresh metadata.
- `plots/one_step_errors.png`: mean one-step errors by split with one-standard-deviation bands.
- `plots/recursive_errors.png`: mean recursive test/benchmark errors with variability bands.
- `plots/fluid_isolation.png`: matched one-step discrepancies on a logarithmic scale.
- `plots/<split>_<trajectory_id>_physics.png`: first flight of each family, preselected by saved index, not accuracy.
- `run_metadata.json`: source-data hashes, source-code hashes, code revision, model provenance, timing, properties, exact command.

The physics API is `RigidBodyPhysics(parameters, config).step(state, applied_control)`; `step_array` also accepts batches with matching leading shapes. `rollout(initial_states, applied_controls)` accepts no future truth. The evaluator loads phase-2 archives without modifying them. Prediction archives retain trajectory identity and link to source-data paths and hashes in run metadata.

## Reproduction

From the repository root, with the project environment installed:

```powershell
python scripts/drone/evaluate_physics.py
```

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_drone_physics.py -q
```

Default inputs are `runs/Drone/phase_2/dataset.npz` and `runs/Drone/phase_2/benchmark_dataset.npz`. Use `--dataset`, `--benchmark`, or `--output-root` to select alternatives. Repeated executions preserve existing results in `phase_3/repeat_N/`, each with `Phase 3 Data.md`.

## Implementation verification

The full project suite passed: **138 tests**, including the existing pendulum, unicycle, drone simulator, dataset, and playback tests. The suite completed in 51.42 seconds while the full physics evaluation was also running.

```powershell
.\.venv\Scripts\python.exe -m pytest -q --basetemp .pytest_cache/drone_phase3_regression --tb=short
```

The 25 new physics test cases cover analytic motion, moment signs, gyroscopic coupling, torque-free energy and angular-momentum magnitude, arbitrary-attitude fluid-free MuJoCo comparisons, applied-control saturation, deliberately omitted drag, batch/scalar agreement, quaternion-sign equivalence, rotation-vector composition, residual coordinates, one-step versus recursive state use, equal-flight metric means, invalid inputs, training-only fluid diagnostics, and preservation of prior phase output.

After generation, all five prediction archives were reloaded without pickle and checked for finite values; full-state predictions retained unit quaternions. Saved CSV means were independently recomputed and matched the JSON summaries. Recursive initialization and applied controls matched the source test flights exactly. Every recorded source-code and input-data SHA256 matched the files used. Aggregate plots and a representative per-flight plot were visually inspected for labels, units, and layout. Drone_Plan.md and README.md matched their hashes from the start of this implementation.

## Scope and changes

Added independent dynamics, quaternion-angle diagnostics, physics scoring, analytic verification, fluid-isolation checks, and prediction/error plots. Development scripts now write phase_N folders and Phase N Data.md reports; numbered runs/experiments remain reserved for the formed system. Past phase outputs were not rewritten. Drone_Plan.md and README.md were not edited.

This baseline covers one drone property configuration and the conservative still-air flight envelope from phase 2. Its drift is evidence for interpreting the upcoming learned correction, not an automatic model success/failure rule. Held-out waypoint data are reported separately and never used to fit model parameters. No commit was created.

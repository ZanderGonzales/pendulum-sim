# Learning Dynamical Systems: Pendulum, Unicycle, and Drone

This research project investigates how much simulator data a neural network needs to reproduce a dynamical system. The work began with a torque-driven pendulum, moved to a planar unicycle with explicit body-frame motion, and now includes a MuJoCo Crazyflie drone simulator and interactive flight playback.

The pendulum and unicycle have working training and evaluation pipelines. The drone currently provides reference flight data and playback; its physics-correction neural network is planned but has not been implemented. Across the project, the main experimental variables are the number of trajectories, the variety of motion represented, and the number of optimizer updates. Saved plots and physical-unit errors are used to interpret predictions alongside training loss.

- [Setup](#setup)
- [Repository organization](#repository-organization)
- [Pendulum](#pendulum)
- [Unicycle](#unicycle)
- [Drone](#drone)
- [Training and evaluation conventions](#training-and-evaluation-conventions)
- [Tests](#tests)

## Setup

Run commands from the repository root. The examples below use Windows PowerShell. The package declares Python 3.10 or later; the current development environment uses Python 3.12.

For a new environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
python scripts/smoke_test.py
```

For an existing environment, activate it before running the scripts:

```powershell
.\.venv\Scripts\Activate.ps1
```

The editable installation makes the packages under `src/` importable from the scripts and terminal. If activation is inconvenient, use `.\.venv\Scripts\python.exe` in place of `python`. Run `deactivate` to leave the environment.

NumPy handles numerical arrays, Matplotlib produces plots and animations, PyTorch implements the neural networks, MuJoCo supplies the drone simulation and viewer, and pytest runs the checks. MuJoCo is pinned to **3.16.0**; the other dependency ranges are recorded in `requirements.txt` and `pyproject.toml`.

## Repository organization

Physical simulators are separate from learned models. Runnable entry points live under `scripts/`; generated datasets and experiment artifacts are stored separately from source code.

```text
src/
  pendulum_sim/               Pendulum RK4 simulator, data, and visualization
  model_baseline/             Pendulum direct full-state prediction
  model_residual/             Pendulum one-step increment prediction
  unicycle_sim/               Exact planar motion, frames, and datasets
  model_unicycle_residual/    Body-frame increment learning and rollout evaluation
  drone_sim/                  MuJoCo flights, controller, assets, and playback
scripts/
  simulation/                Pendulum simulation/data demonstrations
  model_baseline/             Pendulum baseline runners and experiments
  model_residual/             Pendulum increment-model runners and experiments
  unicycle/                  Unicycle simulation and dataset generation
  model_unicycle_residual/    Unicycle training, evaluation, and experiments
  drone/                     Flight generation, playback, and asset maintenance
tests/                       Automated checks
data/                        Generated datasets
runs/
  Pendulum/                  Existing pendulum results and earlier demonstrations
  Unicycle/                  Existing unicycle results
  Drone/                     Numbered drone demonstrations and flight recordings
```

Some older scripts still default to writing directly under `runs/`, although existing results have been organized into the system folders above. The commands below distinguish those defaults from the archived results. Unicycle commands pass explicit paths to keep new work under `runs/Unicycle/`. Choose a new output directory when preserving previous results; those scripts can replace artifacts in an existing output folder.

The original design documents remain in [Pendulum_Plan.md](Pendulum_Plan.md), [Unicycle_Plan.md](Unicycle_Plan.md), and [Drone_Plan.md](Drone_Plan.md). This README describes the implemented system and how to use it.

## Pendulum

### Numerical model and simulation data

The first system is a damped pendulum driven by an external torque. Its state is angle `theta` and angular velocity `omega`; its input is torque `tau(t)`. The numerical simulator integrates:

$$
\dot{\theta}=\omega, \qquad
\dot{\omega}=-\frac{g}{L}\sin\theta-\frac{b}{mL^2}\omega+\frac{\tau(t)}{mL^2}.
$$

`src/pendulum_sim/simulator.py` uses fourth-order Runge-Kutta (RK4). Mass, length, gravity, damping, initial state, torque function, duration, and integration-step count are inputs. An integration-step count of 1,000 produces 1,001 state samples, including the initial state.

The main numbered experiments use mass 1 kg, length 1 m, gravity 9.81 m/s^2, damping 0.1, and a 10-second trajectory with a 0.01-second timestep. Early demonstrations use shorter or different horizons. Torque inputs include zero torque, linear ramps, and sinusoidal inputs.

Run a short numerical example or create a trajectory plot and GIF animation:

```powershell
python scripts/simulation/phase2_demo.py
python scripts/simulation/phase2_visualization_demo.py
```

The numerical example prints its initial and final states. The visualization example writes `runs/phase2_trajectory_plot.png` and `runs/phase2_pendulum_animation.gif`. These filenames retain their original development numbering.

The dataset generator combines complete trajectories on a shared time grid. A compressed `.npz` file contains named `time`, `theta`, `omega`, and `torque` arrays, plus JSON metadata describing initial conditions, physical parameters, and torque functions. Run the small dataset example with:

```powershell
python scripts/simulation/phase3_data_demo.py
```

It writes `data/phase3_example.npz` and prints the resulting PyTorch tensor shapes. The simulator produces reference motion; dataset conversion turns that motion into inputs and supervised targets for a chosen learning formulation.

### Direct full-state neural network

The baseline model predicts the pendulum state at a requested time:

```text
[time, initial angle, initial angular velocity, torque at that time]
    -> two hidden layers of 64 neurons, with Tanh activations
    -> [angle at that time, angular velocity at that time]
```

Each prediction is evaluated directly from the requested time and trajectory inputs. Earlier predictions are not fed back into this model. Inputs and targets are standardized using training data only; predictions are converted back to radians and radians/second for evaluation.

This input contract was developed around restricted torque families. An instantaneous torque value does not identify an arbitrary torque history, so the baseline should not be interpreted as a general predictor for any possible input signal.

The experiments expanded initial-condition coverage from a diagonal pairing of angle and velocity to a full 8-by-4 grid, giving 32 training trajectories and four each for validation and testing. A larger experiment used a 10-by-8 grid with 80 training trajectories, 10 validation trajectories, and 10 test trajectories over wider initial-state ranges. Later runs investigated mini-batch training, longer optimization, and exactly 200 balanced batches per epoch.

Run the standard baseline, or the larger 100-trajectory case:

```powershell
python scripts/model_baseline/run_baseline.py
python scripts/model_baseline/run_experiment_2.py
```

The standard runner defaults to batch size 256, an initial learning rate of 0.001, an optimizer-update target of 5,000, and an epoch ceiling of 100. `ReduceLROnPlateau` monitors validation MSE, reducing the learning rate when improvement stalls. The update target is checked at complete epoch boundaries, so the actual count may exceed the target; the epoch ceiling can also stop training before the target is reached.

For 200 balanced batches per epoch and a 20,000-update target:

```powershell
python scripts/model_baseline/run_baseline.py --batches-per-epoch 200 --max-epochs 100 --max-optimizer-steps 20000
```

Balanced batching shuffles all training samples into the requested number of near-equal batches, using every sample once per complete epoch. The fixed experiment scripts below reproduce the longer-optimization and balanced-batch configurations:

```powershell
python scripts/model_baseline/run_experiment_4.py
python scripts/model_baseline/run_experiment_5.py
```

### One-step increment neural network

The next pendulum model changes the learning target to the state increment:

$$
\Delta x_k=x_{k+1}-x_k, \qquad
\hat{x}_{k+1}=\hat{x}_k+\widehat{\Delta x}_k.
$$

The package is named `model_residual`, but its target is the **entire one-step change**, not the error of a separate physics predictor. It receives current angle, current angular velocity, and torque values at the start, midpoint, and end of the interval. The midpoint input is implemented as the average of the endpoint torques, which is exact for linear ramps and an approximation for sinusoidal inputs.

During training, current states come from the simulator. During recursive evaluation, each predicted next state becomes the input state for the following prediction. The known torque sequence remains available. The network uses two hidden layers of 64 neurons with `Tanh`, matching the baseline's hidden-layer structure.

The recorded experiments compared this formulation with the direct baseline on the same trajectories, shortened training from 20,000 to 2,000 updates, reduced the dataset from 40 to 30 trajectories, and replaced torque ramps with sinusoidal inputs. These comparisons examine data requirements and accumulated rollout error as well as training loss. The reduced-data experiment also changes the validation/test subsets, so its aggregate errors require that context when compared with earlier runs.

Run the matched 20,000-update increment-model experiment:

```powershell
python scripts/model_residual/run_residual_experiment_0.py
```

Run the smaller-data or sinusoidal-torque experiments:

```powershell
python scripts/model_residual/run_residual_experiment_2.py
python scripts/model_residual/run_residual_experiment_3.py
```

For configurable training, including the shorter 2,000-update configuration:

```powershell
python -m model_residual.residual_runner --batches-per-epoch 200 --max-epochs 10 --max-optimizer-steps 2000
```

The two pendulum formulations can be compared using the 200-batch, 20,000-update baseline command above and `run_residual_experiment_0.py`. These use the same 32/4/4 trajectory split. Check each saved report for the actual training configuration before comparing results.

### Results and saved artifacts

Existing numbered results are under `runs/Pendulum/baseline_runs_0/` through `baseline_runs_5/` and `runs/Pendulum/residual_runs_0/` through `residual_runs_3/`. Earlier exploratory outputs are also retained under `runs/Pendulum/` and its archive.

The current pendulum runners create their next numbered folder directly under `runs/`, named `baseline_runs_N` or `residual_runs_N`. Numbering is determined by folders present there, so rerunning a named experiment does not guarantee the same historical folder number.

Each numbered run contains:

- `simulation_dataset.npz`: reference trajectories and metadata.
- `baseline_checkpoint.pt` or `residual_checkpoint.pt`: the model selected by lowest validation loss, with normalization and training state.
- A training-log CSV recording epochs, actual optimizer updates, samples processed, learning rate, and losses.
- Learning curves, a validation comparison, and a preselected test comparison.
- A test-error CSV reporting angle and angular-velocity MAE/RMSE per trajectory and aggregate mean/standard deviation.
- `Experiment N Data.md`: the configuration, changes, and artifact descriptions.

For concrete examples, see the [baseline experiment report](<runs/Pendulum/baseline_runs_5/Experiment 5 Data.md>) and [short-training increment-model report](<runs/Pendulum/residual_runs_1/Experiment 1 Data.md>).

## Unicycle

### Exact motion and body-frame representation

The unicycle extends the experiment to a vehicle moving in a plane. Its state is `[x, y, theta]`, where `theta` is heading; the control is forward speed `v` and turn rate `omega`.

$$
\dot{x}=v\cos\theta, \qquad
\dot{y}=v\sin\theta, \qquad
\dot{\theta}=\omega.
$$

World coordinates are right-handed. Body +x is forward and +y is left, and positive heading/turn rate is counter-clockwise. The simulator keeps heading unwrapped internally. It uses the exact constant-control transition over each timestep, with numerically stable expressions near zero turn rate, rather than an Euler approximation to curved motion.

The NN predicts local motion:

```text
[v, omega, dt] -> [delta_x_body, delta_y_body, delta_theta]
```

The default MLP has two hidden layers of 64 neurons with `Tanh`. Current world position and heading are not NN inputs: for this ideal system, the same controls produce the same local motion regardless of global placement. During rollout, the predicted local displacement is rotated by the **current predicted heading** and added to the predicted position. The heading increment is added explicitly. The model learns motion increments, as the pendulum increment model does; the frame transform remains known geometry outside the NN.

Plot analytical reference paths with:

```powershell
python scripts/unicycle/plot_analytic_paths.py --output runs/Unicycle/analytic_paths.png
```

### Generate, train, and evaluate

The generator creates seeded sequences of piecewise-constant controls, holding each sampled control for a configurable number of steps. It deliberately injects boundary and zero-axis control cases and saves a coverage plot. Initial headings vary across the full circle by default. Entire trajectories receive training, validation, or test labels, with nominal fractions 75%, 12.5%, and 12.5%, rounded to integer trajectory counts.

Generate a new dataset:

```powershell
python scripts/unicycle/generate_dataset.py --output runs/Unicycle/example_dataset/dataset.npz --trajectories 100 --steps 100 --dt 0.05 --seed 2026
```

This creates five-second trajectories with 100 transitions and 101 states each. Default speed ranges from 0 to 2 distance units/second, turn rate from -1.5 to 1.5 rad/s, and control holds from 5 to 20 steps. The dataset stores full states, controls, body-frame targets, inertial increments, split labels, and JSON metadata. `control_coverage.png` is saved next to it.

Train a model using that dataset:

```powershell
python scripts/model_unicycle_residual/train_unicycle_residual.py --dataset runs/Unicycle/example_dataset/dataset.npz --output runs/Unicycle/example_training --max-updates 5000
```

The default is Adam with learning rate 0.001, batch size 256, and an epoch ceiling of 300. Unlike the pendulum runners, this trainer stops at the exact update limit when reached, even during an epoch. A smaller epoch ceiling can still end training earlier. Architecture is configurable with `--hidden-size` and `--hidden-layers`.

Evaluate held-out test trajectories recursively:

```powershell
python scripts/model_unicycle_residual/evaluate_unicycle_rollout.py --checkpoint runs/Unicycle/example_training/checkpoint_best.pt --dataset runs/Unicycle/example_dataset/dataset.npz --output runs/Unicycle/example_rollout
```

The training folder contains best/final checkpoints, frozen standardizers, training metrics, one-step test metrics, configuration metadata, and learning curves. The evaluation folder adds saved predictions, path-comparison plots, and per-trajectory/aggregate rollout metrics. These include x/y/heading MAE, Euclidean position MAE/RMSE, final and maximum position error, wrapped heading error, and path-length error. One-step errors and recursive errors are recorded separately.

The older script defaults refer to `runs/unicycle_u2`, `runs/unicycle_u3`, and `runs/unicycle_u4`. Pass `--dataset`, `--checkpoint`, and `--output` explicitly when using the organized result folders or a newly generated dataset, as above.

### Experiments already explored

The unicycle work tested analytical rollout correctness, narrow control coverage, transfer to unseen initial headings, training-trajectory count, motion variety, and optimizer updates. The suite includes nested training sets of 8, 24, and 48 trajectories. Its variety comparison deliberately contrasts 48 similar trajectories with 12 varied ones; count and coverage both change in that comparison. The default optimizer comparison uses 100, 300, and 900 updates on the same dataset.

Run the suite into a new output folder:

```powershell
python scripts/model_unicycle_residual/run_u5_experiments.py --output runs/Unicycle/example_suite --updates 300
```

`--updates` controls the common budget for the main learned comparisons; the optimizer study uses 100, that value, and three times that value. The suite saves condition-level outputs, experiment reports, aggregate CSV/JSON summaries, and comparison plots.

The later numbered experiments use 64 trajectories split 48/8/8, 60 transitions at 0.05 seconds, and exactly 100 balanced batches per epoch for 15 epochs: 1,500 optimizer updates. The first extends optimization on the broad-control dataset. The second broadens training controls to speeds up to 3 and turn rates up to +/-7 rad/s, shortens control holds, and includes a constructed figure-eight test path.

```powershell
python scripts/model_unicycle_residual/run_experiment_1.py --output runs/Unicycle/example_experiment_1
python scripts/model_unicycle_residual/run_experiment_2.py --output runs/Unicycle/example_experiment_2
```

Existing results are retained in `runs/Unicycle/unicycle_u2/` through `unicycle_u5/`, plus `unicycle_run_1/` and `unicycle_run_2/`. Read their `U*_Data.md` or `Experiment N Data.md` reports together with control coverage and rollout plots. Low one-step loss alone does not establish long-path accuracy.

## Drone

### MuJoCo Crazyflie reference model

The drone work moves from analytical reference equations to the official MuJoCo Menagerie Bitcraze Crazyflie 2 model. `src/drone_sim/` currently provides model loading, full-state initialization and extraction, stepping, a flight controller, recorded traces, plotting, and interactive playback.

MuJoCo is pinned to **3.16.0**. The model is vendored at Menagerie revision `71f066ad0be9cd271f7ed58c030243ef157af9f4`, including its original XML, 39 meshes, README, and MIT license. The [provenance manifest](src/drone_sim/assets/bitcraze_crazyflie_2/provenance.json) records SHA-256 hashes. Assets ship with the Python package, so normal simulation and playback do not download model files.

The 13-component state is:

```text
[x, y, z, qw, qx, qy, qz, vx, vy, vz, wx, wy, wz]
```

Positions and linear velocities use world coordinates, with +z upward. Orientation is a scalar-first unit quaternion `[qw, qx, qy, qz]` that rotates body vectors into world coordinates. Angular velocity uses body coordinates. Body +x is forward, +y is left, and +z points upward through the rotors.

The input is a physical wrench: total body +z thrust in newtons and three right-hand body moments in newton-metres. The stock model does not expose four individual rotor speeds. Its moment actuators have negative gear factors, so the wrapper explicitly converts physical moments to raw MuJoCo controls, applies limits, and records the actual resulting wrench. Limits are 0 to 0.35 N thrust and +/-0.00001 N m on each moment axis. Upstream describes these limits as provisional rather than calibrated motor specifications.

Mass is 0.027 kg, with diagonal body inertia `[2.3951e-5, 2.3951e-5, 3.2347e-5]` kg m^2. At gravity 9.81 m/s^2, level stationary hover requires 0.26487 N thrust. The stock density and viscosity remain enabled, with zero wind.

### Controlled flights and recorded data

Six reference families are implemented: hover, straight flight with stops, climb/descent, circle, figure-eight, and seeded three-dimensional waypoints. Quintic interpolation smooths straight/vertical/waypoint segments; circles and figure-eights use smooth phase progression and gentle heading changes.

The controller requests a world-frame force from position/velocity feedback and reference acceleration:

```text
F = mass * (reference_acceleration
            + Kp * position_error + Kd * velocity_error - gravity)
```

The desired body +z axis aligns with that force. An attitude/angular-rate controller then requests body moments, including rotational coupling. Default position/velocity gains are 1.2 and 2.0; attitude/angular-rate gains are 64 and 16, with a 12-degree requested-tilt limit. Actual inputs are clipped to the stock actuator limits.

Generate and plot all six flights:

```powershell
python scripts/drone/plot_simulated_paths.py
```

To also save a still image from MuJoCo:

```powershell
python scripts/drone/plot_simulated_paths.py --render
```

Each invocation creates the next unused `runs/Drone/drone_run_N/` folder. Defaults are 10 seconds per flight, 0.01 seconds between controls/recorded samples, and five RK4 internal steps of 0.002 seconds per interval. A completed flight contains 1,001 states and 1,000 controls. Use `--seed`, `--duration`, `--dt`, `--internal-dt`, or `--output-root` to change these settings; shorter durations make the same geometric paths more demanding.

Each run saves:

- `<family>_flight.npz`: full states, timestamps, requested/applied physical controls, raw actuator controls, contacts, reference positions/yaw, and JSON metadata.
- `plots/path_comparison_summary.png`: reference paths and actual simulated flights.
- `plots/<family>_state_comparison.png`: positions, velocities, tracking error, and applied moments.
- `simulation_metrics.csv`: per-flight validity and controller tracking errors.
- `failed_trajectories.json`: rejected flights and reasons.
- `run_metadata.json` and `Experiment N Data.md`: model versions, parameters, controller settings, initial conditions, seed, and artifact descriptions.

Collection detects contacts at every internal timestep. Initial contact, contact during flight, numerical instability, or leaving the collection envelope rejects the flight and stops collection. The envelope allows heights from 0.05 to 5 m, a horizontal radius of 10 m, speeds up to 10 m/s, and tilt up to 60 degrees. These are data-collection guards, not automatic model-accuracy thresholds.

All six initial recorded flights completed without contacts or failures. The figure-eight was the most demanding: it briefly saturated moments and had a maximum reference-tracking distance of approximately 8.17 cm. These errors measure how well the controller follows its requested path; there is no trained drone NN being scored yet. See the [first drone run report](<runs/Drone/drone_run_1/Experiment 1 Data.md>).

### Watch a saved flight

The interactive viewer is already included in MuJoCo. With the virtual environment active, open an existing recording:

```powershell
python scripts/drone/playback_flight.py runs/Drone/drone_run_1/circle_flight.npz
```

Replace the filename with another saved flight. Playback restores recorded positions, orientations, velocities, and timestamps directly; it does not rerun the controller or advance physics. A blue line shows the recorded path. The camera initially frames the whole path; drag to orbit/pan and scroll to zoom.

Click the viewer window and use:

- **Space:** pause/resume; resuming at the end restarts the flight.
- **R:** restart, preserving the current pause state.
- **A / D:** previous/next recorded frame, pausing playback.
- **- / +:** halve/double speed between 0.125x and 8x; unshifted `=` also increases speed.
- **L:** toggle looping.
- **Q:** quit; closing the window also exits.

Left/right arrows are alternative stepping controls, and up/down arrows change speed. Time, frame number, speed, pause state, and loop state appear in the lower-left corner. Playback pauses on the final frame unless looping is enabled. The controls have been tested interactively by the user.

Additional startup options:

```powershell
python scripts/drone/playback_flight.py runs/Drone/drone_run_1/figure_eight_flight.npz --paused
python scripts/drone/playback_flight.py runs/Drone/drone_run_1/circle_flight.npz --loop --speed 0.5 --follow
```

`--follow` starts with a tracking camera, and `--hide-path` removes the path line. The viewer requires a local desktop and working OpenGL. The `--render` generation option saves a still image; playback does not currently export video.

The function can also be called from Python:

```python
from drone_sim.playback import playback_flight

playback_flight("runs/Drone/drone_run_1/circle_flight.npz", paused=True)
```

`FlightTrack` holds validated time/state data, `PlaybackController` owns timing and controls, and viewer code renders the selected recorded frame. This separation prepares for a transparent second drone showing an NN prediction of the same actual flight. The `nn_prediction` argument is reserved, but currently raises `NotImplementedError`; the overlay has not been implemented.

### Current boundary and planned learning model

The drone has no training/validation/test dataset pipeline, independent no-drag physics predictor, trained residual NN, or truth-refresh rollout evaluator yet. The intended next learning formulation differs from the existing increment models: the NN will learn the difference between a basic rigid-body one-step prediction and MuJoCo's next state.

The design calls for recursive prediction with optional full-state truth refreshes, a default 10,000-update training budget, and controlled comparisons of trajectory quantity, variety, optimizer updates, and NN size. Those settings are documented in [Drone_Plan.md](Drone_Plan.md); they are not current training commands. Future prediction rollouts will replay recorded applied controls, with simulator truth supplied only for initialization or explicitly requested refreshes.

For model asset maintenance only, re-fetch the same pinned upstream files with:

```powershell
python scripts/drone/fetch_crazyflie_model.py
```

This command needs network access and regenerates the provenance manifest. It is unnecessary for normal simulation or playback.

## Training and evaluation conventions

The simulator is the reference source, and complete trajectories are kept in one split to avoid leaking neighboring time samples between training and evaluation. Normalization is fitted on training data only. Validation selects checkpoints; held-out test trajectories measure final performance.

An **epoch** is a pass through the selected training examples. An **optimizer update** is one mini-batch forward pass, loss calculation, backward pass, and parameter update. Dataset size and batch organization change the number of updates per epoch, so compare actual logged updates and samples processed when interpreting experiments. Check the applicable runner's stopping rule and epoch ceiling rather than assuming every model uses the same budget.

Training MSE is generally computed in standardized target coordinates. Physical errors are computed after undoing standardization. Angle and angular velocity errors have different units, and standardized losses from different target formulations are not directly comparable as physical accuracy.

For recursive models, a small one-step error can accumulate into substantial path drift. Inspect held-out trajectory plots, error growth, and physical-unit metrics together. Keep interpolation within trained conditions distinct from tests of wider ranges or unseen control patterns. The number of trajectories alone does not describe whether the dataset covers the relevant motion.

## Tests

Run all automated checks:

```powershell
python -m pytest
```

Run checks for a particular system:

```powershell
python -m pytest tests/test_simulator.py tests/test_data.py tests/test_model.py tests/test_training.py tests/test_baseline_runner.py tests/test_residual_model.py
python -m pytest tests/test_unicycle_simulator.py tests/test_unicycle_data.py tests/test_unicycle_residual.py tests/test_unicycle_rollout.py
python -m pytest tests/test_drone_simulator.py tests/test_drone_playback.py
```

The tests cover numerical/reference motion, data serialization, model inputs and targets, training behavior, frame transforms, rollout behavior, pinned drone assets, actuator signs, deterministic flights, contact rejection, and playback timing/state fidelity. Automated playback tests run without opening a viewer; use the playback command above for interactive inspection.

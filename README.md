# Learning Dynamical Systems: Pendulum, Unicycle, and Drone

This research project investigates how much simulator data a neural network needs to reproduce a dynamical system. The work began with a torque-driven pendulum, moved to a planar unicycle with explicit body-frame motion, and now combines a MuJoCo Crazyflie simulator, an independent drone physics predictor, a learned physics correction, and interactive comparison playback.

All three systems have working data, training, and evaluation pipelines. The drone additionally supports full-state truth refreshes and synchronized playback of simulator, physics-only, and physics+NN flights. Across the project, the main experimental variables are the number of trajectories, the variety of motion represented, and the number of optimizer updates. Saved plots and physical-unit errors are used to interpret predictions alongside training loss.

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
  drone_sim/                  MuJoCo flights, datasets, rigid-body physics, and playback
  model_drone_residual/       Drone physics corrections, training, evaluation, and experiments
scripts/
  simulation/                Pendulum simulation/data demonstrations
  model_baseline/             Pendulum baseline runners and experiments
  model_residual/             Pendulum increment-model runners and experiments
  unicycle/                  Unicycle simulation and dataset generation
  model_unicycle_residual/    Unicycle training, evaluation, and experiments
  drone/                     Flight/data generation, physics checks, playback, and assets
  model_drone_residual/       Drone training, rollout/refresh evaluation, and experiments
tests/                       Automated checks
data/                        Generated datasets
runs/
  Pendulum/                  Existing pendulum results and earlier demonstrations
  Unicycle/                  Existing unicycle results
  Drone/                     Datasets, trained models, named experiments, and flight recordings
```

Some older scripts still default to writing directly under `runs/`, although existing results have been organized into the system folders above. The commands below distinguish those defaults from the archived results. Unicycle commands pass explicit paths to keep new work under `runs/Unicycle/`. Choose a new output directory when preserving previous results; those scripts can replace artifacts in an existing output folder.

For drone commands and any test-flight playback, go directly to [Drone](#drone) or [Watch any saved test flight](#watch-any-saved-test-flight).

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

### Scope and prediction model

The drone subsystem generates controlled flights in MuJoCo, trains a neural correction to an independent rigid-body predictor, evaluates one-step and recursive predictions, and plays the saved reference and predicted motion together. It predicts motion given a **known applied-control sequence**. The controller creates reference data; it does not receive simulator truth while a prediction is rolling forward.

The reference is the MuJoCo Menagerie Bitcraze Crazyflie 2 model. MuJoCo is pinned to **3.16.0**, and the model is vendored at revision `71f066ad0be9cd271f7ed58c030243ef157af9f4`. Its XML, meshes, MIT license, and [provenance manifest](src/drone_sim/assets/bitcraze_crazyflie_2/provenance.json) are included in the package. No separate viewer or model download is needed after installing the project dependencies. Playback needs a local desktop with working OpenGL.

The state and applied control are:

```text
state   = [x, y, z, qw, qx, qy, qz, vx, vy, vz, wx, wy, wz]
control = [total_thrust, body_moment_x, body_moment_y, body_moment_z]
```

Position and linear velocity use world coordinates, with +z upward, in metres and metres/second. Orientation is a normalized scalar-first quaternion rotating body vectors into world coordinates. Angular velocity uses body coordinates and radians/second. Thrust is in newtons and body moments are in newton-metres. The wrapper handles the stock actuator signs and limits and saves the actual applied wrench after clipping. This model exposes total thrust and moments rather than individual rotor-speed commands.

The independent predictor uses the drone's mass, inertia, gravity, thrust, body moments, and quaternion dynamics. It deliberately omits aerodynamic corrections while MuJoCo retains its fluid forces. Both use a 0.01-second prediction interval and five 0.002-second RK4 substeps. The NN learns the remaining **one-step error**, rather than the entire state increment learned by the pendulum and unicycle increment models:

```text
physics_next    = rigid_body_step(current_state, applied_control, dt)
correction     = residual_NN(body_velocity, body_rates, body_gravity, control, dt)
predicted_next = compose_correction(physics_next, correction)
```

The default MLP has 14 inputs, two hidden layers of 64 neurons with `Tanh`, and 12 outputs. Corrections cover position, linear velocity, orientation, and angular velocity. Translational corrections use the current body frame; orientation uses a rotation vector composed with the predicted orientation, followed by quaternion normalization. Body-frame gravity is the world gravity vector expressed along the drone's current axes. Inputs and residual targets are standardized using training flights only.

### Generate reference flights and datasets

Supported flight families are hover, straight flight with stops, climb/descent, circles, figure-eights, and smooth three-dimensional waypoints. The controller tracks a reference using position/velocity and attitude/angular-rate feedback. Flights start airborne; failed or contact-containing attempts are logged and excluded from learning data.

Generate individual examples, optionally including a MuJoCo still image:

```powershell
python scripts/drone/plot_simulated_paths.py
python scripts/drone/plot_simulated_paths.py --render
```

Generate a reproducible learning dataset and separate held-out-family benchmark:

```powershell
python scripts/drone/generate_dataset.py --train-trajectories 80 --validation-trajectories 10 --test-trajectories 10 --benchmark-trajectories 10 --seed 2026
```

The defaults produce ten-second flights with 1,000 transitions each. Hover, straight, climb/descent, circle, and figure-eight flights are balanced within the main splits. Waypoints are excluded from training, validation, and ordinary testing and form a separate benchmark. Complete trajectories stay in one split. Seeds vary placement, initial state, scale, and motion parameters while preserving stable trajectory IDs.

The compressed NumPy archives contain full states, timestamps, applied/requested controls, actuator commands, trajectory IDs, family/split labels, controller references, and JSON metadata. The existing main archive is `runs/Drone/phase_2/dataset.npz`; its separate waypoint archive is `runs/Drone/phase_2/benchmark_dataset.npz`. The generator also saves coverage diagnostics, a trajectory manifest, failure records, and selected individual recordings under `flights/`.

### Train and evaluate

Train the standard residual network and evaluate its best validation checkpoint on the fixed test and benchmark flights:

```powershell
python scripts/model_drone_residual/train_drone_residual.py --dataset runs/Drone/phase_2/dataset.npz --benchmark runs/Drone/phase_2/benchmark_dataset.npz --updates 10000 --seed 0
```

Defaults are Adam, learning rate 0.001, and batch size 256. **Requested optimizer updates are minimums, rounded upward to a complete epoch.** On the full training set, a request for 10,000 updates produces 10,016 updates across 32 complete epochs. The final short batch is retained. Metadata records both requested and actual counts, epochs, samples processed, and runtime. Validation runs every 100 updates and at the final update; its lowest residual MSE selects `checkpoint_best.pt`, which can precede the final training update. `checkpoint_final.pt` preserves the final state.

Change architecture and budget explicitly when needed:

```powershell
python scripts/model_drone_residual/train_drone_residual.py --hidden-layers 2 --hidden-size 128 --updates 15000 --seed 1
```

Evaluate a saved checkpoint without retraining:

```powershell
python scripts/model_drone_residual/evaluate_drone_rollout.py --checkpoint runs/Drone/phase_5/checkpoint_best.pt
```

Run the independent physics diagnostics and physics-only comparison:

```powershell
python scripts/drone/evaluate_physics.py
```

Evaluation compares physics-only and physics+NN against MuJoCo in two distinct modes:

- **One step:** every prediction starts from the corresponding true current state.
- **Recursive:** each predicted next state becomes the next input, with truth used only for initialization and scoring unless refreshes are explicitly enabled.

Both predictors replay identical recorded applied controls. Position MAE is time-average Euclidean distance from MuJoCo; orientation MAE is time-average shortest rotation angle, saved in radians and degrees. Overall MAEs weight each trajectory equally. Outputs also include RMSE, trajectory variability, final/maximum position error, and linear/angular velocity errors. Flight comparisons use a large 3D path plot plus position and orientation-angle error over time; loss curves are separate.

### Optional truth refreshes

No refresh is enabled by default. At a selected prediction timestamp, a refresh saves the forecast, replaces position, orientation, and both velocities with the simulator state at that same time, then continues recursively. It changes state, not NN weights. Both predictors receive the same schedule.

Choose one periodic or explicit schedule, in prediction steps or grid-aligned seconds:

```powershell
python scripts/model_drone_residual/evaluate_drone_refresh.py --refresh-every 100
python scripts/model_drone_residual/evaluate_drone_refresh.py --refresh-steps 50 200 700
python scripts/model_drone_residual/evaluate_drone_refresh.py --refresh-every-seconds 1.0
python scripts/model_drone_residual/evaluate_drone_refresh.py --refresh-times 0.5 2.0 7.0
```

Compare the standard interval set using the same saved checkpoint:

```powershell
python scripts/model_drone_residual/evaluate_drone_refresh.py --sweep
```

This evaluates no refresh and intervals of 1, 5, 10, 25, 50, 100, 200, and 500 steps. The primary errors are measured **before replacement**, so resets cannot hide the forecast's error. Post-replacement states, event snapshots, drift segments, and refresh counts are retained separately. Off-grid times are rejected. Step zero is initialization; a final-step refresh is counted but cannot improve the forecast already made there.

### Watch any saved test flight

The comparison archives contain **every evaluated flight**, even when only representative flights have PNG plots or separate single-flight files. Start with the original baseline's full test archive:

```powershell
$predictionFile = "runs/Drone/phase_5/predictions/test_recursive.npz"
```

List the available trajectory IDs and their flight families:

```powershell
python -c "import numpy as np, sys; a=np.load(sys.argv[1], allow_pickle=False); print(*(f'{tid}: {family}' for tid, family in zip(a['trajectory_ids'], a['families'])), sep=chr(10))" "$predictionFile"
```

Select **any ID from that list**. For example, these commands open different test flights:

```powershell
python scripts/drone/playback_flight.py "$predictionFile" --trajectory-id test_000004 --compare both --paused
python scripts/drone/playback_flight.py "$predictionFile" --trajectory-id test_000009 --compare both --paused
```

The ordinary test IDs run from `test_000000` through `test_000009` in the saved default evaluations. Omitting `--trajectory-id` selects the first flight. The MuJoCo drone keeps its original appearance; **physics-only is translucent blue**, and **physics+NN is translucent orange**. Every visible drone shares the same playback clock.

Choose which predictions to display alongside the MuJoCo reference:

```powershell
python scripts/drone/playback_flight.py "$predictionFile" --trajectory-id test_000004 --compare physics
python scripts/drone/playback_flight.py "$predictionFile" --trajectory-id test_000004 --compare hybrid
python scripts/drone/playback_flight.py "$predictionFile" --trajectory-id test_000004 --compare reference
```

To watch an unseen waypoint flight, switch archives and use a benchmark ID:

```powershell
$predictionFile = "runs/Drone/phase_5/predictions/benchmark_recursive.npz"
python scripts/drone/playback_flight.py "$predictionFile" --trajectory-id benchmark_000009 --compare both --paused
```

To watch a particular experimental model, change the archive path. This example uses the wider network:

```powershell
$predictionFile = "runs/Drone/phase_7/Experiment D - Neural Network Size/layers_2_width_128/seed_0/predictions/test_recursive.npz"
python scripts/drone/playback_flight.py "$predictionFile" --trajectory-id test_000004 --compare both --paused
```

Discover the test archives for all saved conditions and seeds:

```powershell
Get-ChildItem "runs/Drone/phase_7" -Recurse -Filter test_recursive.npz | Select-Object -ExpandProperty FullName
```

The folder's `seed_N` chooses the trained model; `--trajectory-id` chooses the flight. Test IDs identify the same underlying reference flights across the controlled experiments. Paths containing spaces must stay quoted.

Watch a refresh-enabled prediction with the same viewer:

```powershell
$predictionFile = "runs/Drone/phase_7/Experiment E - Refresh Frequency/every_100_steps/seed_0/predictions/test_recursive.npz"
python scripts/drone/playback_flight.py "$predictionFile" --trajectory-id test_000004 --compare both --paused
```

Refresh playback shows **post-replacement** paths, including state resets; its primary error plots use the saved **pre-replacement** forecasts. For uninterrupted drift, select a no-refresh archive. `test_one_step.npz` is also playable, but represents separate one-step predictions from true current states rather than an autonomous recursive path.

Individual simulator-only recordings also work:

```powershell
python scripts/drone/playback_flight.py runs/Drone/phase_1/circle_flight.npz --paused
```

Click the viewer window and use:

- **Space:** play/pause.
- **R:** restart.
- **A / D** or **left/right arrows:** step backward/forward one saved frame and pause.
- **- / +** or **down/up arrows:** slow down/speed up.
- **L:** toggle looping.
- **1:** reference plus blue physics-only prediction.
- **2:** reference plus orange physics+NN prediction.
- **3:** reference plus both predictions.
- **0:** MuJoCo reference only.
- **Q:** quit.

Drag to orbit/pan and scroll to zoom. Startup flags include `--loop`, `--speed 0.5`, `--follow`, `--hide-path`, and `--prediction-opacity 0.35`. Opacity must be strictly between zero and one; the default is 0.55. Playback restores saved states and timestamps without rerunning physics or the controller. It does not currently export video.

The same viewer is callable from Python:

```python
from drone_sim.playback import playback_flight

playback_flight(
    "runs/Drone/phase_5/predictions/test_recursive.npz",
    trajectory_id="test_000004",
    comparison="both",
    paused=True,
)
```

### Controlled learning experiments

The completed suite varies trajectory quantity, family coverage, optimizer budget, hidden-layer width/depth, and refresh frequency. Each unique learning condition is trained with seeds 0, 1, and 2. Identical conditions share their saved checkpoints across comparisons. Validation and evaluation flights stay fixed. The suite completed 36 unique training runs and 27 fixed-checkpoint refresh evaluations.

Inspect the planned conditions without training, run the complete suite, or select experiments:

```powershell
python scripts/model_drone_residual/run_drone_experiments.py --describe
python scripts/model_drone_residual/run_drone_experiments.py
python scripts/model_drone_residual/run_drone_experiments.py --experiments C D --seeds 0 1 2
```

Resume an interrupted new run using the output directory printed by that invocation. For example, if the new run created `repeat_1`:

```powershell
python scripts/model_drone_residual/run_drone_experiments.py --resume "runs/Drone/phase_7/repeat_1"
```

Use the actual run directory and keep its inputs, computational sources, and protected documentation unchanged while resuming. The original completed results remain available for playback without resuming anything.

Results are documented in [the full experiment report](<runs/Drone/phase_7/Phase 7 Data.md>). The following digest focuses on **recursive mean position MAE on the ordinary test flights**. Orientation, one-step errors, waypoint results, seed variability, and every directed within-experiment percentage comparison remain available in that report and its linked CSV/JSON files.

#### Original baseline and comparison rules

The original baseline is the **physics+NN test recorded in phase 5**, using the full training dataset, the standard network, and seed zero. It completed exactly 10,000 updates under the earlier stopping rule and selected its checkpoint at update 9,900. It used no truth refreshes. See its [report](<runs/Drone/phase_5/Phase 5 Data.md>) and [saved rollout metrics](runs/Drone/phase_5/rollout_metrics.json).

- Original hybrid test position MAE: **0.442592 mm**.
- Original hybrid test orientation MAE: **0.000367852 degrees**.
- Physics-only test position MAE: **14.326 mm**.
- Physics-only test orientation MAE: **0.00980406 degrees**.

The new standard condition uses complete epochs and averages three training seeds. Its test position MAE is 0.419956 mm, versus 0.442592 mm for the original baseline. Comparisons with the original baseline are **descriptive** because seed averaging and the final training budget differ. Comparisons within each experiment keep the other settings fixed, subject to the disclosed epoch rounding. Percentage changes use `100 * (candidate_MAE / reference_MAE - 1)`: higher error is worse and lower error is better. These are changes in error, not percentage-accuracy scores.

For each condition below, "original baseline" means the original hybrid predictor, not physics-only. The within-set reference is named separately. Refresh results use forecasts before truth replacement, and their extra state observations must be considered when comparing them with no-refresh models.

#### Trajectory quantity

Nested training subsets retain balanced families. All request the standard update budget; actual updates are rounded to complete epochs.

Within-set reference: **80 broad trajectories**.

**10 broad trajectories**

- Mean test position MAE: **2.84564 mm**.
- Compared with the original baseline: **542.95% higher error**.
- Compared with the within-set reference: **577.605% higher error**.

**20 broad trajectories**

- Mean test position MAE: **1.04873 mm**.
- Compared with the original baseline: **136.953% higher error**.
- Compared with the within-set reference: **149.725% higher error**.

**40 broad trajectories**

- Mean test position MAE: **0.671497 mm**.
- Compared with the original baseline: **51.7193% higher error**.
- Compared with the within-set reference: **59.8971% higher error**.

**80 broad trajectories**

- Mean test position MAE: **0.419956 mm**.
- Compared with the original baseline: **5.11438% lower error**.
- Compared with 10 broad trajectories: **85.2422% lower error**.

[Detailed trajectory quantity results](<runs/Drone/phase_7/Experiment A - Trajectory Quantity/Experiment A - Trajectory Quantity Data.md>).

#### Trajectory variety

Both conditions contain equal numbers of equal-duration flights. Restricted training uses circles and figure-eights; broad training uses all five main families.

Within-set reference: **20 broad-family trajectories**.

**20 restricted-family trajectories**

- Mean test position MAE: **5.17228 mm**.
- Compared with the original baseline: **1068.63% higher error**.
- Compared with the within-set reference: **393.193% higher error**.

**20 broad trajectories**

- Mean test position MAE: **1.04873 mm**.
- Compared with the original baseline: **136.953% higher error**.
- Compared with 20 restricted-family trajectories: **79.7239% lower error**.

[Detailed trajectory variety results](<runs/Drone/phase_7/Experiment B - Trajectory Variety/Experiment B - Trajectory Variety Data.md>).

#### Optimizer updates

The same full dataset and standard architecture are used. The update counts in parentheses are the actual complete-epoch budgets.

Within-set reference: **the new standard update budget**.

**5,000 requested updates (5,008 actual)**

- Mean test position MAE: **0.582882 mm**.
- Compared with the original baseline: **31.6975% higher error**.
- Compared with the within-set reference: **38.796% higher error**.

**10,000 requested updates (10,016 actual)**

- Mean test position MAE: **0.419956 mm**.
- Compared with the original baseline: **5.11438% lower error**.
- Compared with the smaller requested update budget: **27.9518% lower error**.

**15,000 requested updates (15,024 actual)**

- Mean test position MAE: **0.350489 mm**.
- Compared with the original baseline: **20.8099% lower error**.
- Compared with the within-set reference: **16.5416% lower error**.

**20,000 requested updates (20,032 actual)**

- Mean test position MAE: **0.289555 mm**.
- Compared with the original baseline: **34.5773% lower error**.
- Compared with the within-set reference: **31.051% lower error**.

[Detailed optimizer updates results](<runs/Drone/phase_7/Experiment C - Optimizer Updates/Experiment C - Optimizer Updates Data.md>).

#### Neural-network size

Counts describe hidden layers only. Width is compared at fixed depth, and depth at fixed width.

Within-set reference: **the new standard network**.

**Two hidden layers of 32 neurons**

- Mean test position MAE: **0.722308 mm**.
- Compared with the original baseline: **63.1996% higher error**.
- Compared with the within-set reference: **71.9961% higher error**.

**Two hidden layers of 64 neurons**

- Mean test position MAE: **0.419956 mm**.
- Compared with the original baseline: **5.11438% lower error**.
- Compared with two hidden layers of 32 neurons: **41.8592% lower error**.

**Two hidden layers of 128 neurons**

- Mean test position MAE: **0.357211 mm**.
- Compared with the original baseline: **19.291% lower error**.
- Compared with the within-set reference: **14.9408% lower error**.

**One hidden layer of 64 neurons**

- Mean test position MAE: **0.706641 mm**.
- Compared with the original baseline: **59.6598% higher error**.
- Compared with the within-set reference: **68.2656% higher error**.

**Four hidden layers of 64 neurons**

- Mean test position MAE: **0.465169 mm**.
- Compared with the original baseline: **5.10128% higher error**.
- Compared with the within-set reference: **10.7663% higher error**.

[Detailed neural-network size results](<runs/Drone/phase_7/Experiment D - Neural Network Size/Experiment D - Neural Network Size Data.md>).

#### Refresh frequency

Each seed reuses its standard-network checkpoint without retraining. Intervals are prediction steps, with the control/prediction grid unchanged.

Within-set reference: **no refresh with the same new checkpoints**.

**No refresh**

- Mean test position MAE: **0.419956 mm**.
- Compared with the original baseline: **5.11438% lower error**.
- Compared with refresh every 500 steps: **604.177% higher error**.

**Every prediction step**

- Mean test position MAE: **9.04287e-07 mm**.
- Compared with the original baseline: **99.9998% lower error**.
- Compared with the within-set reference: **99.9998% lower error**.

**Every 5 prediction steps**

- Mean test position MAE: **9.81876e-06 mm**.
- Compared with the original baseline: **99.9978% lower error**.
- Compared with the within-set reference: **99.9977% lower error**.

**Every 10 prediction steps**

- Mean test position MAE: **3.44281e-05 mm**.
- Compared with the original baseline: **99.9922% lower error**.
- Compared with the within-set reference: **99.9918% lower error**.

**Every 25 prediction steps**

- Mean test position MAE: **0.000197249 mm**.
- Compared with the original baseline: **99.9554% lower error**.
- Compared with the within-set reference: **99.953% lower error**.

**Every 50 prediction steps**

- Mean test position MAE: **0.000732923 mm**.
- Compared with the original baseline: **99.8344% lower error**.
- Compared with the within-set reference: **99.8255% lower error**.

**Every 100 prediction steps**

- Mean test position MAE: **0.00277821 mm**.
- Compared with the original baseline: **99.3723% lower error**.
- Compared with the within-set reference: **99.3385% lower error**.

**Every 200 prediction steps**

- Mean test position MAE: **0.00963271 mm**.
- Compared with the original baseline: **97.8236% lower error**.
- Compared with the within-set reference: **97.7063% lower error**.

**Every 500 prediction steps**

- Mean test position MAE: **0.0596379 mm**.
- Compared with the original baseline: **86.5253% lower error**.
- Compared with the within-set reference: **85.799% lower error**.

[Detailed refresh frequency results](<runs/Drone/phase_7/Experiment E - Refresh Frequency/Experiment E - Refresh Frequency Data.md>).


#### Waypoint generalization and orientation

Improvement on familiar test families does not guarantee the same improvement on the unseen waypoint family. The original hybrid waypoint benchmark has mean position MAE 1.21452 mm and mean orientation MAE 0.000722628 degrees.

- The new standard condition has waypoint position MAE **1.28233 mm**, which is **5.58% higher** than the original baseline, despite lower ordinary-test position error.
- The larger update budget has waypoint position MAE **1.06645 mm**, **12.19% lower** than the original baseline; its waypoint orientation MAE is still **12.45% higher**.
- The wider network has waypoint position MAE **1.01920 mm**, **16.08% lower** than the original baseline; its waypoint orientation MAE is **21.34% higher**.
- The deeper network raises waypoint position MAE by **30.46%** relative to the new standard network, matching its weaker ordinary-test result.

The restricted-family model also has much larger errors than the equal-count broad-family model. Its standardized validation loss uses different target scales, so physical MAEs are the shared comparison measure. No automatic fidelity threshold or best configuration is imposed.

### Files, outputs, and scope limits

`src/drone_sim/` owns MuJoCo, flight generation, datasets, rigid-body physics, frames, plots, and playback. `src/model_drone_residual/` owns residual features/corrections, the MLP, standardizers, training, evaluation, refresh schedules, and experiments. Entry points are under `scripts/drone/` and `scripts/model_drone_residual/`.

Existing outputs retain historical development-folder names; they are artifact locations, not a required sequence of manual steps:

- **Reference data:** demonstration recordings under `runs/Drone/phase_1/`; learning datasets, manifests, and coverage diagnostics under `runs/Drone/phase_2/`.
- **Physics and residual diagnostics:** independent-physics comparisons under `runs/Drone/phase_3/` and residual/interface checks under `runs/Drone/phase_4/`.
- **Original trained baseline:** checkpoints, metrics, and predictions under `runs/Drone/phase_5/`.
- **Truth-refresh comparisons:** original-checkpoint results under `runs/Drone/phase_6/` and multi-seed results in the named refresh experiment under `runs/Drone/phase_7/`.
- **Controlled experiments:** `runs/Drone/phase_7/`, organized by experiment, condition, and training seed.

Drone entry points allocate their applicable `phase_N/` folder and then unused `repeat_N/` subfolders on subsequent invocations, preserving earlier results. Use `--output-root` to choose another output root. Generating a new dataset does not automatically change later scripts' input paths: pass its `--dataset` and `--benchmark` paths explicitly. New training outputs are also independent; point evaluation/playback at the checkpoint or predictions actually produced.

Training runs save `checkpoint_best.pt`, `checkpoint_final.pt`, `standardizers.json`, `training_metrics.csv`, `training_summary.json`, `run_metadata.json`, and `loss_curves.png`. Evaluation adds `test_metrics.json`, `one_step_metrics.*`, `rollout_metrics.*`, comparison CSVs, `plots/`, and `predictions/`. Combined prediction archives retain truth, physics-only, and hybrid states, controls, IDs, timestamps, and checkpoint metadata. Refresh archives additionally retain forecast/reset states and event schedules. Experiment reports identify the controlled factor in their filenames, such as `Experiment A - Trajectory Quantity Data.md`.

The initial scope uses fixed drone properties, still air, contact-free flight, exact full-state observations at refreshes, and recorded future controls. Individual rotor dynamics, unknown controls, noisy or partial measurements, wind variation, payload changes, and contact learning remain extensions.

For model-asset maintenance only:

```powershell
python scripts/drone/fetch_crazyflie_model.py
```

This re-fetches pinned assets and needs network access; normal simulation, learning, and playback use the included files.

## Training and evaluation conventions

The simulator is the reference source, and complete trajectories are kept in one split to avoid leaking neighboring time samples between training and evaluation. Normalization is fitted on training data only. Validation selects checkpoints; held-out test trajectories measure final performance.

An **epoch** is a pass through the selected training examples. An **optimizer update** is one mini-batch forward pass, loss calculation, backward pass, and parameter update. Dataset size and batch organization change the number of updates per epoch, so compare actual logged updates and samples processed when interpreting experiments. Check the applicable runner's stopping rule and epoch ceiling rather than assuming every model uses the same budget.

Training MSE is generally computed in standardized target coordinates. Physical errors are computed after undoing standardization. Angle and angular velocity errors have different units, and standardized losses from different target formulations are not directly comparable as physical accuracy.

For recursive models, a small one-step error can accumulate into substantial path drift. Inspect held-out trajectory plots, error growth, and physical-unit metrics together. Keep interpolation within trained conditions distinct from tests of wider ranges or unseen control patterns. The number of trajectories alone does not describe whether the dataset covers the relevant motion.

## Tests

For drone work, run **only the drone subsystem tests**:

```powershell
$droneTestFiles = @(Get-ChildItem tests/test_drone*.py | Select-Object -ExpandProperty FullName)
python -m pytest @droneTestFiles -q
```

For a focused playback or experiment check:

```powershell
python -m pytest tests/test_drone_playback.py -q
python -m pytest tests/test_drone_experiments.py -q
```

Drone checks cover simulator determinism, dataset round trips and splits, frames and actuator signs, residual reconstruction, training-only normalization, complete-epoch accounting, architecture variants, metrics and percentages, truth-refresh timing, and playback state fidelity. Automated playback checks do not open a viewer; use the playback commands for interactive inspection.

When working on the other systems, their checks can be run separately:

```powershell
python -m pytest tests/test_simulator.py tests/test_data.py tests/test_model.py tests/test_training.py tests/test_baseline_runner.py tests/test_residual_model.py
python -m pytest tests/test_unicycle_simulator.py tests/test_unicycle_data.py tests/test_unicycle_residual.py tests/test_unicycle_rollout.py
```

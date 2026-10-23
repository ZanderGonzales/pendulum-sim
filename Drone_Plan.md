# Drone Plan

## Project Overview

This document plans the next system in the existing pendulum and unicycle project: predicting drone motion using MuJoCo's Bitcraze Crazyflie 2 simulation as the reference source of truth.

The system will combine a basic rigid-body predictor with a neural network that learns its **one-step prediction error relative to MuJoCo**. Evaluation will default to recursive rollouts, with optional full-state truth refreshes at user-selected times.

Error curves and trajectory plots will support manual interpretation throughout the project. No automatic path-fidelity threshold will define model success.

The project will be developed incrementally in phases. **Each phase must be reviewed and explicitly approved by the user before it is committed to the GitHub repository.**

---

## Project Goals

1. Generate reproducible full-state drone trajectories using MuJoCo's Crazyflie simulation.
2. Implement an independent basic rigid-body physics predictor using the drone's properties.
3. Train a PyTorch neural network to correct the physics predictor's one-step error.
4. Evaluate both one-step predictions and recursive rollouts against held-out simulator trajectories.
5. Support optional full-state truth refreshes and visualize their effect on prediction error.
6. Investigate trajectory quantity, trajectory variety, optimizer updates, and neural-network size through controlled experiments.
7. Preserve the existing project's file architecture, naming conventions, reproducibility, and readable experiment reports.

---

## File Architecture and Naming

**File names, folder organization, and experiment artifacts must follow the existing pendulum and unicycle conventions.** Use drone-specific equivalents of existing names, preserving their responsibilities.

- Simulation: `src/drone_sim/`, following the existing `types.py`, `dynamics.py`, `frames.py`, and `dataset.py` organization.
- Learning: `src/model_drone_residual/`, following the existing `model.py`, `training.py`, and `evaluation.py` organization.
- Entry points: `scripts/drone/` and `scripts/model_drone_residual/`, including `generate_dataset.py`, `train_drone_residual.py`, and `evaluate_drone_rollout.py`.
- Tests: follow the existing naming pattern, including `test_drone_simulator.py`, `test_drone_data.py`, `test_drone_residual.py`, and `test_drone_rollout.py`.
- Outputs: numbered folders under `runs/Drone/`, such as `drone_run_1/`, matching the current `runs/Unicycle/unicycle_run_1/` convention.

Retain established artifact names:

- `checkpoint_best.pt` and `checkpoint_final.pt`
- `standardizers.json` and `run_metadata.json`
- `training_metrics.csv` and `test_metrics.json`
- `rollout_metrics.csv` and `rollout_metrics.json`
- `loss_curves.png`
- `plots/` and `predictions/`
- `Experiment N Data.md`

Reuse appropriate existing utilities without introducing a broad framework refactor. Add drone-specific modules where necessary while preserving the established separation between simulation, learning, scripts, tests, and generated outputs.

---

## Development Phases

### Phase 1: Crazyflie Simulation and Flight Generation

Establish MuJoCo's Bitcraze Crazyflie 2 model as the reference simulator.

Tasks:

- Pin the MuJoCo version and Menagerie model revision; record model provenance and license.
- Add the drone simulation package using the architecture above.
- Implement full-state initialization, stepping, state extraction, and reproducible simulation.
- Use the stock total-thrust and three body-moment inputs, documenting actuator scaling, signs, and limits. These are the inputs defined by the [Crazyflie model](https://github.com/google-deepmind/mujoco_menagerie/blob/main/bitcraze_crazyflie_2/cf2.xml).
- Add a simple flight controller for generating stable reference trajectories. Record the actual applied controls after limits.
- Support hover, straight flight with stops, climbs and descents, circles and turns, figure-eights, and smooth three-dimensional waypoint paths.
- Start airborne and focus on flight without contact. Log failed or contact-containing trajectories and exclude them from the initial learning dataset.

Defaults:

- Prediction and control interval: **0.01 seconds**.
- Trajectory duration: **10 seconds**, giving 1,000 transitions.
- Internal simulation step: **0.002 seconds**, with controls held constant across five substeps.
- Fixed drone properties and still air.

Before completing this phase, demonstrate hover and representative flight paths, explain coordinate conventions, and verify that controls produce the expected motion.

---

### Phase 2: Dataset Generation and Storage

Build a reproducible dataset pipeline that retains complete trajectories.

Tasks:

- Save time, position, orientation, linear velocity, angular velocity, applied controls, initial conditions, trajectory family, and generation settings.
- Represent orientation with normalized quaternions; document component order and frame conventions.
- Store numerical arrays in compressed NumPy archives with JSON metadata.
- Record simulator settings, physical parameters, controller configuration, seeds, and model revision.
- Preserve trajectory identity and control history so both one-step learning and recursive evaluation use the same source data.
- Provide state and control coverage plots, including trajectory-family counts.

Initial dataset:

- **80 training trajectories**
- **10 validation trajectories**
- **10 test trajectories**

Split by complete trajectory. Fit normalization using training data only. Keep validation and test trajectories fixed across controlled comparisons, and maintain a separate held-out trajectory-family benchmark for generalization experiments.

---

### Phase 3: Basic Rigid-Body Physics Predictor

Implement an independent six-degree-of-freedom predictor using:

- Drone mass and inertia.
- Gravity.
- Applied thrust and body moments.
- Translational and rotational rigid-body dynamics.
- Quaternion orientation integration.

Use the same applied controls and prediction interval as MuJoCo. Integrate with RK4 using the same internal substep duration.

Exclude drag and other aerodynamic corrections from this predictor. Retain the reference simulator's fluid effects; MuJoCo documents density- and viscosity-dependent resistance models in its [fluid-force documentation](https://mujoco.readthedocs.io/en/3.3.0/computation/fluid.html).

Tasks:

- Explain the governing equations and their connection to the code.
- Verify free fall, hover balance, thrust direction, and rotational response.
- Compare against MuJoCo with fluid effects disabled to isolate integration and frame errors.
- Measure the residual with normal reference settings before training.

A small residual is a valid finding. Do not introduce artificial parameter errors to make learning appear more useful.

---

### Phase 4: One-Step Physics-Residual Neural Network

Define the learning problem as:

$$
x^{physics}_{k+1}=F_{physics}(x_k,u_k,\Delta t)
$$

$$
r_k=x^{sim}_{k+1}\ominus x^{physics}_{k+1}
$$

$$
\hat{x}_{k+1}=F_{physics}(x_k,u_k,\Delta t)\oplus \hat r_k
$$

Here, orientation differences and corrections use rotation composition rather than quaternion subtraction.

Tasks:

- Train from true simulator current states and the corresponding next-step residual.
- Predict corrections to position, linear velocity, orientation, and angular velocity.
- Express translational corrections in the current body frame and orientation correction as a three-component rotation vector.
- Use body-frame velocity, angular velocity, body-frame gravity, applied controls, and timestep as NN inputs.
- Explain that body-frame gravity is the world gravity vector expressed along the drone's current axes.
- Apply frame transformations and orientation composition explicitly.
- Begin with a configurable MLP using **two hidden layers of 64 neurons each**, with `Tanh` activations.
- Standardize inputs and residual targets using training data only.

Document the distinction between learning a physics correction and learning the entire state increment, as in the unicycle model.

---

### Phase 5: Training and Recursive Evaluation

Train with Adam, an initial learning rate of `0.001`, and a default batch size of `256`.

Training requirements:

- Complete exactly **10,000 optimizer updates** by default, including a partial final epoch when necessary.
- Validate every 100 updates and at the final update.
- Save both the final checkpoint and the checkpoint with lowest validation residual MSE.
- Record actual updates, epochs, samples processed, losses, learning rate, seeds, normalization, optimizer state, and configuration.
- Use test data only for final evaluation.

Evaluate:

- Physics-only prediction.
- Physics plus learned residual.
- One-step prediction using true current states.
- Fully recursive prediction using predicted states.

Replay the recorded simulator controls for both predictors. The flight controller generates reference data; it does not receive simulator truth during prediction.

Make plots available from this phase onward:

- Training and validation loss versus optimizer updates.
- Three-dimensional paths and planar projections.
- Position and velocity components versus time.
- Position, orientation, and velocity error versus time.

Return and save these metrics:

- Per-trajectory position MAE and RMSE.
- Per-trajectory orientation MAE and RMSE.
- **Mean position MAE across all test trajectories.**
- **Mean orientation MAE across all test trajectories.**
- Standard deviation of the per-trajectory metrics.
- Final and maximum position error.
- Linear and angular velocity MAE and RMSE.

Define position MAE as the time-average Euclidean distance between predicted and true positions. Define orientation MAE as the time-average absolute rotation angle between predicted and true orientations, reported in radians and degrees.

Compute each overall mean by averaging the corresponding per-trajectory MAEs with equal weight for every test trajectory. Include these means in saved JSON summaries, experiment comparison CSVs, and the readable experiment report. Keep results separate by predictor and evaluation mode.

---

### Phase 6: Optional Truth Refreshes

Add truth refreshes as an evaluation option, with **no refreshes enabled by default**.

Support:

- A periodic interval measured in prediction steps.
- An explicit list of refresh steps.
- Equivalent time-based configuration restricted to the prediction grid.

At a selected step, replace the predicted position, orientation, and velocities with the simulator state at that same time, then resume recursive prediction. Refreshes do not update NN weights.

Tasks:

- Save the prediction immediately before each refresh and the corrected state separately.
- Mark refresh events on error and trajectory plots.
- Report pre-refresh error and error growth between refreshes so state replacement does not hide drift.
- Apply identical schedules to physics-only and hybrid predictors.
- Make refresh settings reproducible in saved metadata.

Initial comparison intervals: no refresh, then every **1, 5, 10, 25, 50, 100, 200, and 500 steps**.

Plot error versus refresh interval and refresh count, including mean test-trajectory position and orientation MAE. The user will interpret these results manually.

---

### Phase 7: Controlled Learning Experiments

Run comparisons that change one main factor at a time.

**Experiment A: Trajectory quantity**

Compare nested training subsets of **10, 20, 40, and 80 trajectories**, each trained for 10,000 optimizer updates.

**Experiment B: Trajectory variety**

Compare restricted and broad trajectory families at equal training counts and durations. Separately report held-out-family results.

**Experiment C: Optimizer updates**

Compare **5,000, 10,000, 15,000, and 20,000 optimizer updates**, using the same dataset and architecture.

**Experiment D: Neural-network size**

Use the standard **two hidden layers with 64 neurons each** as the reference.

Compare hidden-layer width while holding depth at two:

- 32 neurons per hidden layer.
- 128 neurons per hidden layer.

Compare hidden-layer depth while holding width at 64:  

- One hidden layer.
- Four hidden layers.

This produces four distinct architectures: **2×32, 2×128, 1×64, and 4×64**. These counts refer to hidden layers; input and output layers are additional.

Train every architecture for **10,000 optimizer updates**, using the same dataset, batch size, optimizer, learning rate, activation functions, normalization procedure, and evaluation trajectories. Record trainable parameter counts and training time alongside prediction errors.

**Experiment E: Refresh frequency**

Evaluate the same trained checkpoint under different refresh schedules without retraining.

For every experiment:

- Keep simulator settings and held-out trajectories fixed.
- Keep other training settings fixed except the variable being studied.
- Repeat training with seeds 0, 1, and 2 while preserving the dataset.
- Report each seed separately and summarize variability.
- Include mean position MAE and mean orientation MAE across all test trajectories.
- Show trajectory plots and error curves, including fully recursive results.
- Use the established artifact names and numbered drone run folders.
- Explain dataset size, coverage, architecture, update count, artifact locations, and changes from the preceding experiment in `Experiment N Data.md`.

---

## Interfaces and Verification

Keep simulation, basic physics, residual learning, and evaluation separate. Follow existing file architecture and naming conventions when adding drone-specific interfaces.

Document these contracts:

- Full flight state and coordinate conventions.
- Applied control values and actuator conversion.
- Physics one-step transition.
- Residual construction and correction composition.
- Recursive rollout and optional refresh schedule.
- Configurable hidden-layer count and neurons per hidden layer.
- Dataset, checkpoint, and metric contents.

Required checks include:

- Deterministic generation and dataset round trips.
- Correct axes, actuator signs, units, quaternion normalization, and quaternion-sign equivalence.
- Disjoint trajectory splits and training-only normalization.
- Residual reconstruction recovering the simulator's next state.
- Zero residual reproducing physics-only prediction.
- Exactly 10,000 default optimizer updates.
- Correct construction of all five architecture variants.
- Correct per-trajectory MAEs and equal-weight means across all test trajectories.
- No-refresh rollouts reading truth only for initialization and scoring.
- Correct periodic and explicit refresh behavior, including every-step refresh.
- Existing pendulum and unicycle tests continuing to pass.

---

## Assumptions and Development Workflow

The initial system predicts motion given a known applied-control sequence. Individual rotor dynamics, unknown future controls, noisy measurements, wind variation, payload changes, and contact learning remain future extensions.

Each phase must leave the project runnable and include demonstrations, appropriate tests, an explanation of the physics and learning concepts, and a summary of files and assumptions. Implement phases sequentially. Do not implement future phases prematurely unless explicitly requested.

At the end of each phase:

1. Run appropriate tests or demonstrations and verify the implementation.
2. Summarize what was completed and which files were added or modified.
3. Explain the important physics, mathematics, PyTorch concepts, and implementation decisions.
4. Record assumptions, parameter choices, difficulties, and remaining uncertainties.
5. Explain how the phase connects to the next phase.
6. Give the user an opportunity to review the work.
7. Wait for explicit user approval before creating the phase commit.

**Do not commit automatically or commit to GitHub without explicit user approval.** Preserve reproducibility and prefer small, understandable changes throughout development.

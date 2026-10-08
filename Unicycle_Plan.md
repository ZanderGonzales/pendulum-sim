# Unicycle Model Implementation Plan

## 1. Purpose

Add a second dynamical system to the existing pendulum-simulation project: a planar unicycle model with position, heading, forward speed, and rotational velocity.

The unicycle experiment should preserve the project's existing conventions for:

- reproducible simulation and dataset generation;
- train/validation/test splits;
- mini-batch training and optimizer-update accounting;
- checkpointing and experiment metadata;
- recursive rollout evaluation;
- saved plots and numerical metrics.

The unicycle should be implemented as a separate physical-system package. It should reuse proven project conventions, but it should not be placed inside src/pendulum_sim/ or become dependent on pendulum-specific state names and equations.

The first goal is not to solve a difficult physical-learning problem. The ideal unicycle is intentionally simple and has a known analytical solution. It should therefore act as a clean architecture and representation test before applying the same ideas to more complicated black-box systems, including the long-term drone flight-path problem.

## 2. Architectural decision

### Decision

Keep the unicycle in the same repository, with a new sibling simulator package, a new model package, and its own scripts and run directories.

Do not:

- put unicycle dynamics in src/pendulum_sim/;
- copy the entire repository into a second project;
- immediately refactor every pendulum utility into a generic framework;
- change existing pendulum code or existing run artifacts unless a shared utility extraction is proven necessary.

### Recommended repository layout

~~~text
repository-root/
├── docs/
│   ├── Unicycle_Plan.md
│   └── ...existing project documentation...
├── src/
│   ├── pendulum_sim/
│   ├── model_baseline/
│   ├── model_residual/
│   ├── unicycle_sim/
│   └── model_unicycle_residual/
├── scripts/
│   ├── model_baseline/
│   ├── model_residual/
│   ├── unicycle/
│   └── model_unicycle_residual/
├── tests/
│   ├── test_pendulum_*.py
│   ├── test_unicycle_simulator.py
│   ├── test_unicycle_frames.py
│   ├── test_unicycle_data.py
│   └── test_unicycle_rollout.py
├── runs/
│   ├── baseline_runs_0/
│   ├── residual_runs_0/
│   ├── ...existing pendulum runs...
│   └── unicycle_residual_runs_0/
└── ...existing project files...
~~~

docs/Unicycle_Plan.md is the correct location for this document because it describes the whole experiment rather than one Python module. The simulator belongs in src/unicycle_sim/; the neural-network implementation belongs in src/model_unicycle_residual/; executable entry points belong in scripts/; generated outputs belong in runs/.

If the first unicycle implementation reveals genuinely identical code between pendulum and unicycle experiments, extract only that code into a small shared package, for example:

~~~text
src/experiment_core/
src/common_ml/
~~~

Potential shared utilities include standardization, checkpoint metadata, generic dataset splitting, optimizer-update logging, and generic metric serialization. Do this after the first working unicycle implementation so the abstraction is based on two real users rather than guesses.

## 3. System definition

### 3.1 State and input

Use the state:

~~~text
q = [x, y, theta]
~~~

where:

- x is inertial/world-frame x position;
- y is inertial/world-frame y position;
- theta is heading angle in radians.

Use the input:

~~~text
u = [v, omega]
~~~

where:

- v is signed forward speed in distance/second;
- omega is signed rotational velocity in radians/second.

The initial implementation may focus on nonnegative forward speed if that matches the project's intended operating regime, but the simulator and data generator should make reverse motion configurable. Reverse motion is a useful later test of whether the learned model has actually covered the control space.

### 3.2 Coordinate convention

Use a right-handed planar convention:

- body-frame +x points forward;
- body-frame +y points left;
- inertial-frame +x and +y use the same counter-clockwise orientation;
- positive omega rotates counter-clockwise;
- theta = 0 means the vehicle initially points along inertial +x.

Write this convention in module docstrings and test it. A sign error in the rotation matrix can otherwise produce visually plausible but physically incorrect paths.

### 3.3 Continuous-time dynamics

The ideal inertial-frame dynamics are:

~~~text
dx/dt     = v * cos(theta)
dy/dt     = v * sin(theta)
dtheta/dt = omega
~~~

or, in vector form:

~~~text
q_dot = [v*cos(theta), v*sin(theta), omega]
~~~

For a fixed control held over one timestep dt, the simulator should produce the next state. Internally, retain an unwrapped theta for clean integration and cumulative error calculations. Wrap angles only when a wrapped representation is explicitly requested for display or comparison.

## 4. Simulator design

### 4.1 Proposed modules

The exact filenames may be adjusted to match the existing repository style, but keep responsibilities separated.

~~~text
src/unicycle_sim/
├── __init__.py
├── types.py              # state, control, trajectory/data containers
├── dynamics.py           # continuous dynamics and exact one-step transition
├── frames.py             # body/inertial transforms and angle utilities
├── integration.py        # optional Euler/RK4/general integration helpers
├── controls.py           # random and piecewise-constant control sequences
├── dataset.py            # trajectory generation and train/val/test splitting
└── plotting.py           # true/predicted path plotting helpers, if appropriate
~~~

Do not force every function into a class. Small, explicit functions are preferable for this system because they make the coordinate conventions easy to test.

### 4.2 Ground-truth transition

For a constant control during one timestep, prefer the exact transition as the primary simulator. This avoids asking the neural network to learn numerical integration error.

Let alpha = omega * dt.

The body-frame displacement over the interval is:

~~~text
delta_x_body = (v / omega) * sin(alpha)
delta_y_body = (v / omega) * (1 - cos(alpha))
delta_theta  = omega * dt
~~~

when abs(omega) is safely away from zero. For omega near zero, use the continuous limit:

~~~text
delta_x_body = v * dt
delta_y_body = 0
delta_theta  = omega * dt
~~~

For numerical stability, use a small-omega threshold or a series expansion rather than allowing division by a value near zero.

Convert the body displacement to the inertial frame using the starting heading theta_k:

~~~text
delta_p_inertial = R(theta_k) @ delta_p_body
~~~

with:

~~~text
R(theta) = [[cos(theta), -sin(theta)],
            [sin(theta),  cos(theta)]]
~~~

Then update:

~~~text
x_next     = x_k + delta_x_inertial
y_next     = y_k + delta_y_inertial
theta_next = theta_k + delta_theta
~~~

The exact transition should be the reference used to generate training and test data. Implementing an independent numerical-integrator path, such as RK4, is useful as a test oracle but should not silently replace the exact fixed-control transition.

### 4.3 Why not use only Euler integration?

Euler integration would use approximately:

~~~text
delta_x_inertial = v * cos(theta_k) * dt
delta_y_inertial = v * sin(theta_k) * dt
delta_theta      = omega * dt
~~~

This is acceptable for a very small timestep, but it approximates a curved segment as a straight segment. If the neural network is trained on Euler-generated data and evaluated against exact motion, the model may appear to have a prediction error that is actually caused by inconsistent numerical integration. The exact constant-control solution gives a cleaner experiment.

## 5. Body-frame representation

### 5.1 Primary model representation

The primary model should learn:

~~~text
[v, omega] -> [delta_x_body, delta_y_body, delta_theta]
~~~

For a fixed dt, [v, omega] is sufficient for the ideal body-frame transition. If dt can vary, use:

~~~text
[v, omega, dt] -> [delta_x_body, delta_y_body, delta_theta]
~~~

The model should not need the current theta because the target is expressed in the body frame. This gives a useful invariance test: the same control applied from different inertial headings should produce the same local target.

### 5.2 Explicit rollout transform

During prediction, the neural-network output is local to the vehicle's current frame. The rollout must therefore do the following at every timestep:

~~~text
1. Read current predicted inertial state [x_k, y_k, theta_k].
2. Feed the control [v_k, omega_k] (and dt if variable) to the NN.
3. Receive [delta_x_body, delta_y_body, delta_theta].
4. Rotate [delta_x_body, delta_y_body] by theta_k.
5. Add the rotated displacement to [x_k, y_k].
6. Add delta_theta to theta_k.
7. Feed the resulting predicted state into the next rollout step.
~~~

Do not depend on the residual formulation to perform this transformation implicitly. The residual model describes a local increment; the rotation is known geometry and should remain explicit.

### 5.3 Why this matters for future drone work

A model that predicts local motion does not have to relearn how a vehicle's movement changes when the vehicle rotates. This is an inductive bias: it adds a small amount of known structure while leaving the unknown dynamics to the neural network.

For a drone, the same idea may eventually be extended to body-frame velocity, acceleration, or position increments. Three-dimensional orientation should not be represented by a naive angle subtraction near singularities; use an appropriate rotation representation later, such as quaternions or a continuous 6D rotation representation.

## 6. Data-generation plan

### 6.1 Generate control sequences, not isolated samples

Each trajectory should contain a complete sequence of states and controls. Do not generate one random control pair independently for every training row without preserving trajectory structure. The model must eventually be evaluated under recursive control sequences, and the dataset should represent that usage.

Support several sequence-generation modes:

1. Piecewise-constant controls: sample [v, omega], hold it for a configurable number of timesteps, then sample a new pair.
2. Smooth controls: interpolate between randomly selected control waypoints.
3. Structured trajectories: straight lines, stationary turns, circles, reversals, and stop/start sequences.
4. Random mixed trajectories: combine the above behaviors using a recorded seed.

Piecewise-constant controls are the best initial mode because they match the exact one-step transition and are easy to inspect.

### 6.2 Coverage requirements

The generated controls should deliberately cover:

- low, medium, and high speed;
- low, medium, and high absolute rotational velocity;
- positive and negative rotational velocity;
- zero speed;
- zero rotational velocity;
- combinations of speed and turning, not only one variable at a time;
- forward and, if enabled, reverse speed;
- changes in control over time.

Do not assume that uniform random sampling automatically gives good coverage. Record the sampled control ranges and inspect histograms or scatter plots of (v, omega).

The ranges should be configuration values, not constants buried in simulator functions. Every run must save:

- speed range and sampling distribution;
- rotational-velocity range and sampling distribution;
- timestep and trajectory duration;
- control-hold length or smoothing parameters;
- initial-state distribution;
- random seed;
- number of trajectories in each split.

### 6.3 Initial states

Start with a simple, controlled initial-state distribution so errors are easy to interpret:

- position near the origin, possibly exactly [0, 0] for the first sanity tests;
- heading sampled from a broad range, including values near -pi, 0, and +pi.

Once body-frame invariance has been tested, vary initial positions and headings. Splitting only by time points is not sufficient; the test split should contain complete trajectories or complete control sequences that the model did not see during training.

### 6.4 Dataset schema

Use a schema that preserves both one-step samples and complete trajectories. A one-step record should contain at least:

~~~text
state_current       [x, y, theta]
control_current     [v, omega]
state_next          [x, y, theta]
delta_body_target   [delta_x_body, delta_y_body, delta_theta]
delta_inertial_true [delta_x, delta_y, delta_theta]
trajectory_id
step_index
dt
~~~

The model may use only control_current, dt, and delta_body_target, but retaining the other values makes debugging and evaluation possible.

For saved NumPy data, use named arrays or a documented dictionary of arrays. For metadata, use JSON. Do not rely on the order of unnamed arrays without recording the schema.

## 7. Train/validation/test splitting

Split by trajectory or control sequence, not by randomly shuffling all individual timesteps before splitting.

Recommended initial split:

~~~text
training:   70–80% of trajectories
validation: 10–15% of trajectories
test:       10–15% of trajectories
~~~

The exact counts should be configurable and recorded. The important rule is that neighboring timesteps from one trajectory remain in the same split.

Use at least two test styles:

1. Interpolation test: test combinations fall inside the training control range but belong to unseen trajectories.
2. Coverage/generalization test: test includes deliberately held-out control patterns or portions of the allowed range.

Do not claim that the model generalizes to unseen flight-like behavior if the test set contains nearly identical control sequences to the training set.

## 8. Neural-network model

### 8.1 Initial model

Create a new package such as:

~~~text
src/model_unicycle_residual/
├── __init__.py
├── model.py
├── training.py
├── evaluation.py
├── preprocessing.py
└── config.py
~~~

The initial network should follow the successful residual-model pattern already used for the pendulum:

~~~text
current control (and dt if needed)
    -> standardized input
    -> small MLP
    -> standardized local increment
    -> inverse standardization
    -> explicit body-to-inertial transform during rollout
~~~

Keep the architecture configurable, but do not introduce unnecessary complexity in the first implementation. The objective is to study representation, data variety, and optimizer updates, not to tune a large architecture.

### 8.2 Target definition

For each timestep k, calculate the true body-frame target from the two inertial states:

~~~text
delta_p_inertial = [x_next - x_current, y_next - y_current]
delta_p_body     = R(theta_current)^T @ delta_p_inertial
delta_theta      = theta_next - theta_current
~~~

The training target is:

~~~text
target = [delta_x_body, delta_y_body, delta_theta]
~~~

Prefer the simulator's exact local transition as the reference, but also verify that the target reconstructed from inertial states matches it numerically.

### 8.3 Angle handling

For the first implementation, retain unwrapped heading internally and use the signed increment omega * dt. This avoids an artificial discontinuity at +pi/-pi.

If a wrapped target is ever needed, compute the shortest signed angle with:

~~~text
wrapped_delta = atan2(sin(delta_theta), cos(delta_theta))
~~~

Do not train the model on an arbitrary subtraction of wrapped angles without testing the wraparound case.

### 8.4 Standardization

Fit input and target standardizers using training data only. Apply the frozen training standardizers to validation and test data.

Save the standardizer parameters with each run. Record:

- feature order;
- target order;
- means and scales;
- handling of zero or near-zero scale values.

Do not compare standardized loss values across model formulations as if they were physical errors. Report physical-unit metrics after inverse transformation.

## 9. Training procedure

Use the same terminology and accounting already established in the pendulum project:

- one optimizer update means one forward pass, loss calculation, backward pass, and parameter update on one mini-batch;
- one epoch is a pass through the chosen training samples, possibly divided into multiple mini-batches;
- total optimizer updates are the more direct quantity to compare across experiments.

The training script should log at minimum:

- epoch number;
- optimizer update count;
- batch size;
- number of batches per epoch;
- training loss;
- validation loss;
- learning rate;
- wall-clock time if practical;
- best validation checkpoint;
- random seeds.

Use mini-batches and the existing optimizer conventions first. Preserve the ability to run controlled comparisons where only one variable changes.

For the first clean comparison, hold constant:

- network architecture;
- optimizer and initial learning rate;
- batch size;
- timestep;
- control ranges;
- random seed where practical;
- validation and test data.

Then vary one of:

- number of trajectories;
- control/trajectory variety;
- total optimizer updates;
- model representation.

## 10. Recursive rollout evaluation

A one-step prediction can look accurate while recursive use drifts substantially. Evaluation must therefore include both one-step and free-running rollout tests.

### 10.1 One-step evaluation

Use the true current state and true control for each row. Report physical-unit errors for:

- body-frame delta_x;
- body-frame delta_y;
- delta_theta;
- reconstructed inertial displacement.

### 10.2 Free-running evaluation

For each held-out test trajectory:

1. Initialize the predicted state with the true initial state.
2. At step k, use the prescribed test control.
3. Predict the body-frame local increment.
4. Rotate the local displacement using the current predicted heading.
5. Update the predicted state.
6. Use that predicted state at the next timestep.
7. Continue for the entire trajectory.

Do not replace the predicted state with the true state after every step in the main rollout metric. That would be teacher forcing and would hide accumulated errors.

Also calculate a teacher-forced diagnostic separately if useful. The difference between teacher-forced and free-running performance shows how much error amplification comes from recursive use.

### 10.3 Required rollout metrics

For every test trajectory, report:

~~~text
position MAE              mean Euclidean position error
position RMSE             root-mean-square Euclidean position error
final position error      error at the last timestep
maximum position error    worst error during the rollout
heading MAE               angle error in radians
heading RMSE              angle RMSE in radians
path-length error         predicted versus true traveled distance
~~~

When using wrapped angle differences, calculate the shortest angular error. Also retain an unwrapped heading metric when analyzing long trajectories.

## 11. Plotting requirements

The main visual result should be an inertial-frame 2D path plot.

Each plot should include:

- true path in one clearly labeled style;
- predicted path in another clearly labeled style;
- equal aspect ratio on both axes;
- starting point;
- optional heading arrows at selected points;
- trajectory identifier and run identifier;
- units;
- enough axis padding to make divergence visible.

Save at least:

~~~text
plots/path_comparison_<trajectory_id>.png
plots/path_comparison_summary.png
plots/position_error_vs_time_<trajectory_id>.png
plots/heading_error_vs_time_<trajectory_id>.png
plots/control_coverage.png
plots/training_curves.png
~~~

The 2D path must be plotted after converting predicted body-frame increments into inertial coordinates. Do not plot body-frame increments as though they were global x/y positions.

## 12. Run artifact structure

Use a dedicated run directory that does not overwrite pendulum results. For example:

~~~text
runs/unicycle_residual_runs_0/
├── config.json
├── dataset_metadata.json
├── feature_schema.json
├── standardizers.json
├── train_metrics.csv
├── validation_metrics.csv
├── test_metrics.json
├── checkpoint_best.pt
├── checkpoint_final.pt
├── predictions/
│   ├── trajectory_000.npz
│   └── ...
├── plots/
│   ├── path_comparison_000.png
│   ├── path_comparison_summary.png
│   └── ...
└── README.md
~~~

The run README should summarize:

- the command used;
- the Git commit or code version;
- the seed;
- the simulator convention;
- the number of trajectories and timesteps;
- the model input and target definitions;
- the number of optimizer updates;
- the best validation metrics;
- the final test metrics;
- any deviations from this plan.

## 13. Tests and acceptance criteria

### 13.1 Simulator tests

Implement tests for:

1. v=0, omega=0: state remains unchanged.
2. v>0, omega=0: motion is a straight line in the current heading.
3. v=0, omega!=0: position remains fixed while heading changes.
4. Positive omega: path curves in the documented positive direction.
5. Negative omega: path curves in the opposite direction.
6. Small omega: exact formula agrees with the straight-line limit.
7. Exact transition: agrees with an independent high-accuracy numerical integration check.
8. Repeated one-step transitions: agree with the trajectory simulator.

### 13.2 Frame-transform tests

Test that:

1. body-to-inertial followed by inertial-to-body returns the original vector;
2. a forward body displacement at theta=0 moves inertial +x;
3. a forward body displacement at theta=pi/2 moves inertial +y;
4. the same local displacement at different headings produces rotated inertial displacements;
5. extracting a body-frame target from two inertial states recovers the original local target;
6. angle errors near -pi and +pi use the intended convention.

### 13.3 Data tests

Test that:

- the same seed reproduces the same controls and trajectories;
- a different seed changes the generated data;
- all configured boundary cases appear when requested;
- train/validation/test trajectory IDs do not overlap;
- metadata exactly describes the generated arrays;
- targets have the expected ordering and units.

### 13.4 Model and rollout tests

Test that:

- a saved model can be loaded into a fresh process;
- the standardizer is fit only on training data;
- one-step predictions have the expected shape;
- rollout length matches the control sequence length;
- the rollout uses predicted state recursively;
- changing the initial inertial heading rotates the predicted path while preserving the local prediction for the same control;
- a perfect local-increment model reconstructs the exact inertial path within numerical tolerance.

### 13.5 Minimum completion criteria

The implementation is ready for the first experiment when:

- all simulator and transform tests pass;
- a deterministic dataset can be regenerated from metadata and a seed;
- a training command completes and saves a checkpoint;
- a test command loads that checkpoint without retraining;
- the output contains true and predicted inertial paths;
- metrics distinguish one-step error from recursive rollout error;
- existing pendulum experiments still run unchanged.

## 14. Suggested implementation phases

### Phase U1 — Simulator and coordinate conventions

Implement state/control types, exact one-step dynamics, trajectory simulation, angle utilities, and body/inertial transforms.

Deliverables:

- src/unicycle_sim/;
- simulator unit tests;
- a small script that plots a few analytically generated paths;
- documented sign and axis conventions.

### Phase U2 — Control generation and datasets

Implement seeded control-sequence generation, initial-state generation, trajectory splitting, target extraction, metadata, and dataset serialization.

Deliverables:

- configurable dataset-generation script;
- saved controls and trajectories;
- control-coverage plot;
- no train/test trajectory leakage.

### Phase U3 — Residual model and one-step training

Implement the body-frame residual MLP, training/validation loops, training-only standardization, checkpointing, and optimizer-update logging.

Deliverables:

- src/model_unicycle_residual/;
- training script;
- loss curves;
- checkpoint and run metadata;
- one-step physical-unit metrics.

### Phase U4 — Recursive rollout and inertial plots

Implement model loading, explicit body-to-inertial rollout, per-trajectory prediction files, and 2D path comparisons.

Deliverables:

- recursive rollout script;
- path plots;
- position and heading error plots;
- free-running metrics.

### Phase U5 — Controlled experiments

Run a small, reproducible experiment matrix to isolate the effects of model representation, data amount, data variety, and optimizer updates.

Deliverables:

- run directories with complete metadata;
- summary table of metrics;
- comparison plots;
- short conclusions that distinguish interpolation from generalization.

### Phase U6 — Shared infrastructure review

Only after U1–U5, compare the pendulum and unicycle implementations. Extract genuinely common utilities if doing so reduces duplication without hiding system-specific behavior.

Do not make this refactor a prerequisite for proving that the unicycle experiment works.

## 15. Initial experiment matrix

The first experiments should be small and controlled. The exact counts can follow the current pendulum conventions, but each run must record them explicitly.

### Experiment A — Simulator and transform sanity

Use a perfect analytical local-transition function in place of a trained neural network. Confirm that the body-to-inertial rollout reproduces the true path. This isolates plotting and frame-transform bugs from learning bugs.

### Experiment B — Narrow-control residual model

Train the body-frame residual model on a narrow, well-covered control range. Measure one-step and recursive rollout error.

### Experiment C — Initial-heading invariance

Train on several starting headings and test on unseen headings. The same local control behavior should be reusable across headings.

### Experiment D — Data quantity

Hold control ranges, architecture, seed policy, and optimizer updates constant while varying the number of training trajectories.

### Experiment E — Data variety

Compare many similar trajectories against fewer trajectories containing a broader range of speeds, turn rates, control changes, and initial headings.

### Experiment F — Optimizer updates

Hold the dataset and architecture constant while varying total optimizer updates. Use validation performance and rollout metrics to identify whether the model is undertrained or data-limited.

### Experiment G — Representation comparison

After the primary body-frame model is working, compare it with a deliberately less structured alternative, such as an inertial-frame residual model receiving theta as an input. Keep the comparison fair:

- same train/validation/test trajectories;
- same control inputs;
- same update budget;
- same evaluation metrics;
- separate target standardizers.

Do not compare standardized losses directly when the target definitions differ. Compare physical errors and rollout quality.

## 16. Expected failure modes and safeguards

### Wrong sign or axis convention

Symptom: paths turn in the opposite direction or move sideways. Safeguard: test known cases at theta=0 and theta=pi/2, and document the convention in every relevant module.

### Hidden frame conversion

Symptom: the network works only for headings seen during training. Safeguard: make R(theta) explicit and include heading-invariance tests.

### Division by small omega

Symptom: large numerical spikes near straight-line motion. Safeguard: use the analytic limit or a stable series expansion.

### Angle-wrap error

Symptom: a tiny heading error near pi appears to be almost 2*pi. Safeguard: use unwrapped internal headings or shortest-angle error functions consistently.

### Train/test leakage

Symptom: test error is unrealistically low. Safeguard: split by complete trajectories and save trajectory IDs.

### Teacher-forced evaluation mistaken for rollout quality

Symptom: one-step metrics look excellent while long paths drift. Safeguard: evaluate free-running recursive rollouts with predicted state feedback.

### Model learning simulator artifacts

Symptom: model does not match a higher-accuracy reference even though the equations are known. Safeguard: use the exact fixed-control transition as the main simulator and keep numerical integration checks separate.

### Future-control mismatch

The pendulum experiments can use future torque values if those values are available in the prescribed sequence. For the unicycle, only give the neural network controls that will actually be available at prediction time. If future controls are part of a known plan, document that assumption. For a future drone, do not train with future commands that the deployed system cannot access.

### Recursive error amplification

The model is trained on true current states but deployed on predicted current states. This distribution shift may become important as the system becomes more complex. Keep teacher-forced and free-running metrics separate. Later, consider training with perturbed current states, noise injection, or scheduled sampling if recursive drift becomes the dominant error.

## 17. Relationship to the eventual drone model

The unicycle experiment should answer architecture questions, not be treated as a realistic drone benchmark. Its useful lessons are:

- local residual prediction can be easier than predicting the entire next state;
- body-frame targets can reduce unnecessary dependence on global orientation;
- explicit known geometry can reduce the burden on the neural network;
- recursive rollout is a stricter test than one-step loss;
- data diversity must be evaluated by the control and state regimes it covers, not only by row count;
- optimizer updates help an undertrained model but cannot teach behavior absent from the dataset.

For the eventual drone system, the state will likely need to include more than position and heading, such as velocity, angular velocity, attitude, actuator state, and possibly environmental variables. The model will also need data covering disturbances, wind, payload changes, battery state, actuator saturation, and aggressive maneuvers. The unicycle should therefore keep system-specific physics in unicycle_sim/ while making the experiment workflow reusable.

## 18. Final implementation checklist

Before merging the unicycle work:

- [ ] docs/Unicycle_Plan.md is present and updated if implementation choices changed.
- [ ] src/unicycle_sim/ is independent of pendulum-specific equations.
- [ ] The coordinate convention is documented and tested.
- [ ] Exact one-step ground truth handles omega near zero.
- [ ] Body-to-inertial conversion is explicit during rollout.
- [ ] Data generation is seeded and configurable.
- [ ] Splits are by complete trajectories or control sequences.
- [ ] Training standardizers use training data only.
- [ ] Model inputs and target ordering are saved in metadata.
- [ ] Total optimizer updates are logged.
- [ ] One-step and recursive rollout metrics are both reported.
- [ ] Predicted paths are plotted in the inertial frame.
- [ ] Existing pendulum runs remain reproducible.
- [ ] At least one perfect-model transform test passes before neural-network training is interpreted.
- [ ] At least one controlled comparison varies data amount, data variety, or optimizer updates while holding other factors fixed.


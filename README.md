# Supervised Neural Network for a Torque-Driven Pendulum
## Project Overview

The goal of this project is to develop a supervised PyTorch neural network that learns to reproduce simulations of a simple pendulum subject to an applied torque input.

The project will be developed incrementally in phases. **Each phase must be reviewed and approved by me before it is committed to the GitHub repository.**

The overall goal is not only to create a working neural-network emulator, but also to understand the numerical simulation, dataset generation, neural-network implementation, and training process. The numerical simulator is the reference source of truth; the neural network learns to approximate its full-state trajectories from examples.

---

# Project Goals

The final system should be capable of learning the full state of a torque-driven pendulum from simulator-generated examples and reproducing trajectories for new combinations of initial conditions and supported torque inputs.

The project will include:

1. A numerical pendulum simulator.
2. A configurable dataset-generation pipeline.
3. A PyTorch neural network.
4. A configurable supervised-learning neural network.
5. A reproducible training and evaluation pipeline.
6. Training-loss, trajectory, and prediction-error visualization.
7. Experiments investigating how the amount and variety of simulation data affect model performance.

The project should be written so that individual components are modular and can be modified without unnecessarily changing the rest of the project.

---

# Development Phases

## Phase 1: Project Architecture

The goal of this phase is to establish the project structure and development environment.

Tasks:

* Initialize the local Git repository and connect it to a GitHub repository when the remote URL is available.
* Create a Python virtual environment.
* Install and document required dependencies.
* Use PyTorch for neural-network development.
* Establish a sensible project directory structure.
* Create initial documentation.
* Establish a reproducible way to install dependencies.
* Verify that the development environment works by running a small test program.

### Phase 1 Project Structure

The initial structure is intentionally small:

```text
README.md                 Project requirements and learning notes
requirements.txt          Runtime and development dependency ranges
pyproject.toml            Package metadata and pytest configuration
.gitignore                Local environment and generated-output exclusions
src/pendulum_sim/         Physical system simulation and data package
src/model_baseline/       Baseline supervised model package
tests/                    Automated checks
scripts/simulation/       Simulation and data demonstrations
scripts/model_baseline/   Model and experiment demonstrations
```

The `src` layout keeps project code separate from tests and scripts. The `data/` and `runs/` directories will be created when later phases generate datasets and experiment outputs; they are excluded from Git because those files are generated artifacts.

### Phase 1 Setup

From the project directory on Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
python scripts\smoke_test.py
python -m pytest
```

The virtual environment keeps this project's Python packages isolated from the system Python installation. It can be left with `deactivate` and reactivated later with `.\.venv\Scripts\Activate.ps1`. The dependency ranges are recorded in both `requirements.txt` and `pyproject.toml` so the environment can be installed directly or through the package metadata.

The Phase 1 dependencies have these roles:

* NumPy provides numerical arrays and calculations for the simulator.
* Matplotlib provides plots and the pendulum animation.
* PyTorch provides tensors and the supervised neural network.
* Pytest runs the automated checks.

Before committing Phase 1, explain:

* The purpose of each major directory/file.
* Why the selected dependencies are necessary.
* How the virtual environment works.
* How the smoke test and automated test verify the installation.

---

## Phase 2: Dynamic System Simulator

Develop a numerical simulator for a simple pendulum with an applied torque input.

### Governing Dynamics

Begin with a clearly defined physical model and document all assumptions.

For example, the model may take the form:

$$
\ddot{\theta}
=
-\frac{g}{L}\sin(\theta)
-\frac{b}{mL^2}\dot{\theta}
+\frac{\tau(t)}{mL^2}
$$

where:

* \(\theta\) = pendulum angle
* \(\dot{\theta}\) = angular velocity
* \(\ddot{\theta}\) = angular acceleration
* \(m\) = pendulum mass
* \(L\) = pendulum length
* \(g\) = gravitational acceleration
* \(b\) = damping coefficient
* \(\tau(t)\) = applied torque

If a different model is chosen, explain why.

### Numerical Integration

Use a **Runge-Kutta method**, preferably fourth-order Runge-Kutta (RK4), to numerically integrate the equations of motion.

The implementation should make the following parameters easy to change:

* Simulation duration
* Number of time steps
* Time-step size
* Initial angle
* Initial angular velocity
* Pendulum parameters
* Applied torque function

The number of time samples must be configurable so that later experiments can investigate how the quantity of training data affects neural-network performance.

### Visualization

Create an intuitive visualization system that can:

* Plot angle versus time.
* Plot angular velocity versus time.
* Plot applied torque versus time.
* Display an animation of the pendulum motion.

The visualization code should be separate from the core numerical simulator where practical.

Before committing Phase 2, explain:

* The governing equations.
* How the equations are converted into a form suitable for numerical integration.
* How RK4 works.
* The meaning of the simulator's inputs and outputs.
* How the visualization works.
* Any numerical or modeling assumptions that were made.

---

## Phase 3: Data Generation and Storage

Create a data-generation pipeline using the simulator from Phase 2.

The pipeline should make it easy to:

* Run simulations with different numbers of time samples.
* Change initial conditions.
* Change torque inputs.
* Change physical parameters.
* Save simulation results.
* Load saved simulation results for training.

The saved data should contain enough information to reproduce or understand the simulation, including relevant:

* Time values
* Inputs
* States
* Physical parameters
* Initial conditions

Use a data format that is convenient for Python/PyTorch while remaining reasonably easy to inspect.

Document the data format.

Before committing Phase 3, explain:

* What is being saved.
* Why the chosen data format was used.
* How the data will later be converted into PyTorch tensors.
* The difference between simulation data and training data.

### Phase 3 Data Format

The initial pipeline saves each dataset as a compressed NumPy `.npz` archive. A dataset contains trajectories generated on one shared time grid:

* `time`: one-dimensional time values with shape `(num_times,)`.
* `theta`: angle values with shape `(num_trajectories, num_times)`.
* `omega`: angular velocity values with shape `(num_trajectories, num_times)`.
* `torque`: applied torque values with shape `(num_trajectories, num_times)`.
* `metadata_json`: JSON metadata containing duration, sample count, initial conditions, physical parameters, and torque-function names and parameters.

The shared-grid design keeps the file easy to inspect with NumPy while allowing one file to contain multiple trajectories. Datasets with a different number of time samples can be generated and saved as separate files, which supports the later experiments on data quantity.

The `SimulationDataset.as_tensors()` method converts each trajectory-time pair into one supervised-learning example. Its four inputs are time, initial angle, initial angular velocity, and torque at that time. Its two targets are angle and angular velocity at that time. The resulting input tensor has shape `(num_trajectories * num_times, 4)`, and the target tensor has shape `(num_trajectories * num_times, 2)`.

Run the Phase 3 example with:

```powershell
python scripts\simulation\phase3_data_demo.py
```

This writes an example dataset to `data/phase3_example.npz`. The `data/` directory contains generated training material and is excluded from Git.

---

## Phase 4: Supervised Neural Network

Using PyTorch, create a neural network that predicts the full pendulum state at a requested time.

The simulator remains separate from the neural network. The simulator generates reference trajectories, and the network learns from those trajectories using ordinary supervised learning.

### Model Contract

The initial model should learn a family of trajectories while physical parameters remain fixed. Each training example represents one time on one simulated trajectory.

The network inputs are:

* Time, `t`.
* Initial angle, `theta_0`.
* Initial angular velocity, `omega_0`.
* Applied torque evaluated at that time, `tau(t)`.

The network outputs are the full state at that time:

* Angle, `theta(t)`.
* Angular velocity, `omega(t)`.

The initial implementation should use documented analytic torque functions, such as zero, constant, sinusoidal, or pulse torque. The selected torque family and its parameters must be recorded with each trajectory. If the model later needs to generalize across torque functions, the torque-function parameters or a sampled torque history must be added to the model inputs rather than assuming that one instantaneous torque value uniquely identifies an entire input signal.

The network architecture should be simple enough to understand and modify.

Document:

* Network inputs.
* Network outputs.
* Number of layers.
* Number of neurons per layer.
* Activation functions.
* Weight initialization, if applicable.
* How input and output normalization is performed.

Before committing Phase 4, explain:

* What a PyTorch tensor is.
* How the neural network is represented in PyTorch.
* How forward propagation works in the implementation.
* What the activation functions do.
* What the network is actually learning from the simulator data.
* Why the model predicts both angle and angular velocity as a full state.
* How input and output normalization affects training.

### Phase 4 Initial Architecture

The initial implementation uses `PendulumStateNetwork`, a small multilayer perceptron with:

* Four input features: `t`, `theta_0`, `omega_0`, and `tau(t)`.
* Two hidden layers with 64 neurons each.
* `Tanh` activation after each hidden layer.
* Two output values: `theta(t)` and `omega(t)`.
* PyTorch's default linear-layer weight initialization.

The `Standardizer` stores a feature-wise mean and standard deviation calculated from the training data. Inputs are standardized before the forward pass, and predicted targets can be converted back to physical units with the stored target standardizer. A zero-variance feature uses a scale of one so constant features remain well-defined.

Run the Phase 4 model demonstration with:

```powershell
python scripts\model_baseline\phase4_model_demo.py
```

This demonstrates dataset-to-tensor conversion, normalization, a forward pass, and the two-component full-state output. It does not train the network; training belongs to Phase 5.

---

## Phase 5: Train and Evaluate the Neural Network

Train the neural network using the simulation data.

Track and visualize the training loss throughout the training process.

At minimum, investigate:

* Training loss versus epoch.
* Model predictions versus simulator results.
* Prediction error.
* The effect of changing the amount of training data.
* Performance on simulator trajectories not used during training.
* Performance for initial conditions and supported torque inputs that were not present in the training split.

Split data by complete trajectory into training, validation, and test sets. Do not randomly split neighboring time samples from one trajectory across all three sets, because that would make evaluation overly optimistic.

The training process should save enough information to reproduce experiments, including the random seed, configuration, normalization values, model weights, optimizer state, and loss history.

### Phase 5 Training Outputs

The initial training pipeline uses mean squared error (MSE) between normalized predicted states and normalized simulator states. It records training and validation loss for every epoch. The evaluation pipeline converts predictions back to physical units and reports mean absolute error, root mean squared error, and maximum absolute state error on complete held-out trajectories.

The training demo also saves:

* `runs/phase5_training_history.png`: training and validation loss versus epoch.
* `runs/phase5_prediction.png`: model and simulator angle/velocity trajectories for one test trajectory.
* `runs/phase5_checkpoint.pt`: model weights, optimizer state, normalization values, trajectory split, and loss history.

Run it with:

```powershell
python scripts\model_baseline\phase5_training_demo.py
```

---

## Phase 6: Supervised-Learning Experiments

Use the trained supervised model to investigate:

* More simulation data is available.
* Less simulation data is available.
* Different initial conditions are used.
* Different torque inputs are used.

Compare interpolation and generalization using trajectory plots and numerical metrics such as mean absolute error, root mean squared error, and maximum absolute state error. Also investigate how prediction quality changes over the simulation time horizon.

Before committing Phase 6, explain:

* How the experiment changes the available training information.
* Whether the model is interpolating within the training distribution or generalizing to an unseen condition.
* How the numerical metrics relate to visible trajectory differences.
* What limitations remain in a purely data-driven approximation.

---

## Phase 7: Baseline Run Artifacts

Run the current full-state supervised baseline with:

```powershell
python scripts\model_baseline\run_baseline.py
```

Each run creates the next unused `runs/baseline_runs_N/` folder. It saves the generated dataset and checkpoint, training and validation MSE versus epoch, one validation trajectory plot, one preselected test trajectory plot, `baseline_test_error_data.csv`, and `baseline_training_log.csv`. The test-error CSV contains separate angle and angular-velocity MAE/RMSE for every test trajectory, followed by the mean and standard deviation across test trajectories. The training log records epoch, optimizer step, samples seen, learning rate after the scheduler update, training loss, and validation loss. The checkpoint contains the model state selected by the lowest validation MSE. Test data is used only for final metrics and the preselected example plot.

Training uses shuffled mini-batches of 256 samples by default. This is appropriate for the current baseline dataset: 32 training trajectories with 1001 samples each produce 32,032 training samples, or 126 batches per epoch (the final batch is retained). The default target is 5000 optimizer updates, with a maximum of 100 epochs. The step target is checked at epoch boundaries so every completed epoch uses each training sample exactly once; with this dataset the default run reaches about 5040 updates in 40 complete epochs. Training stops when either the update target or epoch ceiling is reached.

The learning rate starts at `0.001`. `ReduceLROnPlateau` monitors validation MSE once per epoch, reducing the learning rate by a factor of `0.5` after 10 epochs without improvement, down to `1e-6`. Validation is not shuffled, and normalization continues to be fit using training samples only. Batch size, update budget, epoch ceiling, learning rate, and scheduler settings can be changed through the runner's command-line options, for example:

```powershell
python scripts\model_baseline\run_baseline.py --batch-size 128 --max-optimizer-steps 6000
```

Experiment 1 changes the training initial conditions from a diagonal pairing to a full grid: 8 initial-angle values crossed with 4 initial-angular-velocity values, for 32 distinct combinations. The torque slopes are balanced across the same three values and assigned reproducibly. The validation and test trajectories, model, training settings, and simulation horizon remain unchanged from Experiment 0 so that the effect of broader training coverage can be checked directly.

Run Experiment 2 with:

```powershell
python scripts\model_baseline\run_experiment_2.py
```

Experiment 2 uses 100 trajectories total: 80 training, 10 validation, and 10 test. Its training initial conditions span a 10-by-8 grid over -1.4 to 1.4 rad and -1.0 to 1.0 rad/s. It retains the first four Experiment 1 test cases and adds six wider-range test cases; `Experiment 2 Data.md` records the exact conditions and changes from Experiment 1. The existing model, optimizer settings, seed, torque family, and 10-second simulation duration are unchanged.

---

# Experimental Goals

A major goal of this project is to understand the relationship between the amount of available data and the model's ability to reproduce the pendulum dynamics.

Experiments should therefore be designed so that the number of simulation samples can easily be changed.

Where practical, compare:

* Large datasets vs. small datasets.
* Different ranges of initial conditions.
* Training torque functions vs. held-out torque functions.
* Different training durations.
* Short-horizon vs. long-horizon prediction accuracy.

Results should be visualized rather than evaluated solely from numerical loss values.

---

# Code Quality and Project Structure

Prefer a modular project structure rather than putting the entire project into one Python file.

Keep separate concerns such as:

* Physics/model definition
* Numerical simulation
* Data generation
* Data loading
* Neural-network definition
* Training
* Evaluation metrics
* Visualization
* Experiment configuration

Use clear variable and function names.

Avoid unnecessary abstractions that make the project harder for a beginner to understand.

Do not introduce libraries or architectural patterns without explaining why they are useful.

---

# AI/Copilot Instructions

I am an undergraduate Mechanical Engineering student working on this project as part of a research lab.

My primary goal is **to learn**, not simply to have the project written for me.

I have taken system dynamics and remember most of the relevant concepts, but I have not previously worked with PyTorch. I understand neural networks theoretically, but I need additional explanation of how they are implemented in PyTorch.

Therefore:

* Explain important implementation decisions before or while implementing them.
* Explain PyTorch concepts when they first appear.
* Connect the code to the underlying mathematics and physics.
* Do not hide important implementation details behind unnecessary abstractions.
* Prefer understandable code over excessively optimized code.
* If there are multiple reasonable approaches, explain the tradeoffs and let me choose when the decision is significant.
* Do not make major architectural decisions without explaining them.
* Point out when an implementation choice is a simplification of the real physical system.
* Clearly distinguish between the simulator, the generated dataset, the supervised-learning model, and the evaluation process.

I want to understand the code well enough that I could explain it to another engineering student.

---

# Phase Review and Git Workflow

Each phase is a separate milestone and should correspond to a separate Git commit.

**Do not commit changes automatically.**

At the end of every phase:

1. Run appropriate tests or demonstrations.
2. Verify that the implementation works.
3. Summarize what was completed.
4. Explain the important concepts used.
5. Explain important implementation decisions.
6. Identify any difficulties, bugs, or uncertainties encountered.
7. Explain what files were added or modified.
8. Explain how the phase connects to the next phase.
9. Give me an opportunity to review the work.
10. Wait for my explicit approval before creating the commit.

The commit should only be created after I explicitly approve the phase.

Use clear commit messages such as:

* `Phase 1: Set up project architecture`
* `Phase 2: Implement pendulum simulator`
* `Phase 3: Add simulation data pipeline`
* `Phase 4: Implement neural network`
* `Phase 5: Train supervised baseline`
* `Phase 6: Run supervised-learning experiments`

---

# General Development Rules

* Do not skip phases.
* Do not implement future phases prematurely unless I explicitly ask.
* Keep the project runnable at the end of each phase.
* Prefer small, understandable changes.
* Test functionality as it is developed.
* Explain errors and debugging steps rather than silently fixing them.
* Do not commit to GitHub without my explicit approval.
* Preserve reproducibility of experiments.
* Record important assumptions and parameter choices in the documentation.

# Original Project Plan: Supervised Neural Network for a Torque-Driven Pendulum

> This document is the baseline project plan before any development phase is completed. It is preserved as a reference while `README.md` continues to evolve with setup instructions, implementation details, test results, and phase-specific notes.

## Project Overview

The goal of this project is to develop a supervised PyTorch neural network that learns to reproduce simulations of a simple pendulum subject to an applied torque input.

The project will be developed incrementally in phases. **Each phase must be reviewed and approved by me before it is committed to the GitHub repository.**

The overall goal is not only to create a working neural-network emulator, but also to understand the numerical simulation, dataset generation, neural-network implementation, and training process. The numerical simulator is the reference source of truth; the neural network learns to approximate its full-state trajectories from examples. The biggest thing that needs to be testable is how much data a NN requires to accurately model a dynamic system. 

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
src/pendulum_sim/         Importable project source package
tests/                    Automated checks
scripts/                  Runnable development utilities
```

The `src` layout keeps project code separate from tests and scripts. The `data/` and `runs/` directories will be created when later phases generate datasets and experiment outputs; they are excluded from Git because those files are generated artifacts.

### Phase 1 Setup

From the project directory on Windows PowerShell:

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
python scripts\\smoke_test.py
python -m pytest
```

The virtual environment keeps this project's Python packages isolated from the system Python installation. It can be left with `deactivate` and reactivated later with `.\\.venv\\Scripts\\Activate.ps1`. The dependency ranges are recorded in both `requirements.txt` and `pyproject.toml` so the environment can be installed directly or through the package metadata.

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

$$
\\ddot{\\theta}
=
-\\frac{g}{L}\\sin(\\theta)
-\\frac{b}{mL^2}\\dot{\\theta}
+\\frac{\\tau(t)}{mL^2}
$$

where:

* \\(\\theta\\) = pendulum angle
* \\(\\dot{\\theta}\\) = angular velocity
* \\(\\ddot{\\theta}\\) = angular acceleration
* \\(m\\) = pendulum mass
* \\(L\\) = pendulum length
* \\(g\\) = gravitational acceleration
* \\(b\\) = damping coefficient
* \\(\\tau(t)\\) = applied torque as a control input

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

The most important aspect at this stage is to be able to see clearly how much data a NN needs to simulate a dynamic system.
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

## Phase 7: Increase Scope Architecture

Now that there is a basic model running the goal is to do more, working with the current architecture and code as a starting point, but also changing some of how it works.

Goals:
* Make it so that all numerical simulation scripts are kept in a different folder from all model scripts, this will make it easier to change what physical model I am testing in the future, as I may want to solve a unicycle physical system
* Put all current model architecture in a folder referred to as model_baseline, as I will soon want to create a new model that trains off of the residual instead of the full system state, and I want this to be able to be run seperately so that they can be compared
* Make it so that tests that are currently run are called baseline_learning_curves (this graph contains Training MSE vs Epochs and Validation MSE vs Epochs. Validation will be testing on generated trajectories that were held out from training data, 10% of the total trajectories), and baseline_training_comparison (this will hold a graph that shows how the lowest validation MSE model compares with the numerical simulation after all training, and will include theta_dot and theta vs time for 10 seconds using a validation trajectory) and baseline_test_comparison (this will be a graph for one test trajectory selected before training, not selected based on model performance). Finally create a table called baseline_test_error_data that reports angle and angular-velocity MAE and RMSE for each test trajectory, along with the mean and standard deviation of each metric across all test trajectories.
* Store all graphs and tables in a folder called baseline_runs_0, and increase the subscript by 1 each time a new experiment is run
* Create a file in the runs folder (eg. baseline_runs_0) called "Experiment 0 Data" (with the number moving up by one to match the subscript in the runs folder) that details exactly where all data can be found and what it represents, as well as an explanation of the general flow of data, including how much data is being included and trained on. Make this part systematic and very simple to read so that others can understand. This section should include:
    * how many trajectories are in the dataset,
    * how many time points per trajectory,
    * that training/validation/test are split by trajectory, and have a 80/10/10 ratio
    * what the exact torque families are,
    * where each generated plot/checkpoint comes from and where they are stored.
    * a section describing if anything changed with respect to the code between the last experiment and this one

Use multiple test trajectories so that variability across trajectories can be summarized. If 10% of a small dataset would leave too few test trajectories, reserve a larger test set and document the resulting split.

This stage is only for setting up future changes, not creating or trying to run and compare new models. Make minimal changes to functional code while creating architectural splits that allow for other models or physical systems to be run in the future using this same framework. The residual model as well as comparison will be completed in future stages, not this one.

## Phase 8: Residual Model

The goal is to create a similar NN and model as the last model, but by calculating the residual, which is a one-step state change as opposed to finding the next state in its entirety. The one-step state change is $\Delta x_k = x_{k+1} - x_k$. The model predicts this change, then reconstructs the next state as $\hat{x}_{k+1} = x_k + \widehat{\Delta x}_k$.

Use a fixed time step of 0.01 seconds. The model inputs are the current state \(x_k = [\theta_k, \dot{\theta}_k]\) and the known applied torque at the start, midpoint, and end of the time step. The model outputs \(\Delta x_k = [\Delta\theta_k, \Delta\dot{\theta}_k]\). During training, use simulator states as the current state and the simulator's next-step state change as the target. During evaluation, perform a rollout: use each predicted state as the current state for the next step, and compare the resulting full trajectory with the simulator.

All architecture and procedures should mirror the baseline model, with the word residual replacing the word baseline in all files (eg. model_residual as the top level folder and residual_runs_0 holding all graphs and tables). All test procedures should be the same, and it should be trained on the exact same training, validation, and test trajectories as the baseline model, with similar graphs and per-trajectory error tables being made. Include a section of the README that details all of the same data as was created for the baseline model.

## Phase 9: Model Comparison

Compare the baseline and residual models on the same test trajectories. Manually compare the example graphs, and compare the per-trajectory angle and angular-velocity MAE and RMSE, including their mean and standard deviation across trajectories. Use validation data to select each model's checkpoint; do not use test results to select models or training settings. Focus on how much data each model needs to predict the pendulum motion accurately and consistently.

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

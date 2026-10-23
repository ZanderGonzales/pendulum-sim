# Phase 4 Data: One-Step Physics-Residual Neural Network

## Results and scope

The residual NN, supervised examples, train-only standardizers, one-step hybrid inference, and portable initial checkpoint are implemented. This phase verifies the learning problem and correction geometry. **No optimizer updates were performed and the checkpoint is untrained.** The full 10,000-update Adam training schedule and learned recursive evaluation remain phase 5.

- Architecture: 14 inputs, 2 hidden layers of 64 neurons, Tanh hidden activations, 12 linear outputs.
- Trainable parameters: 5,900.
- Model initialization seed: 0; PyTorch: 2.14.0+cpu.
- Prepared samples: {'train': 80000, 'validation': 10000, 'test': 10000, 'benchmark': 10000}.
- Standardizer fitting: 80,000 training samples from 80 complete training trajectories only.
- Forward/backward check: 256 training samples; finite gradients for every parameter tensor; weights unchanged; zero optimizer updates.
- Initial checkpoint reload: maximum state-component difference 0 on the fixed training-state check batch.

## Exact-residual reconstruction checks

These checks apply the known simulator-minus-physics residual to verify the coordinate transformations. They use true next states and are **not learned predictions, generalization scores, or recursive rollouts**. Zero-residual checks independently verify that applying zero physical correction preserves physics-only prediction.

- train: 80,000 transitions; maximum reconstruction position error 0 m, orientation error 3.33170795e-16 rad, linear velocity error 6.77626358e-21 m/s, angular velocity error 0 rad/s.
- validation: 10,000 transitions; maximum reconstruction position error 0 m, orientation error 3.33104176e-16 rad, linear velocity error 6.6174449e-24 m/s, angular velocity error 0 rad/s.
- test: 10,000 transitions; maximum reconstruction position error 0 m, orientation error 4.44089243e-16 rad, linear velocity error 1.69406589e-21 m/s, angular velocity error 0 rad/s.
- benchmark: 10,000 transitions; maximum reconstruction position error 0 m, orientation error 3.33067896e-16 rad, linear velocity error 0 m/s, angular velocity error 0 rad/s.

### Test and benchmark mean MAEs

The following are equal-weight means of the per-trajectory one-step MAEs. The exact-residual values measure reconstruction precision, not NN accuracy.

- test, physics_only: mean position MAE **4.19603804e-08 m**, std 2.8284042e-08 m; mean orientation MAE **1.24415934e-09 rad (7.12850792e-08 deg)**, std 1.0248782e-09 rad.
- test, exact_residual_reconstruction: mean position MAE **0 m**, std 0 m; mean orientation MAE **3.17486471e-17 rad (1.81906348e-15 deg)**, std 2.20325617e-17 rad.
- benchmark, physics_only: mean position MAE **4.29712985e-08 m**, std 1.90215184e-08 m; mean orientation MAE **1.56173415e-09 rad (8.94807754e-08 deg)**, std 4.29757267e-10 rad.
- benchmark, exact_residual_reconstruction: mean position MAE **0 m**, std 0 m; mean orientation MAE **3.34692754e-17 rad (1.91764822e-15 deg)**, std 1.61987076e-17 rad.

## What the network learns

For a true simulator current state x_k and the actual applied wrench u_k, first compute the independent physics step. The target is the finite-step error of that prediction:

$$x^p_{k+1}=F_{physics}(x_k,u_k,\Delta t),\qquad r_k=x^{sim}_{k+1}\ominus x^p_{k+1}$$

$$\hat x_{k+1}=x^p_{k+1}\oplus NN(z_k)$$

The NN is not asked to relearn gravity, thrust acceleration, or rigid-body rotation. Those are already present in the independent predictor. The unicycle model learned its entire one-step body displacement and heading increment; this drone model learns only the discrepancy between physics and MuJoCo. The residual is not an acceleration and is not divided by the timestep.

## The 14 inputs

- Current body-frame linear velocity: 3 components, R(q_k).T @ v_world.
- Current body-frame angular velocity: 3 components, already stored in that frame.
- Current body-frame gravity: 3 components, R(q_k).T @ g_world.
- Applied physical control: total thrust in N and three right-hand body moments in N m.
- Prediction interval in seconds: 1 component.

**Body-frame gravity is the world gravity vector expressed along the drone's current axes.** A level drone sees [0, 0, -9.81] regardless of yaw; a tilted drone sees components along its tilted axes. This is the same gravity used by the physics model, not an additional force. The features omit absolute position and global yaw: rigid-body motion and still-air resistance do not require them for this setup. Every input comes from the current state, the known applied control, and fixed physics settings; the NN receives no next-state truth.

The exact feature order is saved in standardizers.json and the initial checkpoint. The controls are applied SI wrenches after actuator limits, not raw MuJoCo commands or rotor speeds.

## The 12 outputs and how they are applied

Let R_k be the current body-to-world orientation. Position and velocity corrections are:

$$r_p=R_k^T(p^{sim}_{k+1}-p^p_{k+1}),\quad r_v=R_k^T(v^{sim}_{k+1}-v^p_{k+1})$$

$$\hat p_{k+1}=p^p_{k+1}+R_k\hat r_p,\quad \hat v_{k+1}=v^p_{k+1}+R_k\hat r_v$$

The three orientation outputs form a shortest rotation vector:

$$r_\theta=\mathrm{Log}((R^p_{k+1})^T R^{sim}_{k+1}),\quad \hat R_{k+1}=R^p_{k+1}\mathrm{Exp}(\hat r_\theta)$$

This orientation correction is in predicted-next body axes and composes on the right. The code converts the vector to a unit quaternion and uses the Hamilton product q_physics_next * quaternion_from_rotvec(r_theta). Quaternion components are never subtracted. q and -q yield the same physical correction and error. The remaining three outputs are simulator-minus-physics angular-velocity state components, added in their respective body-coordinate representation.

`apply_residual` explicitly implements these transformations. Its output remains a 13-component state with a normalized scalar-first body-to-world quaternion. Training targets are built from true current states; eventual recursive use must compute features and correction frames from predicted current states.

## Standardization and numerical precision

Physics integration, residual construction, population means, and population standard deviations use float64. Each feature and target coordinate is standardized independently with statistics from the train split. Only the standardized values become float32 NN tensors. Network outputs are converted back to float64 before unstandardization and state correction.

Training target standard deviations span 7.95915019e-10 to 1.01649303e-05 in their respective physical units. An inherited absolute scale cutoff of 1e-8 would incorrectly stop normalizing some orientation targets. This implementation uses the measured positive standard deviation for nonconstant columns and scale=1 only for exactly constant columns. Constant means use their recorded value exactly; the fixed dt column therefore becomes exactly zero. Very small targets are preserved rather than artificially enlarged.

Validation, test, and held-out waypoint samples use the frozen training statistics and cannot be passed to fit_standardizers. The saved standardizer includes the fitting trajectory IDs and sample count. The benchmark remains separate and is used here only for algebraic consistency checks, not tuning.

A zero standardized NN output unstandardizes to the training target mean. It does not necessarily mean zero physical residual. The physics-equivalence check therefore applies an explicit physical zero vector.

## Architecture and PyTorch

The default MLP uses Linear(14,64), Tanh, Linear(64,64), Tanh, Linear(64,12). The final layer is linear so signed standardized residuals are unrestricted. Hidden width and hidden-layer count are configurable. Input and output layers are additional to the hidden-layer count. PyTorch autograd checks backpropagation through the NN's standardized residual MSE. Physics and target construction happen outside that graph because this is supervised one-step residual learning, not differentiation through MuJoCo.

The architecture variants are constructible (parameter counts include all biases):

- 2x32: 1,932 trainable parameters.
- 2x64: 5,900 trainable parameters.
- 2x128: 19,980 trainable parameters.
- 1x64: 1,740 trainable parameters.
- 4x64: 14,220 trainable parameters.

References: [PyTorch Linear](https://docs.pytorch.org/docs/2.14/generated/torch.nn.Linear.html) and [Tanh](https://docs.pytorch.org/docs/2.14/generated/torch.nn.Tanh.html).

## Artifacts and file architecture

- `src/model_drone_residual/model.py`: configurable MLP, float64 standardizers, serialized feature/target contract.
- `src/model_drone_residual/residuals.py`: input features, frame definitions, and correction composition.
- `src/model_drone_residual/training.py`: true-state supervised examples, training-only scaler fitting, tensor preparation, backward check. No scheduled fitting loop yet.
- `src/model_drone_residual/evaluation.py`: one-step HybridPredictor and initial checkpoint save/load. No recursive evaluator yet.
- `src/drone_sim/frames.py`: reusable vector rotation, quaternion composition, rotation-vector exponential map.
- `scripts/model_drone_residual/prepare_drone_residual.py`: this reproducible phase-4 entry point.
- `tests/test_drone_residual.py`: geometry, leakage prevention, tiny-target precision, NN variants, gradients, checkpoint tests.
- `standardizers.json`: training-fitted statistics, coordinate ordering, fitting trajectory IDs and count.
- `checkpoint_initial.pt`: UNTRAINED seeded model, frozen standardizers, physics/timing constants, schema and frame contract. It is not checkpoint_best.pt or checkpoint_final.pt.
- `prepared_samples/<split>.npz`: raw float64 features/targets, standardized float32 arrays, per-transition trajectory IDs/step indices, metadata.
- `contract_checks.json`: reconstruction, zero-residual, frozen statistics, gradient, and checkpoint reload results.
- `construction_metrics.csv` / `.json`: per-flight and equal-weight per-split physical metrics for physics-only versus exact-residual reconstruction.
- `comparison_metrics.csv`: split/method summary rows, including mean test position/orientation MAEs and standard deviations.
- `plots/<trajectory_id>_construction.png`: preselected test/benchmark examples with a large 3D path and smaller position/orientation angle error plots. No planar projection or position/velocity component plots.
- `predictions/<trajectory_id>_construction.npz`: the corresponding true, physics-next, and exact-residual reconstructed states; these are construction checks, not NN forecasts.
- `run_metadata.json`: exact command, source/input SHA256s, model/source provenance, architecture, seed, schema, dtype, phase status, and zero optimizer updates.

Position MAE uses time-average Euclidean distance, orientation MAE uses shortest absolute rotation angle in radians/degrees, and the exact initial state is excluded. Means give every flight equal weight; standard deviations use ddof=0. Velocity MAE/RMSE, position/orientation RMSE, and final/maximum position errors remain in the CSV/JSON, even though velocity curves are omitted from plots.

## Reproduction and interfaces

From the repository root:

```powershell
python scripts/model_drone_residual/prepare_drone_residual.py
```

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_drone_residual.py -q
```

The entry point accepts `--dataset`, `--benchmark`, `--output-root`, `--seed`, `--hidden-size`, and `--hidden-layers`. Default output is runs/Drone/phase_4; repeats preserve earlier results under repeat_N.

`prepare_samples(dataset, 'train')` builds true-state samples; `fit_standardizers(training_samples)` fits only train statistics. `HybridPredictor(model, standardizers, physics).step(state, applied_control)` computes a physics transition and its NN correction. `load_checkpoint(path)` returns that predictor and its checkpoint metadata. **The saved initialization is not ready for useful forecasting until trained.**

## Implementation verification

The full project suite passed: **169 tests in 18.76 seconds**, including the existing pendulum, unicycle, drone simulator, dataset, physics, and playback tests. The 31 new residual cases cover all five architecture variants, parameter counts, body-frame gravity and velocity, translation/heading/quaternion-sign invariance, batched rotations, quaternion exponential/composition, arbitrary and recorded-state residual reconstruction, zero-residual equivalence, transition alignment, tiny-target precision, constant-input scaling, train-only fitting, finite gradients without weight updates, initial checkpoint/JSON round trips, and invalid contracts and inputs.

```powershell
.\.venv\Scripts\python.exe -m pytest -q --basetemp .pytest_cache/drone_phase4_regression --tb=short
```

After generation, all four prepared-sample archives were reloaded with pickle disabled and checked for shape, dtype, finite values, standardized-target consistency, and exactly zero standardized dt. Training targets retained unit standard deviation after float32 conversion. The checkpoint weights matched a freshly constructed model with the recorded seed exactly, confirming that the forward/backward diagnostic did not train it. The standalone JSON standardizers matched the checkpoint statistics. Saved equal-flight means were independently recomputed from CSV and matched JSON. All six exported construction examples retained normalized quaternions and exact reconstructed positions. Every recorded source-code/input-data SHA256 matched the files used. Representative ordinary-test and benchmark figures were visually checked against the requested large-3D-plus-two-errors layout. Drone_Plan.md and README.md retained their starting hashes.

## Interpretation and next work

Successful reconstruction verifies that targets and correction composition are mutually consistent. Finite gradients verify that the NN can receive a training signal. Neither proves learned accuracy. All data use one drone property configuration, still air, conservative flight, and one timestep; including dt as an input does not establish generalization to other timesteps.

Phase 5 will use Adam, learning rate 0.001, batch size 256, exactly 10,000 default optimizer updates, validation every 100 updates and at the end, best/final checkpoints, and separate physics/hybrid one-step and fully recursive results. Phase 4 has no optimizer state, trained best/final checkpoints, loss curves, or learned test-accuracy claims. No truth refresh mechanism was introduced.

Drone_Plan.md and README.md were not edited. Prior phase output was not rewritten. No commit was created.

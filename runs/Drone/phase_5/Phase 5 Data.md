# Phase 5 Data: Training and Recursive Evaluation

## Results

The physics-residual NN is trained and evaluated against held-out MuJoCo flights. The checkpoint used for these predictions is recorded below. The standard training entry point selects its best checkpoint using validation standardized residual MSE. Physics-only and hybrid predictions replay identical recorded applied controls. Recursive prediction uses simulator truth only for initialization and later scoring; there are no truth refreshes.

- Architecture: 2 hidden layers, 64 neurons per hidden layer, Tanh, 14 inputs and 12 outputs.
- Optimizer: Adam; learning rate 0.001; batch size 256; seed 0.
- Selected checkpoint update: 9,900.
- Checkpoint source: runs/Drone/phase_5/checkpoint_best.pt; selection: lowest validation standardized residual MSE.
- Dataset: {'train': 80, 'validation': 10, 'test': 10}; separate held-out-family benchmark: 10 flights.
- Each default flight is 10 s, with 1,000 predictions at 0.01 s; the physics predictor uses five 0.002 s RK4 substeps.

- Actual optimizer updates: **10,000**.
- Epochs started/completed: 32 / 31; fractional epoch progress: 31.9504.
- Samples processed: 2,556,032; 313 batches per complete epoch.
- Training runtime: 28.011 s, excluding 7.411 s preparation; cpu, 1 PyTorch thread(s).
- Trainable parameters: 5,900.
- Initial validation residual MSE: 1.05766129; best: **0.000604778282** at update 9,900.
- Final full-training residual MSE: 0.000193039749; final validation residual MSE: 0.000626383327.

## Test trajectory results

### One step

- **physics_only**, 10 flights: mean position MAE **4.19603804e-08 m**, std 2.8284042e-08 m; mean orientation MAE **1.24415934e-09 rad (7.12850792e-08 deg)**, std 1.0248782e-09 rad.
  Mean position/orientation RMSE: 6.33156537e-08 m / 1.78778873e-09 rad. Mean final/max position error: 1.76875091e-10 / 1.60043329e-07 m.
  Mean linear velocity MAE/RMSE: 8.39190432e-06 / 1.26629922e-05 m/s; mean angular velocity MAE/RMSE: 2.48805357e-07 / 3.57541147e-07 rad/s.
- **hybrid**, 10 flights: mean position MAE **9.41133954e-10 m**, std 4.39598037e-10 m; mean orientation MAE **2.7038358e-11 rad (1.5491838e-09 deg)**, std 1.06021303e-11 rad.
  Mean position/orientation RMSE: 1.44659253e-09 m / 4.49786159e-11 rad. Mean final/max position error: 1.68682967e-10 / 9.08533821e-09 m.
  Mean linear velocity MAE/RMSE: 1.91456012e-07 / 2.89948855e-07 m/s; mean angular velocity MAE/RMSE: 5.32774977e-09 / 9.03027646e-09 rad/s.

Reduction in mean MAE relative to physics-only: position **97.757%**, orientation **97.827%**. A negative reduction indicates an increase in error.

### Recursive

- **physics_only**, 10 flights: mean position MAE **0.0143260365 m**, std 0.00579547429 m; mean orientation MAE **0.000171113069 rad (0.00980405669 deg)**, std 6.29730519e-05 rad.
  Mean position/orientation RMSE: 0.0205988425 m / 0.00019932992 rad. Mean final/max position error: 0.0512667036 / 0.0512667036 m.
  Mean linear velocity MAE/RMSE: 0.00548275882 / 0.00702696875 m/s; mean angular velocity MAE/RMSE: 5.1033175e-05 / 5.48593664e-05 rad/s.
- **hybrid**, 10 flights: mean position MAE **0.000442591641 m**, std 0.000434539123 m; mean orientation MAE **6.42021996e-06 rad (0.000367851507 deg)**, std 5.98451333e-06 rad.
  Mean position/orientation RMSE: 0.000651834309 m / 7.95964998e-06 rad. Mean final/max position error: 0.00171486678 / 0.00171486678 m.
  Mean linear velocity MAE/RMSE: 0.000179734604 / 0.000237861927 m/s; mean angular velocity MAE/RMSE: 1.68335213e-06 / 1.82553607e-06 rad/s.

Reduction in mean MAE relative to physics-only: position **96.911%**, orientation **96.248%**. A negative reduction indicates an increase in error.

## Benchmark trajectory results

### One step

- **physics_only**, 10 flights: mean position MAE **4.29712985e-08 m**, std 1.90215184e-08 m; mean orientation MAE **1.56173415e-09 rad (8.94807754e-08 deg)**, std 4.29757267e-10 rad.
  Mean position/orientation RMSE: 6.58198841e-08 m / 1.9570189e-09 rad. Mean final/max position error: 1.67331365e-09 / 2.01678114e-07 m.
  Mean linear velocity MAE/RMSE: 8.59415333e-06 / 1.31638905e-05 m/s; mean angular velocity MAE/RMSE: 3.12390761e-07 / 3.91433257e-07 rad/s.
- **hybrid**, 10 flights: mean position MAE **9.14795116e-09 m**, std 6.8070108e-09 m; mean orientation MAE **1.26054735e-10 rad (7.22240432e-09 deg)**, std 6.76666267e-11 rad.
  Mean position/orientation RMSE: 1.50734873e-08 m / 1.74191476e-10 rad. Mean final/max position error: 1.00918644e-09 / 5.33483625e-08 m.
  Mean linear velocity MAE/RMSE: 1.85729416e-06 / 3.04228877e-06 m/s; mean angular velocity MAE/RMSE: 2.52722139e-08 / 3.4856617e-08 rad/s.

Reduction in mean MAE relative to physics-only: position **78.711%**, orientation **91.929%**. A negative reduction indicates an increase in error.

### Recursive

- **physics_only**, 10 flights: mean position MAE **0.0121544784 m**, std 0.00491539226 m; mean orientation MAE **0.000127819033 rad (0.00732349112 deg)**, std 4.9017943e-05 rad.
  Mean position/orientation RMSE: 0.0173916283 m / 0.000147807128 rad. Mean final/max position error: 0.0440691331 / 0.0440691331 m.
  Mean linear velocity MAE/RMSE: 0.00464961522 / 0.00594905206 m/s; mean angular velocity MAE/RMSE: 2.90908592e-05 / 3.06901298e-05 rad/s.
- **hybrid**, 10 flights: mean position MAE **0.00121451697 m**, std 0.000920154814 m; mean orientation MAE **1.26122314e-05 rad (0.000722627628 deg)**, std 7.06397542e-06 rad.
  Mean position/orientation RMSE: 0.001777322 m / 1.66744993e-05 rad. Mean final/max position error: 0.00397136973 / 0.0042472956 m.
  Mean linear velocity MAE/RMSE: 0.000503572897 / 0.00066572488 m/s; mean angular velocity MAE/RMSE: 4.23298266e-06 / 5.13014456e-06 rad/s.

Reduction in mean MAE relative to physics-only: position **90.008%**, orientation **90.133%**. A negative reduction indicates an increase in error.

## Interpretation of this run

For the familiar-family test flights, recursive mean position MAE decreased from **14.33 mm to 0.443 mm**, a **96.91% reduction**, and mean orientation MAE decreased from **0.009804 degrees to 0.000368 degrees**. Mean final position error after 10 seconds decreased from **51.27 mm to 1.71 mm**. The hybrid position-MAE standard deviation was 0.435 mm across the ten test trajectories, so performance still varies by flight.

The separate waypoint-family benchmark also improved: recursive mean position MAE decreased from **12.15 mm to 1.21 mm**, and mean orientation MAE from **0.007323 degrees to 0.000723 degrees**. Its mean final position error decreased from **44.07 mm to 3.97 mm**. The learned model is less accurate on this held-out family than on the ordinary test set, while improving both against their corresponding physics-only baselines.

The trained correction reduces drift in this fixed dataset without simulator truth refreshes. These are results for seed 0 with known future controls and the existing conservative still-air envelope; the planned multi-seed and coverage comparisons have not been run. The validation-selected update 9,900 is retained even though training completed all 10,000 updates. Test results were not used to replace that selection or change the model settings.

## Training theory and implementation

Training examples use the simulator's true current state, the actual applied wrench during that interval, and the simulator's next state. The independent rigid-body predictor provides the physics next state. The 12 targets are only its finite-step error: current-body-frame position/velocity differences, a right-composed orientation rotation vector in predicted-next body axes, and angular-velocity component differences. Phase 4 defines and verifies those transformations.

The 14 inputs are body-frame linear velocity (3), angular velocity (3), body-frame gravity (3), applied thrust/body moments (4), and dt (1). Body-frame gravity is the world gravity vector expressed along the current drone axes, R(q).T @ g_world. Translational correction vectors rotate back using the current attitude; orientation is corrected by quaternion composition, never component subtraction.

The loss is mean squared error across all 12 standardized residual coordinates. Each target coordinate is centered and scaled with training-only statistics, so the loss balances their observed variation rather than mixing metres, radians, and velocity units directly. Adam adjusts the NN weights from first- and second-moment estimates of minibatch gradients. Learning rate stays constant; no scheduler or early stopping changes the optimizer-update budget. The physics integrator is outside the autograd graph: only the correction MLP is optimized. See [PyTorch Adam](https://docs.pytorch.org/docs/2.14/generated/torch.optim.Adam.html).

Every epoch shuffles all training transitions using a seeded independent torch.Generator. The final smaller batch of a complete epoch is retained. Training stops immediately after the requested number of optimizer.step calls, including a partial final epoch if needed. Validation is measured at update 0, every configured interval (100 by default), and the final update without duplicating it. Each logged training and validation loss is a full-split sample/coordinate-weighted MSE at the current weights, not a running average of minibatch losses.

The best checkpoint minimizes validation residual MSE, including initialization. The final checkpoint records the weights and optimizer state at the exact requested update count. They can differ. Neither test data nor the separate waypoint benchmark is requested by the training function. Held-out data are evaluated only after training and checkpoint selection. No setting was selected using the test results in this phase.

Physics, raw residual subtraction, standardizer statistics, unstandardization, and state corrections use float64. Only standardized arrays and NN weights use float32. Nonconstant residual coordinates retain their actual small standard deviations; exactly constant columns use scale 1. This preserves the nanometre-scale one-step position residual instead of losing it in float32 state subtraction.

## One-step versus recursive prediction

One-step evaluation restarts each prediction from its true current state. Recursive evaluation initializes once and then feeds the previous predicted state into both the physics predictor and NN feature construction. Thus body-frame gravity, velocity, and correction transformations follow the predicted attitude. The recursive API accepts only initial states and applied-control arrays; it cannot read future true states. The controller generates reference data but is not rerun or given simulator truth while predicting. These are predictions conditional on known controls.

Training minimizes local residual error. A lower one-step residual MSE does not guarantee a proportional reduction in recursive drift: corrections change subsequent states, and small biased errors can accumulate. Interpret the path and error curves manually; no automatic fidelity threshold defines success. The benchmark evaluates new waypoint-family flights, separately from familiar-family tests.

## Metric definitions

Position MAE is the time-average Euclidean distance between predicted and true positions. Orientation MAE is the time-average shortest absolute rotation angle, reported in radians and degrees. RMSE is the square root of mean squared norm/angle. Linear and angular velocity metrics use vector norms of world-linear and body-angular state-component errors. The exact initial state is excluded from means and maxima. Final position error is at the last timestamp. Every overall mean gives each trajectory equal weight; standard deviations are across trajectory metrics with ddof=0. Splits, prediction modes, and predictors remain separate in every summary.

## Files and artifacts

- `src/model_drone_residual/training.py`: configurable exact-update training, train-only scaling, full-split validation, best/final checkpoint snapshots.
- `src/model_drone_residual/evaluation.py`: recursive hybrid inference, held-out comparisons, saved predictions and physical metrics.
- `scripts/model_drone_residual/train_drone_residual.py`: train, select, save, and evaluate this phase.
- `scripts/model_drone_residual/evaluate_drone_rollout.py`: repeat evaluation of a saved checkpoint without retraining.
- `checkpoint_best.pt` / `checkpoint_final.pt`: model, standardizers, physics/timing contract, optimizer state, update/epoch/sample counters, seed, sampler/RNG states, configuration, losses, history, provenance.
- `standardizers.json`: train-fitted statistics and fitting trajectory IDs/sample count.
- `training_metrics.csv`, `training_summary.json`, `loss_curves.png`: full training/validation losses versus updates and actual training accounting.
- `test_metrics.json`: all final test and benchmark summaries, separated by mode and predictor.
- `one_step_metrics.csv` / `.json`, `rollout_metrics.csv` / `.json`: per-trajectory metrics and equal-weight summaries.
- `comparison_metrics.csv`: split/mode/predictor summary rows, including mean position and orientation MAE and variability.
- `predictions/<split>_<mode>.npz`: full truth/physics/hybrid traces, applied controls, time, IDs, families, checkpoint metadata.
- `predictions/<trajectory_id>_hybrid_recursive.npz`: individual NN flight tracks compatible with the existing single-drone playback script.
- `plots/<trajectory_id>_<mode>.png`: first saved flight of each family, chosen without reference to accuracy; large 3D path and smaller position/orientation angle errors only.
- `run_metadata.json`: source/input hashes, revision/dirty state, configuration, checkpoint selection, runtime, simulation provenance, and completion status.

The checkpoints record sampler position and RNG state for reproducibility; automatic training resumption is not implemented in this phase. An evaluation-only repeat retains its source checkpoint and writes fresh evaluation artifacts; training artifacts stay in the source directory.

## Reproduction

From the repository root:

```powershell
python scripts/model_drone_residual/train_drone_residual.py
```

Default training and independent evaluation commands:

```powershell
.\.venv\Scripts\python.exe scripts/model_drone_residual/train_drone_residual.py
.\.venv\Scripts\python.exe scripts/model_drone_residual/evaluate_drone_rollout.py --checkpoint runs/Drone/phase_5/checkpoint_best.pt
```

For example, play a learned recursive test trajectory:

```powershell
python scripts/drone/playback_flight.py runs/Drone/phase_5/predictions/test_000000_hybrid_recursive.npz --paused
```

Defaults read the fixed phase-2 archives. Training accepts `--updates`, `--batch-size`, `--learning-rate`, `--validation-interval`, `--seed`, `--hidden-size`, `--hidden-layers`, and `--threads`. Both entry points accept dataset/benchmark paths and an output root. Repeated executions preserve earlier results under `phase_5/repeat_N/`.

## Implementation verification

The full project suite passed: **186 tests in 37.16 seconds**, including the existing pendulum, unicycle, drone simulator, data, physics, residual, and playback checks. The 17 new phase-5 cases verify exactly 10,000 real Adam step calls by default, final partial-epoch accounting, validation at intervals and the final update without duplication, validation-only checkpoint selection, training's exclusion of test data, seeded repeatability, optimizer/normalizer checkpoint contents, recursive use of predicted states with no future-truth argument, batch/single rollout agreement, split/mode/predictor metric separation, equal-flight means, playback exports, and invalid settings.

```powershell
.\.venv\Scripts\python.exe -m pytest -q --basetemp .pytest_cache/drone_phase5_regression --tb=short
```

Artifact verification confirmed 10,000 final optimizer updates, 2,556,032 processed samples, 31 complete epochs plus a partial 32nd, and 101 loss measurements at updates 0 through 10,000. Adam state counters were 9,900 in the best checkpoint and 10,000 in the final checkpoint. Frozen standardizers matched phase 4 exactly. All four combined prediction archives contained finite full states and normalized quaternions. Per-trajectory CSV means independently matched every saved overall position/orientation MAE. Physics-only recursive traces matched phase 3 byte-for-byte as arrays. All 20 individual learned recursive tracks loaded through the existing playback loader without opening a GUI.

The standalone evaluation command was also run against the selected checkpoint, writing temporary verification output under `.pytest_cache/drone_phase5_cli/phase_5`. It reproduced every saved test and benchmark metric exactly, without retraining. Loss curves and representative one-step/recursive test and benchmark figures were visually inspected. Recorded source-code and input-data SHA256s matched the files used. Drone_Plan.md, README.md, and Runs Masterlist.md retained their original hashes for this phase.

## Assumptions and next work

This is one seed with one fixed drone property configuration, still air, conservative contact-free flights, and recorded future controls. Broader seed, quantity, variety, update-count, and architecture comparisons remain phase 7. Refresh schedules remain phase 6; none are enabled or implemented here. The benchmark is reported separately and is not used for checkpoint selection.

Drone_Plan.md, README.md, Runs Masterlist.md, and prior phase outputs were not edited. No commit was created.

## To watch

```powershell
.\.venv\Scripts\python.exe scripts/drone/playback_flight.py runs/Drone/phase_5/predictions/test_recursive.npz --trajectory-id test_000000 --compare both --paused
```
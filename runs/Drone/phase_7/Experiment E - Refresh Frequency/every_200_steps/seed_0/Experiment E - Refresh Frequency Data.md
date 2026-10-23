# Experiment: Refresh Frequency

## Run: Every 200 steps

- Training seed: 0.

- Requested optimizer updates for source training: 10,000.
- Actual optimizer updates for source training: 10,016.
- Completed source-training epochs: 32.
- Selected checkpoint update: 10,016.
- Trainable parameters: 5,900.
- Source training time: 13.3145 s.

No training or weight updates occurred for this refresh run. The source checkpoint remains fixed.

Source run: `runs/Drone/phase_7/Experiment A - Trajectory Quantity/broad_80/seed_0`.

Errors below use forecasts saved before any truth replacement. Playback shows post-replacement states.

## Test: recursive

### Physics only

- Mean position MAE: 0.000478894 m.
- Trajectory standard deviation of position MAE: 0.000296752 m.
- Mean orientation MAE: 0.000955521 deg.
- Trajectory standard deviation of orientation MAE: 0.000737477 deg.
- Mean orientation MAE in radians: 1.6677e-05 rad.
- Mean position RMSE: 0.000829327 m.
- Mean orientation RMSE: 0.0015888 deg.
- Mean linear velocity MAE: 0.000722576 m/s.
- Mean linear velocity RMSE: 0.00111017 m/s.
- Mean angular velocity MAE: 2.26643e-05 rad/s.
- Mean angular velocity RMSE: 3.16186e-05 rad/s.
- Mean final position error: 0.000386622 m.
- Mean maximum position error: 0.00306362 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.0687749%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00939736%.

### Physics + NN

- Mean position MAE: 9.4704e-06 m.
- Trajectory standard deviation of position MAE: 4.25888e-06 m.
- Mean orientation MAE: 1.66891e-05 deg.
- Trajectory standard deviation of orientation MAE: 1.05053e-05 deg.
- Mean orientation MAE in radians: 2.9128e-07 rad.
- Mean position RMSE: 1.42259e-05 m.
- Mean orientation RMSE: 2.92106e-05 deg.
- Mean linear velocity MAE: 1.27679e-05 m/s.
- Mean linear velocity RMSE: 1.6304e-05 m/s.
- Mean angular velocity MAE: 3.8192e-07 rad/s.
- Mean angular velocity RMSE: 5.50824e-07 rad/s.
- Mean final position error: 9.7221e-06 m.
- Mean maximum position error: 4.51182e-05 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.00315103%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.000288247%.

### Hybrid improvement versus physics-only

- Position error reduction: 98.0224%.
- Orientation error reduction: 98.2534%.

## Benchmark: recursive

### Physics only

- Mean position MAE: 0.000618421 m.
- Trajectory standard deviation of position MAE: 0.000314686 m.
- Mean orientation MAE: 0.000937417 deg.
- Trajectory standard deviation of orientation MAE: 0.000257272 deg.
- Mean orientation MAE in radians: 1.6361e-05 rad.
- Mean position RMSE: 0.00113251 m.
- Mean orientation RMSE: 0.00144299 deg.
- Mean linear velocity MAE: 0.000851767 m/s.
- Mean linear velocity RMSE: 0.00127294 m/s.
- Mean angular velocity MAE: 2.04872e-05 rad/s.
- Mean angular velocity RMSE: 2.59961e-05 rad/s.
- Mean final position error: 0.0018357 m.
- Mean maximum position error: 0.00432453 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.0757791%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00619945%.

### Physics + NN

- Mean position MAE: 0.000130021 m.
- Trajectory standard deviation of position MAE: 0.000122058 m.
- Mean orientation MAE: 8.13549e-05 deg.
- Trajectory standard deviation of orientation MAE: 5.51949e-05 deg.
- Mean orientation MAE in radians: 1.41991e-06 rad.
- Mean position RMSE: 0.00025645 m.
- Mean orientation RMSE: 0.000143198 deg.
- Mean linear velocity MAE: 0.000178265 m/s.
- Mean linear velocity RMSE: 0.000284284 m/s.
- Mean angular velocity MAE: 1.98141e-06 rad/s.
- Mean angular velocity RMSE: 2.90049e-06 rad/s.
- Mean final position error: 0.000276841 m.
- Mean maximum position error: 0.00103667 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.0149703%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.000505528%.

### Hybrid improvement versus physics-only

- Position error reduction: 78.9753%.
- Orientation error reduction: 91.3214%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

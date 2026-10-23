# Experiment: Refresh Frequency

## Run: Every 200 steps

- Training seed: 1.

- Requested optimizer updates for source training: 10,000.
- Actual optimizer updates for source training: 10,016.
- Completed source-training epochs: 32.
- Selected checkpoint update: 10,016.
- Trainable parameters: 5,900.
- Source training time: 13.0851 s.

No training or weight updates occurred for this refresh run. The source checkpoint remains fixed.

Source run: `runs/Drone/phase_7/Experiment A - Trajectory Quantity/broad_80/seed_1`.

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

- Mean position MAE: 9.38273e-06 m.
- Trajectory standard deviation of position MAE: 3.69315e-06 m.
- Mean orientation MAE: 1.94751e-05 deg.
- Trajectory standard deviation of orientation MAE: 1.23971e-05 deg.
- Mean orientation MAE in radians: 3.39904e-07 rad.
- Mean position RMSE: 1.41904e-05 m.
- Mean orientation RMSE: 3.57585e-05 deg.
- Mean linear velocity MAE: 1.31065e-05 m/s.
- Mean linear velocity RMSE: 1.69391e-05 m/s.
- Mean angular velocity MAE: 4.49637e-07 rad/s.
- Mean angular velocity RMSE: 6.75944e-07 rad/s.
- Mean final position error: 1.57672e-05 m.
- Mean maximum position error: 5.18868e-05 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.00429835%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00031973%.

### Hybrid improvement versus physics-only

- Position error reduction: 98.0407%.
- Orientation error reduction: 97.9618%.

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

- Mean position MAE: 0.000103562 m.
- Trajectory standard deviation of position MAE: 0.000112317 m.
- Mean orientation MAE: 8.66482e-05 deg.
- Trajectory standard deviation of orientation MAE: 5.90838e-05 deg.
- Mean orientation MAE in radians: 1.5123e-06 rad.
- Mean position RMSE: 0.000206251 m.
- Mean orientation RMSE: 0.000156716 deg.
- Mean linear velocity MAE: 0.000145504 m/s.
- Mean linear velocity RMSE: 0.000234746 m/s.
- Mean angular velocity MAE: 2.08134e-06 rad/s.
- Mean angular velocity RMSE: 3.08893e-06 rad/s.
- Mean final position error: 0.000213909 m.
- Mean maximum position error: 0.000856016 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.0117828%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.000535977%.

### Hybrid improvement versus physics-only

- Position error reduction: 83.2538%.
- Orientation error reduction: 90.7567%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

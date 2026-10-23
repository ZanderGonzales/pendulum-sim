# Experiment: Refresh Frequency

## Run: Every 200 steps

- Training seed: 2.

- Requested optimizer updates for source training: 10,000.
- Actual optimizer updates for source training: 10,016.
- Completed source-training epochs: 32.
- Selected checkpoint update: 9,800.
- Trainable parameters: 5,900.
- Source training time: 12.4214 s.

No training or weight updates occurred for this refresh run. The source checkpoint remains fixed.

Source run: `runs/Drone/phase_7/Experiment A - Trajectory Quantity/broad_80/seed_2`.

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

- Mean position MAE: 1.0045e-05 m.
- Trajectory standard deviation of position MAE: 4.07184e-06 m.
- Mean orientation MAE: 1.94544e-05 deg.
- Trajectory standard deviation of orientation MAE: 1.10058e-05 deg.
- Mean orientation MAE in radians: 3.39544e-07 rad.
- Mean position RMSE: 1.47978e-05 m.
- Mean orientation RMSE: 3.1817e-05 deg.
- Mean linear velocity MAE: 1.33692e-05 m/s.
- Mean linear velocity RMSE: 1.67592e-05 m/s.
- Mean angular velocity MAE: 4.494e-07 rad/s.
- Mean angular velocity RMSE: 6.13672e-07 rad/s.
- Mean final position error: 1.7416e-05 m.
- Mean maximum position error: 4.82882e-05 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.00397442%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.000375383%.

### Hybrid improvement versus physics-only

- Position error reduction: 97.9025%.
- Orientation error reduction: 97.964%.

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

- Mean position MAE: 0.000146547 m.
- Trajectory standard deviation of position MAE: 0.000121427 m.
- Mean orientation MAE: 0.000101487 deg.
- Trajectory standard deviation of orientation MAE: 6.7056e-05 deg.
- Mean orientation MAE in radians: 1.77128e-06 rad.
- Mean position RMSE: 0.000264316 m.
- Mean orientation RMSE: 0.000174081 deg.
- Mean linear velocity MAE: 0.000201255 m/s.
- Mean linear velocity RMSE: 0.000298501 m/s.
- Mean angular velocity MAE: 2.53387e-06 rad/s.
- Mean angular velocity RMSE: 3.69453e-06 rad/s.
- Mean final position error: 0.000425709 m.
- Mean maximum position error: 0.00101657 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.0170809%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.000634204%.

### Hybrid improvement versus physics-only

- Position error reduction: 76.3031%.
- Orientation error reduction: 89.1738%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

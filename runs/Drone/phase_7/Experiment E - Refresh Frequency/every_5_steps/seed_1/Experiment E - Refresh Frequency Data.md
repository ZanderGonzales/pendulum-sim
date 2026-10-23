# Experiment: Refresh Frequency

## Run: Every 5 steps

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

- Mean position MAE: 4.61582e-07 m.
- Trajectory standard deviation of position MAE: 3.11082e-07 m.
- Mean orientation MAE: 7.843e-07 deg.
- Trajectory standard deviation of orientation MAE: 6.45787e-07 deg.
- Mean orientation MAE in radians: 1.36886e-08 rad.
- Mean position RMSE: 8.85877e-07 m.
- Mean orientation RMSE: 1.43268e-06 deg.
- Mean linear velocity MAE: 2.51753e-05 m/s.
- Mean linear velocity RMSE: 4.19917e-05 m/s.
- Mean angular velocity MAE: 7.4646e-07 rad/s.
- Mean angular velocity RMSE: 1.18506e-06 rad/s.
- Mean final position error: 4.62601e-09 m.
- Mean maximum position error: 3.99778e-06 m.
- Position MAE as a percentage of MuJoCo distance traveled: 6.28772e-05%.
- Orientation MAE as a percentage of MuJoCo angular travel: 6.208e-06%.

### Physics + NN

- Mean position MAE: 9.4018e-09 m.
- Trajectory standard deviation of position MAE: 3.81707e-09 m.
- Mean orientation MAE: 1.53683e-08 deg.
- Trajectory standard deviation of orientation MAE: 7.35387e-09 deg.
- Mean orientation MAE in radians: 2.68227e-10 rad.
- Mean position RMSE: 1.65919e-08 m.
- Mean orientation RMSE: 3.67607e-08 deg.
- Mean linear velocity MAE: 5.11384e-07 m/s.
- Mean linear velocity RMSE: 7.77815e-07 m/s.
- Mean angular velocity MAE: 1.46412e-08 rad/s.
- Mean angular velocity RMSE: 3.03127e-08 rad/s.
- Mean final position error: 6.35282e-09 m.
- Mean maximum position error: 1.54419e-07 m.
- Position MAE as a percentage of MuJoCo distance traveled: 3.77915e-06%.
- Orientation MAE as a percentage of MuJoCo angular travel: 2.49939e-07%.

### Hybrid improvement versus physics-only

- Position error reduction: 97.9631%.
- Orientation error reduction: 98.0405%.

## Benchmark: recursive

### Physics only

- Mean position MAE: 4.72688e-07 m.
- Trajectory standard deviation of position MAE: 2.09246e-07 m.
- Mean orientation MAE: 9.82776e-07 deg.
- Trajectory standard deviation of orientation MAE: 2.70099e-07 deg.
- Mean orientation MAE in radians: 1.71527e-08 rad.
- Mean position RMSE: 9.20809e-07 m.
- Mean orientation RMSE: 1.56676e-06 deg.
- Mean linear velocity MAE: 2.57815e-05 m/s.
- Mean linear velocity RMSE: 4.36472e-05 m/s.
- Mean angular velocity MAE: 9.36008e-07 rad/s.
- Mean angular velocity RMSE: 1.29638e-06 rad/s.
- Mean final position error: 2.88312e-08 m.
- Mean maximum position error: 5.03878e-06 m.
- Position MAE as a percentage of MuJoCo distance traveled: 5.86556e-05%.
- Orientation MAE as a percentage of MuJoCo angular travel: 6.4907e-06%.

### Physics + NN

- Mean position MAE: 9.11184e-08 m.
- Trajectory standard deviation of position MAE: 7.35924e-08 m.
- Mean orientation MAE: 8.10083e-08 deg.
- Trajectory standard deviation of orientation MAE: 4.68989e-08 deg.
- Mean orientation MAE in radians: 1.41386e-09 rad.
- Mean position RMSE: 1.86743e-07 m.
- Mean orientation RMSE: 1.47744e-07 deg.
- Mean linear velocity MAE: 4.96742e-06 m/s.
- Mean linear velocity RMSE: 8.83566e-06 m/s.
- Mean angular velocity MAE: 7.69963e-08 rad/s.
- Mean angular velocity RMSE: 1.21972e-07 rad/s.
- Mean final position error: 3.54357e-08 m.
- Mean maximum position error: 1.21126e-06 m.
- Position MAE as a percentage of MuJoCo distance traveled: 1.08331e-05%.
- Orientation MAE as a percentage of MuJoCo angular travel: 5.11976e-07%.

### Hybrid improvement versus physics-only

- Position error reduction: 80.7233%.
- Orientation error reduction: 91.7572%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

# Experiment: Refresh Frequency

## Run: Every 1 steps

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

- Mean position MAE: 4.19604e-08 m.
- Trajectory standard deviation of position MAE: 2.8284e-08 m.
- Mean orientation MAE: 7.12851e-08 deg.
- Trajectory standard deviation of orientation MAE: 5.87212e-08 deg.
- Mean orientation MAE in radians: 1.24416e-09 rad.
- Mean position RMSE: 6.33157e-08 m.
- Mean orientation RMSE: 1.02433e-07 deg.
- Mean linear velocity MAE: 8.3919e-06 m/s.
- Mean linear velocity RMSE: 1.2663e-05 m/s.
- Mean angular velocity MAE: 2.48805e-07 rad/s.
- Mean angular velocity RMSE: 3.57541e-07 rad/s.
- Mean final position error: 1.76875e-10 m.
- Mean maximum position error: 1.60043e-07 m.
- Position MAE as a percentage of MuJoCo distance traveled: 5.71351e-06%.
- Orientation MAE as a percentage of MuJoCo angular travel: 5.63836e-07%.

### Physics + NN

- Mean position MAE: 9.42911e-10 m.
- Trajectory standard deviation of position MAE: 4.17316e-10 m.
- Mean orientation MAE: 1.45925e-09 deg.
- Trajectory standard deviation of orientation MAE: 6.30905e-10 deg.
- Mean orientation MAE in radians: 2.54687e-11 rad.
- Mean position RMSE: 1.35166e-09 m.
- Mean orientation RMSE: 2.40346e-09 deg.
- Mean linear velocity MAE: 1.90522e-07 m/s.
- Mean linear velocity RMSE: 2.7978e-07 m/s.
- Mean angular velocity MAE: 5.16404e-09 rad/s.
- Mean angular velocity RMSE: 8.69164e-09 rad/s.
- Mean final position error: 3.4725e-10 m.
- Mean maximum position error: 7.63459e-09 m.
- Position MAE as a percentage of MuJoCo distance traveled: 3.39736e-07%.
- Orientation MAE as a percentage of MuJoCo angular travel: 2.50006e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 97.7529%.
- Orientation error reduction: 97.9529%.

## Benchmark: recursive

### Physics only

- Mean position MAE: 4.29713e-08 m.
- Trajectory standard deviation of position MAE: 1.90215e-08 m.
- Mean orientation MAE: 8.94808e-08 deg.
- Trajectory standard deviation of orientation MAE: 2.46233e-08 deg.
- Mean orientation MAE in radians: 1.56173e-09 rad.
- Mean position RMSE: 6.58199e-08 m.
- Mean orientation RMSE: 1.12129e-07 deg.
- Mean linear velocity MAE: 8.59415e-06 m/s.
- Mean linear velocity RMSE: 1.31639e-05 m/s.
- Mean angular velocity MAE: 3.12391e-07 rad/s.
- Mean angular velocity RMSE: 3.91433e-07 rad/s.
- Mean final position error: 1.67331e-09 m.
- Mean maximum position error: 2.01678e-07 m.
- Position MAE as a percentage of MuJoCo distance traveled: 5.33231e-06%.
- Orientation MAE as a percentage of MuJoCo angular travel: 5.90909e-07%.

### Physics + NN

- Mean position MAE: 1.11804e-08 m.
- Trajectory standard deviation of position MAE: 7.96546e-09 m.
- Mean orientation MAE: 9.54695e-09 deg.
- Trajectory standard deviation of orientation MAE: 5.0298e-09 deg.
- Mean orientation MAE in radians: 1.66626e-10 rad.
- Mean position RMSE: 1.69677e-08 m.
- Mean orientation RMSE: 1.38145e-08 deg.
- Mean linear velocity MAE: 2.19215e-06 m/s.
- Mean linear velocity RMSE: 3.32695e-06 m/s.
- Mean angular velocity MAE: 3.2217e-08 rad/s.
- Mean angular velocity RMSE: 4.68189e-08 rad/s.
- Mean final position error: 1.52032e-09 m.
- Mean maximum position error: 5.46175e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 1.32827e-06%.
- Orientation MAE as a percentage of MuJoCo angular travel: 6.0516e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 73.9817%.
- Orientation error reduction: 89.3307%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

# Experiment: Refresh Frequency

## Run: Every 1 steps

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

- Mean position MAE: 8.79553e-10 m.
- Trajectory standard deviation of position MAE: 3.68703e-10 m.
- Mean orientation MAE: 1.4261e-09 deg.
- Trajectory standard deviation of orientation MAE: 6.58956e-10 deg.
- Mean orientation MAE in radians: 2.48902e-11 rad.
- Mean position RMSE: 1.23785e-09 m.
- Mean orientation RMSE: 2.64192e-09 deg.
- Mean linear velocity MAE: 1.70409e-07 m/s.
- Mean linear velocity RMSE: 2.35875e-07 m/s.
- Mean angular velocity MAE: 4.86842e-09 rad/s.
- Mean angular velocity RMSE: 9.16601e-09 rad/s.
- Mean final position error: 2.48781e-10 m.
- Mean maximum position error: 7.04642e-09 m.
- Position MAE as a percentage of MuJoCo distance traveled: 3.52929e-07%.
- Orientation MAE as a percentage of MuJoCo angular travel: 2.37076e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 97.9038%.
- Orientation error reduction: 97.9994%.

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

- Mean position MAE: 8.33724e-09 m.
- Trajectory standard deviation of position MAE: 6.83633e-09 m.
- Mean orientation MAE: 7.46099e-09 deg.
- Trajectory standard deviation of orientation MAE: 4.29224e-09 deg.
- Mean orientation MAE in radians: 1.30219e-10 rad.
- Mean position RMSE: 1.3471e-08 m.
- Mean orientation RMSE: 1.07149e-08 deg.
- Mean linear velocity MAE: 1.65746e-06 m/s.
- Mean linear velocity RMSE: 2.66679e-06 m/s.
- Mean angular velocity MAE: 2.56827e-08 rad/s.
- Mean angular velocity RMSE: 3.68226e-08 rad/s.
- Mean final position error: 1.90459e-09 m.
- Mean maximum position error: 4.89643e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 9.87699e-07%.
- Orientation MAE as a percentage of MuJoCo angular travel: 4.72031e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 80.5981%.
- Orientation error reduction: 91.6619%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

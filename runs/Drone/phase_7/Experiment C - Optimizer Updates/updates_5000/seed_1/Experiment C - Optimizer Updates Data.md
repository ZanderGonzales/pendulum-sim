# Experiment: Optimizer Updates

## Run: 5,000 requested optimizer updates

- Training seed: 1.

- Requested optimizer updates for source training: 5,000.
- Actual optimizer updates for source training: 5,008.
- Completed source-training epochs: 16.
- Selected checkpoint update: 4,900.
- Trainable parameters: 5,900.
- Source training time: 7.4764 s.

## Test: recursive

### Physics only

- Mean position MAE: 0.014326 m.
- Trajectory standard deviation of position MAE: 0.00579547 m.
- Mean orientation MAE: 0.00980406 deg.
- Trajectory standard deviation of orientation MAE: 0.00360809 deg.
- Mean orientation MAE in radians: 0.000171113 rad.
- Mean position RMSE: 0.0205988 m.
- Mean orientation RMSE: 0.0114208 deg.
- Mean linear velocity MAE: 0.00548276 m/s.
- Mean linear velocity RMSE: 0.00702697 m/s.
- Mean angular velocity MAE: 5.10332e-05 rad/s.
- Mean angular velocity RMSE: 5.48594e-05 rad/s.
- Mean final position error: 0.0512667 m.
- Mean maximum position error: 0.0512667 m.
- Position MAE as a percentage of MuJoCo distance traveled: 6.73386%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.186432%.

### Physics + NN

- Mean position MAE: 0.000617209 m.
- Trajectory standard deviation of position MAE: 0.000657854 m.
- Mean orientation MAE: 0.000522042 deg.
- Trajectory standard deviation of orientation MAE: 0.000414865 deg.
- Mean orientation MAE in radians: 9.11135e-06 rad.
- Mean position RMSE: 0.000890068 m.
- Mean orientation RMSE: 0.00062771 deg.
- Mean linear velocity MAE: 0.000246061 m/s.
- Mean linear velocity RMSE: 0.000320464 m/s.
- Mean angular velocity MAE: 2.22439e-06 rad/s.
- Mean angular velocity RMSE: 2.34417e-06 rad/s.
- Mean final position error: 0.00228357 m.
- Mean maximum position error: 0.00228357 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.235973%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.01106%.

### Hybrid improvement versus physics-only

- Position error reduction: 95.6917%.
- Orientation error reduction: 94.6752%.

## Test: one step

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

- Mean position MAE: 1.73135e-09 m.
- Trajectory standard deviation of position MAE: 7.87659e-10 m.
- Mean orientation MAE: 2.08001e-09 deg.
- Trajectory standard deviation of orientation MAE: 8.92112e-10 deg.
- Mean orientation MAE in radians: 3.63031e-11 rad.
- Mean position RMSE: 2.40569e-09 m.
- Mean orientation RMSE: 3.61202e-09 deg.
- Mean linear velocity MAE: 3.32997e-07 m/s.
- Mean linear velocity RMSE: 4.70411e-07 m/s.
- Mean angular velocity MAE: 7.19262e-09 rad/s.
- Mean angular velocity RMSE: 1.24618e-08 rad/s.
- Mean final position error: 3.94243e-10 m.
- Mean maximum position error: 1.24677e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 5.42873e-07%.
- Orientation MAE as a percentage of MuJoCo angular travel: 3.51426e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 95.8738%.
- Orientation error reduction: 97.0821%.

## Benchmark: recursive

### Physics only

- Mean position MAE: 0.0121545 m.
- Trajectory standard deviation of position MAE: 0.00491539 m.
- Mean orientation MAE: 0.00732349 deg.
- Trajectory standard deviation of orientation MAE: 0.00280852 deg.
- Mean orientation MAE in radians: 0.000127819 rad.
- Mean position RMSE: 0.0173916 m.
- Mean orientation RMSE: 0.00846872 deg.
- Mean linear velocity MAE: 0.00464962 m/s.
- Mean linear velocity RMSE: 0.00594905 m/s.
- Mean angular velocity MAE: 2.90909e-05 rad/s.
- Mean angular velocity RMSE: 3.06901e-05 rad/s.
- Mean final position error: 0.0440691 m.
- Mean maximum position error: 0.0440691 m.
- Position MAE as a percentage of MuJoCo distance traveled: 1.6057%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.0488005%.

### Physics + NN

- Mean position MAE: 0.00164322 m.
- Trajectory standard deviation of position MAE: 0.0012406 m.
- Mean orientation MAE: 0.00111905 deg.
- Trajectory standard deviation of orientation MAE: 0.000597191 deg.
- Mean orientation MAE in radians: 1.95311e-05 rad.
- Mean position RMSE: 0.00225677 m.
- Mean orientation RMSE: 0.001457 deg.
- Mean linear velocity MAE: 0.00062164 m/s.
- Mean linear velocity RMSE: 0.000785165 m/s.
- Mean angular velocity MAE: 6.18598e-06 rad/s.
- Mean angular velocity RMSE: 7.17485e-06 rad/s.
- Mean final position error: 0.00523855 m.
- Mean maximum position error: 0.00526073 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.204693%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00710065%.

### Hybrid improvement versus physics-only

- Position error reduction: 86.4806%.
- Orientation error reduction: 84.7197%.

## Benchmark: one step

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

- Mean position MAE: 1.29853e-08 m.
- Trajectory standard deviation of position MAE: 8.93782e-09 m.
- Mean orientation MAE: 9.26783e-09 deg.
- Trajectory standard deviation of orientation MAE: 4.61571e-09 deg.
- Mean orientation MAE in radians: 1.61754e-10 rad.
- Mean position RMSE: 1.92414e-08 m.
- Mean orientation RMSE: 1.25109e-08 deg.
- Mean linear velocity MAE: 2.5987e-06 m/s.
- Mean linear velocity RMSE: 3.82727e-06 m/s.
- Mean angular velocity MAE: 3.23053e-08 rad/s.
- Mean angular velocity RMSE: 4.29917e-08 rad/s.
- Mean final position error: 2.45593e-09 m.
- Mean maximum position error: 6.57475e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 1.5617e-06%.
- Orientation MAE as a percentage of MuJoCo angular travel: 5.88642e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 69.7815%.
- Orientation error reduction: 89.6427%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

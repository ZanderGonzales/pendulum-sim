# Experiment: Neural Network Size

## Run: 1 hidden layers x 64 neurons

- Training seed: 2.

- Requested optimizer updates for source training: 10,000.
- Actual optimizer updates for source training: 10,016.
- Completed source-training epochs: 32.
- Selected checkpoint update: 10,016.
- Trainable parameters: 1,740.
- Source training time: 8.3505 s.

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

- Mean position MAE: 0.000687749 m.
- Trajectory standard deviation of position MAE: 0.000599697 m.
- Mean orientation MAE: 0.000591388 deg.
- Trajectory standard deviation of orientation MAE: 0.000456096 deg.
- Mean orientation MAE in radians: 1.03217e-05 rad.
- Mean position RMSE: 0.00097571 m.
- Mean orientation RMSE: 0.000707117 deg.
- Mean linear velocity MAE: 0.000261105 m/s.
- Mean linear velocity RMSE: 0.000338424 m/s.
- Mean angular velocity MAE: 2.42647e-06 rad/s.
- Mean angular velocity RMSE: 2.57252e-06 rad/s.
- Mean final position error: 0.00244935 m.
- Mean maximum position error: 0.00244935 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.310543%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.0109155%.

### Hybrid improvement versus physics-only

- Position error reduction: 95.1993%.
- Orientation error reduction: 93.9679%.

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

- Mean position MAE: 2.01086e-09 m.
- Trajectory standard deviation of position MAE: 1.03801e-09 m.
- Mean orientation MAE: 2.52617e-09 deg.
- Trajectory standard deviation of orientation MAE: 1.15028e-09 deg.
- Mean orientation MAE in radians: 4.40899e-11 rad.
- Mean position RMSE: 2.92673e-09 m.
- Mean orientation RMSE: 3.99542e-09 deg.
- Mean linear velocity MAE: 3.98788e-07 m/s.
- Mean linear velocity RMSE: 5.80061e-07 m/s.
- Mean angular velocity MAE: 8.87385e-09 rad/s.
- Mean angular velocity RMSE: 1.41633e-08 rad/s.
- Mean final position error: 6.00065e-10 m.
- Mean maximum position error: 1.56727e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 6.01096e-07%.
- Orientation MAE as a percentage of MuJoCo angular travel: 3.93254e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 95.2077%.
- Orientation error reduction: 96.4562%.

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

- Mean position MAE: 0.00233078 m.
- Trajectory standard deviation of position MAE: 0.00137872 m.
- Mean orientation MAE: 0.00131659 deg.
- Trajectory standard deviation of orientation MAE: 0.000826037 deg.
- Mean orientation MAE in radians: 2.29788e-05 rad.
- Mean position RMSE: 0.00330438 m.
- Mean orientation RMSE: 0.00173284 deg.
- Mean linear velocity MAE: 0.000923675 m/s.
- Mean linear velocity RMSE: 0.00118705 m/s.
- Mean angular velocity MAE: 8.1526e-06 rad/s.
- Mean angular velocity RMSE: 9.81049e-06 rad/s.
- Mean final position error: 0.00780313 m.
- Mean maximum position error: 0.00788787 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.290756%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00810418%.

### Hybrid improvement versus physics-only

- Position error reduction: 80.8237%.
- Orientation error reduction: 82.0224%.

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

- Mean position MAE: 1.65171e-08 m.
- Trajectory standard deviation of position MAE: 8.83068e-09 m.
- Mean orientation MAE: 1.29551e-08 deg.
- Trajectory standard deviation of orientation MAE: 6.85026e-09 deg.
- Mean orientation MAE in radians: 2.26109e-10 rad.
- Mean position RMSE: 2.42952e-08 m.
- Mean orientation RMSE: 1.70884e-08 deg.
- Mean linear velocity MAE: 3.28503e-06 m/s.
- Mean linear velocity RMSE: 4.82462e-06 m/s.
- Mean angular velocity MAE: 4.54741e-08 rad/s.
- Mean angular velocity RMSE: 6.00448e-08 rad/s.
- Mean final position error: 2.80269e-09 m.
- Mean maximum position error: 7.08792e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 2.03508e-06%.
- Orientation MAE as a percentage of MuJoCo angular travel: 8.23441e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 61.5625%.
- Orientation error reduction: 85.5219%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

# Experiment: Trajectory Quantity

## Run: 80 broad trajectories

- Training seed: 0.

- Requested optimizer updates for source training: 10,000.
- Actual optimizer updates for source training: 10,016.
- Completed source-training epochs: 32.
- Selected checkpoint update: 10,016.
- Trainable parameters: 5,900.
- Source training time: 13.3145 s.

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

- Mean position MAE: 0.000401772 m.
- Trajectory standard deviation of position MAE: 0.000418742 m.
- Mean orientation MAE: 0.000290801 deg.
- Trajectory standard deviation of orientation MAE: 0.000309551 deg.
- Mean orientation MAE in radians: 5.07544e-06 rad.
- Mean position RMSE: 0.000576238 m.
- Mean orientation RMSE: 0.000350857 deg.
- Mean linear velocity MAE: 0.00015171 m/s.
- Mean linear velocity RMSE: 0.000194212 m/s.
- Mean angular velocity MAE: 1.2485e-06 rad/s.
- Mean angular velocity RMSE: 1.34977e-06 rad/s.
- Mean final position error: 0.00146568 m.
- Mean maximum position error: 0.00146568 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.158366%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00534212%.

### Hybrid improvement versus physics-only

- Position error reduction: 97.1955%.
- Orientation error reduction: 97.0339%.

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

- Mean position MAE: 8.90396e-10 m.
- Trajectory standard deviation of position MAE: 4.24456e-10 m.
- Mean orientation MAE: 1.3442e-09 deg.
- Trajectory standard deviation of orientation MAE: 6.23974e-10 deg.
- Mean orientation MAE in radians: 2.34607e-11 rad.
- Mean position RMSE: 1.34363e-09 m.
- Mean orientation RMSE: 2.45054e-09 deg.
- Mean linear velocity MAE: 1.75519e-07 m/s.
- Mean linear velocity RMSE: 2.6629e-07 m/s.
- Mean angular velocity MAE: 4.64974e-09 rad/s.
- Mean angular velocity RMSE: 8.64685e-09 rad/s.
- Mean final position error: 1.80813e-10 m.
- Mean maximum position error: 8.14623e-09 m.
- Position MAE as a percentage of MuJoCo distance traveled: 2.90004e-07%.
- Orientation MAE as a percentage of MuJoCo angular travel: 2.18124e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 97.878%.
- Orientation error reduction: 98.1143%.

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

- Mean position MAE: 0.00119401 m.
- Trajectory standard deviation of position MAE: 0.000928269 m.
- Mean orientation MAE: 0.000683165 deg.
- Trajectory standard deviation of orientation MAE: 0.000424805 deg.
- Mean orientation MAE in radians: 1.19235e-05 rad.
- Mean position RMSE: 0.00171727 m.
- Mean orientation RMSE: 0.000903132 deg.
- Mean linear velocity MAE: 0.000489034 m/s.
- Mean linear velocity RMSE: 0.000637278 m/s.
- Mean angular velocity MAE: 4.08977e-06 rad/s.
- Mean angular velocity RMSE: 4.95839e-06 rad/s.
- Mean final position error: 0.00381521 m.
- Mean maximum position error: 0.00397806 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.145746%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00436768%.

### Hybrid improvement versus physics-only

- Position error reduction: 90.1764%.
- Orientation error reduction: 90.6716%.

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

- Mean position MAE: 9.15103e-09 m.
- Trajectory standard deviation of position MAE: 6.7291e-09 m.
- Mean orientation MAE: 7.14534e-09 deg.
- Trajectory standard deviation of orientation MAE: 3.84411e-09 deg.
- Mean orientation MAE in radians: 1.2471e-10 rad.
- Mean position RMSE: 1.50072e-08 m.
- Mean orientation RMSE: 9.96016e-09 deg.
- Mean linear velocity MAE: 1.86436e-06 m/s.
- Mean linear velocity RMSE: 3.03573e-06 m/s.
- Mean angular velocity MAE: 2.50245e-08 rad/s.
- Mean angular velocity RMSE: 3.48453e-08 rad/s.
- Mean final position error: 9.5043e-10 m.
- Mean maximum position error: 5.29721e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 1.08462e-06%.
- Orientation MAE as a percentage of MuJoCo angular travel: 4.54578e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 78.7043%.
- Orientation error reduction: 92.0147%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

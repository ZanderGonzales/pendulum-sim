# Experiment: Trajectory Quantity

## Run: 10 broad trajectories

- Training seed: 1.

- Requested optimizer updates for source training: 10,000.
- Actual optimizer updates for source training: 10,000.
- Completed source-training epochs: 250.
- Selected checkpoint update: 9,900.
- Trainable parameters: 5,900.
- Source training time: 13.4060 s.

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

- Mean position MAE: 0.00269471 m.
- Trajectory standard deviation of position MAE: 0.00204888 m.
- Mean orientation MAE: 0.00218868 deg.
- Trajectory standard deviation of orientation MAE: 0.00163489 deg.
- Mean orientation MAE in radians: 3.81996e-05 rad.
- Mean position RMSE: 0.00393689 m.
- Mean orientation RMSE: 0.00275378 deg.
- Mean linear velocity MAE: 0.00108403 m/s.
- Mean linear velocity RMSE: 0.00142906 m/s.
- Mean angular velocity MAE: 1.01563e-05 rad/s.
- Mean angular velocity RMSE: 1.13773e-05 rad/s.
- Mean final position error: 0.0103329 m.
- Mean maximum position error: 0.0103329 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.674242%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.0294591%.

### Hybrid improvement versus physics-only

- Position error reduction: 81.1901%.
- Orientation error reduction: 77.6758%.

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

- Mean position MAE: 6.45056e-09 m.
- Trajectory standard deviation of position MAE: 6.93313e-09 m.
- Mean orientation MAE: 7.4251e-09 deg.
- Trajectory standard deviation of orientation MAE: 7.05722e-09 deg.
- Mean orientation MAE in radians: 1.29592e-10 rad.
- Mean position RMSE: 1.07086e-08 m.
- Mean orientation RMSE: 1.50142e-08 deg.
- Mean linear velocity MAE: 1.29033e-06 m/s.
- Mean linear velocity RMSE: 2.1478e-06 m/s.
- Mean angular velocity MAE: 2.60737e-08 rad/s.
- Mean angular velocity RMSE: 5.26528e-08 rad/s.
- Mean final position error: 4.28867e-10 m.
- Mean maximum position error: 4.91742e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 1.17511e-06%.
- Orientation MAE as a percentage of MuJoCo angular travel: 7.95302e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 84.627%.
- Orientation error reduction: 89.5839%.

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

- Mean position MAE: 0.00369093 m.
- Trajectory standard deviation of position MAE: 0.002689 m.
- Mean orientation MAE: 0.00256167 deg.
- Trajectory standard deviation of orientation MAE: 0.00139417 deg.
- Mean orientation MAE in radians: 4.47095e-05 rad.
- Mean position RMSE: 0.00526454 m.
- Mean orientation RMSE: 0.00324923 deg.
- Mean linear velocity MAE: 0.00146687 m/s.
- Mean linear velocity RMSE: 0.00190106 m/s.
- Mean angular velocity MAE: 1.32843e-05 rad/s.
- Mean angular velocity RMSE: 1.5022e-05 rad/s.
- Mean final position error: 0.013307 m.
- Mean maximum position error: 0.013307 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.487053%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.0160062%.

### Hybrid improvement versus physics-only

- Position error reduction: 69.6332%.
- Orientation error reduction: 65.0213%.

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

- Mean position MAE: 1.88548e-08 m.
- Trajectory standard deviation of position MAE: 1.10878e-08 m.
- Mean orientation MAE: 2.00918e-08 deg.
- Trajectory standard deviation of orientation MAE: 9.29398e-09 deg.
- Mean orientation MAE in radians: 3.50668e-10 rad.
- Mean position RMSE: 2.73205e-08 m.
- Mean orientation RMSE: 2.82283e-08 deg.
- Mean linear velocity MAE: 3.78816e-06 m/s.
- Mean linear velocity RMSE: 5.48918e-06 m/s.
- Mean angular velocity MAE: 7.13513e-08 rad/s.
- Mean angular velocity RMSE: 9.98337e-08 rad/s.
- Mean final position error: 5.81952e-09 m.
- Mean maximum position error: 9.22162e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 2.32186e-06%.
- Orientation MAE as a percentage of MuJoCo angular travel: 1.28273e-07%.

### Hybrid improvement versus physics-only

- Position error reduction: 56.1223%.
- Orientation error reduction: 77.5463%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

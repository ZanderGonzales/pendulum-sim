# Experiment: Trajectory Variety

## Run: 20 restricted trajectories

- Training seed: 0.

- Requested optimizer updates for source training: 10,000.
- Actual optimizer updates for source training: 10,033.
- Completed source-training epochs: 127.
- Selected checkpoint update: 10,000.
- Trainable parameters: 5,900.
- Source training time: 9.4645 s.

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

- Mean position MAE: 0.00351851 m.
- Trajectory standard deviation of position MAE: 0.00390455 m.
- Mean orientation MAE: 0.00325217 deg.
- Trajectory standard deviation of orientation MAE: 0.00425988 deg.
- Mean orientation MAE in radians: 5.6761e-05 rad.
- Mean position RMSE: 0.00479799 m.
- Mean orientation RMSE: 0.00390257 deg.
- Mean linear velocity MAE: 0.00152926 m/s.
- Mean linear velocity RMSE: 0.00197622 m/s.
- Mean angular velocity MAE: 1.36194e-05 rad/s.
- Mean angular velocity RMSE: 1.43166e-05 rad/s.
- Mean final position error: 0.0125198 m.
- Mean maximum position error: 0.0125198 m.
- Position MAE as a percentage of MuJoCo distance traveled: 1.01192%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.121339%.

### Hybrid improvement versus physics-only

- Position error reduction: 75.4397%.
- Orientation error reduction: 66.8284%.

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

- Mean position MAE: 1.33648e-08 m.
- Trajectory standard deviation of position MAE: 1.89804e-08 m.
- Mean orientation MAE: 1.36009e-08 deg.
- Trajectory standard deviation of orientation MAE: 1.89531e-08 deg.
- Mean orientation MAE in radians: 2.3738e-10 rad.
- Mean position RMSE: 2.04583e-08 m.
- Mean orientation RMSE: 2.19945e-08 deg.
- Mean linear velocity MAE: 2.68267e-06 m/s.
- Mean linear velocity RMSE: 4.11022e-06 m/s.
- Mean angular velocity MAE: 4.53929e-08 rad/s.
- Mean angular velocity RMSE: 7.30732e-08 rad/s.
- Mean final position error: 6.32136e-10 m.
- Mean maximum position error: 7.13354e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 3.18876e-06%.
- Orientation MAE as a percentage of MuJoCo angular travel: 5.21429e-07%.

### Hybrid improvement versus physics-only

- Position error reduction: 68.149%.
- Orientation error reduction: 80.9205%.

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

- Mean position MAE: 0.00664359 m.
- Trajectory standard deviation of position MAE: 0.0021223 m.
- Mean orientation MAE: 0.00773326 deg.
- Trajectory standard deviation of orientation MAE: 0.00352837 deg.
- Mean orientation MAE in radians: 0.000134971 rad.
- Mean position RMSE: 0.00941209 m.
- Mean orientation RMSE: 0.00976277 deg.
- Mean linear velocity MAE: 0.00317661 m/s.
- Mean linear velocity RMSE: 0.00430739 m/s.
- Mean angular velocity MAE: 3.88612e-05 rad/s.
- Mean angular velocity RMSE: 4.25065e-05 rad/s.
- Mean final position error: 0.0255344 m.
- Mean maximum position error: 0.0255344 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.950512%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.0534988%.

### Hybrid improvement versus physics-only

- Position error reduction: 45.3404%.
- Orientation error reduction: -5.59523%.

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

- Mean position MAE: 4.16714e-08 m.
- Trajectory standard deviation of position MAE: 1.85426e-08 m.
- Mean orientation MAE: 5.31786e-08 deg.
- Trajectory standard deviation of orientation MAE: 2.02314e-08 deg.
- Mean orientation MAE in radians: 9.28142e-10 rad.
- Mean position RMSE: 5.38254e-08 m.
- Mean orientation RMSE: 6.9305e-08 deg.
- Mean linear velocity MAE: 8.41069e-06 m/s.
- Mean linear velocity RMSE: 1.08819e-05 m/s.
- Mean angular velocity MAE: 1.82061e-07 rad/s.
- Mean angular velocity RMSE: 2.36775e-07 rad/s.
- Mean final position error: 7.1568e-09 m.
- Mean maximum position error: 1.46334e-07 m.
- Position MAE as a percentage of MuJoCo distance traveled: 5.28872e-06%.
- Orientation MAE as a percentage of MuJoCo angular travel: 3.54754e-07%.

### Hybrid improvement versus physics-only

- Position error reduction: 3.02495%.
- Orientation error reduction: 40.5698%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

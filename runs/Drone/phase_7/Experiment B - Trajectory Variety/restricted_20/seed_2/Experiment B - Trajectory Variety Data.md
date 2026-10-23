# Experiment: Trajectory Variety

## Run: 20 restricted trajectories

- Training seed: 2.

- Requested optimizer updates for source training: 10,000.
- Actual optimizer updates for source training: 10,033.
- Completed source-training epochs: 127.
- Selected checkpoint update: 10,033.
- Trainable parameters: 5,900.
- Source training time: 9.8430 s.

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

- Mean position MAE: 0.00558632 m.
- Trajectory standard deviation of position MAE: 0.00754503 m.
- Mean orientation MAE: 0.00468571 deg.
- Trajectory standard deviation of orientation MAE: 0.00696786 deg.
- Mean orientation MAE in radians: 8.1781e-05 rad.
- Mean position RMSE: 0.00783184 m.
- Mean orientation RMSE: 0.00571049 deg.
- Mean linear velocity MAE: 0.00203833 m/s.
- Mean linear velocity RMSE: 0.00255422 m/s.
- Mean angular velocity MAE: 1.86505e-05 rad/s.
- Mean angular velocity RMSE: 1.9659e-05 rad/s.
- Mean final position error: 0.0192902 m.
- Mean maximum position error: 0.0192902 m.
- Position MAE as a percentage of MuJoCo distance traveled: 1.48658%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.185135%.

### Hybrid improvement versus physics-only

- Position error reduction: 61.0058%.
- Orientation error reduction: 52.2065%.

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

- Mean position MAE: 1.67567e-08 m.
- Trajectory standard deviation of position MAE: 2.28913e-08 m.
- Mean orientation MAE: 1.53531e-08 deg.
- Trajectory standard deviation of orientation MAE: 2.1427e-08 deg.
- Mean orientation MAE in radians: 2.67963e-10 rad.
- Mean position RMSE: 2.43504e-08 m.
- Mean orientation RMSE: 2.31835e-08 deg.
- Mean linear velocity MAE: 3.41771e-06 m/s.
- Mean linear velocity RMSE: 4.97717e-06 m/s.
- Mean angular velocity MAE: 5.33136e-08 rad/s.
- Mean angular velocity RMSE: 8.03962e-08 rad/s.
- Mean final position error: 5.35465e-10 m.
- Mean maximum position error: 6.87334e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 3.80691e-06%.
- Orientation MAE as a percentage of MuJoCo angular travel: 5.85794e-07%.

### Hybrid improvement versus physics-only

- Position error reduction: 60.0654%.
- Orientation error reduction: 78.4624%.

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

- Mean position MAE: 0.00941562 m.
- Trajectory standard deviation of position MAE: 0.00384812 m.
- Mean orientation MAE: 0.00831285 deg.
- Trajectory standard deviation of orientation MAE: 0.00350189 deg.
- Mean orientation MAE in radians: 0.000145087 rad.
- Mean position RMSE: 0.0124076 m.
- Mean orientation RMSE: 0.0103579 deg.
- Mean linear velocity MAE: 0.00318145 m/s.
- Mean linear velocity RMSE: 0.00379273 m/s.
- Mean angular velocity MAE: 4.24321e-05 rad/s.
- Mean angular velocity RMSE: 4.61982e-05 rad/s.
- Mean final position error: 0.0278281 m.
- Mean maximum position error: 0.0278281 m.
- Position MAE as a percentage of MuJoCo distance traveled: 1.36242%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.0572488%.

### Hybrid improvement versus physics-only

- Position error reduction: 22.5337%.
- Orientation error reduction: -13.5094%.

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

- Mean position MAE: 5.48404e-08 m.
- Trajectory standard deviation of position MAE: 2.01328e-08 m.
- Mean orientation MAE: 6.1444e-08 deg.
- Trajectory standard deviation of orientation MAE: 2.17283e-08 deg.
- Mean orientation MAE in radians: 1.0724e-09 rad.
- Mean position RMSE: 7.29128e-08 m.
- Mean orientation RMSE: 7.55542e-08 deg.
- Mean linear velocity MAE: 1.12561e-05 m/s.
- Mean linear velocity RMSE: 1.49242e-05 m/s.
- Mean angular velocity MAE: 2.12035e-07 rad/s.
- Mean angular velocity RMSE: 2.62188e-07 rad/s.
- Mean final position error: 8.19278e-09 m.
- Mean maximum position error: 2.04643e-07 m.
- Position MAE as a percentage of MuJoCo distance traveled: 7.13872e-06%.
- Orientation MAE as a percentage of MuJoCo angular travel: 4.1718e-07%.

### Hybrid improvement versus physics-only

- Position error reduction: -27.6209%.
- Orientation error reduction: 31.3328%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

# Experiment: Optimizer Updates

## Run: 5,000 requested optimizer updates

- Training seed: 0.

- Requested optimizer updates for source training: 5,000.
- Actual optimizer updates for source training: 5,008.
- Completed source-training epochs: 16.
- Selected checkpoint update: 4,800.
- Trainable parameters: 5,900.
- Source training time: 7.0837 s.

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

- Mean position MAE: 0.000582118 m.
- Trajectory standard deviation of position MAE: 0.000515677 m.
- Mean orientation MAE: 0.000485355 deg.
- Trajectory standard deviation of orientation MAE: 0.000440507 deg.
- Mean orientation MAE in radians: 8.47103e-06 rad.
- Mean position RMSE: 0.000837174 m.
- Mean orientation RMSE: 0.000588298 deg.
- Mean linear velocity MAE: 0.000230998 m/s.
- Mean linear velocity RMSE: 0.000302515 m/s.
- Mean angular velocity MAE: 2.06014e-06 rad/s.
- Mean angular velocity RMSE: 2.16443e-06 rad/s.
- Mean final position error: 0.00212351 m.
- Mean maximum position error: 0.00212351 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.255291%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00904421%.

### Hybrid improvement versus physics-only

- Position error reduction: 95.9366%.
- Orientation error reduction: 95.0495%.

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

- Mean position MAE: 1.74255e-09 m.
- Trajectory standard deviation of position MAE: 8.15878e-10 m.
- Mean orientation MAE: 1.93111e-09 deg.
- Trajectory standard deviation of orientation MAE: 9.43539e-10 deg.
- Mean orientation MAE in radians: 3.37042e-11 rad.
- Mean position RMSE: 2.40968e-09 m.
- Mean orientation RMSE: 3.51845e-09 deg.
- Mean linear velocity MAE: 3.64743e-07 m/s.
- Mean linear velocity RMSE: 4.95973e-07 m/s.
- Mean angular velocity MAE: 6.62296e-09 rad/s.
- Mean angular velocity RMSE: 1.23379e-08 rad/s.
- Mean final position error: 5.96197e-10 m.
- Mean maximum position error: 1.27066e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 6.04609e-07%.
- Orientation MAE as a percentage of MuJoCo angular travel: 2.93748e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 95.8472%.
- Orientation error reduction: 97.291%.

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

- Mean position MAE: 0.00175447 m.
- Trajectory standard deviation of position MAE: 0.00113633 m.
- Mean orientation MAE: 0.00074604 deg.
- Trajectory standard deviation of orientation MAE: 0.000476606 deg.
- Mean orientation MAE in radians: 1.30209e-05 rad.
- Mean position RMSE: 0.00246247 m.
- Mean orientation RMSE: 0.000955957 deg.
- Mean linear velocity MAE: 0.000663733 m/s.
- Mean linear velocity RMSE: 0.000850249 m/s.
- Mean angular velocity MAE: 4.57713e-06 rad/s.
- Mean angular velocity RMSE: 5.30487e-06 rad/s.
- Mean final position error: 0.00544392 m.
- Mean maximum position error: 0.00562553 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.222874%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00469725%.

### Hybrid improvement versus physics-only

- Position error reduction: 85.5653%.
- Orientation error reduction: 89.8131%.

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

- Mean position MAE: 1.25982e-08 m.
- Trajectory standard deviation of position MAE: 8.01796e-09 m.
- Mean orientation MAE: 9.00245e-09 deg.
- Trajectory standard deviation of orientation MAE: 4.39459e-09 deg.
- Mean orientation MAE in radians: 1.57122e-10 rad.
- Mean position RMSE: 1.90223e-08 m.
- Mean orientation RMSE: 1.21033e-08 deg.
- Mean linear velocity MAE: 2.52887e-06 m/s.
- Mean linear velocity RMSE: 3.81248e-06 m/s.
- Mean angular velocity MAE: 3.13539e-08 rad/s.
- Mean angular velocity RMSE: 4.23485e-08 rad/s.
- Mean final position error: 2.08628e-09 m.
- Mean maximum position error: 6.19864e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 1.51555e-06%.
- Orientation MAE as a percentage of MuJoCo angular travel: 5.72532e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 70.6823%.
- Orientation error reduction: 89.9392%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

# Experiment: Trajectory Quantity

## Run: 20 broad trajectories

- Training seed: 0.

- Requested optimizer updates for source training: 10,000.
- Actual optimizer updates for source training: 10,033.
- Completed source-training epochs: 127.
- Selected checkpoint update: 10,033.
- Trainable parameters: 5,900.
- Source training time: 12.2007 s.

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

- Mean position MAE: 0.0010384 m.
- Trajectory standard deviation of position MAE: 0.00123432 m.
- Mean orientation MAE: 0.0008018 deg.
- Trajectory standard deviation of orientation MAE: 0.000958116 deg.
- Mean orientation MAE in radians: 1.39941e-05 rad.
- Mean position RMSE: 0.00150096 m.
- Mean orientation RMSE: 0.000955067 deg.
- Mean linear velocity MAE: 0.000402799 m/s.
- Mean linear velocity RMSE: 0.000521799 m/s.
- Mean angular velocity MAE: 3.17236e-06 rad/s.
- Mean angular velocity RMSE: 3.31254e-06 rad/s.
- Mean final position error: 0.00384509 m.
- Mean maximum position error: 0.00384509 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.371377%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.0137941%.

### Hybrid improvement versus physics-only

- Position error reduction: 92.7516%.
- Orientation error reduction: 91.8217%.

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

- Mean position MAE: 2.09522e-09 m.
- Trajectory standard deviation of position MAE: 1.32756e-09 m.
- Mean orientation MAE: 2.41059e-09 deg.
- Trajectory standard deviation of orientation MAE: 1.51529e-09 deg.
- Mean orientation MAE in radians: 4.20727e-11 rad.
- Mean position RMSE: 3.60373e-09 m.
- Mean orientation RMSE: 5.44318e-09 deg.
- Mean linear velocity MAE: 4.20812e-07 m/s.
- Mean linear velocity RMSE: 7.21088e-07 m/s.
- Mean angular velocity MAE: 8.38409e-09 rad/s.
- Mean angular velocity RMSE: 1.93032e-08 rad/s.
- Mean final position error: 5.4382e-10 m.
- Mean maximum position error: 2.56283e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 6.75335e-07%.
- Orientation MAE as a percentage of MuJoCo angular travel: 3.53575e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 95.0067%.
- Orientation error reduction: 96.6184%.

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

- Mean position MAE: 0.00185227 m.
- Trajectory standard deviation of position MAE: 0.00152826 m.
- Mean orientation MAE: 0.00127773 deg.
- Trajectory standard deviation of orientation MAE: 0.000800353 deg.
- Mean orientation MAE in radians: 2.23005e-05 rad.
- Mean position RMSE: 0.00262082 m.
- Mean orientation RMSE: 0.00161923 deg.
- Mean linear velocity MAE: 0.000806084 m/s.
- Mean linear velocity RMSE: 0.00104311 m/s.
- Mean angular velocity MAE: 6.79695e-06 rad/s.
- Mean angular velocity RMSE: 7.79933e-06 rad/s.
- Mean final position error: 0.00654856 m.
- Mean maximum position error: 0.00657241 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.231282%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.0083882%.

### Hybrid improvement versus physics-only

- Position error reduction: 84.7606%.
- Orientation error reduction: 82.553%.

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

- Mean position MAE: 1.29975e-08 m.
- Trajectory standard deviation of position MAE: 7.61903e-09 m.
- Mean orientation MAE: 1.03831e-08 deg.
- Trajectory standard deviation of orientation MAE: 4.77272e-09 deg.
- Mean orientation MAE in radians: 1.8122e-10 rad.
- Mean position RMSE: 1.95021e-08 m.
- Mean orientation RMSE: 1.44937e-08 deg.
- Mean linear velocity MAE: 2.58247e-06 m/s.
- Mean linear velocity RMSE: 3.88276e-06 m/s.
- Mean angular velocity MAE: 3.67054e-08 rad/s.
- Mean angular velocity RMSE: 5.10708e-08 rad/s.
- Mean final position error: 3.49156e-09 m.
- Mean maximum position error: 6.48096e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 1.59316e-06%.
- Orientation MAE as a percentage of MuJoCo angular travel: 6.60934e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 69.7531%.
- Orientation error reduction: 88.3962%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

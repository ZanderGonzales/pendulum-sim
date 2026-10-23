# Experiment: Trajectory Quantity

## Run: 40 broad trajectories

- Training seed: 0.

- Requested optimizer updates for source training: 10,000.
- Actual optimizer updates for source training: 10,048.
- Completed source-training epochs: 64.
- Selected checkpoint update: 10,000.
- Trainable parameters: 5,900.
- Source training time: 10.5970 s.

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

- Mean position MAE: 0.000582463 m.
- Trajectory standard deviation of position MAE: 0.000708303 m.
- Mean orientation MAE: 0.000515371 deg.
- Trajectory standard deviation of orientation MAE: 0.000504143 deg.
- Mean orientation MAE in radians: 8.99491e-06 rad.
- Mean position RMSE: 0.000845893 m.
- Mean orientation RMSE: 0.000628906 deg.
- Mean linear velocity MAE: 0.000235543 m/s.
- Mean linear velocity RMSE: 0.000312884 m/s.
- Mean angular velocity MAE: 2.25144e-06 rad/s.
- Mean angular velocity RMSE: 2.39248e-06 rad/s.
- Mean final position error: 0.00222315 m.
- Mean maximum position error: 0.00222315 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.201857%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00843827%.

### Hybrid improvement versus physics-only

- Position error reduction: 95.9342%.
- Orientation error reduction: 94.7433%.

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

- Mean position MAE: 1.25064e-09 m.
- Trajectory standard deviation of position MAE: 5.76442e-10 m.
- Mean orientation MAE: 1.77757e-09 deg.
- Trajectory standard deviation of orientation MAE: 9.14635e-10 deg.
- Mean orientation MAE in radians: 3.10245e-11 rad.
- Mean position RMSE: 1.90349e-09 m.
- Mean orientation RMSE: 3.44079e-09 deg.
- Mean linear velocity MAE: 2.50258e-07 m/s.
- Mean linear velocity RMSE: 3.8366e-07 m/s.
- Mean angular velocity MAE: 6.01732e-09 rad/s.
- Mean angular velocity RMSE: 1.19664e-08 rad/s.
- Mean final position error: 4.01626e-10 m.
- Mean maximum position error: 1.24697e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 4.86975e-07%.
- Orientation MAE as a percentage of MuJoCo angular travel: 2.87886e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 97.0195%.
- Orientation error reduction: 97.5064%.

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

- Mean position MAE: 0.00146765 m.
- Trajectory standard deviation of position MAE: 0.000832011 m.
- Mean orientation MAE: 0.00104232 deg.
- Trajectory standard deviation of orientation MAE: 0.000612424 deg.
- Mean orientation MAE in radians: 1.8192e-05 rad.
- Mean position RMSE: 0.00205641 m.
- Mean orientation RMSE: 0.00139861 deg.
- Mean linear velocity MAE: 0.000617553 m/s.
- Mean linear velocity RMSE: 0.000789739 m/s.
- Mean angular velocity MAE: 5.87513e-06 rad/s.
- Mean angular velocity RMSE: 7.12764e-06 rad/s.
- Mean final position error: 0.00491493 m.
- Mean maximum position error: 0.00492827 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.187396%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00661134%.

### Hybrid improvement versus physics-only

- Position error reduction: 87.925%.
- Orientation error reduction: 85.7674%.

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

- Mean position MAE: 1.14818e-08 m.
- Trajectory standard deviation of position MAE: 7.89347e-09 m.
- Mean orientation MAE: 8.20282e-09 deg.
- Trajectory standard deviation of orientation MAE: 4.24183e-09 deg.
- Mean orientation MAE in radians: 1.43166e-10 rad.
- Mean position RMSE: 1.76218e-08 m.
- Mean orientation RMSE: 1.13754e-08 deg.
- Mean linear velocity MAE: 2.27001e-06 m/s.
- Mean linear velocity RMSE: 3.51478e-06 m/s.
- Mean angular velocity MAE: 2.83826e-08 rad/s.
- Mean angular velocity RMSE: 3.96293e-08 rad/s.
- Mean final position error: 1.82252e-09 m.
- Mean maximum position error: 5.99065e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 1.37996e-06%.
- Orientation MAE as a percentage of MuJoCo angular travel: 5.17459e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 73.2802%.
- Orientation error reduction: 90.8329%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

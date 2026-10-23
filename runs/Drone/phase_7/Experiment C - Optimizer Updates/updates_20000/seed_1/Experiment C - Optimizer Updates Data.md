# Experiment: Optimizer Updates

## Run: 20,000 requested optimizer updates

- Training seed: 1.

- Requested optimizer updates for source training: 20,000.
- Actual optimizer updates for source training: 20,032.
- Completed source-training epochs: 64.
- Selected checkpoint update: 19,700.
- Trainable parameters: 5,900.
- Source training time: 23.9397 s.

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

- Mean position MAE: 0.000279016 m.
- Trajectory standard deviation of position MAE: 0.000377901 m.
- Mean orientation MAE: 0.000231699 deg.
- Trajectory standard deviation of orientation MAE: 0.000279928 deg.
- Mean orientation MAE in radians: 4.04392e-06 rad.
- Mean position RMSE: 0.000404676 m.
- Mean orientation RMSE: 0.000278822 deg.
- Mean linear velocity MAE: 0.000110292 m/s.
- Mean linear velocity RMSE: 0.000144939 m/s.
- Mean angular velocity MAE: 1.0218e-06 rad/s.
- Mean angular velocity RMSE: 1.10069e-06 rad/s.
- Mean final position error: 0.00103649 m.
- Mean maximum position error: 0.00103866 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.0820795%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00400897%.

### Hybrid improvement versus physics-only

- Position error reduction: 98.0524%.
- Orientation error reduction: 97.6367%.

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

- Mean position MAE: 6.07845e-10 m.
- Trajectory standard deviation of position MAE: 2.8831e-10 m.
- Mean orientation MAE: 1.03356e-09 deg.
- Trajectory standard deviation of orientation MAE: 5.53893e-10 deg.
- Mean orientation MAE in radians: 1.8039e-11 rad.
- Mean position RMSE: 8.96245e-10 m.
- Mean orientation RMSE: 1.88453e-09 deg.
- Mean linear velocity MAE: 1.20898e-07 m/s.
- Mean linear velocity RMSE: 1.71131e-07 m/s.
- Mean angular velocity MAE: 3.64018e-09 rad/s.
- Mean angular velocity RMSE: 6.64669e-09 rad/s.
- Mean final position error: 2.33304e-10 m.
- Mean maximum position error: 5.09499e-09 m.
- Position MAE as a percentage of MuJoCo distance traveled: 2.54706e-07%.
- Orientation MAE as a percentage of MuJoCo angular travel: 1.60068e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 98.5514%.
- Orientation error reduction: 98.5501%.

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

- Mean position MAE: 0.000903684 m.
- Trajectory standard deviation of position MAE: 0.000623402 m.
- Mean orientation MAE: 0.000817998 deg.
- Trajectory standard deviation of orientation MAE: 0.00050621 deg.
- Mean orientation MAE in radians: 1.42768e-05 rad.
- Mean position RMSE: 0.00131399 m.
- Mean orientation RMSE: 0.00113608 deg.
- Mean linear velocity MAE: 0.000372995 m/s.
- Mean linear velocity RMSE: 0.000497263 m/s.
- Mean angular velocity MAE: 5.35705e-06 rad/s.
- Mean angular velocity RMSE: 6.54517e-06 rad/s.
- Mean final position error: 0.00328227 m.
- Mean maximum position error: 0.00328227 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.118093%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00549851%.

### Hybrid improvement versus physics-only

- Position error reduction: 92.565%.
- Orientation error reduction: 88.8305%.

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

- Mean position MAE: 6.48056e-09 m.
- Trajectory standard deviation of position MAE: 5.77119e-09 m.
- Mean orientation MAE: 6.61964e-09 deg.
- Trajectory standard deviation of orientation MAE: 3.92547e-09 deg.
- Mean orientation MAE in radians: 1.15535e-10 rad.
- Mean position RMSE: 1.12672e-08 m.
- Mean orientation RMSE: 9.72513e-09 deg.
- Mean linear velocity MAE: 1.28158e-06 m/s.
- Mean linear velocity RMSE: 2.22292e-06 m/s.
- Mean angular velocity MAE: 2.32126e-08 rad/s.
- Mean angular velocity RMSE: 3.40358e-08 rad/s.
- Mean final position error: 9.58796e-10 m.
- Mean maximum position error: 4.36609e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 7.56731e-07%.
- Orientation MAE as a percentage of MuJoCo angular travel: 4.18355e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 84.9189%.
- Orientation error reduction: 92.6022%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

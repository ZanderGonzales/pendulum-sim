# Experiment: Neural Network Size

## Run: 2 hidden layers x 32 neurons

- Training seed: 1.

- Requested optimizer updates for source training: 10,000.
- Actual optimizer updates for source training: 10,016.
- Completed source-training epochs: 32.
- Selected checkpoint update: 10,016.
- Trainable parameters: 1,932.
- Source training time: 10.9767 s.

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

- Mean position MAE: 0.000824123 m.
- Trajectory standard deviation of position MAE: 0.000804175 m.
- Mean orientation MAE: 0.000529141 deg.
- Trajectory standard deviation of orientation MAE: 0.000497888 deg.
- Mean orientation MAE in radians: 9.23525e-06 rad.
- Mean position RMSE: 0.00113605 m.
- Mean orientation RMSE: 0.00064564 deg.
- Mean linear velocity MAE: 0.00029412 m/s.
- Mean linear velocity RMSE: 0.000366915 m/s.
- Mean angular velocity MAE: 2.29699e-06 rad/s.
- Mean angular velocity RMSE: 2.45929e-06 rad/s.
- Mean final position error: 0.00278311 m.
- Mean maximum position error: 0.00278311 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.357172%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.0081%.

### Hybrid improvement versus physics-only

- Position error reduction: 94.2474%.
- Orientation error reduction: 94.6028%.

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

- Mean position MAE: 2.24031e-09 m.
- Trajectory standard deviation of position MAE: 9.69727e-10 m.
- Mean orientation MAE: 2.33174e-09 deg.
- Trajectory standard deviation of orientation MAE: 1.02064e-09 deg.
- Mean orientation MAE in radians: 4.06966e-11 rad.
- Mean position RMSE: 3.03826e-09 m.
- Mean orientation RMSE: 3.98603e-09 deg.
- Mean linear velocity MAE: 4.40646e-07 m/s.
- Mean linear velocity RMSE: 6.00205e-07 m/s.
- Mean angular velocity MAE: 8.08992e-09 rad/s.
- Mean angular velocity RMSE: 1.36573e-08 rad/s.
- Mean final position error: 6.41246e-10 m.
- Mean maximum position error: 1.40495e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 7.35532e-07%.
- Orientation MAE as a percentage of MuJoCo angular travel: 3.61925e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 94.6609%.
- Orientation error reduction: 96.729%.

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

- Mean position MAE: 0.00227272 m.
- Trajectory standard deviation of position MAE: 0.00156159 m.
- Mean orientation MAE: 0.00134491 deg.
- Trajectory standard deviation of orientation MAE: 0.000511905 deg.
- Mean orientation MAE in radians: 2.3473e-05 rad.
- Mean position RMSE: 0.00320391 m.
- Mean orientation RMSE: 0.00179468 deg.
- Mean linear velocity MAE: 0.000895611 m/s.
- Mean linear velocity RMSE: 0.0011435 m/s.
- Mean angular velocity MAE: 8.32182e-06 rad/s.
- Mean angular velocity RMSE: 9.91586e-06 rad/s.
- Mean final position error: 0.00756774 m.
- Mean maximum position error: 0.00757093 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.301041%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00906988%.

### Hybrid improvement versus physics-only

- Position error reduction: 81.3014%.
- Orientation error reduction: 81.6357%.

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

- Mean position MAE: 1.53698e-08 m.
- Trajectory standard deviation of position MAE: 9.0795e-09 m.
- Mean orientation MAE: 1.35896e-08 deg.
- Trajectory standard deviation of orientation MAE: 7.06271e-09 deg.
- Mean orientation MAE in radians: 2.37184e-10 rad.
- Mean position RMSE: 2.18746e-08 m.
- Mean orientation RMSE: 1.81814e-08 deg.
- Mean linear velocity MAE: 3.0793e-06 m/s.
- Mean linear velocity RMSE: 4.37791e-06 m/s.
- Mean angular velocity MAE: 4.80948e-08 rad/s.
- Mean angular velocity RMSE: 6.43943e-08 rad/s.
- Mean final position error: 3.07704e-09 m.
- Mean maximum position error: 6.40736e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 1.89206e-06%.
- Orientation MAE as a percentage of MuJoCo angular travel: 8.63709e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 64.2324%.
- Orientation error reduction: 84.8128%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

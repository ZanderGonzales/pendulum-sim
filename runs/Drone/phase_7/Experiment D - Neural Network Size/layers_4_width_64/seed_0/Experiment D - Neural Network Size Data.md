# Experiment: Neural Network Size

## Run: 4 hidden layers x 64 neurons

- Training seed: 0.

- Requested optimizer updates for source training: 10,000.
- Actual optimizer updates for source training: 10,016.
- Completed source-training epochs: 32.
- Selected checkpoint update: 9,900.
- Trainable parameters: 14,220.
- Source training time: 20.6258 s.

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

- Mean position MAE: 0.000497743 m.
- Trajectory standard deviation of position MAE: 0.000666193 m.
- Mean orientation MAE: 0.000443254 deg.
- Trajectory standard deviation of orientation MAE: 0.000466432 deg.
- Mean orientation MAE in radians: 7.73624e-06 rad.
- Mean position RMSE: 0.000722962 m.
- Mean orientation RMSE: 0.000540041 deg.
- Mean linear velocity MAE: 0.0001949 m/s.
- Mean linear velocity RMSE: 0.000252548 m/s.
- Mean angular velocity MAE: 1.89996e-06 rad/s.
- Mean angular velocity RMSE: 2.01388e-06 rad/s.
- Mean final position error: 0.00186451 m.
- Mean maximum position error: 0.00186451 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.137644%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00716759%.

### Hybrid improvement versus physics-only

- Position error reduction: 96.5256%.
- Orientation error reduction: 95.4789%.

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

- Mean position MAE: 1.12273e-09 m.
- Trajectory standard deviation of position MAE: 4.20726e-10 m.
- Mean orientation MAE: 1.51349e-09 deg.
- Trajectory standard deviation of orientation MAE: 6.95786e-10 deg.
- Mean orientation MAE in radians: 2.64153e-11 rad.
- Mean position RMSE: 1.51479e-09 m.
- Mean orientation RMSE: 2.90492e-09 deg.
- Mean linear velocity MAE: 2.1388e-07 m/s.
- Mean linear velocity RMSE: 2.85586e-07 m/s.
- Mean angular velocity MAE: 5.11026e-09 rad/s.
- Mean angular velocity RMSE: 1.02837e-08 rad/s.
- Mean final position error: 5.47441e-10 m.
- Mean maximum position error: 6.73097e-09 m.
- Position MAE as a percentage of MuJoCo distance traveled: 4.80472e-07%.
- Orientation MAE as a percentage of MuJoCo angular travel: 2.6934e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 97.3243%.
- Orientation error reduction: 97.8769%.

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

- Mean position MAE: 0.00174188 m.
- Trajectory standard deviation of position MAE: 0.000977893 m.
- Mean orientation MAE: 0.00115097 deg.
- Trajectory standard deviation of orientation MAE: 0.000615424 deg.
- Mean orientation MAE in radians: 2.00882e-05 rad.
- Mean position RMSE: 0.00252375 m.
- Mean orientation RMSE: 0.00158472 deg.
- Mean linear velocity MAE: 0.000662938 m/s.
- Mean linear velocity RMSE: 0.000850186 m/s.
- Mean angular velocity MAE: 7.01776e-06 rad/s.
- Mean angular velocity RMSE: 8.5691e-06 rad/s.
- Mean final position error: 0.00597917 m.
- Mean maximum position error: 0.00602973 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.222325%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00773704%.

### Hybrid improvement versus physics-only

- Position error reduction: 85.6688%.
- Orientation error reduction: 84.2839%.

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

- Mean position MAE: 1.0645e-08 m.
- Trajectory standard deviation of position MAE: 7.42124e-09 m.
- Mean orientation MAE: 8.93094e-09 deg.
- Trajectory standard deviation of orientation MAE: 4.92006e-09 deg.
- Mean orientation MAE in radians: 1.55874e-10 rad.
- Mean position RMSE: 1.84375e-08 m.
- Mean orientation RMSE: 1.29657e-08 deg.
- Mean linear velocity MAE: 2.10352e-06 m/s.
- Mean linear velocity RMSE: 3.69513e-06 m/s.
- Mean angular velocity MAE: 2.99102e-08 rad/s.
- Mean angular velocity RMSE: 4.3146e-08 rad/s.
- Mean final position error: 9.49216e-10 m.
- Mean maximum position error: 6.86862e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 1.27683e-06%.
- Orientation MAE as a percentage of MuJoCo angular travel: 5.70619e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 75.2277%.
- Orientation error reduction: 90.0192%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

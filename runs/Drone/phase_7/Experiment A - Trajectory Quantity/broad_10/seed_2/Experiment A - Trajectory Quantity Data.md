# Experiment: Trajectory Quantity

## Run: 10 broad trajectories

- Training seed: 2.

- Requested optimizer updates for source training: 10,000.
- Actual optimizer updates for source training: 10,000.
- Completed source-training epochs: 250.
- Selected checkpoint update: 10,000.
- Trainable parameters: 5,900.
- Source training time: 9.1248 s.

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

- Mean position MAE: 0.00314322 m.
- Trajectory standard deviation of position MAE: 0.00231518 m.
- Mean orientation MAE: 0.0023608 deg.
- Trajectory standard deviation of orientation MAE: 0.00154634 deg.
- Mean orientation MAE in radians: 4.12038e-05 rad.
- Mean position RMSE: 0.00458096 m.
- Mean orientation RMSE: 0.00291364 deg.
- Mean linear velocity MAE: 0.00125306 m/s.
- Mean linear velocity RMSE: 0.00165015 m/s.
- Mean angular velocity MAE: 1.06909e-05 rad/s.
- Mean angular velocity RMSE: 1.18011e-05 rad/s.
- Mean final position error: 0.0120697 m.
- Mean maximum position error: 0.0120697 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.922031%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.0361512%.

### Hybrid improvement versus physics-only

- Position error reduction: 78.0594%.
- Orientation error reduction: 75.9201%.

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

- Mean position MAE: 6.72747e-09 m.
- Trajectory standard deviation of position MAE: 7.50629e-09 m.
- Mean orientation MAE: 7.60214e-09 deg.
- Trajectory standard deviation of orientation MAE: 7.56963e-09 deg.
- Mean orientation MAE in radians: 1.32682e-10 rad.
- Mean position RMSE: 1.13652e-08 m.
- Mean orientation RMSE: 1.61788e-08 deg.
- Mean linear velocity MAE: 1.33647e-06 m/s.
- Mean linear velocity RMSE: 2.26184e-06 m/s.
- Mean angular velocity MAE: 2.66352e-08 rad/s.
- Mean angular velocity RMSE: 5.68708e-08 rad/s.
- Mean final position error: 5.60334e-10 m.
- Mean maximum position error: 5.85102e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 1.26625e-06%.
- Orientation MAE as a percentage of MuJoCo angular travel: 7.76549e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 83.9671%.
- Orientation error reduction: 89.3356%.

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

- Mean position MAE: 0.00440028 m.
- Trajectory standard deviation of position MAE: 0.00348492 m.
- Mean orientation MAE: 0.00319987 deg.
- Trajectory standard deviation of orientation MAE: 0.00251453 deg.
- Mean orientation MAE in radians: 5.58482e-05 rad.
- Mean position RMSE: 0.00629339 m.
- Mean orientation RMSE: 0.00398535 deg.
- Mean linear velocity MAE: 0.0016728 m/s.
- Mean linear velocity RMSE: 0.0021274 m/s.
- Mean angular velocity MAE: 1.53938e-05 rad/s.
- Mean angular velocity RMSE: 1.68259e-05 rad/s.
- Mean final position error: 0.0158768 m.
- Mean maximum position error: 0.0158768 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.584913%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.0197463%.

### Hybrid improvement versus physics-only

- Position error reduction: 63.797%.
- Orientation error reduction: 56.3068%.

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

- Mean position MAE: 1.90223e-08 m.
- Trajectory standard deviation of position MAE: 1.11843e-08 m.
- Mean orientation MAE: 1.997e-08 deg.
- Trajectory standard deviation of orientation MAE: 9.60915e-09 deg.
- Mean orientation MAE in radians: 3.48543e-10 rad.
- Mean position RMSE: 2.59443e-08 m.
- Mean orientation RMSE: 2.64284e-08 deg.
- Mean linear velocity MAE: 3.74708e-06 m/s.
- Mean linear velocity RMSE: 5.1353e-06 m/s.
- Mean angular velocity MAE: 6.89103e-08 rad/s.
- Mean angular velocity RMSE: 9.13343e-08 rad/s.
- Mean final position error: 7.74698e-09 m.
- Mean maximum position error: 8.658e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 2.34022e-06%.
- Orientation MAE as a percentage of MuJoCo angular travel: 1.26531e-07%.

### Hybrid improvement versus physics-only

- Position error reduction: 55.7325%.
- Orientation error reduction: 77.6823%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

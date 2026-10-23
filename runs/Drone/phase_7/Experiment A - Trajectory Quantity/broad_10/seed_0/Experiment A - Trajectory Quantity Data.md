# Experiment: Trajectory Quantity

## Run: 10 broad trajectories

- Training seed: 0.

- Requested optimizer updates for source training: 10,000.
- Actual optimizer updates for source training: 10,000.
- Completed source-training epochs: 250.
- Selected checkpoint update: 10,000.
- Trainable parameters: 5,900.
- Source training time: 17.7002 s.

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

- Mean position MAE: 0.002699 m.
- Trajectory standard deviation of position MAE: 0.0022763 m.
- Mean orientation MAE: 0.00207868 deg.
- Trajectory standard deviation of orientation MAE: 0.00167862 deg.
- Mean orientation MAE in radians: 3.62799e-05 rad.
- Mean position RMSE: 0.00390629 m.
- Mean orientation RMSE: 0.00255244 deg.
- Mean linear velocity MAE: 0.00105845 m/s.
- Mean linear velocity RMSE: 0.00137691 m/s.
- Mean angular velocity MAE: 9.00086e-06 rad/s.
- Mean angular velocity RMSE: 9.94071e-06 rad/s.
- Mean final position error: 0.0101139 m.
- Mean maximum position error: 0.0101139 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.638761%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.0259044%.

### Hybrid improvement versus physics-only

- Position error reduction: 81.1602%.
- Orientation error reduction: 78.7977%.

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

- Mean position MAE: 6.34048e-09 m.
- Trajectory standard deviation of position MAE: 7.00341e-09 m.
- Mean orientation MAE: 6.97447e-09 deg.
- Trajectory standard deviation of orientation MAE: 5.84478e-09 deg.
- Mean orientation MAE in radians: 1.21727e-10 rad.
- Mean position RMSE: 1.09499e-08 m.
- Mean orientation RMSE: 1.40546e-08 deg.
- Mean linear velocity MAE: 1.27641e-06 m/s.
- Mean linear velocity RMSE: 2.21266e-06 m/s.
- Mean angular velocity MAE: 2.47168e-08 rad/s.
- Mean angular velocity RMSE: 4.92583e-08 rad/s.
- Mean final position error: 2.94833e-10 m.
- Mean maximum position error: 4.70234e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 1.11363e-06%.
- Orientation MAE as a percentage of MuJoCo angular travel: 7.714e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 84.8894%.
- Orientation error reduction: 90.2161%.

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

- Mean position MAE: 0.00354391 m.
- Trajectory standard deviation of position MAE: 0.00185906 m.
- Mean orientation MAE: 0.0021347 deg.
- Trajectory standard deviation of orientation MAE: 0.00115466 deg.
- Mean orientation MAE in radians: 3.72576e-05 rad.
- Mean position RMSE: 0.00490905 m.
- Mean orientation RMSE: 0.00269475 deg.
- Mean linear velocity MAE: 0.00128281 m/s.
- Mean linear velocity RMSE: 0.00163187 m/s.
- Mean angular velocity MAE: 1.19109e-05 rad/s.
- Mean angular velocity RMSE: 1.36306e-05 rad/s.
- Mean final position error: 0.0117052 m.
- Mean maximum position error: 0.0117133 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.473681%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.0131565%.

### Hybrid improvement versus physics-only

- Position error reduction: 70.8427%.
- Orientation error reduction: 70.8513%.

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

- Mean position MAE: 1.89188e-08 m.
- Trajectory standard deviation of position MAE: 1.00128e-08 m.
- Mean orientation MAE: 1.86855e-08 deg.
- Trajectory standard deviation of orientation MAE: 8.83438e-09 deg.
- Mean orientation MAE in radians: 3.26124e-10 rad.
- Mean position RMSE: 2.63562e-08 m.
- Mean orientation RMSE: 2.54153e-08 deg.
- Mean linear velocity MAE: 3.76367e-06 m/s.
- Mean linear velocity RMSE: 5.2568e-06 m/s.
- Mean angular velocity MAE: 6.57096e-08 rad/s.
- Mean angular velocity RMSE: 8.89026e-08 rad/s.
- Mean final position error: 4.96613e-09 m.
- Mean maximum position error: 8.30405e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 2.36197e-06%.
- Orientation MAE as a percentage of MuJoCo angular travel: 1.18636e-07%.

### Hybrid improvement versus physics-only

- Position error reduction: 55.9734%.
- Orientation error reduction: 79.1178%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

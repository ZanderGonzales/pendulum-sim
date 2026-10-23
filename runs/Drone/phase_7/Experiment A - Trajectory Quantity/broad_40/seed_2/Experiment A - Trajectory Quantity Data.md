# Experiment: Trajectory Quantity

## Run: 40 broad trajectories

- Training seed: 2.

- Requested optimizer updates for source training: 10,000.
- Actual optimizer updates for source training: 10,048.
- Completed source-training epochs: 64.
- Selected checkpoint update: 10,000.
- Trainable parameters: 5,900.
- Source training time: 11.1440 s.

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

- Mean position MAE: 0.000769253 m.
- Trajectory standard deviation of position MAE: 0.000806815 m.
- Mean orientation MAE: 0.00054536 deg.
- Trajectory standard deviation of orientation MAE: 0.000552514 deg.
- Mean orientation MAE in radians: 9.51833e-06 rad.
- Mean position RMSE: 0.00109526 m.
- Mean orientation RMSE: 0.000642722 deg.
- Mean linear velocity MAE: 0.000289918 m/s.
- Mean linear velocity RMSE: 0.000372835 m/s.
- Mean angular velocity MAE: 2.07296e-06 rad/s.
- Mean angular velocity RMSE: 2.11253e-06 rad/s.
- Mean final position error: 0.00278648 m.
- Mean maximum position error: 0.00278648 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.364789%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00822757%.

### Hybrid improvement versus physics-only

- Position error reduction: 94.6304%.
- Orientation error reduction: 94.4374%.

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

- Mean position MAE: 1.44788e-09 m.
- Trajectory standard deviation of position MAE: 5.96589e-10 m.
- Mean orientation MAE: 1.70307e-09 deg.
- Trajectory standard deviation of orientation MAE: 9.90976e-10 deg.
- Mean orientation MAE in radians: 2.97242e-11 rad.
- Mean position RMSE: 2.30253e-09 m.
- Mean orientation RMSE: 3.66453e-09 deg.
- Mean linear velocity MAE: 2.88612e-07 m/s.
- Mean linear velocity RMSE: 4.56244e-07 m/s.
- Mean angular velocity MAE: 5.83652e-09 rad/s.
- Mean angular velocity RMSE: 1.29051e-08 rad/s.
- Mean final position error: 6.75355e-10 m.
- Mean maximum position error: 1.62002e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 7.17256e-07%.
- Orientation MAE as a percentage of MuJoCo angular travel: 2.44297e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 96.5494%.
- Orientation error reduction: 97.6109%.

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

- Mean position MAE: 0.00177171 m.
- Trajectory standard deviation of position MAE: 0.00144315 m.
- Mean orientation MAE: 0.00132028 deg.
- Trajectory standard deviation of orientation MAE: 0.00107874 deg.
- Mean orientation MAE in radians: 2.30433e-05 rad.
- Mean position RMSE: 0.00258569 m.
- Mean orientation RMSE: 0.0017136 deg.
- Mean linear velocity MAE: 0.000756685 m/s.
- Mean linear velocity RMSE: 0.000995599 m/s.
- Mean angular velocity MAE: 6.90447e-06 rad/s.
- Mean angular velocity RMSE: 7.90774e-06 rad/s.
- Mean final position error: 0.00656149 m.
- Mean maximum position error: 0.0065839 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.215566%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.0081279%.

### Hybrid improvement versus physics-only

- Position error reduction: 85.4234%.
- Orientation error reduction: 81.9719%.

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

- Mean position MAE: 1.19533e-08 m.
- Trajectory standard deviation of position MAE: 7.78758e-09 m.
- Mean orientation MAE: 9.0069e-09 deg.
- Trajectory standard deviation of orientation MAE: 4.50593e-09 deg.
- Mean orientation MAE in radians: 1.572e-10 rad.
- Mean position RMSE: 1.79775e-08 m.
- Mean orientation RMSE: 1.24177e-08 deg.
- Mean linear velocity MAE: 2.38583e-06 m/s.
- Mean linear velocity RMSE: 3.58086e-06 m/s.
- Mean angular velocity MAE: 3.07188e-08 rad/s.
- Mean angular velocity RMSE: 4.26972e-08 rad/s.
- Mean final position error: 2.57794e-09 m.
- Mean maximum position error: 6.17374e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 1.43744e-06%.
- Orientation MAE as a percentage of MuJoCo angular travel: 5.69051e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 72.1831%.
- Orientation error reduction: 89.9343%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

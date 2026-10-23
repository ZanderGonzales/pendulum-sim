# Experiment: Trajectory Quantity

## Run: 20 broad trajectories

- Training seed: 1.

- Requested optimizer updates for source training: 10,000.
- Actual optimizer updates for source training: 10,033.
- Completed source-training epochs: 127.
- Selected checkpoint update: 9,800.
- Trainable parameters: 5,900.
- Source training time: 12.0278 s.

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

- Mean position MAE: 0.00104445 m.
- Trajectory standard deviation of position MAE: 0.00111858 m.
- Mean orientation MAE: 0.000844325 deg.
- Trajectory standard deviation of orientation MAE: 0.000837996 deg.
- Mean orientation MAE in radians: 1.47363e-05 rad.
- Mean position RMSE: 0.00155738 m.
- Mean orientation RMSE: 0.00100493 deg.
- Mean linear velocity MAE: 0.000432086 m/s.
- Mean linear velocity RMSE: 0.000577338 m/s.
- Mean angular velocity MAE: 3.38662e-06 rad/s.
- Mean angular velocity RMSE: 3.52687e-06 rad/s.
- Mean final position error: 0.00412146 m.
- Mean maximum position error: 0.00412146 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.368736%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.0150408%.

### Hybrid improvement versus physics-only

- Position error reduction: 92.7094%.
- Orientation error reduction: 91.388%.

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

- Mean position MAE: 1.73667e-09 m.
- Trajectory standard deviation of position MAE: 8.80493e-10 m.
- Mean orientation MAE: 2.48651e-09 deg.
- Trajectory standard deviation of orientation MAE: 1.46622e-09 deg.
- Mean orientation MAE in radians: 4.33978e-11 rad.
- Mean position RMSE: 3.14974e-09 m.
- Mean orientation RMSE: 5.75105e-09 deg.
- Mean linear velocity MAE: 3.45403e-07 m/s.
- Mean linear velocity RMSE: 6.28041e-07 m/s.
- Mean angular velocity MAE: 8.52726e-09 rad/s.
- Mean angular velocity RMSE: 1.99188e-08 rad/s.
- Mean final position error: 3.83448e-10 m.
- Mean maximum position error: 2.01373e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 6.38162e-07%.
- Orientation MAE as a percentage of MuJoCo angular travel: 3.76579e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 95.8612%.
- Orientation error reduction: 96.5119%.

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

- Mean position MAE: 0.00158115 m.
- Trajectory standard deviation of position MAE: 0.000938236 m.
- Mean orientation MAE: 0.00153547 deg.
- Trajectory standard deviation of orientation MAE: 0.000821661 deg.
- Mean orientation MAE in radians: 2.67991e-05 rad.
- Mean position RMSE: 0.00224656 m.
- Mean orientation RMSE: 0.00193534 deg.
- Mean linear velocity MAE: 0.000734807 m/s.
- Mean linear velocity RMSE: 0.000965253 m/s.
- Mean angular velocity MAE: 7.77579e-06 rad/s.
- Mean angular velocity RMSE: 8.83492e-06 rad/s.
- Mean final position error: 0.00581305 m.
- Mean maximum position error: 0.00581305 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.199143%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.0102012%.

### Hybrid improvement versus physics-only

- Position error reduction: 86.9912%.
- Orientation error reduction: 79.0336%.

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

- Mean position MAE: 1.29238e-08 m.
- Trajectory standard deviation of position MAE: 8.277e-09 m.
- Mean orientation MAE: 1.11448e-08 deg.
- Trajectory standard deviation of orientation MAE: 5.25699e-09 deg.
- Mean orientation MAE in radians: 1.94514e-10 rad.
- Mean position RMSE: 1.89262e-08 m.
- Mean orientation RMSE: 1.54098e-08 deg.
- Mean linear velocity MAE: 2.57311e-06 m/s.
- Mean linear velocity RMSE: 3.75829e-06 m/s.
- Mean angular velocity MAE: 3.8948e-08 rad/s.
- Mean angular velocity RMSE: 5.43754e-08 rad/s.
- Mean final position error: 2.9274e-09 m.
- Mean maximum position error: 6.26131e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 1.57759e-06%.
- Orientation MAE as a percentage of MuJoCo angular travel: 7.12467e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 69.9246%.
- Orientation error reduction: 87.545%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

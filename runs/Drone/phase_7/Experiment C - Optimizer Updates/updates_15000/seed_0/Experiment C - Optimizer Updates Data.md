# Experiment: Optimizer Updates

## Run: 15,000 requested optimizer updates

- Training seed: 0.

- Requested optimizer updates for source training: 15,000.
- Actual optimizer updates for source training: 15,024.
- Completed source-training epochs: 48.
- Selected checkpoint update: 15,024.
- Trainable parameters: 5,900.
- Source training time: 19.4095 s.

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

- Mean position MAE: 0.000320074 m.
- Trajectory standard deviation of position MAE: 0.000376798 m.
- Mean orientation MAE: 0.000256141 deg.
- Trajectory standard deviation of orientation MAE: 0.000313826 deg.
- Mean orientation MAE in radians: 4.47051e-06 rad.
- Mean position RMSE: 0.000463588 m.
- Mean orientation RMSE: 0.00031072 deg.
- Mean linear velocity MAE: 0.000124271 m/s.
- Mean linear velocity RMSE: 0.000161231 m/s.
- Mean angular velocity MAE: 1.12829e-06 rad/s.
- Mean angular velocity RMSE: 1.22007e-06 rad/s.
- Mean final position error: 0.00117691 m.
- Mean maximum position error: 0.00117818 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.103863%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00391242%.

### Hybrid improvement versus physics-only

- Position error reduction: 97.7658%.
- Orientation error reduction: 97.3874%.

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

- Mean position MAE: 7.76055e-10 m.
- Trajectory standard deviation of position MAE: 3.42594e-10 m.
- Mean orientation MAE: 1.08779e-09 deg.
- Trajectory standard deviation of orientation MAE: 6.87599e-10 deg.
- Mean orientation MAE in radians: 1.89856e-11 rad.
- Mean position RMSE: 1.10644e-09 m.
- Mean orientation RMSE: 2.07096e-09 deg.
- Mean linear velocity MAE: 1.51724e-07 m/s.
- Mean linear velocity RMSE: 2.20642e-07 m/s.
- Mean angular velocity MAE: 3.90126e-09 rad/s.
- Mean angular velocity RMSE: 7.39228e-09 rad/s.
- Mean final position error: 2.2477e-10 m.
- Mean maximum position error: 6.38662e-09 m.
- Position MAE as a percentage of MuJoCo distance traveled: 3.12678e-07%.
- Orientation MAE as a percentage of MuJoCo angular travel: 1.37545e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 98.1505%.
- Orientation error reduction: 98.474%.

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

- Mean position MAE: 0.00106874 m.
- Trajectory standard deviation of position MAE: 0.000902558 m.
- Mean orientation MAE: 0.000658234 deg.
- Trajectory standard deviation of orientation MAE: 0.00039612 deg.
- Mean orientation MAE in radians: 1.14884e-05 rad.
- Mean position RMSE: 0.00155599 m.
- Mean orientation RMSE: 0.000878259 deg.
- Mean linear velocity MAE: 0.000462962 m/s.
- Mean linear velocity RMSE: 0.00060716 m/s.
- Mean angular velocity MAE: 3.89549e-06 rad/s.
- Mean angular velocity RMSE: 4.73212e-06 rad/s.
- Mean final position error: 0.00358112 m.
- Mean maximum position error: 0.00368045 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.129629%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00422158%.

### Hybrid improvement versus physics-only

- Position error reduction: 91.207%.
- Orientation error reduction: 91.012%.

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

- Mean position MAE: 8.23915e-09 m.
- Trajectory standard deviation of position MAE: 6.32075e-09 m.
- Mean orientation MAE: 6.45535e-09 deg.
- Trajectory standard deviation of orientation MAE: 3.57158e-09 deg.
- Mean orientation MAE in radians: 1.12667e-10 rad.
- Mean position RMSE: 1.40366e-08 m.
- Mean orientation RMSE: 9.14203e-09 deg.
- Mean linear velocity MAE: 1.66751e-06 m/s.
- Mean linear velocity RMSE: 2.82262e-06 m/s.
- Mean angular velocity MAE: 2.23612e-08 rad/s.
- Mean angular velocity RMSE: 3.1719e-08 rad/s.
- Mean final position error: 1.08877e-09 m.
- Mean maximum position error: 5.04806e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 9.72078e-07%.
- Orientation MAE as a percentage of MuJoCo angular travel: 4.10122e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 80.8264%.
- Orientation error reduction: 92.7858%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

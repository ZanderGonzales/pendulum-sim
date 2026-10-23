# Experiment: Optimizer Updates

## Run: 20,000 requested optimizer updates

- Training seed: 2.

- Requested optimizer updates for source training: 20,000.
- Actual optimizer updates for source training: 20,032.
- Completed source-training epochs: 64.
- Selected checkpoint update: 19,800.
- Trainable parameters: 5,900.
- Source training time: 25.0690 s.

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

- Mean position MAE: 0.000304694 m.
- Trajectory standard deviation of position MAE: 0.000328554 m.
- Mean orientation MAE: 0.000202869 deg.
- Trajectory standard deviation of orientation MAE: 0.000241618 deg.
- Mean orientation MAE in radians: 3.54073e-06 rad.
- Mean position RMSE: 0.000432554 m.
- Mean orientation RMSE: 0.000244371 deg.
- Mean linear velocity MAE: 0.00011265 m/s.
- Mean linear velocity RMSE: 0.000144174 m/s.
- Mean angular velocity MAE: 8.77106e-07 rad/s.
- Mean angular velocity RMSE: 9.64105e-07 rad/s.
- Mean final position error: 0.00109037 m.
- Mean maximum position error: 0.00109037 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.122459%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00306429%.

### Hybrid improvement versus physics-only

- Position error reduction: 97.8731%.
- Orientation error reduction: 97.9308%.

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

- Mean position MAE: 6.17862e-10 m.
- Trajectory standard deviation of position MAE: 2.50223e-10 m.
- Mean orientation MAE: 9.01312e-10 deg.
- Trajectory standard deviation of orientation MAE: 5.41255e-10 deg.
- Mean orientation MAE in radians: 1.57309e-11 rad.
- Mean position RMSE: 8.9471e-10 m.
- Mean orientation RMSE: 1.69701e-09 deg.
- Mean linear velocity MAE: 1.22751e-07 m/s.
- Mean linear velocity RMSE: 1.81587e-07 m/s.
- Mean angular velocity MAE: 3.17093e-09 rad/s.
- Mean angular velocity RMSE: 5.95289e-09 rad/s.
- Mean final position error: 2.46589e-10 m.
- Mean maximum position error: 5.0854e-09 m.
- Position MAE as a percentage of MuJoCo distance traveled: 2.5965e-07%.
- Orientation MAE as a percentage of MuJoCo angular travel: 1.14845e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 98.5275%.
- Orientation error reduction: 98.7356%.

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

- Mean position MAE: 0.00127267 m.
- Trajectory standard deviation of position MAE: 0.00108898 m.
- Mean orientation MAE: 0.00101404 deg.
- Trajectory standard deviation of orientation MAE: 0.000628901 deg.
- Mean orientation MAE in radians: 1.76983e-05 rad.
- Mean position RMSE: 0.00185602 m.
- Mean orientation RMSE: 0.00140219 deg.
- Mean linear velocity MAE: 0.000549837 m/s.
- Mean linear velocity RMSE: 0.000727169 m/s.
- Mean angular velocity MAE: 5.99195e-06 rad/s.
- Mean angular velocity RMSE: 7.26012e-06 rad/s.
- Mean final position error: 0.00471964 m.
- Mean maximum position error: 0.00472771 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.1515%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00638342%.

### Hybrid improvement versus physics-only

- Position error reduction: 89.5292%.
- Orientation error reduction: 86.1536%.

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

- Mean position MAE: 8.37542e-09 m.
- Trajectory standard deviation of position MAE: 6.64089e-09 m.
- Mean orientation MAE: 7.39587e-09 deg.
- Trajectory standard deviation of orientation MAE: 3.77796e-09 deg.
- Mean orientation MAE in radians: 1.29082e-10 rad.
- Mean position RMSE: 1.35845e-08 m.
- Mean orientation RMSE: 1.11513e-08 deg.
- Mean linear velocity MAE: 1.64074e-06 m/s.
- Mean linear velocity RMSE: 2.66369e-06 m/s.
- Mean angular velocity MAE: 2.48725e-08 rad/s.
- Mean angular velocity RMSE: 3.75984e-08 rad/s.
- Mean final position error: 7.94934e-10 m.
- Mean maximum position error: 4.51382e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 9.81302e-07%.
- Orientation MAE as a percentage of MuJoCo angular travel: 4.71738e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 80.5093%.
- Orientation error reduction: 91.7347%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

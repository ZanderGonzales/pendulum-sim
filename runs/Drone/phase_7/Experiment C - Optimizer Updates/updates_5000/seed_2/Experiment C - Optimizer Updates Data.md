# Experiment: Optimizer Updates

## Run: 5,000 requested optimizer updates

- Training seed: 2.

- Requested optimizer updates for source training: 5,000.
- Actual optimizer updates for source training: 5,008.
- Completed source-training epochs: 16.
- Selected checkpoint update: 5,000.
- Trainable parameters: 5,900.
- Source training time: 6.3296 s.

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

- Mean position MAE: 0.000549319 m.
- Trajectory standard deviation of position MAE: 0.000420765 m.
- Mean orientation MAE: 0.00042757 deg.
- Trajectory standard deviation of orientation MAE: 0.000340127 deg.
- Mean orientation MAE in radians: 7.4625e-06 rad.
- Mean position RMSE: 0.00077586 m.
- Mean orientation RMSE: 0.00051879 deg.
- Mean linear velocity MAE: 0.00020216 m/s.
- Mean linear velocity RMSE: 0.000254759 m/s.
- Mean angular velocity MAE: 1.8682e-06 rad/s.
- Mean angular velocity RMSE: 1.96629e-06 rad/s.
- Mean final position error: 0.00193063 m.
- Mean maximum position error: 0.00193063 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.245806%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.0079256%.

### Hybrid improvement versus physics-only

- Position error reduction: 96.1656%.
- Orientation error reduction: 95.6388%.

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

- Mean position MAE: 1.87236e-09 m.
- Trajectory standard deviation of position MAE: 7.37999e-10 m.
- Mean orientation MAE: 2.08335e-09 deg.
- Trajectory standard deviation of orientation MAE: 1.15727e-09 deg.
- Mean orientation MAE in radians: 3.63614e-11 rad.
- Mean position RMSE: 2.43624e-09 m.
- Mean orientation RMSE: 3.39486e-09 deg.
- Mean linear velocity MAE: 3.81101e-07 m/s.
- Mean linear velocity RMSE: 5.01344e-07 m/s.
- Mean angular velocity MAE: 7.22444e-09 rad/s.
- Mean angular velocity RMSE: 1.21235e-08 rad/s.
- Mean final position error: 9.55319e-10 m.
- Mean maximum position error: 1.33387e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 7.67412e-07%.
- Orientation MAE as a percentage of MuJoCo angular travel: 2.89614e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 95.5378%.
- Orientation error reduction: 97.0774%.

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

- Mean position MAE: 0.00194164 m.
- Trajectory standard deviation of position MAE: 0.00123738 m.
- Mean orientation MAE: 0.00136899 deg.
- Trajectory standard deviation of orientation MAE: 0.000719839 deg.
- Mean orientation MAE in radians: 2.38933e-05 rad.
- Mean position RMSE: 0.00276355 m.
- Mean orientation RMSE: 0.00184373 deg.
- Mean linear velocity MAE: 0.000841381 m/s.
- Mean linear velocity RMSE: 0.00109806 m/s.
- Mean angular velocity MAE: 7.80573e-06 rad/s.
- Mean angular velocity RMSE: 9.42244e-06 rad/s.
- Mean final position error: 0.00700913 m.
- Mean maximum position error: 0.00700913 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.242831%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00887591%.

### Hybrid improvement versus physics-only

- Position error reduction: 84.0253%.
- Orientation error reduction: 81.3069%.

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

- Mean position MAE: 1.45657e-08 m.
- Trajectory standard deviation of position MAE: 9.27227e-09 m.
- Mean orientation MAE: 1.13574e-08 deg.
- Trajectory standard deviation of orientation MAE: 5.46669e-09 deg.
- Mean orientation MAE in radians: 1.98223e-10 rad.
- Mean position RMSE: 2.1295e-08 m.
- Mean orientation RMSE: 1.52575e-08 deg.
- Mean linear velocity MAE: 2.88017e-06 m/s.
- Mean linear velocity RMSE: 4.21338e-06 m/s.
- Mean angular velocity MAE: 3.7895e-08 rad/s.
- Mean angular velocity RMSE: 5.1051e-08 rad/s.
- Mean final position error: 2.61649e-09 m.
- Mean maximum position error: 6.85139e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 1.75995e-06%.
- Orientation MAE as a percentage of MuJoCo angular travel: 7.23083e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 66.1037%.
- Orientation error reduction: 87.3075%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

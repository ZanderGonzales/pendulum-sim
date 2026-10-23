# Experiment: Trajectory Quantity

## Run: 80 broad trajectories

- Training seed: 1.

- Requested optimizer updates for source training: 10,000.
- Actual optimizer updates for source training: 10,016.
- Completed source-training epochs: 32.
- Selected checkpoint update: 10,016.
- Trainable parameters: 5,900.
- Source training time: 13.0851 s.

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

- Mean position MAE: 0.00044946 m.
- Trajectory standard deviation of position MAE: 0.000519224 m.
- Mean orientation MAE: 0.00039414 deg.
- Trajectory standard deviation of orientation MAE: 0.000349143 deg.
- Mean orientation MAE in radians: 6.87903e-06 rad.
- Mean position RMSE: 0.000647313 m.
- Mean orientation RMSE: 0.000475224 deg.
- Mean linear velocity MAE: 0.000176074 m/s.
- Mean linear velocity RMSE: 0.000231193 m/s.
- Mean angular velocity MAE: 1.64081e-06 rad/s.
- Mean angular velocity RMSE: 1.73754e-06 rad/s.
- Mean final position error: 0.00166337 m.
- Mean maximum position error: 0.00166337 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.143813%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00726775%.

### Hybrid improvement versus physics-only

- Position error reduction: 96.8626%.
- Orientation error reduction: 95.9798%.

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

- Mean position MAE: 8.79553e-10 m.
- Trajectory standard deviation of position MAE: 3.68703e-10 m.
- Mean orientation MAE: 1.4261e-09 deg.
- Trajectory standard deviation of orientation MAE: 6.58956e-10 deg.
- Mean orientation MAE in radians: 2.48902e-11 rad.
- Mean position RMSE: 1.23785e-09 m.
- Mean orientation RMSE: 2.64192e-09 deg.
- Mean linear velocity MAE: 1.70409e-07 m/s.
- Mean linear velocity RMSE: 2.35875e-07 m/s.
- Mean angular velocity MAE: 4.86842e-09 rad/s.
- Mean angular velocity RMSE: 9.16601e-09 rad/s.
- Mean final position error: 2.48781e-10 m.
- Mean maximum position error: 7.04642e-09 m.
- Position MAE as a percentage of MuJoCo distance traveled: 3.52929e-07%.
- Orientation MAE as a percentage of MuJoCo angular travel: 2.37076e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 97.9038%.
- Orientation error reduction: 97.9994%.

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

- Mean position MAE: 0.000988661 m.
- Trajectory standard deviation of position MAE: 0.000749946 m.
- Mean orientation MAE: 0.00090311 deg.
- Trajectory standard deviation of orientation MAE: 0.00039237 deg.
- Mean orientation MAE in radians: 1.57622e-05 rad.
- Mean position RMSE: 0.00140217 m.
- Mean orientation RMSE: 0.00121819 deg.
- Mean linear velocity MAE: 0.000420524 m/s.
- Mean linear velocity RMSE: 0.000551447 m/s.
- Mean angular velocity MAE: 5.49169e-06 rad/s.
- Mean angular velocity RMSE: 6.55448e-06 rad/s.
- Mean final position error: 0.00344532 m.
- Mean maximum position error: 0.00344532 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.12655%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00607089%.

### Hybrid improvement versus physics-only

- Position error reduction: 91.8659%.
- Orientation error reduction: 87.6683%.

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

- Mean position MAE: 8.33724e-09 m.
- Trajectory standard deviation of position MAE: 6.83633e-09 m.
- Mean orientation MAE: 7.46099e-09 deg.
- Trajectory standard deviation of orientation MAE: 4.29224e-09 deg.
- Mean orientation MAE in radians: 1.30219e-10 rad.
- Mean position RMSE: 1.3471e-08 m.
- Mean orientation RMSE: 1.07149e-08 deg.
- Mean linear velocity MAE: 1.65746e-06 m/s.
- Mean linear velocity RMSE: 2.66679e-06 m/s.
- Mean angular velocity MAE: 2.56827e-08 rad/s.
- Mean angular velocity RMSE: 3.68226e-08 rad/s.
- Mean final position error: 1.90459e-09 m.
- Mean maximum position error: 4.89643e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 9.87699e-07%.
- Orientation MAE as a percentage of MuJoCo angular travel: 4.72031e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 80.5981%.
- Orientation error reduction: 91.6619%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

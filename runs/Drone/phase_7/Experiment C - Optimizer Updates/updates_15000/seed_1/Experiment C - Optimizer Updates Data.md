# Experiment: Optimizer Updates

## Run: 15,000 requested optimizer updates

- Training seed: 1.

- Requested optimizer updates for source training: 15,000.
- Actual optimizer updates for source training: 15,024.
- Completed source-training epochs: 48.
- Selected checkpoint update: 14,500.
- Trainable parameters: 5,900.
- Source training time: 25.9722 s.

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

- Mean position MAE: 0.000355313 m.
- Trajectory standard deviation of position MAE: 0.000415062 m.
- Mean orientation MAE: 0.000340938 deg.
- Trajectory standard deviation of orientation MAE: 0.00032029 deg.
- Mean orientation MAE in radians: 5.95049e-06 rad.
- Mean position RMSE: 0.000528632 m.
- Mean orientation RMSE: 0.000422279 deg.
- Mean linear velocity MAE: 0.000146119 m/s.
- Mean linear velocity RMSE: 0.000196276 m/s.
- Mean angular velocity MAE: 1.58319e-06 rad/s.
- Mean angular velocity RMSE: 1.714e-06 rad/s.
- Mean final position error: 0.00141021 m.
- Mean maximum position error: 0.00141021 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.15221%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00583981%.

### Hybrid improvement versus physics-only

- Position error reduction: 97.5198%.
- Orientation error reduction: 96.5225%.

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

- Mean position MAE: 8.41154e-10 m.
- Trajectory standard deviation of position MAE: 3.90747e-10 m.
- Mean orientation MAE: 1.2868e-09 deg.
- Trajectory standard deviation of orientation MAE: 6.34746e-10 deg.
- Mean orientation MAE in radians: 2.24589e-11 rad.
- Mean position RMSE: 1.14285e-09 m.
- Mean orientation RMSE: 2.18286e-09 deg.
- Mean linear velocity MAE: 1.65305e-07 m/s.
- Mean linear velocity RMSE: 2.19834e-07 m/s.
- Mean angular velocity MAE: 4.74438e-09 rad/s.
- Mean angular velocity RMSE: 7.78497e-09 rad/s.
- Mean final position error: 2.94668e-10 m.
- Mean maximum position error: 5.64342e-09 m.
- Position MAE as a percentage of MuJoCo distance traveled: 3.22975e-07%.
- Orientation MAE as a percentage of MuJoCo angular travel: 2.06903e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 97.9954%.
- Orientation error reduction: 98.1949%.

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

- Mean position MAE: 0.000895068 m.
- Trajectory standard deviation of position MAE: 0.000629591 m.
- Mean orientation MAE: 0.000838223 deg.
- Trajectory standard deviation of orientation MAE: 0.000470623 deg.
- Mean orientation MAE in radians: 1.46298e-05 rad.
- Mean position RMSE: 0.00129134 m.
- Mean orientation RMSE: 0.00115747 deg.
- Mean linear velocity MAE: 0.000387591 m/s.
- Mean linear velocity RMSE: 0.000516725 m/s.
- Mean angular velocity MAE: 5.42323e-06 rad/s.
- Mean angular velocity RMSE: 6.61333e-06 rad/s.
- Mean final position error: 0.00327664 m.
- Mean maximum position error: 0.00327664 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.116824%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00563699%.

### Hybrid improvement versus physics-only

- Position error reduction: 92.6359%.
- Orientation error reduction: 88.5543%.

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

- Mean position MAE: 7.1229e-09 m.
- Trajectory standard deviation of position MAE: 6.19168e-09 m.
- Mean orientation MAE: 6.90523e-09 deg.
- Trajectory standard deviation of orientation MAE: 4.02929e-09 deg.
- Mean orientation MAE in radians: 1.20519e-10 rad.
- Mean position RMSE: 1.20255e-08 m.
- Mean orientation RMSE: 1.00445e-08 deg.
- Mean linear velocity MAE: 1.40985e-06 m/s.
- Mean linear velocity RMSE: 2.36977e-06 m/s.
- Mean angular velocity MAE: 2.41265e-08 rad/s.
- Mean angular velocity RMSE: 3.5052e-08 rad/s.
- Mean final position error: 1.29429e-09 m.
- Mean maximum position error: 4.54999e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 8.37436e-07%.
- Orientation MAE as a percentage of MuJoCo angular travel: 4.36794e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 83.4241%.
- Orientation error reduction: 92.283%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

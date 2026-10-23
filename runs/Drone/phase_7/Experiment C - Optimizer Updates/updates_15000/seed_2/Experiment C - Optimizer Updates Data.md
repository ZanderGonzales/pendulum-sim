# Experiment: Optimizer Updates

## Run: 15,000 requested optimizer updates

- Training seed: 2.

- Requested optimizer updates for source training: 15,000.
- Actual optimizer updates for source training: 15,024.
- Completed source-training epochs: 48.
- Selected checkpoint update: 14,900.
- Trainable parameters: 5,900.
- Source training time: 21.9645 s.

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

- Mean position MAE: 0.000376079 m.
- Trajectory standard deviation of position MAE: 0.000394055 m.
- Mean orientation MAE: 0.000327443 deg.
- Trajectory standard deviation of orientation MAE: 0.000258196 deg.
- Mean orientation MAE in radians: 5.71496e-06 rad.
- Mean position RMSE: 0.000536429 m.
- Mean orientation RMSE: 0.000405393 deg.
- Mean linear velocity MAE: 0.000144897 m/s.
- Mean linear velocity RMSE: 0.000188451 m/s.
- Mean angular velocity MAE: 1.49139e-06 rad/s.
- Mean angular velocity RMSE: 1.60861e-06 rad/s.
- Mean final position error: 0.00137862 m.
- Mean maximum position error: 0.00137862 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.128526%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00562278%.

### Hybrid improvement versus physics-only

- Position error reduction: 97.3749%.
- Orientation error reduction: 96.6601%.

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

- Mean position MAE: 7.9732e-10 m.
- Trajectory standard deviation of position MAE: 3.59999e-10 m.
- Mean orientation MAE: 1.26737e-09 deg.
- Trajectory standard deviation of orientation MAE: 5.53904e-10 deg.
- Mean orientation MAE in radians: 2.21198e-11 rad.
- Mean position RMSE: 1.17144e-09 m.
- Mean orientation RMSE: 2.04862e-09 deg.
- Mean linear velocity MAE: 1.64968e-07 m/s.
- Mean linear velocity RMSE: 2.41386e-07 m/s.
- Mean angular velocity MAE: 4.52737e-09 rad/s.
- Mean angular velocity RMSE: 7.2808e-09 rad/s.
- Mean final position error: 3.13283e-10 m.
- Mean maximum position error: 6.4259e-09 m.
- Position MAE as a percentage of MuJoCo distance traveled: 3.27952e-07%.
- Orientation MAE as a percentage of MuJoCo angular travel: 2.13816e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 98.0998%.
- Orientation error reduction: 98.2221%.

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

- Mean position MAE: 0.00143541 m.
- Trajectory standard deviation of position MAE: 0.00123289 m.
- Mean orientation MAE: 0.00114207 deg.
- Trajectory standard deviation of orientation MAE: 0.000717231 deg.
- Mean orientation MAE in radians: 1.99329e-05 rad.
- Mean position RMSE: 0.00208367 m.
- Mean orientation RMSE: 0.00158486 deg.
- Mean linear velocity MAE: 0.000614404 m/s.
- Mean linear velocity RMSE: 0.000811279 m/s.
- Mean angular velocity MAE: 6.78188e-06 rad/s.
- Mean angular velocity RMSE: 8.24554e-06 rad/s.
- Mean final position error: 0.00530998 m.
- Mean maximum position error: 0.00530998 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.170799%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00712446%.

### Hybrid improvement versus physics-only

- Position error reduction: 88.1903%.
- Orientation error reduction: 84.4054%.

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

- Mean position MAE: 9.28393e-09 m.
- Trajectory standard deviation of position MAE: 7.09211e-09 m.
- Mean orientation MAE: 8.30048e-09 deg.
- Trajectory standard deviation of orientation MAE: 4.28751e-09 deg.
- Mean orientation MAE in radians: 1.44871e-10 rad.
- Mean position RMSE: 1.46104e-08 m.
- Mean orientation RMSE: 1.23713e-08 deg.
- Mean linear velocity MAE: 1.81953e-06 m/s.
- Mean linear velocity RMSE: 2.86667e-06 m/s.
- Mean angular velocity MAE: 2.79319e-08 rad/s.
- Mean angular velocity RMSE: 4.16752e-08 rad/s.
- Mean final position error: 1.10313e-09 m.
- Mean maximum position error: 4.82024e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 1.09317e-06%.
- Orientation MAE as a percentage of MuJoCo angular travel: 5.28402e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 78.395%.
- Orientation error reduction: 90.7237%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

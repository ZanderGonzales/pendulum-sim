# Experiment: Trajectory Variety

## Run: 20 restricted trajectories

- Training seed: 1.

- Requested optimizer updates for source training: 10,000.
- Actual optimizer updates for source training: 10,033.
- Completed source-training epochs: 127.
- Selected checkpoint update: 9,600.
- Trainable parameters: 5,900.
- Source training time: 9.5200 s.

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

- Mean position MAE: 0.00641199 m.
- Trajectory standard deviation of position MAE: 0.0088251 m.
- Mean orientation MAE: 0.00557779 deg.
- Trajectory standard deviation of orientation MAE: 0.00828206 deg.
- Mean orientation MAE in radians: 9.73508e-05 rad.
- Mean position RMSE: 0.00903249 m.
- Mean orientation RMSE: 0.00660755 deg.
- Mean linear velocity MAE: 0.00279043 m/s.
- Mean linear velocity RMSE: 0.00361139 m/s.
- Mean angular velocity MAE: 2.43697e-05 rad/s.
- Mean angular velocity RMSE: 2.55705e-05 rad/s.
- Mean final position error: 0.0240049 m.
- Mean maximum position error: 0.0240049 m.
- Position MAE as a percentage of MuJoCo distance traveled: 1.61469%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.217039%.

### Hybrid improvement versus physics-only

- Position error reduction: 55.2424%.
- Orientation error reduction: 43.1073%.

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

- Mean position MAE: 1.7503e-08 m.
- Trajectory standard deviation of position MAE: 2.54017e-08 m.
- Mean orientation MAE: 2.42597e-08 deg.
- Trajectory standard deviation of orientation MAE: 3.91559e-08 deg.
- Mean orientation MAE in radians: 4.23412e-10 rad.
- Mean position RMSE: 2.48931e-08 m.
- Mean orientation RMSE: 3.74354e-08 deg.
- Mean linear velocity MAE: 3.45112e-06 m/s.
- Mean linear velocity RMSE: 4.91733e-06 m/s.
- Mean angular velocity MAE: 8.22788e-08 rad/s.
- Mean angular velocity RMSE: 1.27517e-07 rad/s.
- Mean final position error: 1.48088e-09 m.
- Mean maximum position error: 7.57044e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 4.45203e-06%.
- Orientation MAE as a percentage of MuJoCo angular travel: 1.00336e-06%.

### Hybrid improvement versus physics-only

- Position error reduction: 58.2869%.
- Orientation error reduction: 65.968%.

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

- Mean position MAE: 0.0131681 m.
- Trajectory standard deviation of position MAE: 0.00666305 m.
- Mean orientation MAE: 0.0108637 deg.
- Trajectory standard deviation of orientation MAE: 0.005157 deg.
- Mean orientation MAE in radians: 0.000189607 rad.
- Mean position RMSE: 0.0175767 m.
- Mean orientation RMSE: 0.013149 deg.
- Mean linear velocity MAE: 0.00463697 m/s.
- Mean linear velocity RMSE: 0.00560327 m/s.
- Mean angular velocity MAE: 6.17116e-05 rad/s.
- Mean angular velocity RMSE: 6.71673e-05 rad/s.
- Mean final position error: 0.0405258 m.
- Mean maximum position error: 0.0405929 m.
- Position MAE as a percentage of MuJoCo distance traveled: 1.96935%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.0807417%.

### Hybrid improvement versus physics-only

- Position error reduction: -8.33973%.
- Orientation error reduction: -48.34%.

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

- Mean position MAE: 6.95717e-08 m.
- Trajectory standard deviation of position MAE: 2.1716e-08 m.
- Mean orientation MAE: 1.0056e-07 deg.
- Trajectory standard deviation of orientation MAE: 3.69457e-08 deg.
- Mean orientation MAE in radians: 1.75511e-09 rad.
- Mean position RMSE: 9.00635e-08 m.
- Mean orientation RMSE: 1.32915e-07 deg.
- Mean linear velocity MAE: 1.35856e-05 m/s.
- Mean linear velocity RMSE: 1.76354e-05 m/s.
- Mean angular velocity MAE: 3.43019e-07 rad/s.
- Mean angular velocity RMSE: 4.53128e-07 rad/s.
- Mean final position error: 7.36051e-09 m.
- Mean maximum position error: 2.11357e-07 m.
- Position MAE as a percentage of MuJoCo distance traveled: 9.20863e-06%.
- Orientation MAE as a percentage of MuJoCo angular travel: 6.84669e-07%.

### Hybrid improvement versus physics-only

- Position error reduction: -61.9027%.
- Orientation error reduction: -12.3821%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

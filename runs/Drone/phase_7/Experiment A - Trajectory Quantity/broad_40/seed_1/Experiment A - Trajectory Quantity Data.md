# Experiment: Trajectory Quantity

## Run: 40 broad trajectories

- Training seed: 1.

- Requested optimizer updates for source training: 10,000.
- Actual optimizer updates for source training: 10,048.
- Completed source-training epochs: 64.
- Selected checkpoint update: 9,900.
- Trainable parameters: 5,900.
- Source training time: 11.3581 s.

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

- Mean position MAE: 0.000662775 m.
- Trajectory standard deviation of position MAE: 0.000717139 m.
- Mean orientation MAE: 0.000521758 deg.
- Trajectory standard deviation of orientation MAE: 0.000566444 deg.
- Mean orientation MAE in radians: 9.1064e-06 rad.
- Mean position RMSE: 0.00097403 m.
- Mean orientation RMSE: 0.000617423 deg.
- Mean linear velocity MAE: 0.00026383 m/s.
- Mean linear velocity RMSE: 0.000348092 m/s.
- Mean angular velocity MAE: 2.03442e-06 rad/s.
- Mean angular velocity RMSE: 2.08867e-06 rad/s.
- Mean final position error: 0.00255621 m.
- Mean maximum position error: 0.00255621 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.283175%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.0071316%.

### Hybrid improvement versus physics-only

- Position error reduction: 95.3736%.
- Orientation error reduction: 94.6781%.

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

- Mean position MAE: 1.09594e-09 m.
- Trajectory standard deviation of position MAE: 4.08074e-10 m.
- Mean orientation MAE: 1.48632e-09 deg.
- Trajectory standard deviation of orientation MAE: 9.55161e-10 deg.
- Mean orientation MAE in radians: 2.59412e-11 rad.
- Mean position RMSE: 1.75285e-09 m.
- Mean orientation RMSE: 3.59104e-09 deg.
- Mean linear velocity MAE: 2.10835e-07 m/s.
- Mean linear velocity RMSE: 3.36842e-07 m/s.
- Mean angular velocity MAE: 5.40413e-09 rad/s.
- Mean angular velocity RMSE: 1.26481e-08 rad/s.
- Mean final position error: 3.75765e-10 m.
- Mean maximum position error: 1.02017e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 4.84776e-07%.
- Orientation MAE as a percentage of MuJoCo angular travel: 1.99943e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 97.3882%.
- Orientation error reduction: 97.915%.

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

- Mean position MAE: 0.00138677 m.
- Trajectory standard deviation of position MAE: 0.00109606 m.
- Mean orientation MAE: 0.0013599 deg.
- Trajectory standard deviation of orientation MAE: 0.000899496 deg.
- Mean orientation MAE in radians: 2.37347e-05 rad.
- Mean position RMSE: 0.0019575 m.
- Mean orientation RMSE: 0.00180265 deg.
- Mean linear velocity MAE: 0.000571021 m/s.
- Mean linear velocity RMSE: 0.00074295 m/s.
- Mean angular velocity MAE: 7.47298e-06 rad/s.
- Mean angular velocity RMSE: 8.8181e-06 rad/s.
- Mean final position error: 0.00478446 m.
- Mean maximum position error: 0.00478446 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.182143%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00861996%.

### Hybrid improvement versus physics-only

- Position error reduction: 88.5905%.
- Orientation error reduction: 81.431%.

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

- Mean position MAE: 1.02052e-08 m.
- Trajectory standard deviation of position MAE: 7.47753e-09 m.
- Mean orientation MAE: 9.68202e-09 deg.
- Trajectory standard deviation of orientation MAE: 5.06666e-09 deg.
- Mean orientation MAE in radians: 1.68983e-10 rad.
- Mean position RMSE: 1.58656e-08 m.
- Mean orientation RMSE: 1.38783e-08 deg.
- Mean linear velocity MAE: 2.00633e-06 m/s.
- Mean linear velocity RMSE: 3.11897e-06 m/s.
- Mean angular velocity MAE: 3.31146e-08 rad/s.
- Mean angular velocity RMSE: 4.75277e-08 rad/s.
- Mean final position error: 1.92219e-09 m.
- Mean maximum position error: 5.58065e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 1.21841e-06%.
- Orientation MAE as a percentage of MuJoCo angular travel: 6.09088e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 76.2511%.
- Orientation error reduction: 89.1798%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

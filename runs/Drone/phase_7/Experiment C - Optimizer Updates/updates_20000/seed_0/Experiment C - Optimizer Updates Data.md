# Experiment: Optimizer Updates

## Run: 20,000 requested optimizer updates

- Training seed: 0.

- Requested optimizer updates for source training: 20,000.
- Actual optimizer updates for source training: 20,032.
- Completed source-training epochs: 64.
- Selected checkpoint update: 20,032.
- Trainable parameters: 5,900.
- Source training time: 30.6880 s.

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

- Mean position MAE: 0.000284956 m.
- Trajectory standard deviation of position MAE: 0.000368592 m.
- Mean orientation MAE: 0.000247183 deg.
- Trajectory standard deviation of orientation MAE: 0.000303741 deg.
- Mean orientation MAE in radians: 4.31415e-06 rad.
- Mean position RMSE: 0.000410678 m.
- Mean orientation RMSE: 0.000300685 deg.
- Mean linear velocity MAE: 0.000112902 m/s.
- Mean linear velocity RMSE: 0.000147749 m/s.
- Mean angular velocity MAE: 1.06831e-06 rad/s.
- Mean angular velocity RMSE: 1.14688e-06 rad/s.
- Mean final position error: 0.00106883 m.
- Mean maximum position error: 0.00106883 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.0881792%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00404151%.

### Hybrid improvement versus physics-only

- Position error reduction: 98.0109%.
- Orientation error reduction: 97.4788%.

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

- Mean position MAE: 6.55761e-10 m.
- Trajectory standard deviation of position MAE: 2.61028e-10 m.
- Mean orientation MAE: 9.78607e-10 deg.
- Trajectory standard deviation of orientation MAE: 5.27244e-10 deg.
- Mean orientation MAE in radians: 1.70799e-11 rad.
- Mean position RMSE: 9.83693e-10 m.
- Mean orientation RMSE: 1.85827e-09 deg.
- Mean linear velocity MAE: 1.31348e-07 m/s.
- Mean linear velocity RMSE: 1.93778e-07 m/s.
- Mean angular velocity MAE: 3.45208e-09 rad/s.
- Mean angular velocity RMSE: 6.67156e-09 rad/s.
- Mean final position error: 2.50295e-10 m.
- Mean maximum position error: 5.86949e-09 m.
- Position MAE as a percentage of MuJoCo distance traveled: 2.87334e-07%.
- Orientation MAE as a percentage of MuJoCo angular travel: 1.4663e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 98.4372%.
- Orientation error reduction: 98.6272%.

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

- Mean position MAE: 0.001023 m.
- Trajectory standard deviation of position MAE: 0.000880417 m.
- Mean orientation MAE: 0.000605751 deg.
- Trajectory standard deviation of orientation MAE: 0.000319686 deg.
- Mean orientation MAE in radians: 1.05724e-05 rad.
- Mean position RMSE: 0.00150224 m.
- Mean orientation RMSE: 0.000830461 deg.
- Mean linear velocity MAE: 0.000435225 m/s.
- Mean linear velocity RMSE: 0.000574417 m/s.
- Mean angular velocity MAE: 3.69324e-06 rad/s.
- Mean angular velocity RMSE: 4.56993e-06 rad/s.
- Mean final position error: 0.00339583 m.
- Mean maximum position error: 0.00354837 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.122991%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00387207%.

### Hybrid improvement versus physics-only

- Position error reduction: 91.5833%.
- Orientation error reduction: 91.7287%.

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

- Mean position MAE: 7.82758e-09 m.
- Trajectory standard deviation of position MAE: 6.16055e-09 m.
- Mean orientation MAE: 6.07156e-09 deg.
- Trajectory standard deviation of orientation MAE: 3.43984e-09 deg.
- Mean orientation MAE in radians: 1.05969e-10 rad.
- Mean position RMSE: 1.36659e-08 m.
- Mean orientation RMSE: 8.69863e-09 deg.
- Mean linear velocity MAE: 1.5806e-06 m/s.
- Mean linear velocity RMSE: 2.74366e-06 m/s.
- Mean angular velocity MAE: 2.09682e-08 rad/s.
- Mean angular velocity RMSE: 3.00883e-08 rad/s.
- Mean final position error: 6.95289e-10 m.
- Mean maximum position error: 5.00296e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 9.19975e-07%.
- Orientation MAE as a percentage of MuJoCo angular travel: 3.85938e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 81.7842%.
- Orientation error reduction: 93.2147%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

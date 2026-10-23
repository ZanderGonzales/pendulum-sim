# Experiment: Neural Network Size

## Run: 4 hidden layers x 64 neurons

- Training seed: 1.

- Requested optimizer updates for source training: 10,000.
- Actual optimizer updates for source training: 10,016.
- Completed source-training epochs: 32.
- Selected checkpoint update: 9,700.
- Trainable parameters: 14,220.
- Source training time: 21.3525 s.

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

- Mean position MAE: 0.000418606 m.
- Trajectory standard deviation of position MAE: 0.000539975 m.
- Mean orientation MAE: 0.000316466 deg.
- Trajectory standard deviation of orientation MAE: 0.000446961 deg.
- Mean orientation MAE in radians: 5.52337e-06 rad.
- Mean position RMSE: 0.000622875 m.
- Mean orientation RMSE: 0.000379256 deg.
- Mean linear velocity MAE: 0.000170553 m/s.
- Mean linear velocity RMSE: 0.000227939 m/s.
- Mean angular velocity MAE: 1.40038e-06 rad/s.
- Mean angular velocity RMSE: 1.47772e-06 rad/s.
- Mean final position error: 0.00164998 m.
- Mean maximum position error: 0.00164998 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.186462%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00492351%.

### Hybrid improvement versus physics-only

- Position error reduction: 97.078%.
- Orientation error reduction: 96.7721%.

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

- Mean position MAE: 1.02452e-09 m.
- Trajectory standard deviation of position MAE: 4.42964e-10 m.
- Mean orientation MAE: 1.44968e-09 deg.
- Trajectory standard deviation of orientation MAE: 7.57793e-10 deg.
- Mean orientation MAE in radians: 2.53016e-11 rad.
- Mean position RMSE: 1.44916e-09 m.
- Mean orientation RMSE: 2.77779e-09 deg.
- Mean linear velocity MAE: 2.05049e-07 m/s.
- Mean linear velocity RMSE: 2.9162e-07 m/s.
- Mean angular velocity MAE: 4.94398e-09 rad/s.
- Mean angular velocity RMSE: 9.69046e-09 rad/s.
- Mean final position error: 3.33114e-10 m.
- Mean maximum position error: 7.48937e-09 m.
- Position MAE as a percentage of MuJoCo distance traveled: 4.3331e-07%.
- Orientation MAE as a percentage of MuJoCo angular travel: 2.34131e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 97.5584%.
- Orientation error reduction: 97.9664%.

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

- Mean position MAE: 0.00148963 m.
- Trajectory standard deviation of position MAE: 0.00131833 m.
- Mean orientation MAE: 0.00135688 deg.
- Trajectory standard deviation of orientation MAE: 0.000806567 deg.
- Mean orientation MAE in radians: 2.36821e-05 rad.
- Mean position RMSE: 0.00222341 m.
- Mean orientation RMSE: 0.00187248 deg.
- Mean linear velocity MAE: 0.000658722 m/s.
- Mean linear velocity RMSE: 0.000900891 m/s.
- Mean angular velocity MAE: 7.94987e-06 rad/s.
- Mean angular velocity RMSE: 9.63862e-06 rad/s.
- Mean final position error: 0.00560388 m.
- Mean maximum position error: 0.00562943 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.179867%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00840815%.

### Hybrid improvement versus physics-only

- Position error reduction: 87.7442%.
- Orientation error reduction: 81.4722%.

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

- Mean position MAE: 1.07053e-08 m.
- Trajectory standard deviation of position MAE: 7.86086e-09 m.
- Mean orientation MAE: 8.85881e-09 deg.
- Trajectory standard deviation of orientation MAE: 4.43085e-09 deg.
- Mean orientation MAE in radians: 1.54615e-10 rad.
- Mean position RMSE: 1.81749e-08 m.
- Mean orientation RMSE: 1.23722e-08 deg.
- Mean linear velocity MAE: 2.12938e-06 m/s.
- Mean linear velocity RMSE: 3.60907e-06 m/s.
- Mean angular velocity MAE: 3.10997e-08 rad/s.
- Mean angular velocity RMSE: 4.41066e-08 rad/s.
- Mean final position error: 9.58941e-10 m.
- Mean maximum position error: 6.69527e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 1.27575e-06%.
- Orientation MAE as a percentage of MuJoCo angular travel: 5.62041e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 75.0872%.
- Orientation error reduction: 90.0998%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

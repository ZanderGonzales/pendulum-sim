# Experiment: Neural Network Size

## Run: 1 hidden layers x 64 neurons

- Training seed: 0.

- Requested optimizer updates for source training: 10,000.
- Actual optimizer updates for source training: 10,016.
- Completed source-training epochs: 32.
- Selected checkpoint update: 9,900.
- Trainable parameters: 1,740.
- Source training time: 8.8371 s.

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

- Mean position MAE: 0.000675094 m.
- Trajectory standard deviation of position MAE: 0.000629981 m.
- Mean orientation MAE: 0.000496026 deg.
- Trajectory standard deviation of orientation MAE: 0.000355186 deg.
- Mean orientation MAE in radians: 8.65728e-06 rad.
- Mean position RMSE: 0.000923962 m.
- Mean orientation RMSE: 0.000610501 deg.
- Mean linear velocity MAE: 0.000237479 m/s.
- Mean linear velocity RMSE: 0.000299439 m/s.
- Mean angular velocity MAE: 2.18665e-06 rad/s.
- Mean angular velocity RMSE: 2.33361e-06 rad/s.
- Mean final position error: 0.00225758 m.
- Mean maximum position error: 0.00225758 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.229177%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00830318%.

### Hybrid improvement versus physics-only

- Position error reduction: 95.2876%.
- Orientation error reduction: 94.9406%.

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

- Mean position MAE: 2.13279e-09 m.
- Trajectory standard deviation of position MAE: 1.0758e-09 m.
- Mean orientation MAE: 2.42463e-09 deg.
- Trajectory standard deviation of orientation MAE: 1.13064e-09 deg.
- Mean orientation MAE in radians: 4.23178e-11 rad.
- Mean position RMSE: 3.17222e-09 m.
- Mean orientation RMSE: 3.70712e-09 deg.
- Mean linear velocity MAE: 4.22944e-07 m/s.
- Mean linear velocity RMSE: 6.34214e-07 m/s.
- Mean angular velocity MAE: 8.45881e-09 rad/s.
- Mean angular velocity RMSE: 1.29137e-08 rad/s.
- Mean final position error: 3.91547e-10 m.
- Mean maximum position error: 1.63116e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 5.99973e-07%.
- Orientation MAE as a percentage of MuJoCo angular travel: 3.87954e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 94.9171%.
- Orientation error reduction: 96.5987%.

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

- Mean position MAE: 0.00207474 m.
- Trajectory standard deviation of position MAE: 0.000995472 m.
- Mean orientation MAE: 0.00117758 deg.
- Trajectory standard deviation of orientation MAE: 0.000785309 deg.
- Mean orientation MAE in radians: 2.05526e-05 rad.
- Mean position RMSE: 0.00285961 m.
- Mean orientation RMSE: 0.00151986 deg.
- Mean linear velocity MAE: 0.000752675 m/s.
- Mean linear velocity RMSE: 0.000925966 m/s.
- Mean angular velocity MAE: 7.077e-06 rad/s.
- Mean angular velocity RMSE: 8.16762e-06 rad/s.
- Mean final position error: 0.0064423 m.
- Mean maximum position error: 0.00646371 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.266595%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00747294%.

### Hybrid improvement versus physics-only

- Position error reduction: 82.9302%.
- Orientation error reduction: 83.9205%.

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

- Mean position MAE: 1.41417e-08 m.
- Trajectory standard deviation of position MAE: 7.49685e-09 m.
- Mean orientation MAE: 1.32582e-08 deg.
- Trajectory standard deviation of orientation MAE: 5.86537e-09 deg.
- Mean orientation MAE in radians: 2.31399e-10 rad.
- Mean position RMSE: 1.98036e-08 m.
- Mean orientation RMSE: 1.69799e-08 deg.
- Mean linear velocity MAE: 2.81945e-06 m/s.
- Mean linear velocity RMSE: 3.96102e-06 m/s.
- Mean angular velocity MAE: 4.52353e-08 rad/s.
- Mean angular velocity RMSE: 5.80286e-08 rad/s.
- Mean final position error: 3.46795e-09 m.
- Mean maximum position error: 6.09689e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 1.73195e-06%.
- Orientation MAE as a percentage of MuJoCo angular travel: 8.61844e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 67.0904%.
- Orientation error reduction: 85.1832%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

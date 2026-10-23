# Experiment: Neural Network Size

## Run: 2 hidden layers x 128 neurons

- Training seed: 2.

- Requested optimizer updates for source training: 10,000.
- Actual optimizer updates for source training: 10,016.
- Completed source-training epochs: 32.
- Selected checkpoint update: 10,000.
- Trainable parameters: 19,980.
- Source training time: 20.9513 s.

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

- Mean position MAE: 0.000326807 m.
- Trajectory standard deviation of position MAE: 0.000386498 m.
- Mean orientation MAE: 0.000319585 deg.
- Trajectory standard deviation of orientation MAE: 0.0002947 deg.
- Mean orientation MAE in radians: 5.57781e-06 rad.
- Mean position RMSE: 0.000478204 m.
- Mean orientation RMSE: 0.000385943 deg.
- Mean linear velocity MAE: 0.000134408 m/s.
- Mean linear velocity RMSE: 0.000178626 m/s.
- Mean angular velocity MAE: 1.36628e-06 rad/s.
- Mean angular velocity RMSE: 1.44897e-06 rad/s.
- Mean final position error: 0.00124645 m.
- Mean maximum position error: 0.00125775 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.1411%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00707056%.

### Hybrid improvement versus physics-only

- Position error reduction: 97.7188%.
- Orientation error reduction: 96.7403%.

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

- Mean position MAE: 8.06171e-10 m.
- Trajectory standard deviation of position MAE: 2.51599e-10 m.
- Mean orientation MAE: 1.1045e-09 deg.
- Trajectory standard deviation of orientation MAE: 4.42233e-10 deg.
- Mean orientation MAE in radians: 1.92771e-11 rad.
- Mean position RMSE: 1.15646e-09 m.
- Mean orientation RMSE: 2.13772e-09 deg.
- Mean linear velocity MAE: 1.69947e-07 m/s.
- Mean linear velocity RMSE: 2.45504e-07 m/s.
- Mean angular velocity MAE: 3.941e-09 rad/s.
- Mean angular velocity RMSE: 7.57469e-09 rad/s.
- Mean final position error: 4.11454e-10 m.
- Mean maximum position error: 7.55939e-09 m.
- Position MAE as a percentage of MuJoCo distance traveled: 4.67062e-07%.
- Orientation MAE as a percentage of MuJoCo angular travel: 2.02214e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 98.0787%.
- Orientation error reduction: 98.4506%.

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

- Mean position MAE: 0.00114765 m.
- Trajectory standard deviation of position MAE: 0.000854038 m.
- Mean orientation MAE: 0.000738362 deg.
- Trajectory standard deviation of orientation MAE: 0.000522492 deg.
- Mean orientation MAE in radians: 1.28868e-05 rad.
- Mean position RMSE: 0.00163084 m.
- Mean orientation RMSE: 0.00100665 deg.
- Mean linear velocity MAE: 0.00046248 m/s.
- Mean linear velocity RMSE: 0.000588858 m/s.
- Mean angular velocity MAE: 4.56567e-06 rad/s.
- Mean angular velocity RMSE: 5.508e-06 rad/s.
- Mean final position error: 0.00389954 m.
- Mean maximum position error: 0.00389954 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.14358%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00463029%.

### Hybrid improvement versus physics-only

- Position error reduction: 90.5578%.
- Orientation error reduction: 89.9179%.

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

- Mean position MAE: 8.79476e-09 m.
- Trajectory standard deviation of position MAE: 6.11551e-09 m.
- Mean orientation MAE: 6.64917e-09 deg.
- Trajectory standard deviation of orientation MAE: 4.02587e-09 deg.
- Mean orientation MAE in radians: 1.1605e-10 rad.
- Mean position RMSE: 1.43768e-08 m.
- Mean orientation RMSE: 8.80385e-09 deg.
- Mean linear velocity MAE: 1.78493e-06 m/s.
- Mean linear velocity RMSE: 2.91496e-06 m/s.
- Mean angular velocity MAE: 2.32133e-08 rad/s.
- Mean angular velocity RMSE: 3.07914e-08 rad/s.
- Mean final position error: 1.0496e-09 m.
- Mean maximum position error: 5.25442e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 1.04975e-06%.
- Orientation MAE as a percentage of MuJoCo angular travel: 4.15271e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 79.5334%.
- Orientation error reduction: 92.5692%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

# Experiment: Neural Network Size

## Run: 1 hidden layers x 64 neurons

- Training seed: 1.

- Requested optimizer updates for source training: 10,000.
- Actual optimizer updates for source training: 10,016.
- Completed source-training epochs: 32.
- Selected checkpoint update: 10,016.
- Trainable parameters: 1,740.
- Source training time: 9.0678 s.

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

- Mean position MAE: 0.00075708 m.
- Trajectory standard deviation of position MAE: 0.000522863 m.
- Mean orientation MAE: 0.000632599 deg.
- Trajectory standard deviation of orientation MAE: 0.00056185 deg.
- Mean orientation MAE in radians: 1.10409e-05 rad.
- Mean position RMSE: 0.00112373 m.
- Mean orientation RMSE: 0.000753499 deg.
- Mean linear velocity MAE: 0.000315236 m/s.
- Mean linear velocity RMSE: 0.000418213 m/s.
- Mean angular velocity MAE: 2.55769e-06 rad/s.
- Mean angular velocity RMSE: 2.67192e-06 rad/s.
- Mean final position error: 0.00294992 m.
- Mean maximum position error: 0.00295227 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.349734%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.0125878%.

### Hybrid improvement versus physics-only

- Position error reduction: 94.7154%.
- Orientation error reduction: 93.5476%.

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

- Mean position MAE: 2.29243e-09 m.
- Trajectory standard deviation of position MAE: 1.12484e-09 m.
- Mean orientation MAE: 2.66165e-09 deg.
- Trajectory standard deviation of orientation MAE: 1.1413e-09 deg.
- Mean orientation MAE in radians: 4.64546e-11 rad.
- Mean position RMSE: 3.27972e-09 m.
- Mean orientation RMSE: 4.50261e-09 deg.
- Mean linear velocity MAE: 4.61219e-07 m/s.
- Mean linear velocity RMSE: 6.59449e-07 m/s.
- Mean angular velocity MAE: 9.37716e-09 rad/s.
- Mean angular velocity RMSE: 1.58552e-08 rad/s.
- Mean final position error: 5.73646e-10 m.
- Mean maximum position error: 1.42184e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 7.63191e-07%.
- Orientation MAE as a percentage of MuJoCo angular travel: 4.46301e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 94.5367%.
- Orientation error reduction: 96.2662%.

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

- Mean position MAE: 0.00224362 m.
- Trajectory standard deviation of position MAE: 0.000850986 m.
- Mean orientation MAE: 0.00197721 deg.
- Trajectory standard deviation of orientation MAE: 0.00102345 deg.
- Mean orientation MAE in radians: 3.45087e-05 rad.
- Mean position RMSE: 0.00310766 m.
- Mean orientation RMSE: 0.0026331 deg.
- Mean linear velocity MAE: 0.000916339 m/s.
- Mean linear velocity RMSE: 0.001188 m/s.
- Mean angular velocity MAE: 1.07915e-05 rad/s.
- Mean angular velocity RMSE: 1.27228e-05 rad/s.
- Mean final position error: 0.00774334 m.
- Mean maximum position error: 0.00774334 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.297212%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.0133846%.

### Hybrid improvement versus physics-only

- Position error reduction: 81.5408%.
- Orientation error reduction: 73.0019%.

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

- Mean position MAE: 1.4531e-08 m.
- Trajectory standard deviation of position MAE: 7.3911e-09 m.
- Mean orientation MAE: 1.26928e-08 deg.
- Trajectory standard deviation of orientation MAE: 4.75737e-09 deg.
- Mean orientation MAE in radians: 2.21532e-10 rad.
- Mean position RMSE: 2.03039e-08 m.
- Mean orientation RMSE: 1.65178e-08 deg.
- Mean linear velocity MAE: 2.9469e-06 m/s.
- Mean linear velocity RMSE: 4.11477e-06 m/s.
- Mean angular velocity MAE: 4.50128e-08 rad/s.
- Mean angular velocity RMSE: 5.86499e-08 rad/s.
- Mean final position error: 2.37524e-09 m.
- Mean maximum position error: 6.10485e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 1.80446e-06%.
- Orientation MAE as a percentage of MuJoCo angular travel: 8.31875e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 66.1844%.
- Orientation error reduction: 85.815%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

# Experiment: Neural Network Size

## Run: 2 hidden layers x 32 neurons

- Training seed: 2.

- Requested optimizer updates for source training: 10,000.
- Actual optimizer updates for source training: 10,016.
- Completed source-training epochs: 32.
- Selected checkpoint update: 9,700.
- Trainable parameters: 1,932.
- Source training time: 9.6931 s.

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

- Mean position MAE: 0.000708559 m.
- Trajectory standard deviation of position MAE: 0.000733117 m.
- Mean orientation MAE: 0.000534088 deg.
- Trajectory standard deviation of orientation MAE: 0.000509868 deg.
- Mean orientation MAE in radians: 9.3216e-06 rad.
- Mean position RMSE: 0.000999886 m.
- Mean orientation RMSE: 0.00065123 deg.
- Mean linear velocity MAE: 0.000266264 m/s.
- Mean linear velocity RMSE: 0.000340923 m/s.
- Mean angular velocity MAE: 2.29404e-06 rad/s.
- Mean angular velocity RMSE: 2.44623e-06 rad/s.
- Mean final position error: 0.00250183 m.
- Mean maximum position error: 0.00251009 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.173189%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.0082958%.

### Hybrid improvement versus physics-only

- Position error reduction: 95.054%.
- Orientation error reduction: 94.5524%.

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

- Mean position MAE: 1.8883e-09 m.
- Trajectory standard deviation of position MAE: 9.08134e-10 m.
- Mean orientation MAE: 2.13384e-09 deg.
- Trajectory standard deviation of orientation MAE: 1.04907e-09 deg.
- Mean orientation MAE in radians: 3.72425e-11 rad.
- Mean position RMSE: 2.52553e-09 m.
- Mean orientation RMSE: 3.50348e-09 deg.
- Mean linear velocity MAE: 3.78056e-07 m/s.
- Mean linear velocity RMSE: 5.02274e-07 m/s.
- Mean angular velocity MAE: 7.63257e-09 rad/s.
- Mean angular velocity RMSE: 1.25851e-08 rad/s.
- Mean final position error: 5.57157e-10 m.
- Mean maximum position error: 1.05523e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 5.64259e-07%.
- Orientation MAE as a percentage of MuJoCo angular travel: 3.11224e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 95.4998%.
- Orientation error reduction: 97.0066%.

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

- Mean position MAE: 0.00151592 m.
- Trajectory standard deviation of position MAE: 0.00107418 m.
- Mean orientation MAE: 0.00163284 deg.
- Trajectory standard deviation of orientation MAE: 0.000920988 deg.
- Mean orientation MAE in radians: 2.84984e-05 rad.
- Mean position RMSE: 0.00206313 m.
- Mean orientation RMSE: 0.00221069 deg.
- Mean linear velocity MAE: 0.00062943 m/s.
- Mean linear velocity RMSE: 0.000793332 m/s.
- Mean angular velocity MAE: 9.25038e-06 rad/s.
- Mean angular velocity RMSE: 1.10157e-05 rad/s.
- Mean final position error: 0.00477676 m.
- Mean maximum position error: 0.00480338 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.201506%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.0104818%.

### Hybrid improvement versus physics-only

- Position error reduction: 87.5279%.
- Orientation error reduction: 77.7041%.

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

- Mean position MAE: 1.07886e-08 m.
- Trajectory standard deviation of position MAE: 6.65741e-09 m.
- Mean orientation MAE: 1.03173e-08 deg.
- Trajectory standard deviation of orientation MAE: 5.48096e-09 deg.
- Mean orientation MAE in radians: 1.8007e-10 rad.
- Mean position RMSE: 1.71202e-08 m.
- Mean orientation RMSE: 1.40553e-08 deg.
- Mean linear velocity MAE: 2.11621e-06 m/s.
- Mean linear velocity RMSE: 3.35214e-06 m/s.
- Mean angular velocity MAE: 3.70995e-08 rad/s.
- Mean angular velocity RMSE: 5.07088e-08 rad/s.
- Mean final position error: 1.67187e-09 m.
- Mean maximum position error: 6.1466e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 1.31039e-06%.
- Orientation MAE as a percentage of MuJoCo angular travel: 6.5465e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 74.8936%.
- Orientation error reduction: 88.4698%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

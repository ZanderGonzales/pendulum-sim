# Experiment: Neural Network Size

## Run: 2 hidden layers x 128 neurons

- Training seed: 1.

- Requested optimizer updates for source training: 10,000.
- Actual optimizer updates for source training: 10,016.
- Completed source-training epochs: 32.
- Selected checkpoint update: 8,900.
- Trainable parameters: 19,980.
- Source training time: 21.9560 s.

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

- Mean position MAE: 0.000369082 m.
- Trajectory standard deviation of position MAE: 0.000421221 m.
- Mean orientation MAE: 0.000330144 deg.
- Trajectory standard deviation of orientation MAE: 0.000323326 deg.
- Mean orientation MAE in radians: 5.76209e-06 rad.
- Mean position RMSE: 0.00054557 m.
- Mean orientation RMSE: 0.000402597 deg.
- Mean linear velocity MAE: 0.000155531 m/s.
- Mean linear velocity RMSE: 0.000209552 m/s.
- Mean angular velocity MAE: 1.40566e-06 rad/s.
- Mean angular velocity RMSE: 1.49488e-06 rad/s.
- Mean final position error: 0.00147378 m.
- Mean maximum position error: 0.00147378 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.161098%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00576197%.

### Hybrid improvement versus physics-only

- Position error reduction: 97.4237%.
- Orientation error reduction: 96.6326%.

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

- Mean position MAE: 8.82729e-10 m.
- Trajectory standard deviation of position MAE: 3.07182e-10 m.
- Mean orientation MAE: 1.26783e-09 deg.
- Trajectory standard deviation of orientation MAE: 5.1485e-10 deg.
- Mean orientation MAE in radians: 2.21278e-11 rad.
- Mean position RMSE: 1.26208e-09 m.
- Mean orientation RMSE: 2.32216e-09 deg.
- Mean linear velocity MAE: 1.72513e-07 m/s.
- Mean linear velocity RMSE: 2.59225e-07 m/s.
- Mean angular velocity MAE: 4.22158e-09 rad/s.
- Mean angular velocity RMSE: 7.70059e-09 rad/s.
- Mean final position error: 4.12448e-10 m.
- Mean maximum position error: 7.68689e-09 m.
- Position MAE as a percentage of MuJoCo distance traveled: 3.99301e-07%.
- Orientation MAE as a percentage of MuJoCo angular travel: 2.27281e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 97.8963%.
- Orientation error reduction: 98.2215%.

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

- Mean position MAE: 0.000927212 m.
- Trajectory standard deviation of position MAE: 0.000646125 m.
- Mean orientation MAE: 0.000907023 deg.
- Trajectory standard deviation of orientation MAE: 0.000546269 deg.
- Mean orientation MAE in radians: 1.58305e-05 rad.
- Mean position RMSE: 0.00126699 m.
- Mean orientation RMSE: 0.00118771 deg.
- Mean linear velocity MAE: 0.00039829 m/s.
- Mean linear velocity RMSE: 0.000514062 m/s.
- Mean angular velocity MAE: 4.82675e-06 rad/s.
- Mean angular velocity RMSE: 5.57813e-06 rad/s.
- Mean final position error: 0.00299726 m.
- Mean maximum position error: 0.00300628 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.11735%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00580421%.

### Hybrid improvement versus physics-only

- Position error reduction: 92.3714%.
- Orientation error reduction: 87.6149%.

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

- Mean position MAE: 7.50915e-09 m.
- Trajectory standard deviation of position MAE: 4.74241e-09 m.
- Mean orientation MAE: 6.59898e-09 deg.
- Trajectory standard deviation of orientation MAE: 3.29926e-09 deg.
- Mean orientation MAE in radians: 1.15174e-10 rad.
- Mean position RMSE: 1.2068e-08 m.
- Mean orientation RMSE: 8.82285e-09 deg.
- Mean linear velocity MAE: 1.50051e-06 m/s.
- Mean linear velocity RMSE: 2.43601e-06 m/s.
- Mean angular velocity MAE: 2.28712e-08 rad/s.
- Mean angular velocity RMSE: 3.07553e-08 rad/s.
- Mean final position error: 1.62503e-09 m.
- Mean maximum position error: 4.40876e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 9.06445e-07%.
- Orientation MAE as a percentage of MuJoCo angular travel: 4.21719e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 82.5252%.
- Orientation error reduction: 92.6253%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

# Experiment: Neural Network Size

## Run: 2 hidden layers x 128 neurons

- Training seed: 0.

- Requested optimizer updates for source training: 10,000.
- Actual optimizer updates for source training: 10,016.
- Completed source-training epochs: 32.
- Selected checkpoint update: 9,600.
- Trainable parameters: 19,980.
- Source training time: 23.9819 s.

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

- Mean position MAE: 0.000375745 m.
- Trajectory standard deviation of position MAE: 0.000282567 m.
- Mean orientation MAE: 0.000314276 deg.
- Trajectory standard deviation of orientation MAE: 0.000213309 deg.
- Mean orientation MAE in radians: 5.48515e-06 rad.
- Mean position RMSE: 0.000560748 m.
- Mean orientation RMSE: 0.00037887 deg.
- Mean linear velocity MAE: 0.000154438 m/s.
- Mean linear velocity RMSE: 0.000204942 m/s.
- Mean angular velocity MAE: 1.38792e-06 rad/s.
- Mean angular velocity RMSE: 1.4852e-06 rad/s.
- Mean final position error: 0.00148942 m.
- Mean maximum position error: 0.00148942 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.188062%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00692605%.

### Hybrid improvement versus physics-only

- Position error reduction: 97.3772%.
- Orientation error reduction: 96.7944%.

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

- Mean position MAE: 7.45996e-10 m.
- Trajectory standard deviation of position MAE: 3.23209e-10 m.
- Mean orientation MAE: 1.2432e-09 deg.
- Trajectory standard deviation of orientation MAE: 6.11367e-10 deg.
- Mean orientation MAE in radians: 2.16979e-11 rad.
- Mean position RMSE: 1.17458e-09 m.
- Mean orientation RMSE: 2.34767e-09 deg.
- Mean linear velocity MAE: 1.48622e-07 m/s.
- Mean linear velocity RMSE: 2.32176e-07 m/s.
- Mean angular velocity MAE: 4.34878e-09 rad/s.
- Mean angular velocity RMSE: 8.34969e-09 rad/s.
- Mean final position error: 2.44723e-10 m.
- Mean maximum position error: 7.29648e-09 m.
- Position MAE as a percentage of MuJoCo distance traveled: 2.97547e-07%.
- Orientation MAE as a percentage of MuJoCo angular travel: 2.21583e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 98.2221%.
- Orientation error reduction: 98.256%.

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

- Mean position MAE: 0.000982744 m.
- Trajectory standard deviation of position MAE: 0.000612932 m.
- Mean orientation MAE: 0.000985207 deg.
- Trajectory standard deviation of orientation MAE: 0.000650443 deg.
- Mean orientation MAE in radians: 1.71951e-05 rad.
- Mean position RMSE: 0.00138222 m.
- Mean orientation RMSE: 0.00129808 deg.
- Mean linear velocity MAE: 0.000373987 m/s.
- Mean linear velocity RMSE: 0.000479652 m/s.
- Mean angular velocity MAE: 5.24602e-06 rad/s.
- Mean angular velocity RMSE: 6.15757e-06 rad/s.
- Mean final position error: 0.00323894 m.
- Mean maximum position error: 0.00323894 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.126783%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00642198%.

### Hybrid improvement versus physics-only

- Position error reduction: 91.9146%.
- Orientation error reduction: 86.5473%.

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

- Mean position MAE: 7.985e-09 m.
- Trajectory standard deviation of position MAE: 6.19003e-09 m.
- Mean orientation MAE: 7.21914e-09 deg.
- Trajectory standard deviation of orientation MAE: 4.26241e-09 deg.
- Mean orientation MAE in radians: 1.25998e-10 rad.
- Mean position RMSE: 1.27791e-08 m.
- Mean orientation RMSE: 9.92013e-09 deg.
- Mean linear velocity MAE: 1.55369e-06 m/s.
- Mean linear velocity RMSE: 2.4675e-06 m/s.
- Mean angular velocity MAE: 2.51576e-08 rad/s.
- Mean angular velocity RMSE: 3.44256e-08 rad/s.
- Mean final position error: 8.45884e-10 m.
- Mean maximum position error: 4.6196e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 9.47433e-07%.
- Orientation MAE as a percentage of MuJoCo angular travel: 4.5771e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 81.4178%.
- Orientation error reduction: 91.9322%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

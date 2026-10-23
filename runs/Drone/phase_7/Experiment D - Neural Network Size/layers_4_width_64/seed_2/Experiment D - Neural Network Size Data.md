# Experiment: Neural Network Size

## Run: 4 hidden layers x 64 neurons

- Training seed: 2.

- Requested optimizer updates for source training: 10,000.
- Actual optimizer updates for source training: 10,016.
- Completed source-training epochs: 32.
- Selected checkpoint update: 8,800.
- Trainable parameters: 14,220.
- Source training time: 21.7193 s.

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

- Mean position MAE: 0.000479159 m.
- Trajectory standard deviation of position MAE: 0.000546479 m.
- Mean orientation MAE: 0.00039771 deg.
- Trajectory standard deviation of orientation MAE: 0.00030618 deg.
- Mean orientation MAE in radians: 6.94134e-06 rad.
- Mean position RMSE: 0.00069286 m.
- Mean orientation RMSE: 0.000486985 deg.
- Mean linear velocity MAE: 0.00018959 m/s.
- Mean linear velocity RMSE: 0.000250203 m/s.
- Mean angular velocity MAE: 1.70581e-06 rad/s.
- Mean angular velocity RMSE: 1.82546e-06 rad/s.
- Mean final position error: 0.00180978 m.
- Mean maximum position error: 0.00180978 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.155853%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00671519%.

### Hybrid improvement versus physics-only

- Position error reduction: 96.6553%.
- Orientation error reduction: 95.9434%.

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

- Mean position MAE: 9.79926e-10 m.
- Trajectory standard deviation of position MAE: 4.54505e-10 m.
- Mean orientation MAE: 1.5157e-09 deg.
- Trajectory standard deviation of orientation MAE: 7.51079e-10 deg.
- Mean orientation MAE in radians: 2.6454e-11 rad.
- Mean position RMSE: 1.45617e-09 m.
- Mean orientation RMSE: 2.89342e-09 deg.
- Mean linear velocity MAE: 1.95085e-07 m/s.
- Mean linear velocity RMSE: 2.87664e-07 m/s.
- Mean angular velocity MAE: 5.30143e-09 rad/s.
- Mean angular velocity RMSE: 9.9082e-09 rad/s.
- Mean final position error: 3.45528e-10 m.
- Mean maximum position error: 8.56189e-09 m.
- Position MAE as a percentage of MuJoCo distance traveled: 3.7351e-07%.
- Orientation MAE as a percentage of MuJoCo angular travel: 2.30846e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 97.6646%.
- Orientation error reduction: 97.8737%.

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

- Mean position MAE: 0.00178737 m.
- Trajectory standard deviation of position MAE: 0.00145061 m.
- Mean orientation MAE: 0.00108282 deg.
- Trajectory standard deviation of orientation MAE: 0.00064964 deg.
- Mean orientation MAE in radians: 1.88988e-05 rad.
- Mean position RMSE: 0.00254678 m.
- Mean orientation RMSE: 0.00148111 deg.
- Mean linear velocity MAE: 0.000698312 m/s.
- Mean linear velocity RMSE: 0.000894238 m/s.
- Mean angular velocity MAE: 6.37391e-06 rad/s.
- Mean angular velocity RMSE: 7.81039e-06 rad/s.
- Mean final position error: 0.00606659 m.
- Mean maximum position error: 0.00606659 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.214379%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00706711%.

### Hybrid improvement versus physics-only

- Position error reduction: 85.2945%.
- Orientation error reduction: 85.2144%.

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

- Mean position MAE: 1.24412e-08 m.
- Trajectory standard deviation of position MAE: 9.74505e-09 m.
- Mean orientation MAE: 8.92381e-09 deg.
- Trajectory standard deviation of orientation MAE: 5.60925e-09 deg.
- Mean orientation MAE in radians: 1.5575e-10 rad.
- Mean position RMSE: 2.0113e-08 m.
- Mean orientation RMSE: 1.27473e-08 deg.
- Mean linear velocity MAE: 2.48094e-06 m/s.
- Mean linear velocity RMSE: 4.01125e-06 m/s.
- Mean angular velocity MAE: 3.06804e-08 rad/s.
- Mean angular velocity RMSE: 4.41303e-08 rad/s.
- Mean final position error: 1.43001e-09 m.
- Mean maximum position error: 7.03988e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 1.46506e-06%.
- Orientation MAE as a percentage of MuJoCo angular travel: 5.59954e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 71.0476%.
- Orientation error reduction: 90.0271%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

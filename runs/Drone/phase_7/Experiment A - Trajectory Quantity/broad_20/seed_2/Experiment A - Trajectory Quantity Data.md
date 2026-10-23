# Experiment: Trajectory Quantity

## Run: 20 broad trajectories

- Training seed: 2.

- Requested optimizer updates for source training: 10,000.
- Actual optimizer updates for source training: 10,033.
- Completed source-training epochs: 127.
- Selected checkpoint update: 9,900.
- Trainable parameters: 5,900.
- Source training time: 9.3572 s.

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

- Mean position MAE: 0.00106335 m.
- Trajectory standard deviation of position MAE: 0.00108893 m.
- Mean orientation MAE: 0.00082112 deg.
- Trajectory standard deviation of orientation MAE: 0.000847837 deg.
- Mean orientation MAE in radians: 1.43312e-05 rad.
- Mean position RMSE: 0.00153988 m.
- Mean orientation RMSE: 0.00100758 deg.
- Mean linear velocity MAE: 0.000418593 m/s.
- Mean linear velocity RMSE: 0.000542989 m/s.
- Mean angular velocity MAE: 3.61293e-06 rad/s.
- Mean angular velocity RMSE: 3.98065e-06 rad/s.
- Mean final position error: 0.00397939 m.
- Mean maximum position error: 0.00397939 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.382516%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.0137349%.

### Hybrid improvement versus physics-only

- Position error reduction: 92.5775%.
- Orientation error reduction: 91.6247%.

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

- Mean position MAE: 2.0298e-09 m.
- Trajectory standard deviation of position MAE: 1.30208e-09 m.
- Mean orientation MAE: 2.67072e-09 deg.
- Trajectory standard deviation of orientation MAE: 1.94134e-09 deg.
- Mean orientation MAE in radians: 4.66129e-11 rad.
- Mean position RMSE: 3.66794e-09 m.
- Mean orientation RMSE: 5.9323e-09 deg.
- Mean linear velocity MAE: 4.07044e-07 m/s.
- Mean linear velocity RMSE: 7.28748e-07 m/s.
- Mean angular velocity MAE: 9.43871e-09 rad/s.
- Mean angular velocity RMSE: 2.08087e-08 rad/s.
- Mean final position error: 3.50506e-10 m.
- Mean maximum position error: 2.37118e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 5.86804e-07%.
- Orientation MAE as a percentage of MuJoCo angular travel: 3.51694e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 95.1626%.
- Orientation error reduction: 96.2535%.

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

- Mean position MAE: 0.00173051 m.
- Trajectory standard deviation of position MAE: 0.000908045 m.
- Mean orientation MAE: 0.00145591 deg.
- Trajectory standard deviation of orientation MAE: 0.00103173 deg.
- Mean orientation MAE in radians: 2.54104e-05 rad.
- Mean position RMSE: 0.00241015 m.
- Mean orientation RMSE: 0.00186765 deg.
- Mean linear velocity MAE: 0.00067641 m/s.
- Mean linear velocity RMSE: 0.000860439 m/s.
- Mean angular velocity MAE: 7.68771e-06 rad/s.
- Mean angular velocity RMSE: 8.85956e-06 rad/s.
- Mean final position error: 0.00534534 m.
- Mean maximum position error: 0.00548714 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.223349%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00900681%.

### Hybrid improvement versus physics-only

- Position error reduction: 85.7624%.
- Orientation error reduction: 80.12%.

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

- Mean position MAE: 1.43866e-08 m.
- Trajectory standard deviation of position MAE: 9.14044e-09 m.
- Mean orientation MAE: 1.1829e-08 deg.
- Trajectory standard deviation of orientation MAE: 5.54794e-09 deg.
- Mean orientation MAE in radians: 2.06455e-10 rad.
- Mean position RMSE: 2.1472e-08 m.
- Mean orientation RMSE: 1.57868e-08 deg.
- Mean linear velocity MAE: 2.91272e-06 m/s.
- Mean linear velocity RMSE: 4.35838e-06 m/s.
- Mean angular velocity MAE: 4.0856e-08 rad/s.
- Mean angular velocity RMSE: 5.43317e-08 rad/s.
- Mean final position error: 3.42221e-09 m.
- Mean maximum position error: 7.34112e-08 m.
- Position MAE as a percentage of MuJoCo distance traveled: 1.75131e-06%.
- Orientation MAE as a percentage of MuJoCo angular travel: 7.50494e-08%.

### Hybrid improvement versus physics-only

- Position error reduction: 66.5204%.
- Orientation error reduction: 86.7804%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

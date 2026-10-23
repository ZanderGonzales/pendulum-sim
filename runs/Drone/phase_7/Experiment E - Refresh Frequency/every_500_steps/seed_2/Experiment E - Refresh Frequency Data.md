# Experiment: Refresh Frequency

## Run: Every 500 steps

- Training seed: 2.

- Requested optimizer updates for source training: 10,000.
- Actual optimizer updates for source training: 10,016.
- Completed source-training epochs: 32.
- Selected checkpoint update: 9,800.
- Trainable parameters: 5,900.
- Source training time: 12.4214 s.

No training or weight updates occurred for this refresh run. The source checkpoint remains fixed.

Source run: `runs/Drone/phase_7/Experiment A - Trajectory Quantity/broad_80/seed_2`.

Errors below use forecasts saved before any truth replacement. Playback shows post-replacement states.

## Test: recursive

### Physics only

- Mean position MAE: 0.00360604 m.
- Trajectory standard deviation of position MAE: 0.0019562 m.
- Mean orientation MAE: 0.0061472 deg.
- Trajectory standard deviation of orientation MAE: 0.00525044 deg.
- Mean orientation MAE in radians: 0.000107289 rad.
- Mean position RMSE: 0.00554953 m.
- Mean orientation RMSE: 0.00898609 deg.
- Mean linear velocity MAE: 0.00222139 m/s.
- Mean linear velocity RMSE: 0.00286789 m/s.
- Mean angular velocity MAE: 5.4578e-05 rad/s.
- Mean angular velocity RMSE: 6.62203e-05 rad/s.
- Mean final position error: 0.0118723 m.
- Mean maximum position error: 0.0142192 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.758731%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.0603179%.

### Physics + NN

- Mean position MAE: 6.1378e-05 m.
- Trajectory standard deviation of position MAE: 3.21412e-05 m.
- Mean orientation MAE: 0.000112313 deg.
- Trajectory standard deviation of orientation MAE: 7.68839e-05 deg.
- Mean orientation MAE in radians: 1.96024e-06 rad.
- Mean position RMSE: 8.96182e-05 m.
- Mean orientation RMSE: 0.000153816 deg.
- Mean linear velocity MAE: 3.92594e-05 m/s.
- Mean linear velocity RMSE: 4.97832e-05 m/s.
- Mean angular velocity MAE: 9.85207e-07 rad/s.
- Mean angular velocity RMSE: 1.1627e-06 rad/s.
- Mean final position error: 0.00011694 m.
- Mean maximum position error: 0.000255655 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.0263032%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00203187%.

### Hybrid improvement versus physics-only

- Position error reduction: 98.2979%.
- Orientation error reduction: 98.1729%.

## Benchmark: recursive

### Physics only

- Mean position MAE: 0.0034595 m.
- Trajectory standard deviation of position MAE: 0.00136417 m.
- Mean orientation MAE: 0.00282407 deg.
- Trajectory standard deviation of orientation MAE: 0.000971428 deg.
- Mean orientation MAE in radians: 4.92894e-05 rad.
- Mean position RMSE: 0.00511391 m.
- Mean orientation RMSE: 0.00347595 deg.
- Mean linear velocity MAE: 0.00190594 m/s.
- Mean linear velocity RMSE: 0.00239055 m/s.
- Mean angular velocity MAE: 2.34745e-05 rad/s.
- Mean angular velocity RMSE: 2.667e-05 rad/s.
- Mean final position error: 0.0106433 m.
- Mean maximum position error: 0.0124666 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.435461%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.0187545%.

### Physics + NN

- Mean position MAE: 0.000589366 m.
- Trajectory standard deviation of position MAE: 0.000443909 m.
- Mean orientation MAE: 0.000458018 deg.
- Trajectory standard deviation of orientation MAE: 0.000306227 deg.
- Mean orientation MAE in radians: 7.99392e-06 rad.
- Mean position RMSE: 0.000946146 m.
- Mean orientation RMSE: 0.000696325 deg.
- Mean linear velocity MAE: 0.000375292 m/s.
- Mean linear velocity RMSE: 0.000493515 m/s.
- Mean angular velocity MAE: 4.78966e-06 rad/s.
- Mean angular velocity RMSE: 6.31932e-06 rad/s.
- Mean final position error: 0.00239108 m.
- Mean maximum position error: 0.00263613 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.0694653%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00286975%.

### Hybrid improvement versus physics-only

- Position error reduction: 82.9639%.
- Orientation error reduction: 83.7816%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

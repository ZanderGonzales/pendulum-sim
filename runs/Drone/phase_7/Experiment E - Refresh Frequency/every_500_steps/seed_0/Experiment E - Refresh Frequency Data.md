# Experiment: Refresh Frequency

## Run: Every 500 steps

- Training seed: 0.

- Requested optimizer updates for source training: 10,000.
- Actual optimizer updates for source training: 10,016.
- Completed source-training epochs: 32.
- Selected checkpoint update: 10,016.
- Trainable parameters: 5,900.
- Source training time: 13.3145 s.

No training or weight updates occurred for this refresh run. The source checkpoint remains fixed.

Source run: `runs/Drone/phase_7/Experiment A - Trajectory Quantity/broad_80/seed_0`.

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

- Mean position MAE: 5.27806e-05 m.
- Trajectory standard deviation of position MAE: 3.03253e-05 m.
- Mean orientation MAE: 9.82953e-05 deg.
- Trajectory standard deviation of orientation MAE: 6.53151e-05 deg.
- Mean orientation MAE in radians: 1.71558e-06 rad.
- Mean position RMSE: 8.03084e-05 m.
- Mean orientation RMSE: 0.000146031 deg.
- Mean linear velocity MAE: 3.45608e-05 m/s.
- Mean linear velocity RMSE: 4.73636e-05 m/s.
- Mean angular velocity MAE: 8.63146e-07 rad/s.
- Mean angular velocity RMSE: 1.07646e-06 rad/s.
- Mean final position error: 7.17297e-05 m.
- Mean maximum position error: 0.000245603 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.0194354%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00166403%.

### Hybrid improvement versus physics-only

- Position error reduction: 98.5363%.
- Orientation error reduction: 98.401%.

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

- Mean position MAE: 0.000647227 m.
- Trajectory standard deviation of position MAE: 0.000610866 m.
- Mean orientation MAE: 0.000395195 deg.
- Trajectory standard deviation of orientation MAE: 0.000207813 deg.
- Mean orientation MAE in radians: 6.89746e-06 rad.
- Mean position RMSE: 0.00106923 m.
- Mean orientation RMSE: 0.000621866 deg.
- Mean linear velocity MAE: 0.000377613 m/s.
- Mean linear velocity RMSE: 0.00051048 m/s.
- Mean angular velocity MAE: 3.84985e-06 rad/s.
- Mean angular velocity RMSE: 4.99414e-06 rad/s.
- Mean final position error: 0.00271424 m.
- Mean maximum position error: 0.00298248 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.074943%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00249916%.

### Hybrid improvement versus physics-only

- Position error reduction: 81.2913%.
- Orientation error reduction: 86.0062%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

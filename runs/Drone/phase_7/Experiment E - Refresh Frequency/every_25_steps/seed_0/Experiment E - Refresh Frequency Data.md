# Experiment: Refresh Frequency

## Run: Every 25 steps

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

- Mean position MAE: 9.26426e-06 m.
- Trajectory standard deviation of position MAE: 6.23515e-06 m.
- Mean orientation MAE: 1.56815e-05 deg.
- Trajectory standard deviation of orientation MAE: 1.29518e-05 deg.
- Mean orientation MAE in radians: 2.73693e-07 rad.
- Mean position RMSE: 1.85287e-05 m.
- Mean orientation RMSE: 2.94277e-05 deg.
- Mean linear velocity MAE: 0.00010891 m/s.
- Mean linear velocity RMSE: 0.000187494 m/s.
- Mean angular velocity MAE: 3.22196e-06 rad/s.
- Mean angular velocity RMSE: 5.20686e-06 rad/s.
- Mean final position error: 1.53319e-07 m.
- Mean maximum position error: 9.82589e-05 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.00126417%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.000123527%.

### Physics + NN

- Mean position MAE: 1.94008e-07 m.
- Trajectory standard deviation of position MAE: 8.98186e-08 m.
- Mean orientation MAE: 2.92166e-07 deg.
- Trajectory standard deviation of orientation MAE: 1.38704e-07 deg.
- Mean orientation MAE in radians: 5.09926e-09 rad.
- Mean position RMSE: 3.7928e-07 m.
- Mean orientation RMSE: 6.88762e-07 deg.
- Mean linear velocity MAE: 2.23943e-06 m/s.
- Mean linear velocity RMSE: 3.68646e-06 m/s.
- Mean angular velocity MAE: 5.87402e-08 rad/s.
- Mean angular velocity RMSE: 1.1338e-07 rad/s.
- Mean final position error: 1.27978e-07 m.
- Mean maximum position error: 2.85002e-06 m.
- Position MAE as a percentage of MuJoCo distance traveled: 6.71507e-05%.
- Orientation MAE as a percentage of MuJoCo angular travel: 4.66198e-06%.

### Hybrid improvement versus physics-only

- Position error reduction: 97.9058%.
- Orientation error reduction: 98.1369%.

## Benchmark: recursive

### Physics only

- Mean position MAE: 9.48864e-06 m.
- Trajectory standard deviation of position MAE: 4.20279e-06 m.
- Mean orientation MAE: 1.94801e-05 deg.
- Trajectory standard deviation of orientation MAE: 5.3877e-06 deg.
- Mean orientation MAE in radians: 3.39993e-07 rad.
- Mean position RMSE: 1.92221e-05 m.
- Mean orientation RMSE: 3.23411e-05 deg.
- Mean linear velocity MAE: 0.000111523 m/s.
- Mean linear velocity RMSE: 0.000194412 m/s.
- Mean angular velocity MAE: 3.98759e-06 rad/s.
- Mean angular velocity RMSE: 5.6668e-06 rad/s.
- Mean final position error: 4.3807e-07 m.
- Mean maximum position error: 0.000122132 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.00117737%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.000128586%.

### Physics + NN

- Mean position MAE: 2.0357e-06 m.
- Trajectory standard deviation of position MAE: 1.49449e-06 m.
- Mean orientation MAE: 1.55261e-06 deg.
- Trajectory standard deviation of orientation MAE: 8.52324e-07 deg.
- Mean orientation MAE in radians: 2.70982e-08 rad.
- Mean position RMSE: 4.40568e-06 m.
- Mean orientation RMSE: 2.88848e-06 deg.
- Mean linear velocity MAE: 2.3926e-05 m/s.
- Mean linear velocity RMSE: 4.45016e-05 m/s.
- Mean angular velocity MAE: 3.17328e-07 rad/s.
- Mean angular velocity RMSE: 5.06256e-07 rad/s.
- Mean final position error: 3.11127e-07 m.
- Mean maximum position error: 3.15428e-05 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.000241434%.
- Orientation MAE as a percentage of MuJoCo angular travel: 9.83316e-06%.

### Hybrid improvement versus physics-only

- Position error reduction: 78.5459%.
- Orientation error reduction: 92.0298%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

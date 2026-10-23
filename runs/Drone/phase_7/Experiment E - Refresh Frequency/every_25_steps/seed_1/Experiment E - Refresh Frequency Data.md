# Experiment: Refresh Frequency

## Run: Every 25 steps

- Training seed: 1.

- Requested optimizer updates for source training: 10,000.
- Actual optimizer updates for source training: 10,016.
- Completed source-training epochs: 32.
- Selected checkpoint update: 10,016.
- Trainable parameters: 5,900.
- Source training time: 13.0851 s.

No training or weight updates occurred for this refresh run. The source checkpoint remains fixed.

Source run: `runs/Drone/phase_7/Experiment A - Trajectory Quantity/broad_80/seed_1`.

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

- Mean position MAE: 1.86413e-07 m.
- Trajectory standard deviation of position MAE: 7.38084e-08 m.
- Mean orientation MAE: 3.11138e-07 deg.
- Trajectory standard deviation of orientation MAE: 1.51e-07 deg.
- Mean orientation MAE in radians: 5.43038e-09 rad.
- Mean position RMSE: 3.31249e-07 m.
- Mean orientation RMSE: 7.50293e-07 deg.
- Mean linear velocity MAE: 2.16695e-06 m/s.
- Mean linear velocity RMSE: 3.26463e-06 m/s.
- Mean angular velocity MAE: 6.23982e-08 rad/s.
- Mean angular velocity RMSE: 1.22943e-07 rad/s.
- Mean final position error: 1.71898e-07 m.
- Mean maximum position error: 2.41069e-06 m.
- Position MAE as a percentage of MuJoCo distance traveled: 7.60178e-05%.
- Orientation MAE as a percentage of MuJoCo angular travel: 5.02065e-06%.

### Hybrid improvement versus physics-only

- Position error reduction: 97.9878%.
- Orientation error reduction: 98.0159%.

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

- Mean position MAE: 1.80586e-06 m.
- Trajectory standard deviation of position MAE: 1.45824e-06 m.
- Mean orientation MAE: 1.60931e-06 deg.
- Trajectory standard deviation of orientation MAE: 9.2919e-07 deg.
- Mean orientation MAE in radians: 2.80877e-08 rad.
- Mean position RMSE: 3.86259e-06 m.
- Mean orientation RMSE: 3.06985e-06 deg.
- Mean linear velocity MAE: 2.1209e-05 m/s.
- Mean linear velocity RMSE: 3.89867e-05 m/s.
- Mean angular velocity MAE: 3.28537e-07 rad/s.
- Mean angular velocity RMSE: 5.36496e-07 rad/s.
- Mean final position error: 5.29053e-07 m.
- Mean maximum position error: 2.78436e-05 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.000214955%.
- Orientation MAE as a percentage of MuJoCo angular travel: 1.01664e-05%.

### Hybrid improvement versus physics-only

- Position error reduction: 80.9682%.
- Orientation error reduction: 91.7387%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

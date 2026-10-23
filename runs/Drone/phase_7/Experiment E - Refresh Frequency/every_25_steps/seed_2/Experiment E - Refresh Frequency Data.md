# Experiment: Refresh Frequency

## Run: Every 25 steps

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

- Mean position MAE: 2.11327e-07 m.
- Trajectory standard deviation of position MAE: 9.58167e-08 m.
- Mean orientation MAE: 3.32595e-07 deg.
- Trajectory standard deviation of orientation MAE: 1.44635e-07 deg.
- Mean orientation MAE in radians: 5.80487e-09 rad.
- Mean position RMSE: 4.01239e-07 m.
- Mean orientation RMSE: 7.20187e-07 deg.
- Mean linear velocity MAE: 2.41781e-06 m/s.
- Mean linear velocity RMSE: 3.81641e-06 m/s.
- Mean angular velocity MAE: 6.6644e-08 rad/s.
- Mean angular velocity RMSE: 1.18671e-07 rad/s.
- Mean final position error: 2.33682e-07 m.
- Mean maximum position error: 3.06277e-06 m.
- Position MAE as a percentage of MuJoCo distance traveled: 7.58253e-05%.
- Orientation MAE as a percentage of MuJoCo angular travel: 5.81496e-06%.

### Hybrid improvement versus physics-only

- Position error reduction: 97.7189%.
- Orientation error reduction: 97.8791%.

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

- Mean position MAE: 2.39908e-06 m.
- Trajectory standard deviation of position MAE: 1.71092e-06 m.
- Mean orientation MAE: 2.02294e-06 deg.
- Trajectory standard deviation of orientation MAE: 1.06634e-06 deg.
- Mean orientation MAE in radians: 3.5307e-08 rad.
- Mean position RMSE: 4.82944e-06 m.
- Mean orientation RMSE: 3.89503e-06 deg.
- Mean linear velocity MAE: 2.81191e-05 m/s.
- Mean linear velocity RMSE: 4.86911e-05 m/s.
- Mean angular velocity MAE: 4.11806e-07 rad/s.
- Mean angular velocity RMSE: 6.81374e-07 rad/s.
- Mean final position error: 8.90171e-07 m.
- Mean maximum position error: 3.12253e-05 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.000285061%.
- Orientation MAE as a percentage of MuJoCo angular travel: 1.28163e-05%.

### Hybrid improvement versus physics-only

- Position error reduction: 74.7163%.
- Orientation error reduction: 89.6154%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

# Experiment: Refresh Frequency

## Run: Every 10 steps

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

- Mean position MAE: 1.61545e-06 m.
- Trajectory standard deviation of position MAE: 1.08843e-06 m.
- Mean orientation MAE: 2.74474e-06 deg.
- Trajectory standard deviation of orientation MAE: 2.25979e-06 deg.
- Mean orientation MAE in radians: 4.79047e-08 rad.
- Mean position RMSE: 3.18537e-06 m.
- Mean orientation RMSE: 5.14467e-06 deg.
- Mean linear velocity MAE: 4.61467e-05 m/s.
- Mean linear velocity RMSE: 7.85209e-05 m/s.
- Mean angular velocity MAE: 1.36818e-06 rad/s.
- Mean angular velocity RMSE: 2.21254e-06 rad/s.
- Mean final position error: 1.96487e-08 m.
- Mean maximum position error: 1.59452e-05 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.00022017%.
- Orientation MAE as a percentage of MuJoCo angular travel: 2.17164e-05%.

### Physics + NN

- Mean position MAE: 3.27497e-08 m.
- Trajectory standard deviation of position MAE: 1.31885e-08 m.
- Mean orientation MAE: 5.41701e-08 deg.
- Trajectory standard deviation of orientation MAE: 2.5906e-08 deg.
- Mean orientation MAE in radians: 9.45447e-10 rad.
- Mean position RMSE: 5.83896e-08 m.
- Mean orientation RMSE: 1.31988e-07 deg.
- Mean linear velocity MAE: 9.32312e-07 m/s.
- Mean linear velocity RMSE: 1.42437e-06 m/s.
- Mean angular velocity MAE: 2.68806e-08 rad/s.
- Mean angular velocity RMSE: 5.61309e-08 rad/s.
- Mean final position error: 2.58337e-08 m.
- Mean maximum position error: 4.90951e-07 m.
- Position MAE as a percentage of MuJoCo distance traveled: 1.32754e-05%.
- Orientation MAE as a percentage of MuJoCo angular travel: 8.81144e-07%.

### Hybrid improvement versus physics-only

- Position error reduction: 97.9727%.
- Orientation error reduction: 98.0264%.

## Benchmark: recursive

### Physics only

- Mean position MAE: 1.65431e-06 m.
- Trajectory standard deviation of position MAE: 7.32379e-07 m.
- Mean orientation MAE: 3.43052e-06 deg.
- Trajectory standard deviation of orientation MAE: 9.42696e-07 deg.
- Mean orientation MAE in radians: 5.98739e-08 rad.
- Mean position RMSE: 3.31007e-06 m.
- Mean orientation RMSE: 5.61937e-06 deg.
- Mean linear velocity MAE: 4.72586e-05 m/s.
- Mean linear velocity RMSE: 8.15895e-05 m/s.
- Mean angular velocity MAE: 1.71051e-06 rad/s.
- Mean angular velocity RMSE: 2.41705e-06 rad/s.
- Mean final position error: 6.20383e-08 m.
- Mean maximum position error: 2.01086e-05 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.000205281%.
- Orientation MAE as a percentage of MuJoCo angular travel: 2.26565e-05%.

### Physics + NN

- Mean position MAE: 3.18042e-07 m.
- Trajectory standard deviation of position MAE: 2.55829e-07 m.
- Mean orientation MAE: 2.829e-07 deg.
- Trajectory standard deviation of orientation MAE: 1.63739e-07 deg.
- Mean orientation MAE in radians: 4.93753e-09 rad.
- Mean position RMSE: 6.69935e-07 m.
- Mean orientation RMSE: 5.2948e-07 deg.
- Mean linear velocity MAE: 9.08144e-06 m/s.
- Mean linear velocity RMSE: 1.64898e-05 m/s.
- Mean angular velocity MAE: 1.40844e-07 rad/s.
- Mean angular velocity RMSE: 2.27433e-07 rad/s.
- Mean final position error: 1.23331e-07 m.
- Mean maximum position error: 4.82086e-06 m.
- Position MAE as a percentage of MuJoCo distance traveled: 3.78458e-05%.
- Orientation MAE as a percentage of MuJoCo angular travel: 1.78796e-06%.

### Hybrid improvement versus physics-only

- Position error reduction: 80.775%.
- Orientation error reduction: 91.7535%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

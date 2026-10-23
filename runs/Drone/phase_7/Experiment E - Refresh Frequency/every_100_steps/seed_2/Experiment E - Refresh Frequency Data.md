# Experiment: Refresh Frequency

## Run: Every 100 steps

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

- Mean position MAE: 0.000138796 m.
- Trajectory standard deviation of position MAE: 9.21895e-05 m.
- Mean orientation MAE: 0.000257092 deg.
- Trajectory standard deviation of orientation MAE: 0.000197419 deg.
- Mean orientation MAE in radians: 4.4871e-06 rad.
- Mean position RMSE: 0.000269831 m.
- Mean orientation RMSE: 0.00046842 deg.
- Mean linear velocity MAE: 0.000411404 m/s.
- Mean linear velocity RMSE: 0.000691005 m/s.
- Mean angular velocity MAE: 1.29579e-05 rad/s.
- Mean angular velocity RMSE: 2.0079e-05 rad/s.
- Mean final position error: 7.07094e-06 m.
- Mean maximum position error: 0.00129649 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.0189487%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00232898%.

### Physics + NN

- Mean position MAE: 2.91304e-06 m.
- Trajectory standard deviation of position MAE: 1.20259e-06 m.
- Mean orientation MAE: 5.0209e-06 deg.
- Trajectory standard deviation of orientation MAE: 2.21507e-06 deg.
- Mean orientation MAE in radians: 8.76313e-08 rad.
- Mean position RMSE: 4.84469e-06 m.
- Mean orientation RMSE: 9.49166e-06 deg.
- Mean linear velocity MAE: 7.94487e-06 m/s.
- Mean linear velocity RMSE: 1.09496e-05 m/s.
- Mean angular velocity MAE: 2.47018e-07 rad/s.
- Mean angular velocity RMSE: 3.8564e-07 rad/s.
- Mean final position error: 2.89993e-06 m.
- Mean maximum position error: 2.09682e-05 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.00108187%.
- Orientation MAE as a percentage of MuJoCo angular travel: 9.43539e-05%.

### Hybrid improvement versus physics-only

- Position error reduction: 97.9012%.
- Orientation error reduction: 98.047%.

## Benchmark: recursive

### Physics only

- Mean position MAE: 0.000142794 m.
- Trajectory standard deviation of position MAE: 6.34523e-05 m.
- Mean orientation MAE: 0.000263877 deg.
- Trajectory standard deviation of orientation MAE: 7.01437e-05 deg.
- Mean orientation MAE in radians: 4.60553e-06 rad.
- Mean position RMSE: 0.000286527 m.
- Mean orientation RMSE: 0.000444154 deg.
- Mean linear velocity MAE: 0.000421724 m/s.
- Mean linear velocity RMSE: 0.000730209 m/s.
- Mean angular velocity MAE: 1.39377e-05 rad/s.
- Mean angular velocity RMSE: 1.96147e-05 rad/s.
- Mean final position error: 0.000411166 m.
- Mean maximum position error: 0.00163238 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.0177123%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00174877%.

### Physics + NN

- Mean position MAE: 3.5082e-05 m.
- Trajectory standard deviation of position MAE: 2.71783e-05 m.
- Mean orientation MAE: 2.79737e-05 deg.
- Trajectory standard deviation of orientation MAE: 1.53095e-05 deg.
- Mean orientation MAE in radians: 4.88233e-07 rad.
- Mean position RMSE: 6.82409e-05 m.
- Mean orientation RMSE: 5.11338e-05 deg.
- Mean linear velocity MAE: 0.000104646 m/s.
- Mean linear velocity RMSE: 0.000174965 m/s.
- Mean angular velocity MAE: 1.43207e-06 rad/s.
- Mean angular velocity RMSE: 2.27319e-06 rad/s.
- Mean final position error: 8.70262e-05 m.
- Mean maximum position error: 0.000368638 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.00413697%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.000176682%.

### Hybrid improvement versus physics-only

- Position error reduction: 75.4318%.
- Orientation error reduction: 89.399%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

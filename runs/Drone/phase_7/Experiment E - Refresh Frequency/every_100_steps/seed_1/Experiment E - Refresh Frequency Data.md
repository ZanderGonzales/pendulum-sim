# Experiment: Refresh Frequency

## Run: Every 100 steps

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

- Mean position MAE: 2.69755e-06 m.
- Trajectory standard deviation of position MAE: 1.06188e-06 m.
- Mean orientation MAE: 5.02417e-06 deg.
- Trajectory standard deviation of orientation MAE: 2.54557e-06 deg.
- Mean orientation MAE in radians: 8.76883e-08 rad.
- Mean position RMSE: 4.3032e-06 m.
- Mean orientation RMSE: 1.05435e-05 deg.
- Mean linear velocity MAE: 7.3906e-06 m/s.
- Mean linear velocity RMSE: 9.8995e-06 m/s.
- Mean angular velocity MAE: 2.43314e-07 rad/s.
- Mean angular velocity RMSE: 4.23432e-07 rad/s.
- Mean final position error: 2.66137e-06 m.
- Mean maximum position error: 1.79941e-05 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.00111565%.
- Orientation MAE as a percentage of MuJoCo angular travel: 8.2708e-05%.

### Hybrid improvement versus physics-only

- Position error reduction: 98.0565%.
- Orientation error reduction: 98.0458%.

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

- Mean position MAE: 2.50867e-05 m.
- Trajectory standard deviation of position MAE: 2.09209e-05 m.
- Mean orientation MAE: 2.23081e-05 deg.
- Trajectory standard deviation of orientation MAE: 1.18213e-05 deg.
- Mean orientation MAE in radians: 3.8935e-07 rad.
- Mean position RMSE: 5.3904e-05 m.
- Mean orientation RMSE: 4.13204e-05 deg.
- Mean linear velocity MAE: 7.59609e-05 m/s.
- Mean linear velocity RMSE: 0.000140265 m/s.
- Mean angular velocity MAE: 1.16512e-06 rad/s.
- Mean angular velocity RMSE: 1.86659e-06 rad/s.
- Mean final position error: 5.90821e-05 m.
- Mean maximum position error: 0.000323885 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.00297531%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.000141899%.

### Hybrid improvement versus physics-only

- Position error reduction: 82.4316%.
- Orientation error reduction: 91.546%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

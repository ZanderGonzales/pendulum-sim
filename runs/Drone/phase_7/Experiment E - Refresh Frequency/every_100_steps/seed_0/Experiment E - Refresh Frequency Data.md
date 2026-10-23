# Experiment: Refresh Frequency

## Run: Every 100 steps

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

- Mean position MAE: 2.72404e-06 m.
- Trajectory standard deviation of position MAE: 1.26641e-06 m.
- Mean orientation MAE: 4.35691e-06 deg.
- Trajectory standard deviation of orientation MAE: 2.21118e-06 deg.
- Mean orientation MAE in radians: 7.60425e-08 rad.
- Mean position RMSE: 4.69991e-06 m.
- Mean orientation RMSE: 8.79986e-06 deg.
- Mean linear velocity MAE: 7.49821e-06 m/s.
- Mean linear velocity RMSE: 1.07022e-05 m/s.
- Mean angular velocity MAE: 2.15312e-07 rad/s.
- Mean angular velocity RMSE: 3.61306e-07 rad/s.
- Mean final position error: 1.67444e-06 m.
- Mean maximum position error: 2.10847e-05 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.000940428%.
- Orientation MAE as a percentage of MuJoCo angular travel: 7.30022e-05%.

### Hybrid improvement versus physics-only

- Position error reduction: 98.0374%.
- Orientation error reduction: 98.3053%.

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

- Mean position MAE: 3.00359e-05 m.
- Trajectory standard deviation of position MAE: 2.34285e-05 m.
- Mean orientation MAE: 2.12913e-05 deg.
- Trajectory standard deviation of orientation MAE: 1.28121e-05 deg.
- Mean orientation MAE in radians: 3.71603e-07 rad.
- Mean position RMSE: 6.52767e-05 m.
- Mean orientation RMSE: 3.7881e-05 deg.
- Mean linear velocity MAE: 8.94033e-05 m/s.
- Mean linear velocity RMSE: 0.00016649 m/s.
- Mean angular velocity MAE: 1.09824e-06 rad/s.
- Mean angular velocity RMSE: 1.69255e-06 rad/s.
- Mean final position error: 3.61099e-05 m.
- Mean maximum position error: 0.0003957 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.00354059%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.0001344%.

### Hybrid improvement versus physics-only

- Position error reduction: 78.9656%.
- Orientation error reduction: 91.9314%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

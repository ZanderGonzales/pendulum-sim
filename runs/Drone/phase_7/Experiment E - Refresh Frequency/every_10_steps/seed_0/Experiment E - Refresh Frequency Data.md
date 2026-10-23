# Experiment: Refresh Frequency

## Run: Every 10 steps

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

- Mean position MAE: 3.3889e-08 m.
- Trajectory standard deviation of position MAE: 1.60081e-08 m.
- Mean orientation MAE: 5.15467e-08 deg.
- Trajectory standard deviation of orientation MAE: 2.41027e-08 deg.
- Mean orientation MAE in radians: 8.9966e-10 rad.
- Mean position RMSE: 6.70905e-08 m.
- Mean orientation RMSE: 1.23479e-07 deg.
- Mean linear velocity MAE: 9.64376e-07 m/s.
- Mean linear velocity RMSE: 1.61958e-06 m/s.
- Mean angular velocity MAE: 2.55799e-08 rad/s.
- Mean angular velocity RMSE: 5.27076e-08 rad/s.
- Mean final position error: 1.94365e-08 m.
- Mean maximum position error: 6.19788e-07 m.
- Position MAE as a percentage of MuJoCo distance traveled: 1.18885e-05%.
- Orientation MAE as a percentage of MuJoCo angular travel: 8.20342e-07%.

### Hybrid improvement versus physics-only

- Position error reduction: 97.9022%.
- Orientation error reduction: 98.122%.

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

- Mean position MAE: 3.57018e-07 m.
- Trajectory standard deviation of position MAE: 2.62147e-07 m.
- Mean orientation MAE: 2.74739e-07 deg.
- Trajectory standard deviation of orientation MAE: 1.49806e-07 deg.
- Mean orientation MAE in radians: 4.7951e-09 rad.
- Mean position RMSE: 7.61414e-07 m.
- Mean orientation RMSE: 4.99778e-07 deg.
- Mean linear velocity MAE: 1.02233e-05 m/s.
- Mean linear velocity RMSE: 1.87842e-05 m/s.
- Mean angular velocity MAE: 1.37035e-07 rad/s.
- Mean angular velocity RMSE: 2.15098e-07 rad/s.
- Mean final position error: 7.20789e-08 m.
- Mean maximum position error: 5.23498e-06 m.
- Position MAE as a percentage of MuJoCo distance traveled: 4.23355e-05%.
- Orientation MAE as a percentage of MuJoCo angular travel: 1.74113e-06%.

### Hybrid improvement versus physics-only

- Position error reduction: 78.4189%.
- Orientation error reduction: 91.9913%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

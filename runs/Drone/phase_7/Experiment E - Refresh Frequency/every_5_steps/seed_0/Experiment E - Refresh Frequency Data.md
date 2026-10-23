# Experiment: Refresh Frequency

## Run: Every 5 steps

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

- Mean position MAE: 4.61582e-07 m.
- Trajectory standard deviation of position MAE: 3.11082e-07 m.
- Mean orientation MAE: 7.843e-07 deg.
- Trajectory standard deviation of orientation MAE: 6.45787e-07 deg.
- Mean orientation MAE in radians: 1.36886e-08 rad.
- Mean position RMSE: 8.85877e-07 m.
- Mean orientation RMSE: 1.43268e-06 deg.
- Mean linear velocity MAE: 2.51753e-05 m/s.
- Mean linear velocity RMSE: 4.19917e-05 m/s.
- Mean angular velocity MAE: 7.4646e-07 rad/s.
- Mean angular velocity RMSE: 1.18506e-06 rad/s.
- Mean final position error: 4.62601e-09 m.
- Mean maximum position error: 3.99778e-06 m.
- Position MAE as a percentage of MuJoCo distance traveled: 6.28772e-05%.
- Orientation MAE as a percentage of MuJoCo angular travel: 6.208e-06%.

### Physics + NN

- Mean position MAE: 9.64966e-09 m.
- Trajectory standard deviation of position MAE: 4.62166e-09 m.
- Mean orientation MAE: 1.46448e-08 deg.
- Trajectory standard deviation of orientation MAE: 6.811e-09 deg.
- Mean orientation MAE in radians: 2.556e-10 rad.
- Mean position RMSE: 1.86985e-08 m.
- Mean orientation RMSE: 3.44038e-08 deg.
- Mean linear velocity MAE: 5.27099e-07 m/s.
- Mean linear velocity RMSE: 8.80309e-07 m/s.
- Mean angular velocity MAE: 1.39653e-08 rad/s.
- Mean angular velocity RMSE: 2.85349e-08 rad/s.
- Mean final position error: 4.74041e-09 m.
- Mean maximum position error: 1.8723e-07 m.
- Position MAE as a percentage of MuJoCo distance traveled: 3.29038e-06%.
- Orientation MAE as a percentage of MuJoCo angular travel: 2.34043e-07%.

### Hybrid improvement versus physics-only

- Position error reduction: 97.9094%.
- Orientation error reduction: 98.1328%.

## Benchmark: recursive

### Physics only

- Mean position MAE: 4.72688e-07 m.
- Trajectory standard deviation of position MAE: 2.09246e-07 m.
- Mean orientation MAE: 9.82776e-07 deg.
- Trajectory standard deviation of orientation MAE: 2.70099e-07 deg.
- Mean orientation MAE in radians: 1.71527e-08 rad.
- Mean position RMSE: 9.20809e-07 m.
- Mean orientation RMSE: 1.56676e-06 deg.
- Mean linear velocity MAE: 2.57815e-05 m/s.
- Mean linear velocity RMSE: 4.36472e-05 m/s.
- Mean angular velocity MAE: 9.36008e-07 rad/s.
- Mean angular velocity RMSE: 1.29638e-06 rad/s.
- Mean final position error: 2.88312e-08 m.
- Mean maximum position error: 5.03878e-06 m.
- Position MAE as a percentage of MuJoCo distance traveled: 5.86556e-05%.
- Orientation MAE as a percentage of MuJoCo angular travel: 6.4907e-06%.

### Physics + NN

- Mean position MAE: 1.01895e-07 m.
- Trajectory standard deviation of position MAE: 7.49164e-08 m.
- Mean orientation MAE: 7.85528e-08 deg.
- Trajectory standard deviation of orientation MAE: 4.27607e-08 deg.
- Mean orientation MAE in radians: 1.371e-09 rad.
- Mean position RMSE: 2.11647e-07 m.
- Mean orientation RMSE: 1.39176e-07 deg.
- Mean linear velocity MAE: 5.58961e-06 m/s.
- Mean linear velocity RMSE: 1.00605e-05 m/s.
- Mean angular velocity MAE: 7.50003e-08 rad/s.
- Mean angular velocity RMSE: 1.15412e-07 rad/s.
- Mean final position error: 2.12728e-08 m.
- Mean maximum position error: 1.32164e-06 m.
- Position MAE as a percentage of MuJoCo distance traveled: 1.20789e-05%.
- Orientation MAE as a percentage of MuJoCo angular travel: 4.98061e-07%.

### Hybrid improvement versus physics-only

- Position error reduction: 78.4435%.
- Orientation error reduction: 92.0071%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

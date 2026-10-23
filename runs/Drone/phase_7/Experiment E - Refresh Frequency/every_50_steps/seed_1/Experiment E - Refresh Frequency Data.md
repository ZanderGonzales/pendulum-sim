# Experiment: Refresh Frequency

## Run: Every 50 steps

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

- Mean position MAE: 3.5806e-05 m.
- Trajectory standard deviation of position MAE: 2.40362e-05 m.
- Mean orientation MAE: 6.08885e-05 deg.
- Trajectory standard deviation of orientation MAE: 4.97478e-05 deg.
- Mean orientation MAE in radians: 1.0627e-06 rad.
- Mean position RMSE: 7.16866e-05 m.
- Mean orientation RMSE: 0.000112274 deg.
- Mean linear velocity MAE: 0.000212183 m/s.
- Mean linear velocity RMSE: 0.000365238 m/s.
- Mean angular velocity MAE: 6.32502e-06 rad/s.
- Mean angular velocity RMSE: 1.01903e-05 rad/s.
- Mean final position error: 1.019e-06 m.
- Mean maximum position error: 0.000382825 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.0048821%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.000491487%.

### Physics + NN

- Mean position MAE: 6.90834e-07 m.
- Trajectory standard deviation of position MAE: 2.76095e-07 m.
- Mean orientation MAE: 1.1192e-06 deg.
- Trajectory standard deviation of orientation MAE: 4.89721e-07 deg.
- Mean orientation MAE in radians: 1.95338e-08 rad.
- Mean position RMSE: 1.19007e-06 m.
- Mean orientation RMSE: 2.39028e-06 deg.
- Mean linear velocity MAE: 4.00124e-06 m/s.
- Mean linear velocity RMSE: 5.779e-06 m/s.
- Mean angular velocity MAE: 1.16796e-07 rad/s.
- Mean angular velocity RMSE: 2.24512e-07 rad/s.
- Mean final position error: 6.79858e-07 m.
- Mean maximum position error: 6.54739e-06 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.000285721%.
- Orientation MAE as a percentage of MuJoCo angular travel: 1.85906e-05%.

### Hybrid improvement versus physics-only

- Position error reduction: 98.0706%.
- Orientation error reduction: 98.1619%.

## Benchmark: recursive

### Physics only

- Mean position MAE: 3.67621e-05 m.
- Trajectory standard deviation of position MAE: 1.63052e-05 m.
- Mean orientation MAE: 7.18119e-05 deg.
- Trajectory standard deviation of orientation MAE: 1.97305e-05 deg.
- Mean orientation MAE in radians: 1.25335e-06 rad.
- Mean position RMSE: 7.40075e-05 m.
- Mean orientation RMSE: 0.000117271 deg.
- Mean linear velocity MAE: 0.000217848 m/s.
- Mean linear velocity RMSE: 0.000376329 m/s.
- Mean angular velocity MAE: 7.34825e-06 rad/s.
- Mean angular velocity RMSE: 1.03394e-05 rad/s.
- Mean final position error: 2.19669e-05 m.
- Mean maximum position error: 0.000411444 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.00456084%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.000474232%.

### Physics + NN

- Mean position MAE: 6.85785e-06 m.
- Trajectory standard deviation of position MAE: 5.59961e-06 m.
- Mean orientation MAE: 6.06109e-06 deg.
- Trajectory standard deviation of orientation MAE: 3.55057e-06 deg.
- Mean orientation MAE in radians: 1.05786e-07 rad.
- Mean position RMSE: 1.42791e-05 m.
- Mean orientation RMSE: 1.11055e-05 deg.
- Mean linear velocity MAE: 4.03406e-05 m/s.
- Mean linear velocity RMSE: 7.2257e-05 m/s.
- Mean angular velocity MAE: 6.18851e-07 rad/s.
- Mean angular velocity RMSE: 9.83489e-07 rad/s.
- Mean final position error: 5.53851e-06 m.
- Mean maximum position error: 8.65439e-05 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.000816136%.
- Orientation MAE as a percentage of MuJoCo angular travel: 3.83411e-05%.

### Hybrid improvement versus physics-only

- Position error reduction: 81.3453%.
- Orientation error reduction: 91.5598%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

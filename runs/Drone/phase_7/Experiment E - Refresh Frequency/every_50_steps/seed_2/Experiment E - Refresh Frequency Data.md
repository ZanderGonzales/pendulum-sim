# Experiment: Refresh Frequency

## Run: Every 50 steps

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

- Mean position MAE: 7.72484e-07 m.
- Trajectory standard deviation of position MAE: 3.25803e-07 m.
- Mean orientation MAE: 1.21816e-06 deg.
- Trajectory standard deviation of orientation MAE: 4.65685e-07 deg.
- Mean orientation MAE in radians: 2.12609e-08 rad.
- Mean position RMSE: 1.39478e-06 m.
- Mean orientation RMSE: 2.33226e-06 deg.
- Mean linear velocity MAE: 4.4652e-06 m/s.
- Mean linear velocity RMSE: 6.75e-06 m/s.
- Mean angular velocity MAE: 1.25217e-07 rad/s.
- Mean angular velocity RMSE: 2.12534e-07 rad/s.
- Mean final position error: 9.07154e-07 m.
- Mean maximum position error: 8.64925e-06 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.000289287%.
- Orientation MAE as a percentage of MuJoCo angular travel: 2.25204e-05%.

### Hybrid improvement versus physics-only

- Position error reduction: 97.8426%.
- Orientation error reduction: 97.9994%.

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

- Mean position MAE: 9.16985e-06 m.
- Trajectory standard deviation of position MAE: 6.74035e-06 m.
- Mean orientation MAE: 7.54099e-06 deg.
- Trajectory standard deviation of orientation MAE: 3.99682e-06 deg.
- Mean orientation MAE in radians: 1.31615e-07 rad.
- Mean position RMSE: 1.80748e-05 m.
- Mean orientation RMSE: 1.43776e-05 deg.
- Mean linear velocity MAE: 5.39408e-05 m/s.
- Mean linear velocity RMSE: 9.1272e-05 m/s.
- Mean angular velocity MAE: 7.7705e-07 rad/s.
- Mean angular velocity RMSE: 1.27664e-06 rad/s.
- Mean final position error: 6.80264e-06 m.
- Mean maximum position error: 0.000101422 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.00108843%.
- Orientation MAE as a percentage of MuJoCo angular travel: 4.78541e-05%.

### Hybrid improvement versus physics-only

- Position error reduction: 75.0562%.
- Orientation error reduction: 89.499%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

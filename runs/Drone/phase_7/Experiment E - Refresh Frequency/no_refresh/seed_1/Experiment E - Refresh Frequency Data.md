# Experiment: Refresh Frequency

## Run: No refresh

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

- Mean position MAE: 0.014326 m.
- Trajectory standard deviation of position MAE: 0.00579547 m.
- Mean orientation MAE: 0.00980406 deg.
- Trajectory standard deviation of orientation MAE: 0.00360809 deg.
- Mean orientation MAE in radians: 0.000171113 rad.
- Mean position RMSE: 0.0205988 m.
- Mean orientation RMSE: 0.0114208 deg.
- Mean linear velocity MAE: 0.00548276 m/s.
- Mean linear velocity RMSE: 0.00702697 m/s.
- Mean angular velocity MAE: 5.10332e-05 rad/s.
- Mean angular velocity RMSE: 5.48594e-05 rad/s.
- Mean final position error: 0.0512667 m.
- Mean maximum position error: 0.0512667 m.
- Position MAE as a percentage of MuJoCo distance traveled: 6.73386%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.186432%.

### Physics + NN

- Mean position MAE: 0.00044946 m.
- Trajectory standard deviation of position MAE: 0.000519224 m.
- Mean orientation MAE: 0.00039414 deg.
- Trajectory standard deviation of orientation MAE: 0.000349143 deg.
- Mean orientation MAE in radians: 6.87903e-06 rad.
- Mean position RMSE: 0.000647313 m.
- Mean orientation RMSE: 0.000475224 deg.
- Mean linear velocity MAE: 0.000176074 m/s.
- Mean linear velocity RMSE: 0.000231193 m/s.
- Mean angular velocity MAE: 1.64081e-06 rad/s.
- Mean angular velocity RMSE: 1.73754e-06 rad/s.
- Mean final position error: 0.00166337 m.
- Mean maximum position error: 0.00166337 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.143813%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00726775%.

### Hybrid improvement versus physics-only

- Position error reduction: 96.8626%.
- Orientation error reduction: 95.9798%.

## Benchmark: recursive

### Physics only

- Mean position MAE: 0.0121545 m.
- Trajectory standard deviation of position MAE: 0.00491539 m.
- Mean orientation MAE: 0.00732349 deg.
- Trajectory standard deviation of orientation MAE: 0.00280852 deg.
- Mean orientation MAE in radians: 0.000127819 rad.
- Mean position RMSE: 0.0173916 m.
- Mean orientation RMSE: 0.00846872 deg.
- Mean linear velocity MAE: 0.00464962 m/s.
- Mean linear velocity RMSE: 0.00594905 m/s.
- Mean angular velocity MAE: 2.90909e-05 rad/s.
- Mean angular velocity RMSE: 3.06901e-05 rad/s.
- Mean final position error: 0.0440691 m.
- Mean maximum position error: 0.0440691 m.
- Position MAE as a percentage of MuJoCo distance traveled: 1.6057%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.0488005%.

### Physics + NN

- Mean position MAE: 0.000988661 m.
- Trajectory standard deviation of position MAE: 0.000749946 m.
- Mean orientation MAE: 0.00090311 deg.
- Trajectory standard deviation of orientation MAE: 0.00039237 deg.
- Mean orientation MAE in radians: 1.57622e-05 rad.
- Mean position RMSE: 0.00140217 m.
- Mean orientation RMSE: 0.00121819 deg.
- Mean linear velocity MAE: 0.000420524 m/s.
- Mean linear velocity RMSE: 0.000551447 m/s.
- Mean angular velocity MAE: 5.49169e-06 rad/s.
- Mean angular velocity RMSE: 6.55448e-06 rad/s.
- Mean final position error: 0.00344532 m.
- Mean maximum position error: 0.00344532 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.12655%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00607089%.

### Hybrid improvement versus physics-only

- Position error reduction: 91.8659%.
- Orientation error reduction: 87.6683%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

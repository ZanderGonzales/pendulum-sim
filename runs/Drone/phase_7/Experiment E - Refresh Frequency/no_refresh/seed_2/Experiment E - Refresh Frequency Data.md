# Experiment: Refresh Frequency

## Run: No refresh

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

- Mean position MAE: 0.000408635 m.
- Trajectory standard deviation of position MAE: 0.00039975 m.
- Mean orientation MAE: 0.000354522 deg.
- Trajectory standard deviation of orientation MAE: 0.000312087 deg.
- Mean orientation MAE in radians: 6.18758e-06 rad.
- Mean position RMSE: 0.000588048 m.
- Mean orientation RMSE: 0.000437629 deg.
- Mean linear velocity MAE: 0.000162625 m/s.
- Mean linear velocity RMSE: 0.000216087 m/s.
- Mean angular velocity MAE: 1.63281e-06 rad/s.
- Mean angular velocity RMSE: 1.77878e-06 rad/s.
- Mean final position error: 0.00153018 m.
- Mean maximum position error: 0.00153018 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.231104%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00676656%.

### Hybrid improvement versus physics-only

- Position error reduction: 97.1476%.
- Orientation error reduction: 96.3839%.

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

- Mean position MAE: 0.00166432 m.
- Trajectory standard deviation of position MAE: 0.00134848 m.
- Mean orientation MAE: 0.00130332 deg.
- Trajectory standard deviation of orientation MAE: 0.000810249 deg.
- Mean orientation MAE in radians: 2.27473e-05 rad.
- Mean position RMSE: 0.00241091 m.
- Mean orientation RMSE: 0.00180927 deg.
- Mean linear velocity MAE: 0.000717766 m/s.
- Mean linear velocity RMSE: 0.000950918 m/s.
- Mean angular velocity MAE: 7.76651e-06 rad/s.
- Mean angular velocity RMSE: 9.48371e-06 rad/s.
- Mean final position error: 0.00617082 m.
- Mean maximum position error: 0.00617082 m.
- Position MAE as a percentage of MuJoCo distance traveled: 0.200657%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00816162%.

### Hybrid improvement versus physics-only

- Position error reduction: 86.307%.
- Orientation error reduction: 82.2035%.

## Artifacts

`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. `training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. `test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. `plots/` contains the large 3D comparison and position/orientation error panels. Experiment-level reports compare this condition with the other conditions using matched seeds.

[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).

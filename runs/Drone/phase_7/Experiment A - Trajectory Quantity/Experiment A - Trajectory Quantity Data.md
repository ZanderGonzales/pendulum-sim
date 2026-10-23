# Experiment: Trajectory Quantity

Nested, balanced source-order subsets vary training trajectory count. Network size and requested updates stay fixed.

All displayed run summaries use fully recursive forecasts. Positive comparison percentages mean less error; negative percentages mean more error. The comparison denominator is the named reference run. Seed means weight each training seed equally; each seed first weights each test flight equally.

[All pairwise percentages](<pairwise_comparisons.csv>).

[Comparison plot](<plots/comparison_mae.png>).

### Run: 10 broad trajectories

Artifacts: [10 broad trajectories](<broad_10/seed_0/>).

#### Training composition

- Training trajectories: 10.
- Hidden layers: 2.
- Neurons per hidden layer: 64.
- hover training trajectories: 2.
- climb_descent training trajectories: 2.
- figure_eight training trajectories: 2.
- circle training trajectories: 2.
- straight training trajectories: 2.

#### Test: mean across training seeds

- Mean position MAE against MuJoCo: **0.00284564 m**.
- Mean orientation MAE against MuJoCo: **0.00220939 deg**.
- Orientation MAE in radians: 3.85611e-05 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.745011%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.0305049%.
- Position error reduction versus physics-only: 80.1366%.
- Orientation error reduction versus physics-only: 77.4646%.
- Physics-only mean position MAE: **0.014326 m**.
- Physics-only mean orientation MAE: **0.00980406 deg**.
- Seed standard deviation of mean position MAE: 0.000210423 m.
- Seed standard deviation of mean orientation MAE: 0.000116103 deg.

#### Test: comparisons with other runs

- Position error reduction versus 20 broad trajectories: -171.341%.
- Orientation error reduction versus 20 broad trajectories: -168.646%.
- Position error reduction versus 40 broad trajectories: -323.776%.
- Orientation error reduction versus 40 broad trajectories: -318.844%.
- Position error reduction versus 80 broad trajectories: -577.605%.
- Orientation error reduction versus 80 broad trajectories: -537.653%.

#### Benchmark: mean across training seeds

- Mean position MAE against MuJoCo: **0.00387838 m**.
- Mean orientation MAE against MuJoCo: **0.00263208 deg**.
- Orientation MAE in radians: 4.59384e-05 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.515216%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.016303%.
- Position error reduction versus physics-only: 68.091%.
- Orientation error reduction versus physics-only: 64.0598%.
- Physics-only mean position MAE: **0.0121545 m**.
- Physics-only mean orientation MAE: **0.00732349 deg**.
- Seed standard deviation of mean position MAE: 0.000373893 m.
- Seed standard deviation of mean orientation MAE: 0.000437693 deg.

#### Benchmark: comparisons with other runs

- Position error reduction versus 20 broad trajectories: -125.315%.
- Orientation error reduction versus 20 broad trajectories: -84.962%.
- Position error reduction versus 40 broad trajectories: -151.509%.
- Orientation error reduction versus 40 broad trajectories: -112.121%.
- Position error reduction versus 80 broad trajectories: -202.448%.
- Orientation error reduction versus 80 broad trajectories: -173.264%.

#### Seed 0

- Actual source-training optimizer updates: 10,000.
- Completed source-training epochs: 250.
- Trainable parameters: 5,900.
- Source training time: 17.7002 s.
- Test mean position MAE: 0.002699 m.
- Test mean orientation MAE: 0.00207868 deg.
- Benchmark mean position MAE: 0.00354391 m.
- Benchmark mean orientation MAE: 0.0021347 deg.

Detailed seed report: [Experiment A - Trajectory Quantity Data.md](<broad_10/seed_0/Experiment A - Trajectory Quantity Data.md>).

#### Seed 1

- Actual source-training optimizer updates: 10,000.
- Completed source-training epochs: 250.
- Trainable parameters: 5,900.
- Source training time: 13.4060 s.
- Test mean position MAE: 0.00269471 m.
- Test mean orientation MAE: 0.00218868 deg.
- Benchmark mean position MAE: 0.00369093 m.
- Benchmark mean orientation MAE: 0.00256167 deg.

Detailed seed report: [Experiment A - Trajectory Quantity Data.md](<broad_10/seed_1/Experiment A - Trajectory Quantity Data.md>).

#### Seed 2

- Actual source-training optimizer updates: 10,000.
- Completed source-training epochs: 250.
- Trainable parameters: 5,900.
- Source training time: 9.1248 s.
- Test mean position MAE: 0.00314322 m.
- Test mean orientation MAE: 0.0023608 deg.
- Benchmark mean position MAE: 0.00440028 m.
- Benchmark mean orientation MAE: 0.00319987 deg.

Detailed seed report: [Experiment A - Trajectory Quantity Data.md](<broad_10/seed_2/Experiment A - Trajectory Quantity Data.md>).

### Run: 20 broad trajectories

Artifacts: [20 broad trajectories](<broad_20/seed_0/>).

#### Training composition

- Training trajectories: 20.
- Hidden layers: 2.
- Neurons per hidden layer: 64.
- hover training trajectories: 4.
- climb_descent training trajectories: 4.
- figure_eight training trajectories: 4.
- circle training trajectories: 4.
- straight training trajectories: 4.

#### Test: mean across training seeds

- Mean position MAE against MuJoCo: **0.00104873 m**.
- Mean orientation MAE against MuJoCo: **0.000822415 deg**.
- Orientation MAE in radians: 1.43539e-05 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.37421%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.0141899%.
- Position error reduction versus physics-only: 92.6795%.
- Orientation error reduction versus physics-only: 91.6115%.
- Physics-only mean position MAE: **0.014326 m**.
- Physics-only mean orientation MAE: **0.00980406 deg**.
- Seed standard deviation of mean position MAE: 1.06258e-05 m.
- Seed standard deviation of mean orientation MAE: 1.73849e-05 deg.

#### Test: comparisons with other runs

- Position error reduction versus 10 broad trajectories: 63.146%.
- Orientation error reduction versus 10 broad trajectories: 62.7763%.
- Position error reduction versus 40 broad trajectories: -56.1784%.
- Orientation error reduction versus 40 broad trajectories: -55.9092%.
- Position error reduction versus 80 broad trajectories: -149.725%.
- Orientation error reduction versus 80 broad trajectories: -137.358%.

#### Benchmark: mean across training seeds

- Mean position MAE against MuJoCo: **0.00172131 m**.
- Mean orientation MAE against MuJoCo: **0.00142304 deg**.
- Orientation MAE in radians: 2.48367e-05 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.217925%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00919873%.
- Position error reduction versus physics-only: 85.8381%.
- Orientation error reduction versus physics-only: 80.5689%.
- Physics-only mean position MAE: **0.0121545 m**.
- Physics-only mean orientation MAE: **0.00732349 deg**.
- Seed standard deviation of mean position MAE: 0.000110878 m.
- Seed standard deviation of mean orientation MAE: 0.000107762 deg.

#### Benchmark: comparisons with other runs

- Position error reduction versus 10 broad trajectories: 55.6178%.
- Orientation error reduction versus 10 broad trajectories: 45.9348%.
- Position error reduction versus 40 broad trajectories: -11.6253%.
- Orientation error reduction versus 40 broad trajectories: -14.6838%.
- Position error reduction versus 80 broad trajectories: -34.2331%.
- Orientation error reduction versus 80 broad trajectories: -47.7406%.

#### Seed 0

- Actual source-training optimizer updates: 10,033.
- Completed source-training epochs: 127.
- Trainable parameters: 5,900.
- Source training time: 12.2007 s.
- Test mean position MAE: 0.0010384 m.
- Test mean orientation MAE: 0.0008018 deg.
- Benchmark mean position MAE: 0.00185227 m.
- Benchmark mean orientation MAE: 0.00127773 deg.

Detailed seed report: [Experiment A - Trajectory Quantity Data.md](<broad_20/seed_0/Experiment A - Trajectory Quantity Data.md>).

#### Seed 1

- Actual source-training optimizer updates: 10,033.
- Completed source-training epochs: 127.
- Trainable parameters: 5,900.
- Source training time: 12.0278 s.
- Test mean position MAE: 0.00104445 m.
- Test mean orientation MAE: 0.000844325 deg.
- Benchmark mean position MAE: 0.00158115 m.
- Benchmark mean orientation MAE: 0.00153547 deg.

Detailed seed report: [Experiment A - Trajectory Quantity Data.md](<broad_20/seed_1/Experiment A - Trajectory Quantity Data.md>).

#### Seed 2

- Actual source-training optimizer updates: 10,033.
- Completed source-training epochs: 127.
- Trainable parameters: 5,900.
- Source training time: 9.3572 s.
- Test mean position MAE: 0.00106335 m.
- Test mean orientation MAE: 0.00082112 deg.
- Benchmark mean position MAE: 0.00173051 m.
- Benchmark mean orientation MAE: 0.00145591 deg.

Detailed seed report: [Experiment A - Trajectory Quantity Data.md](<broad_20/seed_2/Experiment A - Trajectory Quantity Data.md>).

### Run: 40 broad trajectories

Artifacts: [40 broad trajectories](<broad_40/seed_0/>).

#### Training composition

- Training trajectories: 40.
- Hidden layers: 2.
- Neurons per hidden layer: 64.
- hover training trajectories: 8.
- climb_descent training trajectories: 8.
- figure_eight training trajectories: 8.
- circle training trajectories: 8.
- straight training trajectories: 8.

#### Test: mean across training seeds

- Mean position MAE against MuJoCo: **0.000671497 m**.
- Mean orientation MAE against MuJoCo: **0.000527496 deg**.
- Orientation MAE in radians: 9.20655e-06 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.283274%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00793248%.
- Position error reduction versus physics-only: 95.3128%.
- Orientation error reduction versus physics-only: 94.6196%.
- Physics-only mean position MAE: **0.014326 m**.
- Physics-only mean orientation MAE: **0.00980406 deg**.
- Seed standard deviation of mean position MAE: 7.65059e-05 m.
- Seed standard deviation of mean orientation MAE: 1.2898e-05 deg.

#### Test: comparisons with other runs

- Position error reduction versus 10 broad trajectories: 76.4026%.
- Orientation error reduction versus 10 broad trajectories: 76.1248%.
- Position error reduction versus 20 broad trajectories: 35.9707%.
- Orientation error reduction versus 20 broad trajectories: 35.8601%.
- Position error reduction versus 80 broad trajectories: -59.8971%.
- Orientation error reduction versus 80 broad trajectories: -52.241%.

#### Benchmark: mean across training seeds

- Mean position MAE against MuJoCo: **0.00154204 m**.
- Mean orientation MAE against MuJoCo: **0.00124084 deg**.
- Orientation MAE in radians: 2.16567e-05 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.195035%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.0077864%.
- Position error reduction versus physics-only: 87.313%.
- Orientation error reduction versus physics-only: 83.0568%.
- Physics-only mean position MAE: **0.0121545 m**.
- Physics-only mean orientation MAE: **0.00732349 deg**.
- Seed standard deviation of mean position MAE: 0.000165721 m.
- Seed standard deviation of mean orientation MAE: 0.000141297 deg.

#### Benchmark: comparisons with other runs

- Position error reduction versus 10 broad trajectories: 60.24%.
- Orientation error reduction versus 10 broad trajectories: 52.8572%.
- Position error reduction versus 20 broad trajectories: 10.4146%.
- Orientation error reduction versus 20 broad trajectories: 12.8037%.
- Position error reduction versus 80 broad trajectories: -20.2532%.
- Orientation error reduction versus 80 broad trajectories: -28.8243%.

#### Seed 0

- Actual source-training optimizer updates: 10,048.
- Completed source-training epochs: 64.
- Trainable parameters: 5,900.
- Source training time: 10.5970 s.
- Test mean position MAE: 0.000582463 m.
- Test mean orientation MAE: 0.000515371 deg.
- Benchmark mean position MAE: 0.00146765 m.
- Benchmark mean orientation MAE: 0.00104232 deg.

Detailed seed report: [Experiment A - Trajectory Quantity Data.md](<broad_40/seed_0/Experiment A - Trajectory Quantity Data.md>).

#### Seed 1

- Actual source-training optimizer updates: 10,048.
- Completed source-training epochs: 64.
- Trainable parameters: 5,900.
- Source training time: 11.3581 s.
- Test mean position MAE: 0.000662775 m.
- Test mean orientation MAE: 0.000521758 deg.
- Benchmark mean position MAE: 0.00138677 m.
- Benchmark mean orientation MAE: 0.0013599 deg.

Detailed seed report: [Experiment A - Trajectory Quantity Data.md](<broad_40/seed_1/Experiment A - Trajectory Quantity Data.md>).

#### Seed 2

- Actual source-training optimizer updates: 10,048.
- Completed source-training epochs: 64.
- Trainable parameters: 5,900.
- Source training time: 11.1440 s.
- Test mean position MAE: 0.000769253 m.
- Test mean orientation MAE: 0.00054536 deg.
- Benchmark mean position MAE: 0.00177171 m.
- Benchmark mean orientation MAE: 0.00132028 deg.

Detailed seed report: [Experiment A - Trajectory Quantity Data.md](<broad_40/seed_2/Experiment A - Trajectory Quantity Data.md>).

### Run: 80 broad trajectories

Artifacts: [80 broad trajectories](<broad_80/seed_0/>).

#### Training composition

- Training trajectories: 80.
- Hidden layers: 2.
- Neurons per hidden layer: 64.
- hover training trajectories: 16.
- climb_descent training trajectories: 16.
- figure_eight training trajectories: 16.
- circle training trajectories: 16.
- straight training trajectories: 16.

#### Test: mean across training seeds

- Mean position MAE against MuJoCo: **0.000419956 m**.
- Mean orientation MAE against MuJoCo: **0.000346488 deg**.
- Orientation MAE in radians: 6.04735e-06 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.177761%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00645881%.
- Position error reduction versus physics-only: 97.0686%.
- Orientation error reduction versus physics-only: 96.4659%.
- Physics-only mean position MAE: **0.014326 m**.
- Physics-only mean orientation MAE: **0.00980406 deg**.
- Seed standard deviation of mean position MAE: 2.10501e-05 m.
- Seed standard deviation of mean orientation MAE: 4.25686e-05 deg.

#### Test: comparisons with other runs

- Position error reduction versus 10 broad trajectories: 85.2422%.
- Orientation error reduction versus 10 broad trajectories: 84.3175%.
- Position error reduction versus 20 broad trajectories: 59.9559%.
- Orientation error reduction versus 20 broad trajectories: 57.8695%.
- Position error reduction versus 40 broad trajectories: 37.4598%.
- Orientation error reduction versus 40 broad trajectories: 34.3147%.

#### Benchmark: mean across training seeds

- Mean position MAE against MuJoCo: **0.00128233 m**.
- Mean orientation MAE against MuJoCo: **0.0009632 deg**.
- Orientation MAE in radians: 1.6811e-05 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.157651%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00620006%.
- Position error reduction versus physics-only: 89.4497%.
- Orientation error reduction versus physics-only: 86.8478%.
- Physics-only mean position MAE: **0.0121545 m**.
- Physics-only mean orientation MAE: **0.00732349 deg**.
- Seed standard deviation of mean position MAE: 0.000282818 m.
- Seed standard deviation of mean orientation MAE: 0.000256719 deg.

#### Benchmark: comparisons with other runs

- Position error reduction versus 10 broad trajectories: 66.9364%.
- Orientation error reduction versus 10 broad trajectories: 63.4053%.
- Position error reduction versus 20 broad trajectories: 25.5027%.
- Orientation error reduction versus 20 broad trajectories: 32.3138%.
- Position error reduction versus 40 broad trajectories: 16.8422%.
- Orientation error reduction versus 40 broad trajectories: 22.3749%.

#### Seed 0

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 13.3145 s.
- Test mean position MAE: 0.000401772 m.
- Test mean orientation MAE: 0.000290801 deg.
- Benchmark mean position MAE: 0.00119401 m.
- Benchmark mean orientation MAE: 0.000683165 deg.

Detailed seed report: [Experiment A - Trajectory Quantity Data.md](<broad_80/seed_0/Experiment A - Trajectory Quantity Data.md>).

#### Seed 1

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 13.0851 s.
- Test mean position MAE: 0.00044946 m.
- Test mean orientation MAE: 0.00039414 deg.
- Benchmark mean position MAE: 0.000988661 m.
- Benchmark mean orientation MAE: 0.00090311 deg.

Detailed seed report: [Experiment A - Trajectory Quantity Data.md](<broad_80/seed_1/Experiment A - Trajectory Quantity Data.md>).

#### Seed 2

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 12.4214 s.
- Test mean position MAE: 0.000408635 m.
- Test mean orientation MAE: 0.000354522 deg.
- Benchmark mean position MAE: 0.00166432 m.
- Benchmark mean orientation MAE: 0.00130332 deg.

Detailed seed report: [Experiment A - Trajectory Quantity Data.md](<broad_80/seed_2/Experiment A - Trajectory Quantity Data.md>).


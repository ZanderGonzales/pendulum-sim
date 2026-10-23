# Experiment: Optimizer Updates

Only the requested optimizer-update budget changes. Dataset, architecture, optimizer, and evaluation flights stay fixed.

All displayed run summaries use fully recursive forecasts. Positive comparison percentages mean less error; negative percentages mean more error. The comparison denominator is the named reference run. Seed means weight each training seed equally; each seed first weights each test flight equally.

[All pairwise percentages](<pairwise_comparisons.csv>).

[Comparison plot](<plots/comparison_mae.png>).

### Run: 5,000 requested optimizer updates

Artifacts: [5,000 requested optimizer updates](<updates_5000/seed_0/>).

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

- Mean position MAE against MuJoCo: **0.000582882 m**.
- Mean orientation MAE against MuJoCo: **0.000478322 deg**.
- Orientation MAE in radians: 8.3483e-06 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.24569%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00934327%.
- Position error reduction versus physics-only: 95.9313%.
- Orientation error reduction versus physics-only: 95.1212%.
- Physics-only mean position MAE: **0.014326 m**.
- Physics-only mean orientation MAE: **0.00980406 deg**.
- Seed standard deviation of mean position MAE: 2.77215e-05 m.
- Seed standard deviation of mean orientation MAE: 3.88874e-05 deg.

#### Test: comparisons with other runs

- Position error reduction versus 10,000 requested optimizer updates: -38.796%.
- Orientation error reduction versus 10,000 requested optimizer updates: -38.0488%.
- Position error reduction versus 15,000 requested optimizer updates: -66.3056%.
- Orientation error reduction versus 15,000 requested optimizer updates: -55.2117%.
- Position error reduction versus 20,000 requested optimizer updates: -101.303%.
- Orientation error reduction versus 20,000 requested optimizer updates: -110.482%.

#### Benchmark: mean across training seeds

- Mean position MAE against MuJoCo: **0.00177977 m**.
- Mean orientation MAE against MuJoCo: **0.00107803 deg**.
- Orientation MAE in radians: 1.88151e-05 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.223466%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00689127%.
- Position error reduction versus physics-only: 85.3571%.
- Orientation error reduction versus physics-only: 85.2799%.
- Physics-only mean position MAE: **0.0121545 m**.
- Physics-only mean orientation MAE: **0.00732349 deg**.
- Seed standard deviation of mean position MAE: 0.000123136 m.
- Seed standard deviation of mean orientation MAE: 0.000255966 deg.

#### Benchmark: comparisons with other runs

- Position error reduction versus 10,000 requested optimizer updates: -38.7923%.
- Orientation error reduction versus 10,000 requested optimizer updates: -11.9213%.
- Position error reduction versus 15,000 requested optimizer updates: -57.0749%.
- Orientation error reduction versus 15,000 requested optimizer updates: -22.5712%.
- Position error reduction versus 20,000 requested optimizer updates: -66.887%.
- Orientation error reduction versus 20,000 requested optimizer updates: -32.6643%.

#### Seed 0

- Actual source-training optimizer updates: 5,008.
- Completed source-training epochs: 16.
- Trainable parameters: 5,900.
- Source training time: 7.0837 s.
- Test mean position MAE: 0.000582118 m.
- Test mean orientation MAE: 0.000485355 deg.
- Benchmark mean position MAE: 0.00175447 m.
- Benchmark mean orientation MAE: 0.00074604 deg.

Detailed seed report: [Experiment C - Optimizer Updates Data.md](<updates_5000/seed_0/Experiment C - Optimizer Updates Data.md>).

#### Seed 1

- Actual source-training optimizer updates: 5,008.
- Completed source-training epochs: 16.
- Trainable parameters: 5,900.
- Source training time: 7.4764 s.
- Test mean position MAE: 0.000617209 m.
- Test mean orientation MAE: 0.000522042 deg.
- Benchmark mean position MAE: 0.00164322 m.
- Benchmark mean orientation MAE: 0.00111905 deg.

Detailed seed report: [Experiment C - Optimizer Updates Data.md](<updates_5000/seed_1/Experiment C - Optimizer Updates Data.md>).

#### Seed 2

- Actual source-training optimizer updates: 5,008.
- Completed source-training epochs: 16.
- Trainable parameters: 5,900.
- Source training time: 6.3296 s.
- Test mean position MAE: 0.000549319 m.
- Test mean orientation MAE: 0.00042757 deg.
- Benchmark mean position MAE: 0.00194164 m.
- Benchmark mean orientation MAE: 0.00136899 deg.

Detailed seed report: [Experiment C - Optimizer Updates Data.md](<updates_5000/seed_2/Experiment C - Optimizer Updates Data.md>).

### Run: 10,000 requested optimizer updates

Artifacts: [10,000 requested optimizer updates](<../Experiment A - Trajectory Quantity/broad_80/seed_0/>).

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

- Position error reduction versus 5,000 requested optimizer updates: 27.9518%.
- Orientation error reduction versus 5,000 requested optimizer updates: 27.5619%.
- Position error reduction versus 15,000 requested optimizer updates: -19.8201%.
- Orientation error reduction versus 15,000 requested optimizer updates: -12.4325%.
- Position error reduction versus 20,000 requested optimizer updates: -45.0348%.
- Orientation error reduction versus 20,000 requested optimizer updates: -52.4696%.

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

- Position error reduction versus 5,000 requested optimizer updates: 27.9499%.
- Orientation error reduction versus 5,000 requested optimizer updates: 10.6515%.
- Position error reduction versus 15,000 requested optimizer updates: -13.1727%.
- Orientation error reduction versus 15,000 requested optimizer updates: -9.51554%.
- Position error reduction versus 20,000 requested optimizer updates: -20.2423%.
- Orientation error reduction versus 20,000 requested optimizer updates: -18.5336%.

#### Seed 0

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 13.3145 s.
- Test mean position MAE: 0.000401772 m.
- Test mean orientation MAE: 0.000290801 deg.
- Benchmark mean position MAE: 0.00119401 m.
- Benchmark mean orientation MAE: 0.000683165 deg.

Detailed seed report: [Experiment A - Trajectory Quantity Data.md](<../Experiment A - Trajectory Quantity/broad_80/seed_0/Experiment A - Trajectory Quantity Data.md>).

#### Seed 1

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 13.0851 s.
- Test mean position MAE: 0.00044946 m.
- Test mean orientation MAE: 0.00039414 deg.
- Benchmark mean position MAE: 0.000988661 m.
- Benchmark mean orientation MAE: 0.00090311 deg.

Detailed seed report: [Experiment A - Trajectory Quantity Data.md](<../Experiment A - Trajectory Quantity/broad_80/seed_1/Experiment A - Trajectory Quantity Data.md>).

#### Seed 2

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 12.4214 s.
- Test mean position MAE: 0.000408635 m.
- Test mean orientation MAE: 0.000354522 deg.
- Benchmark mean position MAE: 0.00166432 m.
- Benchmark mean orientation MAE: 0.00130332 deg.

Detailed seed report: [Experiment A - Trajectory Quantity Data.md](<../Experiment A - Trajectory Quantity/broad_80/seed_2/Experiment A - Trajectory Quantity Data.md>).

### Run: 15,000 requested optimizer updates

Artifacts: [15,000 requested optimizer updates](<updates_15000/seed_0/>).

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

- Mean position MAE against MuJoCo: **0.000350489 m**.
- Mean orientation MAE against MuJoCo: **0.000308174 deg**.
- Orientation MAE in radians: 5.37865e-06 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.1282%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.005125%.
- Position error reduction versus physics-only: 97.5535%.
- Orientation error reduction versus physics-only: 96.8567%.
- Physics-only mean position MAE: **0.014326 m**.
- Physics-only mean orientation MAE: **0.00980406 deg**.
- Seed standard deviation of mean position MAE: 2.3117e-05 m.
- Seed standard deviation of mean orientation MAE: 3.7203e-05 deg.

#### Test: comparisons with other runs

- Position error reduction versus 5,000 requested optimizer updates: 39.8697%.
- Orientation error reduction versus 5,000 requested optimizer updates: 35.5719%.
- Position error reduction versus 10,000 requested optimizer updates: 16.5416%.
- Orientation error reduction versus 10,000 requested optimizer updates: 11.0577%.
- Position error reduction versus 20,000 requested optimizer updates: -21.0438%.
- Orientation error reduction versus 20,000 requested optimizer updates: -35.6099%.

#### Benchmark: mean across training seeds

- Mean position MAE against MuJoCo: **0.00113307 m**.
- Mean orientation MAE against MuJoCo: **0.000879509 deg**.
- Orientation MAE in radians: 1.53503e-05 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.139084%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00566101%.
- Position error reduction versus physics-only: 90.6777%.
- Orientation error reduction versus physics-only: 87.9906%.
- Physics-only mean position MAE: **0.0121545 m**.
- Physics-only mean orientation MAE: **0.00732349 deg**.
- Seed standard deviation of mean position MAE: 0.000225233 m.
- Seed standard deviation of mean orientation MAE: 0.000199671 deg.

#### Benchmark: comparisons with other runs

- Position error reduction versus 5,000 requested optimizer updates: 36.3361%.
- Orientation error reduction versus 5,000 requested optimizer updates: 18.4148%.
- Position error reduction versus 10,000 requested optimizer updates: 11.6395%.
- Orientation error reduction versus 10,000 requested optimizer updates: 8.68876%.
- Position error reduction versus 20,000 requested optimizer updates: -6.24676%.
- Orientation error reduction versus 20,000 requested optimizer updates: -8.23449%.

#### Seed 0

- Actual source-training optimizer updates: 15,024.
- Completed source-training epochs: 48.
- Trainable parameters: 5,900.
- Source training time: 19.4095 s.
- Test mean position MAE: 0.000320074 m.
- Test mean orientation MAE: 0.000256141 deg.
- Benchmark mean position MAE: 0.00106874 m.
- Benchmark mean orientation MAE: 0.000658234 deg.

Detailed seed report: [Experiment C - Optimizer Updates Data.md](<updates_15000/seed_0/Experiment C - Optimizer Updates Data.md>).

#### Seed 1

- Actual source-training optimizer updates: 15,024.
- Completed source-training epochs: 48.
- Trainable parameters: 5,900.
- Source training time: 25.9722 s.
- Test mean position MAE: 0.000355313 m.
- Test mean orientation MAE: 0.000340938 deg.
- Benchmark mean position MAE: 0.000895068 m.
- Benchmark mean orientation MAE: 0.000838223 deg.

Detailed seed report: [Experiment C - Optimizer Updates Data.md](<updates_15000/seed_1/Experiment C - Optimizer Updates Data.md>).

#### Seed 2

- Actual source-training optimizer updates: 15,024.
- Completed source-training epochs: 48.
- Trainable parameters: 5,900.
- Source training time: 21.9645 s.
- Test mean position MAE: 0.000376079 m.
- Test mean orientation MAE: 0.000327443 deg.
- Benchmark mean position MAE: 0.00143541 m.
- Benchmark mean orientation MAE: 0.00114207 deg.

Detailed seed report: [Experiment C - Optimizer Updates Data.md](<updates_15000/seed_2/Experiment C - Optimizer Updates Data.md>).

### Run: 20,000 requested optimizer updates

Artifacts: [20,000 requested optimizer updates](<updates_20000/seed_0/>).

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

- Mean position MAE against MuJoCo: **0.000289555 m**.
- Mean orientation MAE against MuJoCo: **0.00022725 deg**.
- Orientation MAE in radians: 3.96627e-06 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.0975726%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00370492%.
- Position error reduction versus physics-only: 97.9788%.
- Orientation error reduction versus physics-only: 97.6821%.
- Physics-only mean position MAE: **0.014326 m**.
- Physics-only mean orientation MAE: **0.00980406 deg**.
- Seed standard deviation of mean position MAE: 1.09759e-05 m.
- Seed standard deviation of mean orientation MAE: 1.83626e-05 deg.

#### Test: comparisons with other runs

- Position error reduction versus 5,000 requested optimizer updates: 50.3235%.
- Orientation error reduction versus 5,000 requested optimizer updates: 52.4901%.
- Position error reduction versus 10,000 requested optimizer updates: 31.051%.
- Orientation error reduction versus 10,000 requested optimizer updates: 34.4131%.
- Position error reduction versus 15,000 requested optimizer updates: 17.3853%.
- Orientation error reduction versus 15,000 requested optimizer updates: 26.2591%.

#### Benchmark: mean across training seeds

- Mean position MAE against MuJoCo: **0.00106645 m**.
- Mean orientation MAE against MuJoCo: **0.000812596 deg**.
- Orientation MAE in radians: 1.41825e-05 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.130861%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00525133%.
- Position error reduction versus physics-only: 91.2258%.
- Orientation error reduction versus physics-only: 88.9042%.
- Physics-only mean position MAE: **0.0121545 m**.
- Physics-only mean orientation MAE: **0.00732349 deg**.
- Seed standard deviation of mean position MAE: 0.000153741 m.
- Seed standard deviation of mean orientation MAE: 0.000166727 deg.

#### Benchmark: comparisons with other runs

- Position error reduction versus 5,000 requested optimizer updates: 40.0792%.
- Orientation error reduction versus 5,000 requested optimizer updates: 24.6218%.
- Position error reduction versus 10,000 requested optimizer updates: 16.8346%.
- Orientation error reduction versus 10,000 requested optimizer updates: 15.6357%.
- Position error reduction versus 15,000 requested optimizer updates: 5.87948%.
- Orientation error reduction versus 15,000 requested optimizer updates: 7.60801%.

#### Seed 0

- Actual source-training optimizer updates: 20,032.
- Completed source-training epochs: 64.
- Trainable parameters: 5,900.
- Source training time: 30.6880 s.
- Test mean position MAE: 0.000284956 m.
- Test mean orientation MAE: 0.000247183 deg.
- Benchmark mean position MAE: 0.001023 m.
- Benchmark mean orientation MAE: 0.000605751 deg.

Detailed seed report: [Experiment C - Optimizer Updates Data.md](<updates_20000/seed_0/Experiment C - Optimizer Updates Data.md>).

#### Seed 1

- Actual source-training optimizer updates: 20,032.
- Completed source-training epochs: 64.
- Trainable parameters: 5,900.
- Source training time: 23.9397 s.
- Test mean position MAE: 0.000279016 m.
- Test mean orientation MAE: 0.000231699 deg.
- Benchmark mean position MAE: 0.000903684 m.
- Benchmark mean orientation MAE: 0.000817998 deg.

Detailed seed report: [Experiment C - Optimizer Updates Data.md](<updates_20000/seed_1/Experiment C - Optimizer Updates Data.md>).

#### Seed 2

- Actual source-training optimizer updates: 20,032.
- Completed source-training epochs: 64.
- Trainable parameters: 5,900.
- Source training time: 25.0690 s.
- Test mean position MAE: 0.000304694 m.
- Test mean orientation MAE: 0.000202869 deg.
- Benchmark mean position MAE: 0.00127267 m.
- Benchmark mean orientation MAE: 0.00101404 deg.

Detailed seed report: [Experiment C - Optimizer Updates Data.md](<updates_20000/seed_2/Experiment C - Optimizer Updates Data.md>).


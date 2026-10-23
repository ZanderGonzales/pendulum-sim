# Experiment: Trajectory Variety

Both conditions use the same training count and flight duration. Restricted data contain circles and figure-eights; broad data cover all main families. Validation and test flights are identical.

All displayed run summaries use fully recursive forecasts. Positive comparison percentages mean less error; negative percentages mean more error. The comparison denominator is the named reference run. Seed means weight each training seed equally; each seed first weights each test flight equally.

[All pairwise percentages](<pairwise_comparisons.csv>).

[Comparison plot](<plots/comparison_mae.png>).

### Run: 20 restricted trajectories

Artifacts: [20 restricted trajectories](<restricted_20/seed_0/>).

#### Training composition

- Training trajectories: 20.
- Hidden layers: 2.
- Neurons per hidden layer: 64.
- figure_eight training trajectories: 10.
- circle training trajectories: 10.

#### Test: mean across training seeds

- Mean position MAE against MuJoCo: **0.00517228 m**.
- Mean orientation MAE against MuJoCo: **0.00450522 deg**.
- Orientation MAE in radians: 7.86309e-05 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 1.37106%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.174504%.
- Position error reduction versus physics-only: 63.896%.
- Orientation error reduction versus physics-only: 54.0474%.
- Physics-only mean position MAE: **0.014326 m**.
- Physics-only mean orientation MAE: **0.00980406 deg**.
- Seed standard deviation of mean position MAE: 0.001217 m.
- Seed standard deviation of mean orientation MAE: 0.000957972 deg.

#### Test: comparisons with other runs

- Position error reduction versus 20 broad trajectories: -393.193%.
- Orientation error reduction versus 20 broad trajectories: -447.804%.

#### Benchmark: mean across training seeds

- Mean position MAE against MuJoCo: **0.00974245 m**.
- Mean orientation MAE against MuJoCo: **0.00896993 deg**.
- Orientation MAE in radians: 0.000156555 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 1.42743%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.0638298%.
- Position error reduction versus physics-only: 19.8448%.
- Orientation error reduction versus physics-only: -22.4816%.
- Physics-only mean position MAE: **0.0121545 m**.
- Physics-only mean orientation MAE: **0.00732349 deg**.
- Seed standard deviation of mean position MAE: 0.00267364 m.
- Seed standard deviation of mean orientation MAE: 0.00135982 deg.

#### Benchmark: comparisons with other runs

- Position error reduction versus 20 broad trajectories: -465.99%.
- Orientation error reduction versus 20 broad trajectories: -530.337%.

#### Seed 0

- Actual source-training optimizer updates: 10,033.
- Completed source-training epochs: 127.
- Trainable parameters: 5,900.
- Source training time: 9.4645 s.
- Test mean position MAE: 0.00351851 m.
- Test mean orientation MAE: 0.00325217 deg.
- Benchmark mean position MAE: 0.00664359 m.
- Benchmark mean orientation MAE: 0.00773326 deg.

Detailed seed report: [Experiment B - Trajectory Variety Data.md](<restricted_20/seed_0/Experiment B - Trajectory Variety Data.md>).

#### Seed 1

- Actual source-training optimizer updates: 10,033.
- Completed source-training epochs: 127.
- Trainable parameters: 5,900.
- Source training time: 9.5200 s.
- Test mean position MAE: 0.00641199 m.
- Test mean orientation MAE: 0.00557779 deg.
- Benchmark mean position MAE: 0.0131681 m.
- Benchmark mean orientation MAE: 0.0108637 deg.

Detailed seed report: [Experiment B - Trajectory Variety Data.md](<restricted_20/seed_1/Experiment B - Trajectory Variety Data.md>).

#### Seed 2

- Actual source-training optimizer updates: 10,033.
- Completed source-training epochs: 127.
- Trainable parameters: 5,900.
- Source training time: 9.8430 s.
- Test mean position MAE: 0.00558632 m.
- Test mean orientation MAE: 0.00468571 deg.
- Benchmark mean position MAE: 0.00941562 m.
- Benchmark mean orientation MAE: 0.00831285 deg.

Detailed seed report: [Experiment B - Trajectory Variety Data.md](<restricted_20/seed_2/Experiment B - Trajectory Variety Data.md>).

### Run: 20 broad trajectories

Artifacts: [20 broad trajectories](<../Experiment A - Trajectory Quantity/broad_20/seed_0/>).

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

- Position error reduction versus 20 restricted trajectories: 79.7239%.
- Orientation error reduction versus 20 restricted trajectories: 81.7453%.

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

- Position error reduction versus 20 restricted trajectories: 82.3319%.
- Orientation error reduction versus 20 restricted trajectories: 84.1355%.

#### Seed 0

- Actual source-training optimizer updates: 10,033.
- Completed source-training epochs: 127.
- Trainable parameters: 5,900.
- Source training time: 12.2007 s.
- Test mean position MAE: 0.0010384 m.
- Test mean orientation MAE: 0.0008018 deg.
- Benchmark mean position MAE: 0.00185227 m.
- Benchmark mean orientation MAE: 0.00127773 deg.

Detailed seed report: [Experiment A - Trajectory Quantity Data.md](<../Experiment A - Trajectory Quantity/broad_20/seed_0/Experiment A - Trajectory Quantity Data.md>).

#### Seed 1

- Actual source-training optimizer updates: 10,033.
- Completed source-training epochs: 127.
- Trainable parameters: 5,900.
- Source training time: 12.0278 s.
- Test mean position MAE: 0.00104445 m.
- Test mean orientation MAE: 0.000844325 deg.
- Benchmark mean position MAE: 0.00158115 m.
- Benchmark mean orientation MAE: 0.00153547 deg.

Detailed seed report: [Experiment A - Trajectory Quantity Data.md](<../Experiment A - Trajectory Quantity/broad_20/seed_1/Experiment A - Trajectory Quantity Data.md>).

#### Seed 2

- Actual source-training optimizer updates: 10,033.
- Completed source-training epochs: 127.
- Trainable parameters: 5,900.
- Source training time: 9.3572 s.
- Test mean position MAE: 0.00106335 m.
- Test mean orientation MAE: 0.00082112 deg.
- Benchmark mean position MAE: 0.00173051 m.
- Benchmark mean orientation MAE: 0.00145591 deg.

Detailed seed report: [Experiment A - Trajectory Quantity Data.md](<../Experiment A - Trajectory Quantity/broad_20/seed_2/Experiment A - Trajectory Quantity Data.md>).


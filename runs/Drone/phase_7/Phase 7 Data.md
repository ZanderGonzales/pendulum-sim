# Phase 7 Data: Controlled Learning Experiments

## How to read these results

Experiments are separated by the factor being controlled; each condition has its own run heading and individual seed subheadings. Each metric bullet contains one numerical result. The main report emphasizes recursive rollout; seed reports and CSV/JSON files also retain one-step results.

Position MAE is mean Euclidean distance to the saved MuJoCo position. Orientation MAE is the mean shortest rotation angle. The initial state is excluded. MuJoCo compared with itself has zero error, so a percentage reduction relative to MuJoCo error would divide by zero. Instead, the simulator-relative percentages divide each flight’s position MAE by its total MuJoCo distance traveled, or its orientation MAE by its total MuJoCo angular travel, then average flights equally. They are normalized errors, not claims of percentage accuracy. Stationary denominators produce N/A.

Percentage error reduction = 100 × (reference error − candidate error) / reference error. Every condition is compared with every other condition within its experiment. All matched-seed and seed-mean comparisons, for each predictor, evaluation mode, and held-out split, are retained in `pairwise_comparisons.csv`.

## Shared settings and complete epochs

Requested optimizer updates are minimum budgets, rounded upward to the next complete epoch. The final short batch is included in every epoch. Actual budgets differ slightly across dataset sizes and are disclosed; this is the small rounding difference in the trajectory-quantity comparison. Validation still runs at the configured update interval and at the final update. The lowest validation residual MSE selects the best checkpoint, which may precede the end of training or lie between epoch boundaries. Test and benchmark errors never select weights, subsets, or checkpoints.

- Standard requested optimizer updates: 10,000.
- Standard hidden layers: 2.
- Standard neurons per hidden layer: 64.
- Batch size: 256.
- Learning rate: 0.001.
- Prediction interval: 0.01 s.
- Flight duration: 10 s.
- Training seeds per unique condition: 3.

Adam, Tanh activation, training-only input/target standardization, fixed drone properties, still air, and recorded applied controls are shared. Validation/test trajectories and the separate waypoint-family benchmark remain fixed. Identical training conditions reuse the same saved seed checkpoint across experiments; no older partial-epoch phase-5 training run substitutes for the new complete-epoch baseline.

## Navigate the experiments

- [Trajectory Quantity](#experiment-trajectory-quantity).
- [Trajectory Variety](#experiment-trajectory-variety).
- [Optimizer Updates](#experiment-optimizer-updates).
- [Neural Network Size](#experiment-neural-network-size).
- [Refresh Frequency](#experiment-refresh-frequency).

## Main comparisons at a glance

These are predefined comparisons of seed-mean recursive position error. The detailed experiment sections below include every condition, orientation errors, individual seeds, and all pairwise percentages.

- More training trajectories, test position error reduction: 85.2422%.
- More training trajectories, benchmark position error reduction: 66.9364%.
-------------
- Broad versus restricted families, test position error reduction: 79.7239%.
- Broad versus restricted families, benchmark position error reduction: 82.3319%.
-------------
- Larger versus smaller update budget, test position error reduction: 50.3235%.
- Larger versus smaller update budget, benchmark position error reduction: 40.0792%.
-------------
- Wider network versus standard width, test position error reduction: 14.9408%.
- Wider network versus standard width, benchmark position error reduction: 20.5194%.
-------------
- Deeper network versus standard depth, test position error reduction: -10.7663%.
- Deeper network versus standard depth, benchmark position error reduction: -30.4625%.
-------------
- Periodic refresh versus no refresh, test position error reduction: 99.3385%.
- Periodic refresh versus no refresh, benchmark position error reduction: 97.6552%.

## Experiment: Trajectory Quantity

Nested, balanced source-order subsets vary training trajectory count. Network size and requested updates stay fixed.

All displayed run summaries use fully recursive forecasts. Positive comparison percentages mean less error; negative percentages mean more error. The comparison denominator is the named reference run. Seed means weight each training seed equally; each seed first weights each test flight equally.

[All pairwise percentages](<Experiment A - Trajectory Quantity/pairwise_comparisons.csv>).

[Comparison plot](<Experiment A - Trajectory Quantity/plots/comparison_mae.png>).

### Run: 10 broad trajectories

Artifacts: [10 broad trajectories](<Experiment A - Trajectory Quantity/broad_10/seed_0/>).

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

- Mean position MAE against MuJoCo: **2.84564 mm**.
- Mean orientation MAE against MuJoCo: **0.00220939 deg**.
- Orientation MAE in radians: 3.85611e-05 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.745011%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.0305049%.
- Position error reduction versus physics-only: 80.1366%.
- Orientation error reduction versus physics-only: 77.4646%.
- Physics-only mean position MAE: **14.326 mm**.
- Physics-only mean orientation MAE: **0.00980406 deg**.
- Seed standard deviation of mean position MAE: 0.210423 mm.
- Seed standard deviation of mean orientation MAE: 0.000116103 deg.

#### Test: comparisons with other runs

- Position error reduction versus 20 broad trajectories: -171.341%.
- Orientation error reduction versus 20 broad trajectories: -168.646%.
- Position error reduction versus 40 broad trajectories: -323.776%.
- Orientation error reduction versus 40 broad trajectories: -318.844%.
- Position error reduction versus 80 broad trajectories: -577.605%.
- Orientation error reduction versus 80 broad trajectories: -537.653%.

#### Benchmark: mean across training seeds

- Mean position MAE against MuJoCo: **3.87838 mm**.
- Mean orientation MAE against MuJoCo: **0.00263208 deg**.
- Orientation MAE in radians: 4.59384e-05 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.515216%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.016303%.
- Position error reduction versus physics-only: 68.091%.
- Orientation error reduction versus physics-only: 64.0598%.
- Physics-only mean position MAE: **12.1545 mm**.
- Physics-only mean orientation MAE: **0.00732349 deg**.
- Seed standard deviation of mean position MAE: 0.373893 mm.
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
- Test mean position MAE: 2.699 mm.
- Test mean orientation MAE: 0.00207868 deg.
- Benchmark mean position MAE: 3.54391 mm.
- Benchmark mean orientation MAE: 0.0021347 deg.

Detailed seed report: [Experiment A - Trajectory Quantity Data.md](<Experiment A - Trajectory Quantity/broad_10/seed_0/Experiment A - Trajectory Quantity Data.md>).

#### Seed 1

- Actual source-training optimizer updates: 10,000.
- Completed source-training epochs: 250.
- Trainable parameters: 5,900.
- Source training time: 13.4060 s.
- Test mean position MAE: 2.69471 mm.
- Test mean orientation MAE: 0.00218868 deg.
- Benchmark mean position MAE: 3.69093 mm.
- Benchmark mean orientation MAE: 0.00256167 deg.

Detailed seed report: [Experiment A - Trajectory Quantity Data.md](<Experiment A - Trajectory Quantity/broad_10/seed_1/Experiment A - Trajectory Quantity Data.md>).

#### Seed 2

- Actual source-training optimizer updates: 10,000.
- Completed source-training epochs: 250.
- Trainable parameters: 5,900.
- Source training time: 9.1248 s.
- Test mean position MAE: 3.14322 mm.
- Test mean orientation MAE: 0.0023608 deg.
- Benchmark mean position MAE: 4.40028 mm.
- Benchmark mean orientation MAE: 0.00319987 deg.

Detailed seed report: [Experiment A - Trajectory Quantity Data.md](<Experiment A - Trajectory Quantity/broad_10/seed_2/Experiment A - Trajectory Quantity Data.md>).

### Run: 20 broad trajectories

Artifacts: [20 broad trajectories](<Experiment A - Trajectory Quantity/broad_20/seed_0/>).

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

- Mean position MAE against MuJoCo: **1.04873 mm**.
- Mean orientation MAE against MuJoCo: **0.000822415 deg**.
- Orientation MAE in radians: 1.43539e-05 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.37421%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.0141899%.
- Position error reduction versus physics-only: 92.6795%.
- Orientation error reduction versus physics-only: 91.6115%.
- Physics-only mean position MAE: **14.326 mm**.
- Physics-only mean orientation MAE: **0.00980406 deg**.
- Seed standard deviation of mean position MAE: 0.0106258 mm.
- Seed standard deviation of mean orientation MAE: 1.73849e-05 deg.

#### Test: comparisons with other runs

- Position error reduction versus 10 broad trajectories: 63.146%.
- Orientation error reduction versus 10 broad trajectories: 62.7763%.
- Position error reduction versus 40 broad trajectories: -56.1784%.
- Orientation error reduction versus 40 broad trajectories: -55.9092%.
- Position error reduction versus 80 broad trajectories: -149.725%.
- Orientation error reduction versus 80 broad trajectories: -137.358%.

#### Benchmark: mean across training seeds

- Mean position MAE against MuJoCo: **1.72131 mm**.
- Mean orientation MAE against MuJoCo: **0.00142304 deg**.
- Orientation MAE in radians: 2.48367e-05 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.217925%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00919873%.
- Position error reduction versus physics-only: 85.8381%.
- Orientation error reduction versus physics-only: 80.5689%.
- Physics-only mean position MAE: **12.1545 mm**.
- Physics-only mean orientation MAE: **0.00732349 deg**.
- Seed standard deviation of mean position MAE: 0.110878 mm.
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
- Test mean position MAE: 1.0384 mm.
- Test mean orientation MAE: 0.0008018 deg.
- Benchmark mean position MAE: 1.85227 mm.
- Benchmark mean orientation MAE: 0.00127773 deg.

Detailed seed report: [Experiment A - Trajectory Quantity Data.md](<Experiment A - Trajectory Quantity/broad_20/seed_0/Experiment A - Trajectory Quantity Data.md>).

#### Seed 1

- Actual source-training optimizer updates: 10,033.
- Completed source-training epochs: 127.
- Trainable parameters: 5,900.
- Source training time: 12.0278 s.
- Test mean position MAE: 1.04445 mm.
- Test mean orientation MAE: 0.000844325 deg.
- Benchmark mean position MAE: 1.58115 mm.
- Benchmark mean orientation MAE: 0.00153547 deg.

Detailed seed report: [Experiment A - Trajectory Quantity Data.md](<Experiment A - Trajectory Quantity/broad_20/seed_1/Experiment A - Trajectory Quantity Data.md>).

#### Seed 2

- Actual source-training optimizer updates: 10,033.
- Completed source-training epochs: 127.
- Trainable parameters: 5,900.
- Source training time: 9.3572 s.
- Test mean position MAE: 1.06335 mm.
- Test mean orientation MAE: 0.00082112 deg.
- Benchmark mean position MAE: 1.73051 mm.
- Benchmark mean orientation MAE: 0.00145591 deg.

Detailed seed report: [Experiment A - Trajectory Quantity Data.md](<Experiment A - Trajectory Quantity/broad_20/seed_2/Experiment A - Trajectory Quantity Data.md>).

### Run: 40 broad trajectories

Artifacts: [40 broad trajectories](<Experiment A - Trajectory Quantity/broad_40/seed_0/>).

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

- Mean position MAE against MuJoCo: **0.671497 mm**.
- Mean orientation MAE against MuJoCo: **0.000527496 deg**.
- Orientation MAE in radians: 9.20655e-06 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.283274%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00793248%.
- Position error reduction versus physics-only: 95.3128%.
- Orientation error reduction versus physics-only: 94.6196%.
- Physics-only mean position MAE: **14.326 mm**.
- Physics-only mean orientation MAE: **0.00980406 deg**.
- Seed standard deviation of mean position MAE: 0.0765059 mm.
- Seed standard deviation of mean orientation MAE: 1.2898e-05 deg.

#### Test: comparisons with other runs

- Position error reduction versus 10 broad trajectories: 76.4026%.
- Orientation error reduction versus 10 broad trajectories: 76.1248%.
- Position error reduction versus 20 broad trajectories: 35.9707%.
- Orientation error reduction versus 20 broad trajectories: 35.8601%.
- Position error reduction versus 80 broad trajectories: -59.8971%.
- Orientation error reduction versus 80 broad trajectories: -52.241%.

#### Benchmark: mean across training seeds

- Mean position MAE against MuJoCo: **1.54204 mm**.
- Mean orientation MAE against MuJoCo: **0.00124084 deg**.
- Orientation MAE in radians: 2.16567e-05 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.195035%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.0077864%.
- Position error reduction versus physics-only: 87.313%.
- Orientation error reduction versus physics-only: 83.0568%.
- Physics-only mean position MAE: **12.1545 mm**.
- Physics-only mean orientation MAE: **0.00732349 deg**.
- Seed standard deviation of mean position MAE: 0.165721 mm.
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
- Test mean position MAE: 0.582463 mm.
- Test mean orientation MAE: 0.000515371 deg.
- Benchmark mean position MAE: 1.46765 mm.
- Benchmark mean orientation MAE: 0.00104232 deg.

Detailed seed report: [Experiment A - Trajectory Quantity Data.md](<Experiment A - Trajectory Quantity/broad_40/seed_0/Experiment A - Trajectory Quantity Data.md>).

#### Seed 1

- Actual source-training optimizer updates: 10,048.
- Completed source-training epochs: 64.
- Trainable parameters: 5,900.
- Source training time: 11.3581 s.
- Test mean position MAE: 0.662775 mm.
- Test mean orientation MAE: 0.000521758 deg.
- Benchmark mean position MAE: 1.38677 mm.
- Benchmark mean orientation MAE: 0.0013599 deg.

Detailed seed report: [Experiment A - Trajectory Quantity Data.md](<Experiment A - Trajectory Quantity/broad_40/seed_1/Experiment A - Trajectory Quantity Data.md>).

#### Seed 2

- Actual source-training optimizer updates: 10,048.
- Completed source-training epochs: 64.
- Trainable parameters: 5,900.
- Source training time: 11.1440 s.
- Test mean position MAE: 0.769253 mm.
- Test mean orientation MAE: 0.00054536 deg.
- Benchmark mean position MAE: 1.77171 mm.
- Benchmark mean orientation MAE: 0.00132028 deg.

Detailed seed report: [Experiment A - Trajectory Quantity Data.md](<Experiment A - Trajectory Quantity/broad_40/seed_2/Experiment A - Trajectory Quantity Data.md>).

### Run: 80 broad trajectories

Artifacts: [80 broad trajectories](<Experiment A - Trajectory Quantity/broad_80/seed_0/>).

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

- Mean position MAE against MuJoCo: **0.419956 mm**.
- Mean orientation MAE against MuJoCo: **0.000346488 deg**.
- Orientation MAE in radians: 6.04735e-06 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.177761%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00645881%.
- Position error reduction versus physics-only: 97.0686%.
- Orientation error reduction versus physics-only: 96.4659%.
- Physics-only mean position MAE: **14.326 mm**.
- Physics-only mean orientation MAE: **0.00980406 deg**.
- Seed standard deviation of mean position MAE: 0.0210501 mm.
- Seed standard deviation of mean orientation MAE: 4.25686e-05 deg.

#### Test: comparisons with other runs

- Position error reduction versus 10 broad trajectories: 85.2422%.
- Orientation error reduction versus 10 broad trajectories: 84.3175%.
- Position error reduction versus 20 broad trajectories: 59.9559%.
- Orientation error reduction versus 20 broad trajectories: 57.8695%.
- Position error reduction versus 40 broad trajectories: 37.4598%.
- Orientation error reduction versus 40 broad trajectories: 34.3147%.

#### Benchmark: mean across training seeds

- Mean position MAE against MuJoCo: **1.28233 mm**.
- Mean orientation MAE against MuJoCo: **0.0009632 deg**.
- Orientation MAE in radians: 1.6811e-05 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.157651%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00620006%.
- Position error reduction versus physics-only: 89.4497%.
- Orientation error reduction versus physics-only: 86.8478%.
- Physics-only mean position MAE: **12.1545 mm**.
- Physics-only mean orientation MAE: **0.00732349 deg**.
- Seed standard deviation of mean position MAE: 0.282818 mm.
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
- Test mean position MAE: 0.401772 mm.
- Test mean orientation MAE: 0.000290801 deg.
- Benchmark mean position MAE: 1.19401 mm.
- Benchmark mean orientation MAE: 0.000683165 deg.

Detailed seed report: [Experiment A - Trajectory Quantity Data.md](<Experiment A - Trajectory Quantity/broad_80/seed_0/Experiment A - Trajectory Quantity Data.md>).

#### Seed 1

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 13.0851 s.
- Test mean position MAE: 0.44946 mm.
- Test mean orientation MAE: 0.00039414 deg.
- Benchmark mean position MAE: 0.988661 mm.
- Benchmark mean orientation MAE: 0.00090311 deg.

Detailed seed report: [Experiment A - Trajectory Quantity Data.md](<Experiment A - Trajectory Quantity/broad_80/seed_1/Experiment A - Trajectory Quantity Data.md>).

#### Seed 2

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 12.4214 s.
- Test mean position MAE: 0.408635 mm.
- Test mean orientation MAE: 0.000354522 deg.
- Benchmark mean position MAE: 1.66432 mm.
- Benchmark mean orientation MAE: 0.00130332 deg.

Detailed seed report: [Experiment A - Trajectory Quantity Data.md](<Experiment A - Trajectory Quantity/broad_80/seed_2/Experiment A - Trajectory Quantity Data.md>).

## Experiment: Trajectory Variety

Both conditions use the same training count and flight duration. Restricted data contain circles and figure-eights; broad data cover all main families. Validation and test flights are identical.

All displayed run summaries use fully recursive forecasts. Positive comparison percentages mean less error; negative percentages mean more error. The comparison denominator is the named reference run. Seed means weight each training seed equally; each seed first weights each test flight equally.

[All pairwise percentages](<Experiment B - Trajectory Variety/pairwise_comparisons.csv>).

[Comparison plot](<Experiment B - Trajectory Variety/plots/comparison_mae.png>).

### Run: 20 restricted trajectories

Artifacts: [20 restricted trajectories](<Experiment B - Trajectory Variety/restricted_20/seed_0/>).

#### Training composition

- Training trajectories: 20.
- Hidden layers: 2.
- Neurons per hidden layer: 64.
- figure_eight training trajectories: 10.
- circle training trajectories: 10.

#### Test: mean across training seeds

- Mean position MAE against MuJoCo: **5.17228 mm**.
- Mean orientation MAE against MuJoCo: **0.00450522 deg**.
- Orientation MAE in radians: 7.86309e-05 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 1.37106%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.174504%.
- Position error reduction versus physics-only: 63.896%.
- Orientation error reduction versus physics-only: 54.0474%.
- Physics-only mean position MAE: **14.326 mm**.
- Physics-only mean orientation MAE: **0.00980406 deg**.
- Seed standard deviation of mean position MAE: 1.217 mm.
- Seed standard deviation of mean orientation MAE: 0.000957972 deg.

#### Test: comparisons with other runs

- Position error reduction versus 20 broad trajectories: -393.193%.
- Orientation error reduction versus 20 broad trajectories: -447.804%.

#### Benchmark: mean across training seeds

- Mean position MAE against MuJoCo: **9.74245 mm**.
- Mean orientation MAE against MuJoCo: **0.00896993 deg**.
- Orientation MAE in radians: 0.000156555 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 1.42743%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.0638298%.
- Position error reduction versus physics-only: 19.8448%.
- Orientation error reduction versus physics-only: -22.4816%.
- Physics-only mean position MAE: **12.1545 mm**.
- Physics-only mean orientation MAE: **0.00732349 deg**.
- Seed standard deviation of mean position MAE: 2.67364 mm.
- Seed standard deviation of mean orientation MAE: 0.00135982 deg.

#### Benchmark: comparisons with other runs

- Position error reduction versus 20 broad trajectories: -465.99%.
- Orientation error reduction versus 20 broad trajectories: -530.337%.

#### Seed 0

- Actual source-training optimizer updates: 10,033.
- Completed source-training epochs: 127.
- Trainable parameters: 5,900.
- Source training time: 9.4645 s.
- Test mean position MAE: 3.51851 mm.
- Test mean orientation MAE: 0.00325217 deg.
- Benchmark mean position MAE: 6.64359 mm.
- Benchmark mean orientation MAE: 0.00773326 deg.

Detailed seed report: [Experiment B - Trajectory Variety Data.md](<Experiment B - Trajectory Variety/restricted_20/seed_0/Experiment B - Trajectory Variety Data.md>).

#### Seed 1

- Actual source-training optimizer updates: 10,033.
- Completed source-training epochs: 127.
- Trainable parameters: 5,900.
- Source training time: 9.5200 s.
- Test mean position MAE: 6.41199 mm.
- Test mean orientation MAE: 0.00557779 deg.
- Benchmark mean position MAE: 13.1681 mm.
- Benchmark mean orientation MAE: 0.0108637 deg.

Detailed seed report: [Experiment B - Trajectory Variety Data.md](<Experiment B - Trajectory Variety/restricted_20/seed_1/Experiment B - Trajectory Variety Data.md>).

#### Seed 2

- Actual source-training optimizer updates: 10,033.
- Completed source-training epochs: 127.
- Trainable parameters: 5,900.
- Source training time: 9.8430 s.
- Test mean position MAE: 5.58632 mm.
- Test mean orientation MAE: 0.00468571 deg.
- Benchmark mean position MAE: 9.41562 mm.
- Benchmark mean orientation MAE: 0.00831285 deg.

Detailed seed report: [Experiment B - Trajectory Variety Data.md](<Experiment B - Trajectory Variety/restricted_20/seed_2/Experiment B - Trajectory Variety Data.md>).

### Run: 20 broad trajectories

Artifacts: [20 broad trajectories](<Experiment A - Trajectory Quantity/broad_20/seed_0/>).

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

- Mean position MAE against MuJoCo: **1.04873 mm**.
- Mean orientation MAE against MuJoCo: **0.000822415 deg**.
- Orientation MAE in radians: 1.43539e-05 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.37421%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.0141899%.
- Position error reduction versus physics-only: 92.6795%.
- Orientation error reduction versus physics-only: 91.6115%.
- Physics-only mean position MAE: **14.326 mm**.
- Physics-only mean orientation MAE: **0.00980406 deg**.
- Seed standard deviation of mean position MAE: 0.0106258 mm.
- Seed standard deviation of mean orientation MAE: 1.73849e-05 deg.

#### Test: comparisons with other runs

- Position error reduction versus 20 restricted trajectories: 79.7239%.
- Orientation error reduction versus 20 restricted trajectories: 81.7453%.

#### Benchmark: mean across training seeds

- Mean position MAE against MuJoCo: **1.72131 mm**.
- Mean orientation MAE against MuJoCo: **0.00142304 deg**.
- Orientation MAE in radians: 2.48367e-05 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.217925%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00919873%.
- Position error reduction versus physics-only: 85.8381%.
- Orientation error reduction versus physics-only: 80.5689%.
- Physics-only mean position MAE: **12.1545 mm**.
- Physics-only mean orientation MAE: **0.00732349 deg**.
- Seed standard deviation of mean position MAE: 0.110878 mm.
- Seed standard deviation of mean orientation MAE: 0.000107762 deg.

#### Benchmark: comparisons with other runs

- Position error reduction versus 20 restricted trajectories: 82.3319%.
- Orientation error reduction versus 20 restricted trajectories: 84.1355%.

#### Seed 0

- Actual source-training optimizer updates: 10,033.
- Completed source-training epochs: 127.
- Trainable parameters: 5,900.
- Source training time: 12.2007 s.
- Test mean position MAE: 1.0384 mm.
- Test mean orientation MAE: 0.0008018 deg.
- Benchmark mean position MAE: 1.85227 mm.
- Benchmark mean orientation MAE: 0.00127773 deg.

Detailed seed report: [Experiment A - Trajectory Quantity Data.md](<Experiment A - Trajectory Quantity/broad_20/seed_0/Experiment A - Trajectory Quantity Data.md>).

#### Seed 1

- Actual source-training optimizer updates: 10,033.
- Completed source-training epochs: 127.
- Trainable parameters: 5,900.
- Source training time: 12.0278 s.
- Test mean position MAE: 1.04445 mm.
- Test mean orientation MAE: 0.000844325 deg.
- Benchmark mean position MAE: 1.58115 mm.
- Benchmark mean orientation MAE: 0.00153547 deg.

Detailed seed report: [Experiment A - Trajectory Quantity Data.md](<Experiment A - Trajectory Quantity/broad_20/seed_1/Experiment A - Trajectory Quantity Data.md>).

#### Seed 2

- Actual source-training optimizer updates: 10,033.
- Completed source-training epochs: 127.
- Trainable parameters: 5,900.
- Source training time: 9.3572 s.
- Test mean position MAE: 1.06335 mm.
- Test mean orientation MAE: 0.00082112 deg.
- Benchmark mean position MAE: 1.73051 mm.
- Benchmark mean orientation MAE: 0.00145591 deg.

Detailed seed report: [Experiment A - Trajectory Quantity Data.md](<Experiment A - Trajectory Quantity/broad_20/seed_2/Experiment A - Trajectory Quantity Data.md>).

## Experiment: Optimizer Updates

Only the requested optimizer-update budget changes. Dataset, architecture, optimizer, and evaluation flights stay fixed.

All displayed run summaries use fully recursive forecasts. Positive comparison percentages mean less error; negative percentages mean more error. The comparison denominator is the named reference run. Seed means weight each training seed equally; each seed first weights each test flight equally.

[All pairwise percentages](<Experiment C - Optimizer Updates/pairwise_comparisons.csv>).

[Comparison plot](<Experiment C - Optimizer Updates/plots/comparison_mae.png>).

### Run: 5,000 requested optimizer updates

Artifacts: [5,000 requested optimizer updates](<Experiment C - Optimizer Updates/updates_5000/seed_0/>).

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

- Mean position MAE against MuJoCo: **0.582882 mm**.
- Mean orientation MAE against MuJoCo: **0.000478322 deg**.
- Orientation MAE in radians: 8.3483e-06 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.24569%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00934327%.
- Position error reduction versus physics-only: 95.9313%.
- Orientation error reduction versus physics-only: 95.1212%.
- Physics-only mean position MAE: **14.326 mm**.
- Physics-only mean orientation MAE: **0.00980406 deg**.
- Seed standard deviation of mean position MAE: 0.0277215 mm.
- Seed standard deviation of mean orientation MAE: 3.88874e-05 deg.

#### Test: comparisons with other runs

- Position error reduction versus 10,000 requested optimizer updates: -38.796%.
- Orientation error reduction versus 10,000 requested optimizer updates: -38.0488%.
- Position error reduction versus 15,000 requested optimizer updates: -66.3056%.
- Orientation error reduction versus 15,000 requested optimizer updates: -55.2117%.
- Position error reduction versus 20,000 requested optimizer updates: -101.303%.
- Orientation error reduction versus 20,000 requested optimizer updates: -110.482%.

#### Benchmark: mean across training seeds

- Mean position MAE against MuJoCo: **1.77977 mm**.
- Mean orientation MAE against MuJoCo: **0.00107803 deg**.
- Orientation MAE in radians: 1.88151e-05 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.223466%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00689127%.
- Position error reduction versus physics-only: 85.3571%.
- Orientation error reduction versus physics-only: 85.2799%.
- Physics-only mean position MAE: **12.1545 mm**.
- Physics-only mean orientation MAE: **0.00732349 deg**.
- Seed standard deviation of mean position MAE: 0.123136 mm.
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
- Test mean position MAE: 0.582118 mm.
- Test mean orientation MAE: 0.000485355 deg.
- Benchmark mean position MAE: 1.75447 mm.
- Benchmark mean orientation MAE: 0.00074604 deg.

Detailed seed report: [Experiment C - Optimizer Updates Data.md](<Experiment C - Optimizer Updates/updates_5000/seed_0/Experiment C - Optimizer Updates Data.md>).

#### Seed 1

- Actual source-training optimizer updates: 5,008.
- Completed source-training epochs: 16.
- Trainable parameters: 5,900.
- Source training time: 7.4764 s.
- Test mean position MAE: 0.617209 mm.
- Test mean orientation MAE: 0.000522042 deg.
- Benchmark mean position MAE: 1.64322 mm.
- Benchmark mean orientation MAE: 0.00111905 deg.

Detailed seed report: [Experiment C - Optimizer Updates Data.md](<Experiment C - Optimizer Updates/updates_5000/seed_1/Experiment C - Optimizer Updates Data.md>).

#### Seed 2

- Actual source-training optimizer updates: 5,008.
- Completed source-training epochs: 16.
- Trainable parameters: 5,900.
- Source training time: 6.3296 s.
- Test mean position MAE: 0.549319 mm.
- Test mean orientation MAE: 0.00042757 deg.
- Benchmark mean position MAE: 1.94164 mm.
- Benchmark mean orientation MAE: 0.00136899 deg.

Detailed seed report: [Experiment C - Optimizer Updates Data.md](<Experiment C - Optimizer Updates/updates_5000/seed_2/Experiment C - Optimizer Updates Data.md>).

### Run: 10,000 requested optimizer updates

Artifacts: [10,000 requested optimizer updates](<Experiment A - Trajectory Quantity/broad_80/seed_0/>).

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

- Mean position MAE against MuJoCo: **0.419956 mm**.
- Mean orientation MAE against MuJoCo: **0.000346488 deg**.
- Orientation MAE in radians: 6.04735e-06 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.177761%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00645881%.
- Position error reduction versus physics-only: 97.0686%.
- Orientation error reduction versus physics-only: 96.4659%.
- Physics-only mean position MAE: **14.326 mm**.
- Physics-only mean orientation MAE: **0.00980406 deg**.
- Seed standard deviation of mean position MAE: 0.0210501 mm.
- Seed standard deviation of mean orientation MAE: 4.25686e-05 deg.

#### Test: comparisons with other runs

- Position error reduction versus 5,000 requested optimizer updates: 27.9518%.
- Orientation error reduction versus 5,000 requested optimizer updates: 27.5619%.
- Position error reduction versus 15,000 requested optimizer updates: -19.8201%.
- Orientation error reduction versus 15,000 requested optimizer updates: -12.4325%.
- Position error reduction versus 20,000 requested optimizer updates: -45.0348%.
- Orientation error reduction versus 20,000 requested optimizer updates: -52.4696%.

#### Benchmark: mean across training seeds

- Mean position MAE against MuJoCo: **1.28233 mm**.
- Mean orientation MAE against MuJoCo: **0.0009632 deg**.
- Orientation MAE in radians: 1.6811e-05 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.157651%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00620006%.
- Position error reduction versus physics-only: 89.4497%.
- Orientation error reduction versus physics-only: 86.8478%.
- Physics-only mean position MAE: **12.1545 mm**.
- Physics-only mean orientation MAE: **0.00732349 deg**.
- Seed standard deviation of mean position MAE: 0.282818 mm.
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
- Test mean position MAE: 0.401772 mm.
- Test mean orientation MAE: 0.000290801 deg.
- Benchmark mean position MAE: 1.19401 mm.
- Benchmark mean orientation MAE: 0.000683165 deg.

Detailed seed report: [Experiment A - Trajectory Quantity Data.md](<Experiment A - Trajectory Quantity/broad_80/seed_0/Experiment A - Trajectory Quantity Data.md>).

#### Seed 1

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 13.0851 s.
- Test mean position MAE: 0.44946 mm.
- Test mean orientation MAE: 0.00039414 deg.
- Benchmark mean position MAE: 0.988661 mm.
- Benchmark mean orientation MAE: 0.00090311 deg.

Detailed seed report: [Experiment A - Trajectory Quantity Data.md](<Experiment A - Trajectory Quantity/broad_80/seed_1/Experiment A - Trajectory Quantity Data.md>).

#### Seed 2

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 12.4214 s.
- Test mean position MAE: 0.408635 mm.
- Test mean orientation MAE: 0.000354522 deg.
- Benchmark mean position MAE: 1.66432 mm.
- Benchmark mean orientation MAE: 0.00130332 deg.

Detailed seed report: [Experiment A - Trajectory Quantity Data.md](<Experiment A - Trajectory Quantity/broad_80/seed_2/Experiment A - Trajectory Quantity Data.md>).

### Run: 15,000 requested optimizer updates

Artifacts: [15,000 requested optimizer updates](<Experiment C - Optimizer Updates/updates_15000/seed_0/>).

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

- Mean position MAE against MuJoCo: **0.350489 mm**.
- Mean orientation MAE against MuJoCo: **0.000308174 deg**.
- Orientation MAE in radians: 5.37865e-06 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.1282%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.005125%.
- Position error reduction versus physics-only: 97.5535%.
- Orientation error reduction versus physics-only: 96.8567%.
- Physics-only mean position MAE: **14.326 mm**.
- Physics-only mean orientation MAE: **0.00980406 deg**.
- Seed standard deviation of mean position MAE: 0.023117 mm.
- Seed standard deviation of mean orientation MAE: 3.7203e-05 deg.

#### Test: comparisons with other runs

- Position error reduction versus 5,000 requested optimizer updates: 39.8697%.
- Orientation error reduction versus 5,000 requested optimizer updates: 35.5719%.
- Position error reduction versus 10,000 requested optimizer updates: 16.5416%.
- Orientation error reduction versus 10,000 requested optimizer updates: 11.0577%.
- Position error reduction versus 20,000 requested optimizer updates: -21.0438%.
- Orientation error reduction versus 20,000 requested optimizer updates: -35.6099%.

#### Benchmark: mean across training seeds

- Mean position MAE against MuJoCo: **1.13307 mm**.
- Mean orientation MAE against MuJoCo: **0.000879509 deg**.
- Orientation MAE in radians: 1.53503e-05 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.139084%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00566101%.
- Position error reduction versus physics-only: 90.6777%.
- Orientation error reduction versus physics-only: 87.9906%.
- Physics-only mean position MAE: **12.1545 mm**.
- Physics-only mean orientation MAE: **0.00732349 deg**.
- Seed standard deviation of mean position MAE: 0.225233 mm.
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
- Test mean position MAE: 0.320074 mm.
- Test mean orientation MAE: 0.000256141 deg.
- Benchmark mean position MAE: 1.06874 mm.
- Benchmark mean orientation MAE: 0.000658234 deg.

Detailed seed report: [Experiment C - Optimizer Updates Data.md](<Experiment C - Optimizer Updates/updates_15000/seed_0/Experiment C - Optimizer Updates Data.md>).

#### Seed 1

- Actual source-training optimizer updates: 15,024.
- Completed source-training epochs: 48.
- Trainable parameters: 5,900.
- Source training time: 25.9722 s.
- Test mean position MAE: 0.355313 mm.
- Test mean orientation MAE: 0.000340938 deg.
- Benchmark mean position MAE: 0.895068 mm.
- Benchmark mean orientation MAE: 0.000838223 deg.

Detailed seed report: [Experiment C - Optimizer Updates Data.md](<Experiment C - Optimizer Updates/updates_15000/seed_1/Experiment C - Optimizer Updates Data.md>).

#### Seed 2

- Actual source-training optimizer updates: 15,024.
- Completed source-training epochs: 48.
- Trainable parameters: 5,900.
- Source training time: 21.9645 s.
- Test mean position MAE: 0.376079 mm.
- Test mean orientation MAE: 0.000327443 deg.
- Benchmark mean position MAE: 1.43541 mm.
- Benchmark mean orientation MAE: 0.00114207 deg.

Detailed seed report: [Experiment C - Optimizer Updates Data.md](<Experiment C - Optimizer Updates/updates_15000/seed_2/Experiment C - Optimizer Updates Data.md>).

### Run: 20,000 requested optimizer updates

Artifacts: [20,000 requested optimizer updates](<Experiment C - Optimizer Updates/updates_20000/seed_0/>).

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

- Mean position MAE against MuJoCo: **0.289555 mm**.
- Mean orientation MAE against MuJoCo: **0.00022725 deg**.
- Orientation MAE in radians: 3.96627e-06 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.0975726%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00370492%.
- Position error reduction versus physics-only: 97.9788%.
- Orientation error reduction versus physics-only: 97.6821%.
- Physics-only mean position MAE: **14.326 mm**.
- Physics-only mean orientation MAE: **0.00980406 deg**.
- Seed standard deviation of mean position MAE: 0.0109759 mm.
- Seed standard deviation of mean orientation MAE: 1.83626e-05 deg.

#### Test: comparisons with other runs

- Position error reduction versus 5,000 requested optimizer updates: 50.3235%.
- Orientation error reduction versus 5,000 requested optimizer updates: 52.4901%.
- Position error reduction versus 10,000 requested optimizer updates: 31.051%.
- Orientation error reduction versus 10,000 requested optimizer updates: 34.4131%.
- Position error reduction versus 15,000 requested optimizer updates: 17.3853%.
- Orientation error reduction versus 15,000 requested optimizer updates: 26.2591%.

#### Benchmark: mean across training seeds

- Mean position MAE against MuJoCo: **1.06645 mm**.
- Mean orientation MAE against MuJoCo: **0.000812596 deg**.
- Orientation MAE in radians: 1.41825e-05 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.130861%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00525133%.
- Position error reduction versus physics-only: 91.2258%.
- Orientation error reduction versus physics-only: 88.9042%.
- Physics-only mean position MAE: **12.1545 mm**.
- Physics-only mean orientation MAE: **0.00732349 deg**.
- Seed standard deviation of mean position MAE: 0.153741 mm.
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
- Test mean position MAE: 0.284956 mm.
- Test mean orientation MAE: 0.000247183 deg.
- Benchmark mean position MAE: 1.023 mm.
- Benchmark mean orientation MAE: 0.000605751 deg.

Detailed seed report: [Experiment C - Optimizer Updates Data.md](<Experiment C - Optimizer Updates/updates_20000/seed_0/Experiment C - Optimizer Updates Data.md>).

#### Seed 1

- Actual source-training optimizer updates: 20,032.
- Completed source-training epochs: 64.
- Trainable parameters: 5,900.
- Source training time: 23.9397 s.
- Test mean position MAE: 0.279016 mm.
- Test mean orientation MAE: 0.000231699 deg.
- Benchmark mean position MAE: 0.903684 mm.
- Benchmark mean orientation MAE: 0.000817998 deg.

Detailed seed report: [Experiment C - Optimizer Updates Data.md](<Experiment C - Optimizer Updates/updates_20000/seed_1/Experiment C - Optimizer Updates Data.md>).

#### Seed 2

- Actual source-training optimizer updates: 20,032.
- Completed source-training epochs: 64.
- Trainable parameters: 5,900.
- Source training time: 25.0690 s.
- Test mean position MAE: 0.304694 mm.
- Test mean orientation MAE: 0.000202869 deg.
- Benchmark mean position MAE: 1.27267 mm.
- Benchmark mean orientation MAE: 0.00101404 deg.

Detailed seed report: [Experiment C - Optimizer Updates Data.md](<Experiment C - Optimizer Updates/updates_20000/seed_2/Experiment C - Optimizer Updates Data.md>).

## Experiment: Neural Network Size

Width comparisons hold hidden depth fixed. Depth comparisons hold hidden width fixed. The shared standard network supplies the reference.

All displayed run summaries use fully recursive forecasts. Positive comparison percentages mean less error; negative percentages mean more error. The comparison denominator is the named reference run. Seed means weight each training seed equally; each seed first weights each test flight equally.

[All pairwise percentages](<Experiment D - Neural Network Size/pairwise_comparisons.csv>).

[Comparison plot](<Experiment D - Neural Network Size/plots/comparison_mae.png>).

### Run: 2 hidden layers x 32 neurons

Artifacts: [2 hidden layers x 32 neurons](<Experiment D - Neural Network Size/layers_2_width_32/seed_0/>).

#### Training composition

- Training trajectories: 80.
- Hidden layers: 2.
- Neurons per hidden layer: 32.
- hover training trajectories: 16.
- climb_descent training trajectories: 16.
- figure_eight training trajectories: 16.
- circle training trajectories: 16.
- straight training trajectories: 16.

#### Test: mean across training seeds

- Mean position MAE against MuJoCo: **0.722308 mm**.
- Mean orientation MAE against MuJoCo: **0.000526848 deg**.
- Orientation MAE in radians: 9.19523e-06 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.274422%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00871825%.
- Position error reduction versus physics-only: 94.9581%.
- Orientation error reduction versus physics-only: 94.6262%.
- Physics-only mean position MAE: **14.326 mm**.
- Physics-only mean orientation MAE: **0.00980406 deg**.
- Seed standard deviation of mean position MAE: 0.0781265 mm.
- Seed standard deviation of mean orientation MAE: 7.03677e-06 deg.

#### Test: comparisons with other runs

- Position error reduction versus 2 hidden layers x 64 neurons: -71.9961%.
- Orientation error reduction versus 2 hidden layers x 64 neurons: -52.0539%.
- Position error reduction versus 2 hidden layers x 128 neurons: -102.207%.
- Orientation error reduction versus 2 hidden layers x 128 neurons: -63.956%.
- Position error reduction versus 1 hidden layers x 64 neurons: -2.21705%.
- Orientation error reduction versus 1 hidden layers x 64 neurons: 8.10859%.
- Position error reduction versus 4 hidden layers x 64 neurons: -55.2784%.
- Orientation error reduction versus 4 hidden layers x 64 neurons: -36.5564%.

#### Benchmark: mean across training seeds

- Mean position MAE against MuJoCo: **2.10814 mm**.
- Mean orientation MAE against MuJoCo: **0.00151822 deg**.
- Orientation MAE in radians: 2.6498e-05 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.27459%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00994615%.
- Position error reduction versus physics-only: 82.6554%.
- Orientation error reduction versus physics-only: 79.2692%.
- Physics-only mean position MAE: **12.1545 mm**.
- Physics-only mean orientation MAE: **0.00732349 deg**.
- Seed standard deviation of mean position MAE: 0.432319 mm.
- Seed standard deviation of mean orientation MAE: 0.00012466 deg.

#### Benchmark: comparisons with other runs

- Position error reduction versus 2 hidden layers x 64 neurons: -64.3995%.
- Orientation error reduction versus 2 hidden layers x 64 neurons: -57.6227%.
- Position error reduction versus 2 hidden layers x 128 neurons: -106.842%.
- Orientation error reduction versus 2 hidden layers x 128 neurons: -73.1421%.
- Position error reduction versus 1 hidden layers x 64 neurons: 4.88345%.
- Orientation error reduction versus 1 hidden layers x 64 neurons: -1.86275%.
- Position error reduction versus 4 hidden layers x 64 neurons: -26.0128%.
- Orientation error reduction versus 4 hidden layers x 64 neurons: -26.8472%.

#### Seed 0

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 1,932.
- Source training time: 10.8048 s.
- Test mean position MAE: 0.634241 mm.
- Test mean orientation MAE: 0.000517315 deg.
- Benchmark mean position MAE: 2.53579 mm.
- Benchmark mean orientation MAE: 0.00157692 deg.

Detailed seed report: [Experiment D - Neural Network Size Data.md](<Experiment D - Neural Network Size/layers_2_width_32/seed_0/Experiment D - Neural Network Size Data.md>).

#### Seed 1

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 1,932.
- Source training time: 10.9767 s.
- Test mean position MAE: 0.824123 mm.
- Test mean orientation MAE: 0.000529141 deg.
- Benchmark mean position MAE: 2.27272 mm.
- Benchmark mean orientation MAE: 0.00134491 deg.

Detailed seed report: [Experiment D - Neural Network Size Data.md](<Experiment D - Neural Network Size/layers_2_width_32/seed_1/Experiment D - Neural Network Size Data.md>).

#### Seed 2

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 1,932.
- Source training time: 9.6931 s.
- Test mean position MAE: 0.708559 mm.
- Test mean orientation MAE: 0.000534088 deg.
- Benchmark mean position MAE: 1.51592 mm.
- Benchmark mean orientation MAE: 0.00163284 deg.

Detailed seed report: [Experiment D - Neural Network Size Data.md](<Experiment D - Neural Network Size/layers_2_width_32/seed_2/Experiment D - Neural Network Size Data.md>).

### Run: 2 hidden layers x 64 neurons

Artifacts: [2 hidden layers x 64 neurons](<Experiment A - Trajectory Quantity/broad_80/seed_0/>).

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

- Mean position MAE against MuJoCo: **0.419956 mm**.
- Mean orientation MAE against MuJoCo: **0.000346488 deg**.
- Orientation MAE in radians: 6.04735e-06 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.177761%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00645881%.
- Position error reduction versus physics-only: 97.0686%.
- Orientation error reduction versus physics-only: 96.4659%.
- Physics-only mean position MAE: **14.326 mm**.
- Physics-only mean orientation MAE: **0.00980406 deg**.
- Seed standard deviation of mean position MAE: 0.0210501 mm.
- Seed standard deviation of mean orientation MAE: 4.25686e-05 deg.

#### Test: comparisons with other runs

- Position error reduction versus 2 hidden layers x 32 neurons: 41.8592%.
- Orientation error reduction versus 2 hidden layers x 32 neurons: 34.2339%.
- Position error reduction versus 2 hidden layers x 128 neurons: -17.5651%.
- Orientation error reduction versus 2 hidden layers x 128 neurons: -7.82753%.
- Position error reduction versus 1 hidden layers x 64 neurons: 40.5701%.
- Orientation error reduction versus 1 hidden layers x 64 neurons: 39.5666%.
- Position error reduction versus 4 hidden layers x 64 neurons: 9.71983%.
- Orientation error reduction versus 4 hidden layers x 64 neurons: 10.1921%.

#### Benchmark: mean across training seeds

- Mean position MAE against MuJoCo: **1.28233 mm**.
- Mean orientation MAE against MuJoCo: **0.0009632 deg**.
- Orientation MAE in radians: 1.6811e-05 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.157651%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00620006%.
- Position error reduction versus physics-only: 89.4497%.
- Orientation error reduction versus physics-only: 86.8478%.
- Physics-only mean position MAE: **12.1545 mm**.
- Physics-only mean orientation MAE: **0.00732349 deg**.
- Seed standard deviation of mean position MAE: 0.282818 mm.
- Seed standard deviation of mean orientation MAE: 0.000256719 deg.

#### Benchmark: comparisons with other runs

- Position error reduction versus 2 hidden layers x 32 neurons: 39.1725%.
- Orientation error reduction versus 2 hidden layers x 32 neurons: 36.5574%.
- Position error reduction versus 2 hidden layers x 128 neurons: -25.8168%.
- Orientation error reduction versus 2 hidden layers x 128 neurons: -9.84593%.
- Position error reduction versus 1 hidden layers x 64 neurons: 42.143%.
- Orientation error reduction versus 1 hidden layers x 64 neurons: 35.3756%.
- Position error reduction versus 4 hidden layers x 64 neurons: 23.3496%.
- Orientation error reduction versus 4 hidden layers x 64 neurons: 19.5248%.

#### Seed 0

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 13.3145 s.
- Test mean position MAE: 0.401772 mm.
- Test mean orientation MAE: 0.000290801 deg.
- Benchmark mean position MAE: 1.19401 mm.
- Benchmark mean orientation MAE: 0.000683165 deg.

Detailed seed report: [Experiment A - Trajectory Quantity Data.md](<Experiment A - Trajectory Quantity/broad_80/seed_0/Experiment A - Trajectory Quantity Data.md>).

#### Seed 1

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 13.0851 s.
- Test mean position MAE: 0.44946 mm.
- Test mean orientation MAE: 0.00039414 deg.
- Benchmark mean position MAE: 0.988661 mm.
- Benchmark mean orientation MAE: 0.00090311 deg.

Detailed seed report: [Experiment A - Trajectory Quantity Data.md](<Experiment A - Trajectory Quantity/broad_80/seed_1/Experiment A - Trajectory Quantity Data.md>).

#### Seed 2

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 12.4214 s.
- Test mean position MAE: 0.408635 mm.
- Test mean orientation MAE: 0.000354522 deg.
- Benchmark mean position MAE: 1.66432 mm.
- Benchmark mean orientation MAE: 0.00130332 deg.

Detailed seed report: [Experiment A - Trajectory Quantity Data.md](<Experiment A - Trajectory Quantity/broad_80/seed_2/Experiment A - Trajectory Quantity Data.md>).

### Run: 2 hidden layers x 128 neurons

Artifacts: [2 hidden layers x 128 neurons](<Experiment D - Neural Network Size/layers_2_width_128/seed_0/>).

#### Training composition

- Training trajectories: 80.
- Hidden layers: 2.
- Neurons per hidden layer: 128.
- hover training trajectories: 16.
- climb_descent training trajectories: 16.
- figure_eight training trajectories: 16.
- circle training trajectories: 16.
- straight training trajectories: 16.

#### Test: mean across training seeds

- Mean position MAE against MuJoCo: **0.357211 mm**.
- Mean orientation MAE against MuJoCo: **0.000321335 deg**.
- Orientation MAE in radians: 5.60835e-06 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.16342%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00658619%.
- Position error reduction versus physics-only: 97.5066%.
- Orientation error reduction versus physics-only: 96.7224%.
- Physics-only mean position MAE: **14.326 mm**.
- Physics-only mean orientation MAE: **0.00980406 deg**.
- Seed standard deviation of mean position MAE: 0.0216703 mm.
- Seed standard deviation of mean orientation MAE: 6.59504e-06 deg.

#### Test: comparisons with other runs

- Position error reduction versus 2 hidden layers x 32 neurons: 50.5458%.
- Orientation error reduction versus 2 hidden layers x 32 neurons: 39.008%.
- Position error reduction versus 2 hidden layers x 64 neurons: 14.9408%.
- Orientation error reduction versus 2 hidden layers x 64 neurons: 7.25931%.
- Position error reduction versus 1 hidden layers x 64 neurons: 49.4494%.
- Orientation error reduction versus 1 hidden layers x 64 neurons: 43.9536%.
- Position error reduction versus 4 hidden layers x 64 neurons: 23.2084%.
- Orientation error reduction versus 4 hidden layers x 64 neurons: 16.7116%.

#### Benchmark: mean across training seeds

- Mean position MAE against MuJoCo: **1.0192 mm**.
- Mean orientation MAE against MuJoCo: **0.000876864 deg**.
- Orientation MAE in radians: 1.53042e-05 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.129238%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00561883%.
- Position error reduction versus physics-only: 91.6146%.
- Orientation error reduction versus physics-only: 88.0267%.
- Physics-only mean position MAE: **12.1545 mm**.
- Physics-only mean orientation MAE: **0.00732349 deg**.
- Seed standard deviation of mean position MAE: 0.0936151 mm.
- Seed standard deviation of mean orientation MAE: 0.000103006 deg.

#### Benchmark: comparisons with other runs

- Position error reduction versus 2 hidden layers x 32 neurons: 51.654%.
- Orientation error reduction versus 2 hidden layers x 32 neurons: 42.244%.
- Position error reduction versus 2 hidden layers x 64 neurons: 20.5194%.
- Orientation error reduction versus 2 hidden layers x 64 neurons: 8.9634%.
- Position error reduction versus 1 hidden layers x 64 neurons: 54.0149%.
- Orientation error reduction versus 1 hidden layers x 64 neurons: 41.1681%.
- Position error reduction versus 4 hidden layers x 64 neurons: 39.0778%.
- Orientation error reduction versus 4 hidden layers x 64 neurons: 26.7381%.

#### Seed 0

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 19,980.
- Source training time: 23.9819 s.
- Test mean position MAE: 0.375745 mm.
- Test mean orientation MAE: 0.000314276 deg.
- Benchmark mean position MAE: 0.982744 mm.
- Benchmark mean orientation MAE: 0.000985207 deg.

Detailed seed report: [Experiment D - Neural Network Size Data.md](<Experiment D - Neural Network Size/layers_2_width_128/seed_0/Experiment D - Neural Network Size Data.md>).

#### Seed 1

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 19,980.
- Source training time: 21.9560 s.
- Test mean position MAE: 0.369082 mm.
- Test mean orientation MAE: 0.000330144 deg.
- Benchmark mean position MAE: 0.927212 mm.
- Benchmark mean orientation MAE: 0.000907023 deg.

Detailed seed report: [Experiment D - Neural Network Size Data.md](<Experiment D - Neural Network Size/layers_2_width_128/seed_1/Experiment D - Neural Network Size Data.md>).

#### Seed 2

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 19,980.
- Source training time: 20.9513 s.
- Test mean position MAE: 0.326807 mm.
- Test mean orientation MAE: 0.000319585 deg.
- Benchmark mean position MAE: 1.14765 mm.
- Benchmark mean orientation MAE: 0.000738362 deg.

Detailed seed report: [Experiment D - Neural Network Size Data.md](<Experiment D - Neural Network Size/layers_2_width_128/seed_2/Experiment D - Neural Network Size Data.md>).

### Run: 1 hidden layers x 64 neurons

Artifacts: [1 hidden layers x 64 neurons](<Experiment D - Neural Network Size/layers_1_width_64/seed_0/>).

#### Training composition

- Training trajectories: 80.
- Hidden layers: 1.
- Neurons per hidden layer: 64.
- hover training trajectories: 16.
- climb_descent training trajectories: 16.
- figure_eight training trajectories: 16.
- circle training trajectories: 16.
- straight training trajectories: 16.

#### Test: mean across training seeds

- Mean position MAE against MuJoCo: **0.706641 mm**.
- Mean orientation MAE against MuJoCo: **0.000573338 deg**.
- Orientation MAE in radians: 1.00066e-05 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.296485%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.0106021%.
- Position error reduction versus physics-only: 95.0674%.
- Orientation error reduction versus physics-only: 94.152%.
- Physics-only mean position MAE: **14.326 mm**.
- Physics-only mean orientation MAE: **0.00980406 deg**.
- Seed standard deviation of mean position MAE: 0.0360377 mm.
- Seed standard deviation of mean orientation MAE: 5.7198e-05 deg.

#### Test: comparisons with other runs

- Position error reduction versus 2 hidden layers x 32 neurons: 2.16897%.
- Orientation error reduction versus 2 hidden layers x 32 neurons: -8.8241%.
- Position error reduction versus 2 hidden layers x 64 neurons: -68.2656%.
- Orientation error reduction versus 2 hidden layers x 64 neurons: -65.4713%.
- Position error reduction versus 2 hidden layers x 128 neurons: -97.8217%.
- Orientation error reduction versus 2 hidden layers x 128 neurons: -78.4236%.
- Position error reduction versus 4 hidden layers x 64 neurons: -51.9105%.
- Orientation error reduction versus 4 hidden layers x 64 neurons: -48.6063%.

#### Benchmark: mean across training seeds

- Mean position MAE against MuJoCo: **2.21638 mm**.
- Mean orientation MAE against MuJoCo: **0.00149046 deg**.
- Orientation MAE in radians: 2.60134e-05 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.284854%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00965391%.
- Position error reduction versus physics-only: 81.7649%.
- Orientation error reduction versus physics-only: 79.6483%.
- Physics-only mean position MAE: **12.1545 mm**.
- Physics-only mean orientation MAE: **0.00732349 deg**.
- Seed standard deviation of mean position MAE: 0.106286 mm.
- Seed standard deviation of mean orientation MAE: 0.00034883 deg.

#### Benchmark: comparisons with other runs

- Position error reduction versus 2 hidden layers x 32 neurons: -5.13418%.
- Orientation error reduction versus 2 hidden layers x 32 neurons: 1.82868%.
- Position error reduction versus 2 hidden layers x 64 neurons: -72.84%.
- Orientation error reduction versus 2 hidden layers x 64 neurons: -54.7403%.
- Position error reduction versus 2 hidden layers x 128 neurons: -117.462%.
- Orientation error reduction versus 2 hidden layers x 128 neurons: -69.9759%.
- Position error reduction versus 4 hidden layers x 64 neurons: -32.4825%.
- Orientation error reduction versus 4 hidden layers x 64 neurons: -24.5276%.

#### Seed 0

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 1,740.
- Source training time: 8.8371 s.
- Test mean position MAE: 0.675094 mm.
- Test mean orientation MAE: 0.000496026 deg.
- Benchmark mean position MAE: 2.07474 mm.
- Benchmark mean orientation MAE: 0.00117758 deg.

Detailed seed report: [Experiment D - Neural Network Size Data.md](<Experiment D - Neural Network Size/layers_1_width_64/seed_0/Experiment D - Neural Network Size Data.md>).

#### Seed 1

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 1,740.
- Source training time: 9.0678 s.
- Test mean position MAE: 0.75708 mm.
- Test mean orientation MAE: 0.000632599 deg.
- Benchmark mean position MAE: 2.24362 mm.
- Benchmark mean orientation MAE: 0.00197721 deg.

Detailed seed report: [Experiment D - Neural Network Size Data.md](<Experiment D - Neural Network Size/layers_1_width_64/seed_1/Experiment D - Neural Network Size Data.md>).

#### Seed 2

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 1,740.
- Source training time: 8.3505 s.
- Test mean position MAE: 0.687749 mm.
- Test mean orientation MAE: 0.000591388 deg.
- Benchmark mean position MAE: 2.33078 mm.
- Benchmark mean orientation MAE: 0.00131659 deg.

Detailed seed report: [Experiment D - Neural Network Size Data.md](<Experiment D - Neural Network Size/layers_1_width_64/seed_2/Experiment D - Neural Network Size Data.md>).

### Run: 4 hidden layers x 64 neurons

Artifacts: [4 hidden layers x 64 neurons](<Experiment D - Neural Network Size/layers_4_width_64/seed_0/>).

#### Training composition

- Training trajectories: 80.
- Hidden layers: 4.
- Neurons per hidden layer: 64.
- hover training trajectories: 16.
- climb_descent training trajectories: 16.
- figure_eight training trajectories: 16.
- circle training trajectories: 16.
- straight training trajectories: 16.

#### Test: mean across training seeds

- Mean position MAE against MuJoCo: **0.465169 mm**.
- Mean orientation MAE against MuJoCo: **0.00038581 deg**.
- Orientation MAE in radians: 6.73365e-06 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.159986%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00626876%.
- Position error reduction versus physics-only: 96.753%.
- Orientation error reduction versus physics-only: 96.0648%.
- Physics-only mean position MAE: **14.326 mm**.
- Physics-only mean orientation MAE: **0.00980406 deg**.
- Seed standard deviation of mean position MAE: 0.0337883 mm.
- Seed standard deviation of mean orientation MAE: 5.24406e-05 deg.

#### Test: comparisons with other runs

- Position error reduction versus 2 hidden layers x 32 neurons: 35.5995%.
- Orientation error reduction versus 2 hidden layers x 32 neurons: 26.7702%.
- Position error reduction versus 2 hidden layers x 64 neurons: -10.7663%.
- Orientation error reduction versus 2 hidden layers x 64 neurons: -11.3488%.
- Position error reduction versus 2 hidden layers x 128 neurons: -30.2225%.
- Orientation error reduction versus 2 hidden layers x 128 neurons: -20.0647%.
- Position error reduction versus 1 hidden layers x 64 neurons: 34.1717%.
- Orientation error reduction versus 1 hidden layers x 64 neurons: 32.7081%.

#### Benchmark: mean across training seeds

- Mean position MAE against MuJoCo: **1.67296 mm**.
- Mean orientation MAE against MuJoCo: **0.00119689 deg**.
- Orientation MAE in radians: 2.08897e-05 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.205524%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00773744%.
- Position error reduction versus physics-only: 86.2359%.
- Orientation error reduction versus physics-only: 83.6568%.
- Physics-only mean position MAE: **12.1545 mm**.
- Physics-only mean orientation MAE: **0.00732349 deg**.
- Seed standard deviation of mean position MAE: 0.130958 mm.
- Seed standard deviation of mean orientation MAE: 0.000116504 deg.

#### Benchmark: comparisons with other runs

- Position error reduction versus 2 hidden layers x 32 neurons: 20.643%.
- Orientation error reduction versus 2 hidden layers x 32 neurons: 21.165%.
- Position error reduction versus 2 hidden layers x 64 neurons: -30.4625%.
- Orientation error reduction versus 2 hidden layers x 64 neurons: -24.2619%.
- Position error reduction versus 2 hidden layers x 128 neurons: -64.1438%.
- Orientation error reduction versus 2 hidden layers x 128 neurons: -36.4966%.
- Position error reduction versus 1 hidden layers x 64 neurons: 24.5183%.
- Orientation error reduction versus 1 hidden layers x 64 neurons: 19.6965%.

#### Seed 0

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 14,220.
- Source training time: 20.6258 s.
- Test mean position MAE: 0.497743 mm.
- Test mean orientation MAE: 0.000443254 deg.
- Benchmark mean position MAE: 1.74188 mm.
- Benchmark mean orientation MAE: 0.00115097 deg.

Detailed seed report: [Experiment D - Neural Network Size Data.md](<Experiment D - Neural Network Size/layers_4_width_64/seed_0/Experiment D - Neural Network Size Data.md>).

#### Seed 1

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 14,220.
- Source training time: 21.3525 s.
- Test mean position MAE: 0.418606 mm.
- Test mean orientation MAE: 0.000316466 deg.
- Benchmark mean position MAE: 1.48963 mm.
- Benchmark mean orientation MAE: 0.00135688 deg.

Detailed seed report: [Experiment D - Neural Network Size Data.md](<Experiment D - Neural Network Size/layers_4_width_64/seed_1/Experiment D - Neural Network Size Data.md>).

#### Seed 2

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 14,220.
- Source training time: 21.7193 s.
- Test mean position MAE: 0.479159 mm.
- Test mean orientation MAE: 0.00039771 deg.
- Benchmark mean position MAE: 1.78737 mm.
- Benchmark mean orientation MAE: 0.00108282 deg.

Detailed seed report: [Experiment D - Neural Network Size Data.md](<Experiment D - Neural Network Size/layers_4_width_64/seed_2/Experiment D - Neural Network Size Data.md>).

## Experiment: Refresh Frequency

Each seed uses its full-data standard-network checkpoint for every schedule. No retraining occurs between schedules. Primary metrics score forecasts before replacement.

All displayed run summaries use fully recursive forecasts. Positive comparison percentages mean less error; negative percentages mean more error. The comparison denominator is the named reference run. Seed means weight each training seed equally; each seed first weights each test flight equally.

[All pairwise percentages](<Experiment E - Refresh Frequency/pairwise_comparisons.csv>).

[Comparison plot](<Experiment E - Refresh Frequency/plots/comparison_mae.png>).

### Run: No refresh

Artifacts: [No refresh](<Experiment E - Refresh Frequency/no_refresh/seed_0/>).

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

- Mean position MAE against MuJoCo: **0.419956 mm**.
- Mean orientation MAE against MuJoCo: **0.000346488 deg**.
- Orientation MAE in radians: 6.04735e-06 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.177761%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00645881%.
- Position error reduction versus physics-only: 97.0686%.
- Orientation error reduction versus physics-only: 96.4659%.
- Physics-only mean position MAE: **14.326 mm**.
- Physics-only mean orientation MAE: **0.00980406 deg**.
- Seed standard deviation of mean position MAE: 0.0210501 mm.
- Seed standard deviation of mean orientation MAE: 4.25686e-05 deg.

#### Test: comparisons with other runs

- Position error reduction versus Every 1 steps: -4.64405e+07%.
- Orientation error reduction versus Every 1 steps: -2.45761e+07%.
- Position error reduction versus Every 5 steps: -4.27698e+06%.
- Orientation error reduction versus Every 5 steps: -2.25147e+06%.
- Position error reduction versus Every 10 steps: -1.21971e+06%.
- Orientation error reduction versus Every 10 steps: -639535%.
- Position error reduction versus Every 25 steps: -212806%.
- Orientation error reduction versus Every 25 steps: -110966%.
- Position error reduction versus Every 50 steps: -57198.8%.
- Orientation error reduction versus Every 50 steps: -30719.2%.
- Position error reduction versus Every 100 steps: -15016%.
- Orientation error reduction versus Every 100 steps: -7117.5%.
- Position error reduction versus Every 200 steps: -4259.69%.
- Orientation error reduction versus Every 200 steps: -1768.91%.
- Position error reduction versus Every 500 steps: -604.177%.
- Orientation error reduction versus Every 500 steps: -212.901%.

#### Benchmark: mean across training seeds

- Mean position MAE against MuJoCo: **1.28233 mm**.
- Mean orientation MAE against MuJoCo: **0.0009632 deg**.
- Orientation MAE in radians: 1.6811e-05 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.157651%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00620006%.
- Position error reduction versus physics-only: 89.4497%.
- Orientation error reduction versus physics-only: 86.8478%.
- Physics-only mean position MAE: **12.1545 mm**.
- Physics-only mean orientation MAE: **0.00732349 deg**.
- Seed standard deviation of mean position MAE: 0.282818 mm.
- Seed standard deviation of mean orientation MAE: 0.000256719 deg.

#### Benchmark: comparisons with other runs

- Position error reduction versus Every 1 steps: -1.34187e+07%.
- Orientation error reduction versus Every 1 steps: -1.19635e+07%.
- Position error reduction versus Every 5 steps: -1.22486e+06%.
- Orientation error reduction versus Every 5 steps: -1.10375e+06%.
- Position error reduction versus Every 10 steps: -350495%.
- Orientation error reduction versus Every 10 steps: -316121%.
- Position error reduction versus Every 25 steps: -61544.1%.
- Orientation error reduction versus Every 25 steps: -55631.5%.
- Position error reduction versus Every 50 steps: -16066%.
- Orientation error reduction versus Every 50 steps: -14795.6%.
- Position error reduction versus Every 100 steps: -4164.73%.
- Orientation error reduction versus Every 100 steps: -3937.27%.
- Position error reduction versus Every 200 steps: -912.02%.
- Orientation error reduction versus Every 200 steps: -972.246%.
- Position error reduction versus Every 500 steps: -117.621%.
- Orientation error reduction versus Every 500 steps: -133.889%.

#### Seed 0

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 13.3145 s.
- Optimizer updates in this refresh run: 0.
- Test mean position MAE: 0.401772 mm.
- Test mean orientation MAE: 0.000290801 deg.
- Benchmark mean position MAE: 1.19401 mm.
- Benchmark mean orientation MAE: 0.000683165 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<Experiment E - Refresh Frequency/no_refresh/seed_0/Experiment E - Refresh Frequency Data.md>).

#### Seed 1

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 13.0851 s.
- Optimizer updates in this refresh run: 0.
- Test mean position MAE: 0.44946 mm.
- Test mean orientation MAE: 0.00039414 deg.
- Benchmark mean position MAE: 0.988661 mm.
- Benchmark mean orientation MAE: 0.00090311 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<Experiment E - Refresh Frequency/no_refresh/seed_1/Experiment E - Refresh Frequency Data.md>).

#### Seed 2

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 12.4214 s.
- Optimizer updates in this refresh run: 0.
- Test mean position MAE: 0.408635 mm.
- Test mean orientation MAE: 0.000354522 deg.
- Benchmark mean position MAE: 1.66432 mm.
- Benchmark mean orientation MAE: 0.00130332 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<Experiment E - Refresh Frequency/no_refresh/seed_2/Experiment E - Refresh Frequency Data.md>).

### Run: Every 1 steps

Artifacts: [Every 1 steps](<Experiment E - Refresh Frequency/every_1_steps/seed_0/>).

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

- Mean position MAE against MuJoCo: **9.04287E-07 mm**.
- Mean orientation MAE against MuJoCo: **1.40985e-09 deg**.
- Orientation MAE in radians: 2.46065e-11 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 3.27556e-07%.
- Orientation MAE as a percentage of MuJoCo angular travel: 2.35069e-08%.
- Position error reduction versus physics-only: 97.8449%.
- Orientation error reduction versus physics-only: 98.0222%.
- Physics-only mean position MAE: **4.19604E-05 mm**.
- Physics-only mean orientation MAE: **7.12851e-08 deg**.
- Seed standard deviation of mean position MAE: 2.76679E-08 mm.
- Seed standard deviation of mean orientation MAE: 4.83555e-11 deg.

#### Test: comparisons with other runs

- Position error reduction versus No refresh: 99.9998%.
- Orientation error reduction versus No refresh: 99.9996%.
- Position error reduction versus Every 5 steps: 90.7902%.
- Orientation error reduction versus Every 5 steps: 90.8384%.
- Position error reduction versus Every 10 steps: 97.3734%.
- Orientation error reduction versus Every 10 steps: 97.3973%.
- Position error reduction versus Every 25 steps: 99.5416%.
- Orientation error reduction versus Every 25 steps: 99.5481%.
- Position error reduction versus Every 50 steps: 99.8766%.
- Orientation error reduction versus Every 50 steps: 99.8746%.
- Position error reduction versus Every 100 steps: 99.9675%.
- Orientation error reduction versus Every 100 steps: 99.9706%.
- Position error reduction versus Every 200 steps: 99.9906%.
- Orientation error reduction versus Every 200 steps: 99.9924%.
- Position error reduction versus Every 500 steps: 99.9985%.
- Orientation error reduction versus Every 500 steps: 99.9987%.

#### Benchmark: mean across training seeds

- Mean position MAE against MuJoCo: **9.55622E-06 mm**.
- Mean orientation MAE against MuJoCo: **8.05109e-09 deg**.
- Orientation MAE in radians: 1.40518e-10 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 1.13353e-06%.
- Orientation MAE as a percentage of MuJoCo angular travel: 5.1059e-08%.
- Position error reduction versus physics-only: 77.7614%.
- Orientation error reduction versus physics-only: 91.0024%.
- Physics-only mean position MAE: **4.29713E-05 mm**.
- Physics-only mean orientation MAE: **8.94808e-08 deg**.
- Seed standard deviation of mean position MAE: 1.19555E-06 mm.
- Seed standard deviation of mean orientation MAE: 1.06555e-09 deg.

#### Benchmark: comparisons with other runs

- Position error reduction versus No refresh: 99.9993%.
- Orientation error reduction versus No refresh: 99.9992%.
- Position error reduction versus Every 5 steps: 90.8713%.
- Orientation error reduction versus Every 5 steps: 90.7733%.
- Position error reduction versus Every 10 steps: 97.3873%.
- Orientation error reduction versus Every 10 steps: 97.3568%.
- Position error reduction versus Every 25 steps: 99.5406%.
- Orientation error reduction versus Every 25 steps: 99.5342%.
- Position error reduction versus Every 50 steps: 99.8795%.
- Orientation error reduction versus Every 50 steps: 99.8755%.
- Position error reduction versus Every 100 steps: 99.9682%.
- Orientation error reduction versus Every 100 steps: 99.9663%.
- Position error reduction versus Every 200 steps: 99.9925%.
- Orientation error reduction versus Every 200 steps: 99.991%.
- Position error reduction versus Every 500 steps: 99.9984%.
- Orientation error reduction versus Every 500 steps: 99.998%.

#### Seed 0

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 13.3145 s.
- Optimizer updates in this refresh run: 0.
- Test mean position MAE: 8.90396E-07 mm.
- Test mean orientation MAE: 1.3442e-09 deg.
- Benchmark mean position MAE: 9.15103E-06 mm.
- Benchmark mean orientation MAE: 7.14534e-09 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<Experiment E - Refresh Frequency/every_1_steps/seed_0/Experiment E - Refresh Frequency Data.md>).

#### Seed 1

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 13.0851 s.
- Optimizer updates in this refresh run: 0.
- Test mean position MAE: 8.79553E-07 mm.
- Test mean orientation MAE: 1.4261e-09 deg.
- Benchmark mean position MAE: 8.33724E-06 mm.
- Benchmark mean orientation MAE: 7.46099e-09 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<Experiment E - Refresh Frequency/every_1_steps/seed_1/Experiment E - Refresh Frequency Data.md>).

#### Seed 2

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 12.4214 s.
- Optimizer updates in this refresh run: 0.
- Test mean position MAE: 9.42911E-07 mm.
- Test mean orientation MAE: 1.45925e-09 deg.
- Benchmark mean position MAE: 1.11804E-05 mm.
- Benchmark mean orientation MAE: 9.54695e-09 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<Experiment E - Refresh Frequency/every_1_steps/seed_2/Experiment E - Refresh Frequency Data.md>).

### Run: Every 5 steps

Artifacts: [Every 5 steps](<Experiment E - Refresh Frequency/every_5_steps/seed_0/>).

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

- Mean position MAE against MuJoCo: **9.81876E-06 mm**.
- Mean orientation MAE against MuJoCo: **1.53887e-08 deg**.
- Orientation MAE in radians: 2.68584e-10 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 3.55856e-06%.
- Orientation MAE as a percentage of MuJoCo angular travel: 2.54633e-07%.
- Position error reduction versus physics-only: 97.8728%.
- Orientation error reduction versus physics-only: 98.0379%.
- Physics-only mean position MAE: **0.000461582 mm**.
- Physics-only mean orientation MAE: **7.843e-07 deg**.
- Seed standard deviation of mean position MAE: 4.26575E-07 mm.
- Seed standard deviation of mean orientation MAE: 6.15888e-10 deg.

#### Test: comparisons with other runs

- Position error reduction versus No refresh: 99.9977%.
- Orientation error reduction versus No refresh: 99.9956%.
- Position error reduction versus Every 1 steps: -985.801%.
- Orientation error reduction versus Every 1 steps: -991.513%.
- Position error reduction versus Every 10 steps: 71.4804%.
- Orientation error reduction versus Every 10 steps: 71.5916%.
- Position error reduction versus Every 25 steps: 95.0222%.
- Orientation error reduction versus Every 25 steps: 95.0672%.
- Position error reduction versus Every 50 steps: 98.6603%.
- Orientation error reduction versus Every 50 steps: 98.6312%.
- Position error reduction versus Every 100 steps: 99.6466%.
- Orientation error reduction versus Every 100 steps: 99.6794%.
- Position error reduction versus Every 200 steps: 99.8981%.
- Orientation error reduction versus Every 200 steps: 99.917%.
- Position error reduction versus Every 500 steps: 99.9835%.
- Orientation error reduction versus Every 500 steps: 99.9861%.

#### Benchmark: mean across training seeds

- Mean position MAE against MuJoCo: **0.000104683 mm**.
- Mean orientation MAE against MuJoCo: **8.72583e-08 deg**.
- Orientation MAE in radians: 1.52294e-09 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 1.24293e-05%.
- Orientation MAE as a percentage of MuJoCo angular travel: 5.5239e-07%.
- Position error reduction versus physics-only: 77.8536%.
- Orientation error reduction versus physics-only: 91.1213%.
- Physics-only mean position MAE: **0.000472688 mm**.
- Physics-only mean orientation MAE: **9.82776e-07 deg**.
- Seed standard deviation of mean position MAE: 1.23722E-05 mm.
- Seed standard deviation of mean orientation MAE: 1.06225e-08 deg.

#### Benchmark: comparisons with other runs

- Position error reduction versus No refresh: 99.9918%.
- Orientation error reduction versus No refresh: 99.9909%.
- Position error reduction versus Every 1 steps: -995.448%.
- Orientation error reduction versus Every 1 steps: -983.807%.
- Position error reduction versus Every 10 steps: 71.379%.
- Orientation error reduction versus Every 10 steps: 71.3529%.
- Position error reduction versus Every 25 steps: 94.9677%.
- Orientation error reduction versus Every 25 steps: 94.9512%.
- Position error reduction versus Every 50 steps: 98.6803%.
- Orientation error reduction versus Every 50 steps: 98.6506%.
- Position error reduction versus Every 100 steps: 99.6518%.
- Orientation error reduction versus Every 100 steps: 99.6343%.
- Position error reduction versus Every 200 steps: 99.9174%.
- Orientation error reduction versus Every 200 steps: 99.9029%.
- Position error reduction versus Every 500 steps: 99.9822%.
- Orientation error reduction versus Every 500 steps: 99.9788%.

#### Seed 0

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 13.3145 s.
- Optimizer updates in this refresh run: 0.
- Test mean position MAE: 9.64966E-06 mm.
- Test mean orientation MAE: 1.46448e-08 deg.
- Benchmark mean position MAE: 0.000101895 mm.
- Benchmark mean orientation MAE: 7.85528e-08 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<Experiment E - Refresh Frequency/every_5_steps/seed_0/Experiment E - Refresh Frequency Data.md>).

#### Seed 1

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 13.0851 s.
- Optimizer updates in this refresh run: 0.
- Test mean position MAE: 9.4018E-06 mm.
- Test mean orientation MAE: 1.53683e-08 deg.
- Benchmark mean position MAE: 9.11184E-05 mm.
- Benchmark mean orientation MAE: 8.10083e-08 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<Experiment E - Refresh Frequency/every_5_steps/seed_1/Experiment E - Refresh Frequency Data.md>).

#### Seed 2

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 12.4214 s.
- Optimizer updates in this refresh run: 0.
- Test mean position MAE: 1.04048E-05 mm.
- Test mean orientation MAE: 1.6153e-08 deg.
- Benchmark mean position MAE: 0.000121037 mm.
- Benchmark mean orientation MAE: 1.02214e-07 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<Experiment E - Refresh Frequency/every_5_steps/seed_2/Experiment E - Refresh Frequency Data.md>).

### Run: Every 10 steps

Artifacts: [Every 10 steps](<Experiment E - Refresh Frequency/every_10_steps/seed_0/>).

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

- Mean position MAE against MuJoCo: **3.44281E-05 mm**.
- Mean orientation MAE against MuJoCo: **5.41696e-08 deg**.
- Orientation MAE in radians: 9.45437e-10 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 1.26682e-05%.
- Orientation MAE as a percentage of MuJoCo angular travel: 8.98819e-07%.
- Position error reduction versus physics-only: 97.8688%.
- Orientation error reduction versus physics-only: 98.0264%.
- Physics-only mean position MAE: **0.00161545 mm**.
- Physics-only mean orientation MAE: **2.74474e-06 deg**.
- Seed standard deviation of mean position MAE: 1.63552E-06 mm.
- Seed standard deviation of mean orientation MAE: 2.14131e-09 deg.

#### Test: comparisons with other runs

- Position error reduction versus No refresh: 99.9918%.
- Orientation error reduction versus No refresh: 99.9844%.
- Position error reduction versus Every 1 steps: -3707.21%.
- Orientation error reduction versus Every 1 steps: -3742.22%.
- Position error reduction versus Every 5 steps: -250.636%.
- Orientation error reduction versus Every 5 steps: -252.009%.
- Position error reduction versus Every 25 steps: 82.5459%.
- Orientation error reduction versus Every 25 steps: 82.6361%.
- Position error reduction versus Every 50 steps: 95.3026%.
- Orientation error reduction versus Every 50 steps: 95.1818%.
- Position error reduction versus Every 100 steps: 98.7608%.
- Orientation error reduction versus Every 100 steps: 98.8716%.
- Position error reduction versus Every 200 steps: 99.6426%.
- Orientation error reduction versus Every 200 steps: 99.7078%.
- Position error reduction versus Every 500 steps: 99.9423%.
- Orientation error reduction versus Every 500 steps: 99.9511%.

#### Benchmark: mean across training seeds

- Mean position MAE against MuJoCo: **0.000365758 mm**.
- Mean orientation MAE against MuJoCo: **3.04597e-07 deg**.
- Orientation MAE in radians: 5.31622e-09 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 4.34441e-05%.
- Orientation MAE as a percentage of MuJoCo angular travel: 1.92804e-06%.
- Position error reduction versus physics-only: 77.8906%.
- Orientation error reduction versus physics-only: 91.121%.
- Physics-only mean position MAE: **0.00165431 mm**.
- Physics-only mean orientation MAE: **3.43052e-06 deg**.
- Seed standard deviation of mean position MAE: 4.29749E-05 mm.
- Seed standard deviation of mean orientation MAE: 3.6607e-08 deg.

#### Benchmark: comparisons with other runs

- Position error reduction versus No refresh: 99.9715%.
- Orientation error reduction versus No refresh: 99.9684%.
- Position error reduction versus Every 1 steps: -3727.43%.
- Orientation error reduction versus Every 1 steps: -3683.3%.
- Position error reduction versus Every 5 steps: -249.394%.
- Orientation error reduction versus Every 5 steps: -249.075%.
- Position error reduction versus Every 25 steps: 82.4173%.
- Orientation error reduction versus Every 25 steps: 82.3758%.
- Position error reduction versus Every 50 steps: 95.389%.
- Orientation error reduction versus Every 50 steps: 95.2895%.
- Position error reduction versus Every 100 steps: 98.7836%.
- Orientation error reduction versus Every 100 steps: 98.7233%.
- Position error reduction versus Every 200 steps: 99.7113%.
- Orientation error reduction versus Every 200 steps: 99.6609%.
- Position error reduction versus Every 500 steps: 99.9379%.
- Orientation error reduction versus Every 500 steps: 99.926%.

#### Seed 0

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 13.3145 s.
- Optimizer updates in this refresh run: 0.
- Test mean position MAE: 3.3889E-05 mm.
- Test mean orientation MAE: 5.15467e-08 deg.
- Benchmark mean position MAE: 0.000357018 mm.
- Benchmark mean orientation MAE: 2.74739e-07 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<Experiment E - Refresh Frequency/every_10_steps/seed_0/Experiment E - Refresh Frequency Data.md>).

#### Seed 1

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 13.0851 s.
- Optimizer updates in this refresh run: 0.
- Test mean position MAE: 3.27497E-05 mm.
- Test mean orientation MAE: 5.41701e-08 deg.
- Benchmark mean position MAE: 0.000318042 mm.
- Benchmark mean orientation MAE: 2.829e-07 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<Experiment E - Refresh Frequency/every_10_steps/seed_1/Experiment E - Refresh Frequency Data.md>).

#### Seed 2

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 12.4214 s.
- Optimizer updates in this refresh run: 0.
- Test mean position MAE: 3.66455E-05 mm.
- Test mean orientation MAE: 5.67919e-08 deg.
- Benchmark mean position MAE: 0.000422214 mm.
- Benchmark mean orientation MAE: 3.56152e-07 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<Experiment E - Refresh Frequency/every_10_steps/seed_2/Experiment E - Refresh Frequency Data.md>).

### Run: Every 25 steps

Artifacts: [Every 25 steps](<Experiment E - Refresh Frequency/every_25_steps/seed_0/>).

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

- Mean position MAE against MuJoCo: **0.000197249 mm**.
- Mean orientation MAE against MuJoCo: **3.11966e-07 deg**.
- Orientation MAE in radians: 5.44484e-09 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 7.29979e-05%.
- Orientation MAE as a percentage of MuJoCo angular travel: 5.16587e-06%.
- Position error reduction versus physics-only: 97.8709%.
- Orientation error reduction versus physics-only: 98.0106%.
- Physics-only mean position MAE: **0.00926426 mm**.
- Physics-only mean orientation MAE: **1.56815e-05 deg**.
- Seed standard deviation of mean position MAE: 1.0426E-05 mm.
- Seed standard deviation of mean orientation MAE: 1.65152e-08 deg.

#### Test: comparisons with other runs

- Position error reduction versus No refresh: 99.953%.
- Orientation error reduction versus No refresh: 99.91%.
- Position error reduction versus Every 1 steps: -21712.7%.
- Orientation error reduction versus Every 1 steps: -22027.6%.
- Position error reduction versus Every 5 steps: -1908.9%.
- Orientation error reduction versus Every 5 steps: -1927.24%.
- Position error reduction versus Every 10 steps: -472.931%.
- Orientation error reduction versus Every 10 steps: -475.907%.
- Position error reduction versus Every 50 steps: 73.0873%.
- Orientation error reduction versus Every 50 steps: 72.2514%.
- Position error reduction versus Every 100 steps: 92.9001%.
- Orientation error reduction versus Every 100 steps: 93.5016%.
- Position error reduction versus Every 200 steps: 97.9523%.
- Orientation error reduction versus Every 200 steps: 98.3173%.
- Position error reduction versus Every 500 steps: 99.6693%.
- Orientation error reduction versus Every 500 steps: 99.7183%.

#### Benchmark: mean across training seeds

- Mean position MAE against MuJoCo: **0.00208021 mm**.
- Mean orientation MAE against MuJoCo: **1.72829e-06 deg**.
- Orientation MAE in radians: 3.01643e-08 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.00024715%.
- Orientation MAE as a percentage of MuJoCo angular travel: 1.09386e-05%.
- Position error reduction versus physics-only: 78.0768%.
- Orientation error reduction versus physics-only: 91.128%.
- Physics-only mean position MAE: **0.00948864 mm**.
- Physics-only mean orientation MAE: **1.94801e-05 deg**.
- Seed standard deviation of mean position MAE: 0.000244218 mm.
- Seed standard deviation of mean orientation MAE: 2.09636e-07 deg.

#### Benchmark: comparisons with other runs

- Position error reduction versus No refresh: 99.8378%.
- Orientation error reduction versus No refresh: 99.8206%.
- Position error reduction versus Every 1 steps: -21668.2%.
- Orientation error reduction versus Every 1 steps: -21366.5%.
- Position error reduction versus Every 5 steps: -1887.15%.
- Orientation error reduction versus Every 5 steps: -1880.66%.
- Position error reduction versus Every 10 steps: -468.74%.
- Orientation error reduction versus Every 10 steps: -467.401%.
- Position error reduction versus Every 50 steps: 73.7753%.
- Orientation error reduction versus Every 50 steps: 73.2726%.
- Position error reduction versus Every 100 steps: 93.0817%.
- Orientation error reduction versus Every 100 steps: 92.7559%.
- Position error reduction versus Every 200 steps: 98.3583%.
- Orientation error reduction versus Every 200 steps: 98.076%.
- Position error reduction versus Every 500 steps: 99.647%.
- Orientation error reduction versus Every 500 steps: 99.5803%.

#### Seed 0

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 13.3145 s.
- Optimizer updates in this refresh run: 0.
- Test mean position MAE: 0.000194008 mm.
- Test mean orientation MAE: 2.92166e-07 deg.
- Benchmark mean position MAE: 0.0020357 mm.
- Benchmark mean orientation MAE: 1.55261e-06 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<Experiment E - Refresh Frequency/every_25_steps/seed_0/Experiment E - Refresh Frequency Data.md>).

#### Seed 1

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 13.0851 s.
- Optimizer updates in this refresh run: 0.
- Test mean position MAE: 0.000186413 mm.
- Test mean orientation MAE: 3.11138e-07 deg.
- Benchmark mean position MAE: 0.00180586 mm.
- Benchmark mean orientation MAE: 1.60931e-06 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<Experiment E - Refresh Frequency/every_25_steps/seed_1/Experiment E - Refresh Frequency Data.md>).

#### Seed 2

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 12.4214 s.
- Optimizer updates in this refresh run: 0.
- Test mean position MAE: 0.000211327 mm.
- Test mean orientation MAE: 3.32595e-07 deg.
- Benchmark mean position MAE: 0.00239908 mm.
- Benchmark mean orientation MAE: 2.02294e-06 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<Experiment E - Refresh Frequency/every_25_steps/seed_2/Experiment E - Refresh Frequency Data.md>).

### Run: Every 50 steps

Artifacts: [Every 50 steps](<Experiment E - Refresh Frequency/every_50_steps/seed_0/>).

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

- Mean position MAE against MuJoCo: **0.000732923 mm**.
- Mean orientation MAE against MuJoCo: **1.12426e-06 deg**.
- Orientation MAE in radians: 1.9622e-08 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.000280204%.
- Orientation MAE as a percentage of MuJoCo angular travel: 1.95079e-05%.
- Position error reduction versus physics-only: 97.9531%.
- Orientation error reduction versus physics-only: 98.1536%.
- Physics-only mean position MAE: **0.035806 mm**.
- Physics-only mean orientation MAE: **6.08885e-05 deg**.
- Seed standard deviation of mean position MAE: 3.33814E-05 mm.
- Seed standard deviation of mean orientation MAE: 7.46932e-08 deg.

#### Test: comparisons with other runs

- Position error reduction versus No refresh: 99.8255%.
- Orientation error reduction versus No refresh: 99.6755%.
- Position error reduction versus Every 1 steps: -80949.9%.
- Orientation error reduction versus Every 1 steps: -79643.1%.
- Position error reduction versus Every 5 steps: -7364.52%.
- Orientation error reduction versus Every 5 steps: -7205.74%.
- Position error reduction versus Every 10 steps: -2028.85%.
- Orientation error reduction versus Every 10 steps: -1975.44%.
- Position error reduction versus Every 25 steps: -271.572%.
- Orientation error reduction versus Every 25 steps: -260.378%.
- Position error reduction versus Every 100 steps: 73.6189%.
- Orientation error reduction versus Every 100 steps: 76.5812%.
- Position error reduction versus Every 200 steps: 92.3913%.
- Orientation error reduction versus Every 200 steps: 93.9359%.
- Position error reduction versus Every 500 steps: 98.771%.
- Orientation error reduction versus Every 500 steps: 98.9847%.

#### Benchmark: mean across training seeds

- Mean position MAE against MuJoCo: **0.00793226 mm**.
- Mean orientation MAE against MuJoCo: **6.46635e-06 deg**.
- Orientation MAE in radians: 1.12859e-07 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.000942308%.
- Orientation MAE as a percentage of MuJoCo angular travel: 4.10047e-05%.
- Position error reduction versus physics-only: 78.4227%.
- Orientation error reduction versus physics-only: 90.9954%.
- Physics-only mean position MAE: **0.0367621 mm**.
- Physics-only mean orientation MAE: **7.18119e-05 deg**.
- Seed standard deviation of mean position MAE: 0.000950897 mm.
- Seed standard deviation of mean orientation MAE: 7.67499e-07 deg.

#### Benchmark: comparisons with other runs

- Position error reduction versus No refresh: 99.3814%.
- Orientation error reduction versus No refresh: 99.3287%.
- Position error reduction versus Every 1 steps: -82906.3%.
- Orientation error reduction versus Every 1 steps: -80216.4%.
- Position error reduction versus Every 5 steps: -7477.38%.
- Orientation error reduction versus Every 5 steps: -7310.59%.
- Position error reduction versus Every 10 steps: -2068.72%.
- Orientation error reduction versus Every 10 steps: -2022.92%.
- Position error reduction versus Every 25 steps: -281.32%.
- Orientation error reduction versus Every 25 steps: -274.148%.
- Position error reduction versus Every 100 steps: 73.6191%.
- Orientation error reduction versus Every 100 steps: 72.8962%.
- Position error reduction versus Every 200 steps: 93.7398%.
- Orientation error reduction versus Every 200 steps: 92.8016%.
- Position error reduction versus Every 500 steps: 98.6538%.
- Orientation error reduction versus Every 500 steps: 98.4298%.

#### Seed 0

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 13.3145 s.
- Optimizer updates in this refresh run: 0.
- Test mean position MAE: 0.000735452 mm.
- Test mean orientation MAE: 1.03541e-06 deg.
- Benchmark mean position MAE: 0.00776908 mm.
- Benchmark mean orientation MAE: 5.79697e-06 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<Experiment E - Refresh Frequency/every_50_steps/seed_0/Experiment E - Refresh Frequency Data.md>).

#### Seed 1

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 13.0851 s.
- Optimizer updates in this refresh run: 0.
- Test mean position MAE: 0.000690834 mm.
- Test mean orientation MAE: 1.1192e-06 deg.
- Benchmark mean position MAE: 0.00685785 mm.
- Benchmark mean orientation MAE: 6.06109e-06 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<Experiment E - Refresh Frequency/every_50_steps/seed_1/Experiment E - Refresh Frequency Data.md>).

#### Seed 2

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 12.4214 s.
- Optimizer updates in this refresh run: 0.
- Test mean position MAE: 0.000772484 mm.
- Test mean orientation MAE: 1.21816e-06 deg.
- Benchmark mean position MAE: 0.00916985 mm.
- Benchmark mean orientation MAE: 7.54099e-06 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<Experiment E - Refresh Frequency/every_50_steps/seed_2/Experiment E - Refresh Frequency Data.md>).

### Run: Every 100 steps

Artifacts: [Every 100 steps](<Experiment E - Refresh Frequency/every_100_steps/seed_0/>).

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

- Mean position MAE against MuJoCo: **0.00277821 mm**.
- Mean orientation MAE against MuJoCo: **4.80066e-06 deg**.
- Orientation MAE in radians: 8.37873e-08 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.00104599%.
- Orientation MAE as a percentage of MuJoCo angular travel: 8.33547e-05%.
- Position error reduction versus physics-only: 97.9983%.
- Orientation error reduction versus physics-only: 98.1327%.
- Physics-only mean position MAE: **0.138796 mm**.
- Physics-only mean orientation MAE: **0.000257092 deg**.
- Seed standard deviation of mean position MAE: 9.59523E-05 mm.
- Seed standard deviation of mean orientation MAE: 3.13781e-07 deg.

#### Test: comparisons with other runs

- Position error reduction versus No refresh: 99.3385%.
- Orientation error reduction versus No refresh: 98.6145%.
- Position error reduction versus Every 1 steps: -307127%.
- Orientation error reduction versus Every 1 steps: -340409%.
- Position error reduction versus Every 5 steps: -28194.9%.
- Orientation error reduction versus Every 5 steps: -31096%.
- Position error reduction versus Every 10 steps: -7969.61%.
- Orientation error reduction versus Every 10 steps: -8762.28%.
- Position error reduction versus Every 25 steps: -1308.48%.
- Orientation error reduction versus Every 25 steps: -1438.84%.
- Position error reduction versus Every 50 steps: -279.059%.
- Orientation error reduction versus Every 50 steps: -327.007%.
- Position error reduction versus Every 200 steps: 71.1586%.
- Orientation error reduction versus Every 200 steps: 74.1058%.
- Position error reduction versus Every 500 steps: 95.3415%.
- Orientation error reduction versus Every 500 steps: 95.6647%.

#### Benchmark: mean across training seeds

- Mean position MAE against MuJoCo: **0.0300682 mm**.
- Mean orientation MAE against MuJoCo: **2.38577e-05 deg**.
- Orientation MAE in radians: 4.16396e-07 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.00355096%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.000150994%.
- Position error reduction versus physics-only: 78.943%.
- Orientation error reduction versus physics-only: 90.9588%.
- Physics-only mean position MAE: **0.142794 mm**.
- Physics-only mean orientation MAE: **0.000263877 deg**.
- Seed standard deviation of mean position MAE: 0.00408064 mm.
- Seed standard deviation of mean orientation MAE: 2.93991e-06 deg.

#### Benchmark: comparisons with other runs

- Position error reduction versus No refresh: 97.6552%.
- Orientation error reduction versus No refresh: 97.5231%.
- Position error reduction versus Every 1 steps: -314545%.
- Orientation error reduction versus Every 1 steps: -296229%.
- Position error reduction versus Every 5 steps: -28623%.
- Orientation error reduction versus Every 5 steps: -27241.5%.
- Position error reduction versus Every 10 steps: -8120.79%.
- Orientation error reduction versus Every 10 steps: -7732.55%.
- Position error reduction versus Every 25 steps: -1345.44%.
- Orientation error reduction versus Every 25 steps: -1280.42%.
- Position error reduction versus Every 50 steps: -279.062%.
- Orientation error reduction versus Every 50 steps: -268.952%.
- Position error reduction versus Every 200 steps: 76.27%.
- Orientation error reduction versus Every 200 steps: 73.4413%.
- Position error reduction versus Every 500 steps: 94.8972%.
- Orientation error reduction versus Every 500 steps: 94.2068%.

#### Seed 0

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 13.3145 s.
- Optimizer updates in this refresh run: 0.
- Test mean position MAE: 0.00272404 mm.
- Test mean orientation MAE: 4.35691e-06 deg.
- Benchmark mean position MAE: 0.0300359 mm.
- Benchmark mean orientation MAE: 2.12913e-05 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<Experiment E - Refresh Frequency/every_100_steps/seed_0/Experiment E - Refresh Frequency Data.md>).

#### Seed 1

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 13.0851 s.
- Optimizer updates in this refresh run: 0.
- Test mean position MAE: 0.00269755 mm.
- Test mean orientation MAE: 5.02417e-06 deg.
- Benchmark mean position MAE: 0.0250867 mm.
- Benchmark mean orientation MAE: 2.23081e-05 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<Experiment E - Refresh Frequency/every_100_steps/seed_1/Experiment E - Refresh Frequency Data.md>).

#### Seed 2

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 12.4214 s.
- Optimizer updates in this refresh run: 0.
- Test mean position MAE: 0.00291304 mm.
- Test mean orientation MAE: 5.0209e-06 deg.
- Benchmark mean position MAE: 0.035082 mm.
- Benchmark mean orientation MAE: 2.79737e-05 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<Experiment E - Refresh Frequency/every_100_steps/seed_2/Experiment E - Refresh Frequency Data.md>).

### Run: Every 200 steps

Artifacts: [Every 200 steps](<Experiment E - Refresh Frequency/every_200_steps/seed_0/>).

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

- Mean position MAE against MuJoCo: **0.00963271 mm**.
- Mean orientation MAE against MuJoCo: **1.85396e-05 deg**.
- Orientation MAE in radians: 3.23576e-07 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.00380793%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.000327787%.
- Position error reduction versus physics-only: 97.9886%.
- Orientation error reduction versus physics-only: 98.0597%.
- Physics-only mean position MAE: **0.478894 mm**.
- Physics-only mean orientation MAE: **0.000955521 deg**.
- Seed standard deviation of mean position MAE: 0.00029372 mm.
- Seed standard deviation of mean orientation MAE: 1.30848e-06 deg.

#### Test: comparisons with other runs

- Position error reduction versus No refresh: 97.7063%.
- Orientation error reduction versus No refresh: 94.6493%.
- Position error reduction versus Every 1 steps: -1.06513e+06%.
- Orientation error reduction versus Every 1 steps: -1.3149e+06%.
- Position error reduction versus Every 5 steps: -98005.2%.
- Orientation error reduction versus Every 5 steps: -120375%.
- Position error reduction versus Every 10 steps: -27879.2%.
- Orientation error reduction versus Every 10 steps: -34125%.
- Position error reduction versus Every 25 steps: -4783.52%.
- Orientation error reduction versus Every 25 steps: -5842.81%.
- Position error reduction versus Every 50 steps: -1214.29%.
- Orientation error reduction versus Every 50 steps: -1549.05%.
- Position error reduction versus Every 100 steps: -246.723%.
- Orientation error reduction versus Every 100 steps: -286.187%.
- Position error reduction versus Every 500 steps: 83.848%.
- Orientation error reduction versus Every 500 steps: 83.2576%.

#### Benchmark: mean across training seeds

- Mean position MAE against MuJoCo: **0.12671 mm**.
- Mean orientation MAE against MuJoCo: **8.983e-05 deg**.
- Orientation MAE in radians: 1.56783e-06 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.0146113%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00055857%.
- Position error reduction versus physics-only: 79.5107%.
- Orientation error reduction versus physics-only: 90.4173%.
- Physics-only mean position MAE: **0.618421 mm**.
- Physics-only mean orientation MAE: **0.000937417 deg**.
- Seed standard deviation of mean position MAE: 0.0177039 mm.
- Seed standard deviation of mean orientation MAE: 8.5213e-06 deg.

#### Benchmark: comparisons with other runs

- Position error reduction versus No refresh: 90.1188%.
- Orientation error reduction versus No refresh: 90.6738%.
- Position error reduction versus Every 1 steps: -1.32584e+06%.
- Orientation error reduction versus Every 1 steps: -1.11565e+06%.
- Position error reduction versus Every 5 steps: -120941%.
- Orientation error reduction versus Every 5 steps: -102847%.
- Position error reduction versus Every 10 steps: -34543.1%.
- Orientation error reduction versus Every 10 steps: -29391.4%.
- Position error reduction versus Every 25 steps: -5991.2%.
- Orientation error reduction versus Every 25 steps: -5097.63%.
- Position error reduction versus Every 50 steps: -1497.4%.
- Orientation error reduction versus Every 50 steps: -1289.19%.
- Position error reduction versus Every 100 steps: -321.408%.
- Orientation error reduction versus Every 100 steps: -276.524%.
- Position error reduction versus Every 500 steps: 78.4964%.
- Orientation error reduction versus Every 500 steps: 78.187%.

#### Seed 0

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 13.3145 s.
- Optimizer updates in this refresh run: 0.
- Test mean position MAE: 0.0094704 mm.
- Test mean orientation MAE: 1.66891e-05 deg.
- Benchmark mean position MAE: 0.130021 mm.
- Benchmark mean orientation MAE: 8.13549e-05 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<Experiment E - Refresh Frequency/every_200_steps/seed_0/Experiment E - Refresh Frequency Data.md>).

#### Seed 1

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 13.0851 s.
- Optimizer updates in this refresh run: 0.
- Test mean position MAE: 0.00938273 mm.
- Test mean orientation MAE: 1.94751e-05 deg.
- Benchmark mean position MAE: 0.103562 mm.
- Benchmark mean orientation MAE: 8.66482e-05 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<Experiment E - Refresh Frequency/every_200_steps/seed_1/Experiment E - Refresh Frequency Data.md>).

#### Seed 2

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 12.4214 s.
- Optimizer updates in this refresh run: 0.
- Test mean position MAE: 0.010045 mm.
- Test mean orientation MAE: 1.94544e-05 deg.
- Benchmark mean position MAE: 0.146547 mm.
- Benchmark mean orientation MAE: 0.000101487 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<Experiment E - Refresh Frequency/every_200_steps/seed_2/Experiment E - Refresh Frequency Data.md>).

### Run: Every 500 steps

Artifacts: [Every 500 steps](<Experiment E - Refresh Frequency/every_500_steps/seed_0/>).

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

- Mean position MAE against MuJoCo: **0.0596379 mm**.
- Mean orientation MAE against MuJoCo: **0.000110734 deg**.
- Orientation MAE in radians: 1.93267e-06 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.023349%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00190928%.
- Position error reduction versus physics-only: 98.3462%.
- Orientation error reduction versus physics-only: 98.1986%.
- Physics-only mean position MAE: **3.60604 mm**.
- Physics-only mean orientation MAE: **0.0061472 deg**.
- Seed standard deviation of mean position MAE: 0.00504099 mm.
- Seed standard deviation of mean orientation MAE: 9.57654e-06 deg.

#### Test: comparisons with other runs

- Position error reduction versus No refresh: 85.799%.
- Orientation error reduction versus No refresh: 68.041%.
- Position error reduction versus Every 1 steps: -6.59492e+06%.
- Orientation error reduction versus Every 1 steps: -7.8542e+06%.
- Position error reduction versus Every 5 steps: -607287%.
- Orientation error reduction versus Every 5 steps: -719479%.
- Position error reduction versus Every 10 steps: -173124%.
- Orientation error reduction versus Every 10 steps: -204321%.
- Position error reduction versus Every 25 steps: -30134.8%.
- Orientation error reduction versus Every 25 steps: -35395.5%.
- Position error reduction versus Every 50 steps: -8036.99%.
- Orientation error reduction versus Every 50 steps: -9749.5%.
- Position error reduction versus Every 100 steps: -2046.63%.
- Orientation error reduction versus Every 100 steps: -2206.64%.
- Position error reduction versus Every 200 steps: -519.118%.
- Orientation error reduction versus Every 200 steps: -497.284%.

#### Benchmark: mean across training seeds

- Mean position MAE against MuJoCo: **0.589248 mm**.
- Mean orientation MAE against MuJoCo: **0.00041182 deg**.
- Orientation MAE in radians: 7.18761e-06 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.0686408%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00259793%.
- Position error reduction versus physics-only: 82.9673%.
- Orientation error reduction versus physics-only: 85.4175%.
- Physics-only mean position MAE: **3.4595 mm**.
- Physics-only mean orientation MAE: **0.00282407 deg**.
- Seed standard deviation of mean position MAE: 0.0473873 mm.
- Seed standard deviation of mean orientation MAE: 3.30924e-05 deg.

#### Benchmark: comparisons with other runs

- Position error reduction versus No refresh: 54.0486%.
- Orientation error reduction versus No refresh: 57.2446%.
- Position error reduction versus Every 1 steps: -6.16603e+06%.
- Orientation error reduction versus Every 1 steps: -5.11498e+06%.
- Position error reduction versus Every 5 steps: -562786%.
- Orientation error reduction versus Every 5 steps: -471855%.
- Position error reduction versus Every 10 steps: -161003%.
- Orientation error reduction versus Every 10 steps: -135101%.
- Position error reduction versus Every 25 steps: -28226.3%.
- Orientation error reduction versus Every 25 steps: -23728.2%.
- Position error reduction versus Every 50 steps: -7328.5%.
- Orientation error reduction versus Every 50 steps: -6268.65%.
- Position error reduction versus Every 100 steps: -1859.71%.
- Orientation error reduction versus Every 100 steps: -1626.15%.
- Position error reduction versus Every 200 steps: -365.037%.
- Orientation error reduction versus Every 200 steps: -358.443%.

#### Seed 0

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 13.3145 s.
- Optimizer updates in this refresh run: 0.
- Test mean position MAE: 0.0527806 mm.
- Test mean orientation MAE: 9.82953e-05 deg.
- Benchmark mean position MAE: 0.647227 mm.
- Benchmark mean orientation MAE: 0.000395195 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<Experiment E - Refresh Frequency/every_500_steps/seed_0/Experiment E - Refresh Frequency Data.md>).

#### Seed 1

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 13.0851 s.
- Optimizer updates in this refresh run: 0.
- Test mean position MAE: 0.064755 mm.
- Test mean orientation MAE: 0.000121593 deg.
- Benchmark mean position MAE: 0.531153 mm.
- Benchmark mean orientation MAE: 0.000382245 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<Experiment E - Refresh Frequency/every_500_steps/seed_1/Experiment E - Refresh Frequency Data.md>).

#### Seed 2

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 12.4214 s.
- Optimizer updates in this refresh run: 0.
- Test mean position MAE: 0.061378 mm.
- Test mean orientation MAE: 0.000112313 deg.
- Benchmark mean position MAE: 0.589366 mm.
- Benchmark mean orientation MAE: 0.000458018 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<Experiment E - Refresh Frequency/every_500_steps/seed_2/Experiment E - Refresh Frequency Data.md>).

## Theory, controls, and interpretation

The NN learns a true-state one-step physics residual. Recursive evaluation then feeds each predicted state back into physics and feature construction, so small local errors can accumulate. Additional trajectories change sample quantity; additional families change state/control coverage; more optimizer updates change fitting opportunity; network size changes function capacity. A lower one-step residual loss does not guarantee lower recursive path error. Checkpoint selection and standardization use training/validation only; standardizers are fitted separately for each selected training subset and reused across seeds of that condition.

Standardized residual losses from different training subsets use different target scales and should not be compared as if they shared a physical unit. This matters especially for restricted-family training, where some residual components vary very little in training but vary in the common validation flights. The physical position/orientation MAEs and simulator-normalized errors provide the shared comparison scale.

For the variety experiment, the restricted set balances circles and figure-eights while the broad set balances all main families. Both keep the same total training duration. Their training paths differ by design; validation/test paths do not. The waypoint benchmark remains unseen in every condition. Family-specific metrics are retained with each trajectory so narrow-coverage effects can be inspected.

Width and depth comparisons use the common standard architecture as a reference. Inputs and outputs are additional layers. Parameter counts and measured training times accompany each run. Training-time comparisons are CPU measurements under the recorded thread setting.

Refresh experiments use full-state truth replacement at selected prediction timestamps, after saving the forecast. The primary error is measured before replacement; post-replacement metrics, event snapshots, and drift segments remain saved separately. Every-step refresh approaches one-step evaluation rather than zero forecast error. Final-timestamp resets count as observations but cannot improve an already-computed final forecast. All seeds use the same schedules, and their checkpoint weights and normalizers remain fixed.

No automatic fidelity threshold or winning interval is imposed. The raw errors, seed variability, physics comparisons, and pairwise percentages support manual interpretation.

## Reproduction and artifacts

```powershell
.\.venv\Scripts\python.exe scripts/model_drone_residual/run_drone_experiments.py
python scripts/model_drone_residual/run_drone_experiments.py --resume "runs/Drone/phase_7"
```

Use `--experiments A B C D E` and `--seeds 0 1 2` to select comparisons; defaults run the full design. New invocations preserve earlier output under phase_7/repeat_N. Resuming checks source/input hashes and reuses completed runs. Canonical training artifacts are stored once under their owning experiment; shared baselines are linked from all other experiment reports. All seed reports identify the controlled factor in their filenames. Combined prediction archives load in the existing MuJoCo comparison viewer.

`suite_manifest.json` records the protocol and exact training subsets. `run_metadata.json` records progress, runtimes, source/input hashes, and completion. `suite_results.json` retains every seed summary. `comparison_metrics.csv` contains raw and simulator-normalized errors. `pairwise_comparisons.csv` contains every directed condition comparison, including negative reductions. `experiment_summary.json` contains means and population standard deviations across seeds. Each experiment has its own report, summary, pairwise CSV, and comparison plots. Per-seed artifacts preserve best/final checkpoints, normalization, loss curves, full prediction/control histories, per-flight metrics, and path/error plots.

Drone_Plan.md, README.md, Runs Masterlist.md, and prior phase outputs are unchanged. No commit was created.

## Completed execution and verification

- Unique training runs completed: 36.
- Fixed-checkpoint refresh runs completed: 27.
- Requested optimizer updates across unique training runs: 390,000.
- Actual optimizer updates across unique training runs: 390,774.
- Sum of measured training times: 530.814 s.
- Complete suite runtime: 919.193 s.
- Drone subsystem regression tests passed: 201.
- Drone regression test runtime: 28.85 s.
- Additional focused percentage/report test passed: 1.
- Prediction archives independently checked: 198.
- Per-seed comparison summary rows: 468.
- Directed pairwise percentage comparison rows: 5,248.
- Predictor-specific refresh event rows: 165,240.
- Drift segment rows: 165,360.
- PNG figures produced: 216.

All final checkpoints end on complete epochs. Each selected best checkpoint is the lowest validation residual MSE in that run?s recorded history; it may select an earlier update. Training-only normalizers contain exactly the selected training trajectory IDs. All optimizer step counters, epoch totals, sample counts, parameter counts, and update schedules agree with the saved configuration.

Independently recomputed all saved trajectory errors, simulator-relative percentages, equal-flight means, and trajectory standard deviations from the prediction archives. Recomputed every directed pairwise percentage from its stored raw MAEs. Checked all report links, loaded every combined archive through the existing comparison playback loader, and verified all full-state refresh snapshots and replacements.

No-refresh predictions reproduce the corresponding baseline training evaluation exactly. Every-step refresh retains nonzero one-step forecast error while post-replacement states match truth. Small differences from the separately batched one-step archives arise from float32 NN batch rounding; they do not indicate drift.

Visually inspected a representative restricted-family waypoint comparison, the network-size summary, and the refresh-count summary. The requested large 3D path plus position/orientation error layout is retained for flight plots; comparison figures distinguish mean results from individual seeds.

The physics, learning, and evaluation sources and input archives retain their recorded hashes. Report generators received wording, formatting, and link improvements after computation started. Their execution hashes and current report hashes are recorded separately; checkpoint provenance is unchanged. The unused legacy training-report emitter?s documentation-only change is explicitly recorded in the resume-compatibility metadata.

Drone_Plan.md, README.md, Runs Masterlist.md, and the original phase-5 checkpoint match their pre-phase hashes. No pendulum or unicycle tests were run. No commit was created.

Machine-readable checks: [artifact_verification.json](<artifact_verification.json>).

Drone-only regression command:

```powershell
$droneTestFiles = @(rg --files tests -g "test_drone*.py")
& .\.venv\Scripts\python.exe -m pytest @droneTestFiles -q --basetemp .pytest_cache/drone_phase7_regression --tb=short
```

Example playback of the standard-network baseline:

```powershell
python scripts/drone/playback_flight.py "runs/Drone/phase_7/Experiment A - Trajectory Quantity/broad_80/seed_0/predictions/test_recursive.npz" --trajectory-id test_000000 --compare both --paused
```

Example playback with periodic truth refreshes:

```powershell
python scripts/drone/playback_flight.py "runs/Drone/phase_7/Experiment E - Refresh Frequency/every_100_steps/seed_0/predictions/test_recursive.npz" --trajectory-id test_000000 --compare both --paused
```

## Implementation files

- `src/model_drone_residual/experiments.py`: controlled conditions, nested training subsets, fixed family selection, cached sample selection, and percentage definitions.
- `src/model_drone_residual/experiment_evaluation.py`: shared held-out physics references, independent hybrid forecasts, simulator-normalized metrics, prediction archives, and refresh diagnostics.
- `src/model_drone_residual/experiment_reporting.py`: experiment/run/seed headings, one result per metric bullet, seed variability, all directed percentage comparisons, and linked reports.
- `src/model_drone_residual/experiment_plotting.py`: condition comparisons with individual seed points and refresh-count figures.
- `scripts/model_drone_residual/run_drone_experiments.py`: complete experiment runner, completed-run reuse, progress metadata, protected-file checks, and source/checkpoint provenance.
- `src/model_drone_residual/training.py`: complete-epoch budgets and validated reuse of unstandardized residual samples.
- `scripts/model_drone_residual/train_drone_residual.py`: standalone training now reports requested and rounded actual budgets.
- `src/model_drone_residual/reporting.py`: future standalone training reports explain complete-epoch rounding consistently.
- `tests/test_drone_experiments.py`: controlled-design, cache, percentage, metric, refresh, and report checks.
- `tests/test_drone_rollout.py`: complete-epoch training expectations replace partial-final-epoch expectations.

# Experiment: Neural Network Size

Width comparisons hold hidden depth fixed. Depth comparisons hold hidden width fixed. The shared standard network supplies the reference.

All displayed run summaries use fully recursive forecasts. Positive comparison percentages mean less error; negative percentages mean more error. The comparison denominator is the named reference run. Seed means weight each training seed equally; each seed first weights each test flight equally.

[All pairwise percentages](<pairwise_comparisons.csv>).

[Comparison plot](<plots/comparison_mae.png>).

### Run: 2 hidden layers x 32 neurons

Artifacts: [2 hidden layers x 32 neurons](<layers_2_width_32/seed_0/>).

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

- Mean position MAE against MuJoCo: **0.000722308 m**.
- Mean orientation MAE against MuJoCo: **0.000526848 deg**.
- Orientation MAE in radians: 9.19523e-06 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.274422%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00871825%.
- Position error reduction versus physics-only: 94.9581%.
- Orientation error reduction versus physics-only: 94.6262%.
- Physics-only mean position MAE: **0.014326 m**.
- Physics-only mean orientation MAE: **0.00980406 deg**.
- Seed standard deviation of mean position MAE: 7.81265e-05 m.
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

- Mean position MAE against MuJoCo: **0.00210814 m**.
- Mean orientation MAE against MuJoCo: **0.00151822 deg**.
- Orientation MAE in radians: 2.6498e-05 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.27459%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00994615%.
- Position error reduction versus physics-only: 82.6554%.
- Orientation error reduction versus physics-only: 79.2692%.
- Physics-only mean position MAE: **0.0121545 m**.
- Physics-only mean orientation MAE: **0.00732349 deg**.
- Seed standard deviation of mean position MAE: 0.000432319 m.
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
- Test mean position MAE: 0.000634241 m.
- Test mean orientation MAE: 0.000517315 deg.
- Benchmark mean position MAE: 0.00253579 m.
- Benchmark mean orientation MAE: 0.00157692 deg.

Detailed seed report: [Experiment D - Neural Network Size Data.md](<layers_2_width_32/seed_0/Experiment D - Neural Network Size Data.md>).

#### Seed 1

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 1,932.
- Source training time: 10.9767 s.
- Test mean position MAE: 0.000824123 m.
- Test mean orientation MAE: 0.000529141 deg.
- Benchmark mean position MAE: 0.00227272 m.
- Benchmark mean orientation MAE: 0.00134491 deg.

Detailed seed report: [Experiment D - Neural Network Size Data.md](<layers_2_width_32/seed_1/Experiment D - Neural Network Size Data.md>).

#### Seed 2

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 1,932.
- Source training time: 9.6931 s.
- Test mean position MAE: 0.000708559 m.
- Test mean orientation MAE: 0.000534088 deg.
- Benchmark mean position MAE: 0.00151592 m.
- Benchmark mean orientation MAE: 0.00163284 deg.

Detailed seed report: [Experiment D - Neural Network Size Data.md](<layers_2_width_32/seed_2/Experiment D - Neural Network Size Data.md>).

### Run: 2 hidden layers x 64 neurons

Artifacts: [2 hidden layers x 64 neurons](<../Experiment A - Trajectory Quantity/broad_80/seed_0/>).

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

- Position error reduction versus 2 hidden layers x 32 neurons: 41.8592%.
- Orientation error reduction versus 2 hidden layers x 32 neurons: 34.2339%.
- Position error reduction versus 2 hidden layers x 128 neurons: -17.5651%.
- Orientation error reduction versus 2 hidden layers x 128 neurons: -7.82753%.
- Position error reduction versus 1 hidden layers x 64 neurons: 40.5701%.
- Orientation error reduction versus 1 hidden layers x 64 neurons: 39.5666%.
- Position error reduction versus 4 hidden layers x 64 neurons: 9.71983%.
- Orientation error reduction versus 4 hidden layers x 64 neurons: 10.1921%.

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

### Run: 2 hidden layers x 128 neurons

Artifacts: [2 hidden layers x 128 neurons](<layers_2_width_128/seed_0/>).

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

- Mean position MAE against MuJoCo: **0.000357211 m**.
- Mean orientation MAE against MuJoCo: **0.000321335 deg**.
- Orientation MAE in radians: 5.60835e-06 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.16342%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00658619%.
- Position error reduction versus physics-only: 97.5066%.
- Orientation error reduction versus physics-only: 96.7224%.
- Physics-only mean position MAE: **0.014326 m**.
- Physics-only mean orientation MAE: **0.00980406 deg**.
- Seed standard deviation of mean position MAE: 2.16703e-05 m.
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

- Mean position MAE against MuJoCo: **0.0010192 m**.
- Mean orientation MAE against MuJoCo: **0.000876864 deg**.
- Orientation MAE in radians: 1.53042e-05 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.129238%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00561883%.
- Position error reduction versus physics-only: 91.6146%.
- Orientation error reduction versus physics-only: 88.0267%.
- Physics-only mean position MAE: **0.0121545 m**.
- Physics-only mean orientation MAE: **0.00732349 deg**.
- Seed standard deviation of mean position MAE: 9.36151e-05 m.
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
- Test mean position MAE: 0.000375745 m.
- Test mean orientation MAE: 0.000314276 deg.
- Benchmark mean position MAE: 0.000982744 m.
- Benchmark mean orientation MAE: 0.000985207 deg.

Detailed seed report: [Experiment D - Neural Network Size Data.md](<layers_2_width_128/seed_0/Experiment D - Neural Network Size Data.md>).

#### Seed 1

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 19,980.
- Source training time: 21.9560 s.
- Test mean position MAE: 0.000369082 m.
- Test mean orientation MAE: 0.000330144 deg.
- Benchmark mean position MAE: 0.000927212 m.
- Benchmark mean orientation MAE: 0.000907023 deg.

Detailed seed report: [Experiment D - Neural Network Size Data.md](<layers_2_width_128/seed_1/Experiment D - Neural Network Size Data.md>).

#### Seed 2

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 19,980.
- Source training time: 20.9513 s.
- Test mean position MAE: 0.000326807 m.
- Test mean orientation MAE: 0.000319585 deg.
- Benchmark mean position MAE: 0.00114765 m.
- Benchmark mean orientation MAE: 0.000738362 deg.

Detailed seed report: [Experiment D - Neural Network Size Data.md](<layers_2_width_128/seed_2/Experiment D - Neural Network Size Data.md>).

### Run: 1 hidden layers x 64 neurons

Artifacts: [1 hidden layers x 64 neurons](<layers_1_width_64/seed_0/>).

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

- Mean position MAE against MuJoCo: **0.000706641 m**.
- Mean orientation MAE against MuJoCo: **0.000573338 deg**.
- Orientation MAE in radians: 1.00066e-05 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.296485%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.0106021%.
- Position error reduction versus physics-only: 95.0674%.
- Orientation error reduction versus physics-only: 94.152%.
- Physics-only mean position MAE: **0.014326 m**.
- Physics-only mean orientation MAE: **0.00980406 deg**.
- Seed standard deviation of mean position MAE: 3.60377e-05 m.
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

- Mean position MAE against MuJoCo: **0.00221638 m**.
- Mean orientation MAE against MuJoCo: **0.00149046 deg**.
- Orientation MAE in radians: 2.60134e-05 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.284854%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00965391%.
- Position error reduction versus physics-only: 81.7649%.
- Orientation error reduction versus physics-only: 79.6483%.
- Physics-only mean position MAE: **0.0121545 m**.
- Physics-only mean orientation MAE: **0.00732349 deg**.
- Seed standard deviation of mean position MAE: 0.000106286 m.
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
- Test mean position MAE: 0.000675094 m.
- Test mean orientation MAE: 0.000496026 deg.
- Benchmark mean position MAE: 0.00207474 m.
- Benchmark mean orientation MAE: 0.00117758 deg.

Detailed seed report: [Experiment D - Neural Network Size Data.md](<layers_1_width_64/seed_0/Experiment D - Neural Network Size Data.md>).

#### Seed 1

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 1,740.
- Source training time: 9.0678 s.
- Test mean position MAE: 0.00075708 m.
- Test mean orientation MAE: 0.000632599 deg.
- Benchmark mean position MAE: 0.00224362 m.
- Benchmark mean orientation MAE: 0.00197721 deg.

Detailed seed report: [Experiment D - Neural Network Size Data.md](<layers_1_width_64/seed_1/Experiment D - Neural Network Size Data.md>).

#### Seed 2

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 1,740.
- Source training time: 8.3505 s.
- Test mean position MAE: 0.000687749 m.
- Test mean orientation MAE: 0.000591388 deg.
- Benchmark mean position MAE: 0.00233078 m.
- Benchmark mean orientation MAE: 0.00131659 deg.

Detailed seed report: [Experiment D - Neural Network Size Data.md](<layers_1_width_64/seed_2/Experiment D - Neural Network Size Data.md>).

### Run: 4 hidden layers x 64 neurons

Artifacts: [4 hidden layers x 64 neurons](<layers_4_width_64/seed_0/>).

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

- Mean position MAE against MuJoCo: **0.000465169 m**.
- Mean orientation MAE against MuJoCo: **0.00038581 deg**.
- Orientation MAE in radians: 6.73365e-06 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.159986%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00626876%.
- Position error reduction versus physics-only: 96.753%.
- Orientation error reduction versus physics-only: 96.0648%.
- Physics-only mean position MAE: **0.014326 m**.
- Physics-only mean orientation MAE: **0.00980406 deg**.
- Seed standard deviation of mean position MAE: 3.37883e-05 m.
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

- Mean position MAE against MuJoCo: **0.00167296 m**.
- Mean orientation MAE against MuJoCo: **0.00119689 deg**.
- Orientation MAE in radians: 2.08897e-05 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.205524%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00773744%.
- Position error reduction versus physics-only: 86.2359%.
- Orientation error reduction versus physics-only: 83.6568%.
- Physics-only mean position MAE: **0.0121545 m**.
- Physics-only mean orientation MAE: **0.00732349 deg**.
- Seed standard deviation of mean position MAE: 0.000130958 m.
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
- Test mean position MAE: 0.000497743 m.
- Test mean orientation MAE: 0.000443254 deg.
- Benchmark mean position MAE: 0.00174188 m.
- Benchmark mean orientation MAE: 0.00115097 deg.

Detailed seed report: [Experiment D - Neural Network Size Data.md](<layers_4_width_64/seed_0/Experiment D - Neural Network Size Data.md>).

#### Seed 1

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 14,220.
- Source training time: 21.3525 s.
- Test mean position MAE: 0.000418606 m.
- Test mean orientation MAE: 0.000316466 deg.
- Benchmark mean position MAE: 0.00148963 m.
- Benchmark mean orientation MAE: 0.00135688 deg.

Detailed seed report: [Experiment D - Neural Network Size Data.md](<layers_4_width_64/seed_1/Experiment D - Neural Network Size Data.md>).

#### Seed 2

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 14,220.
- Source training time: 21.7193 s.
- Test mean position MAE: 0.000479159 m.
- Test mean orientation MAE: 0.00039771 deg.
- Benchmark mean position MAE: 0.00178737 m.
- Benchmark mean orientation MAE: 0.00108282 deg.

Detailed seed report: [Experiment D - Neural Network Size Data.md](<layers_4_width_64/seed_2/Experiment D - Neural Network Size Data.md>).


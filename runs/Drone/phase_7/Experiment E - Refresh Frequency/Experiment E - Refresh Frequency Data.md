# Experiment: Refresh Frequency

Each seed uses its full-data standard-network checkpoint for every schedule. No retraining occurs between schedules. Primary metrics score forecasts before replacement.

All displayed run summaries use fully recursive forecasts. Positive comparison percentages mean less error; negative percentages mean more error. The comparison denominator is the named reference run. Seed means weight each training seed equally; each seed first weights each test flight equally.

[All pairwise percentages](<pairwise_comparisons.csv>).

[Comparison plot](<plots/comparison_mae.png>).

### Run: No refresh

Artifacts: [No refresh](<no_refresh/seed_0/>).

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
- Test mean position MAE: 0.000401772 m.
- Test mean orientation MAE: 0.000290801 deg.
- Benchmark mean position MAE: 0.00119401 m.
- Benchmark mean orientation MAE: 0.000683165 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<no_refresh/seed_0/Experiment E - Refresh Frequency Data.md>).

#### Seed 1

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 13.0851 s.
- Optimizer updates in this refresh run: 0.
- Test mean position MAE: 0.00044946 m.
- Test mean orientation MAE: 0.00039414 deg.
- Benchmark mean position MAE: 0.000988661 m.
- Benchmark mean orientation MAE: 0.00090311 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<no_refresh/seed_1/Experiment E - Refresh Frequency Data.md>).

#### Seed 2

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 12.4214 s.
- Optimizer updates in this refresh run: 0.
- Test mean position MAE: 0.000408635 m.
- Test mean orientation MAE: 0.000354522 deg.
- Benchmark mean position MAE: 0.00166432 m.
- Benchmark mean orientation MAE: 0.00130332 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<no_refresh/seed_2/Experiment E - Refresh Frequency Data.md>).

### Run: Every 1 steps

Artifacts: [Every 1 steps](<every_1_steps/seed_0/>).

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

- Mean position MAE against MuJoCo: **9.04287e-10 m**.
- Mean orientation MAE against MuJoCo: **1.40985e-09 deg**.
- Orientation MAE in radians: 2.46065e-11 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 3.27556e-07%.
- Orientation MAE as a percentage of MuJoCo angular travel: 2.35069e-08%.
- Position error reduction versus physics-only: 97.8449%.
- Orientation error reduction versus physics-only: 98.0222%.
- Physics-only mean position MAE: **4.19604e-08 m**.
- Physics-only mean orientation MAE: **7.12851e-08 deg**.
- Seed standard deviation of mean position MAE: 2.76679e-11 m.
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

- Mean position MAE against MuJoCo: **9.55622e-09 m**.
- Mean orientation MAE against MuJoCo: **8.05109e-09 deg**.
- Orientation MAE in radians: 1.40518e-10 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 1.13353e-06%.
- Orientation MAE as a percentage of MuJoCo angular travel: 5.1059e-08%.
- Position error reduction versus physics-only: 77.7614%.
- Orientation error reduction versus physics-only: 91.0024%.
- Physics-only mean position MAE: **4.29713e-08 m**.
- Physics-only mean orientation MAE: **8.94808e-08 deg**.
- Seed standard deviation of mean position MAE: 1.19555e-09 m.
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
- Test mean position MAE: 8.90396e-10 m.
- Test mean orientation MAE: 1.3442e-09 deg.
- Benchmark mean position MAE: 9.15103e-09 m.
- Benchmark mean orientation MAE: 7.14534e-09 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<every_1_steps/seed_0/Experiment E - Refresh Frequency Data.md>).

#### Seed 1

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 13.0851 s.
- Optimizer updates in this refresh run: 0.
- Test mean position MAE: 8.79553e-10 m.
- Test mean orientation MAE: 1.4261e-09 deg.
- Benchmark mean position MAE: 8.33724e-09 m.
- Benchmark mean orientation MAE: 7.46099e-09 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<every_1_steps/seed_1/Experiment E - Refresh Frequency Data.md>).

#### Seed 2

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 12.4214 s.
- Optimizer updates in this refresh run: 0.
- Test mean position MAE: 9.42911e-10 m.
- Test mean orientation MAE: 1.45925e-09 deg.
- Benchmark mean position MAE: 1.11804e-08 m.
- Benchmark mean orientation MAE: 9.54695e-09 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<every_1_steps/seed_2/Experiment E - Refresh Frequency Data.md>).

### Run: Every 5 steps

Artifacts: [Every 5 steps](<every_5_steps/seed_0/>).

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

- Mean position MAE against MuJoCo: **9.81876e-09 m**.
- Mean orientation MAE against MuJoCo: **1.53887e-08 deg**.
- Orientation MAE in radians: 2.68584e-10 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 3.55856e-06%.
- Orientation MAE as a percentage of MuJoCo angular travel: 2.54633e-07%.
- Position error reduction versus physics-only: 97.8728%.
- Orientation error reduction versus physics-only: 98.0379%.
- Physics-only mean position MAE: **4.61582e-07 m**.
- Physics-only mean orientation MAE: **7.843e-07 deg**.
- Seed standard deviation of mean position MAE: 4.26575e-10 m.
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

- Mean position MAE against MuJoCo: **1.04683e-07 m**.
- Mean orientation MAE against MuJoCo: **8.72583e-08 deg**.
- Orientation MAE in radians: 1.52294e-09 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 1.24293e-05%.
- Orientation MAE as a percentage of MuJoCo angular travel: 5.5239e-07%.
- Position error reduction versus physics-only: 77.8536%.
- Orientation error reduction versus physics-only: 91.1213%.
- Physics-only mean position MAE: **4.72688e-07 m**.
- Physics-only mean orientation MAE: **9.82776e-07 deg**.
- Seed standard deviation of mean position MAE: 1.23722e-08 m.
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
- Test mean position MAE: 9.64966e-09 m.
- Test mean orientation MAE: 1.46448e-08 deg.
- Benchmark mean position MAE: 1.01895e-07 m.
- Benchmark mean orientation MAE: 7.85528e-08 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<every_5_steps/seed_0/Experiment E - Refresh Frequency Data.md>).

#### Seed 1

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 13.0851 s.
- Optimizer updates in this refresh run: 0.
- Test mean position MAE: 9.4018e-09 m.
- Test mean orientation MAE: 1.53683e-08 deg.
- Benchmark mean position MAE: 9.11184e-08 m.
- Benchmark mean orientation MAE: 8.10083e-08 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<every_5_steps/seed_1/Experiment E - Refresh Frequency Data.md>).

#### Seed 2

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 12.4214 s.
- Optimizer updates in this refresh run: 0.
- Test mean position MAE: 1.04048e-08 m.
- Test mean orientation MAE: 1.6153e-08 deg.
- Benchmark mean position MAE: 1.21037e-07 m.
- Benchmark mean orientation MAE: 1.02214e-07 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<every_5_steps/seed_2/Experiment E - Refresh Frequency Data.md>).

### Run: Every 10 steps

Artifacts: [Every 10 steps](<every_10_steps/seed_0/>).

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

- Mean position MAE against MuJoCo: **3.44281e-08 m**.
- Mean orientation MAE against MuJoCo: **5.41696e-08 deg**.
- Orientation MAE in radians: 9.45437e-10 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 1.26682e-05%.
- Orientation MAE as a percentage of MuJoCo angular travel: 8.98819e-07%.
- Position error reduction versus physics-only: 97.8688%.
- Orientation error reduction versus physics-only: 98.0264%.
- Physics-only mean position MAE: **1.61545e-06 m**.
- Physics-only mean orientation MAE: **2.74474e-06 deg**.
- Seed standard deviation of mean position MAE: 1.63552e-09 m.
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

- Mean position MAE against MuJoCo: **3.65758e-07 m**.
- Mean orientation MAE against MuJoCo: **3.04597e-07 deg**.
- Orientation MAE in radians: 5.31622e-09 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 4.34441e-05%.
- Orientation MAE as a percentage of MuJoCo angular travel: 1.92804e-06%.
- Position error reduction versus physics-only: 77.8906%.
- Orientation error reduction versus physics-only: 91.121%.
- Physics-only mean position MAE: **1.65431e-06 m**.
- Physics-only mean orientation MAE: **3.43052e-06 deg**.
- Seed standard deviation of mean position MAE: 4.29749e-08 m.
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
- Test mean position MAE: 3.3889e-08 m.
- Test mean orientation MAE: 5.15467e-08 deg.
- Benchmark mean position MAE: 3.57018e-07 m.
- Benchmark mean orientation MAE: 2.74739e-07 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<every_10_steps/seed_0/Experiment E - Refresh Frequency Data.md>).

#### Seed 1

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 13.0851 s.
- Optimizer updates in this refresh run: 0.
- Test mean position MAE: 3.27497e-08 m.
- Test mean orientation MAE: 5.41701e-08 deg.
- Benchmark mean position MAE: 3.18042e-07 m.
- Benchmark mean orientation MAE: 2.829e-07 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<every_10_steps/seed_1/Experiment E - Refresh Frequency Data.md>).

#### Seed 2

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 12.4214 s.
- Optimizer updates in this refresh run: 0.
- Test mean position MAE: 3.66455e-08 m.
- Test mean orientation MAE: 5.67919e-08 deg.
- Benchmark mean position MAE: 4.22214e-07 m.
- Benchmark mean orientation MAE: 3.56152e-07 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<every_10_steps/seed_2/Experiment E - Refresh Frequency Data.md>).

### Run: Every 25 steps

Artifacts: [Every 25 steps](<every_25_steps/seed_0/>).

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

- Mean position MAE against MuJoCo: **1.97249e-07 m**.
- Mean orientation MAE against MuJoCo: **3.11966e-07 deg**.
- Orientation MAE in radians: 5.44484e-09 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 7.29979e-05%.
- Orientation MAE as a percentage of MuJoCo angular travel: 5.16587e-06%.
- Position error reduction versus physics-only: 97.8709%.
- Orientation error reduction versus physics-only: 98.0106%.
- Physics-only mean position MAE: **9.26426e-06 m**.
- Physics-only mean orientation MAE: **1.56815e-05 deg**.
- Seed standard deviation of mean position MAE: 1.0426e-08 m.
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

- Mean position MAE against MuJoCo: **2.08021e-06 m**.
- Mean orientation MAE against MuJoCo: **1.72829e-06 deg**.
- Orientation MAE in radians: 3.01643e-08 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.00024715%.
- Orientation MAE as a percentage of MuJoCo angular travel: 1.09386e-05%.
- Position error reduction versus physics-only: 78.0768%.
- Orientation error reduction versus physics-only: 91.128%.
- Physics-only mean position MAE: **9.48864e-06 m**.
- Physics-only mean orientation MAE: **1.94801e-05 deg**.
- Seed standard deviation of mean position MAE: 2.44218e-07 m.
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
- Test mean position MAE: 1.94008e-07 m.
- Test mean orientation MAE: 2.92166e-07 deg.
- Benchmark mean position MAE: 2.0357e-06 m.
- Benchmark mean orientation MAE: 1.55261e-06 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<every_25_steps/seed_0/Experiment E - Refresh Frequency Data.md>).

#### Seed 1

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 13.0851 s.
- Optimizer updates in this refresh run: 0.
- Test mean position MAE: 1.86413e-07 m.
- Test mean orientation MAE: 3.11138e-07 deg.
- Benchmark mean position MAE: 1.80586e-06 m.
- Benchmark mean orientation MAE: 1.60931e-06 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<every_25_steps/seed_1/Experiment E - Refresh Frequency Data.md>).

#### Seed 2

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 12.4214 s.
- Optimizer updates in this refresh run: 0.
- Test mean position MAE: 2.11327e-07 m.
- Test mean orientation MAE: 3.32595e-07 deg.
- Benchmark mean position MAE: 2.39908e-06 m.
- Benchmark mean orientation MAE: 2.02294e-06 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<every_25_steps/seed_2/Experiment E - Refresh Frequency Data.md>).

### Run: Every 50 steps

Artifacts: [Every 50 steps](<every_50_steps/seed_0/>).

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

- Mean position MAE against MuJoCo: **7.32923e-07 m**.
- Mean orientation MAE against MuJoCo: **1.12426e-06 deg**.
- Orientation MAE in radians: 1.9622e-08 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.000280204%.
- Orientation MAE as a percentage of MuJoCo angular travel: 1.95079e-05%.
- Position error reduction versus physics-only: 97.9531%.
- Orientation error reduction versus physics-only: 98.1536%.
- Physics-only mean position MAE: **3.5806e-05 m**.
- Physics-only mean orientation MAE: **6.08885e-05 deg**.
- Seed standard deviation of mean position MAE: 3.33814e-08 m.
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

- Mean position MAE against MuJoCo: **7.93226e-06 m**.
- Mean orientation MAE against MuJoCo: **6.46635e-06 deg**.
- Orientation MAE in radians: 1.12859e-07 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.000942308%.
- Orientation MAE as a percentage of MuJoCo angular travel: 4.10047e-05%.
- Position error reduction versus physics-only: 78.4227%.
- Orientation error reduction versus physics-only: 90.9954%.
- Physics-only mean position MAE: **3.67621e-05 m**.
- Physics-only mean orientation MAE: **7.18119e-05 deg**.
- Seed standard deviation of mean position MAE: 9.50897e-07 m.
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
- Test mean position MAE: 7.35452e-07 m.
- Test mean orientation MAE: 1.03541e-06 deg.
- Benchmark mean position MAE: 7.76908e-06 m.
- Benchmark mean orientation MAE: 5.79697e-06 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<every_50_steps/seed_0/Experiment E - Refresh Frequency Data.md>).

#### Seed 1

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 13.0851 s.
- Optimizer updates in this refresh run: 0.
- Test mean position MAE: 6.90834e-07 m.
- Test mean orientation MAE: 1.1192e-06 deg.
- Benchmark mean position MAE: 6.85785e-06 m.
- Benchmark mean orientation MAE: 6.06109e-06 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<every_50_steps/seed_1/Experiment E - Refresh Frequency Data.md>).

#### Seed 2

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 12.4214 s.
- Optimizer updates in this refresh run: 0.
- Test mean position MAE: 7.72484e-07 m.
- Test mean orientation MAE: 1.21816e-06 deg.
- Benchmark mean position MAE: 9.16985e-06 m.
- Benchmark mean orientation MAE: 7.54099e-06 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<every_50_steps/seed_2/Experiment E - Refresh Frequency Data.md>).

### Run: Every 100 steps

Artifacts: [Every 100 steps](<every_100_steps/seed_0/>).

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

- Mean position MAE against MuJoCo: **2.77821e-06 m**.
- Mean orientation MAE against MuJoCo: **4.80066e-06 deg**.
- Orientation MAE in radians: 8.37873e-08 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.00104599%.
- Orientation MAE as a percentage of MuJoCo angular travel: 8.33547e-05%.
- Position error reduction versus physics-only: 97.9983%.
- Orientation error reduction versus physics-only: 98.1327%.
- Physics-only mean position MAE: **0.000138796 m**.
- Physics-only mean orientation MAE: **0.000257092 deg**.
- Seed standard deviation of mean position MAE: 9.59523e-08 m.
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

- Mean position MAE against MuJoCo: **3.00682e-05 m**.
- Mean orientation MAE against MuJoCo: **2.38577e-05 deg**.
- Orientation MAE in radians: 4.16396e-07 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.00355096%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.000150994%.
- Position error reduction versus physics-only: 78.943%.
- Orientation error reduction versus physics-only: 90.9588%.
- Physics-only mean position MAE: **0.000142794 m**.
- Physics-only mean orientation MAE: **0.000263877 deg**.
- Seed standard deviation of mean position MAE: 4.08064e-06 m.
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
- Test mean position MAE: 2.72404e-06 m.
- Test mean orientation MAE: 4.35691e-06 deg.
- Benchmark mean position MAE: 3.00359e-05 m.
- Benchmark mean orientation MAE: 2.12913e-05 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<every_100_steps/seed_0/Experiment E - Refresh Frequency Data.md>).

#### Seed 1

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 13.0851 s.
- Optimizer updates in this refresh run: 0.
- Test mean position MAE: 2.69755e-06 m.
- Test mean orientation MAE: 5.02417e-06 deg.
- Benchmark mean position MAE: 2.50867e-05 m.
- Benchmark mean orientation MAE: 2.23081e-05 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<every_100_steps/seed_1/Experiment E - Refresh Frequency Data.md>).

#### Seed 2

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 12.4214 s.
- Optimizer updates in this refresh run: 0.
- Test mean position MAE: 2.91304e-06 m.
- Test mean orientation MAE: 5.0209e-06 deg.
- Benchmark mean position MAE: 3.5082e-05 m.
- Benchmark mean orientation MAE: 2.79737e-05 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<every_100_steps/seed_2/Experiment E - Refresh Frequency Data.md>).

### Run: Every 200 steps

Artifacts: [Every 200 steps](<every_200_steps/seed_0/>).

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

- Mean position MAE against MuJoCo: **9.63271e-06 m**.
- Mean orientation MAE against MuJoCo: **1.85396e-05 deg**.
- Orientation MAE in radians: 3.23576e-07 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.00380793%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.000327787%.
- Position error reduction versus physics-only: 97.9886%.
- Orientation error reduction versus physics-only: 98.0597%.
- Physics-only mean position MAE: **0.000478894 m**.
- Physics-only mean orientation MAE: **0.000955521 deg**.
- Seed standard deviation of mean position MAE: 2.9372e-07 m.
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

- Mean position MAE against MuJoCo: **0.00012671 m**.
- Mean orientation MAE against MuJoCo: **8.983e-05 deg**.
- Orientation MAE in radians: 1.56783e-06 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.0146113%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00055857%.
- Position error reduction versus physics-only: 79.5107%.
- Orientation error reduction versus physics-only: 90.4173%.
- Physics-only mean position MAE: **0.000618421 m**.
- Physics-only mean orientation MAE: **0.000937417 deg**.
- Seed standard deviation of mean position MAE: 1.77039e-05 m.
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
- Test mean position MAE: 9.4704e-06 m.
- Test mean orientation MAE: 1.66891e-05 deg.
- Benchmark mean position MAE: 0.000130021 m.
- Benchmark mean orientation MAE: 8.13549e-05 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<every_200_steps/seed_0/Experiment E - Refresh Frequency Data.md>).

#### Seed 1

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 13.0851 s.
- Optimizer updates in this refresh run: 0.
- Test mean position MAE: 9.38273e-06 m.
- Test mean orientation MAE: 1.94751e-05 deg.
- Benchmark mean position MAE: 0.000103562 m.
- Benchmark mean orientation MAE: 8.66482e-05 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<every_200_steps/seed_1/Experiment E - Refresh Frequency Data.md>).

#### Seed 2

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 12.4214 s.
- Optimizer updates in this refresh run: 0.
- Test mean position MAE: 1.0045e-05 m.
- Test mean orientation MAE: 1.94544e-05 deg.
- Benchmark mean position MAE: 0.000146547 m.
- Benchmark mean orientation MAE: 0.000101487 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<every_200_steps/seed_2/Experiment E - Refresh Frequency Data.md>).

### Run: Every 500 steps

Artifacts: [Every 500 steps](<every_500_steps/seed_0/>).

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

- Mean position MAE against MuJoCo: **5.96379e-05 m**.
- Mean orientation MAE against MuJoCo: **0.000110734 deg**.
- Orientation MAE in radians: 1.93267e-06 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.023349%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00190928%.
- Position error reduction versus physics-only: 98.3462%.
- Orientation error reduction versus physics-only: 98.1986%.
- Physics-only mean position MAE: **0.00360604 m**.
- Physics-only mean orientation MAE: **0.0061472 deg**.
- Seed standard deviation of mean position MAE: 5.04099e-06 m.
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

- Mean position MAE against MuJoCo: **0.000589248 m**.
- Mean orientation MAE against MuJoCo: **0.00041182 deg**.
- Orientation MAE in radians: 7.18761e-06 rad.
- Position MAE as a percentage of MuJoCo distance traveled: 0.0686408%.
- Orientation MAE as a percentage of MuJoCo angular travel: 0.00259793%.
- Position error reduction versus physics-only: 82.9673%.
- Orientation error reduction versus physics-only: 85.4175%.
- Physics-only mean position MAE: **0.0034595 m**.
- Physics-only mean orientation MAE: **0.00282407 deg**.
- Seed standard deviation of mean position MAE: 4.73873e-05 m.
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
- Test mean position MAE: 5.27806e-05 m.
- Test mean orientation MAE: 9.82953e-05 deg.
- Benchmark mean position MAE: 0.000647227 m.
- Benchmark mean orientation MAE: 0.000395195 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<every_500_steps/seed_0/Experiment E - Refresh Frequency Data.md>).

#### Seed 1

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 13.0851 s.
- Optimizer updates in this refresh run: 0.
- Test mean position MAE: 6.4755e-05 m.
- Test mean orientation MAE: 0.000121593 deg.
- Benchmark mean position MAE: 0.000531153 m.
- Benchmark mean orientation MAE: 0.000382245 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<every_500_steps/seed_1/Experiment E - Refresh Frequency Data.md>).

#### Seed 2

- Actual source-training optimizer updates: 10,016.
- Completed source-training epochs: 32.
- Trainable parameters: 5,900.
- Source training time: 12.4214 s.
- Optimizer updates in this refresh run: 0.
- Test mean position MAE: 6.1378e-05 m.
- Test mean orientation MAE: 0.000112313 deg.
- Benchmark mean position MAE: 0.000589366 m.
- Benchmark mean orientation MAE: 0.000458018 deg.

Detailed seed report: [Experiment E - Refresh Frequency Data.md](<every_500_steps/seed_2/Experiment E - Refresh Frequency Data.md>).


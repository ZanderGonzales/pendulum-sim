# Phase 6 Data: Optional Truth Refreshes

## Results and scope

The existing phase-5 checkpoint is evaluated under reproducible full-state truth-refresh schedules. No training, weight updates, new dataset generation, or checkpoint reselection occurred. Both physics-only and physics+NN predictors replay the same recorded applied controls and receive the same truth at the same selected steps.

- Checkpoint: `runs/Drone/phase_5/checkpoint_best.pt`, selected at optimizer update 9,900 in phase 5.
- Optimizer updates in this phase: **0**; checkpoint file, model weights, and standardizers verified unchanged.
- Prediction grid: 0.01 s; each flight has 1000 transitions.
- Held-out counts: {'test': 10, 'benchmark': 10}.
- Schedule cases: 9.
- Default schedule: **no refresh**. The recorded `--sweep` command explicitly requests the interval comparison when used.

**Primary errors are measured before any truth replacement at each prediction timestamp.** Secondary after-replacement metrics are saved separately. This prevents resets from making the predictor look artificially exact at refreshed samples.

## Test trajectories

All following means average the corresponding per-trajectory MAEs with equal flight weight. Orientation is the shortest absolute rotation angle. The shared initial state is excluded.

### no_refresh: 0 refreshes per trajectory

- **physics_only**, forecast before replacement: mean position MAE **0.0143260365 m**, std 0.00579547429 m; mean orientation MAE **0.000171113069 rad (0.00980405669 deg)**, std 6.29730519e-05 rad.
  Mean final forecast position error: 0.0512667036 m; mean maximum position error: 0.0512667036 m.
  After-replacement mean position/orientation MAE: 0.0143260365 m / 0.000171113069 rad; mean final after-replacement position error 0.0512667036 m.
  Mean segment endpoint growth per second: 0.00512667036 m/s / 3.21537725e-05 rad/s.
- **hybrid**, forecast before replacement: mean position MAE **0.000442591641 m**, std 0.000434539123 m; mean orientation MAE **6.42021996e-06 rad (0.000367851507 deg)**, std 5.98451333e-06 rad.
  Mean final forecast position error: 0.00171486678 m; mean maximum position error: 0.00171486678 m.
  After-replacement mean position/orientation MAE: 0.000442591641 m / 6.42021996e-06 rad; mean final after-replacement position error 0.00171486678 m.
  Mean segment endpoint growth per second: 0.000171486678 m/s / 1.57243047e-06 rad/s.

### every_1_steps: 1000 refreshes per trajectory

- **physics_only**, forecast before replacement: mean position MAE **4.19603804e-08 m**, std 2.8284042e-08 m; mean orientation MAE **1.24415934e-09 rad (7.12850792e-08 deg)**, std 1.0248782e-09 rad.
  Mean final forecast position error: 1.76875091e-10 m; mean maximum position error: 1.60043329e-07 m.
  After-replacement mean position/orientation MAE: 0 m / 0 rad; mean final after-replacement position error 0 m.
  Mean error immediately before refresh events: 4.19603804e-08 m / 1.24415934e-09 rad.
  Mean segment endpoint growth per second: 4.19603804e-06 m/s / 1.24415934e-07 rad/s.
- **hybrid**, forecast before replacement: mean position MAE **9.41133952e-10 m**, std 4.39598039e-10 m; mean orientation MAE **2.70383581e-11 rad (1.5491838e-09 deg)**, std 1.06021303e-11 rad.
  Mean final forecast position error: 1.68682967e-10 m; mean maximum position error: 9.08533821e-09 m.
  After-replacement mean position/orientation MAE: 0 m / 0 rad; mean final after-replacement position error 0 m.
  Mean error immediately before refresh events: 9.41133952e-10 m / 2.70383581e-11 rad.
  Mean segment endpoint growth per second: 9.41133952e-08 m/s / 2.70383581e-09 rad/s.

### every_5_steps: 200 refreshes per trajectory

- **physics_only**, forecast before replacement: mean position MAE **4.61582447e-07 m**, std 3.11082222e-07 m; mean orientation MAE **1.36886181e-08 rad (7.84300043e-07 deg)**, std 1.1271117e-08 rad.
  Mean final forecast position error: 4.62601169e-09 m; mean maximum position error: 3.99777776e-06 m.
  After-replacement mean position/orientation MAE: 2.51785222e-07 m / 7.46796572e-09 rad; mean final after-replacement position error 0 m.
  Mean error immediately before refresh events: 1.04898612e-06 m / 3.11032618e-08 rad.
  Mean segment endpoint growth per second: 2.09797225e-05 m/s / 6.22065236e-07 rad/s.
- **hybrid**, forecast before replacement: mean position MAE **1.04574588e-08 m**, std 4.84221044e-09 m; mean orientation MAE **2.93355113e-10 rad (1.68080099e-08 deg)**, std 1.16096269e-10 rad.
  Mean final forecast position error: 5.1903233e-09 m; mean maximum position error: 2.06558108e-07 m.
  After-replacement mean position/orientation MAE: 5.70936552e-09 m / 1.60352429e-10 rad; mean final after-replacement position error 0 m.
  Mean error immediately before refresh events: 2.37404666e-08 m / 6.6501342e-10 rad.
  Mean segment endpoint growth per second: 4.74809333e-07 m/s / 1.33002684e-08 rad/s.

### every_10_steps: 100 refreshes per trajectory

- **physics_only**, forecast before replacement: mean position MAE **1.6154514e-06 m**, std 1.08842844e-06 m; mean orientation MAE **4.79047378e-08 rad (2.7447393e-06 deg)**, std 3.94406896e-08 rad.
  Mean final forecast position error: 1.96487428e-08 m; mean maximum position error: 1.59452029e-05 m.
  After-replacement mean position/orientation MAE: 1.19594556e-06 m / 3.54686629e-08 rad; mean final after-replacement position error 0 m.
  Mean error immediately before refresh events: 4.19505841e-06 m / 1.2436075e-07 rad.
  Mean segment endpoint growth per second: 4.19505841e-05 m/s / 1.2436075e-06 rad/s.
- **hybrid**, forecast before replacement: mean position MAE **3.69146242e-08 m**, std 1.67773377e-08 m; mean orientation MAE **1.0316728e-09 rad (5.9110497e-08 deg)**, std 4.10893417e-10 rad.
  Mean final forecast position error: 2.1897734e-08 m; mean maximum position error: 6.98025763e-07 m.
  After-replacement mean position/orientation MAE: 2.73953274e-08 m / 7.6559834e-10 rad; mean final after-replacement position error 0 m.
  Mean error immediately before refresh events: 9.5192968e-08 m / 2.66074456e-09 rad.
  Mean segment endpoint growth per second: 9.5192968e-07 m/s / 2.66074456e-08 rad/s.

### every_25_steps: 40 refreshes per trajectory

- **physics_only**, forecast before replacement: mean position MAE **9.26425804e-06 m**, std 6.23514711e-06 m; mean orientation MAE **2.73693043e-07 rad (1.56814562e-05 deg)**, std 2.26051664e-07 rad.
  Mean final forecast position error: 1.53318858e-07 m; mean maximum position error: 9.82589016e-05 m.
  After-replacement mean position/orientation MAE: 8.21741651e-06 m / 2.42754798e-07 rad; mean final after-replacement position error 0 m.
  Mean error immediately before refresh events: 2.61710382e-05 m / 7.7345611e-07 rad.
  Mean segment endpoint growth per second: 0.000104684153 m/s / 3.09382444e-06 rad/s.
- **hybrid**, forecast before replacement: mean position MAE **2.11173975e-07 m**, std 9.42832458e-08 m; mean orientation MAE **5.82456453e-09 rad (3.33722965e-07 deg)**, std 2.38388381e-09 rad.
  Mean final forecast position error: 1.4705174e-07 m; mean maximum position error: 3.29360571e-06 m.
  After-replacement mean position/orientation MAE: 1.87935436e-07 m / 5.18405914e-09 rad; mean final after-replacement position error 0 m.
  Mean error immediately before refresh events: 5.80963463e-07 m / 1.60126347e-08 rad.
  Mean segment endpoint growth per second: 2.32385385e-06 m/s / 6.40505387e-08 rad/s.

### every_50_steps: 20 refreshes per trajectory

- **physics_only**, forecast before replacement: mean position MAE **3.58059987e-05 m**, std 2.40361985e-05 m; mean orientation MAE **1.06270398e-06 rad (6.0888453e-05 deg)**, std 8.68263135e-07 rad.
  Mean final forecast position error: 1.01899711e-06 m; mean maximum position error: 0.000382825146 m.
  After-replacement mean position/orientation MAE: 3.37294713e-05 m / 1.00085455e-06 rad; mean final after-replacement position error 0 m.
  Mean error immediately before refresh events: 0.000103826374 m / 3.09247178e-06 rad.
  Mean segment endpoint growth per second: 0.000207652747 m/s / 6.18494356e-06 rad/s.
- **hybrid**, forecast before replacement: mean position MAE **8.08653968e-07 m**, std 3.72542206e-07 m; mean orientation MAE **2.11035281e-08 rad (1.20914309e-06 deg)**, std 7.29637655e-09 rad.
  Mean final forecast position error: 5.91966088e-07 m; mean maximum position error: 9.27641629e-06 m.
  After-replacement mean position/orientation MAE: 7.64143322e-07 m / 1.98807862e-08 rad; mean final after-replacement position error 0 m.
  Mean error immediately before refresh events: 2.22553232e-06 m / 6.11370963e-08 rad.
  Mean segment endpoint growth per second: 4.45106465e-06 m/s / 1.22274193e-07 rad/s.

### every_100_steps: 10 refreshes per trajectory

- **physics_only**, forecast before replacement: mean position MAE **0.000138795589 m**, std 9.218951e-05 m; mean orientation MAE **4.48710107e-06 rad (0.000257091954 deg)**, std 3.44560448e-06 rad.
  Mean final forecast position error: 7.0709445e-06 m; mean maximum position error: 0.00129649111 m.
  After-replacement mean position/orientation MAE: 0.000134748353 m / 4.35990531e-06 rad; mean final after-replacement position error 0 m.
  Mean error immediately before refresh events: 0.000404723608 m / 1.27195766e-05 rad.
  Mean segment endpoint growth per second: 0.000404723608 m/s / 1.27195766e-05 rad/s.
- **hybrid**, forecast before replacement: mean position MAE **2.99553633e-06 m**, std 1.42499366e-06 m; mean orientation MAE **8.91426371e-08 rad (5.10749688e-06 deg)**, std 4.06073084e-08 rad.
  Mean final forecast position error: 1.97990596e-06 m; mean maximum position error: 2.32914579e-05 m.
  After-replacement mean position/orientation MAE: 2.91681373e-06 m / 8.66621212e-08 rad; mean final after-replacement position error 0 m.
  Mean error immediately before refresh events: 7.87225996e-06 m / 2.48051598e-07 rad.
  Mean segment endpoint growth per second: 7.87225996e-06 m/s / 2.48051598e-07 rad/s.

### every_200_steps: 5 refreshes per trajectory

- **physics_only**, forecast before replacement: mean position MAE **0.000478894007 m**, std 0.00029675223 m; mean orientation MAE **1.6676987e-05 rad (0.00095552097 deg)**, std 1.28714065e-05 rad.
  Mean final forecast position error: 0.000386622017 m; mean maximum position error: 0.0030636174 m.
  After-replacement mean position/orientation MAE: 0.000472065117 m / 1.6460868e-05 rad; mean final after-replacement position error 0 m.
  Mean error immediately before refresh events: 0.00136577787 m / 4.32237931e-05 rad.
  Mean segment endpoint growth per second: 0.000682888935 m/s / 2.16118966e-05 rad/s.
- **hybrid**, forecast before replacement: mean position MAE **1.04914653e-05 m**, std 4.97993215e-06 m; mean orientation MAE **3.5099961e-07 rad (2.01107962e-05 deg)**, std 2.00398352e-07 rad.
  Mean final forecast position error: 1.45163523e-05 m; mean maximum position error: 4.87639094e-05 m.
  After-replacement mean position/orientation MAE: 1.03615947e-05 m / 3.46472105e-07 rad; mean final after-replacement position error 0 m.
  Mean error immediately before refresh events: 2.59741103e-05 m / 9.05500857e-07 rad.
  Mean segment endpoint growth per second: 1.29870552e-05 m/s / 4.52750429e-07 rad/s.

### every_500_steps: 2 refreshes per trajectory

- **physics_only**, forecast before replacement: mean position MAE **0.00360603751 m**, std 0.00195619611 m; mean orientation MAE **0.000107288919 rad (0.00614720226 deg)**, std 9.16375033e-05 rad.
  Mean final forecast position error: 0.0118723477 m; mean maximum position error: 0.0142191627 m.
  After-replacement mean position/orientation MAE: 0.00358486344 m / 0.000106769722 rad; mean final after-replacement position error 0 m.
  Mean error immediately before refresh events: 0.0105870364 m / 0.000259598531 rad.
  Mean segment endpoint growth per second: 0.00211740729 m/s / 5.19197061e-05 rad/s.
- **hybrid**, forecast before replacement: mean position MAE **6.03851848e-05 m**, std 2.96379987e-05 m; mean orientation MAE **2.04459953e-06 rad (0.000117146924 deg)**, std 1.41621342e-06 rad.
  Mean final forecast position error: 0.000111692288 m; mean maximum position error: 0.000263025192 m.
  After-replacement mean position/orientation MAE: 6.00331504e-05 m / 2.03476227e-06 rad; mean final after-replacement position error 0 m.
  Mean error immediately before refresh events: 0.000176017242 m / 4.91863051e-06 rad.
  Mean segment endpoint growth per second: 3.52034485e-05 m/s / 9.83726102e-07 rad/s.

## Benchmark trajectories

All following means average the corresponding per-trajectory MAEs with equal flight weight. Orientation is the shortest absolute rotation angle. The shared initial state is excluded.

### no_refresh: 0 refreshes per trajectory

- **physics_only**, forecast before replacement: mean position MAE **0.0121544784 m**, std 0.00491539226 m; mean orientation MAE **0.000127819033 rad (0.00732349112 deg)**, std 4.9017943e-05 rad.
  Mean final forecast position error: 0.0440691331 m; mean maximum position error: 0.0440691331 m.
  After-replacement mean position/orientation MAE: 0.0121544784 m / 0.000127819033 rad; mean final after-replacement position error 0.0440691331 m.
  Mean segment endpoint growth per second: 0.00440691331 m/s / 2.55779142e-05 rad/s.
- **hybrid**, forecast before replacement: mean position MAE **0.00121451697 m**, std 0.000920154814 m; mean orientation MAE **1.26122314e-05 rad (0.000722627628 deg)**, std 7.06397542e-06 rad.
  Mean final forecast position error: 0.00397136973 m; mean maximum position error: 0.0042472956 m.
  After-replacement mean position/orientation MAE: 0.00121451697 m / 1.26122314e-05 rad; mean final after-replacement position error 0.00397136973 m.
  Mean segment endpoint growth per second: 0.000397136973 m/s / 3.50812301e-06 rad/s.

### every_1_steps: 1000 refreshes per trajectory

- **physics_only**, forecast before replacement: mean position MAE **4.29712985e-08 m**, std 1.90215184e-08 m; mean orientation MAE **1.56173415e-09 rad (8.94807754e-08 deg)**, std 4.29757267e-10 rad.
  Mean final forecast position error: 1.67331365e-09 m; mean maximum position error: 2.01678114e-07 m.
  After-replacement mean position/orientation MAE: 0 m / 0 rad; mean final after-replacement position error 0 m.
  Mean error immediately before refresh events: 4.29712985e-08 m / 1.56173415e-09 rad.
  Mean segment endpoint growth per second: 4.29712985e-06 m/s / 1.56173415e-07 rad/s.
- **hybrid**, forecast before replacement: mean position MAE **9.14795116e-09 m**, std 6.8070108e-09 m; mean orientation MAE **1.26054735e-10 rad (7.22240432e-09 deg)**, std 6.76666267e-11 rad.
  Mean final forecast position error: 1.00918644e-09 m; mean maximum position error: 5.33483625e-08 m.
  After-replacement mean position/orientation MAE: 0 m / 0 rad; mean final after-replacement position error 0 m.
  Mean error immediately before refresh events: 9.14795116e-09 m / 1.26054735e-10 rad.
  Mean segment endpoint growth per second: 9.14795116e-07 m/s / 1.26054735e-08 rad/s.

### every_5_steps: 200 refreshes per trajectory

- **physics_only**, forecast before replacement: mean position MAE **4.7268758e-07 m**, std 2.09245597e-07 m; mean orientation MAE **1.71526848e-08 rad (9.82776446e-07 deg)**, std 4.7141252e-09 rad.
  Mean final forecast position error: 2.88312227e-08 m; mean maximum position error: 5.03877992e-06 m.
  After-replacement mean position/orientation MAE: 2.57838542e-07 m / 9.35469098e-09 rad; mean final after-replacement position error 0 m.
  Mean error immediately before refresh events: 1.07424519e-06 m / 3.8989969e-08 rad.
  Mean segment endpoint growth per second: 2.14849038e-05 m/s / 7.79799381e-07 rad/s.
- **hybrid**, forecast before replacement: mean position MAE **1.01605685e-07 m**, std 7.55958295e-08 m; mean orientation MAE **1.385023e-09 rad (7.93559723e-08 deg)**, std 7.51520051e-10 rad.
  Mean final forecast position error: 2.1320204e-08 m; mean maximum position error: 1.32812272e-06 m.
  After-replacement mean position/orientation MAE: 5.53894188e-08 m / 7.556159e-10 rad; mean final after-replacement position error 0 m.
  Mean error immediately before refresh events: 2.31081332e-07 m / 3.14703549e-09 rad.
  Mean segment endpoint growth per second: 4.62162664e-06 m/s / 6.29407098e-08 rad/s.

### every_10_steps: 100 refreshes per trajectory

- **physics_only**, forecast before replacement: mean position MAE **1.65430907e-06 m**, std 7.32379416e-07 m; mean orientation MAE **5.98739121e-08 rad (3.43052247e-06 deg)**, std 1.64531542e-08 rad.
  Mean final forecast position error: 6.2038271e-08 m; mean maximum position error: 2.01086153e-05 m.
  After-replacement mean position/orientation MAE: 1.22468213e-06 m / 4.43324631e-08 rad; mean final after-replacement position error 0 m.
  Mean error immediately before refresh events: 4.29626943e-06 m / 1.55414491e-07 rad.
  Mean segment endpoint growth per second: 4.29626943e-05 m/s / 1.55414491e-06 rad/s.
- **hybrid**, forecast before replacement: mean position MAE **3.55791785e-07 m**, std 2.6433148e-07 m; mean orientation MAE **4.84377775e-09 rad (2.77528022e-07 deg)**, std 2.63188328e-09 rad.
  Mean final forecast position error: 6.69418048e-08 m; mean maximum position error: 5.2540203e-06 m.
  After-replacement mean position/orientation MAE: 2.63475444e-07 m / 3.58851943e-09 rad; mean final after-replacement position error 0 m.
  Mean error immediately before refresh events: 9.23163411e-07 m / 1.25525833e-08 rad.
  Mean segment endpoint growth per second: 9.23163411e-06 m/s / 1.25525833e-07 rad/s.

### every_25_steps: 40 refreshes per trajectory

- **physics_only**, forecast before replacement: mean position MAE **9.48863772e-06 m**, std 4.2027909e-06 m; mean orientation MAE **3.39992727e-07 rad (1.94801483e-05 deg)**, std 9.40331738e-08 rad.
  Mean final forecast position error: 4.38069799e-07 m; mean maximum position error: 0.000122132084 m.
  After-replacement mean position/orientation MAE: 8.41639331e-06 m / 3.01825389e-07 rad; mean final after-replacement position error 0 m.
  Mean error immediately before refresh events: 2.68061103e-05 m / 9.54183452e-07 rad.
  Mean segment endpoint growth per second: 0.000107224441 m/s / 3.81673381e-06 rad/s.
- **hybrid**, forecast before replacement: mean position MAE **2.02951434e-06 m**, std 1.50885285e-06 m; mean orientation MAE **2.73964417e-08 rad (1.56970048e-06 deg)**, std 1.50223502e-08 rad.
  Mean final forecast position error: 4.07951738e-07 m; mean maximum position error: 3.16342231e-05 m.
  After-replacement mean position/orientation MAE: 1.80134246e-06 m / 2.43352156e-08 rad; mean final after-replacement position error 0 m.
  Mean error immediately before refresh events: 5.70429689e-06 m / 7.65306521e-08 rad.
  Mean segment endpoint growth per second: 2.28171876e-05 m/s / 3.06122608e-07 rad/s.

### every_50_steps: 20 refreshes per trajectory

- **physics_only**, forecast before replacement: mean position MAE **3.676212e-05 m**, std 1.63051723e-05 m; mean orientation MAE **1.25335429e-06 rad (7.18119109e-05 deg)**, std 3.44362106e-07 rad.
  Mean final forecast position error: 2.19668516e-05 m; mean maximum position error: 0.000411443715 m.
  After-replacement mean position/orientation MAE: 3.46276426e-05 m / 1.18374815e-06 rad; mean final after-replacement position error 0 m.
  Mean error immediately before refresh events: 0.000106723872 m / 3.48030674e-06 rad.
  Mean segment endpoint growth per second: 0.000213447744 m/s / 6.96061349e-06 rad/s.
- **hybrid**, forecast before replacement: mean position MAE **7.73589464e-06 m**, std 5.73581569e-06 m; mean orientation MAE **1.02256345e-07 rad (5.85885699e-06 deg)**, std 5.70846454e-08 rad.
  Mean final forecast position error: 3.06806023e-06 m; mean maximum position error: 0.000101246574 m.
  After-replacement mean position/orientation MAE: 7.29267157e-06 m / 9.64638818e-08 rad; mean final after-replacement position error 0 m.
  Mean error immediately before refresh events: 2.21611539e-05 m / 2.89623151e-07 rad.
  Mean segment endpoint growth per second: 4.43223079e-05 m/s / 5.79246301e-07 rad/s.

### every_100_steps: 10 refreshes per trajectory

- **physics_only**, forecast before replacement: mean position MAE **0.000142794238 m**, std 6.34523358e-05 m; mean orientation MAE **4.605526e-06 rad (0.000263877202 deg)**, std 1.22423837e-06 rad.
  Mean final forecast position error: 0.000411165879 m; mean maximum position error: 0.00163237613 m.
  After-replacement mean position/orientation MAE: 0.00013862778 m / 4.47711649e-06 rad; mean final after-replacement position error 0 m.
  Mean error immediately before refresh events: 0.000416645801 m / 1.28409502e-05 rad.
  Mean segment endpoint growth per second: 0.000416645801 m/s / 1.28409502e-05 rad/s.
- **hybrid**, forecast before replacement: mean position MAE **2.9814647e-05 m**, std 2.35996513e-05 m; mean orientation MAE **3.74658982e-07 rad (2.14663784e-05 deg)**, std 2.26806635e-07 rad.
  Mean final forecast position error: 3.02811234e-05 m; mean maximum position error: 0.000397226013 m.
  After-replacement mean position/orientation MAE: 2.89489364e-05 m / 3.64098748e-07 rad; mean final after-replacement position error 0 m.
  Mean error immediately before refresh events: 8.65710658e-05 m / 1.05602338e-06 rad.
  Mean segment endpoint growth per second: 8.65710658e-05 m/s / 1.05602338e-06 rad/s.

### every_200_steps: 5 refreshes per trajectory

- **physics_only**, forecast before replacement: mean position MAE **0.000618420854 m**, std 0.000314685779 m; mean orientation MAE **1.63610126e-05 rad (0.000937416969 deg)**, std 4.49024056e-06 rad.
  Mean final forecast position error: 0.0018357001 m; mean maximum position error: 0.00432452536 m.
  After-replacement mean position/orientation MAE: 0.000610103073 m / 1.61691518e-05 rad; mean final after-replacement position error 0 m.
  Mean error immediately before refresh events: 0.00166355625 m / 3.83721551e-05 rad.
  Mean segment endpoint growth per second: 0.000831778125 m/s / 1.91860775e-05 rad/s.
- **hybrid**, forecast before replacement: mean position MAE **0.000129511545 m**, std 0.000122879202 m; mean orientation MAE **1.43985469e-06 rad (8.2497597e-05 deg)**, std 9.72480158e-07 rad.
  Mean final forecast position error: 0.000270539872 m; mean maximum position error: 0.00104405005 m.
  After-replacement mean position/orientation MAE: 0.000127795643 m / 1.42089979e-06 rad; mean final after-replacement position error 0 m.
  Mean error immediately before refresh events: 0.000343180541 m / 3.79098015e-06 rad.
  Mean segment endpoint growth per second: 0.000171590271 m/s / 1.89549007e-06 rad/s.

### every_500_steps: 2 refreshes per trajectory

- **physics_only**, forecast before replacement: mean position MAE **0.0034595046 m**, std 0.00136417222 m; mean orientation MAE **4.92893578e-05 rad (0.00282407218 deg)**, std 1.69546165e-05 rad.
  Mean final forecast position error: 0.0106433156 m; mean maximum position error: 0.012466616 m.
  After-replacement mean position/orientation MAE: 0.00344137032 m / 4.90928123e-05 rad; mean final after-replacement position error 0 m.
  Mean error immediately before refresh events: 0.00906714444 m / 9.82727562e-05 rad.
  Mean segment endpoint growth per second: 0.00181342889 m/s / 1.96545512e-05 rad/s.
- **hybrid**, forecast before replacement: mean position MAE **0.000647920914 m**, std 0.000617633743 m; mean orientation MAE **7.05546305e-06 rad (0.000404248255 deg)**, std 3.65497105e-06 rad.
  Mean final forecast position error: 0.00273376346 m; mean maximum position error: 0.00301311765 m.
  After-replacement mean position/orientation MAE: 0.000644348632 m / 7.01879098e-06 rad; mean final after-replacement position error 0 m.
  Mean error immediately before refresh events: 0.00178614116 m / 1.8336033e-05 rad.
  Mean segment endpoint growth per second: 0.000357228231 m/s / 3.6672066e-06 rad/s.

## Refresh timing and theory

A schedule selects state indices, not control indices. Step k corresponds to t=k*dt. The transition from k-1 to k first uses the recorded control u[k-1] and the previous post-replacement state. Its forecast is saved before any reset:

$$\tilde x_k=F(\hat x^+_{k-1},u_{k-1},\Delta t)$$

$$\hat x^+_k=\begin{cases}x^{sim}_k,&k\in\mathcal R\\\tilde x_k,&k\notin\mathcal R\end{cases}$$

For the hybrid predictor, F is the independent physics step followed by the learned residual composition from phases 4 and 5. A refresh replaces position, scalar-first quaternion orientation, world-frame linear velocity, and body-frame angular velocity together. The next prediction constructs NN features from that replaced state. Replacing position alone would leave velocity and attitude drift in the continuing rollout; that partial-reset behavior is not used here.

A refresh is state replacement, not retraining or an NN weight update. There is no online controller feedback, noisy measurement model, partial observation filter, or interpolation. The truth provider returns the saved simulator state only when the core rollout requests a selected step. With no schedule, it is never called. The original physics and hybrid no-refresh rollout interfaces remain unchanged and accept no future truth.

## Supported schedule contracts

- `RefreshSchedule()` disables refreshes by default.
- `RefreshSchedule(interval_steps=100)` refreshes at 100, 200, ... within the horizon.
- `RefreshSchedule(steps=(50, 200, 700))` uses those explicit state indices, sorted chronologically.
- `RefreshSchedule(interval_seconds=1.0)` is the grid-aligned time equivalent of every 100 steps at dt=0.01 s.
- `RefreshSchedule(times=(0.5, 2.0, 7.0))` uses explicit times relative to initialization.

Choose one schedule form. Times must align with the prediction grid; off-grid inputs are rejected, not silently rounded. Explicit steps outside the flight horizon, duplicates, and nonpositive steps/times are rejected. Step 0 is initialization and is not counted as a refresh. A periodic interval longer than the horizon produces no events. Final-step events are allowed and counted: for 1,000 transitions, every 500 steps produces events at 500 and 1,000. The final event changes the after-replacement state but cannot change the forecast already made at step 1,000.

## Why both metric views are retained

`forecast_before_replacement` scores the saved local forecast at every timestamp. At refresh times this is the error immediately before injecting truth; between refreshes it is the ordinary recursive error. This is the primary view in the report and frequency plots.

`state_after_replacement` scores the state that is actually used to continue the rollout. It has zero error at exact full-state reset times by construction. With refresh every step it becomes perfect at every scored timestamp, so it is not used to claim model accuracy. The corresponding before-replacement forecast still has the model's ordinary one-step error. No refresh reproduces the phase-5 recursive results in both views.

Position MAE is time-average Euclidean distance; orientation MAE is time-average shortest rotation angle in radians/degrees. RMSE, final/maximum position error, linear/angular velocity MAE/RMSE, and per-trajectory variability are saved for both views. Means use equal flight weights and standard deviations across trajectory metrics use ddof=0. Test and waypoint benchmark stay separate.

## Pre-refresh events and growth segments

Each refresh has a separate full-state before snapshot and corrected snapshot. Event CSVs report the position, orientation, and velocity errors immediately before replacement, plus the post-reset position/orientation error. Each segment begins at initialization or a corrected refresh state and ends at the next refresh forecast or the final forecast. A trailing unrefreshed segment is retained; a final-step refresh does not add an empty segment.

Segment rows report the initial post-reset error, endpoint forecast error, maximum/time-mean forecast errors, and endpoint-minus-start growth divided by elapsed seconds. That growth rate is an interval-average endpoint measure, not an instantaneous derivative or a claim that error grows monotonically. Per-flight drift rows average their segments equally; the readable report then averages those rows equally across trajectories.

## Plots and playback

Each flight-comparison plot retains the large 3D path plus position and orientation angle error over time. The 3D curves show continuing post-replacement paths, with open predicted-point markers immediately before sampled refresh events and green marks at truth replacement locations. The error curves always show before-replacement forecasts. All refresh timestamps appear as green rug ticks along the bottom of the error plots; sparse schedules also get vertical event lines. For dense schedules, up to 40 3D event markers are sampled and that count is disclosed in the legend. Full event records are never subsampled in saved data.

Frequency figures compare mean position/orientation MAE against periodic interval and actual refresh count, separately for test and benchmark. Interval cases are categorical so 'None' has no invented finite duration. Count plots retain zero for no refresh using a symlog axis. No automatic path-fidelity threshold or optimal interval is selected; interpret these tradeoffs manually.

Combined prediction archives use `physics_states` and `hybrid_states` for the post-replacement paths used in playback. Their `*_forecast_states` arrays preserve every before-replacement forecast. Existing blue/orange comparison playback loads these files without a rendering change. Jumping back to truth in playback is an explicit reset, not an improvement made by the NN.

## Files and artifacts

- `src/model_drone_residual/refresh.py`: schedule validation/resolution, refresh-aware rollout, before/after event snapshots.
- `src/model_drone_residual/refresh_evaluation.py`: shared-schedule physics/hybrid comparisons, both metric views, refresh events and drift segments.
- `scripts/model_drone_residual/evaluate_drone_refresh.py`: no-refresh, custom schedule, and fixed-checkpoint sweep entry point.
- `rollout_metrics.csv` / `.json`, `test_metrics.json`: per-trajectory physical errors and equal-weight means, separated by schedule/split/predictor/metric view.
- `comparison_metrics.csv`: summary rows including interval, event count, mean position/orientation MAEs, and standard deviations.
- `drift_metrics.csv`: per-trajectory pre-refresh errors and segment-growth summaries.
- `<schedule>/refresh_schedule.json`: requested configuration, exact resolved steps/times, final-step semantics.
- `<schedule>/predictions/<split>_recursive.npz`: truth, applied controls, IDs, times, pre/post full traces, separate pre-refresh/corrected snapshots, refresh steps/times, checkpoint metadata.
- `<schedule>/refresh_events_<split>.csv`, `segments_<split>.csv`, `drift_metrics_<split>.csv`: full event/segment diagnostics.
- `<schedule>/trajectory_metrics_<split>.csv`, `metrics_<split>.json`: individual schedule results for both metric views.
- `<schedule>/plots/`: preselected first trajectory per family, using the existing large-3D-plus-two-errors layout.
- `plots/refresh_frequency_test.png`, `refresh_frequency_benchmark.png`: primary errors versus interval and count.
- `run_metadata.json`: exact command, immutable source/checkpoint/input hashes, model provenance, resolved schedules, completion status, runtime, and zero weight updates.

## Reproduction

Actual command for this directory:

```powershell
python scripts/model_drone_residual/evaluate_drone_refresh.py --sweep
```

From the repository root, default no-refresh evaluation and the initial nine-case sweep:

```powershell
.\.venv\Scripts\python.exe scripts/model_drone_residual/evaluate_drone_refresh.py
.\.venv\Scripts\python.exe scripts/model_drone_residual/evaluate_drone_refresh.py --sweep
```

Custom schedule examples:

```powershell
python scripts/model_drone_residual/evaluate_drone_refresh.py --refresh-every 100
python scripts/model_drone_residual/evaluate_drone_refresh.py --refresh-steps 50 200 700
python scripts/model_drone_residual/evaluate_drone_refresh.py --refresh-every-seconds 1.0
python scripts/model_drone_residual/evaluate_drone_refresh.py --refresh-times 0.5 2.0 7.0
```

Example comparison playback (when the sweep includes this directory):

```powershell
python scripts/drone/playback_flight.py runs/Drone/phase_6/every_100_steps/predictions/test_recursive.npz --trajectory-id test_000000 --compare both --paused
```

Default inputs are the fixed phase-2 archives and phase-5 best checkpoint. Use `--dataset`, `--benchmark`, `--checkpoint`, `--output-root`, and `--threads` to change paths/runtime. Outputs go under phase_6 and then repeat_N subdirectories, preserving previous results.

## Assumptions and next work

Refreshes use exact simulator full states. Real sensors, noisy or partial observations, estimation filters, communication latency, wind, contact, and altered drone properties are outside this phase. The results are for one previously trained seed and checkpoint; phase 7 remains the controlled learning experiment stage. Fixed weights and held-out trajectories allow refresh schedules to be compared without retraining or changing the reference controller.

Drone_Plan.md, README.md, Runs Masterlist.md, phase-5 checkpoint, and prior phase outputs were not edited. No commit was created.

## Interpretation of this sweep

More frequent full-state refreshes reduced both position and orientation forecast MAE for both predictors in the tested schedules. The hybrid predictor retained lower mean errors than physics alone. Resetting the complete state limits accumulated velocity and attitude errors as well as position drift; the fixed neural network continues to provide its learned local correction between resets.

- Test, hybrid: no refresh gives 0.442592 mm position MAE and 0.000367852 deg orientation MAE. Every 100 steps (1 s) gives 0.00299554 mm and 5.1075e-06 deg, respectively.
- Benchmark, hybrid: no refresh gives 1.21452 mm position MAE and 0.000722628 deg orientation MAE. Every 100 steps (1 s) gives 0.0298146 mm and 2.14664e-05 deg, respectively.

These are observations for the existing fixed checkpoint and flights. No acceptable-error cutoff or recommended refresh interval is imposed. With refresh every step, each forecast is a genuine one-step prediction from the preceding true state; only the separately scored post-replacement trace is exact by construction.

## Implementation verification

- Full project regression: **221 tests passed in 39.14 s**, including the existing pendulum and unicycle tests and 26 new refresh checks.
- New checks cover step/time schedules, off-grid rejection, full-state replacement, correct control indexing, no future-truth requests without refresh, every-step and final-step behavior, drift segments, equal-flight metrics, unchanged weights/normalization, and compatibility with comparison playback.
- An additional real-data CLI run using `--refresh-times 0.5 2.0 7.0` completed successfully in the ignored `.pytest_cache/refresh_cli_smoke/phase_6/` directory. It resolved exactly to steps 50, 200, and 700, including the trailing segment after the last refresh.
- The recorded nine-case sweep completed in 277.69 s: 18 schedule/split evaluations, 55,080 predictor-specific refresh events, 55,120 drift segments, 720 trajectory-metric rows, 72 comparison-summary rows, and 56 PNG figures.
- Independently recomputed every saved trajectory metric and its equal-weight mean/standard deviation from all 18 prediction archives. All JSON summaries and comparison CSV values agree.
- No-refresh physics and hybrid traces reproduce the saved phase-5 recursive traces **exactly**, for both test and benchmark.
- Every-step forecasts match an independent one-step calculation **exactly** when using the same batch size. Compared with the saved phase-5 one-step arrays, the largest absolute state-component difference is 2.77200485e-12; this is numerical variation from the float32 NN batch calculation (phase 5 used larger batches), rather than recursive drift.
- Checked every refresh snapshot and corrected state against its archived forecast and truth, every untouched timestamp against the continuing forecast, finite states and unit quaternions, and all combined archives with the existing playback loader.
- Visually inspected both frequency figures and representative dense, 25-step, and 100-step flight comparisons. The large 3D plot and the two forecast-error panels are retained, with refresh markers and units visible.
- Source/input hashes match run metadata. Drone_Plan.md, README.md, Runs Masterlist.md, and the phase-5 checkpoint match their hashes from before phase-6 work. No commit was created.

Machine-readable artifact checks: `artifact_verification.json`.

Regression command:

```powershell
.\.venv\Scripts\python.exe -m pytest -q --basetemp .pytest_cache/drone_phase6_regression --tb=short
```

## Run Commands

```powershell
python scripts/model_drone_residual/evaluate_drone_refresh.py --refresh-every 100
```

```powershell
python scripts/model_drone_residual/evaluate_drone_refresh.py --refresh-every-seconds 1.0
```

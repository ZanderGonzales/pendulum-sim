# Baseline Model: python scripts\model_baseline\run_experiment_n.py
Model trained using traditional supervised learning, given the complete initial pendulum state and asked to produce the entire pattern.
[t, theta0, omega0, torque(t)] -> [theta(t), omega(t)]

## Baseline Run 0
Tested new model architecture to set a baseline. Essentially failed, with the model predicting no pendulum movement.
- 40 trajectories
- 300 epochs
- 300 optimizer updates
- Mean Theta MAE: 0.186361, Mean Omega MAE 0.579537

## Baseline Run 1
Tried to expand the space of training data, sampling an 8x4 grid of initial conditions for training data. *Slight* improvement.
- 40 trajectories
- 300 epochs
- 300 optimizer updates
- Sampled 8x4 grid for training trajectories
- Mean Theta MAE: 0.186017, Mean Omega MAE 0.563198

## Baseline Run 2
Increased trajectory sample size from 40 to 100. Slight improvement on shared tests from 0 and 1, but overall higher error from the aggregate of the tests
- 100 trajectories
- 300 epochs
- 300 optimizer updates
- Mean Theta MAE: 0.338884, Mean Omega MAE 0.980828

## Baseline Run 3
Changed training procedures to have mini-batches and more frequent optimizer updates rather than once per epoch. Also used a learning-rate scheduler (this didn't do anythinga as the improvement never slowed). Performed better, started to see predicted oscillation.
- 40 trajectories
- 40 epochs
- 126 batches per epoch, 256 samples per batch
- 5040 optimizer updates
- Mean Theta MAE: 0.171791, Mean Omega MAE 0.502750

## Baseline Run 4
Changed to have even more optimizer updates, and it had VAST improvements.
- 40 trajectories
- 120 epochs
- 126 batches per epoch, 256 samples per batch
- 15120 optimizer updates
- Mean theta MAE: 0.026866, Mean omega MAE 0.094048

## Baseline Run 5
Changed to have more optimizer updates but fewer epochs, had slight improvement
- 40 trajectories
- 100 epochs
- 200 batches per epoch, 160 samples per batch
- 20000 optimizer updates
- Mean Theta MAE: 0.020872, Mean Omega MAE 0.070498

# Residual Model: python scripts\model_residual\run_residual_experiment_n.py
Supervised learning model that is trained to learn the residual, or the difference between a given state and the next. The next state is then constructed and propagated for the next input.
[current theta, current omega, torque at the current step, midpoint torque, and next-step torque] -> [delta_theta, delta_omega]

## Residual Run 0
Converged WAY faster than the baseline model despite having the exact same data and conditions as Baseline Run 5
- 40 trajectories
- 100 epochs
- 200 batches per epoch, 160 samples per batch
- 20000 optimizer updates
- Mean Theta MAE: 0.000741, Mean Omega MAE 0.002320

## Residual Run 1
Still got to the same amount of error despite having a tenth of the optimizer updates as run 0
- 40 trajectories
- 10 epochs
- 200 batches per epoch, 160 samples per batch
- 2000 optimizer updates
- Mean Theta MAE: 0.010362, Mean Omega MAE 0.031768

## Residual Run 2
STILL got to the same amount of error with only 30 trajectories
- 30 trajectories
- 10 epochs
- 200 batches per epoch, 160 samples per batch
- 2000 optimizer updates
- Mean Theta MAE: 0.010625, Mean Omega MAE 0.032377

## Residual Run 3
Changed the torque patterns to be substantially more difficult, with sinusoidal torques with frequency from 0-2pi rad/s and amplitude from 5-10 N*m. Had higher error than Residual Run 0 (what the rest was based on) but still did well
- 40 trajectories
- 100 epochs
- 200 batches per epoch, 160 samples per batch
- 20000 optimizer updates
- Mean Theta MAE: 0.038217, Mean Omega MAE 0.112272


# Unicycle Residual
Supervised learning model that is trained to learn the residual, or the difference between a given state and the next. The next state is then constructed and propagated for the next input.
[forward v, omega] -> [delta_x_body, delta_y_body, delta_theta]

## Phase U5 Experiment Matrix
### Experiment A
Didn't use an NN, just made sure that converting body to inertial frames and then plotting it worked correctly

### Experiment B
Used a narrower field of v and omega values, performed well
- 64 trajectories
- 25 epochs
- 12 batches per epoch, ~256 samples per batch
- 300 optimizer updates
- Mean X MAE: 0.0063102, Mean Y MAE: 0.00660586, Mean Theta MAE: 0.00757348, 

### Experiment C
Trained with cardinal starting headings and then validated against random headings
- 64 trajectories
- 25 epochs
- 12 batches per epoch, ~256 samples per batch
- 300 optimizer updates
- Mean X MAE: 0.0154338, Mean Y MAE: 0.0189883, Mean Theta MAE: 0.0175798,

### Experiment D
Ran similar data while having 8, 24, and 48 training trajectories. Performance was not affected greaetly
-  trajectories
-  epochs
-  batches per epoch, 256 samples per batch
-  optimizer updates
- Mean X MAE: , Mean Y MAE: , Mean Theta MAE: ,

### Experiment E
Compared having 48 similar training trajectories vs 12 varied training trajectories. The 12 performed significantly better
-  trajectories
-  epochs
-  batches per epoch, 256 samples per batch
-  optimizer updates
- Mean X MAE: , Mean Y MAE: , Mean Theta MAE: ,

### Experiment F
Changed optimizer updates from 100,300, and 900. Performance increased dramatically
-  trajectories
-  epochs
-  batches per epoch, 256 samples per batch
-  optimizer updates
- Mean X MAE: , Mean Y MAE: , Mean Theta MAE: ,

# Agent Instructions
Never edit this file; this file is for manual run notes only
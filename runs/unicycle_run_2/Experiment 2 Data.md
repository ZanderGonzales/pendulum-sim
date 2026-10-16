# Experiment 2: Aggressive maneuvers and figure-eight test

**Difference from Experiment 1:** training controls use speeds of 0-3 and turn rates of -7 to 7 rad/s, with a new control every 1-3 steps rather than speeds of 0-2, turn rates of -1.5 to 1.5 rad/s, and 3-10 steps. One held-out test trajectory is a 60-step Gerono figure eight with a transverse crossing (trajectory ID 12; maximum speed 2.3614 and maximum |omega| 6.6403 rad/s). The model, optimizer, split sizes, training transitions per epoch, and update schedule match Experiment 1.

- Number of trajectories: total 64 (train 48, validation 8, test 8)
- Epochs: 15
- Batches per epoch: 100
- Samples per batch: 28-29 (balanced; 2880 training samples per epoch)
- Optimizer updates: 1500
- Figure-eight test trajectory ID: 12 (60 steps, maximum speed 2.3614, maximum |omega| 6.6403 rad/s, endpoint position error 0.003448)
- Mean X MAE: 0.011381085
- Mean Y MAE: 0.016579357
- Mean Theta MAE: 0.017290707 rad
- One-step body-frame RMSE: 0.0010822162
- Free-running position RMSE: 0.027905438
- Best validation MSE (standardized): 0.00022216581
- Path comparisons and per-trajectory predictions: `plots/` and `predictions/`.

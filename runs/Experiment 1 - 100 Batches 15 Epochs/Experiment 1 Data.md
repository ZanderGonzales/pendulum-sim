# Experiment 1: 100 batches per epoch, 15 epochs

**Difference from the previous update-budget experiments:** uses the same broad-control dataset seed and 48/8/8 trajectory split as U5 Experiments D/F, while setting a smaller balanced batch size through exactly 100 batches per epoch for 15 epochs (1500 updates). This extends the update budget beyond the prior 900-update run.

- Number of trajectories: total 64 (train 48, validation 8, test 8)
- Epochs: 15
- Batches per epoch: 100
- Samples per batch: 28-29 (balanced; 2880 training samples per epoch)
- Optimizer updates: 1500
- Mean X MAE: 0.0066391725
- Mean Y MAE: 0.0035642349
- Mean Theta MAE: 0.0059398077 rad
- One-step body-frame RMSE: 0.0004167759
- Free-running position RMSE: 0.010098803
- Best validation MSE (standardized): 0.001263928
- Path comparison plots and per-trajectory predictions: `plots/` and `predictions/`.

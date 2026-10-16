# Unicycle U4 recursive rollout

Predicted local body increments are rotated by the current predicted heading before updating position. The resulting predicted state is fed into the next step; test states are not substituted during rollout.

- Command: `'C:\Users\micha\OneDrive\Documents\Research\Pendulum Sim\.venv\Scripts\python.exe' scripts/model_unicycle_residual/evaluate_unicycle_rollout.py`
- Code version: 9a1cc33
- Checkpoint: `runs\unicycle_u3\checkpoint_best.pt`
- Dataset: `runs\unicycle_u2\dataset.npz`
- Test trajectories: [12, 13]
- Dataset seed: 2026
- Mean test position RMSE: 0.01741033
- Mean test final position error: 0.038259956
- Mean test wrapped heading RMSE: 0.024711946 rad
- Mean test path-length error: -0.020760646

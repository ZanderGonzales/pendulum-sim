# Unicycle U3 residual model run

The MLP maps standardized [v, omega, dt] to standardized body-frame [delta_x_body, delta_y_body, delta_theta]. Standardizers were fit on training trajectories only.

Coordinate convention: right-handed inertial x-y plane; body +x forward, body +y left, theta=0 along inertial +x, positive omega counter-clockwise.

- Command: `'C:\Users\micha\OneDrive\Documents\Research\Pendulum Sim\.venv\Scripts\python.exe' scripts/model_unicycle_residual/train_unicycle_residual.py --epochs 80 --batch-size 128 --max-updates 500 --seed 2026`
- Code version: b1bb010 (working tree dirty)
- Seed: 2026
- Optimizer updates: 400
- Best validation epoch: 80
- Best standardized validation MSE: 0.007151878
- Test physical-unit metrics: `{"dtheta_mae": 0.0009515354176983237, "dtheta_rmse": 0.0011629745131358504, "dx_body_mae": 0.0006443645106628537, "dx_body_rmse": 0.0008636770071461797, "dy_body_mae": 7.131414895411581e-05, "dy_body_rmse": 7.456464663846418e-05, "overall_rmse": 0.0008374580065719783}`

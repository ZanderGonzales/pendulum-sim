# Experiment F: Optimizer Updates

**Difference from an average run / previous experiment:** Changes only the optimizer-update budget (100, 300, 900) while holding dataset, split, architecture, controls, and seed fixed.

### Training budget

| Condition | Number of trajectories | Epochs | Batches per epoch | Samples per batch | Optimizer updates |
|---|---|---:|---:|---|---:|
| updates_0100 | total 64 (train 48, validation 8, test 8) | 9 | 12 (final 4) | 256 (final 64) | 100 |
| updates_0300 | total 64 (train 48, validation 8, test 8) | 25 | 12 | 256 (final 64) | 300 |
| updates_0900 | total 64 (train 48, validation 8, test 8) | 75 | 12 | 256 (final 64) | 900 |

### Test metrics

| Condition | Mean X MAE | Mean Y MAE | Mean Theta MAE (rad) | One-step body RMSE | Position RMSE | Final position error | Heading RMSE (rad) | Path-length error |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| updates_0100 | 0.0461948 | 0.0431672 | 0.0487147 | 0.00307634 | 0.0888057 | 0.165903 | 0.0614033 | -0.0551054 |
| updates_0300 | 0.0326286 | 0.0224776 | 0.0328437 | 0.00177279 | 0.0548468 | 0.108262 | 0.0408026 | -0.0280632 |
| updates_0900 | 0.00971699 | 0.0055489 | 0.00832975 | 0.000495932 | 0.0147711 | 0.0277964 | 0.00997106 | -0.0075159 |

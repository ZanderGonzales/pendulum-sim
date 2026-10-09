# Experiment E: Data Variety

**Difference from an average run / previous experiment:** Compares many narrow-range training trajectories with fewer broad-range trajectories on identical broad validation/test paths; both count and variety change.

### Training budget

| Condition | Number of trajectories | Epochs | Batches per epoch | Samples per batch | Optimizer updates |
|---|---|---:|---:|---|---:|
| fewer_varied_12 | total 64 (train 12, validation 8, test 8, unused 36) | 100 | 3 | 256 (final 208) | 300 |
| many_similar_48 | total 64 (train 48, validation 8, test 8) | 25 | 12 | 256 (final 64) | 300 |

### Test metrics

| Condition | Mean X MAE | Mean Y MAE | Mean Theta MAE (rad) | One-step body RMSE | Position RMSE | Final position error | Heading RMSE (rad) | Path-length error |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| fewer_varied_12 | 0.0430729 | 0.0286913 | 0.0456472 | 0.00232996 | 0.0734548 | 0.146107 | 0.0552615 | -0.042148 |
| many_similar_48 | 0.336526 | 0.320474 | 0.352452 | 0.02506 | 0.600198 | 1.00953 | 0.408473 | -0.500168 |

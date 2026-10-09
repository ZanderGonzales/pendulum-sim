# Experiment B: Narrow Control

**Difference from an average run / previous experiment:** Compared with the broad-range average run, this model uses narrower speed and turn-rate ranges and measures interpolation within that configured envelope.

### Training budget

| Condition | Number of trajectories | Epochs | Batches per epoch | Samples per batch | Optimizer updates |
|---|---|---:|---:|---|---:|
| narrow_well_covered | total 64 (train 48, validation 8, test 8) | 25 | 12 | 256 (final 64) | 300 |

### Test metrics

| Condition | Mean X MAE | Mean Y MAE | Mean Theta MAE (rad) | One-step body RMSE | Position RMSE | Final position error | Heading RMSE (rad) | Path-length error |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| narrow_well_covered | 0.0063102 | 0.00660586 | 0.00757348 | 0.000743718 | 0.011496 | 0.0170718 | 0.00949926 | -0.00583904 |

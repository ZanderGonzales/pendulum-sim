# Experiment D: Data Quantity

**Difference from an average run / previous experiment:** Varies training trajectory count (8, 24, 48) while keeping the nested data source, held-out trajectories, architecture, seed, and update budget fixed.

### Training budget

| Condition | Number of trajectories | Epochs | Batches per epoch | Samples per batch | Optimizer updates |
|---|---|---:|---:|---|---:|
| train_08 | total 64 (train 8, validation 8, test 8, unused 40) | 150 | 2 | 256 (final 224) | 300 |
| train_24 | total 64 (train 24, validation 8, test 8, unused 24) | 50 | 6 | 256 (final 160) | 300 |
| train_48 | total 64 (train 48, validation 8, test 8) | 25 | 12 | 256 (final 64) | 300 |

### Test metrics

| Condition | Mean X MAE | Mean Y MAE | Mean Theta MAE (rad) | One-step body RMSE | Position RMSE | Final position error | Heading RMSE (rad) | Path-length error |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| train_08 | 0.0418248 | 0.0236768 | 0.0416407 | 0.00218521 | 0.0658768 | 0.131723 | 0.0508095 | -0.0192461 |
| train_24 | 0.0307373 | 0.0214848 | 0.0312012 | 0.00166765 | 0.0517675 | 0.101667 | 0.037691 | -0.017184 |
| train_48 | 0.0326286 | 0.0224776 | 0.0328437 | 0.00177279 | 0.0548468 | 0.108262 | 0.0408026 | -0.0280632 |

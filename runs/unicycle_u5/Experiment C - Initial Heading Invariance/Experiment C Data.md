# Experiment C: Initial Heading Invariance

**Difference from an average run / previous experiment:** Compared with the standard broad-control run, this changes the initial-heading design: training uses cardinal headings while validation and test use unseen headings.

### Training budget

| Condition | Number of trajectories | Epochs | Batches per epoch | Samples per batch | Optimizer updates |
|---|---|---:|---:|---|---:|
| unseen_test_headings | total 64 (train 48, validation 8, test 8) | 25 | 12 | 256 (final 64) | 300 |

### Test metrics

| Condition | Mean X MAE | Mean Y MAE | Mean Theta MAE (rad) | One-step body RMSE | Position RMSE | Final position error | Heading RMSE (rad) | Path-length error |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| unseen_test_headings | 0.0154338 | 0.0189883 | 0.0175798 | 0.00135082 | 0.0322835 | 0.0521441 | 0.0206334 | -0.00062447 |

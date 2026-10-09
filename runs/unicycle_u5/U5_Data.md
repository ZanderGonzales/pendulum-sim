# Unicycle Phase U5: Controlled experiments A-F

Experiment G (representation comparison) was excluded as requested. Experiments A-F use lettered folders and `Experiment [letter] Data.md` summaries. Future user-defined experiments can use numbered names such as `Experiment 1`. Condition folders retain training curves, physical one-step metrics, standardizers, checkpoints, data split IDs, and free-running rollout metrics.

See `summary.csv` and `comparison_metrics.png` for the combined results. Experiments D and F hold out the same broad-dataset validation and test trajectories. Experiment E also holds evaluation trajectories fixed while changing training count and variety.

## Conclusions

- **Interpolation (B):** narrow-range test position RMSE was 0.0115; this measures performance within the same configured operating envelope.
- **Heading transfer (C):** held-out initial-heading test position RMSE was 0.03228, with wrapped heading RMSE 0.02063 rad.
- **Data quantity (D):** position RMSEs for 8/24/48 training trajectories were 0.06588/0.05177/0.05485; the result is not monotonic at this fixed update budget, so 300 updates may not let every dataset size converge equally.
- **Variety (E):** on the same broad held-out set, 48 similar trajectories gave position RMSE 0.6002, versus 0.07345 for 12 varied trajectories. This shows the trade-off under this run, and does not isolate variety from sample count.
- **Optimizer updates (F):** position RMSE at 100/300/900 updates was 0.08881/0.05485/0.01477; more updates improved this fixed-data run.

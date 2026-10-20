# Experiment 1 Data: Drone Phase 1

Six controlled MuJoCo flights; no training, learned model, or train/validation/test split.

- Seed: 0
- Prediction interval: 0.01 s; internal interval: 0.002 s
- Requested duration: 10.0 s per family; 1000 transitions each
- Valid flights: 6/6

## Artifacts

- `plots/path_comparison_summary.png`: controller reference and actual MuJoCo paths.
- `plots/<family>_state_comparison.png`: position, velocity, tracking error, applied moments.
- `<family>_flight.npz`: N+1 full states, N requested/applied physical controls and raw actuator controls, contacts, references, timing, JSON metadata.
- `simulation_metrics.csv`: per-flight validity and reference-tracking errors in metres.
- `failed_trajectories.json`: rejected flights and reasons; empty when all flights are valid.
- `run_metadata.json`: physical parameters, simulator/model versions, controller gains, reference paths, initial states, code revision, and seed.

## Interpretation

Tracking error measures the flight controller's ability to follow its reference. It is not an NN prediction error. Interpret curves manually; no model-fidelity acceptance threshold is imposed.

## Changes and next phase

Phase 1 adds the pinned reference simulator and controller. No earlier drone learning experiment exists. Phase 2 will add larger seeded datasets, coverage plots, storage/loading, and trajectory splits.

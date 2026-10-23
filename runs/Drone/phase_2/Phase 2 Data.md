# Phase 2 Data: Drone Dataset Generation

## Results

- Main dataset: 100 complete trajectories, with {'train': 80, 'validation': 10, 'test': 10}.
- Separate benchmark: 10 complete waypoints trajectories.
- Each trajectory: 1000 transitions, 1001 full states, 10 seconds.
- Prediction/control interval: 0.01 s; internal RK4 step: 0.002 s.
- Rejected attempts: 0; all saved trajectories are complete and contact-free.
- Root dataset seed: 2026.

## How the data are generated

Each trajectory is a controlled MuJoCo simulation. Seeded draws vary world placement, height, yaw, path scale, circle/figure-eight cycle count, initial roll/pitch, linear velocity, and angular velocity. The five main families are balanced within each split up to integer remainders. Hover changes placement and initial disturbance, not its reference path shape. The benchmark family is excluded from training, validation, and the ordinary test set.

## Why these splits are used

Complete trajectories stay in one split so neighboring timesteps cannot leak into validation or testing. The ordinary test split contains new trajectories from familiar families. The separate benchmark tests a family absent from all main splits. Keep it out of checkpoint selection and hyperparameter tuning when claiming held-out-family generalization.

IDs use <split>_<within-split index>. Seeds are derived from the root seed, split code, within-split index, and retry number. Family ordering is fixed per split. Increasing the training count retains existing training flights and leaves validation, test, and benchmark flights unchanged when other settings are fixed.

## Saved arrays and units

- `time`: shared seconds, shape (steps+1,).
- `states`: shape (trajectories, steps+1, 13), ordered [x,y,z,qw,qx,qy,qz,vx,vy,vz,wx,wy,wz].
- Position and linear velocity are world-frame metres and metres/second; angular velocity is body-frame radians/second.
- Orientations are normalized scalar-first wxyz quaternions rotating body vectors to world coordinates.
- `controls`: actual applied [thrust, moment_x, moment_y, moment_z], shape (trajectories, steps, 4), in N and N m.
- `requested_controls` and `actuator_controls`: physical requests before clipping and raw MuJoCo actuator commands.
- `contacts`: shape (trajectories, steps), false for all accepted trajectories.
- `reference_positions` / `reference_yaw`: desired positions and headings at the state sample times.
- `trajectory_ids`, `families`, `split`: one stable ID, family, and split per trajectory.
- `metadata_json`: schema version, model revision, physical and controller settings, randomization ranges, per-flight initial states, path parameters, seeds, and failed-attempt records.

The states at k and k+1 pair with controls[k], held across that prediction interval. `dataset.samples('train')` exposes those one-step records while keeping trajectory and step IDs. No residual target is calculated here; that requires the independent physics predictor. Data remain in physical units. Fit later feature/target normalizers using only the train split, then freeze them for validation, testing, and the benchmark.

## Artifacts

- `dataset.npz`: the main train/validation/test dataset; load with drone_sim.dataset.load_dataset.
- `benchmark_dataset.npz`: the held-out-family dataset, labeled benchmark only.
- `trajectory_manifest.csv`: stable IDs, seeds, split/family labels, lengths, tracking errors, and saturation rates.
- `coverage_summary.json`: per-split trajectory/family counts, physical state/control ranges, and saturation fractions.
- `plots/state_coverage.png`, `plots/control_coverage.png`, `plots/trajectory_family_counts.png`: coverage diagnostics.
- `plots/path_comparison_summary.png`: preselected ordinary test examples and one benchmark flight.
- `flights/`: preselected examples in the existing playback-compatible single-flight format.
- `failed_trajectories.json`: deterministic rejected attempts, reasons, and reproduction settings.
- `run_metadata.json`: configuration, code revision/dirty state, source hashes, model settings, and summaries.

## Reproduction and inspection

```powershell
python scripts/drone/generate_dataset.py
```

For example, inspect an exported flight using:

```powershell
python scripts/drone/playback_flight.py runs/Drone/drone_run_2/flights/test_000003.npz --paused
```

## Interpretation and limitations

Coverage plots show what this dataset contains, not proof of uniform coverage of all possible drone motion. All flights use one mass/inertia configuration, still air, the same controller, and conservative flight envelopes. Yaw/position changes add geometric variety; path scale, cycle count, and initial disturbances vary the actual motion. Retrying failed flights conditions the dataset on valid flight; inspect rejected attempts when comparing datasets.

Tracking errors compare the simulated vehicle with the controller reference. They are not learned-model errors. There is no automatic fidelity threshold and no NN training in this run. The next model component will predict basic rigid-body motion so one-step physics errors can be formed.

## Changes from earlier drone work

Earlier outputs contained six individual demonstration flights. This run adds multiple seeded trajectories, stable splits, a separate family benchmark, validated save/load, transition access, and coverage diagnostics. Drone_Plan.md and README.md were not edited during this implementation.

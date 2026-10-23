"""Readable phase-5 results, theory, artifact contracts, and reproduction."""

from pathlib import Path


def write_phase_report(output: Path, metadata: dict, summary: dict, training: dict | None = None) -> None:
    config = metadata["training_config"]
    lines = ["# Phase 5 Data: Training and Recursive Evaluation", "", "## Results", "",
             "The physics-residual NN is trained and evaluated against held-out MuJoCo flights. "
             "The checkpoint used for these predictions is recorded below. The standard training entry point "
             "selects its best checkpoint using validation standardized residual MSE. "
             "Physics-only and hybrid predictions replay identical recorded applied controls. "
             "Recursive prediction uses simulator truth only for initialization and later scoring; there are no truth refreshes.", "",
             f"- Architecture: {config['hidden_layers']} hidden layers, {config['hidden_size']} neurons per hidden layer, Tanh, 14 inputs and 12 outputs.",
             f"- Optimizer: Adam; learning rate {config['learning_rate']:g}; batch size {config['batch_size']}; seed {config['seed']}.",
             f"- Selected checkpoint update: {metadata['checkpoint']['optimizer_updates']:,}.",
             f"- Checkpoint source: {metadata['checkpoint']['path']}; selection: {metadata['checkpoint']['selection']}.",
             f"- Dataset: {metadata['dataset_counts']}; separate held-out-family benchmark: {metadata['benchmark_count']} flights.",
             "- Each default flight is 10 s, with 1,000 predictions at 0.01 s; the physics predictor uses five 0.002 s RK4 substeps.", ""]
    if training is not None:
        lines += [f"- Requested optimizer updates: {training.get('requested_optimizer_updates', training['optimizer_updates']):,}.",
                  f"- Actual optimizer updates: **{training['optimizer_updates']:,}**.",
                  f"- Epochs started/completed: {training['epochs_started']} / {training['completed_epochs']}; "
                  f"fractional epoch progress: {training['epoch_fraction']:.6g}.",
                  f"- Samples processed: {training['samples_processed']:,}; {training['batches_per_complete_epoch']} batches per complete epoch.",
                  f"- Training runtime: {training['training_seconds']:.3f} s, excluding {training['preparation_seconds']:.3f} s preparation; "
                  f"{training['device']}, {training['num_threads']} PyTorch thread(s).",
                  f"- Trainable parameters: {training['trainable_parameters']:,}.",
                  f"- Initial validation residual MSE: {training['initial_validation_residual_mse']:.9g}; "
                  f"best: **{training['best_validation_residual_mse']:.9g}** at update {training['best_update']:,}.",
                  f"- Final full-training residual MSE: {training['final_train_residual_mse']:.9g}; "
                  f"final validation residual MSE: {training['final_validation_residual_mse']:.9g}.", ""]
    else:
        lines += ["This directory is an evaluation-only repeat of an existing checkpoint; no retraining was performed. "
                  "Its recorded update count describes the loaded checkpoint, not a new optimizer run.", ""]
    for split, modes in summary.items():
        lines += [f"## {split.capitalize()} trajectory results", ""]
        for mode, predictors in modes.items():
            lines += [f"### {mode.replace('_', ' ').capitalize()}", ""]
            for name, values in predictors.items():
                lines += [f"- **{name}**, {values['trajectories']} flights: mean position MAE "
                          f"**{values['mean_position_mae_m']:.9g} m**, std {values['std_position_mae_m']:.9g} m; "
                          f"mean orientation MAE **{values['mean_orientation_mae_rad']:.9g} rad "
                          f"({values['mean_orientation_mae_deg']:.9g} deg)**, std {values['std_orientation_mae_rad']:.9g} rad.",
                          f"  Mean position/orientation RMSE: {values['mean_position_rmse_m']:.9g} m / "
                          f"{values['mean_orientation_rmse_rad']:.9g} rad. Mean final/max position error: "
                          f"{values['mean_final_position_error_m']:.9g} / {values['mean_maximum_position_error_m']:.9g} m.",
                          f"  Mean linear velocity MAE/RMSE: {values['mean_linear_velocity_mae_m_s']:.9g} / "
                          f"{values['mean_linear_velocity_rmse_m_s']:.9g} m/s; mean angular velocity MAE/RMSE: "
                          f"{values['mean_angular_velocity_mae_rad_s']:.9g} / {values['mean_angular_velocity_rmse_rad_s']:.9g} rad/s."]
            physics, hybrid = predictors["physics_only"], predictors["hybrid"]
            position = 100*(1-hybrid["mean_position_mae_m"]/physics["mean_position_mae_m"]) if physics["mean_position_mae_m"] else None
            angle = 100*(1-hybrid["mean_orientation_mae_rad"]/physics["mean_orientation_mae_rad"]) if physics["mean_orientation_mae_rad"] else None
            if position is not None and angle is not None:
                lines += ["", f"Reduction in mean MAE relative to physics-only: position **{position:.3f}%**, "
                          f"orientation **{angle:.3f}%**. A negative reduction indicates an increase in error.", ""]
    lines += ["## Training theory and implementation", "",
              "Training examples use the simulator's true current state, the actual applied wrench during that "
              "interval, and the simulator's next state. The independent rigid-body predictor provides the "
              "physics next state. The 12 targets are only its finite-step error: current-body-frame position/velocity "
              "differences, a right-composed orientation rotation vector in predicted-next body axes, and angular-velocity "
              "component differences. Phase 4 defines and verifies those transformations.", "",
              "The 14 inputs are body-frame linear velocity (3), angular velocity (3), body-frame gravity (3), "
              "applied thrust/body moments (4), and dt (1). Body-frame gravity is the world gravity vector expressed "
              "along the current drone axes, R(q).T @ g_world. Translational correction vectors rotate back using "
              "the current attitude; orientation is corrected by quaternion composition, never component subtraction.", "",
              "The loss is mean squared error across all 12 standardized residual coordinates. "
              "Each target coordinate is centered and scaled with training-only statistics, so the loss balances "
              "their observed variation rather than mixing metres, radians, and velocity units directly. "
              "Adam adjusts the NN weights from first- and second-moment estimates of minibatch gradients. "
              "Learning rate stays constant; no scheduler or early stopping changes the optimizer-update budget. "
              "The physics integrator is outside the autograd graph: only the correction MLP is optimized. "
              "See [PyTorch Adam](https://docs.pytorch.org/docs/2.14/generated/torch.optim.Adam.html).", "",
              "Every epoch shuffles all training transitions using a seeded independent torch.Generator. "
              "The final smaller batch of each epoch is retained. The requested optimizer-update budget is "
              "rounded upward to the next complete epoch, and the actual update count is recorded separately. "
              "Validation is measured at update 0, every configured interval (100 by default), and the final update "
              "without duplicating it. Each logged training and validation loss is a full-split sample/coordinate-weighted "
              "MSE at the current weights, not a running average of minibatch losses.", "",
              "The best checkpoint minimizes validation residual MSE, including initialization. The final checkpoint "
              "records the weights and optimizer state at the rounded final update count. They can differ. "
              "Neither test data nor the separate waypoint benchmark is requested by the training function. "
              "Held-out data are evaluated only after training and checkpoint selection. No setting was selected "
              "using the test results in this phase.", "",
              "Physics, raw residual subtraction, standardizer statistics, unstandardization, and state corrections "
              "use float64. Only standardized arrays and NN weights use float32. Nonconstant residual coordinates "
              "retain their actual small standard deviations; exactly constant columns use scale 1. "
              "This preserves the nanometre-scale one-step position residual instead of losing it in float32 state subtraction.", "",
              "## One-step versus recursive prediction", "",
              "One-step evaluation restarts each prediction from its true current state. Recursive evaluation "
              "initializes once and then feeds the previous predicted state into both the physics predictor and "
              "NN feature construction. Thus body-frame gravity, velocity, and correction transformations follow "
              "the predicted attitude. The recursive API accepts only initial states and applied-control arrays; "
              "it cannot read future true states. The controller generates reference data but is not rerun "
              "or given simulator truth while predicting. These are predictions conditional on known controls.", "",
              "Training minimizes local residual error. A lower one-step residual MSE does not guarantee a "
              "proportional reduction in recursive drift: corrections change subsequent states, and small biased "
              "errors can accumulate. Interpret the path and error curves manually; no automatic fidelity threshold "
              "defines success. The benchmark evaluates new waypoint-family flights, separately from familiar-family tests.", "",
              "## Metric definitions", "",
              "Position MAE is the time-average Euclidean distance between predicted and true positions. "
              "Orientation MAE is the time-average shortest absolute rotation angle, reported in radians and degrees. "
              "RMSE is the square root of mean squared norm/angle. Linear and angular velocity metrics use vector "
              "norms of world-linear and body-angular state-component errors. The exact initial state is excluded "
              "from means and maxima. Final position error is at the last timestamp. "
              "Every overall mean gives each trajectory equal weight; standard deviations are across trajectory "
              "metrics with ddof=0. Splits, prediction modes, and predictors remain separate in every summary.", "",
              "## Files and artifacts", "",
              "- `src/model_drone_residual/training.py`: configurable complete-epoch training, train-only scaling, full-split validation, best/final checkpoint snapshots.",
              "- `src/model_drone_residual/evaluation.py`: recursive hybrid inference, held-out comparisons, saved predictions and physical metrics.",
              "- `scripts/model_drone_residual/train_drone_residual.py`: train, select, save, and evaluate this phase.",
              "- `scripts/model_drone_residual/evaluate_drone_rollout.py`: repeat evaluation of a saved checkpoint without retraining.",
              "- `checkpoint_best.pt` / `checkpoint_final.pt`: model, standardizers, physics/timing contract, optimizer state, update/epoch/sample counters, seed, sampler/RNG states, configuration, losses, history, provenance.",
              "- `standardizers.json`: train-fitted statistics and fitting trajectory IDs/sample count.",
              "- `training_metrics.csv`, `training_summary.json`, `loss_curves.png`: full training/validation losses versus updates and actual training accounting.",
              "- `test_metrics.json`: all final test and benchmark summaries, separated by mode and predictor.",
              "- `one_step_metrics.csv` / `.json`, `rollout_metrics.csv` / `.json`: per-trajectory metrics and equal-weight summaries.",
              "- `comparison_metrics.csv`: split/mode/predictor summary rows, including mean position and orientation MAE and variability.",
              "- `predictions/<split>_<mode>.npz`: full truth/physics/hybrid traces, applied controls, time, IDs, families, checkpoint metadata.",
              "- `predictions/<trajectory_id>_hybrid_recursive.npz`: individual NN flight tracks compatible with the existing single-drone playback script.",
              "- `plots/<trajectory_id>_<mode>.png`: first saved flight of each family, chosen without reference to accuracy; large 3D path and smaller position/orientation angle errors only.",
              "- `run_metadata.json`: source/input hashes, revision/dirty state, configuration, checkpoint selection, runtime, simulation provenance, and completion status.", "",
              "Requested update counts are rounded upward to complete epochs; the last batch may contain fewer samples. "
              "Best-checkpoint selection still uses validation measurements and may select an earlier update. "
              "The checkpoints record sampler position and RNG state for reproducibility; automatic training resumption "
              "is not implemented in this phase. An evaluation-only repeat retains its source checkpoint and writes "
              "fresh evaluation artifacts; training artifacts stay in the source directory.", "",
              "## Reproduction", "", "From the repository root:", "", "```powershell", metadata["command"], "```", "",
              "Default training and independent evaluation commands:", "", "```powershell",
              r".\.venv\Scripts\python.exe scripts/model_drone_residual/train_drone_residual.py",
              r".\.venv\Scripts\python.exe scripts/model_drone_residual/evaluate_drone_rollout.py --checkpoint runs/Drone/phase_5/checkpoint_best.pt",
              "```", "", "For example, play a learned recursive test trajectory:", "", "```powershell",
              f"python scripts/drone/playback_flight.py {(output/'predictions/test_000000_hybrid_recursive.npz').as_posix()} --paused",
              "```", "",
              "Defaults read the fixed phase-2 archives. Training accepts `--updates`, `--batch-size`, "
              "`--learning-rate`, `--validation-interval`, `--seed`, `--hidden-size`, `--hidden-layers`, and `--threads`. "
              "Both entry points accept dataset/benchmark paths and an output root. Repeated executions preserve "
              "earlier results under `phase_5/repeat_N/`.", "",
              "## Assumptions and next work", "",
              "This is one seed with one fixed drone property configuration, still air, conservative contact-free "
              "flights, and recorded future controls. Broader seed, quantity, variety, update-count, and architecture "
              "comparisons remain phase 7. Refresh schedules remain phase 6; none are enabled or implemented here. "
              "The benchmark is reported separately and is not used for checkpoint selection.", "",
              "Drone_Plan.md, README.md, Runs Masterlist.md, and prior phase outputs were not edited. "
              "No commit was created.", ""]
    (output/"Phase 5 Data.md").write_text("\n".join(lines), encoding="utf-8")

"""Readable phase-6 results and definitions of before/after refresh scoring."""

from pathlib import Path
import numpy as np

from model_drone_residual.refresh_evaluation import PRIMARY_VIEW, POST_VIEW


def write_refresh_report(output: Path, metadata: dict, results: list[dict]) -> None:
    lines = ["# Phase 6 Data: Optional Truth Refreshes", "", "## Results and scope", "",
             "The existing phase-5 checkpoint is evaluated under reproducible full-state truth-refresh schedules. "
             "No training, weight updates, new dataset generation, or checkpoint reselection occurred. "
             "Both physics-only and physics+NN predictors replay the same recorded applied controls and receive "
             "the same truth at the same selected steps.", "",
             f"- Checkpoint: `{metadata['checkpoint']['path']}`, selected at optimizer update {metadata['checkpoint']['optimizer_updates']:,} in phase 5.",
             f"- Optimizer updates in this phase: **0**; checkpoint file, model weights, and standardizers verified unchanged.",
             f"- Prediction grid: {metadata['dt_s']:g} s; each flight has {metadata['num_steps']} transitions.",
             f"- Held-out counts: {metadata['held_out_counts']}.",
             f"- Schedule cases: {len(metadata['schedules'])}.",
             "- Default schedule: **no refresh**. The recorded `--sweep` command explicitly requests the interval comparison when used.", "",
             "**Primary errors are measured before any truth replacement at each prediction timestamp.** "
             "Secondary after-replacement metrics are saved separately. This prevents resets from making "
             "the predictor look artificially exact at refreshed samples.", ""]
    for split in dict.fromkeys(result["split"] for result in results):
        lines += [f"## {split.capitalize()} trajectories", "",
                  "All following means average the corresponding per-trajectory MAEs with equal flight weight. "
                  "Orientation is the shortest absolute rotation angle. The shared initial state is excluded.", ""]
        for result in (result for result in results if result["split"] == split):
            label, count = result["label"], result["schedule"]["refresh_count"]
            lines += [f"### {label}: {count} refreshes per trajectory", ""]
            for name in ("physics_only", "hybrid"):
                primary = result["summaries"][PRIMARY_VIEW][name]
                post = result["summaries"][POST_VIEW][name]
                drift = [row for row in result["drift_rows"] if row["predictor"] == name]
                lines += [f"- **{name}**, forecast before replacement: mean position MAE "
                          f"**{primary['mean_position_mae_m']:.9g} m**, std {primary['std_position_mae_m']:.9g} m; "
                          f"mean orientation MAE **{primary['mean_orientation_mae_rad']:.9g} rad "
                          f"({primary['mean_orientation_mae_deg']:.9g} deg)**, std {primary['std_orientation_mae_rad']:.9g} rad.",
                          f"  Mean final forecast position error: {primary['mean_final_position_error_m']:.9g} m; "
                          f"mean maximum position error: {primary['mean_maximum_position_error_m']:.9g} m.",
                          f"  After-replacement mean position/orientation MAE: {post['mean_position_mae_m']:.9g} m / "
                          f"{post['mean_orientation_mae_rad']:.9g} rad; mean final after-replacement position error "
                          f"{post['mean_final_position_error_m']:.9g} m."]
                if count:
                    lines += [f"  Mean error immediately before refresh events: "
                              f"{np.mean([row['pre_refresh_position_mae_m'] for row in drift]):.9g} m / "
                              f"{np.mean([row['pre_refresh_orientation_mae_rad'] for row in drift]):.9g} rad."]
                lines += [f"  Mean segment endpoint growth per second: "
                          f"{np.mean([row['mean_segment_position_growth_per_s'] for row in drift]):.9g} m/s / "
                          f"{np.mean([row['mean_segment_orientation_growth_per_s'] for row in drift]):.9g} rad/s."]
            lines.append("")
    lines += ["## Refresh timing and theory", "",
              "A schedule selects state indices, not control indices. Step k corresponds to t=k*dt. "
              "The transition from k-1 to k first uses the recorded control u[k-1] and the previous "
              "post-replacement state. Its forecast is saved before any reset:", "",
              "$$\\tilde x_k=F(\\hat x^+_{k-1},u_{k-1},\\Delta t)$$", "",
              "$$\\hat x^+_k=\\begin{cases}x^{sim}_k,&k\\in\\mathcal R\\\\\\tilde x_k,&k\\notin\\mathcal R\\end{cases}$$", "",
              "For the hybrid predictor, F is the independent physics step followed by the learned residual "
              "composition from phases 4 and 5. A refresh replaces position, scalar-first quaternion orientation, "
              "world-frame linear velocity, and body-frame angular velocity together. The next prediction "
              "constructs NN features from that replaced state. Replacing position alone would leave velocity "
              "and attitude drift in the continuing rollout; that partial-reset behavior is not used here.", "",
              "A refresh is state replacement, not retraining or an NN weight update. There is no online controller "
              "feedback, noisy measurement model, partial observation filter, or interpolation. The truth provider "
              "returns the saved simulator state only when the core rollout requests a selected step. "
              "With no schedule, it is never called. The original physics and hybrid no-refresh rollout interfaces "
              "remain unchanged and accept no future truth.", "",
              "## Supported schedule contracts", "",
              "- `RefreshSchedule()` disables refreshes by default.",
              "- `RefreshSchedule(interval_steps=100)` refreshes at 100, 200, ... within the horizon.",
              "- `RefreshSchedule(steps=(50, 200, 700))` uses those explicit state indices, sorted chronologically.",
              "- `RefreshSchedule(interval_seconds=1.0)` is the grid-aligned time equivalent of every 100 steps at dt=0.01 s.",
              "- `RefreshSchedule(times=(0.5, 2.0, 7.0))` uses explicit times relative to initialization.", "",
              "Choose one schedule form. Times must align with the prediction grid; off-grid inputs are rejected, "
              "not silently rounded. Explicit steps outside the flight horizon, duplicates, and nonpositive "
              "steps/times are rejected. Step 0 is initialization and is not counted as a refresh. A periodic "
              "interval longer than the horizon produces no events. Final-step events are allowed and counted: "
              "for 1,000 transitions, every 500 steps produces events at 500 and 1,000. The final event changes "
              "the after-replacement state but cannot change the forecast already made at step 1,000.", "",
              "## Why both metric views are retained", "",
              "`forecast_before_replacement` scores the saved local forecast at every timestamp. At refresh times "
              "this is the error immediately before injecting truth; between refreshes it is the ordinary "
              "recursive error. This is the primary view in the report and frequency plots.", "",
              "`state_after_replacement` scores the state that is actually used to continue the rollout. It has "
              "zero error at exact full-state reset times by construction. With refresh every step it becomes "
              "perfect at every scored timestamp, so it is not used to claim model accuracy. The corresponding "
              "before-replacement forecast still has the model's ordinary one-step error. No refresh reproduces "
              "the phase-5 recursive results in both views.", "",
              "Position MAE is time-average Euclidean distance; orientation MAE is time-average shortest rotation "
              "angle in radians/degrees. RMSE, final/maximum position error, linear/angular velocity MAE/RMSE, "
              "and per-trajectory variability are saved for both views. Means use equal flight weights and "
              "standard deviations across trajectory metrics use ddof=0. Test and waypoint benchmark stay separate.", "",
              "## Pre-refresh events and growth segments", "",
              "Each refresh has a separate full-state before snapshot and corrected snapshot. Event CSVs report "
              "the position, orientation, and velocity errors immediately before replacement, plus the post-reset "
              "position/orientation error. Each segment begins at initialization or a corrected refresh state "
              "and ends at the next refresh forecast or the final forecast. A trailing unrefreshed segment is "
              "retained; a final-step refresh does not add an empty segment.", "",
              "Segment rows report the initial post-reset error, endpoint forecast error, maximum/time-mean "
              "forecast errors, and endpoint-minus-start growth divided by elapsed seconds. That growth rate "
              "is an interval-average endpoint measure, not an instantaneous derivative or a claim that error "
              "grows monotonically. Per-flight drift rows average their segments equally; the readable report "
              "then averages those rows equally across trajectories.", "",
              "## Plots and playback", "",
              "Each flight-comparison plot retains the large 3D path plus position and orientation angle error "
              "over time. The 3D curves show continuing post-replacement paths, with open predicted-point markers "
              "immediately before sampled refresh events and green marks at truth replacement locations. "
              "The error curves always show before-replacement forecasts. All refresh timestamps appear as green "
              "rug ticks along the bottom of the error plots; sparse schedules also get vertical event lines. "
              "For dense schedules, up to 40 3D event markers are sampled and that count is disclosed in the legend. "
              "Full event records are never subsampled in saved data.", "",
              "Frequency figures compare mean position/orientation MAE against periodic interval and actual "
              "refresh count, separately for test and benchmark. Interval cases are categorical so 'None' has "
              "no invented finite duration. Count plots retain zero for no refresh using a symlog axis. "
              "No automatic path-fidelity threshold or optimal interval is selected; interpret these tradeoffs manually.", "",
              "Combined prediction archives use `physics_states` and `hybrid_states` for the post-replacement "
              "paths used in playback. Their `*_forecast_states` arrays preserve every before-replacement forecast. "
              "Existing blue/orange comparison playback loads these files without a rendering change. "
              "Jumping back to truth in playback is an explicit reset, not an improvement made by the NN.", "",
              "## Files and artifacts", "",
              "- `src/model_drone_residual/refresh.py`: schedule validation/resolution, refresh-aware rollout, before/after event snapshots.",
              "- `src/model_drone_residual/refresh_evaluation.py`: shared-schedule physics/hybrid comparisons, both metric views, refresh events and drift segments.",
              "- `scripts/model_drone_residual/evaluate_drone_refresh.py`: no-refresh, custom schedule, and fixed-checkpoint sweep entry point.",
              "- `rollout_metrics.csv` / `.json`, `test_metrics.json`: per-trajectory physical errors and equal-weight means, separated by schedule/split/predictor/metric view.",
              "- `comparison_metrics.csv`: summary rows including interval, event count, mean position/orientation MAEs, and standard deviations.",
              "- `drift_metrics.csv`: per-trajectory pre-refresh errors and segment-growth summaries.",
              "- `<schedule>/refresh_schedule.json`: requested configuration, exact resolved steps/times, final-step semantics.",
              "- `<schedule>/predictions/<split>_recursive.npz`: truth, applied controls, IDs, times, pre/post full traces, separate pre-refresh/corrected snapshots, refresh steps/times, checkpoint metadata.",
              "- `<schedule>/refresh_events_<split>.csv`, `segments_<split>.csv`, `drift_metrics_<split>.csv`: full event/segment diagnostics.",
              "- `<schedule>/trajectory_metrics_<split>.csv`, `metrics_<split>.json`: individual schedule results for both metric views.",
              "- `<schedule>/plots/`: preselected first trajectory per family, using the existing large-3D-plus-two-errors layout.",
              "- `plots/refresh_frequency_test.png`, `refresh_frequency_benchmark.png`: primary errors versus interval and count.",
              "- `run_metadata.json`: exact command, immutable source/checkpoint/input hashes, model provenance, resolved schedules, completion status, runtime, and zero weight updates.", "",
              "## Reproduction", "", "Actual command for this directory:", "", "```powershell", metadata["command"], "```", "",
              "From the repository root, default no-refresh evaluation and the initial nine-case sweep:", "", "```powershell",
              r".\.venv\Scripts\python.exe scripts/model_drone_residual/evaluate_drone_refresh.py",
              r".\.venv\Scripts\python.exe scripts/model_drone_residual/evaluate_drone_refresh.py --sweep", "```", "",
              "Custom schedule examples:", "", "```powershell",
              r"python scripts/model_drone_residual/evaluate_drone_refresh.py --refresh-every 100",
              r"python scripts/model_drone_residual/evaluate_drone_refresh.py --refresh-steps 50 200 700",
              r"python scripts/model_drone_residual/evaluate_drone_refresh.py --refresh-every-seconds 1.0",
              r"python scripts/model_drone_residual/evaluate_drone_refresh.py --refresh-times 0.5 2.0 7.0", "```", "",
              "Example comparison playback (when the sweep includes this directory):", "", "```powershell",
              f"python scripts/drone/playback_flight.py {(output/'every_100_steps/predictions/test_recursive.npz').as_posix()} --trajectory-id test_000000 --compare both --paused", "```", "",
              "Default inputs are the fixed phase-2 archives and phase-5 best checkpoint. "
              "Use `--dataset`, `--benchmark`, `--checkpoint`, `--output-root`, and `--threads` to change paths/runtime. "
              "Outputs go under phase_6 and then repeat_N subdirectories, preserving previous results.", "",
              "## Assumptions and next work", "",
              "Refreshes use exact simulator full states. Real sensors, noisy or partial observations, estimation "
              "filters, communication latency, wind, contact, and altered drone properties are outside this phase. "
              "The results are for one previously trained seed and checkpoint; phase 7 remains the controlled "
              "learning experiment stage. Fixed weights and held-out trajectories allow refresh schedules to be "
              "compared without retraining or changing the reference controller.", "",
              "Drone_Plan.md, README.md, Runs Masterlist.md, phase-5 checkpoint, and prior phase outputs were not edited. "
              "No commit was created.", ""]
    (output/"Phase 6 Data.md").write_text("\n".join(lines), encoding="utf-8")

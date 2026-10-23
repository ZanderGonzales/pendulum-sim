"""Held-out truth-refresh comparisons, before/after metrics, and drift segments."""

import csv
import json
from pathlib import Path

import numpy as np

from drone_sim.evaluation import state_errors, summarize_metrics, trajectory_metrics
from drone_sim.physics import RigidBodyParameters
from drone_sim.types import SimulationConfig
from model_drone_residual.refresh import RefreshSchedule, rollout_with_refresh


PRIMARY_VIEW = "forecast_before_replacement"
POST_VIEW = "state_after_replacement"
EVENT_FIELDS = ("schedule", "split", "trajectory_id", "predictor", "step", "time_s",
                "pre_position_error_m", "pre_orientation_error_rad", "pre_orientation_error_deg",
                "pre_linear_velocity_error_m_s", "pre_angular_velocity_error_rad_s",
                "post_position_error_m", "post_orientation_error_rad")
SEGMENT_FIELDS = ("schedule", "split", "trajectory_id", "predictor", "segment", "start_step", "end_step",
                  "duration_s", "ends_in_refresh", "start_post_position_error_m", "start_post_orientation_error_rad",
                  "end_forecast_position_error_m", "end_forecast_orientation_error_rad", "end_forecast_orientation_error_deg",
                  "position_error_growth_m", "orientation_error_growth_rad", "position_growth_per_s", "orientation_growth_per_s",
                  "mean_position_error_m", "maximum_position_error_m", "mean_orientation_error_rad", "maximum_orientation_error_rad")


def write_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, allow_nan=False)+"\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict], fields=None) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(fields) if fields else list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def drift_records(result, truth, *, identifiers, split, predictor, label, dt):
    """Event endpoint errors and error growth since the preceding full-state reset."""
    forecast_errors, post_errors = state_errors(result.forecast_states, truth), state_errors(result.states, truth)
    events, segments, trajectory_drift = [], [], []
    count, final = len(result.refresh_steps), truth.shape[1]-1
    boundaries = [0, *result.refresh_steps.tolist()]
    if boundaries[-1] != final:
        boundaries.append(final)
    for local, identifier in enumerate(identifiers):
        identity = {"schedule": label, "split": split, "trajectory_id": str(identifier), "predictor": predictor}
        for step in result.refresh_steps:
            step = int(step)
            events.append({**identity, "step": step, "time_s": step*dt,
                "pre_position_error_m": float(forecast_errors["position_m"][local, step]),
                "pre_orientation_error_rad": float(forecast_errors["orientation_rad"][local, step]),
                "pre_orientation_error_deg": float(np.degrees(forecast_errors["orientation_rad"][local, step])),
                "pre_linear_velocity_error_m_s": float(forecast_errors["linear_velocity_m_s"][local, step]),
                "pre_angular_velocity_error_rad_s": float(forecast_errors["angular_velocity_rad_s"][local, step]),
                "post_position_error_m": float(post_errors["position_m"][local, step]),
                "post_orientation_error_rad": float(post_errors["orientation_rad"][local, step])})
        local_segments = []
        event_set = set(result.refresh_steps.tolist())
        for index, (start, end) in enumerate(zip(boundaries[:-1], boundaries[1:]), 1):
            duration = (end-start)*dt
            position = forecast_errors["position_m"][local, start+1:end+1]
            orientation = forecast_errors["orientation_rad"][local, start+1:end+1]
            start_p, start_q = post_errors["position_m"][local, start], post_errors["orientation_rad"][local, start]
            segment = {**identity, "segment": index, "start_step": start, "end_step": end, "duration_s": duration,
                "ends_in_refresh": end in event_set,
                "start_post_position_error_m": float(start_p), "start_post_orientation_error_rad": float(start_q),
                "end_forecast_position_error_m": float(position[-1]), "end_forecast_orientation_error_rad": float(orientation[-1]),
                "end_forecast_orientation_error_deg": float(np.degrees(orientation[-1])),
                "position_error_growth_m": float(position[-1]-start_p), "orientation_error_growth_rad": float(orientation[-1]-start_q),
                "position_growth_per_s": float((position[-1]-start_p)/duration), "orientation_growth_per_s": float((orientation[-1]-start_q)/duration),
                "mean_position_error_m": float(position.mean()), "maximum_position_error_m": float(position.max()),
                "mean_orientation_error_rad": float(orientation.mean()), "maximum_orientation_error_rad": float(orientation.max())}
            local_segments.append(segment)
        segments += local_segments
        trajectory_drift.append({**identity, "refresh_count": count, "segment_count": len(local_segments),
            "pre_refresh_position_mae_m": float(forecast_errors["position_m"][local, result.refresh_steps].mean()) if count else None,
            "pre_refresh_orientation_mae_rad": float(forecast_errors["orientation_rad"][local, result.refresh_steps].mean()) if count else None,
            "maximum_pre_refresh_position_error_m": float(forecast_errors["position_m"][local, result.refresh_steps].max()) if count else None,
            "maximum_pre_refresh_orientation_error_rad": float(forecast_errors["orientation_rad"][local, result.refresh_steps].max()) if count else None,
            "mean_segment_endpoint_position_error_m": float(np.mean([row["end_forecast_position_error_m"] for row in local_segments])),
            "mean_segment_endpoint_orientation_error_rad": float(np.mean([row["end_forecast_orientation_error_rad"] for row in local_segments])),
            "mean_segment_position_growth_per_s": float(np.mean([row["position_growth_per_s"] for row in local_segments])),
            "mean_segment_orientation_growth_per_s": float(np.mean([row["orientation_growth_per_s"] for row in local_segments]))})
    return events, segments, trajectory_drift


def evaluate_refresh_schedule(predictor, dataset, output_dir: str | Path, *, split: str = "test",
                              schedule: RefreshSchedule = RefreshSchedule(), label: str = "no_refresh",
                              checkpoint_info: dict | None = None, save_plots: bool = True) -> dict:
    if split not in ("test", "benchmark"):
        raise ValueError("refresh evaluation requires a test or benchmark split")
    settings = dataset.metadata["simulation"]
    if (predictor.physics.parameters != RigidBodyParameters.from_metadata(settings) or
            predictor.physics.config != SimulationConfig(**settings["simulation_config"])):
        raise ValueError("refresh evaluation physics and timing must match the dataset")
    indices = np.flatnonzero(dataset.split == split)
    if not len(indices):
        raise ValueError(f"dataset has no {split} trajectories")
    controls = dataset.controls[indices].copy()
    initial = dataset.states[indices, 0].copy()
    dt = predictor.physics.config.dt
    resolved = schedule.resolve(controls.shape[1], dt)

    def truth_at(step):
        return dataset.states[indices, step].copy()

    outputs = {"physics_only": rollout_with_refresh(predictor.physics, initial, controls, schedule=schedule, truth_provider=truth_at),
               "hybrid": rollout_with_refresh(predictor, initial, controls, schedule=schedule, truth_provider=truth_at)}
    truth = dataset.states[indices]
    identifiers, families = dataset.trajectory_ids[indices], dataset.families[indices]
    output = Path(output_dir)
    (output/"predictions").mkdir(parents=True, exist_ok=True)
    if save_plots:
        (output/"plots").mkdir(exist_ok=True)
    refresh_metadata = schedule.metadata(controls.shape[1], dt)
    metadata = {"mode": "recursive_with_truth_refresh" if resolved else "recursive", "split": split,
                "truth_refresh": refresh_metadata if resolved else None, "refresh_schedule": refresh_metadata,
                "primary_metric_view": PRIMARY_VIEW, "playback_state_view": POST_VIEW,
                "checkpoint": checkpoint_info or {}, "schedule_label": label}
    arrays = {"time": dataset.time, "controls": controls, "trajectory_ids": identifiers, "families": families,
              "truth_states": truth, "refresh_steps": np.asarray(resolved, dtype=np.int64),
              "refresh_times": np.asarray(resolved)*dt, "metadata_json": json.dumps(metadata)}
    for name, result in outputs.items():
        prefix = "physics" if name == "physics_only" else "hybrid"
        arrays[f"{prefix}_states"] = result.states
        arrays[f"{prefix}_forecast_states"] = result.forecast_states
        arrays[f"{prefix}_pre_refresh_states"] = result.pre_refresh_states
        arrays[f"{prefix}_corrected_refresh_states"] = result.corrected_refresh_states
    np.savez_compressed(output/f"predictions/{split}_recursive.npz", **arrays)
    rows, summaries, events, segments, drift = [], {}, [], [], []
    for view, attribute in ((PRIMARY_VIEW, "forecast_states"), (POST_VIEW, "states")):
        summaries[view] = {}
        for name, result in outputs.items():
            values = [trajectory_metrics(predicted, actual) for predicted, actual in zip(getattr(result, attribute), truth)]
            rows += [{"schedule": label, "split": split, "trajectory_id": str(identifiers[i]), "family": str(families[i]),
                      "predictor": name, "metric_view": view, "refresh_count": len(resolved), **row} for i, row in enumerate(values)]
            summaries[view][name] = summarize_metrics(values)
    for name, result in outputs.items():
        e, s, d = drift_records(result, truth, identifiers=identifiers, split=split, predictor=name, label=label, dt=dt)
        events += e
        segments += s
        drift += d
    write_csv(output/f"refresh_events_{split}.csv", events, EVENT_FIELDS)
    write_csv(output/f"segments_{split}.csv", segments, SEGMENT_FIELDS)
    write_csv(output/f"trajectory_metrics_{split}.csv", rows)
    write_csv(output/f"drift_metrics_{split}.csv", drift)
    write_json(output/f"metrics_{split}.json", summaries)
    write_json(output/"refresh_schedule.json", refresh_metadata)
    examples = []
    if save_plots:
        from drone_sim.plotting import plot_prediction_comparison
        for family in dict.fromkeys(families.tolist()):
            local = int(np.flatnonzero(families == family)[0])
            filename = f"{identifiers[local]}_recursive.png"
            plot_prediction_comparison(dataset.time, truth[local],
                {"Physics only": outputs["physics_only"].states[local], "Physics + NN": outputs["hybrid"].states[local]},
                output/"plots"/filename, f"{split} | {family} | {label}\nError measured before any truth replacement",
                refresh_steps=np.asarray(resolved, dtype=np.int64),
                forecast_predictions={"Physics only": outputs["physics_only"].forecast_states[local], "Physics + NN": outputs["hybrid"].forecast_states[local]})
            examples.append((output/"plots"/filename).as_posix())
    return {"label": label, "split": split, "schedule": refresh_metadata, "summaries": summaries,
            "trajectory_rows": rows, "drift_rows": drift, "refresh_events": len(events), "segments": len(segments), "plots": examples}


def save_refresh_summaries(results: list[dict], output: Path) -> dict:
    rows = [row for result in results for row in result["trajectory_rows"]]
    drift = [row for result in results for row in result["drift_rows"]]
    summary = {}
    comparison = []
    for result in results:
        label, split, metadata = result["label"], result["split"], result["schedule"]
        summary.setdefault(label, {})[split] = result["summaries"]
        requested = metadata["requested"]
        interval = requested["interval_steps"]
        if interval is None and requested["interval_seconds"] is not None:
            interval = round(requested["interval_seconds"]/metadata["dt_s"])
        for view, predictors in result["summaries"].items():
            comparison += [{"schedule": label, "split": split, "metric_view": view, "predictor": name,
                            "refresh_interval_steps": interval, "refresh_interval_s": interval*metadata["dt_s"] if interval else None,
                            "refresh_count": metadata["refresh_count"], **values} for name, values in predictors.items()]
    write_csv(output/"rollout_metrics.csv", rows)
    write_json(output/"rollout_metrics.json", summary)
    write_json(output/"test_metrics.json", summary)
    write_csv(output/"comparison_metrics.csv", comparison)
    write_csv(output/"drift_metrics.csv", drift)
    return summary

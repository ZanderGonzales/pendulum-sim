"""Phase 6: optional exact full-state truth refreshes, disabled unless requested.

Use --sweep for no refresh and every 1,5,10,25,50,100,200,500 prediction steps.
The same trained checkpoint and applied controls are used without retraining.
"""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

import torch

from drone_sim import load_dataset
from drone_sim.artifacts import next_phase
from model_drone_residual import RefreshSchedule, load_checkpoint
from model_drone_residual.refresh_evaluation import (PRIMARY_VIEW, evaluate_refresh_schedule,
                                                     save_refresh_summaries, write_json)
from model_drone_residual.refresh_plotting import plot_refresh_frequency
from model_drone_residual.refresh_reporting import write_refresh_report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", type=Path, default=Path("runs/Drone/phase_5/checkpoint_best.pt"))
    parser.add_argument("--dataset", type=Path, default=Path("runs/Drone/phase_2/dataset.npz"))
    parser.add_argument("--benchmark", type=Path, default=Path("runs/Drone/phase_2/benchmark_dataset.npz"))
    parser.add_argument("--output-root", type=Path, default=Path("runs/Drone"))
    parser.add_argument("--threads", type=int, default=1)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--sweep", action="store_true")
    group.add_argument("--refresh-every", "--refresh-every-steps", dest="refresh_every", type=int)
    group.add_argument("--refresh-steps", type=int, nargs="+")
    group.add_argument("--refresh-every-seconds", type=float)
    group.add_argument("--refresh-times", type=float, nargs="+")
    args = parser.parse_args()
    if args.threads < 1:
        parser.error("threads must be positive")
    torch.set_num_threads(args.threads)
    predictor, checkpoint = load_checkpoint(args.checkpoint)
    if checkpoint.get("checkpoint_kind") not in ("best", "final") or "training_run_summary" not in checkpoint:
        parser.error("provide a best/final checkpoint from a completed phase-5 training run")
    main_data, benchmark = load_dataset(args.dataset), load_dataset(args.benchmark)
    if set(main_data.split.tolist()) != {"train", "validation", "test"} or set(benchmark.split.tolist()) != {"benchmark"}:
        parser.error("provide a main train/validation/test archive and separate benchmark archive")
    if (main_data.metadata["simulation"] != benchmark.metadata["simulation"] or
            main_data.metadata["held_out_family"] != benchmark.metadata["held_out_family"] or
            main_data.metadata["config"]["seed"] != benchmark.metadata["config"]["seed"]):
        parser.error("main and benchmark simulator settings, root seed, and held-out family must match")
    dt, num_steps = predictor.physics.config.dt, main_data.controls.shape[1]
    try:
        if args.sweep:
            schedules = [("no_refresh", RefreshSchedule())] + [(f"every_{value}_steps", RefreshSchedule(interval_steps=value))
                          for value in (1, 5, 10, 25, 50, 100, 200, 500)]
        else:
            schedule = RefreshSchedule(interval_steps=args.refresh_every, steps=tuple(args.refresh_steps or ()),
                        interval_seconds=args.refresh_every_seconds, times=tuple(args.refresh_times or ()))
            interval = schedule.interval_steps
            if interval is None and schedule.interval_seconds is not None:
                schedule.resolve(num_steps, dt)
                interval = round(schedule.interval_seconds/dt)
            label = f"every_{interval}_steps" if interval is not None else "explicit_schedule" if schedule.steps or schedule.times else "no_refresh"
            schedules = [(label, schedule)]
        for _, schedule in schedules:
            schedule.resolve(num_steps, dt)
    except ValueError as error:
        parser.error(str(error))
    root = Path(__file__).resolve().parents[2]
    sources = sorted((root/"src/drone_sim").glob("*.py")) + sorted((root/"src/model_drone_residual").glob("*.py")) + [Path(__file__).resolve()]
    revision = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True, check=False)
    dirty = subprocess.run(["git", "status", "--porcelain"], cwd=root, capture_output=True, text=True, check=False)
    checkpoint_hash = hashlib.sha256(args.checkpoint.read_bytes()).hexdigest()
    info = {"path": args.checkpoint.as_posix(), "sha256": checkpoint_hash,
            "optimizer_updates": checkpoint["optimizer_updates"], "training_run_updates": checkpoint["training_run_summary"]["optimizer_updates"]}
    weights = {name: value.detach().cpu().clone() for name, value in predictor.model.state_dict().items()}
    frozen_statistics = json.dumps(predictor.standardizers.to_dict(), sort_keys=True)
    output, _ = next_phase(args.output_root, 6)
    metadata = {"phase": 6, "status": "evaluating", "optimizer_updates_this_phase": 0,
                "command": subprocess.list2cmdline(["python", "scripts/model_drone_residual/evaluate_drone_refresh.py", *sys.argv[1:]]),
                "checkpoint": info, "dt_s": dt, "num_steps": num_steps,
                "held_out_counts": {"test": int((main_data.split == "test").sum()), "benchmark": len(benchmark.states)},
                "reference_simulation": main_data.metadata["simulation"], "threads": args.threads, "torch_version": str(torch.__version__),
                "inputs": {label: {"path": path.as_posix(), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
                           for label, path in (("main", args.dataset), ("benchmark", args.benchmark))},
                "source_sha256": {path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest() for path in sources},
                "code_revision": revision.stdout.strip(), "working_tree_dirty": bool(dirty.stdout.strip()),
                "schedules": [{"label": label, **schedule.metadata(num_steps, dt)} for label, schedule in schedules],
                "primary_metric_view": PRIMARY_VIEW, "completed_schedule_splits": []}
    write_json(output/"run_metadata.json", metadata)
    print(f"Evaluating {len(schedules)} refresh schedule(s) into {output}; NN weights fixed.", flush=True)
    started, results = time.perf_counter(), []
    try:
        for label, schedule in schedules:
            for split, data in (("test", main_data), ("benchmark", benchmark)):
                result = evaluate_refresh_schedule(predictor, data, output/label, split=split, schedule=schedule,
                                                   label=label, checkpoint_info=info)
                results.append(result)
                metadata["completed_schedule_splits"].append({"schedule": label, "split": split,
                    "refresh_count_per_trajectory": result["schedule"]["refresh_count"], "elapsed_seconds": time.perf_counter()-started})
                write_json(output/"run_metadata.json", metadata)
                print(f"{label} | {split}: {result['schedule']['refresh_count']} refreshes/flight; "
                      f"hybrid forecast position MAE={result['summaries'][PRIMARY_VIEW]['hybrid']['mean_position_mae_m']:.6g} m", flush=True)
            save_refresh_summaries(results, output)
        plot_refresh_frequency(results, output/"plots")
        assert all(torch.equal(value.detach().cpu(), weights[name]) for name, value in predictor.model.state_dict().items()), "NN weights changed"
        assert json.dumps(predictor.standardizers.to_dict(), sort_keys=True) == frozen_statistics, "standardizers changed"
        assert hashlib.sha256(args.checkpoint.read_bytes()).hexdigest() == checkpoint_hash, "checkpoint file changed"
        metadata.update(status="complete", elapsed_seconds=time.perf_counter()-started, weights_unchanged=True,
                        standardizers_unchanged=True, checkpoint_file_unchanged=True,
                        total_refresh_events=sum(result["refresh_events"] for result in results),
                        total_segments=sum(result["segments"] for result in results))
        write_json(output/"run_metadata.json", metadata)
        write_refresh_report(output, metadata, results)
    except Exception as error:
        metadata.update(status="failed", failure_reason=str(error))
        write_json(output/"run_metadata.json", metadata)
        raise
    print(f"Results and theory: {output/'Phase 6 Data.md'}", flush=True)


if __name__ == "__main__":
    main()

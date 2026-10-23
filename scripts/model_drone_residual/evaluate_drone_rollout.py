"""Evaluate a saved drone checkpoint in one-step and no-refresh recursive modes."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import torch

from drone_sim import load_dataset
from drone_sim.artifacts import next_phase
from model_drone_residual import load_checkpoint
from model_drone_residual.evaluation import evaluate_test_set, save_evaluation_summaries
from model_drone_residual.reporting import write_phase_report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", type=Path, default=Path("runs/Drone/phase_5/checkpoint_best.pt"))
    parser.add_argument("--dataset", type=Path, default=Path("runs/Drone/phase_2/dataset.npz"))
    parser.add_argument("--benchmark", type=Path, default=Path("runs/Drone/phase_2/benchmark_dataset.npz"))
    parser.add_argument("--output-root", type=Path, default=Path("runs/Drone"))
    parser.add_argument("--threads", type=int, default=1)
    args = parser.parse_args()
    if args.threads < 1:
        parser.error("threads must be positive")
    torch.set_num_threads(args.threads)
    predictor, checkpoint = load_checkpoint(args.checkpoint)
    if checkpoint.get("checkpoint_kind") not in ("best", "final") or "training_run_summary" not in checkpoint:
        parser.error("phase-5 evaluation requires a best/final checkpoint from a completed training run")
    main_data, benchmark = load_dataset(args.dataset), load_dataset(args.benchmark)
    if (main_data.metadata["simulation"] != benchmark.metadata["simulation"] or
            main_data.metadata["held_out_family"] != benchmark.metadata["held_out_family"]):
        parser.error("main and benchmark settings and held-out family must match")
    output, _ = next_phase(args.output_root, 5)
    info = {"path": args.checkpoint.as_posix(), "sha256": hashlib.sha256(args.checkpoint.read_bytes()).hexdigest(),
            "optimizer_updates": checkpoint["optimizer_updates"], "selection": checkpoint.get("checkpoint_kind", "supplied checkpoint")}
    metadata = {"phase": 5, "status": "evaluating", "evaluation_only": True, "checkpoint": info,
                "training_config": checkpoint["training_config"], "truth_refresh": None, "num_threads": args.threads,
                "dataset_counts": main_data.metadata["split_counts"], "benchmark_count": len(benchmark.states),
                "command": subprocess.list2cmdline(["python", "scripts/model_drone_residual/evaluate_drone_rollout.py", *sys.argv[1:]]),
                "inputs": {label: {"path": path.as_posix(), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
                           for label, path in (("main", args.dataset), ("benchmark", args.benchmark))}}
    root = Path(__file__).resolve().parents[2]
    sources = sorted((root/"src/drone_sim").glob("*.py")) + sorted((root/"src/model_drone_residual").glob("*.py")) + [Path(__file__).resolve()]
    metadata["source_sha256"] = {path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest() for path in sources}

    def save_metadata():
        (output/"run_metadata.json").write_text(json.dumps(metadata, indent=2, allow_nan=False)+"\n", encoding="utf-8")

    save_metadata()
    try:
        results = [evaluate_test_set(predictor, data, output, split=split, checkpoint_info=info, progress=lambda value: print(value, flush=True))
                   for split, data in (("test", main_data), ("benchmark", benchmark))]
        summary = save_evaluation_summaries(results, output)
        metadata.update(status="complete", evaluation_summary=summary)
        save_metadata()
        write_phase_report(output, metadata, summary)
    except Exception as error:
        metadata.update(status="failed", failure_reason=str(error))
        save_metadata()
        raise
    print(f"Evaluation saved: {output/'Phase 5 Data.md'}", flush=True)


if __name__ == "__main__":
    main()

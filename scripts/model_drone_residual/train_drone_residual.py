"""Train for at least 10,000 updates by default, rounded up to complete epochs."""

import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import torch

from drone_sim import load_dataset
from drone_sim.artifacts import next_phase
from model_drone_residual import TrainingConfig, train_model, save_training_outputs, load_checkpoint
from model_drone_residual.training import epoch_budget
from model_drone_residual.evaluation import evaluate_test_set, save_evaluation_summaries
from model_drone_residual.plotting import plot_loss_curves
from model_drone_residual.reporting import write_phase_report


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False)+"\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=Path("runs/Drone/phase_2/dataset.npz"))
    parser.add_argument("--benchmark", type=Path, default=Path("runs/Drone/phase_2/benchmark_dataset.npz"))
    parser.add_argument("--output-root", type=Path, default=Path("runs/Drone"))
    parser.add_argument("--updates", type=int, default=10000)
    parser.add_argument("--batch-size", type=int, default=256)
    parser.add_argument("--learning-rate", type=float, default=.001)
    parser.add_argument("--validation-interval", type=int, default=100)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--hidden-size", type=int, default=64)
    parser.add_argument("--hidden-layers", type=int, default=2)
    parser.add_argument("--threads", type=int, default=1)
    args = parser.parse_args()
    try:
        config = TrainingConfig(args.updates, args.batch_size, args.learning_rate, args.validation_interval,
                                args.seed, args.hidden_size, args.hidden_layers, num_threads=args.threads)
    except ValueError as error:
        parser.error(str(error))
    main_data, benchmark = load_dataset(args.dataset), load_dataset(args.benchmark)
    if set(main_data.split.tolist()) != {"train", "validation", "test"} or set(benchmark.split.tolist()) != {"benchmark"}:
        parser.error("provide the main train/validation/test archive and separate benchmark")
    if (main_data.metadata["simulation"] != benchmark.metadata["simulation"] or
            main_data.metadata["held_out_family"] != benchmark.metadata["held_out_family"] or
            main_data.metadata["config"]["seed"] != benchmark.metadata["config"]["seed"]):
        parser.error("main and benchmark must share simulator settings, root seed, and held-out family")
    torch.set_num_threads(config.num_threads)
    budget = epoch_budget(int((main_data.split == 'train').sum())*main_data.controls.shape[1], config.batch_size, config.optimizer_updates)
    output, _ = next_phase(args.output_root, 5)
    root = Path(__file__).resolve().parents[2]
    sources = sorted((root/"src/drone_sim").glob("*.py")) + sorted((root/"src/model_drone_residual").glob("*.py"))
    sources += sorted(Path(__file__).parent.glob("*.py"))
    revision = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True, check=False)
    dirty = subprocess.run(["git", "status", "--porcelain"], cwd=root, capture_output=True, text=True, check=False)
    metadata = {"phase": 5, "status": "training", "training_config": asdict(config),
                "command": subprocess.list2cmdline(["python", "scripts/model_drone_residual/train_drone_residual.py", *sys.argv[1:]]),
                "inputs": {label: {"path": path.as_posix(), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
                           for label, path in (("main", args.dataset), ("benchmark", args.benchmark))},
                "source_sha256": {path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest() for path in sources},
                "code_revision": revision.stdout.strip(), "working_tree_dirty": bool(dirty.stdout.strip()),
                "torch_version": str(torch.__version__), "reference_simulation": main_data.metadata["simulation"],
                "dataset_counts": main_data.metadata["split_counts"], "benchmark_count": len(benchmark.states), "truth_refresh": None}
    write_json(output/"run_metadata.json", metadata)
    print(f"Training into {output}: {config.optimizer_updates:,} requested, {budget['planned_optimizer_updates']:,} actual Adam updates; complete epochs.", flush=True)

    def progress(row):
        if row["optimizer_updates"] % 1000 == 0 or row["optimizer_updates"] == budget['planned_optimizer_updates']:
            print(f"Update {row['optimizer_updates']:,}: train MSE={row['train_loss']:.6g}, "
                  f"validation MSE={row['validation_loss']:.6g}", flush=True)

    try:
        result = train_model(main_data, config, progress)
        save_training_outputs(result, output, provenance={"inputs": metadata["inputs"], "source_sha256": metadata["source_sha256"],
                                                        "code_revision": metadata["code_revision"]})
        plot_loss_curves(result.history, output/"loss_curves.png", result.summary["best_update"])
        predictor, checkpoint = load_checkpoint(output/"checkpoint_best.pt")
        info = {"path": (output/"checkpoint_best.pt").as_posix(),
                "sha256": hashlib.sha256((output/"checkpoint_best.pt").read_bytes()).hexdigest(),
                "optimizer_updates": checkpoint["optimizer_updates"], "selection": "lowest validation standardized residual MSE"}
        metadata.update(status="evaluating", training_summary=result.summary, checkpoint=info)
        write_json(output/"run_metadata.json", metadata)
        print(f"Training complete. Selected update {info['optimizer_updates']:,}; evaluating held-out flights.", flush=True)
        results = [evaluate_test_set(predictor, data, output, split=split, checkpoint_info=info, progress=lambda value: print(value, flush=True))
                   for split, data in (("test", main_data), ("benchmark", benchmark))]
        summary = save_evaluation_summaries(results, output)
        metadata.update(status="complete", evaluation_summary=summary, plots=[name for item in results for name in item["examples"]])
        write_json(output/"run_metadata.json", metadata)
        write_phase_report(output, metadata, summary, result.summary)
    except Exception as error:
        metadata.update(status="failed", failure_reason=str(error))
        write_json(output/"run_metadata.json", metadata)
        raise
    for split, modes in summary.items():
        for name, values in modes["recursive"].items():
            print(f"{split} {name}: recursive mean position MAE={values['mean_position_mae_m']:.6g} m; "
                  f"orientation MAE={values['mean_orientation_mae_rad']:.6g} rad ({values['mean_orientation_mae_deg']:.6g} deg)", flush=True)
    print(f"Results and theory: {output/'Phase 5 Data.md'}", flush=True)


if __name__ == "__main__":
    main()

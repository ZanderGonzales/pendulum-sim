"""Phase 7: controlled quantity, variety, update, architecture, and refresh experiments.

Requested training budgets are rounded upward to complete epochs. Identical
conditions share checkpoints across experiments, but every unique condition is
trained independently for seeds 0, 1, and 2 by default. No test-based selection.
"""

import argparse
from collections import Counter
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

import numpy as np
import torch

from drone_sim import load_dataset
from drone_sim.artifacts import next_phase
from model_drone_residual import TrainingConfig, train_model, save_training_outputs, load_checkpoint, prepare_samples, HybridPredictor
from model_drone_residual.training import epoch_budget
from model_drone_residual.experiments import (EXPERIMENT_NAMES, REFRESH_INTERVALS, experiment_designs,
                                             select_training_dataset, select_prepared_samples)
from model_drone_residual.experiment_evaluation import ExperimentReference, evaluate_experiment, evaluate_refresh_experiment
from model_drone_residual.experiment_reporting import write_experiment_reports, write_seed_report
from model_drone_residual.experiment_plotting import plot_experiments
from model_drone_residual.plotting import plot_loss_curves
from model_drone_residual.refresh_evaluation import write_json


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def owning_experiment(name):
    return 'A' if name.startswith('broad_') else 'B' if name.startswith('restricted') else 'C' if name.startswith('updates') else 'D'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dataset', type=Path, default=Path('runs/Drone/phase_2/dataset.npz'))
    parser.add_argument('--benchmark', type=Path, default=Path('runs/Drone/phase_2/benchmark_dataset.npz'))
    parser.add_argument('--output-root', type=Path, default=Path('runs/Drone'))
    parser.add_argument('--resume', type=Path)
    parser.add_argument('--experiments', nargs='+', choices=tuple(EXPERIMENT_NAMES), default=list(EXPERIMENT_NAMES))
    parser.add_argument('--seeds', type=int, nargs='+', default=[0, 1, 2])
    parser.add_argument('--threads', type=int, default=1)
    parser.add_argument('--describe', action='store_true', help='Print the full training design without performing any runs')
    args = parser.parse_args()
    if args.threads < 1 or any(seed < 0 for seed in args.seeds) or len(set(args.seeds)) != len(args.seeds):
        parser.error('threads must be positive; seeds must be distinct nonnegative integers')
    experiments = list(dict.fromkeys(args.experiments))
    cases, groups = experiment_designs()
    needed = set(name for letter in experiments for name in groups.get(letter, []))
    if 'E' in experiments:
        needed.add('broad_80')
    cases = {name: case for name, case in cases.items() if name in needed}
    main_data, benchmark = load_dataset(args.dataset), load_dataset(args.benchmark)
    if (set(main_data.split.tolist()) != {'train', 'validation', 'test'} or
            main_data.metadata['config']['seed'] != benchmark.metadata['config']['seed']):
        parser.error('use the fixed main archive and matching separately held-out benchmark')
    selections = {name: select_training_dataset(main_data, case) for name, case in cases.items()}
    designs = {name: {**asdict(case), 'selection': selections[name].metadata['experiment_training_selection'],
                       **epoch_budget(case.train_count*main_data.controls.shape[1], 256, case.requested_updates)}
               for name, case in cases.items()}
    if args.describe:
        print(json.dumps(dict(unique_training_runs=len(cases)*len(args.seeds), seeds=args.seeds, designs=designs), indent=2))
        return
    repo = Path(__file__).resolve().parents[2]
    sources = sorted((repo/'src/drone_sim').glob('*.py'))+sorted((repo/'src/model_drone_residual').glob('*.py'))+[Path(__file__).resolve()]
    hashes = {p.relative_to(repo).as_posix(): sha(p) for p in sources}
    # Report/plot changes can be regenerated on resume; cached training and
    # evaluation may only be reused when their computational sources match.
    critical = {key: value for key, value in hashes.items() if not key.endswith(('experiment_reporting.py', 'experiment_plotting.py'))}
    inputs = {label: dict(path=path.as_posix(), sha256=sha(path)) for label, path in (('main', args.dataset), ('benchmark', args.benchmark))}
    protocol = dict(experiments=experiments, seeds=args.seeds, threads=args.threads, cases=designs,
                    groups={k: v for k, v in groups.items() if k in experiments}, inputs=inputs, critical_source_sha256=critical)
    protocol = json.loads(json.dumps(protocol))  # JSON round-trip also normalizes tuple-valued designs for resume.
    protected = {path: sha(path) for path in ('Drone_Plan.md', 'README.md', 'runs/Runs Masterlist.md', 'runs/Drone/phase_5/checkpoint_best.pt')}
    if args.resume:
        output = args.resume
        manifest = json.loads((output/'suite_manifest.json').read_text())
        if any(manifest[key] != value for key, value in protocol.items()):
            parser.error('resume protocol, data, or computational source hashes differ from the saved manifest')
        protected = manifest['protected_file_sha256']
    else:
        output, _ = next_phase(args.output_root, 7)
        revision = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True, check=False)
        manifest = dict(**protocol, phase=7, source_sha256=hashes, protected_file_sha256=protected,
            code_revision=revision.stdout.strip(), torch_version=str(torch.__version__), reference_simulation=main_data.metadata['simulation'],
            command=subprocess.list2cmdline(['python', 'scripts/model_drone_residual/run_drone_experiments.py', *sys.argv[1:]]),
            evaluation_ids=dict(test=main_data.trajectory_ids[main_data.split == 'test'].tolist(), benchmark=benchmark.trajectory_ids.tolist()))
        write_json(output/'suite_manifest.json', manifest)
    torch.set_num_threads(args.threads)
    started = time.perf_counter()
    state = dict(phase=7, status='preparing', unique_training_runs=len(cases)*len(args.seeds),
                 completed_training_runs=0, completed_refresh_runs=0, manifest='suite_manifest.json', command=manifest['command'])
    records, refresh_records = [], []

    def save_state(status):
        state.update(status=status, elapsed_seconds_this_invocation=time.perf_counter()-started,
                     completed_training_runs=len(records), completed_refresh_runs=len(refresh_records))
        write_json(output/'run_metadata.json', state)
        write_json(output/'suite_results.json', dict(training=records, refresh=refresh_records))

    print(f'Phase 7: {len(cases)*len(args.seeds)} unique training runs; complete epochs; output {output}', flush=True)
    save_state('preparing')
    try:
        # These cached arrays contain no standardization. Each training subset
        # still fits its own standardizers, with no held-out statistics.
        full_training = prepare_samples(main_data, 'train')
        validation = prepare_samples(main_data, 'validation')
        reference = ExperimentReference(main_data, benchmark)
        for name, case in cases.items():
            data = selections[name]
            prepared = select_prepared_samples(full_training, data.trajectory_ids[data.split == 'train']), validation
            letter = owning_experiment(name)
            folder = output/f'Experiment {letter} - {EXPERIMENT_NAMES[letter]}'/name
            for seed in args.seeds:
                run_output = folder/f'seed_{seed}'
                run_output.mkdir(parents=True, exist_ok=True)
                record_path = run_output/'run_metadata.json'
                if record_path.exists():
                    saved = json.loads(record_path.read_text())
                    if saved.get('status') == 'complete':
                        records.append(saved['record'])
                        print(f'Reused complete {name}, seed {seed}', flush=True)
                        continue
                config = TrainingConfig(optimizer_updates=case.requested_updates, seed=seed,
                    hidden_size=case.hidden_size, hidden_layers=case.hidden_layers, num_threads=args.threads)
                provenance = dict(inputs=inputs, training_selection=data.metadata['experiment_training_selection'],
                                  source_sha256=critical, training_config=asdict(config))
                print(f'Train {name}, seed {seed}: {designs[name]["planned_optimizer_updates"]:,} updates / '
                      f'{designs[name]["planned_complete_epochs"]} complete epochs', flush=True)
                if not (run_output/'checkpoint_final.pt').exists():
                    write_json(record_path, dict(status='training', provenance=provenance))
                    def progress(row):
                        if row['optimizer_updates'] and row['optimizer_updates'] % 5000 == 0:
                            print(f'  {name} seed {seed}, update {row["optimizer_updates"]:,}, validation MSE {row["validation_loss"]:.5g}', flush=True)
                    fitted = train_model(data, config, progress, prepared_samples=prepared)
                    save_training_outputs(fitted, run_output, provenance=provenance)
                    plot_loss_curves(fitted.history, run_output/'loss_curves.png', fitted.summary['best_update'])
                    del fitted
                predictor, checkpoint = load_checkpoint(run_output/'checkpoint_best.pt')
                if checkpoint['provenance'] != provenance:
                    raise ValueError('saved checkpoint provenance differs from the requested run')
                training_summary = checkpoint['training_run_summary']
                info = dict(path=(run_output/'checkpoint_best.pt').as_posix(), sha256=sha(run_output/'checkpoint_best.pt'),
                            optimizer_updates=checkpoint['optimizer_updates'], selection='lowest validation standardized residual MSE')
                write_json(record_path, dict(status='evaluating', provenance=provenance, checkpoint=info))
                metrics = evaluate_experiment(reference, predictor, run_output, info, all_families=(seed == args.seeds[0]))
                report_filename = f'Experiment {letter} - {EXPERIMENT_NAMES[letter]} Data.md'
                record = dict(case=name, label=case.label, seed=seed, output=run_output.as_posix(),
                              report_filename=report_filename, training_summary=training_summary, checkpoint=info, metrics=metrics,
                              training_selection=data.metadata['experiment_training_selection'])
                write_seed_report(record, run_output/report_filename, EXPERIMENT_NAMES[letter])
                write_json(record_path, dict(status='complete', provenance=provenance, checkpoint=info, record=record))
                records.append(record)
                save_state('training_and_evaluating')
                print(f'Complete {name}, seed {seed}: test recursive position MAE '
                      f'{metrics["test"]["recursive"]["hybrid"]["mean_position_mae_m"]:.6g} m', flush=True)
        if 'E' in experiments:
            for interval in REFRESH_INTERVALS:
                label = 'no_refresh' if interval is None else f'every_{interval}_steps'
                for seed in args.seeds:
                    source = next(run for run in records if run['case'] == 'broad_80' and run['seed'] == seed)
                    run_output = output/f'Experiment E - {EXPERIMENT_NAMES["E"]}'/label/f'seed_{seed}'
                    run_output.mkdir(parents=True, exist_ok=True)
                    record_path = run_output/'run_metadata.json'
                    if record_path.exists():
                        saved = json.loads(record_path.read_text())
                        if saved.get('status') == 'complete':
                            refresh_records.append(saved['record'])
                            continue
                    predictor, checkpoint = load_checkpoint(source['checkpoint']['path'])
                    weights = {name: value.clone() for name, value in predictor.model.state_dict().items()}
                    statistics = json.dumps(predictor.standardizers.to_dict(), sort_keys=True)
                    raw = evaluate_refresh_experiment(reference, predictor, run_output, interval, source['checkpoint'])
                    assert all(torch.equal(weights[name], value) for name, value in predictor.model.state_dict().items())
                    assert statistics == json.dumps(predictor.standardizers.to_dict(), sort_keys=True)
                    assert sha(source['checkpoint']['path']) == source['checkpoint']['sha256']
                    metrics = {split: dict(recursive=views['forecast_before_replacement']) for split, views in raw.items()}
                    report_filename = 'Experiment E - Refresh Frequency Data.md'
                    record = dict(case=label, label='No refresh' if interval is None else f'Every {interval} steps', seed=seed,
                        refresh_interval_steps=interval, refresh_count=0 if interval is None else reference.controls.shape[1]//interval,
                        output=run_output.as_posix(), source_run=source['output'], report_filename=report_filename,
                        training_summary=source['training_summary'], checkpoint=source['checkpoint'], metrics=metrics,
                        training_selection=source['training_selection'])
                    write_seed_report(record, run_output/report_filename, EXPERIMENT_NAMES['E'])
                    write_json(record_path, dict(status='complete', optimizer_updates_this_run=0, weights_unchanged=True,
                                                standardizers_unchanged=True, record=record))
                    refresh_records.append(record)
                    save_state('refresh_evaluation')
                    print(f'Refresh {label}, seed {seed}: test position MAE '
                          f'{metrics["test"]["recursive"]["hybrid"]["mean_position_mae_m"]:.6g} m', flush=True)
        write_experiment_reports(output, manifest, records, refresh_records)
        plot_experiments(output, manifest, records, refresh_records)
        assert all(sha(path) == value for path, value in protected.items()), 'protected file changed'
        state.update(protected_files_unchanged=True, total_actual_training_updates=sum(r['training_summary']['optimizer_updates'] for r in records),
                     total_training_seconds=sum(r['training_summary']['training_seconds'] for r in records),
                     all_training_runs_end_on_complete_epochs=all(r['training_summary']['epoch_fraction'] == r['training_summary']['completed_epochs'] for r in records))
        save_state('complete')
        print(f'Phase 7 complete. Results and theory: {output/"Phase 7 Data.md"}', flush=True)
    except Exception as error:
        state['failure_reason'] = str(error)
        save_state('failed')
        raise


if __name__ == '__main__':
    main()

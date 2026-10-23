"""Readable controlled-experiment results: one metric value per bullet."""

from collections import defaultdict
import csv
import json
from pathlib import Path

import numpy as np

from model_drone_residual.experiments import EXPERIMENT_NAMES, percent_reduction


METRICS = ('mean_position_mae_m', 'mean_orientation_mae_rad', 'mean_orientation_mae_deg',
           'mean_position_error_pct_simulator_distance', 'mean_orientation_error_pct_simulator_rotation')


def number(value, unit=''):
    return 'N/A (zero reference denominator)' if value is None else f'{value:.6g}{unit}'


def condition_label(letter, case, runs):
    if case == 'broad_80' and letter == 'C':
        return '10,000 requested optimizer updates'
    if case == 'broad_80' and letter == 'D':
        return '2 hidden layers x 64 neurons'
    return runs[0]['label']


def aggregate_runs(runs):
    summaries = {}
    for split in ('test', 'benchmark'):
        summaries[split] = {}
        for mode in runs[0]['metrics'][split]:
            summaries[split][mode] = {}
            for predictor in ('physics_only', 'hybrid'):
                values = [run['metrics'][split][mode][predictor] for run in runs]
                result = {}
                for key in values[0]:
                    if key.startswith('mean_'):
                        selected = [row[key] for row in values if row[key] is not None]
                        result[key] = float(np.mean(selected)) if selected else None
                        result['seed_std_'+key] = float(np.std(selected)) if selected else None
                summaries[split][mode][predictor] = result
    return summaries


def pairwise_comparisons(experiment, groups):
    """Compare every ordered pair, matched seed or seed-mean, never cross split/mode."""
    result = []
    for candidate, candidate_runs in groups.items():
        for reference, reference_runs in groups.items():
            if candidate == reference:
                continue
            paired = [(str(run['seed']), run['metrics'], next(other['metrics'] for other in reference_runs if other['seed'] == run['seed']))
                      for run in candidate_runs]
            paired += [('seed_mean', aggregate_runs(candidate_runs), aggregate_runs(reference_runs))]
            for seed, a, b in paired:
                for split in ('test', 'benchmark'):
                    for mode in a[split]:
                        for predictor in ('physics_only', 'hybrid'):
                            for metric in ('mean_position_mae_m', 'mean_orientation_mae_rad'):
                                first, second = a[split][mode][predictor][metric], b[split][mode][predictor][metric]
                                result.append(dict(experiment=experiment, candidate=candidate, reference=reference, seed=seed,
                                    split=split, mode=mode, predictor=predictor, metric=metric, candidate_mae=first,
                                    reference_mae=second, error_reduction_pct=percent_reduction(first, second)))
    return result


def _write_csv(path, rows):
    if not rows:
        return
    with path.open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _metric_bullets(summary, *, include_variability=False):
    hybrid, physics = summary['hybrid'], summary['physics_only']
    lines = [f'- Mean position MAE against MuJoCo: **{number(hybrid["mean_position_mae_m"], " m")}**.',
             f'- Mean orientation MAE against MuJoCo: **{number(hybrid["mean_orientation_mae_deg"], " deg")}**.',
             f'- Orientation MAE in radians: {number(hybrid["mean_orientation_mae_rad"], " rad")}.',
             f'- Position MAE as a percentage of MuJoCo distance traveled: {number(hybrid["mean_position_error_pct_simulator_distance"], "%")}.',
             f'- Orientation MAE as a percentage of MuJoCo angular travel: {number(hybrid["mean_orientation_error_pct_simulator_rotation"], "%")}.',
             f'- Position error reduction versus physics-only: {number(percent_reduction(hybrid["mean_position_mae_m"], physics["mean_position_mae_m"]), "%")}.',
             f'- Orientation error reduction versus physics-only: {number(percent_reduction(hybrid["mean_orientation_mae_rad"], physics["mean_orientation_mae_rad"]), "%")}.']
    lines += [f'- Physics-only mean position MAE: **{number(physics["mean_position_mae_m"], " m")}**.',
              f'- Physics-only mean orientation MAE: **{number(physics["mean_orientation_mae_deg"], " deg")}**.']
    if include_variability:
        lines += [f'- Seed standard deviation of mean position MAE: {number(hybrid["seed_std_mean_position_mae_m"], " m")}.',
                  f'- Seed standard deviation of mean orientation MAE: {number(hybrid["seed_std_mean_orientation_mae_deg"], " deg")}.']
    else:
        lines += [f'- Trajectory standard deviation of position MAE: {number(hybrid["std_position_mae_m"], " m")}.',
                  f'- Trajectory standard deviation of orientation MAE: {number(hybrid["std_orientation_mae_deg"], " deg")}.']
    return lines


def _physical_metric_bullets(values):
    fields = (
        ('mean_position_mae_m', 'Mean position MAE', ' m'),
        ('std_position_mae_m', 'Trajectory standard deviation of position MAE', ' m'),
        ('mean_orientation_mae_deg', 'Mean orientation MAE', ' deg'),
        ('std_orientation_mae_deg', 'Trajectory standard deviation of orientation MAE', ' deg'),
        ('mean_orientation_mae_rad', 'Mean orientation MAE in radians', ' rad'),
        ('mean_position_rmse_m', 'Mean position RMSE', ' m'),
        ('mean_orientation_rmse_deg', 'Mean orientation RMSE', ' deg'),
        ('mean_linear_velocity_mae_m_s', 'Mean linear velocity MAE', ' m/s'),
        ('mean_linear_velocity_rmse_m_s', 'Mean linear velocity RMSE', ' m/s'),
        ('mean_angular_velocity_mae_rad_s', 'Mean angular velocity MAE', ' rad/s'),
        ('mean_angular_velocity_rmse_rad_s', 'Mean angular velocity RMSE', ' rad/s'),
        ('mean_final_position_error_m', 'Mean final position error', ' m'),
        ('mean_maximum_position_error_m', 'Mean maximum position error', ' m'),
        ('mean_position_error_pct_simulator_distance', 'Position MAE as a percentage of MuJoCo distance traveled', '%'),
        ('mean_orientation_error_pct_simulator_rotation', 'Orientation MAE as a percentage of MuJoCo angular travel', '%'),
    )
    return [f'- {label}: {number(values[key], unit)}.' for key, label, unit in fields if key in values]


def write_seed_report(run, path, experiment_name):
    lines = [f'# Experiment: {experiment_name}', '', f'## Run: {run["label"]}', '',
             f'- Training seed: {run["seed"]}.', '']
    training = run['training_summary']
    lines += [f'- Requested optimizer updates for source training: {training["requested_optimizer_updates"]:,}.',
              f'- Actual optimizer updates for source training: {training["optimizer_updates"]:,}.',
              f'- Completed source-training epochs: {training["completed_epochs"]:,}.',
              f'- Selected checkpoint update: {run["checkpoint"]["optimizer_updates"]:,}.',
              f'- Trainable parameters: {training["trainable_parameters"]:,}.',
              f'- Source training time: {training["training_seconds"]:.4f} s.', '']
    if run.get('refresh_interval_steps', 'training') != 'training':
        lines += ['No training or weight updates occurred for this refresh run. The source checkpoint remains fixed.', '',
                  f'Source run: `{run["source_run"]}`.', '',
                  'Errors below use forecasts saved before any truth replacement. Playback shows post-replacement states.', '']
    for split, modes in run['metrics'].items():
        for mode, summary in modes.items():
            lines += [f'## {split.capitalize()}: {mode.replace("_", " ")}', '']
            for name in ('physics_only', 'hybrid'):
                lines += [f'### {"Physics only" if name == "physics_only" else "Physics + NN"}', '',
                          *_physical_metric_bullets(summary[name]), '']
            lines += ['### Hybrid improvement versus physics-only', '',
                      f'- Position error reduction: {number(percent_reduction(summary["hybrid"]["mean_position_mae_m"], summary["physics_only"]["mean_position_mae_m"]), "%")}.',
                      f'- Orientation error reduction: {number(percent_reduction(summary["hybrid"]["mean_orientation_mae_rad"], summary["physics_only"]["mean_orientation_mae_rad"]), "%")}.', '']
    lines += ['## Artifacts', '', '`checkpoint_best.pt` and `checkpoint_final.pt` are saved with the source training run. '
              '`training_metrics.csv`, `training_summary.json`, `standardizers.json`, and `loss_curves.png` document training. '
              '`test_metrics.json`, `rollout_metrics.csv` / `.json`, and prediction archives retain physical errors and full paths. '
              '`plots/` contains the large 3D comparison and position/orientation error panels. '
              'Experiment-level reports compare this condition with the other conditions using matched seeds.', '',
              '[All matched-seed percentage comparisons](<../../../pairwise_comparisons.csv>).', '']
    path.write_text('\n'.join(lines), encoding='utf-8')


def _experiment_lines(letter, groups, pairs, root, experiment_folder):
    title = EXPERIMENT_NAMES[letter]
    descriptions = {
        'A': 'Nested, balanced source-order subsets vary training trajectory count. Network size and requested updates stay fixed.',
        'B': 'Both conditions use the same training count and flight duration. Restricted data contain circles and figure-eights; broad data cover all main families. Validation and test flights are identical.',
        'C': 'Only the requested optimizer-update budget changes. Dataset, architecture, optimizer, and evaluation flights stay fixed.',
        'D': 'Width comparisons hold hidden depth fixed. Depth comparisons hold hidden width fixed. The shared standard network supplies the reference.',
        'E': 'Each seed uses its full-data standard-network checkpoint for every schedule. No retraining occurs between schedules. Primary metrics score forecasts before replacement.',
    }
    lines = [f'## Experiment: {title}', '', descriptions[letter], '',
             'All displayed run summaries use fully recursive forecasts. Positive comparison percentages mean less error; negative percentages mean more error. '
             'The comparison denominator is the named reference run. Seed means weight each training seed equally; each seed first weights each test flight equally.', '',
             f'[All pairwise percentages](<{experiment_folder.relative_to(root).as_posix()}/pairwise_comparisons.csv>).', '',
             f'[Comparison plot](<{experiment_folder.relative_to(root).as_posix()}/plots/comparison_mae.png>).', '']
    for case, runs in groups.items():
        aggregate = aggregate_runs(runs)
        label = condition_label(letter, case, runs)
        lines += [f'### Run: {label}', '',
                  f'Artifacts: [{label}](<{Path(runs[0]["output"]).relative_to(root).as_posix()}/>).', '']
        selection = runs[0].get('training_selection')
        if selection:
            lines += ['#### Training composition', '', f'- Training trajectories: {selection["train_count"]}.',
                      f'- Hidden layers: {selection["hidden_layers"]}.', f'- Neurons per hidden layer: {selection["hidden_size"]}.']
            for family, count in selection['family_counts'].items():
                lines.append(f'- {family} training trajectories: {count}.')
            lines.append('')
        for split in ('test', 'benchmark'):
            lines += [f'#### {split.capitalize()}: mean across training seeds', '',
                      *_metric_bullets(aggregate[split]['recursive'], include_variability=True), '']
            lines += [f'#### {split.capitalize()}: comparisons with other runs', '']
            selected = [row for row in pairs if row['candidate'] == case and row['seed'] == 'seed_mean' and
                        row['split'] == split and row['mode'] == 'recursive' and row['predictor'] == 'hybrid']
            for row in selected:
                label = condition_label(letter, row['reference'], groups[row['reference']])
                metric = 'Position' if row['metric'] == 'mean_position_mae_m' else 'Orientation'
                lines.append(f'- {metric} error reduction versus {label}: {number(row["error_reduction_pct"], "%")}.')
            lines.append('')
        for run in runs:
            lines += [f'#### Seed {run["seed"]}', '',
                      f'- Actual source-training optimizer updates: {run["training_summary"]["optimizer_updates"]:,}.',
                      f'- Completed source-training epochs: {run["training_summary"]["completed_epochs"]:,}.',
                      f'- Trainable parameters: {run["training_summary"]["trainable_parameters"]:,}.',
                      f'- Source training time: {run["training_summary"]["training_seconds"]:.4f} s.']
            if letter == 'E':
                lines.append('- Optimizer updates in this refresh run: 0.')
            for split in ('test', 'benchmark'):
                value = run['metrics'][split]['recursive']['hybrid']
                lines += [f'- {split.capitalize()} mean position MAE: {number(value["mean_position_mae_m"], " m")}.',
                          f'- {split.capitalize()} mean orientation MAE: {number(value["mean_orientation_mae_deg"], " deg")}.']
            report = Path(run['output'])/run['report_filename']
            lines += ['', f'Detailed seed report: [{run["report_filename"]}](<{report.relative_to(root).as_posix()}>).', '']
    return lines


def write_experiment_reports(root, manifest, records, refresh_records):
    root = Path(root)
    index = defaultdict(list)
    for run in records:
        index[run['case']].append(run)
    refresh_index = defaultdict(list)
    for run in refresh_records:
        refresh_index[run['case']].append(run)
    all_rows, all_pairs, all_aggregate = [], [], {}
    main = ['# Phase 7 Data: Controlled Learning Experiments', '', '## How to read these results', '',
            'Experiments are separated by the factor being controlled; each condition has its own run heading and individual seed subheadings. '
            'Each metric bullet contains one numerical result. The main report emphasizes recursive rollout; seed reports and CSV/JSON files also retain one-step results.', '',
            'Position MAE is mean Euclidean distance to the saved MuJoCo position. Orientation MAE is the mean shortest rotation angle. '
            'The initial state is excluded. MuJoCo compared with itself has zero error, so a percentage reduction relative to MuJoCo error would divide by zero. '
            'Instead, the simulator-relative percentages divide each flight’s position MAE by its total MuJoCo distance traveled, or its orientation MAE by its total MuJoCo angular travel, then average flights equally. '
            'They are normalized errors, not claims of percentage accuracy. Stationary denominators produce N/A.', '',
            'Percentage error reduction = 100 × (reference error − candidate error) / reference error. '
            'Every condition is compared with every other condition within its experiment. '
            'All matched-seed and seed-mean comparisons, for each predictor, evaluation mode, and held-out split, are retained in `pairwise_comparisons.csv`.', '',
            '## Shared settings and complete epochs', '',
            'Requested optimizer updates are minimum budgets, rounded upward to the next complete epoch. '
            'The final short batch is included in every epoch. Actual budgets differ slightly across dataset sizes and are disclosed; '
            'this is the small rounding difference in the trajectory-quantity comparison. '
            'Validation still runs at the configured update interval and at the final update. '
            'The lowest validation residual MSE selects the best checkpoint, which may precede the end of training or lie between epoch boundaries. '
            'Test and benchmark errors never select weights, subsets, or checkpoints.', '',
            '- Standard requested optimizer updates: 10,000.',
            '- Standard hidden layers: 2.', '- Standard neurons per hidden layer: 64.',
            '- Batch size: 256.', '- Learning rate: 0.001.', '- Prediction interval: 0.01 s.',
            '- Flight duration: 10 s.', '- Training seeds per unique condition: 3.', '',
            'Adam, Tanh activation, training-only input/target standardization, fixed drone properties, still air, and recorded applied controls are shared. '
            'Validation/test trajectories and the separate waypoint-family benchmark remain fixed. '
            'Identical training conditions reuse the same saved seed checkpoint across experiments; no older partial-epoch phase-5 training run substitutes for the new complete-epoch baseline.', '']
    main += ['## Navigate the experiments', '']
    for letter in manifest['experiments']:
        title = EXPERIMENT_NAMES[letter]
        main.append(f'- [{title}](#experiment-{title.lower().replace(" ", "-")}).')
    main += ['', '## Main comparisons at a glance', '',
             'These are predefined comparisons of seed-mean recursive position error. The detailed experiment sections below include every condition, orientation errors, individual seeds, and all pairwise percentages.', '']
    comparisons = (
        ('A', index, 'broad_80', 'broad_10', 'More training trajectories'),
        ('B', index, 'broad_20', 'restricted_20', 'Broad versus restricted families'),
        ('C', index, 'updates_20000', 'updates_5000', 'Larger versus smaller update budget'),
        ('D', index, 'layers_2_width_128', 'broad_80', 'Wider network versus standard width'),
        ('D', index, 'layers_4_width_64', 'broad_80', 'Deeper network versus standard depth'),
        ('E', refresh_index, 'every_100_steps', 'no_refresh', 'Periodic refresh versus no refresh'),
    )
    for letter, source, candidate, reference, label in comparisons:
        if letter not in manifest['experiments'] or not source.get(candidate) or not source.get(reference):
            continue
        a, b = aggregate_runs(source[candidate]), aggregate_runs(source[reference])
        for split in ('test', 'benchmark'):
            reduction = percent_reduction(a[split]['recursive']['hybrid']['mean_position_mae_m'], b[split]['recursive']['hybrid']['mean_position_mae_m'])
            main.append(f'- {label}, {split} position error reduction: {number(reduction, "%")}.')
    main.append('')
    for letter in manifest['experiments']:
        members = manifest['groups'].get(letter, [])
        groups = {name: sorted(index[name], key=lambda r: r['seed']) for name in members if index[name]}
        if letter == 'E':
            groups = dict(refresh_index)
        if not groups:
            continue
        pairs = pairwise_comparisons(EXPERIMENT_NAMES[letter], groups)
        all_pairs.extend(pairs)
        folder = root/f'Experiment {letter} - {EXPERIMENT_NAMES[letter]}'
        folder.mkdir(exist_ok=True)
        lines = _experiment_lines(letter, groups, pairs, root, folder)
        main.extend(lines)
        # The stand-alone report uses links relative to its own directory.
        import os
        standalone = '\n'.join(lines).replace('## Experiment:', '# Experiment:', 1)
        for runs in groups.values():
            for run in runs:
                relative = Path(run['output']).relative_to(root).as_posix()
                standalone = standalone.replace(f'](<{relative}/', f'](<{os.path.relpath(run["output"], folder).replace(chr(92), "/")}/')
        standalone = standalone.replace(f'](<{folder.relative_to(root).as_posix()}/', '](<')
        (folder/f'Experiment {letter} - {EXPERIMENT_NAMES[letter]} Data.md').write_text(standalone+'\n', encoding='utf-8')
        _write_csv(folder/'pairwise_comparisons.csv', pairs)
        aggregates = {name: aggregate_runs(runs) for name, runs in groups.items()}
        all_aggregate[letter] = aggregates
        (folder/'experiment_summary.json').write_text(json.dumps(aggregates, indent=2, allow_nan=False)+'\n')
        experiment_rows = []
        for name, runs in groups.items():
            for run in runs:
                for split, modes in run['metrics'].items():
                    for mode, predictors in modes.items():
                        for predictor, values in predictors.items():
                            row = dict(experiment=EXPERIMENT_NAMES[letter], condition=name, seed=run['seed'],
                                split=split, mode=mode, predictor=predictor,
                                requested_updates=run['training_summary']['requested_optimizer_updates'],
                                actual_updates=run['training_summary']['optimizer_updates'],
                                completed_epochs=run['training_summary']['completed_epochs'],
                                parameters=run['training_summary']['trainable_parameters'],
                                training_seconds=run['training_summary']['training_seconds'],
                                mean_position_mae_m=values['mean_position_mae_m'],
                                mean_orientation_mae_rad=values['mean_orientation_mae_rad'],
                                mean_orientation_mae_deg=values['mean_orientation_mae_deg'],
                                std_position_mae_m=values['std_position_mae_m'], std_orientation_mae_rad=values['std_orientation_mae_rad'],
                                position_error_pct_simulator_distance=values['mean_position_error_pct_simulator_distance'],
                                orientation_error_pct_simulator_rotation=values['mean_orientation_error_pct_simulator_rotation'],
                                refresh_interval_steps=run.get('refresh_interval_steps'), output=run['output'])
                            experiment_rows.append(row)
        all_rows.extend(experiment_rows)
        _write_csv(folder/'comparison_metrics.csv', experiment_rows)
    _write_csv(root/'comparison_metrics.csv', all_rows)
    _write_csv(root/'pairwise_comparisons.csv', all_pairs)
    (root/'experiment_summary.json').write_text(json.dumps(all_aggregate, indent=2, allow_nan=False)+'\n')
    main += ['## Theory, controls, and interpretation', '',
        'The NN learns a true-state one-step physics residual. Recursive evaluation then feeds each predicted state back into physics and feature construction, so small local errors can accumulate. '
        'Additional trajectories change sample quantity; additional families change state/control coverage; more optimizer updates change fitting opportunity; network size changes function capacity. '
        'A lower one-step residual loss does not guarantee lower recursive path error. '
        'Checkpoint selection and standardization use training/validation only; standardizers are fitted separately for each selected training subset and reused across seeds of that condition.', '',
        'Standardized residual losses from different training subsets use different target scales and should not be compared as if they shared a physical unit. '
        'This matters especially for restricted-family training, where some residual components vary very little in training but vary in the common validation flights. '
        'The physical position/orientation MAEs and simulator-normalized errors provide the shared comparison scale.', '',
        'For the variety experiment, the restricted set balances circles and figure-eights while the broad set balances all main families. '
        'Both keep the same total training duration. Their training paths differ by design; validation/test paths do not. '
        'The waypoint benchmark remains unseen in every condition. Family-specific metrics are retained with each trajectory so narrow-coverage effects can be inspected.', '',
        'Width and depth comparisons use the common standard architecture as a reference. Inputs and outputs are additional layers. '
        'Parameter counts and measured training times accompany each run. Training-time comparisons are CPU measurements under the recorded thread setting.', '',
        'Refresh experiments use full-state truth replacement at selected prediction timestamps, after saving the forecast. '
        'The primary error is measured before replacement; post-replacement metrics, event snapshots, and drift segments remain saved separately. '
        'Every-step refresh approaches one-step evaluation rather than zero forecast error. Final-timestamp resets count as observations but cannot improve an already-computed final forecast. '
        'All seeds use the same schedules, and their checkpoint weights and normalizers remain fixed.', '',
        'No automatic fidelity threshold or winning interval is imposed. The raw errors, seed variability, physics comparisons, and pairwise percentages support manual interpretation.', '',
        '## Reproduction and artifacts', '', '```powershell',
        r'.\.venv\Scripts\python.exe scripts/model_drone_residual/run_drone_experiments.py',
        f'python scripts/model_drone_residual/run_drone_experiments.py --resume "{root.as_posix()}"', '```', '',
        'Use `--experiments A B C D E` and `--seeds 0 1 2` to select comparisons; defaults run the full design. '
        'New invocations preserve earlier output under phase_7/repeat_N. Resuming checks source/input hashes and reuses completed runs. '
        'Canonical training artifacts are stored once under their owning experiment; shared baselines are linked from all other experiment reports. '
        'All seed reports identify the controlled factor in their filenames. Combined prediction archives load in the existing MuJoCo comparison viewer.', '',
        '`suite_manifest.json` records the protocol and exact training subsets. `run_metadata.json` records progress, runtimes, source/input hashes, and completion. '
        '`suite_results.json` retains every seed summary. `comparison_metrics.csv` contains raw and simulator-normalized errors. '
        '`pairwise_comparisons.csv` contains every directed condition comparison, including negative reductions. '
        '`experiment_summary.json` contains means and population standard deviations across seeds. '
        'Each experiment has its own report, summary, pairwise CSV, and comparison plots. '
        'Per-seed artifacts preserve best/final checkpoints, normalization, loss curves, full prediction/control histories, per-flight metrics, and path/error plots.', '',
        'Drone_Plan.md, README.md, Runs Masterlist.md, and prior phase outputs are unchanged. No commit was created.', '']
    (root/'Phase 7 Data.md').write_text('\n'.join(main), encoding='utf-8')

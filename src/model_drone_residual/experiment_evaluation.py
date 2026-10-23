"""Shared physics references and final scoring for the phase-7 experiments."""

import csv
import json
from pathlib import Path

import numpy as np

from drone_sim.evaluation import one_step_predictions, summarize_metrics, trajectory_metrics
from drone_sim.frames import orientation_difference
from drone_sim.physics import RigidBodyParameters, RigidBodyPhysics
from drone_sim.types import SimulationConfig
from model_drone_residual.evaluation import save_evaluation_summaries
from model_drone_residual.refresh import RefreshSchedule, rollout_with_refresh
from model_drone_residual.refresh_evaluation import drift_records, EVENT_FIELDS, SEGMENT_FIELDS, write_csv, write_json
from model_drone_residual.residuals import apply_residual


class ExperimentReference:
    """Cache physics once; preserve all held-out flights and their recorded controls."""

    def __init__(self, main, benchmark):
        if (main.metadata['simulation'] != benchmark.metadata['simulation'] or
                main.metadata['held_out_family'] != benchmark.metadata['held_out_family'] or
                not np.array_equal(main.time, benchmark.time)):
            raise ValueError("test and benchmark must share simulator settings and prediction grid")
        settings = main.metadata['simulation']
        self.physics = RigidBodyPhysics(RigidBodyParameters.from_metadata(settings), SimulationConfig(**settings['simulation_config']))
        self.time = main.time.copy()
        indices = np.flatnonzero(main.split == 'test')
        if not len(indices) or set(benchmark.split.tolist()) != {'benchmark'}:
            raise ValueError("fixed test and separate benchmark trajectories are required")
        self.truth = np.concatenate((main.states[indices], benchmark.states))
        self.controls = np.concatenate((main.controls[indices], benchmark.controls))
        self.ids = np.concatenate((main.trajectory_ids[indices], benchmark.trajectory_ids))
        self.families = np.concatenate((main.families[indices], benchmark.families))
        self.splits = np.array(['test']*len(indices)+['benchmark']*len(benchmark.states))
        self.physics_recursive = self.physics.rollout(self.truth[:, 0], self.controls)
        self.physics_one_step = one_step_predictions(self.physics, self.truth, self.controls)
        self.distance = np.linalg.norm(np.diff(self.truth[..., :3], axis=1), axis=-1).sum(axis=1)
        self.rotation = np.linalg.norm(orientation_difference(self.truth[:, :-1, 3:7], self.truth[:, 1:, 3:7]), axis=-1).sum(axis=1)
        self.refresh_cache = {}

    def validate_predictor(self, predictor):
        if predictor.physics.parameters != self.physics.parameters or predictor.physics.config != self.physics.config:
            raise ValueError("predictor must match the fixed reference physics and timing")

    def one_step_hybrid(self, predictor):
        current = self.truth[:, :-1]
        correction = predictor.predict_residuals(current, self.controls)
        following = apply_residual(current, self.physics_one_step[:, 1:], correction)
        return np.concatenate((self.physics_one_step[:, :1], following), axis=1)

    def physics_refresh(self, interval):
        if interval not in self.refresh_cache:
            self.refresh_cache[interval] = rollout_with_refresh(
                self.physics, self.truth[:, 0], self.controls,
                schedule=RefreshSchedule(interval_steps=interval), truth_provider=lambda step: self.truth[:, step])
        return self.refresh_cache[interval]


def metrics_with_simulator_scale(predicted, truth, distance, rotation):
    metrics = trajectory_metrics(predicted, truth)
    metrics.update(simulator_distance_m=float(distance), simulator_rotation_rad=float(rotation),
                   position_error_pct_simulator_distance=100*metrics['position_mae_m']/distance if distance > 1e-12 else None,
                   orientation_error_pct_simulator_rotation=100*metrics['orientation_mae_rad']/rotation if rotation > 1e-12 else None)
    return metrics


def summarize_experiment_metrics(rows):
    normalized = ('position_error_pct_simulator_distance', 'orientation_error_pct_simulator_rotation')
    summary = summarize_metrics([{key: value for key, value in row.items() if key not in normalized} for row in rows])
    for key in normalized:
        values = [row[key] for row in rows if row[key] is not None]
        summary['mean_'+key] = float(np.mean(values)) if values else None
        summary['std_'+key] = float(np.std(values)) if values else None
        summary[key+'_valid_trajectories'] = len(values)
    return summary


def _save_predictions(reference, path, split, mode, physics, hybrid, metadata, extra=None, shared=None):
    mask = reference.splits == split
    (path/'predictions').mkdir(parents=True, exist_ok=True)
    arrays = dict(time=reference.time, trajectory_ids=reference.ids[mask], families=reference.families[mask],
                  controls=reference.controls[mask], truth_states=reference.truth[mask],
                  physics_states=physics[mask], hybrid_states=hybrid[mask], metadata_json=json.dumps(metadata))
    arrays.update({key: value[mask] for key, value in (extra or {}).items()})
    arrays.update(shared or {})
    np.savez_compressed(path/'predictions'/f'{split}_{mode}.npz', **arrays)


def _plot_examples(reference, path, split, physics, hybrid, *, label, refresh_steps=None, forecast=None, all_families=False):
    from drone_sim.plotting import plot_prediction_comparison
    (path/'plots').mkdir(exist_ok=True)
    indices = np.flatnonzero(reference.splits == split)
    families = list(dict.fromkeys(reference.families[indices].tolist())) if all_families else (
        ['figure_eight'] if 'figure_eight' in reference.families[indices] else [str(reference.families[indices[0]])])
    for family in families:
        index = next(i for i in indices if reference.families[i] == family)
        plot_prediction_comparison(reference.time, reference.truth[index],
            {'Physics only': physics[index], 'Physics + NN': hybrid[index]},
            path/'plots'/f'{reference.ids[index]}_recursive.png', f'{split} | {family} | {label}',
            refresh_steps=refresh_steps,
            forecast_predictions=None if forecast is None else {'Physics only': forecast[0][index], 'Physics + NN': forecast[1][index]})


def evaluate_experiment(reference, predictor, output, checkpoint_info, *, all_families=False):
    reference.validate_predictor(predictor)
    output = Path(output)
    recursive = predictor.rollout(reference.truth[:, 0], reference.controls)
    one_step = reference.one_step_hybrid(predictor)
    results = []
    for split in ('test', 'benchmark'):
        rows, summaries = [], {}
        indices = np.flatnonzero(reference.splits == split)
        for mode, physics, hybrid in (('recursive', reference.physics_recursive, recursive),
                                     ('one_step', reference.physics_one_step, one_step)):
            summaries[mode] = {}
            _save_predictions(reference, output, split, mode, physics, hybrid,
                dict(mode=mode, split=split, truth_refresh=None, checkpoint=checkpoint_info,
                     control_source='recorded applied physical controls', physics_reference_cached=True))
            for name, states in (('physics_only', physics), ('hybrid', hybrid)):
                selected = [dict(trajectory_id=str(reference.ids[i]), split=split, family=str(reference.families[i]),
                                 predictor=name, mode=mode,
                                 **metrics_with_simulator_scale(states[i], reference.truth[i], reference.distance[i], reference.rotation[i]))
                            for i in indices]
                rows.extend(selected)
                summaries[mode][name] = summarize_experiment_metrics(selected)
        write_csv(output/f'{split}_trajectory_metrics.csv', rows)
        write_json(output/f'{split}_metrics.json', summaries)
        _plot_examples(reference, output, split, reference.physics_recursive, recursive,
                       label='Recursive; no truth refresh', all_families=all_families)
        results.append(dict(split=split, rows=rows, summaries=summaries))
    return save_evaluation_summaries(results, output)


def evaluate_refresh_experiment(reference, predictor, output, interval, checkpoint_info):
    reference.validate_predictor(predictor)
    output = Path(output)
    schedule = RefreshSchedule(interval_steps=interval)
    physics = reference.physics_refresh(interval)
    hybrid = rollout_with_refresh(predictor, reference.truth[:, 0], reference.controls, schedule=schedule,
                                  truth_provider=lambda step: reference.truth[:, step])
    metadata = physics.schedule_metadata
    results = {}
    for split in ('test', 'benchmark'):
        mask = reference.splits == split
        indices = np.flatnonzero(mask)
        extra = {}
        for prefix, result in (('physics', physics), ('hybrid', hybrid)):
            extra.update({f'{prefix}_forecast_states': result.forecast_states,
                          f'{prefix}_pre_refresh_states': result.pre_refresh_states,
                          f'{prefix}_corrected_refresh_states': result.corrected_refresh_states})
        _save_predictions(reference, output, split, 'recursive', physics.states, hybrid.states,
            dict(mode='recursive_with_truth_refresh' if interval else 'recursive', split=split,
                 truth_refresh=metadata if interval else None, checkpoint=checkpoint_info,
                 primary_metric_view='forecast_before_replacement', playback_state_view='state_after_replacement'), extra,
            shared={'refresh_steps': physics.refresh_steps, 'refresh_times': physics.refresh_steps*reference.physics.config.dt})
        rows, summaries, events, segments, drift = [], {}, [], [], []
        for view, attribute in (('forecast_before_replacement', 'forecast_states'), ('state_after_replacement', 'states')):
            summaries[view] = {}
            for name, result in (('physics_only', physics), ('hybrid', hybrid)):
                selected = [dict(trajectory_id=str(reference.ids[i]), split=split, family=str(reference.families[i]),
                                 predictor=name, mode='recursive', metric_view=view,
                                 **metrics_with_simulator_scale(getattr(result, attribute)[i], reference.truth[i], reference.distance[i], reference.rotation[i]))
                            for i in indices]
                rows.extend(selected)
                summaries[view][name] = summarize_experiment_metrics(selected)
        from dataclasses import replace
        for name, result in (('physics_only', physics), ('hybrid', hybrid)):
            selected_result = replace(result, forecast_states=result.forecast_states[mask], states=result.states[mask],
                pre_refresh_states=result.pre_refresh_states[mask], corrected_refresh_states=result.corrected_refresh_states[mask])
            e, s, d = drift_records(selected_result, reference.truth[mask], identifiers=reference.ids[mask], split=split,
                predictor=name, label='no_refresh' if interval is None else f'every_{interval}_steps', dt=reference.physics.config.dt)
            events.extend(e)
            segments.extend(s)
            drift.extend(d)
        write_csv(output/f'refresh_events_{split}.csv', events, EVENT_FIELDS)
        write_csv(output/f'segments_{split}.csv', segments, SEGMENT_FIELDS)
        write_csv(output/f'drift_metrics_{split}.csv', drift)
        write_csv(output/f'{split}_trajectory_metrics.csv', rows)
        write_json(output/f'{split}_metrics.json', summaries)
        _plot_examples(reference, output, split, physics.states, hybrid.states,
            label=f'Refresh {interval}; forecast errors before replacement', refresh_steps=physics.refresh_steps,
            forecast=(physics.forecast_states, hybrid.forecast_states))
        results[split] = summaries
    write_json(output/'refresh_schedule.json', metadata)
    write_json(output/'test_metrics.json', results)
    write_json(output/'rollout_metrics.json', results)
    write_csv(output/'rollout_metrics.csv', [row for split in ('test', 'benchmark')
              for row in csv.DictReader((output/f'{split}_trajectory_metrics.csv').open(encoding='utf-8'))])
    return results

"""Controlled subsets, complete epochs, honest percentages, caches, and reports."""

from dataclasses import replace
import csv
import json
from pathlib import Path

import numpy as np
import pytest
import torch

from drone_sim import DatasetConfig, SimulationConfig, generate_dataset, generate_benchmark_dataset
from drone_sim.evaluation import one_step_predictions, trajectory_metrics
from drone_sim.playback import load_comparison
from model_drone_residual import prepare_samples, train_model, TrainingConfig, HybridPredictor, save_training_outputs
from model_drone_residual.training import epoch_budget
from model_drone_residual.experiments import (ExperimentCase, experiment_designs, training_indices,
    select_training_dataset, select_prepared_samples, percent_reduction)
from model_drone_residual.experiment_evaluation import (ExperimentReference, evaluate_experiment,
    evaluate_refresh_experiment, metrics_with_simulator_scale, summarize_experiment_metrics)
from model_drone_residual.experiment_reporting import pairwise_comparisons, write_experiment_reports, write_seed_report


@pytest.fixture(scope='module')
def sources():
    config = DatasetConfig(train_count=20, validation_count=2, test_count=2, benchmark_count=2,
                           simulation=SimulationConfig(duration=.05), seed=96)
    return generate_dataset(config), generate_benchmark_dataset(config)


@pytest.mark.parametrize('count,batch,requested,epochs,updates', [
    (80000, 256, 10000, 32, 10016), (40000, 256, 10000, 64, 10048),
    (20000, 256, 10000, 127, 10033), (10000, 256, 10000, 250, 10000),
    (80000, 256, 5000, 16, 5008), (80000, 256, 15000, 48, 15024),
    (80000, 256, 20000, 64, 20032), (15, 4, 6, 2, 8)])
def test_complete_epoch_rounding(count, batch, requested, epochs, updates):
    result = epoch_budget(count, batch, requested)
    assert result['planned_complete_epochs'] == epochs
    assert result['planned_optimizer_updates'] == updates
    assert updates >= requested and updates-requested < result['batches_per_complete_epoch']


def test_full_design_changes_one_factor_and_reuses_baselines():
    cases, groups = experiment_designs()
    assert len(cases) == 12
    assert [cases[name].train_count for name in groups['A']] == [10, 20, 40, 80]
    assert [cases[name].requested_updates for name in groups['C']] == [5000, 10000, 15000, 20000]
    assert {(cases[name].hidden_layers, cases[name].hidden_size) for name in groups['D']} == {(2, 32), (2, 64), (2, 128), (1, 64), (4, 64)}
    assert cases['restricted_20'].train_count == cases['broad_20'].train_count
    assert all(cases[name].requested_updates == 10000 for name in groups['D'])


def test_nested_subsets_preserve_all_held_out_arrays_and_family_balance(sources):
    main, _ = sources
    small = select_training_dataset(main, ExperimentCase('small', 'small', train_count=10))
    broad = select_training_dataset(main, ExperimentCase('broad', 'broad', train_count=20))
    assert set(small.trajectory_ids[small.split == 'train']) < set(broad.trajectory_ids[broad.split == 'train'])
    assert sorted(small.metadata['experiment_training_selection']['family_counts'].values()) == [2]*5
    for split in ('validation', 'test'):
        for name in ('states', 'controls', 'families', 'trajectory_ids'):
            np.testing.assert_array_equal(getattr(small, name)[small.split == split], getattr(main, name)[main.split == split])
    restricted = select_training_dataset(main, ExperimentCase('restricted', 'restricted', train_count=8,
                                                             restricted_families=('circle', 'figure_eight')))
    assert restricted.metadata['experiment_training_selection']['family_counts'] == {'circle': 4, 'figure_eight': 4}
    assert main.metadata['config']['train_count'] == 20
    with pytest.raises(ValueError):
        training_indices(main, ExperimentCase('invalid', 'invalid', train_count=100))


def test_prepared_cache_matches_uncached_training_and_rejects_mismatched_controls(sources):
    main, _ = sources
    data = select_training_dataset(main, ExperimentCase('small', 'small', train_count=3))
    cached = select_prepared_samples(prepare_samples(main, 'train'), data.trajectory_ids[data.split == 'train'])
    validation = prepare_samples(main, 'validation')
    config = TrainingConfig(optimizer_updates=6, batch_size=4, hidden_size=4, hidden_layers=1, validation_interval=4)
    a = train_model(data, config, prepared_samples=(cached, validation))
    b = train_model(data, config)
    assert a.summary['optimizer_updates'] == 8 and a.summary['samples_processed'] == 30
    for key in a.final_checkpoint['model_state_dict']:
        torch.testing.assert_close(a.final_checkpoint['model_state_dict'][key], b.final_checkpoint['model_state_dict'][key], rtol=0, atol=0)
    altered = replace(cached, features=cached.features+1)
    with pytest.raises(ValueError, match='cached residual samples'):
        train_model(data, config, prepared_samples=(altered, validation))


@pytest.mark.parametrize('candidate,reference,expected', [(1, 4, 75), (6, 4, -50), (4, 4, 0), (0, 4, 100), (0, 0, None), (1, 0, None)])
def test_percentage_definitions_and_zero_denominators(candidate, reference, expected):
    assert percent_reduction(candidate, reference) == expected


def test_simulator_percentages_are_per_flight_ratios_and_zero_motion_is_na(sources):
    main, _ = sources
    truth = main.states[0]
    prediction = truth.copy()
    prediction[1:, 0] += .2
    a = metrics_with_simulator_scale(prediction, truth, 2., 1.)
    b = metrics_with_simulator_scale(prediction, truth, 4., 2.)
    assert a['position_error_pct_simulator_distance'] == pytest.approx(10.)
    assert summarize_experiment_metrics([a, b])['mean_position_error_pct_simulator_distance'] == pytest.approx(7.5)
    stationary = metrics_with_simulator_scale(prediction, truth, 0., 0.)
    assert stationary['position_error_pct_simulator_distance'] is None
    assert summarize_experiment_metrics([stationary])['mean_position_error_pct_simulator_distance'] is None


def test_cached_evaluation_and_refresh_preserve_reference_and_match_old_interfaces(tmp_path, sources):
    main, benchmark = sources
    data = select_training_dataset(main, ExperimentCase('small', 'small', train_count=3))
    fitted = train_model(data, TrainingConfig(optimizer_updates=2, batch_size=4, hidden_size=4, hidden_layers=1))
    predictor = HybridPredictor(fitted.model, fitted.standardizers, fitted.physics)
    reference = ExperimentReference(main, benchmark)
    truth_before = reference.truth.copy()
    summary = evaluate_experiment(reference, predictor, tmp_path/'baseline', {})
    for split in ('test', 'benchmark'):
        with np.load(tmp_path/'baseline/predictions'/f'{split}_one_step.npz') as archive:
            expected = one_step_predictions(predictor, archive['truth_states'], archive['controls'])
            # Float32 NN matrix kernels can round differently for combined
            # versus split evaluation batches; physical corrections are tiny.
            np.testing.assert_allclose(archive['hybrid_states'], expected, atol=1e-10, rtol=0)
    refresh = evaluate_refresh_experiment(reference, predictor, tmp_path/'refresh', 1, {})
    with np.load(tmp_path/'refresh/predictions/test_recursive.npz') as archive:
        np.testing.assert_array_equal(archive['hybrid_states'][:, 1:], archive['truth_states'][:, 1:])
        np.testing.assert_array_equal(archive['refresh_steps'], [1, 2, 3, 4, 5])
        assert archive['hybrid_pre_refresh_states'].shape == (2, 5, 13)
    assert refresh['test']['forecast_before_replacement']['hybrid']['mean_position_mae_m'] > 0
    assert refresh['test']['state_after_replacement']['hybrid']['mean_position_mae_m'] == 0
    none = evaluate_refresh_experiment(reference, predictor, tmp_path/'none', None, {})
    assert none['test']['forecast_before_replacement']['hybrid']['mean_position_mae_m'] == summary['test']['recursive']['hybrid']['mean_position_mae_m']
    np.testing.assert_array_equal(reference.truth, truth_before)
    assert reference.physics_refresh(1) is reference.physics_refresh(1)
    assert load_comparison(tmp_path/'refresh/predictions/test_recursive.npz').default_mode == 'both'


def test_pairwise_comparisons_and_readable_reports(tmp_path):
    def metrics(value):
        return dict(mean_position_mae_m=value, mean_orientation_mae_rad=value, mean_orientation_mae_deg=value,
                    mean_position_error_pct_simulator_distance=value, mean_orientation_error_pct_simulator_rotation=value,
                    std_position_mae_m=0., std_orientation_mae_deg=0., std_orientation_mae_rad=0.)
    training = dict(requested_optimizer_updates=5, optimizer_updates=8, completed_epochs=2, trainable_parameters=100,
                    training_seconds=1.)
    groups = {}
    for name, value in (('broad_10', 1.), ('broad_20', 4.)):
        groups[name] = []
        for seed in (0, 1, 2):
            output = tmp_path/'Experiment A - Trajectory Quantity'/name/f'seed_{seed}'
            output.mkdir(parents=True)
            summary = {split: {mode: dict(hybrid=metrics(value), physics_only=metrics(8.)) for mode in ('recursive', 'one_step')}
                       for split in ('test', 'benchmark')}
            groups[name].append(dict(case=name, label=name, seed=seed, output=output.as_posix(), training_summary=training,
                checkpoint=dict(optimizer_updates=4), metrics=summary, report_filename='Experiment A - Trajectory Quantity Data.md'))
    pairs = pairwise_comparisons('Trajectory Quantity', groups)
    selected = [r for r in pairs if r['candidate'] == 'broad_10' and r['reference'] == 'broad_20' and r['predictor'] == 'hybrid']
    assert len(selected) == 32 and all(row['error_reduction_pct'] == 75 for row in selected)
    write_experiment_reports(tmp_path, dict(experiments=['A'], groups={'A': list(groups)}), sum(groups.values(), []), [])
    text = (tmp_path/'Phase 7 Data.md').read_text(encoding='utf-8')
    assert '## Experiment: Trajectory Quantity' in text and '#### Seed 0' in text
    assert '75%' in text and '- Mean position MAE against MuJoCo: **1 m**.' in text
    assert '](' in text and '](<Experiment A - Trajectory Quantity/' in text
    standalone = (tmp_path/'Experiment A - Trajectory Quantity/Experiment A - Trajectory Quantity Data.md').read_text()
    assert '](<broad_10/seed_0/>)' in standalone

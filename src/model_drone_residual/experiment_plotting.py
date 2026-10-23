"""Scientific comparison plots for controlled drone learning experiments."""

from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from model_drone_residual.experiment_reporting import aggregate_runs, condition_label
from model_drone_residual.experiments import EXPERIMENT_NAMES


def plot_experiments(root, manifest, records, refresh_records):
    for letter in manifest['experiments']:
        source = refresh_records if letter == 'E' else records
        names = list(dict.fromkeys(r['case'] for r in refresh_records)) if letter == 'E' else manifest['groups'][letter]
        groups = {name: [r for r in source if r['case'] == name] for name in names}
        if not groups or any(not group for group in groups.values()):
            continue
        summaries = {name: aggregate_runs(runs) for name, runs in groups.items()}
        labels = [condition_label(letter, name, groups[name]) for name in names]
        folder = Path(root)/f'Experiment {letter} - {EXPERIMENT_NAMES[letter]}'/'plots'
        folder.mkdir(parents=True, exist_ok=True)
        fig, axes = plt.subplots(2, 2, figsize=(14, 10), constrained_layout=True)
        for row, split in enumerate(('test', 'benchmark')):
            for column, (key, unit) in enumerate((('mean_position_mae_m', 'Position MAE [m]'),
                                                   ('mean_orientation_mae_deg', 'Orientation MAE [deg]'))):
                ax = axes[row, column]
                for predictor, label, color in (('physics_only', 'Physics only', 'tab:blue'), ('hybrid', 'Physics + NN', 'tab:orange')):
                    mean = [summaries[name][split]['recursive'][predictor][key] for name in names]
                    ax.plot(np.arange(len(names)), mean, 'o-', color=color, label=label)
                    for i, name in enumerate(names):
                        values = [run['metrics'][split]['recursive'][predictor][key] for run in groups[name]]
                        ax.scatter(i+np.linspace(-.045, .045, len(values)), values, color=color, alpha=.3, s=18)
                ax.set(yscale='log', ylabel=f'{split.capitalize()}: {unit}', xticks=np.arange(len(names)), xticklabels=labels)
                ax.tick_params(axis='x', labelrotation=25, labelsize=8)
                ax.grid(alpha=.25)
                ax.legend()
        fig.suptitle(f'Experiment: {EXPERIMENT_NAMES[letter]}\nRecursive errors against MuJoCo; lines = seed means; faint dots = individual seeds')
        fig.savefig(folder/'comparison_mae.png', dpi=150)
        plt.close(fig)
        if letter == 'E':
            fig, axes = plt.subplots(2, 2, figsize=(12, 8), constrained_layout=True)
            counts = [groups[name][0]['refresh_count'] for name in names]
            order = np.argsort(counts)
            for row, split in enumerate(('test', 'benchmark')):
                for column, key in enumerate(('mean_position_mae_m', 'mean_orientation_mae_deg')):
                    for predictor, label, color in (('physics_only', 'Physics only', 'tab:blue'), ('hybrid', 'Physics + NN', 'tab:orange')):
                        values = np.array([summaries[name][split]['recursive'][predictor][key] for name in names])
                        axes[row, column].plot(np.asarray(counts)[order], values[order], 'o-', color=color, label=label)
                    axes[row, column].set(xscale='symlog', yscale='log', xlabel='Refresh count per flight; includes final-step events',
                        ylabel=f'{split}: '+('Position MAE [m]' if column == 0 else 'Orientation MAE [deg]'))
                    axes[row, column].grid(alpha=.25)
                    axes[row, column].legend()
            fig.suptitle('Experiment: Refresh Frequency\nSeed-mean forecast errors BEFORE replacement; zero count = no refresh')
            fig.savefig(folder/'refresh_count_mae.png', dpi=150)
            plt.close(fig)

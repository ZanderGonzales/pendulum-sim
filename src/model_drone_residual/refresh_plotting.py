"""Refresh-frequency comparisons of pre-replacement position/orientation MAE."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from model_drone_residual.refresh_evaluation import PRIMARY_VIEW


def plot_refresh_frequency(results: list[dict], output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    for split in dict.fromkeys(result["split"] for result in results):
        selected = [result for result in results if result["split"] == split]
        labels, counts = [], []
        for result in selected:
            requested, metadata = result["schedule"]["requested"], result["schedule"]
            interval = requested["interval_steps"]
            if interval is None and requested["interval_seconds"] is not None:
                interval = round(requested["interval_seconds"]/metadata["dt_s"])
            labels.append(str(interval) if interval is not None else "None" if not metadata["refresh_count"] else "Explicit")
            counts.append(metadata["refresh_count"])
        fig, axes = plt.subplots(2, 2, figsize=(12, 8), constrained_layout=True)
        for name, display, color in (("physics_only", "Physics only", "tab:blue"), ("hybrid", "Physics + NN", "tab:orange")):
            for column, (metric, unit, factor) in enumerate((("position_mae_m", "Position MAE [m]", 1.),
                                                           ("orientation_mae_rad", "Orientation MAE [deg]", 180/np.pi))):
                values = np.array([result["summaries"][PRIMARY_VIEW][name]["mean_"+metric] for result in selected])*factor
                axes[0, column].plot(np.arange(len(selected)), values, "o-", color=color, label=display)
                order = np.argsort(counts)
                axes[1, column].plot(np.asarray(counts)[order], values[order], "o-", color=color, label=display)
                axes[0, column].set(xticks=np.arange(len(labels)), xticklabels=labels,
                                    xlabel="Refresh interval [steps; categorical cases]", ylabel=unit, yscale="log")
                axes[1, column].set(xlabel="Refresh count per trajectory (includes final-step events)", ylabel=unit,
                                    xscale="symlog", yscale="log")
        for ax in axes.flat:
            ax.grid(alpha=.25)
            ax.legend()
        fig.suptitle(f"{split}: equal-flight mean forecast errors BEFORE truth replacement\nNone = no refresh; weights fixed for every schedule")
        fig.savefig(output/f"refresh_frequency_{split}.png", dpi=150)
        plt.close(fig)

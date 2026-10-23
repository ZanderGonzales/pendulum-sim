"""Optimizer-update loss curves; flight plots use drone_sim.plotting."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def plot_loss_curves(history: list[dict], output: str | Path, best_update: int) -> None:
    fig, ax = plt.subplots(figsize=(10, 5), constrained_layout=True)
    updates = [row["optimizer_updates"] for row in history]
    ax.semilogy(updates, [row["train_loss"] for row in history], label="Training: full-split MSE")
    ax.semilogy(updates, [row["validation_loss"] for row in history], label="Validation: full-split MSE")
    ax.axvline(best_update, linestyle=":", color="tab:green", label=f"Selected checkpoint: update {best_update:,}")
    ax.set(xlabel="Optimizer updates", ylabel="Standardized residual MSE", title="Drone residual learning")
    ax.grid(alpha=.25)
    ax.legend()
    fig.savefig(output, dpi=150)
    plt.close(fig)

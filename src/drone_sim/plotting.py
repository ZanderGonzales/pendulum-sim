"""Reference-flight, dataset-coverage, and independent physics diagnostic plots."""

from pathlib import Path
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def plot_flight(trajectory, output: Path, family: str) -> None:
    """Plot state, tracking error, and actual applied wrench on one time grid."""
    output.mkdir(parents=True, exist_ok=True)
    states, time = trajectory.states, trajectory.time
    fig, axes = plt.subplots(4, 1, figsize=(10, 11), sharex=True, constrained_layout=True)
    colors = ("tab:blue", "tab:orange", "tab:green")
    for axis, label, color in zip(range(3), ("x", "y", "z"), colors):
        axes[0].plot(time, states[:, axis], color=color, label=f"{label} simulated")
        axes[0].plot(time, trajectory.reference_positions[:, axis], "--", color=color, alpha=.65,
                     label=f"{label} reference")
        axes[1].plot(time, states[:, 7+axis], color=color, label=f"v{label}")
        if len(trajectory.controls):
            axes[3].plot(time[:-1], trajectory.controls[:, 1+axis]*1e6, color=color, label=f"moment {label}")
    axes[2].plot(time, np.linalg.norm(states[:, :3] - trajectory.reference_positions, axis=1), color="tab:red")
    axes[0].set_ylabel("Position [m]")
    axes[1].set_ylabel("Velocity [m/s]")
    axes[2].set_ylabel("Tracking distance [m]")
    axes[3].set(ylabel="Applied moment [micro N m]", xlabel="Time [s]")
    for ax in axes:
        ax.grid(alpha=.25)
    axes[0].legend(ncol=3, fontsize=8)
    axes[1].legend(ncol=3)
    axes[3].legend(ncol=3)
    fig.suptitle(f"Crazyflie reference flight: {family} | {'valid' if trajectory.valid_for_learning else 'rejected'}")
    fig.savefig(output / f"{family}_state_comparison.png", dpi=150)
    plt.close(fig)


def plot_path_summary(trajectories: dict, output: Path, *,
                      title: str = "Crazyflie Phase 1: six controlled MuJoCo flight families") -> None:
    fig = plt.figure(figsize=(14, 8), constrained_layout=True)
    for index, (family, flight) in enumerate(trajectories.items(), start=1):
        ax = fig.add_subplot(2, 3, index, projection="3d")
        ax.plot(*flight.reference_positions.T, "--", color="tab:orange", label="Controller reference")
        ax.plot(*flight.states[:, :3].T, color="tab:blue", label="MuJoCo flight")
        ax.scatter(*flight.states[0, :3], color="black", s=15)
        points = np.vstack((flight.states[:, :3], flight.reference_positions))
        center = (points.max(axis=0) + points.min(axis=0))/2
        half = max(.05, float(np.ptp(points, axis=0).max())/2) * 1.15
        ax.set(xlim=(center[0]-half, center[0]+half), ylim=(center[1]-half, center[1]+half),
               zlim=(center[2]-half, center[2]+half), xlabel="x [m]", ylabel="y [m]", zlabel="z [m]",
               title=family.replace("_", " "))
        ax.set_box_aspect((1, 1, 1))
        ax.legend(fontsize=7, loc="upper left")
    fig.suptitle(title)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=160)
    plt.close(fig)


def plot_dataset_coverage(dataset, benchmark, output: Path) -> None:
    """Compare main splits and the separately held-out family in physical units."""
    from drone_sim.controls import FLIGHT_FAMILIES

    output.mkdir(parents=True, exist_ok=True)
    colors = {"train": "tab:blue", "validation": "tab:orange", "test": "tab:green", "benchmark": "tab:purple"}
    groups = [(label, source, source.split == label) for source in (dataset, benchmark)
              for label in dict.fromkeys(source.split.tolist())]

    def histograms(ax, values, xlabel):
        all_values = np.concatenate([value.ravel() for _, value in values])
        bins = np.histogram_bin_edges(all_values, bins=40)
        for label, value in values:
            ax.hist(value.ravel(), bins=bins, density=True, histtype="step", linewidth=1.5,
                    label=label, color=colors[label])
        ax.set(xlabel=xlabel, ylabel="Density")
        ax.grid(alpha=.2)
        ax.legend(fontsize=8)

    fig, axes = plt.subplots(2, 3, figsize=(14, 8), constrained_layout=True)
    for label, source, mask in groups:
        stride = max(1, len(source.time)//100)
        states = source.states[mask, ::stride]
        axes[0, 0].scatter(states[:, :, 0], states[:, :, 1], s=3, alpha=.2, color=colors[label], label=label)
        initial = source.states[mask, 0]
        axes[1, 2].scatter(initial[:, 0], initial[:, 1], s=22, color=colors[label], label=label)
    axes[0, 0].set(xlabel="World x [m]", ylabel="World y [m]", title="Position coverage (subsampled)")
    axes[1, 2].set(xlabel="Initial x [m]", ylabel="Initial y [m]", title="Initial placement")
    for ax in (axes[0, 0], axes[1, 2]):
        ax.legend(fontsize=8)
        ax.grid(alpha=.2)
        ax.set_aspect("equal", adjustable="datalim")
    histograms(axes[0, 1], [(l, s.states[m, :, 2]) for l, s, m in groups], "Height [m]")
    histograms(axes[0, 2], [(l, np.linalg.norm(s.states[m, :, 7:10], axis=-1)) for l, s, m in groups], "Linear speed [m/s]")
    histograms(axes[1, 0], [(l, np.linalg.norm(s.states[m, :, 10:13], axis=-1)) for l, s, m in groups], "Angular speed [rad/s]")
    histograms(axes[1, 1], [(l, np.rad2deg(np.arccos(np.clip(1-2*(s.states[m, :, 4]**2+s.states[m, :, 5]**2), -1, 1))))
                           for l, s, m in groups], "Tilt from vertical [degrees]")
    fig.suptitle("Drone state coverage | benchmark = unseen trajectory family")
    fig.savefig(output / "state_coverage.png", dpi=150)
    plt.close(fig)

    fig, axes = plt.subplots(2, 2, figsize=(12, 7), constrained_layout=True)
    for index, ax in enumerate(axes.flat):
        factor = 1. if index == 0 else 1e6
        histograms(ax, [(l, s.controls[m, :, index]*factor) for l, s, m in groups],
                   "Applied thrust [N]" if index == 0 else f"Applied moment {'xyz'[index-1]} [micro N m]")
    fig.suptitle("Actual applied controls, after actuator limits")
    fig.savefig(output / "control_coverage.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(11, 5), constrained_layout=True)
    locations = np.arange(len(FLIGHT_FAMILIES))
    width = .18
    maximum_count = 1
    for i, (label, source, mask) in enumerate(groups):
        counts = [np.count_nonzero(source.families[mask] == family) for family in FLIGHT_FAMILIES]
        maximum_count = max(maximum_count, max(counts))
        bars = ax.bar(locations+(i-1.5)*width, counts, width, label=label, color=colors[label])
        ax.bar_label(bars, labels=[str(n) if n else "" for n in counts], fontsize=8, padding=2)
    ax.set(xticks=locations, xticklabels=FLIGHT_FAMILIES, ylabel="Complete trajectories", title="Trajectory families by split")
    ax.set_ylim(0, maximum_count*1.2)
    ax.legend()
    ax.grid(axis="y", alpha=.2)
    fig.savefig(output / "trajectory_family_counts.png", dpi=150)
    plt.close(fig)


def plot_physics_flight(time, truth, prediction, output: Path, title: str) -> None:
    """Physics comparison using the current path-and-two-errors layout."""
    plot_prediction_comparison(time, truth, {"Physics recursive": prediction}, output, title)


def plot_prediction_comparison(time, truth, predictions: dict, output: Path, title: str, *,
                              refresh_steps=None, forecast_predictions: dict | None = None) -> None:
    """Large 3D path above position and orientation errors; no projections/components."""
    from drone_sim.evaluation import state_errors

    fig = plt.figure(figsize=(13, 12), constrained_layout=True)
    grid = fig.add_gridspec(2, 2, height_ratios=(2.5, 1))
    path = fig.add_subplot(grid[0, :], projection="3d")
    position, orientation = fig.add_subplot(grid[1, 0]), fig.add_subplot(grid[1, 1])
    events = np.asarray(refresh_steps if refresh_steps is not None else [], dtype=int)
    marked = events[np.unique(np.linspace(0, len(events)-1, min(len(events), 40), dtype=int))] if len(events) else events
    path.plot(*truth[:, :3].T, color="black", linewidth=2.4, label="MuJoCo reference")
    path.scatter(*truth[0, :3], color="black", s=30, label="Initial position")
    for index, (label, values) in enumerate(predictions.items()):
        color = plt.get_cmap("tab10")(index)
        style = ("--", ":", "-.")[index % 3]
        forecast = forecast_predictions[label] if forecast_predictions is not None else values
        errors = state_errors(forecast, truth)
        path.plot(*values[:, :3].T, linestyle=style, color=color, linewidth=1.8, label=label)
        position.plot(time, errors["position_m"], color=color, linestyle=style, label=label)
        orientation.plot(time, np.degrees(errors["orientation_rad"]), color=color, linestyle=style, label=label)
        if len(marked):
            path.scatter(*forecast[marked, :3].T, s=12, facecolors="none", edgecolors=[color], alpha=.6)
            position.plot(time[marked], errors["position_m"][marked], ".", color=color, markersize=3)
            orientation.plot(time[marked], np.degrees(errors["orientation_rad"][marked]), ".", color=color, markersize=3)
    if len(events):
        note = f"Truth refresh: {len(events)} events"
        if len(marked) != len(events):
            note += f" ({len(marked)} path markers)"
        path.scatter(*truth[marked, :3].T, color="tab:green", marker="x", s=16, alpha=.6, label=note)
        for ax in (position, orientation):
            ax.plot(time[events], np.full(len(events), .02), "|", color="tab:green", alpha=.5,
                    transform=ax.get_xaxis_transform(), markersize=5, label="Truth refresh (all events)")
            ax.plot(time[marked], np.zeros(len(marked)), "x", color="tab:green", markersize=3, alpha=.5)
            if len(events) <= 25:
                for event in events:
                    ax.axvline(time[event], color="tab:green", alpha=.12, linewidth=.7)
    path.set(xlabel="World x [m]", ylabel="World y [m]", zlabel="World z [m]", title="3D flight path comparison")
    path.set_box_aspect((1.2, 1., .8))
    path.legend(loc="upper left", fontsize=9)
    qualifier = "Forecast " if forecast_predictions is not None else ""
    position.set(xlabel="Time [s]", ylabel=f"{qualifier}position error [m]")
    orientation.set(xlabel="Time [s]", ylabel=f"{qualifier}orientation angle error [deg]")
    for ax in (position, orientation):
        ax.grid(alpha=.25)
        ax.legend(fontsize=8)
    fig.suptitle(title)
    fig.savefig(output, dpi=150)
    plt.close(fig)


def plot_physics_errors(time, groups: dict, output: Path, title: str) -> None:
    """Groups map split labels to (prediction,truth); bands are +/- one std."""
    from drone_sim.evaluation import state_errors

    fig, axes = plt.subplots(1, 2, figsize=(12, 4), constrained_layout=True)
    names = ("position_m", "orientation_rad")
    labels = ("Position error [m]", "Orientation error [deg]")
    for label, (prediction, truth) in groups.items():
        errors = state_errors(prediction, truth)
        for ax, name in zip(axes.flat, names):
            value = np.degrees(errors[name]) if name == "orientation_rad" else errors[name]
            mean, std = value.mean(axis=0), value.std(axis=0)
            line, = ax.plot(time[1:], mean[1:], label=label)
            ax.fill_between(time[1:], np.maximum(0, mean[1:]-std[1:]), mean[1:]+std[1:],
                            color=line.get_color(), alpha=.15)
    for ax, label in zip(axes.flat, labels):
        ax.set(xlabel="Time [s]", ylabel=label)
        ax.grid(alpha=.25)
        ax.legend()
    fig.suptitle(title+"\nMean across trajectories; shaded bands: +/- one standard deviation")
    fig.savefig(output, dpi=150)
    plt.close(fig)


def plot_fluid_isolation(arrays: dict, output: Path) -> None:
    """Show the measured numerical gap alongside the normal reference residual."""
    from drone_sim.evaluation import state_errors

    fig, axes = plt.subplots(1, 2, figsize=(11, 4), constrained_layout=True)
    names = ("position_m", "orientation_rad")
    labels = ("Position [m]", "Orientation [rad]")
    for label, key in (("Fluid off", "fluid_off_next"), ("Normal reference", "normal_next")):
        errors = state_errors(arrays["physics_next"], arrays[key])
        for ax, name in zip(axes.flat, names):
            ax.plot(np.arange(1, len(errors[name])+1), np.maximum(errors[name], 1e-18), ".",
                    label=label, markersize=2, alpha=.6)
    for ax, label in zip(axes.flat, labels):
        ax.set(yscale="log", xlabel="Fixed training-state diagnostic sample", ylabel=label)
        ax.grid(alpha=.25)
        ax.legend()
    fig.suptitle("One-step physics error: matched states and controls\nValues below 1e-18 are shown at the plotting floor")
    fig.savefig(output, dpi=150)
    plt.close(fig)

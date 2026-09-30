from types import SimpleNamespace

from model_baseline.experiments import (
    build_baseline_experiment_case,
    build_extended_baseline_experiment_case,
)
from model_baseline.baseline_runner import (
    next_run_directory,
    save_experiment_data_note,
)


def make_training_result():
    return SimpleNamespace(
        training_config={
            "batch_size": 256,
            "max_epochs": 100,
            "max_optimizer_steps": 5000,
            "learning_rate": 1e-3,
            "scheduler_factor": 0.5,
            "scheduler_patience": 10,
            "min_learning_rate": 1e-6,
        },
        history={
            "epoch": [16.0],
            "optimizer_step": [5008.0],
            "samples_seen": [1281280.0],
        },
    )


def test_next_baseline_run_uses_next_number(tmp_path) -> None:
    (tmp_path / "baseline_runs_0").mkdir()

    assert next_run_directory(tmp_path) == tmp_path / "baseline_runs_1"


def test_experiment_note_describes_grid_and_saved_run(tmp_path) -> None:
    case = build_baseline_experiment_case()
    output_dir = tmp_path / "baseline_runs_1"
    output_dir.mkdir()

    save_experiment_data_note(case, make_training_result(), output_dir)
    note = (output_dir / "Experiment 1 Data.md").read_text(encoding="utf-8")

    assert "32 training" in note
    assert "Cartesian product" in note
    assert "## Changes From Experiment 0" in note
    assert "## Training Procedure" in note
    assert "5008 updates" in note
    assert "baseline_checkpoint.pt" in note
    assert "baseline_test_error_data.csv" in note


def test_experiment_two_note_records_differences_from_experiment_one(tmp_path) -> None:
    case = build_extended_baseline_experiment_case()
    output_dir = tmp_path / "baseline_runs_2"
    output_dir.mkdir()

    save_experiment_data_note(case, make_training_result(), output_dir)
    note = (output_dir / "Experiment 2 Data.md").read_text(encoding="utf-8")

    assert "80 training, 10 validation, 10 test" in note
    assert "-1.4000" in note
    assert "Cartesian product" in note
    assert "## Changes From Experiment 1" in note
    assert "32 to 80" in note

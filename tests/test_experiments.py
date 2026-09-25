from pendulum_sim.experiments import (
    build_data_quantity_cases,
    build_experiment_cases,
    summarize_case_metrics,
)


def test_build_experiment_cases_returns_multiple_regimes() -> None:
    cases = build_experiment_cases()

    assert len(cases) >= 2
    for case in cases:
        assert case["name"]
        assert case["train_configs"]
        assert case["test_configs"]


def test_summarize_case_metrics_returns_numeric_fields() -> None:
    summary = summarize_case_metrics(
        train_loss=0.01,
        validation_loss=0.02,
        mae=0.03,
        rmse=0.04,
        max_absolute_error=0.05,
    )

    assert summary["train_loss"] == 0.01
    assert summary["validation_loss"] == 0.02
    assert summary["mae"] == 0.03
    assert summary["rmse"] == 0.04
    assert summary["max_absolute_error"] == 0.05


def test_data_quantity_cases_share_test_conditions_and_nest_training_data() -> None:
    cases = build_data_quantity_cases(train_sizes=(4, 8, 16))

    assert [len(case["train_configs"]) for case in cases] == [4, 8, 16]
    assert cases[0]["test_configs"] is cases[1]["test_configs"]
    assert cases[1]["test_configs"] is cases[2]["test_configs"]
    assert cases[0]["train_configs"] == cases[1]["train_configs"][:4]
    assert cases[1]["train_configs"] == cases[2]["train_configs"][:8]

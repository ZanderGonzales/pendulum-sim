from model_baseline.experiments import (
    build_baseline_experiment_case,
    build_data_quantity_cases,
    build_extended_baseline_experiment_case,
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


def test_baseline_experiment_uses_full_initial_condition_grid() -> None:
    baseline_case = build_baseline_experiment_case()
    train_configs = baseline_case["train_configs"]
    theta_values = {config.theta0 for config in train_configs}
    omega_values = {config.omega0 for config in train_configs}
    observed_pairs = {(config.theta0, config.omega0) for config in train_configs}

    assert len(train_configs) == 32
    assert len(theta_values) == 8
    assert len(omega_values) == 4
    assert observed_pairs == {
        (theta0, omega0)
        for theta0 in theta_values
        for omega0 in omega_values
    }

    prior_case = build_data_quantity_cases(train_sizes=(32,))[0]

    def conditions(configs):
        return [
            (config.theta0, config.omega0, config.torque_parameters["slope"])
            for config in configs
        ]

    assert conditions(baseline_case["validation_configs"]) == conditions(
        prior_case["validation_configs"]
    )
    assert conditions(baseline_case["test_configs"]) == conditions(
        prior_case["test_configs"]
    )


def test_experiment_two_uses_100_trajectories_and_wider_grid() -> None:
    experiment = build_extended_baseline_experiment_case()
    train_configs = experiment["train_configs"]
    theta_values = {config.theta0 for config in train_configs}
    omega_values = {config.omega0 for config in train_configs}
    observed_pairs = {(config.theta0, config.omega0) for config in train_configs}

    assert (len(train_configs), len(experiment["validation_configs"]), len(experiment["test_configs"])) == (80, 10, 10)
    assert len(theta_values) == 10
    assert len(omega_values) == 8
    assert min(theta_values) == -1.4
    assert max(theta_values) == 1.4
    assert min(omega_values) == -1.0
    assert max(omega_values) == 1.0
    assert observed_pairs == {
        (theta0, omega0)
        for theta0 in theta_values
        for omega0 in omega_values
    }

    experiment_one_test = build_baseline_experiment_case()["test_configs"]
    assert [
        (config.theta0, config.omega0, config.torque_parameters["slope"])
        for config in experiment["test_configs"][:4]
    ] == [
        (config.theta0, config.omega0, config.torque_parameters["slope"])
        for config in experiment_one_test
    ]

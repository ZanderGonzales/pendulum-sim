from __future__ import annotations

from model_baseline.baseline_runner import run_baseline_case
from model_baseline.experiments import build_extended_baseline_experiment_case


def main() -> None:
    seed = 7
    case = build_extended_baseline_experiment_case(seed=seed)
    run_baseline_case(case, seed=seed)


if __name__ == "__main__":
    main()

import numpy as np

from pendulum_sim.simulator import PendulumParameters, simulate_pendulum


def test_zero_torque_and_zero_initial_conditions_stay_at_rest() -> None:
    params = PendulumParameters(mass=1.0, length=1.0, gravity=9.81, damping=0.0)
    result = simulate_pendulum(
        duration=1.0,
        num_steps=100,
        theta0=0.0,
        omega0=0.0,
        params=params,
        torque_fn=lambda t: 0.0,
    )

    assert result["theta"].shape == (101,)
    assert result["omega"].shape == (101,)
    assert np.allclose(result["theta"], 0.0)
    assert np.allclose(result["omega"], 0.0)


def test_damped_motion_decays_over_time() -> None:
    params = PendulumParameters(mass=1.0, length=1.0, gravity=9.81, damping=0.5)
    result = simulate_pendulum(
        duration=2.0,
        num_steps=400,
        theta0=0.5,
        omega0=1.0,
        params=params,
        torque_fn=lambda t: 0.0,
    )

    assert np.abs(result["theta"][0]) > np.abs(result["theta"][-1])
    assert np.abs(result["omega"][0]) > 0.0
    assert np.abs(result["omega"][0]) >= np.abs(result["omega"][-1])

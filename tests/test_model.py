import torch

from model_baseline.model import PendulumStateNetwork, Standardizer


def test_standardizer_round_trip_and_constant_feature() -> None:
    values = torch.tensor([[0.0, 2.0], [2.0, 2.0], [4.0, 2.0]])
    standardizer = Standardizer.fit(values)
    transformed = standardizer.transform(values)

    assert torch.allclose(standardizer.inverse_transform(transformed), values)
    assert torch.allclose(transformed[:, 1], torch.zeros(3))


def test_network_predicts_full_state_and_supports_backpropagation() -> None:
    model = PendulumStateNetwork(hidden_size=16)
    inputs = torch.randn(12, 4, requires_grad=True)

    outputs = model(inputs)
    loss = outputs.square().mean()
    loss.backward()

    assert outputs.shape == (12, 2)
    assert inputs.grad is not None
    assert all(parameter.grad is not None for parameter in model.parameters())

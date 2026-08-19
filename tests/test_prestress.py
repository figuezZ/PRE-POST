import pytest

from src.prestress import initial_steel_stress


def test_initial_steel_stress():
    assert initial_steel_stress(1_000_000.0, 0.0007) == pytest.approx(
        1_428_571_428.5714288
    )


@pytest.mark.parametrize("force,area", [(0.0, 0.0007), (1.0, 0.0)])
def test_initial_steel_stress_rejects_nonpositive_inputs(force, area):
    with pytest.raises(ValueError):
        initial_steel_stress(force, area)


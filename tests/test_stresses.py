import pytest

from src.analysis import elastic_fiber_stresses
from src.models import ConcreteInput, RectangularSectionInput
from src.sections import calculate_rectangular_properties


def properties():
    return calculate_rectangular_properties(
        RectangularSectionInput(0.4, 0.8),
        ConcreteInput(35e6, 45e6, 34e9, 25e3),
    )


def test_centered_prestress_produces_uniform_compression():
    result = elastic_fiber_stresses(properties(), 1_000_000.0, 0.0, 0.0)

    assert result.top_pa == pytest.approx(-3_125_000.0)
    assert result.bottom_pa == pytest.approx(-3_125_000.0)


def test_case_a_transfer_stresses_match_hand_calculation():
    result = elastic_fiber_stresses(properties(), 1_000_000.0, -0.20, 100_000.0)

    assert result.prestress_moment_n_m == pytest.approx(-200_000.0)
    assert result.resultant_moment_n_m == pytest.approx(-100_000.0)
    assert result.top_pa == pytest.approx(-781_250.0)
    assert result.bottom_pa == pytest.approx(-5_468_750.0)


def test_sagging_moment_compresses_top_and_tensions_bottom():
    result = elastic_fiber_stresses(properties(), 1.0, 0.0, 100_000.0)

    assert result.top_pa < result.bottom_pa


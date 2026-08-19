import pytest

from src.models import ConcreteInput, RectangularSectionInput
from src.sections import calculate_rectangular_properties


def test_rectangular_properties_match_hand_calculation():
    result = calculate_rectangular_properties(
        RectangularSectionInput(0.4, 0.8),
        ConcreteInput(35e6, 45e6, 34e9, 25e3),
    )

    assert result.area_m2 == pytest.approx(0.32)
    assert result.centroid_from_bottom_m == pytest.approx(0.4)
    assert result.inertia_m4 == pytest.approx(0.01706666666666667)
    assert result.section_modulus_top_m3 == pytest.approx(0.04266666666666667)
    assert result.section_modulus_bottom_m3 == pytest.approx(0.04266666666666667)
    assert result.self_weight_n_m == pytest.approx(8000.0)


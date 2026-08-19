import pytest

from src.models import (
    BeamInput,
    ConcreteInput,
    DesignInput,
    LoadInput,
    PrestressInput,
    ProjectMetadata,
    RectangularSectionInput,
)


def valid_design(**prestress_overrides):
    prestress = {
        "initial_force_n": 1_000_000.0,
        "eccentricity_m": -0.20,
        "steel_area_m2": 0.0007,
        "steel_ultimate_strength_pa": 1_860e6,
    }
    prestress.update(prestress_overrides)
    return DesignInput(
        metadata=ProjectMetadata("Caso", "Equipo", "2026-08-19", "0.1.0", "ACI"),
        beam=BeamInput(10.0),
        section=RectangularSectionInput(0.4, 0.8),
        concrete=ConcreteInput(35e6, 45e6, 34e9, 25e3),
        loads=LoadInput(),
        prestress=PrestressInput(**prestress),
    )


@pytest.mark.parametrize("width,height", [(0.0, 0.8), (-0.4, 0.8), (0.4, 0.0)])
def test_rejects_nonpositive_section_dimensions(width, height):
    with pytest.raises(ValueError):
        RectangularSectionInput(width, height)


def test_rejects_unsupported_support_condition():
    with pytest.raises(ValueError, match="simply_supported"):
        BeamInput(10.0, "continuous")


def test_rejects_service_strength_below_transfer_strength():
    with pytest.raises(ValueError, match="no puede ser menor"):
        ConcreteInput(45e6, 35e6, 34e9, 25e3)


def test_rejects_tendon_center_outside_section():
    with pytest.raises(ValueError, match="dentro de la seccion"):
        valid_design(eccentricity_m=-0.41)


def test_rejects_initial_steel_stress_above_declared_ultimate_strength():
    with pytest.raises(ValueError, match="supera"):
        valid_design(steel_area_m2=0.0001)


def test_rejects_negative_loads():
    with pytest.raises(ValueError, match="no puede ser negativo"):
        LoadInput(superimposed_dead_load_n_m=-1.0)


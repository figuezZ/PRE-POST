import pytest

from src.analysis import analyze_service, analyze_uniform_service_stage
from src.models import (
    BeamInput,
    ConcreteInput,
    DesignInput,
    LoadInput,
    PrestressInput,
    ProjectMetadata,
    RectangularSectionInput,
    SectionProperties,
)
from src.prestress import effective_prestress_force


def test_effective_force_applies_declared_global_loss():
    assert effective_prestress_force(169.0, 0.15) == pytest.approx(143.65)


@pytest.mark.parametrize("loss_ratio", [-0.001, 1.0, 1.2])
def test_effective_force_rejects_invalid_loss_ratio(loss_ratio):
    with pytest.raises(ValueError, match="entre 0 y 1"):
        effective_prestress_force(1_000_000.0, loss_ratio)


def test_class_3_service_example_matches_published_stresses():
    inch = 0.0254
    kip_n = 4448.2216152605
    foot_m = 0.3048
    psi_pa = 6894.757293168
    properties = SectionProperties(
        area_m2=176.0 * inch**2,
        centroid_from_bottom_m=12.0 * inch,
        inertia_m4=12_000.0 * inch**4,
        section_modulus_top_m3=1_000.0 * inch**3,
        section_modulus_bottom_m3=1_000.0 * inch**3,
        self_weight_n_m=(0.1833333333333333 * kip_n / foot_m),
        height_m=24.0 * inch,
    )

    result = analyze_uniform_service_stage(
        properties=properties,
        span_m=40.0 * foot_m,
        initial_prestress_force_n=169.0 * kip_n,
        time_dependent_loss_ratio=0.15,
        eccentricity_m=-5.19 * inch,
        live_load_n_m=0.55 * kip_n / foot_m,
    )

    assert result.effective_prestress_force_n / kip_n == pytest.approx(143.65)
    assert result.stress.top_pa / psi_pa == pytest.approx(-1830.65, abs=0.01)
    assert result.stress.bottom_pa / psi_pa == pytest.approx(198.26, abs=0.01)


def test_design_service_combines_self_weight_dead_and_live_loads():
    design = DesignInput(
        metadata=ProjectMetadata("Servicio", "Equipo", "2026-08-25", "0.2.0", "Por ratificar"),
        beam=BeamInput(10.0),
        section=RectangularSectionInput(0.4, 0.8),
        concrete=ConcreteInput(35e6, 45e6, 34e9, 25e3),
        loads=LoadInput(2_000.0, 5_000.0),
        prestress=PrestressInput(
            initial_force_n=1_000_000.0,
            eccentricity_m=-0.20,
            steel_area_m2=0.0007,
            steel_ultimate_strength_pa=1_860e6,
            time_dependent_loss_ratio=0.15,
        ),
    )

    result = analyze_service(design)

    assert result.effective_prestress_force_n == pytest.approx(850_000.0)
    assert result.total_uniform_load_n_m == pytest.approx(15_000.0)
    assert result.midspan_moment_n_m == pytest.approx(187_500.0)

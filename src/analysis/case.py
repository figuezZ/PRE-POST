"""Orquestacion del primer flujo ejecutable."""

from src.analysis.loads import simply_supported_uniform_load
from src.analysis.stresses import elastic_fiber_stresses
from src.models import CaseAnalysisResult, DesignInput
from src.sections import calculate_rectangular_properties


def analyze_transfer(design: DesignInput) -> CaseAnalysisResult:
    """Analiza transferencia con fuerza inicial y peso propio solamente."""

    section = calculate_rectangular_properties(design.section, design.concrete)
    effects = simply_supported_uniform_load(section.self_weight_n_m, design.beam.span_m)
    stress = elastic_fiber_stresses(
        properties=section,
        prestress_force_n=design.prestress.initial_force_n,
        eccentricity_m=design.prestress.eccentricity_m,
        external_moment_n_m=effects.midspan_moment_n_m,
    )
    return CaseAnalysisResult(
        project_name=design.metadata.name,
        standard=design.metadata.standard,
        section=section,
        transfer_uniform_load_n_m=section.self_weight_n_m,
        transfer_reaction_n=effects.reaction_n,
        transfer_max_shear_n=effects.max_shear_n,
        transfer_midspan_moment_n_m=effects.midspan_moment_n_m,
        transfer_stress=stress,
        initial_steel_stress_pa=design.prestress.initial_stress_pa,
    )


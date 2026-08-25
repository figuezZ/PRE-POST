"""Etapa elastica de servicio con fuerza efectiva y carga uniforme."""

from src.analysis.loads import simply_supported_uniform_load
from src.analysis.stresses import elastic_fiber_stresses
from src.models import DesignInput, SectionProperties, ServiceAnalysisResult
from src.prestress import effective_prestress_force
from src.sections import calculate_rectangular_properties


def analyze_uniform_service_stage(
    *,
    properties: SectionProperties,
    span_m: float,
    initial_prestress_force_n: float,
    time_dependent_loss_ratio: float,
    eccentricity_m: float,
    superimposed_dead_load_n_m: float = 0.0,
    live_load_n_m: float = 0.0,
) -> ServiceAnalysisResult:
    """Calcula la etapa de servicio sin aplicar limites normativos.

    Se usa ``P_e`` despues de la perdida global declarada y se superponen peso
    propio, carga muerta adicional y carga viva sin mayorar. Referencia:
    *Clase 3: analisis elastico de esfuerzos en elementos pretensados*, USS
    (2026), ecuaciones (25)-(28) y ejemplo de las paginas 12-16.

    La guia mide ``e`` positiva hacia abajo. El nucleo conserva su convencion
    unica: ``e`` positiva hacia arriba, por lo que un tendon inferior usa
    ``e < 0``.
    """

    if superimposed_dead_load_n_m < 0:
        raise ValueError("superimposed_dead_load_n_m no puede ser negativa")
    if live_load_n_m < 0:
        raise ValueError("live_load_n_m no puede ser negativa")

    effective_force_n = effective_prestress_force(
        initial_prestress_force_n, time_dependent_loss_ratio
    )
    total_uniform_load_n_m = (
        properties.self_weight_n_m
        + superimposed_dead_load_n_m
        + live_load_n_m
    )
    effects = simply_supported_uniform_load(total_uniform_load_n_m, span_m)
    stress = elastic_fiber_stresses(
        properties=properties,
        prestress_force_n=effective_force_n,
        eccentricity_m=eccentricity_m,
        external_moment_n_m=effects.midspan_moment_n_m,
    )
    return ServiceAnalysisResult(
        section=properties,
        time_dependent_loss_ratio=time_dependent_loss_ratio,
        effective_prestress_force_n=effective_force_n,
        total_uniform_load_n_m=total_uniform_load_n_m,
        reaction_n=effects.reaction_n,
        max_shear_n=effects.max_shear_n,
        midspan_moment_n_m=effects.midspan_moment_n_m,
        stress=stress,
    )


def analyze_service(design: DesignInput) -> ServiceAnalysisResult:
    """Analiza servicio para la seccion rectangular del alcance actual."""

    section = calculate_rectangular_properties(design.section, design.concrete)
    return analyze_uniform_service_stage(
        properties=section,
        span_m=design.beam.span_m,
        initial_prestress_force_n=design.prestress.initial_force_n,
        time_dependent_loss_ratio=design.prestress.time_dependent_loss_ratio,
        eccentricity_m=design.prestress.eccentricity_m,
        superimposed_dead_load_n_m=design.loads.superimposed_dead_load_n_m,
        live_load_n_m=design.loads.live_load_n_m,
    )

"""Tensiones elasticas en las fibras extremas."""

from src.models import ElasticStressResult, SectionProperties


def elastic_fiber_stresses(
    properties: SectionProperties,
    prestress_force_n: float,
    eccentricity_m: float,
    external_moment_n_m: float,
) -> ElasticStressResult:
    """Calcula tensiones con compresion negativa y traccion positiva.

    Convenciones: `y` y `e` son positivos hacia arriba; un tendon bajo el
    centroide tiene `e < 0`; el momento externo sagante es positivo. Se evalua
    sigma(y) = -P/A - (P*e + M)*y/I.
    """

    if prestress_force_n <= 0:
        raise ValueError("prestress_force_n debe ser mayor que cero")
    prestress_moment = prestress_force_n * eccentricity_m
    resultant_moment = prestress_moment + external_moment_n_m
    axial = -prestress_force_n / properties.area_m2
    top_y = properties.height_m / 2.0
    bottom_y = -top_y
    top = axial - resultant_moment * top_y / properties.inertia_m4
    bottom = axial - resultant_moment * bottom_y / properties.inertia_m4
    return ElasticStressResult(
        top_pa=top,
        bottom_pa=bottom,
        axial_component_pa=axial,
        prestress_moment_n_m=prestress_moment,
        external_moment_n_m=external_moment_n_m,
        resultant_moment_n_m=resultant_moment,
    )


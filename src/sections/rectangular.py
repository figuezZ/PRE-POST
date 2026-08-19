"""Propiedades de una seccion rectangular maciza."""

from src.models import ConcreteInput, RectangularSectionInput, SectionProperties


def calculate_rectangular_properties(
    section: RectangularSectionInput, concrete: ConcreteInput
) -> SectionProperties:
    """Calcula propiedades centroidales y peso propio en unidades SI.

    Ecuaciones clasicas: A = b*h, I = b*h^3/12 y W = I/c.
    """

    width = section.width_m
    height = section.height_m
    area = width * height
    centroid = height / 2.0
    inertia = width * height**3 / 12.0
    section_modulus = inertia / centroid
    return SectionProperties(
        area_m2=area,
        centroid_from_bottom_m=centroid,
        inertia_m4=inertia,
        section_modulus_top_m3=section_modulus,
        section_modulus_bottom_m3=section_modulus,
        self_weight_n_m=area * concrete.unit_weight_n_m3,
        height_m=height,
    )


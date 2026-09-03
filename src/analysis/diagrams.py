"""Series numericas para representar resultados del analisis.

El modulo prepara puntos de grafico sin depender de Streamlit. De este modo,
las ecuaciones siguen en el nucleo y pueden verificarse con pruebas unitarias.
"""

from dataclasses import dataclass
from math import isfinite

from src.analysis.loads import simply_supported_uniform_load_at_section


@dataclass(frozen=True, slots=True)
class BeamDiagramPoint:
    """Corte y momento en una posicion de la viga."""

    position_m: float
    shear_n: float
    moment_n_m: float


@dataclass(frozen=True, slots=True)
class FiberStressPoint:
    """Tension elastica en una coordenada medida desde el centroide."""

    elevation_from_centroid_m: float
    stress_pa: float


def uniform_load_diagram(
    uniform_load_n_m: float, span_m: float, point_count: int = 101
) -> tuple[BeamDiagramPoint, ...]:
    """Muestrea los diagramas ``V(x)`` y ``M(x)`` de una carga uniforme.

    Reutiliza las ecuaciones de equilibrio documentadas en
    :func:`src.analysis.loads.simply_supported_uniform_load_at_section`:
    ``V(x)=wL/2-wx`` y ``M(x)=wLx/2-wx^2/2``.
    """

    if isinstance(point_count, bool) or not isinstance(point_count, int):
        raise ValueError("point_count debe ser un numero entero")
    if point_count < 2:
        raise ValueError("point_count debe ser al menos 2")

    points: list[BeamDiagramPoint] = []
    for index in range(point_count):
        position_m = span_m * index / (point_count - 1)
        effects = simply_supported_uniform_load_at_section(
            uniform_load_n_m=uniform_load_n_m,
            span_m=span_m,
            position_from_left_m=position_m,
        )
        points.append(
            BeamDiagramPoint(
                position_m=position_m,
                shear_n=effects.shear_n,
                moment_n_m=effects.moment_n_m,
            )
        )
    return tuple(points)


def linear_fiber_stress_profile(
    *,
    height_m: float,
    top_stress_pa: float,
    bottom_stress_pa: float,
    point_count: int = 51,
) -> tuple[FiberStressPoint, ...]:
    """Interpola la distribucion lineal de tensiones entre fibras extremas.

    Corresponde a la hipotesis elastica de secciones planas utilizada en la
    Clase 3 USS (2026). Los extremos provienen de ``elastic_fiber_stresses``;
    esta funcion no recalcula las solicitaciones ni las tensiones extremas.
    """

    if not isfinite(height_m) or height_m <= 0:
        raise ValueError("height_m debe ser finita y mayor que cero")
    if not isfinite(top_stress_pa) or not isfinite(bottom_stress_pa):
        raise ValueError("Las tensiones extremas deben ser finitas")
    if isinstance(point_count, bool) or not isinstance(point_count, int):
        raise ValueError("point_count debe ser un numero entero")
    if point_count < 2:
        raise ValueError("point_count debe ser al menos 2")

    bottom_elevation_m = -height_m / 2.0
    points: list[FiberStressPoint] = []
    for index in range(point_count):
        ratio = index / (point_count - 1)
        elevation_m = bottom_elevation_m + height_m * ratio
        stress_pa = bottom_stress_pa + (top_stress_pa - bottom_stress_pa) * ratio
        points.append(
            FiberStressPoint(
                elevation_from_centroid_m=elevation_m,
                stress_pa=stress_pa,
            )
        )
    return tuple(points)

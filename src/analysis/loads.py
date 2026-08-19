"""Efectos de carga para una viga simplemente apoyada."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class UniformLoadEffects:
    reaction_n: float
    max_shear_n: float
    midspan_moment_n_m: float


def simply_supported_uniform_load(
    uniform_load_n_m: float, span_m: float
) -> UniformLoadEffects:
    """Retorna R=wL/2, Vmax=wL/2 y Mmax=wL^2/8."""

    if uniform_load_n_m < 0:
        raise ValueError("uniform_load_n_m no puede ser negativa")
    if span_m <= 0:
        raise ValueError("span_m debe ser mayor que cero")
    reaction = uniform_load_n_m * span_m / 2.0
    return UniformLoadEffects(
        reaction_n=reaction,
        max_shear_n=reaction,
        midspan_moment_n_m=uniform_load_n_m * span_m**2 / 8.0,
    )


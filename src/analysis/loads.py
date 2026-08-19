"""Efectos de carga para una viga simplemente apoyada."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class UniformLoadEffects:
    reaction_n: float
    max_shear_n: float
    midspan_moment_n_m: float


@dataclass(frozen=True, slots=True)
class UniformLoadSectionEffects:
    position_from_left_m: float
    left_reaction_n: float
    shear_n: float
    moment_n_m: float


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


def simply_supported_uniform_load_at_section(
    uniform_load_n_m: float, span_m: float, position_from_left_m: float
) -> UniformLoadSectionEffects:
    """Calcula reaccion, corte y momento a una distancia `x` del apoyo izquierdo.

    Por equilibrio: R=wL/2, V(x)=R-wx y M(x)=Rx-wx^2/2. El corte es positivo
    cerca del apoyo izquierdo y el momento sagante es positivo.
    """

    if uniform_load_n_m < 0:
        raise ValueError("uniform_load_n_m no puede ser negativa")
    if span_m <= 0:
        raise ValueError("span_m debe ser mayor que cero")
    if not 0.0 <= position_from_left_m <= span_m:
        raise ValueError("position_from_left_m debe estar dentro de la luz")

    reaction = uniform_load_n_m * span_m / 2.0
    shear = reaction - uniform_load_n_m * position_from_left_m
    moment = (
        reaction * position_from_left_m
        - uniform_load_n_m * position_from_left_m**2 / 2.0
    )
    return UniformLoadSectionEffects(
        position_from_left_m=position_from_left_m,
        left_reaction_n=reaction,
        shear_n=shear,
        moment_n_m=moment,
    )

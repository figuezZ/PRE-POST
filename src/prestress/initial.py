"""Magnitudes iniciales del acero de pretensado."""


def initial_steel_stress(force_n: float, steel_area_m2: float) -> float:
    """Calcula f_pi=P_i/A_p en Pa."""

    if force_n <= 0:
        raise ValueError("force_n debe ser mayor que cero")
    if steel_area_m2 <= 0:
        raise ValueError("steel_area_m2 debe ser mayor que cero")
    return force_n / steel_area_m2


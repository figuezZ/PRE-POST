"""Magnitudes iniciales del acero de pretensado."""


def initial_steel_stress(force_n: float, steel_area_m2: float) -> float:
    """Calcula la tension del acero ``f_p=P/A_p`` en Pa.

    Referencia docente: *Clase 3: analisis elastico de esfuerzos en elementos
    pretensados*, USS, ecuaciones (27)-(28) y ejemplo de las paginas 12-16.
    La misma funcion sirve para la fuerza inicial ``P_i`` y la efectiva ``P_e``.
    """

    if force_n <= 0:
        raise ValueError("force_n debe ser mayor que cero")
    if steel_area_m2 <= 0:
        raise ValueError("steel_area_m2 debe ser mayor que cero")
    return force_n / steel_area_m2

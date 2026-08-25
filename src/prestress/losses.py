"""Transformacion trazable entre fuerza inicial y fuerza efectiva."""


def effective_prestress_force(
    initial_force_n: float, time_dependent_loss_ratio: float
) -> float:
    """Retorna ``P_e=(1-perdida)P_i`` cuando la perdida es un dato de entrada.

    Este calculo no estima retraccion, fluencia ni relajacion por separado. Solo
    aplica un porcentaje global entregado por el problema, como en la ecuacion
    (28) y el ejemplo de las paginas 11-16 de *Clase 3: analisis elastico de
    esfuerzos en elementos pretensados*, USS (2026).
    """

    if initial_force_n <= 0:
        raise ValueError("initial_force_n debe ser mayor que cero")
    if not 0.0 <= time_dependent_loss_ratio < 1.0:
        raise ValueError("time_dependent_loss_ratio debe estar entre 0 y 1")
    return initial_force_n * (1.0 - time_dependent_loss_ratio)

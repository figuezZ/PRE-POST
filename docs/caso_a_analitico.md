# Caso A - control analitico

## Datos

- Seccion rectangular: `b = 0.40 m`, `h = 0.80 m`.
- Luz simplemente apoyada: `L = 10.0 m`.
- Peso especifico: `gamma = 25,000 N/m3`.
- Fuerza inicial: `Pi = 1,000,000 N`.
- Excentricidad: `e = -0.20 m` (bajo el centroide).

No se aplican cargas adicionales en transferencia.

## Derivacion independiente

1. `A = b h = 0.32 m2`.
2. `I = b h^3 / 12 = 0.0170666667 m4`.
3. `w = A gamma = 8,000 N/m`.
4. `R = w L / 2 = 40,000 N`.
5. `M_g = w L^2 / 8 = 100,000 N m`.
6. `M_p = Pi e = -200,000 N m`.
7. `M_resultante = M_p + M_g = -100,000 N m`.
8. `sigma(y) = -Pi/A - M_resultante y/I`.

Con `y_superior = +0.40 m` y `y_inferior = -0.40 m`:

- `sigma_superior = -781,250 Pa = -0.78125 MPa`.
- `sigma_inferior = -5,468,750 Pa = -5.46875 MPa`.

El signo negativo representa compresion. Este caso comprueba algebra,
convenciones y unidades; no comprueba limites normativos.


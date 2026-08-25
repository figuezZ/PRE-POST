# Caso S1 - servicio basado en la Clase 3

## Fuente y alcance

El caso reproduce el ejemplo de las paginas 12-16 de *Clase 3: analisis
elastico de esfuerzos en elementos pretensados*, material docente USS 2026.
Comprueba fuerza efectiva, carga uniforme, momento y tensiones elasticas. No
comprueba limites normativos ni calcula cada mecanismo de perdida.

## Convencion de excentricidad

La guia mide positiva la distancia del tendon hacia abajo. El nucleo PRE-POST
usa `y` y `e` positivos hacia arriba. Los `5.19 in` bajo el centroide se ingresan
como:

```text
e = -5.19 in = -0.131826 m
```

Esta conversion cambia el signo del dato, pero no cambia el fenomeno fisico.

## Datos reproducibles

- Luz: `40 ft = 12.192 m`.
- Area: `176 in2 = 0.11354816 m2`.
- Inercia: `12,000 in4 = 0.0049947771072 m4`.
- Altura: `24 in = 0.6096 m`.
- Fuerza inicial: `Pi = 169 kip = 751,749.453 N`.
- Perdida dependiente del tiempo declarada: `15 %`.
- Peso propio: `0.183333 kip/ft = 2,675.549 N/m`.
- Carga viva: `0.55 kip/ft = 8,026.647 N/m`.

## Desarrollo independiente

1. `Pe = (1 - 0.15) Pi = 143.65 kip = 638,987.035 N`.
2. `w = wpp + wl = 10,702.195 N/m`.
3. `M = w L2 / 8 = 198,853.299 N m`.
4. Se aplica la ecuacion unica del nucleo:
   `sigma(y) = -Pe/A - (Pe e + M)y/I`.

Resultados publicados y reproducidos:

- fibra superior: `-1,830.65 psi = -12.6219 MPa`;
- fibra inferior: `+198.26 psi = +1.3670 MPa`.

El signo negativo representa compresion y el positivo representa traccion. La
traccion inferior muestra por que la fuerza efectiva y las cargas de servicio
no deben mezclarse con el estado inicial de transferencia.

## Trazabilidad en el repositorio

- Datos: `examples/service_clase3.json`.
- Perdida global: `src/prestress/losses.py`.
- Orquestacion: `src/analysis/service.py`.
- Ecuacion seccional: `src/analysis/stresses.py`.
- Pruebas: `tests/test_service.py` y `tests/test_validation.py`.

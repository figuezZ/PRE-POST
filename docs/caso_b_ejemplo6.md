# Caso B - Ejemplo 6 publicado

## Fuente

Adolfo Matamoros y Julio Ramirez, *Ejemplo 6: Viga pretensada*, paginas
164-184. El documento desarrolla la region extrema de una viga pretensada con
modelos de bielas y tirantes segun ACI 318-02.

## Alcance incorporado

Esta primera integracion valida solamente el equilibrio global necesario antes
de construir el modelo de bielas y tirantes. No se presenta como una
verificacion completa del ejemplo.

Datos usados, convertidos desde las unidades originales sin redondear:

| Magnitud | Valor original | Valor SI del nucleo |
|---|---:|---:|
| Luz entre apoyos | 30 ft | 9.144 m |
| Carga ultima uniforme | 0.30 kip/in | 52,538.0506 N/m |
| Distancia del apoyo a la seccion D | 75 in | 1.905 m |
| Ancho de la seccion | 12 in | 0.3048 m |
| Altura de la seccion | 28 in | 0.7112 m |

El PDF muestra varios valores SI redondeados. La autovalidacion conserva los
valores originales imperiales y hace una conversion reproducible a SI.

## Equilibrio independiente

Para una viga simplemente apoyada con carga uniforme:

1. `R = w L / 2`.
2. `V(x) = R - w x`.
3. `M(x) = R x - w x^2 / 2`.

En `x = 1.905 m`, el equilibrio con los datos originales entrega:

- reaccion izquierda: 54 kip = 240.204 kN;
- corte: 31.5 kip = 140.119 kN;
- momento: 3,206.25 kip in = 362.258 kN m.

La fuente publica 240 kN, 140 kN y 362 kN m. La diferencia proviene del
redondeo de la tabla, por lo que el Caso B declara una tolerancia relativa de
0.5 %. Los valores esperados no se modifican para coincidir artificialmente con
el programa.

## Pendiente para completar el ejemplo

- geometria de nodos, bielas y tirantes;
- fuerzas internas de las Tablas 6-2 y 6-5;
- resistencia de bielas y zonas nodales segun ACI 318-02;
- longitud de transferencia y desarrollo de cables;
- dimensionamiento de tirantes y armadura transversal;
- comparacion entre cables rectos y deformados.

ACI 318-02 se conserva como norma historica de la fuente. No reemplaza la norma
principal que el equipo debe ratificar para el producto.

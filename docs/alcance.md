# Alcance declarado - version 0.3.0

## Familia resuelta

- Sistema: viga pretensada con tendon resultante equivalente.
- Condicion estatica: viga simplemente apoyada.
- Seccion: rectangular maciza y constante.
- Etapas activas: transferencia y servicio elastico.
- Fuerza efectiva: porcentaje global de perdida entregado como dato.
- Unidades internas: m, N y Pa.
- Norma principal provisional: ACI 318-19.

La seleccion normativa debe ser ratificada por el equipo y el docente antes de
implementar limites o factores. En esta version, las ecuaciones ejecutables son
de estatica y mecanica elastica; no se declara cumplimiento normativo.

## Convenciones de signo

- Compresion negativa; traccion positiva.
- Coordenada vertical positiva hacia arriba desde el centroide.
- Excentricidad positiva hacia arriba. Un tendon bajo el centroide tiene `e < 0`.
- Momento externo sagante positivo.

## Incluido

1. Validacion de datos positivos y bloques obligatorios.
2. Verificacion de que el centro del tendon esta dentro de la seccion bruta.
3. Area, centroide, inercia, modulos resistentes y peso propio.
4. Reaccion, corte maximo y momento maximo por carga uniforme.
5. Tension inicial del acero.
6. Tensiones elasticas superior e inferior en transferencia.
7. Caso analitico, pruebas automaticas y salida JSON de autovalidacion.
8. Boceto responsive que llama al nucleo.
9. Caso B publicado para reaccion, corte y momento en una seccion de control.
10. Fuerza efectiva `Pe` a partir de `Pi` y una perdida global declarada.
11. Tensiones de servicio por peso propio, carga muerta adicional y carga viva.
12. Caso S1 docente con resultados publicados de la Clase 3.
13. Exportacion tabulada de entradas y resultados a Excel y PDF.

## Fuera de esta version

- Secciones T o I y vigas postensadas.
- Cargas puntuales, continuidad o analisis hiperestatico.
- Calculo separado de friccion, asiento, acortamiento elastico, retraccion,
  fluencia y relajacion.
- Limites normativos de tensiones, fisuracion y flecha.
- Flexion resistente, corte, anclajes y detallamiento.
- Modelo de bielas y tirantes de la region extrema del Ejemplo 6.
- Memoria normativa completa y exportacion CAD.

Estas exclusiones son una secuencia de implementacion, no una renuncia a los
requisitos obligatorios del producto final.

## Referencias docentes incorporadas

- Clase 1: fundamentos, sistemas, materiales y anclajes.
- Clase 2: clasificacion de perdidas instantaneas y diferidas.
- Clase 3: tensiones elasticas por etapas, fuerza efectiva y ejemplo de servicio.
- Clase 4: agrietamiento y resistencia a flexion, conservados para una etapa
  posterior porque requieren ratificacion normativa y ampliacion del modelo.

La guia de Clase 3 define excentricidad positiva hacia abajo. PRE-POST conserva
la convencion unica del repositorio, positiva hacia arriba. Por ello, un valor
positivo de la guia debe ingresar al nucleo con signo negativo.

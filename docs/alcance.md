# Alcance declarado - version 0.1.0

## Familia resuelta

- Sistema: viga pretensada con tendon resultante equivalente.
- Condicion estatica: viga simplemente apoyada.
- Seccion: rectangular maciza y constante.
- Etapa activa: transferencia, con fuerza inicial y peso propio.
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

## Fuera de esta version

- Secciones T o I y vigas postensadas.
- Cargas puntuales, continuidad o analisis hiperestatico.
- Perdidas inmediatas y diferidas.
- Fuerza efectiva y etapas de servicio.
- Limites normativos de tensiones, fisuracion y flecha.
- Flexion resistente, corte, anclajes y detallamiento.
- Memoria automatica y exportacion CAD.

Estas exclusiones son una secuencia de implementacion, no una renuncia a los
requisitos obligatorios del producto final.


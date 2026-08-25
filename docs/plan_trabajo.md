# Plan de trabajo, responsables y riesgos

## Proximo hito: Avance 1 - 10 de septiembre de 2026

| Tarea | Rol responsable | Revisor | Fecha objetivo | Estado |
|---|---|---|---|---|
| Ratificar norma, edicion y bibliografia | Ingenieria y normativa | Desarrollo del nucleo | 21 ago | Pendiente de asignar nombres |
| Revisar derivacion del Caso A | Ingenieria y normativa | Validacion y calidad | 23 ago | Pendiente de revision humana |
| Completar modelos de materiales y tendones | Desarrollo del nucleo | Ingenieria y normativa | 27 ago | Parcial: fuerza efectiva incorporada |
| Probar errores y consistencia dimensional | Validacion y calidad | Desarrollo del nucleo | 29 ago | Base creada |
| Probar interfaz en computador y tableta | Interfaz y entrega | Validacion y calidad | 31 ago | Boceto creado |
| Ensayar cambio de un dato y explicacion previa | Equipo completo | Equipo completo | 5 sep | Pendiente |
| Congelar evidencia del Avance 1 | Equipo completo | Equipo completo | 7 sep | Pendiente |

Cada fila debe recibir un nombre real y una segunda persona revisora. El
historial de GitHub y `contribuciones.md` respaldan la evidencia.

## Riesgos

| Riesgo | Probabilidad | Impacto | Mitigacion | Senal temprana |
|---|---:|---:|---|---|
| Norma no ratificada | Media | Alta | Resolver antes de implementar checks | Ecuaciones sin articulo exacto |
| Mezcla de unidades | Media | Alta | SI en nombres, entradas y pruebas | Conversion dentro del nucleo |
| Signos de excentricidad inconsistentes | Media | Alta | Caso A y convenciones unicas | Interfaz y prueba difieren |
| Trabajo concentrado en una persona | Alta | Alta | Responsable y revisor por tarea | Commits de un solo integrante |
| Interfaz adelanta al nucleo | Media | Media | Interfaz solo consume funciones probadas | Formula aparece en `src/app/` |
| Caso esperado ajustado para pasar | Baja | Critica | Derivacion versionada y revision cruzada | Cambia JSON sin cambiar derivacion |

## Orden posterior

1. Ratificar norma y completar los modelos.
2. Implementar trazado del tendon y limites iniciales.
3. Implementar perdidas inmediatas por mecanismo con TDD.
4. Reemplazar la razon global por perdidas diferidas calculadas y contrastadas.
5. Agregar limites normativos solo despues de ratificar codigo, edicion y articulos.
6. Integrar checks, reportes y luego innovacion.

# Verificaciones obligatorias y secuencia

| Verificacion | Modulo previsto | Estado 0.2.0 |
|---|---|---|
| Propiedades y peso propio | `src/sections/` | Implementada |
| Acciones y solicitaciones | `src/analysis/loads.py` | Parcial: carga uniforme y seccion de control |
| Fuerza y tension inicial | `src/prestress/` | Implementada sin limite normativo |
| Perdidas inmediatas | `src/prestress/losses.py` | Pendiente |
| Perdidas diferidas | `src/prestress/losses.py` | Parcial: razon global entregada como dato |
| Tensiones por etapa | `src/analysis/stresses.py` | Transferencia y servicio implementados |
| Servicio y flecha | `src/analysis/service.py` | Parcial: tensiones implementadas; flecha pendiente |
| Flexion resistente | `src/analysis/flexure.py` | Pendiente |
| Corte | `src/analysis/shear.py` | Pendiente |
| Anclaje o transferencia | `src/analysis/anchorage.py` | Pendiente |
| Detallamiento | `src/reporting/` | Pendiente |
| Resumen CUMPLE/NO CUMPLE/NO APLICA | `src/checks/` | Contrato de datos creado |

Cada implementacion normativa debera mostrar demanda, capacidad, unidades,
razon cuando corresponda, metodo, referencia y mensaje accionable. Ningun
modulo puede redisenar silenciosamente la entrada.

# Matriz requisito - modulo - formula - prueba

Estado: `HECHO`, `PARCIAL` o `PENDIENTE`.

| Requisito de la pauta | Modulo | Metodo o formula | Evidencia / prueba | Estado |
|---|---|---|---|---|
| Datos tipados y validacion | `src/models/inputs.py` | Reglas fisicas y dimensionales | `tests/test_models.py` | HECHO |
| Area y centroide | `src/sections/rectangular.py` | `A=bh`, `yb=h/2` | `test_rectangular_properties` | HECHO |
| Inercia y modulos | `src/sections/rectangular.py` | `I=bh^3/12`, `W=I/c` | `test_rectangular_properties` | HECHO |
| Peso propio | `src/sections/rectangular.py` | `w=A gamma` | `test_rectangular_properties` | HECHO |
| Acciones y solicitaciones | `src/analysis/loads.py` | `R=wL/2`, `Mmax=wL^2/8` | `tests/test_loads.py` | PARCIAL |
| Pretensado inicial | `src/prestress/initial.py` | `fpi=Pi/Ap` | `tests/test_prestress.py` | HECHO |
| Perdidas inmediatas | `src/prestress/losses.py` | Metodo por definir y referenciar | Futura prueba patron | PENDIENTE |
| Perdidas diferidas | `src/prestress/losses.py` | `Pe=(1-perdida)Pi` con perdida declarada | `tests/test_service.py` | PARCIAL |
| Tensiones en transferencia | `src/analysis/stresses.py` | `sigma=-P/A-(P e+M)y/I` | `tests/test_stresses.py` | HECHO |
| Tensiones en servicio | `src/analysis/service.py` | `Pe`, peso propio, carga muerta y carga viva | `tests/test_service.py` y Caso S1 | HECHO |
| Servicio y flecha | `src/analysis/service.py` | Tensiones elasticas; flecha por definir | Caso S1 docente | PARCIAL |
| Flexion resistente | `src/analysis/flexure.py` | Norma por ratificar | Futura demanda/capacidad | PENDIENTE |
| Corte | `src/analysis/shear.py` | Norma por ratificar | Futura demanda/capacidad | PENDIENTE |
| Anclaje/transferencia | `src/analysis/anchorage.py` | Depende del sistema | Futura prueba aplicable | PENDIENTE |
| Estados explicitos | `src/checks/status.py` | Contrato comun | `tests/test_checks.py` | PARCIAL |
| Caso A y tolerancias | `examples/`, `src/validation.py` | Comparacion relativa | `tests/test_validation.py` | HECHO |
| Caso B publicado | `examples/case_b_ejemplo6.json` | Equilibrio global en seccion D | `tests/test_validation.py` | PARCIAL |
| Caso S1 docente | `examples/service_clase3.json` | Fuerza efectiva y tensiones de servicio | `tests/test_validation.py` | HECHO |
| Interfaz sin formulas | `src/app/app.py` | Llama `analyze_transfer` | Revision manual + futura prueba UI | PARCIAL |
| Memoria y JSON/CSV/PDF/XLSX | `src/reporting/exports.py` | Instantanea tabulada sin formulas estructurales duplicadas | `tests/test_reporting.py` y JSON de validacion | PARCIAL |

La norma y los articulos exactos deben reemplazar las filas "por definir" antes
de escribir sus ecuaciones. La matriz se actualiza en el mismo commit que cada
modulo y su prueba.

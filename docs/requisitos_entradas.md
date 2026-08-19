# Requisitos de entradas

El nucleo usa exclusivamente SI. Los nombres de atributos incorporan sus
unidades para evitar conversiones implicitas.

| Bloque | Campo | Unidad | Validacion actual |
|---|---|---:|---|
| Identificacion | nombre, autor, fecha, version, norma | texto | Obligatorios y no vacios |
| Viga | luz | m | Positiva |
| Viga | condicion de apoyo | - | Solo `simply_supported` |
| Seccion | ancho, alto | m | Positivos |
| Hormigon | f'ci, f'c, Ec | Pa | Positivos; f'c no menor que f'ci |
| Hormigon | peso especifico | N/m3 | Positivo |
| Cargas | carga muerta adicional, carga viva | N/m | No negativas |
| Pretensado | fuerza inicial | N | Positiva |
| Pretensado | excentricidad | m | Centro del tendon dentro de la seccion |
| Pretensado | area de acero | m2 | Positiva |
| Pretensado | resistencia ultima | Pa | Positiva y mayor que la tension inicial |

Las cargas adicionales se almacenan desde esta version, pero la etapa de
transferencia utiliza solo peso propio. Se incorporaran en las etapas de
servicio junto con la fuerza efectiva.


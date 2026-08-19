# Contexto persistente del proyecto

Este repositorio sigue la pauta del Proyecto Integrador ICIV 1042 (2026).

## Alcance declarado del primer corte

- Viga pretensada simplemente apoyada.
- Seccion rectangular maciza.
- Nucleo de calculo en SI: m, N y Pa.
- ACI 318-19 como norma principal provisional, pendiente de ratificacion del
  equipo y del docente antes de implementar verificaciones normativas.
- Calculos activos: propiedades, peso propio, carga uniforme, solicitaciones y
  tensiones elasticas iniciales en transferencia.

## Reglas

- No mezclar formulas con `src/app/`.
- Usar entradas tipadas de `src/models/`.
- Compresion negativa, traccion positiva; `y` y excentricidad positivos hacia
  arriba; momento sagante positivo.
- Una tarea por modulo y pruebas en la misma tarea.
- Toda ecuacion normativa nueva exige referencia exacta en `docs/`.

## Verificacion unica

```bash
python -m pytest && python -m src.validation --all --output outputs/validation_summary.json
```

Consultar `docs/alcance.md`, `docs/requisitos_entradas.md` y
`docs/matriz_requisitos.md`; no cargar la pauta completa en cada sesion.


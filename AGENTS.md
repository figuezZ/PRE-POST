# Contexto de trabajo

## Objetivo

Construir una herramienta academica transparente y reproducible para una viga
de hormigon pretensado, conforme a la pauta ICIV 1042 de 2026.

## Convenciones obligatorias

- Nucleo en SI: m, N y Pa. Las fronteras de interfaz pueden mostrar kN o MPa.
- Compresion negativa y traccion positiva.
- Eje vertical `y` positivo hacia arriba desde el centroide.
- Excentricidad del tendon positiva hacia arriba; un tendon bajo el centroide
  tiene excentricidad negativa.
- Momento externo positivo produce flexion sagante.
- La interfaz nunca duplica formulas del nucleo.
- Cada funcion nueva de calculo debe incluir una prueba y una referencia.
- No se implementan decisiones normativas sin documentar norma, edicion,
  articulo y criterio de aceptacion.

## Comando de verificacion

```bash
python -m pytest && python -m src.validation --all --output outputs/validation_summary.json
```

## Limites actuales

Leer `docs/alcance.md` antes de ampliar el modelo. El estado de cada requisito
esta en `docs/matriz_requisitos.md`.


# PRE-POST - ICIV 1042

Base ejecutable del proyecto integrador de Hormigon Pre y Postensado 2026.
El primer corte implementa una viga pretensada simplemente apoyada, de seccion
rectangular, con unidades SI explicitas. Calcula propiedades geometricas, peso
propio, solicitaciones por carga uniforme y tensiones elasticas iniciales en
transferencia.

La interfaz tambien incorpora el Ejemplo 6 de Matamoros y Ramirez como Caso B
publicado. En esta etapa reproduce el equilibrio global en el limite de la
region D; el modelo completo de bielas y tirantes permanece pendiente.

> Herramienta academica en desarrollo. No es software certificado ni debe
> utilizarse para construir obras reales. La norma, las hipotesis y todos los
> resultados deben ser revisados por el equipo y por un profesional competente.

## Instalacion

Requiere Python 3.11 o superior.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev,app]"
```

En Windows, active el entorno con `.venv\Scripts\activate`.

## Verificacion

```bash
python -m pytest
python -m src.validation --all --output outputs/validation_summary.json
```

El segundo comando genera un reporte estructurado, a partir del caso analitico
versionado y del ejemplo publicado, sin editar manualmente los resultados
esperados.

## Interfaz

```bash
streamlit run src/app/app.py
```

La interfaz llama al mismo nucleo que usan las pruebas; no contiene formulas de
ingenieria duplicadas.

## Despliegue en Streamlit Community Cloud

La configuracion del servicio debe apuntar a:

```text
Repository: figuezZ/PRE-POST
Branch: main
Main file path: src/app/app.py
```

El archivo `requirements.txt` fuerza la instalacion con `pip` y evita que el
servicio interprete `pyproject.toml` como un proyecto Poetry.

## Estructura

- `src/models/`: entradas tipadas, validaciones y resultados.
- `src/sections/`: geometria, propiedades y peso propio.
- `src/prestress/`: fuerza inicial y, en iteraciones futuras, perdidas.
- `src/analysis/`: cargas, solicitaciones y tensiones.
- `src/checks/`: estados de cumplimiento trazables.
- `src/reporting/`: generacion futura de memoria y salidas.
- `src/app/`: interfaz responsive.
- `tests/`: pruebas unitarias y de integracion.
- `examples/`: casos reproducibles.
- `docs/`: alcance, requisitos, matriz y derivaciones.
- `outputs/`: resultados regenerables.

## Alcance actual

Las decisiones, exclusiones y convenciones se encuentran en
[`docs/alcance.md`](docs/alcance.md). La trazabilidad del Avance 1 se mantiene en
[`docs/matriz_requisitos.md`](docs/matriz_requisitos.md).

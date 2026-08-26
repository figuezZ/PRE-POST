# PRE-POST - ICIV 1042

Base ejecutable del proyecto integrador de Hormigon Pre y Postensado 2026.
El primer corte implementa una viga pretensada simplemente apoyada, de seccion
rectangular, con unidades SI explicitas. Calcula propiedades geometricas, peso
propio, solicitaciones por carga uniforme y tensiones elasticas en transferencia
y servicio. La etapa de servicio utiliza una perdida global declarada por el
usuario para obtener la fuerza efectiva; aun no estima cada mecanismo de
perdida ni verifica limites normativos.

Despues de cada calculo, la aplicacion permite descargar una instantanea
tabulada en Excel o PDF. Ambos formatos incluyen datos de entrada, propiedades
de la seccion, transferencia, servicio, unidades, convenciones y alcance.

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

El segundo comando genera un reporte estructurado a partir del Caso A, el
Ejemplo 6 publicado y el ejemplo docente de servicio de la Clase 3, sin editar
manualmente los resultados esperados.

## Interfaz

```bash
streamlit run src/app/app.py
```

La interfaz llama al mismo nucleo que usan las pruebas; no contiene formulas de
ingenieria duplicadas.

### Probar la exportacion

1. Complete los datos del Caso A y presione `Calcular etapas`.
2. Revise las pestanas `Transferencia` y `Servicio`.
3. Al final de los resultados, seleccione `Descargar Excel` o `Descargar PDF`.

Los dos archivos corresponden a la misma ejecucion y conservan las unidades,
convenciones, referencia docente y advertencia de uso academico.

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
- `src/prestress/`: tension inicial y transformacion de `Pi` a `Pe` mediante una perdida global declarada.
- `src/analysis/`: cargas, solicitaciones y tensiones de transferencia y servicio.
- `src/checks/`: estados de cumplimiento trazables.
- `src/reporting/`: exportacion tabulada de resultados a Excel y PDF.
- `src/app/`: interfaz responsive.
- `tests/`: pruebas unitarias y de integracion.
- `examples/`: casos reproducibles.
- `docs/`: alcance, requisitos, matriz y derivaciones.
- `outputs/`: resultados regenerables.

## Alcance actual

Las decisiones, exclusiones y convenciones se encuentran en
[`docs/alcance.md`](docs/alcance.md). La trazabilidad del Avance 1 se mantiene en
[`docs/matriz_requisitos.md`](docs/matriz_requisitos.md).

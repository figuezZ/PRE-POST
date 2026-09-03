"""Prueba de regresion para el punto de entrada de Streamlit Cloud."""

import runpy
import sys
from pathlib import Path
from types import ModuleType

from streamlit.testing.v1 import AppTest


def test_app_bootstraps_repository_root(monkeypatch):
    repository_root = Path(__file__).resolve().parents[1]
    app_path = repository_root / "src" / "app" / "app.py"

    # Reproduce el entorno observado en Streamlit Cloud: el directorio del
    # script esta disponible, pero la raiz del repositorio no.
    filtered_path = [
        entry
        for entry in sys.path
        if entry and Path(entry).resolve() != repository_root
    ]
    monkeypatch.setattr(sys, "path", [str(app_path.parent), *filtered_path])
    for module_name in list(sys.modules):
        if module_name == "src" or module_name.startswith("src."):
            monkeypatch.delitem(sys.modules, module_name)
    monkeypatch.setitem(sys.modules, "streamlit", ModuleType("streamlit"))

    runpy.run_path(str(app_path), run_name="streamlit_cloud_import_check")

    assert sys.path[0] == str(repository_root)


def test_app_calculates_and_renders_three_result_charts():
    app_path = Path(__file__).resolve().parents[1] / "src" / "app" / "app.py"
    app = AppTest.from_file(str(app_path)).run(timeout=20)

    assert not app.exception
    assert len(app.radio) == 0

    next(
        button for button in app.button if button.label == "Calcular etapas"
    ).click().run(timeout=20)

    charts = [element for element in app if element.type == "vega_lite_chart"]
    assert not app.exception
    assert len(charts) == 3
    assert [button.label for button in app.download_button] == [
        "Descargar Excel",
        "Descargar PDF",
    ]

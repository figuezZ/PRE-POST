"""Prueba de regresion para el punto de entrada de Streamlit Cloud."""

import runpy
import sys
from pathlib import Path
from types import ModuleType


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


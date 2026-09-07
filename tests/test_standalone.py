"""Equivalencia y portabilidad de la distribucion HTML autonoma."""

import json
from pathlib import Path
import re
import shutil
import subprocess

import pytest

from src.analysis import analyze_service, analyze_transfer
from src.models import (
    BeamInput,
    ConcreteInput,
    DesignInput,
    LoadInput,
    PrestressInput,
    ProjectMetadata,
    RectangularSectionInput,
)


HTML_PATH = (
    Path(__file__).resolve().parents[1]
    / "standalone"
    / "PRE_POST_Standalone.html"
)


def _script(html: str, script_id: str) -> str:
    match = re.search(
        rf'<script id="{script_id}">(?P<script>.*?)</script>',
        html,
        flags=re.DOTALL,
    )
    assert match, f"No se encontro el bloque {script_id}"
    return match.group("script")


def test_standalone_is_one_offline_html_file():
    html = HTML_PATH.read_text(encoding="utf-8")

    assert html.startswith("<!doctype html>")
    assert not re.search(r'(?:src|href)=["\']https?://', html)
    assert "Sistema de unidades" in html
    assert "Calcular etapas" in html
    assert "Descargar Excel" in html
    assert "Imprimir / Guardar PDF" in html
    assert "window.print()" in html
    assert "application/vnd.ms-excel" in html


@pytest.mark.skipif(shutil.which("node") is None, reason="Node no disponible")
def test_standalone_javascript_is_valid_and_matches_python_core():
    html = HTML_PATH.read_text(encoding="utf-8")
    core_script = _script(html, "prepost-core")
    app_script = _script(html, "prepost-app")
    payload = {
        "span_m": 10.0,
        "width_m": 0.4,
        "height_m": 0.8,
        "unit_weight_n_m3": 25_000.0,
        "fci_pa": 35e6,
        "fc_pa": 45e6,
        "dead_load_n_m": 0.0,
        "live_load_n_m": 5_000.0,
        "initial_force_n": 1_000_000.0,
        "eccentricity_m": -0.2,
        "steel_area_m2": 700e-6,
        "loss_ratio": 0.15,
    }
    runner = f"""
new Function({json.dumps(app_script)});
eval({json.dumps(core_script)});
const result = PrePostCore.analyze({json.dumps(payload)});
console.log(JSON.stringify({{
  area_m2: result.section.area_m2,
  inertia_m4: result.section.inertia_m4,
  self_weight_n_m: result.section.self_weight_n_m,
  transfer_moment_n_m: result.transfer.midspan_moment_n_m,
  transfer_top_pa: result.transfer.stress.top_pa,
  transfer_bottom_pa: result.transfer.stress.bottom_pa,
  effective_force_n: result.service.effective_force_n,
  service_moment_n_m: result.service.midspan_moment_n_m,
  service_top_pa: result.service.stress.top_pa,
  service_bottom_pa: result.service.stress.bottom_pa,
  span_ft: PrePostCore.fromSI(10, "span", "USCS")
}}));
"""
    process = subprocess.run(
        ["node", "-e", runner],
        check=True,
        capture_output=True,
        text=True,
    )
    standalone = json.loads(process.stdout)

    design = DesignInput(
        metadata=ProjectMetadata(
            "Control HTML", "Equipo ICIV 1042", "2026-09-07", "0.6.0",
            "ACI 318-19 (provisional)"
        ),
        beam=BeamInput(payload["span_m"]),
        section=RectangularSectionInput(
            payload["width_m"], payload["height_m"]
        ),
        concrete=ConcreteInput(
            payload["fci_pa"], payload["fc_pa"], 34e9,
            payload["unit_weight_n_m3"]
        ),
        loads=LoadInput(payload["dead_load_n_m"], payload["live_load_n_m"]),
        prestress=PrestressInput(
            payload["initial_force_n"], payload["eccentricity_m"],
            payload["steel_area_m2"], 1860e6, payload["loss_ratio"]
        ),
    )
    transfer = analyze_transfer(design)
    service = analyze_service(design)
    expected = {
        "area_m2": transfer.section.area_m2,
        "inertia_m4": transfer.section.inertia_m4,
        "self_weight_n_m": transfer.section.self_weight_n_m,
        "transfer_moment_n_m": transfer.transfer_midspan_moment_n_m,
        "transfer_top_pa": transfer.transfer_stress.top_pa,
        "transfer_bottom_pa": transfer.transfer_stress.bottom_pa,
        "effective_force_n": service.effective_prestress_force_n,
        "service_moment_n_m": service.midspan_moment_n_m,
        "service_top_pa": service.stress.top_pa,
        "service_bottom_pa": service.stress.bottom_pa,
    }

    for name, expected_value in expected.items():
        assert standalone[name] == pytest.approx(expected_value)
    assert standalone["span_ft"] == pytest.approx(32.8083989501)


@pytest.mark.skipif(shutil.which("node") is None, reason="Node no disponible")
def test_standalone_rejects_tendon_outside_section():
    html = HTML_PATH.read_text(encoding="utf-8")
    core_script = _script(html, "prepost-core")
    runner = f"""
eval({json.dumps(core_script)});
try {{
  PrePostCore.analyze({{
    span_m:10,width_m:.4,height_m:.8,unit_weight_n_m3:25000,
    fci_pa:35e6,fc_pa:45e6,dead_load_n_m:0,live_load_n_m:5000,
    initial_force_n:1e6,eccentricity_m:.4,steel_area_m2:.0007,loss_ratio:.15
  }});
  process.exit(1);
}} catch (error) {{
  console.log(error.message);
}}
"""
    process = subprocess.run(
        ["node", "-e", runner],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "dentro de la sección" in process.stdout

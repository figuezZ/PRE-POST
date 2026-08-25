"""Autovalidacion reproducible de los casos versionados."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src import __version__
from src.analysis import (
    analyze_transfer,
    analyze_uniform_service_stage,
    simply_supported_uniform_load_at_section,
)
from src.models import DesignInput, SectionProperties


CASE_A_PATH = Path("examples/case_a_analitico.json")
CASE_B_PATH = Path("examples/case_b_ejemplo6.json")
SERVICE_CASE_PATH = Path("examples/service_clase3.json")


def _relative_error(obtained: float, expected: float) -> float:
    return abs(obtained - expected) / max(abs(expected), 1.0)


def _case_a_values(result: Any) -> dict[str, float]:
    return {
        "area_m2": result.section.area_m2,
        "inertia_m4": result.section.inertia_m4,
        "self_weight_n_m": result.section.self_weight_n_m,
        "midspan_moment_n_m": result.transfer_midspan_moment_n_m,
        "top_stress_pa": result.transfer_stress.top_pa,
        "bottom_stress_pa": result.transfer_stress.bottom_pa,
    }


def _build_comparisons(
    expected_values: dict[str, Any], obtained_values: dict[str, float]
) -> list[dict[str, Any]]:
    comparisons: list[dict[str, Any]] = []
    for name, spec in expected_values.items():
        expected = float(spec["value"])
        obtained = obtained_values[name]
        tolerance = float(spec["relative_tolerance"])
        error = _relative_error(obtained, expected)
        comparison = {
            "name": name,
            "units": spec["units"],
            "expected": expected,
            "obtained": obtained,
            "relative_error": error,
            "relative_tolerance": tolerance,
            "status": "PASS" if error <= tolerance else "FAIL",
        }
        if "published_value" in spec:
            comparison["published_value"] = spec["published_value"]
        comparisons.append(comparison)
    return comparisons


def _case_result(payload: dict[str, Any], comparisons: list[dict[str, Any]]) -> dict[str, Any]:
    passed = all(item["status"] == "PASS" for item in comparisons)
    result = {
        "case_id": payload["case_id"],
        "description": payload["description"],
        "source": payload["source"],
        "status": "PASS" if passed else "FAIL",
        "comparisons": comparisons,
    }
    if "scope" in payload:
        result["scope"] = payload["scope"]
    return result


def validate_case(path: Path = CASE_A_PATH) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    design = DesignInput.from_mapping(payload["input"])
    result = analyze_transfer(design)
    obtained_values = _case_a_values(result)
    comparisons = _build_comparisons(payload["expected"], obtained_values)
    return _case_result(payload, comparisons)


def validate_case_b(path: Path = CASE_B_PATH) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    case_input = payload["input"]
    result = simply_supported_uniform_load_at_section(
        uniform_load_n_m=float(case_input["factored_uniform_load_n_m"]),
        span_m=float(case_input["span_m"]),
        position_from_left_m=float(case_input["position_from_left_support_m"]),
    )
    obtained_values = {
        "left_reaction_n": result.left_reaction_n,
        "shear_n": result.shear_n,
        "moment_n_m": result.moment_n_m,
    }
    comparisons = _build_comparisons(payload["expected"], obtained_values)
    return _case_result(payload, comparisons)


def validate_service_case(path: Path = SERVICE_CASE_PATH) -> dict[str, Any]:
    """Reproduce en SI el ejemplo docente de servicio de la Clase 3."""

    payload = json.loads(path.read_text(encoding="utf-8"))
    case_input = payload["input"]
    result = analyze_uniform_service_stage(
        properties=SectionProperties(**case_input["section_properties"]),
        span_m=float(case_input["span_m"]),
        initial_prestress_force_n=float(case_input["initial_prestress_force_n"]),
        time_dependent_loss_ratio=float(
            case_input["time_dependent_loss_ratio"]
        ),
        eccentricity_m=float(case_input["eccentricity_m"]),
        superimposed_dead_load_n_m=float(
            case_input["superimposed_dead_load_n_m"]
        ),
        live_load_n_m=float(case_input["live_load_n_m"]),
    )
    obtained_values = {
        "effective_force_n": result.effective_prestress_force_n,
        "total_uniform_load_n_m": result.total_uniform_load_n_m,
        "midspan_moment_n_m": result.midspan_moment_n_m,
        "top_stress_pa": result.stress.top_pa,
        "bottom_stress_pa": result.stress.bottom_pa,
    }
    comparisons = _build_comparisons(payload["expected"], obtained_values)
    return _case_result(payload, comparisons)


def build_summary() -> dict[str, Any]:
    cases = [validate_case(), validate_case_b(), validate_service_case()]
    comparisons = [
        comparison
        for case in cases
        for comparison in case["comparisons"]
    ]
    passed_comparisons = sum(
        comparison["status"] == "PASS" for comparison in comparisons
    )
    passed_cases = sum(case["status"] == "PASS" for case in cases)
    return {
        "program_version": __version__,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "tests": {
            "executed": len(comparisons),
            "passed": passed_comparisons,
            "failed": len(comparisons) - passed_comparisons,
            "scope": "comparaciones numericas de los casos de referencia",
        },
        "reference_cases": cases,
        "pending_warnings": [
            "ACI 318-19 es una seleccion provisional pendiente de ratificacion.",
            "La perdida global de servicio es un dato; sus mecanismos aun no se calculan.",
            "Las verificaciones normativas aun no pertenecen a este corte.",
            "El Caso B valida equilibrio global; su modelo de bielas y tirantes sigue pendiente.",
        ],
        "global_status": "PASS" if passed_cases == len(cases) else "FAIL",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all", action="store_true", help="Ejecuta todos los casos disponibles")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("outputs/validation_summary.json"),
        help="Ruta del reporte JSON",
    )
    args = parser.parse_args()
    summary = build_summary()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Autovalidacion: {summary['global_status']} -> {args.output}")
    return 0 if summary["global_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

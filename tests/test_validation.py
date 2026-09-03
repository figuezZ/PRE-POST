import json

from src.validation import (
    build_summary,
    main,
    validate_case,
    validate_service_case,
)


def test_reference_case_passes_with_versioned_tolerances():
    case = validate_case()

    assert case["status"] == "PASS"
    assert all(item["status"] == "PASS" for item in case["comparisons"])


def test_class_3_service_case_passes_with_published_values():
    case = validate_service_case()

    assert case["case_id"] == "S1"
    assert case["status"] == "PASS"
    assert len(case["comparisons"]) == 5
    assert all("published_value" in item for item in case["comparisons"])


def test_summary_contains_required_control_fields():
    summary = build_summary()

    assert summary["program_version"] == "0.4.0"
    assert summary["tests"] == {
        "executed": 11,
        "passed": 11,
        "failed": 0,
        "scope": "comparaciones numericas de los casos de referencia",
    }
    assert [case["case_id"] for case in summary["reference_cases"]] == [
        "A",
        "S1",
    ]
    assert summary["global_status"] == "PASS"
    assert summary["pending_warnings"]


def test_cli_writes_json_report(tmp_path, monkeypatch):
    output = tmp_path / "summary.json"
    monkeypatch.setattr(
        "sys.argv", ["validation", "--all", "--output", str(output)]
    )

    assert main() == 0
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["global_status"] == "PASS"

import json
from pathlib import Path

import pytest

from src.analysis import analyze_transfer
from src.models import DesignInput


def test_case_a_runs_from_json_through_the_core():
    payload = json.loads(
        Path("examples/case_a_analitico.json").read_text(encoding="utf-8")
    )
    result = analyze_transfer(DesignInput.from_mapping(payload["input"]))
    structured = result.to_dict()

    assert structured["section"]["area_m2"] == pytest.approx(0.32)
    assert structured["transfer"]["midspan_moment_n_m"] == pytest.approx(100_000.0)
    assert structured["transfer"]["stress"]["bottom_pa"] == pytest.approx(
        -5_468_750.0
    )
    assert "standard" in structured


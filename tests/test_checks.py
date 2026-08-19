import pytest

from src.checks import CheckResult, CheckStatus


def test_check_result_reports_demand_capacity_ratio():
    result = CheckResult(
        name="Ejemplo",
        status=CheckStatus.PASSES,
        demand=80.0,
        capacity=100.0,
        units="kN",
        method="Control",
        reference="Caso de prueba",
        message="Cumple",
    )

    assert result.demand_capacity_ratio == pytest.approx(0.8)
    assert result.status.value == "CUMPLE"


def test_not_applicable_check_has_no_ratio():
    result = CheckResult(
        name="Anclaje",
        status=CheckStatus.NOT_APPLICABLE,
        demand=None,
        capacity=None,
        units="-",
        method="Alcance",
        reference="docs/alcance.md",
        message="No aplica en esta version",
    )

    assert result.demand_capacity_ratio is None


import pytest

from src.units import (
    FOOT_M,
    INCH_M,
    KIP_N,
    LBF_N,
    PSI_PA,
    Quantity,
    UnitSystem,
    display_unit,
    from_si,
    normalize_unit_system,
    to_si,
)


def test_exact_uscs_base_conversions():
    assert to_si(1.0, Quantity.SPAN, UnitSystem.USCS) == pytest.approx(FOOT_M)
    assert to_si(1.0, Quantity.SECTION_LENGTH, UnitSystem.USCS) == pytest.approx(
        INCH_M
    )
    assert to_si(1.0, Quantity.FORCE, UnitSystem.USCS) == pytest.approx(KIP_N)
    assert to_si(1.0, Quantity.STRESS, UnitSystem.USCS) == pytest.approx(PSI_PA)
    assert to_si(1.0, Quantity.UNIT_WEIGHT, UnitSystem.USCS) == pytest.approx(
        LBF_N / FOOT_M**3
    )


@pytest.mark.parametrize("quantity", list(Quantity))
def test_si_uscs_round_trip_preserves_internal_value(quantity):
    internal_value = 12_345.6789

    displayed = from_si(internal_value, quantity, UnitSystem.USCS)

    assert to_si(displayed, quantity, UnitSystem.USCS) == pytest.approx(
        internal_value
    )


def test_si_display_units_keep_existing_conventions():
    assert display_unit("SI", Quantity.FORCE).symbol == "kN"
    assert display_unit("SI", Quantity.STRESS).symbol == "MPa"
    assert from_si(1_000_000.0, Quantity.STRESS, "SI") == pytest.approx(1.0)


def test_unit_system_rejects_unknown_option():
    with pytest.raises(ValueError, match="SI.*USCS"):
        normalize_unit_system("Imperial")


@pytest.mark.parametrize("value", [float("nan"), float("inf"), True])
def test_conversion_rejects_invalid_values(value):
    with pytest.raises(ValueError):
        to_si(value, Quantity.FORCE, UnitSystem.USCS)

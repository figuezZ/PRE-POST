import pytest

from src.analysis import simply_supported_uniform_load


def test_uniform_load_effects_match_static_equilibrium():
    result = simply_supported_uniform_load(8000.0, 10.0)

    assert result.reaction_n == pytest.approx(40_000.0)
    assert result.max_shear_n == pytest.approx(40_000.0)
    assert result.midspan_moment_n_m == pytest.approx(100_000.0)
    assert 2.0 * result.reaction_n == pytest.approx(8000.0 * 10.0)


def test_uniform_load_rejects_negative_load():
    with pytest.raises(ValueError):
        simply_supported_uniform_load(-1.0, 10.0)


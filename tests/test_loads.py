import pytest

from src.analysis import (
    simply_supported_uniform_load,
    simply_supported_uniform_load_at_section,
)


def test_uniform_load_effects_match_static_equilibrium():
    result = simply_supported_uniform_load(8000.0, 10.0)

    assert result.reaction_n == pytest.approx(40_000.0)
    assert result.max_shear_n == pytest.approx(40_000.0)
    assert result.midspan_moment_n_m == pytest.approx(100_000.0)
    assert 2.0 * result.reaction_n == pytest.approx(8000.0 * 10.0)


def test_uniform_load_rejects_negative_load():
    with pytest.raises(ValueError):
        simply_supported_uniform_load(-1.0, 10.0)


def test_example_6_section_effects_match_published_values():
    result = simply_supported_uniform_load_at_section(
        uniform_load_n_m=52_538.050573943,
        span_m=9.144,
        position_from_left_m=1.905,
    )

    assert result.left_reaction_n == pytest.approx(240_203.967224067)
    assert result.shear_n == pytest.approx(140_118.980880706)
    assert result.moment_n_m == pytest.approx(362_257.608069797)


@pytest.mark.parametrize("position", [-0.001, 9.145])
def test_section_effects_reject_position_outside_span(position):
    with pytest.raises(ValueError, match="dentro de la luz"):
        simply_supported_uniform_load_at_section(1.0, 9.144, position)

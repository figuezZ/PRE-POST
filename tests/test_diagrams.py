import pytest

from src.analysis import linear_fiber_stress_profile, uniform_load_diagram


def test_uniform_load_diagram_matches_supports_and_midspan():
    points = uniform_load_diagram(8000.0, 10.0, point_count=5)

    assert [point.position_m for point in points] == pytest.approx(
        [0.0, 2.5, 5.0, 7.5, 10.0]
    )
    assert [point.shear_n for point in points] == pytest.approx(
        [40_000.0, 20_000.0, 0.0, -20_000.0, -40_000.0]
    )
    assert [point.moment_n_m for point in points] == pytest.approx(
        [0.0, 75_000.0, 100_000.0, 75_000.0, 0.0]
    )


def test_uniform_load_diagram_rejects_too_few_points():
    with pytest.raises(ValueError, match="al menos 2"):
        uniform_load_diagram(8000.0, 10.0, point_count=1)


def test_linear_stress_profile_preserves_extremes_and_midpoint():
    points = linear_fiber_stress_profile(
        height_m=0.8,
        top_stress_pa=-1_000_000.0,
        bottom_stress_pa=-5_000_000.0,
        point_count=5,
    )

    assert [point.elevation_from_centroid_m for point in points] == pytest.approx(
        [-0.4, -0.2, 0.0, 0.2, 0.4]
    )
    assert [point.stress_pa for point in points] == pytest.approx(
        [-5_000_000.0, -4_000_000.0, -3_000_000.0, -2_000_000.0, -1_000_000.0]
    )


@pytest.mark.parametrize(
    ("height_m", "top_stress_pa", "bottom_stress_pa"),
    [
        (0.0, -1.0, -2.0),
        (float("nan"), -1.0, -2.0),
        (1.0, float("inf"), -2.0),
    ],
)
def test_linear_stress_profile_rejects_invalid_values(
    height_m, top_stress_pa, bottom_stress_pa
):
    with pytest.raises(ValueError):
        linear_fiber_stress_profile(
            height_m=height_m,
            top_stress_pa=top_stress_pa,
            bottom_stress_pa=bottom_stress_pa,
        )

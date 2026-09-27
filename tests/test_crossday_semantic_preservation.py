import numpy as np

from market_chi.modal_identifiability import (
    capture_percentile_against_directions,
    fixed_isotropic_directions,
    isotropic_capture_control,
)
from tools.mnq_crossday_semantic_preservation import DATES, KS, specs


def test_fixed_isotropic_directions_are_reproducible_and_unit_norm():
    a = fixed_isotropic_directions(20, count=256, seed=20260927)
    b = fixed_isotropic_directions(20, count=256, seed=20260927)
    assert np.allclose(a, b)
    assert np.allclose(np.linalg.norm(a, axis=1), 1.0)


def test_isotropic_control_tracks_dimension_fraction():
    directions = fixed_isotropic_directions(20, count=5000, seed=7)
    loadings = np.eye(20)
    out = isotropic_capture_control(loadings, directions, k=6)
    assert abs(out["mean"] - 0.30) < 0.02
    assert out["theoretical_isotropic_mean"] == 0.30
    assert out["q05"] < out["median"] < out["q95"]


def test_canonical_alignment_can_exceed_isotropic_control_without_p_value():
    directions = fixed_isotropic_directions(20, count=256, seed=20260927)
    loadings = np.eye(20)
    basis = np.eye(20)[0]
    p = capture_percentile_against_directions(
        loadings, basis, directions, k=2
    )
    assert p > 0.95


def test_q037_dates_are_development_only_and_exclude_may28_discovery():
    assert DATES == ("20260527", "20260529", "20260601", "20260602")
    assert "20260528" not in DATES
    assert all(not x.startswith("20260609") for x in DATES)
    assert all(not x.startswith("20260610") for x in DATES)
    assert all(not x.startswith("20260611") for x in DATES)


def test_q037_wall_clock_windows_are_fixed():
    for date_text in DATES:
        s60 = specs(date_text, 60)
        s30 = specs(date_text, 30)
        assert len(s60) == 21
        assert len(s30) == 42
        assert s60[0]["start"].endswith("00:00:00.000000000Z")
        assert s30[-1]["end"].endswith("21:00:00.000000000Z")


def test_fixed_k_set_does_not_adapt():
    assert KS == (2, 3, 4, 6, 10)

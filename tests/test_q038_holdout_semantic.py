import numpy as np

from market_chi.holdout_semantic import (
    ISOTROPIC_MEAN_D20,
    ISOTROPIC_Q95_D20,
    BootstrapResult,
    moving_block_bootstrap,
    pooled_median,
    primary_outcome,
)
from tools.mnq_q038_holdout_semantic import (
    CORRIDOR_STARTS,
    DATES,
    MIN_PRIMARY_WINDOWS_PER_DAY,
    eligible_segment,
    specs,
)


def test_exact_isotropic_constants_match_dimension_mean():
    assert ISOTROPIC_MEAN_D20[6] == 0.3
    assert ISOTROPIC_MEAN_D20[10] == 0.5
    assert 0.54 < ISOTROPIC_Q95_D20[6] < 0.56
    assert 0.74 < ISOTROPIC_Q95_D20[10] < 0.76


def test_isotropic_q95_matches_known_truth_monte_carlo():
    rng = np.random.default_rng(12345)
    x = rng.normal(size=(100_000, 20))
    x /= np.linalg.norm(x, axis=1)[:, None]
    capture6 = np.sum(x[:, :6] ** 2, axis=1)
    empirical = float(np.quantile(capture6, 0.95))
    assert abs(empirical - ISOTROPIC_Q95_D20[6]) < 0.01


def test_block_bootstrap_is_reproducible_and_preserves_nan_slots():
    days = [
        np.array([0.2, 0.3, np.nan, 0.4, 0.5, 0.6]),
        np.array([0.1, 0.2, 0.3, np.nan, 0.4, 0.5]),
        np.array([0.4, 0.5, 0.6, 0.7, np.nan, 0.8]),
    ]
    a = moving_block_bootstrap(days, pooled_median, block_length=2, reps=500, seed=7)
    b = moving_block_bootstrap(days, pooled_median, block_length=2, reps=500, seed=7)
    assert a.to_dict() == b.to_dict()
    assert np.isfinite(a.point)
    assert a.reps_valid >= 475


def test_primary_outcome_cannot_be_rescued_by_sensitivity():
    survive = BootstrapResult(0.2, 0.1, 0.3, 1000, 1000, 4, 1)
    weak = BootstrapResult(0.2, -0.01, 0.3, 1000, 1000, 2, 1)
    falsified = BootstrapResult(-0.2, -0.3, -0.1, 1000, 1000, 4, 1)
    assert primary_outcome(survive, [survive, survive]) == "EMPIRICAL_CLAIM_SURVIVES_FROZEN_TEST"
    assert primary_outcome(survive, [weak, survive]) == "INDETERMINATE"
    assert primary_outcome(falsified, [survive, survive]) == "EMPIRICAL_CLAIM_FALSIFIED"


def test_q038_holdout_dates_and_windows_are_frozen():
    assert DATES == ("20260609", "20260610", "20260611")
    assert len(specs("20260609", 30)) == 42
    assert len(specs("20260609", 60)) == 21
    assert MIN_PRIMARY_WINDOWS_PER_DAY == 34
    assert CORRIDOR_STARTS == {"08:30", "09:00", "09:30", "10:00", "10:30"}


def test_segmentation_refuses_two_eligible_instruments():
    lo = 0
    hi = 2_000_000_000
    rows = []
    for iid, sym in (("1", "MNQM6"), ("2", "MNQU6")):
        for t in (0, 1_000_000_000):
            rows.append({
                "bin_start_ns": str(t),
                "instrument_id": iid,
                "symbol": sym,
            })
    status, selected, info = eligible_segment(rows, lo, hi)
    assert status == "AMBIGUOUS_MULTI_INSTRUMENT"
    assert selected is None
    assert info["eligible_segment_count"] == 2


def test_segmentation_accepts_exactly_one_eligible_instrument():
    lo = 0
    hi = 2_000_000_000
    rows = [
        {"bin_start_ns": "0", "instrument_id": "1", "symbol": "MNQM6"},
        {"bin_start_ns": "1000000000", "instrument_id": "1", "symbol": "MNQM6"},
        {"bin_start_ns": "1000000000", "instrument_id": "2", "symbol": "MNQU6"},
    ]
    status, selected, info = eligible_segment(rows, lo, hi)
    assert status == "ELIGIBLE"
    assert selected is not None
    assert info["eligible_segment_count"] == 1
    assert info["selected_segment"]["instrument_id"] == "1"

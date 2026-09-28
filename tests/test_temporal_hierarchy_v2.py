import numpy as np

from market_chi.temporal_hierarchy_v2 import (
    BootstrapResult,
    bootstrap_delta_by_day,
    classify_pair,
    evaluate_pair_day,
)


NS = 1_000_000_000


def _semantic_seconds_from_coarse(pattern_mode: str, seed: int = 7):
    """Build 14 hours of 1-second semantic data for the 60->300 test pair."""
    rng = np.random.default_rng(seed)
    hours = 14
    coarse_seconds = 300
    fine_seconds = 60
    n_coarse = hours * 3600 // coarse_seconds
    day_start = 0
    t = np.arange(hours * 3600, dtype=np.int64) * NS

    if pattern_mode == "shape_predicts":
        amp = rng.normal(size=(n_coarse, 2))
        mean = np.zeros_like(amp)
        mean[1:] = amp[:-1]
        pattern = np.array([-1.0, -0.5, 0.0, 0.5, 1.0])
        fine = mean[:, None, :] + pattern[None, :, None] * amp[:, None, :]
    elif pattern_mode == "no_extra":
        mean = np.zeros((n_coarse, 2))
        mean[0] = [0.4, -0.2]
        for i in range(1, n_coarse):
            mean[i] = 0.85 * mean[i - 1] + np.array([0.01, -0.005])
        fine = np.repeat(mean[:, None, :], 5, axis=1)
    elif pattern_mode == "phase_only":
        starts = np.arange(n_coarse) * coarse_seconds
        phase = starts / (21 * 3600)
        mean = np.column_stack([
            np.sin(2 * np.pi * phase),
            np.cos(2 * np.pi * phase),
        ])
        nuisance = 0.2 * np.column_stack([
            np.sin(4 * np.pi * phase),
            np.cos(4 * np.pi * phase),
        ])
        pattern = np.array([-1.0, -0.5, 0.0, 0.5, 1.0])
        fine = mean[:, None, :] + pattern[None, :, None] * nuisance[:, None, :]
    else:
        raise ValueError(pattern_mode)

    semantic = np.empty((hours * 3600, 2), dtype=float)
    for cb in range(n_coarse):
        for fb in range(5):
            lo = cb * coarse_seconds + fb * fine_seconds
            hi = lo + fine_seconds
            semantic[lo:hi] = fine[cb, fb]
    return t, semantic, day_start


def test_structured_shape_adds_beyond_current_coarse_state():
    t, s, start = _semantic_seconds_from_coarse("shape_predicts")
    result, extra = evaluate_pair_day(
        t, s,
        fine_seconds=60,
        coarse_seconds=300,
        day_start_ns=start,
        lead_blocks=1,
    )
    assert result.status == "COMPLETE"
    assert result.leakage_guard_passed
    assert result.delta_b_mean > 0.25
    assert result.depth_mae_structured < result.depth_mae_baseline
    assert result.imbalance_mae_structured < result.imbalance_mae_baseline
    assert np.nanmean(extra["delta_b"]) > 0.25


def test_structured_model_does_not_gain_when_fine_shape_has_no_extra_information():
    t, s, start = _semantic_seconds_from_coarse("no_extra")
    result, _ = evaluate_pair_day(
        t, s,
        fine_seconds=60,
        coarse_seconds=300,
        day_start_ns=start,
        lead_blocks=1,
    )
    assert result.status == "COMPLETE"
    assert result.leakage_guard_passed
    assert abs(result.delta_b_mean) < 1e-8


def test_session_phase_control_prevents_spurious_shape_gain():
    t, s, start = _semantic_seconds_from_coarse("phase_only")
    result, _ = evaluate_pair_day(
        t, s,
        fine_seconds=60,
        coarse_seconds=300,
        day_start_ns=start,
        lead_blocks=1,
    )
    assert result.status == "COMPLETE"
    assert result.leakage_guard_passed
    assert result.delta_b_mean < 0.02


def test_lead_zero_is_refused():
    t, s, start = _semantic_seconds_from_coarse("no_extra")
    try:
        evaluate_pair_day(
            t, s,
            fine_seconds=60,
            coarse_seconds=300,
            day_start_ns=start,
            lead_blocks=0,
        )
    except ValueError as exc:
        assert "lead_blocks" in str(exc)
    else:
        raise AssertionError("lead_blocks=0 must be refused")


def test_nonfrozen_scale_pair_is_refused():
    t, s, start = _semantic_seconds_from_coarse("no_extra")
    try:
        evaluate_pair_day(
            t, s,
            fine_seconds=15,
            coarse_seconds=60,
            day_start_ns=start,
            lead_blocks=1,
        )
    except ValueError as exc:
        assert "frozen hierarchy" in str(exc)
    else:
        raise AssertionError("nonfrozen pair must be refused")


def test_insufficient_post_training_wall_clock_evaluation_refuses():
    # 10 hours cannot satisfy 5 h training + 8 h post-training evaluation.
    t, s, start = _semantic_seconds_from_coarse("no_extra")
    keep = t < 10 * 3600 * NS
    result, _ = evaluate_pair_day(
        t[keep], s[keep],
        fine_seconds=60,
        coarse_seconds=300,
        day_start_ns=start,
        lead_blocks=1,
    )
    assert result.status == "REFUSED_INSUFFICIENT_EVALUATION"


def test_bootstrap_is_seeded_and_uses_one_hour_wall_clock_blocks():
    arrays = [
        np.linspace(0.1, 0.3, 100),
        np.linspace(0.2, 0.4, 100),
        np.linspace(0.0, 0.2, 100),
        np.linspace(0.15, 0.35, 100),
        np.linspace(0.05, 0.25, 100),
    ]
    a = bootstrap_delta_by_day(arrays, coarse_seconds=300, reps=1000, seed=20260929)
    b = bootstrap_delta_by_day(arrays, coarse_seconds=300, reps=1000, seed=20260929)
    assert a == b
    assert a.block_length_observations == 12
    assert a.lower > 0


def test_pair_classification_known_truths():
    add = BootstrapResult(0.2, 0.1, 0.3, 10000, 10000, 12, 20260929)
    out = classify_pair(
        add, [0.1, 0.2, 0.05, 0.08, -0.01],
        depth_mae_baseline=1.0,
        depth_mae_structured=0.8,
        imbalance_mae_baseline=1.1,
        imbalance_mae_structured=0.9,
    )
    assert out == "ADDS_P0D"

    sub = BootstrapResult(-0.2, -0.3, -0.1, 10000, 10000, 12, 20260929)
    out2 = classify_pair(
        sub, [-0.1] * 5,
        depth_mae_baseline=1.0,
        depth_mae_structured=1.2,
        imbalance_mae_baseline=1.0,
        imbalance_mae_structured=1.2,
    )
    assert out2 == "SUBTRACTS_P0D"

import numpy as np

from market_chi.recovery import RecoveryConfig, analyze_recovery_cycle


def cfg(**kw):
    base = dict(
        break_threshold=0.5,
        min_recovery_excursion=0.30,
        failure_drop=0.25,
        reclaim_level=0.0,
        sustain_level=0.0,
        sustain_samples=3,
        max_samples_after_break=100,
    )
    base.update(kw)
    return RecoveryConfig(**base)


def test_failed_recovery_can_cross_level_then_fail_to_sustain():
    x = np.array([0.4, 0.2, -0.7, -0.9, -0.5, -0.1, 0.08, 0.06, -0.25, -0.55])
    out = analyze_recovery_cycle(x, 2, cfg())
    assert out.status == "FAILED_RECOVERIES"
    assert out.failed_attempt_count == 1
    assert out.attempts[0].crossed_reclaim_level is True
    assert out.attempts[0].sustained_reclaim is False


def test_three_to_five_is_not_hardcoded_as_admission_rule():
    x = np.array([0.2, -0.7, -0.9, -0.5, -0.1, -0.45, -0.8])
    out = analyze_recovery_cycle(x, 1, cfg())
    assert out.status == "FAILED_RECOVERIES"
    assert out.failed_attempt_count == 1


def test_sustained_reclaim_is_distinct_from_failed_recovery():
    x = np.array([0.3, -0.8, -0.9, -0.5, -0.1, 0.05, 0.08, 0.12, 0.15])
    out = analyze_recovery_cycle(x, 1, cfg())
    assert out.status == "SUSTAINED_RECLAIM"
    assert out.sustained_reclaim is True
    assert out.attempts[-1].outcome == "SUSTAINED_RECLAIM"


def test_simple_touch_without_active_recovery_is_not_called_rejection():
    x = np.array([0.2, -0.8, -0.85, -0.75, -0.82, -0.78, -0.9])
    out = analyze_recovery_cycle(x, 1, cfg(min_recovery_excursion=0.30))
    assert out.status == "NO_QUALIFYING_RECOVERY"
    assert out.failed_attempt_count == 0


def test_invalid_break_is_refused():
    out = analyze_recovery_cycle(np.array([0.1, -0.2, -0.1]), 1, cfg())
    assert out.status == "REFUSED_BREAK"

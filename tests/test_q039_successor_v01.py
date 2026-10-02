import numpy as np

from market_chi.q039_successor_v01 import (
    bootstrap_regime_heterogeneity,
    factor2_rank_audit,
    holm_adjust,
    run_repaired_factor2_truth,
)


def test_factor2_repair_removes_exact_rank_collision():
    for scale in (30, 60):
        audit = factor2_rank_audit(seed=20261001 + scale, coarse_seconds=scale)
        assert audit["old_rank"] == audit["old_p"] - 1
        assert audit["repaired_a2_rank"] == audit["repaired_a2_p"]
        assert audit["repaired_f2_rank"] == audit["repaired_f2_p"]


def test_factor2_repaired_known_truths():
    for scale in (30, 60):
        sem = run_repaired_factor2_truth(
            "semantic_recency",
            base_seed=20261100 + scale,
            coarse_seconds=scale,
            reps=1000,
        )
        assert sem["status"] == "COMPLETE"
        assert sem["label"] == "LAST_FAST_SEMANTIC_ADDS_P0D"

        for offset, kind in enumerate(("phase_only", "coarse_sufficient", "latent_regime"), start=1):
            null = run_repaired_factor2_truth(
                kind,
                base_seed=20261200 + 10 * scale + offset,
                coarse_seconds=scale,
                reps=1000,
            )
            assert null["status"] == "COMPLETE"
            assert null["label"] != "LAST_FAST_SEMANTIC_ADDS_P0D"


def test_regime_heterogeneity_detects_known_shift():
    rng = np.random.default_rng(20261001)
    gains = []
    highs = []
    for _ in range(5):
        h = np.tile(np.array([False, True]), 60)
        g = rng.normal(scale=0.15, size=len(h)) + h.astype(float) * 0.45
        gains.append(g)
        highs.append(h)

    result = bootstrap_regime_heterogeneity(
        gains,
        highs,
        block_observations=12,
        reps=2000,
        seed=20261002,
    )
    assert result.status == "COMPLETE"
    assert result.point > 0
    assert result.lower > 0
    assert result.p_value < 0.05


def test_regime_heterogeneity_refuses_sparse_strata():
    gains = [np.linspace(-0.1, 0.1, 30) for _ in range(5)]
    highs = [np.zeros(30, dtype=bool) for _ in range(5)]
    result = bootstrap_regime_heterogeneity(
        gains,
        highs,
        block_observations=12,
        reps=100,
        seed=20261002,
    )
    assert result.status == "REGIME_HETEROGENEITY_INSUFFICIENT_SUPPORT"


def test_holm_adjust():
    out = holm_adjust([0.01, 0.04, 0.03, 0.20])
    assert len(out) == 4
    assert all(0 <= x <= 1 for x in out)
    assert out[0] <= out[3]

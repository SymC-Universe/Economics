from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from market_chi.q039_successor_v01 import (
    bootstrap_regime_heterogeneity,
    factor2_rank_audit,
    holm_adjust,
    run_repaired_factor2_truth,
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    rank = {}
    truths = {}
    passed = True

    for scale in (30, 60):
        ra = factor2_rank_audit(seed=20261001 + scale, coarse_seconds=scale)
        rank[str(scale)] = ra
        passed &= ra["old_rank"] == ra["old_p"] - 1
        passed &= ra["repaired_a2_rank"] == ra["repaired_a2_p"]
        passed &= ra["repaired_f2_rank"] == ra["repaired_f2_p"]

        scale_truths = {}
        for offset, kind in enumerate(
            ("phase_only", "coarse_sufficient", "latent_regime", "semantic_recency"),
            start=1,
        ):
            result = run_repaired_factor2_truth(
                kind,
                base_seed=20262000 + 100 * scale + offset,
                coarse_seconds=scale,
                reps=3000,
            )
            scale_truths[kind] = result
            passed &= result["status"] == "COMPLETE"
            if kind == "semantic_recency":
                passed &= result["label"] == "LAST_FAST_SEMANTIC_ADDS_P0D"
            else:
                passed &= result["label"] != "LAST_FAST_SEMANTIC_ADDS_P0D"
        truths[str(scale)] = scale_truths

    rng = np.random.default_rng(20261001)
    gain_shift = []
    high_shift = []
    gain_null = []
    high_null = []
    for _ in range(5):
        h = np.tile(np.array([False, True]), 60)
        gain_shift.append(rng.normal(scale=0.15, size=len(h)) + h.astype(float) * 0.45)
        high_shift.append(h)
        gain_null.append(np.zeros(len(h), dtype=float))
        high_null.append(h)

    regime_shift = bootstrap_regime_heterogeneity(
        gain_shift, high_shift, block_observations=12, reps=5000, seed=20261002
    )
    regime_null = bootstrap_regime_heterogeneity(
        gain_null, high_null, block_observations=12, reps=5000, seed=20261003
    )
    passed &= regime_shift.status == "COMPLETE"
    passed &= regime_shift.point > 0 and regime_shift.lower > 0 and regime_shift.p_value < 0.05
    passed &= regime_null.status == "COMPLETE"
    passed &= abs(regime_null.point) <= 1e-12 and regime_null.p_value >= 0.95

    holm_example = holm_adjust([0.01, 0.04, 0.03, 0.20])

    payload = {
        "schema_version": "q039-successor-v0.1-synthetic-qualification-v1",
        "date": "2026-10-01",
        "real_successor_outcomes_opened": False,
        "factor2_rank_audit": rank,
        "factor2_known_truths": truths,
        "regime_known_shift": regime_shift.__dict__,
        "regime_null": regime_null.__dict__,
        "holm_example": holm_example,
        "status": "PASS" if passed else "FAIL",
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "mnq_temporal_hierarchy_development",
    ROOT / "tools" / "mnq_temporal_hierarchy_development.py",
)
mod = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(mod)


def test_runner_contract_stays_development_only_and_fixed_scale():
    assert mod.DATES == ["20260527", "20260528", "20260529", "20260601", "20260602"]
    assert mod.FACTORS == [15, 30, 60, 300]
    assert mod.TARGETS == ["log_depth_capacity", "log_side_contrast"]
    assert {"20260609", "20260610", "20260611"}.isdisjoint(mod.DATES)


def test_wall_clock_blocks_require_complete_native_seconds():
    day = "20260527"
    start = mod._day_start_ns(day)
    ns = 1_000_000_000
    series = {
        start + i * ns: np.asarray([float(i), float(-i)])
        for i in range(60)
    }
    blocks = mod.build_blocks(series, day, 15)
    assert sorted(blocks) == [0, 1, 2, 3]
    assert blocks[0]["structured"].shape == (12,)
    assert blocks[0]["last"].shape == (2,)
    assert np.allclose(blocks[0]["coarse"], np.asarray([7.0, -7.0]))

    del series[start + 20 * ns]
    blocks_missing = mod.build_blocks(series, day, 15)
    assert sorted(blocks_missing) == [0, 2, 3]


def test_evaluate_is_strictly_lagged_and_emits_both_baselines():
    factor = 15
    blocks = {}
    rng = np.random.default_rng(20260928)
    latent = rng.normal(size=90)
    for b in range(90):
        cur = latent[b]
        nxt = latent[b + 1] if b + 1 < len(latent) else 0.0
        structured = np.asarray([cur, nxt] + [0.0] * 10, dtype=float)
        last = np.asarray([cur, 0.0], dtype=float)
        coarse = np.asarray([cur, -cur], dtype=float)
        blocks[b] = {"structured": structured, "last": last, "coarse": coarse}

    rec = mod.evaluate(
        blocks,
        target_idx=0,
        factor=factor,
        lead_blocks=1,
        min_train_blocks=30,
        test_block_size=10,
    )
    assert rec["status"] == "COMPLETE"
    assert rec["lead_blocks"] == 1
    assert rec["lead_seconds"] == 15
    assert "delta_r2_vs_last" in rec
    assert "delta_r2_vs_persistence" in rec
    assert rec["n_test"] > 0


def test_insufficient_blocks_refuse_instead_of_tuning():
    blocks = {
        i: {
            "structured": np.zeros(12),
            "last": np.zeros(2),
            "coarse": np.zeros(2),
        }
        for i in range(20)
    }
    rec = mod.evaluate(
        blocks,
        target_idx=0,
        factor=300,
        lead_blocks=1,
        min_train_blocks=30,
        test_block_size=10,
    )
    assert rec["status"] == "REFUSED_INSUFFICIENT_BLOCKS"

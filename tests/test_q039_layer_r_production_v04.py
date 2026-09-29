from __future__ import annotations

import math
import numpy as np

from market_chi.q039_blocks_v04 import BlockRecord
from market_chi.q039_layer_r_production_v04 import (
    adjacent_k6_principal_cosines,
    analyze_layer_r_blocks,
    phase_design_from_block_indices,
)


def _block(i: int, x: np.ndarray, scale: int = 300) -> BlockRecord:
    return BlockRecord(
        "COMPLETE", scale, i,
        i * scale * 1_000_000_000,
        (i + 1) * scale * 1_000_000_000,
        scale,
        tuple(float(v) for v in x),
        0.0, 0.0,
        1.0, 1.0, 0.0,
        0.25, 0.0, 0.0,
        0.0, 0.0, 1.0,
    )


def test_phase_design_uses_actual_block_index_not_compressed_row_number():
    q = phase_design_from_block_indices(np.asarray([2, 3]), scale_seconds=300)
    phase2 = 2 * 300 / (21 * 3600)
    assert math.isclose(q[0, 1], math.sin(2 * math.pi * phase2))
    assert math.isclose(q[0, 2], math.cos(2 * math.pi * phase2))


def test_layer_r_production_reports_spectrum_and_direction_diagnostics():
    rng = np.random.default_rng(12)
    blocks = [_block(i, rng.normal(size=20)) for i in range(2, 252)]
    r = analyze_layer_r_blocks(blocks, scale_seconds=300, matched_draws=100)
    assert r["status"] == "COMPLETE"
    assert r["first_complete_block_index"] == 2
    assert "effective_rank" in r["spectral"]
    assert len(r["direction_diagnostics"]["sym_lineage"]["contributions_pc1_to_pc6"]) == 6
    assert r["phase_design_uses_actual_block_indices"] is True


def test_adjacent_principal_cosines_are_one_for_identical_basis():
    rng = np.random.default_rng(44)
    blocks = [_block(i, rng.normal(size=20)) for i in range(252)]
    a = analyze_layer_r_blocks(blocks, scale_seconds=300, matched_draws=50)
    b = analyze_layer_r_blocks(blocks, scale_seconds=300, matched_draws=50)
    c = adjacent_k6_principal_cosines(a, b)
    assert c["status"] == "COMPLETE"
    assert np.allclose(c["principal_cosines"], np.ones(6), atol=1e-10)

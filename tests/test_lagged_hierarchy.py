import numpy as np

from market_chi.lagged_hierarchy import walk_forward_lagged_hierarchy


def test_structured_fast_block_predicts_future_coarse_state_beyond_last_and_persistence():
    rng = np.random.default_rng(20260927)
    factor = 10
    n_blocks = 140
    amplitudes = rng.normal(size=n_blocks)
    phase = np.sin(np.linspace(0.0, np.pi, factor))
    blocks = np.stack([a * phase for a in amplitudes], axis=0)
    fine = blocks.reshape(-1, 1)

    # y[t+1] is encoded by the within-block shape/amplitude at block t.
    # The last fast observation is always ~0 and y[t] is the previous,
    # independent amplitude, so neither comparator has the same information.
    y = np.empty(n_blocks)
    y[0] = 0.0
    y[1:] = amplitudes[:-1]

    result = walk_forward_lagged_hierarchy(
        fine,
        y,
        factor,
        lead_blocks=1,
        min_train_blocks=40,
        test_block_size=10,
    )

    assert result.status == "COMPLETE"
    assert result.structured_r2 > 0.98
    assert result.delta_r2_vs_last > 0.8
    assert result.delta_r2_vs_persistence > 0.8


def test_structured_summary_does_not_gain_over_last_when_block_has_no_extra_structure():
    factor = 8
    n_blocks = 120
    y = np.zeros(n_blocks)
    y[0] = 1.0
    for i in range(1, n_blocks):
        y[i] = 0.82 * y[i - 1] + 0.03

    # Every observation inside a block is identical to current coarse state.
    # Structured summary therefore contains no information beyond LAST_FAST.
    fine = np.repeat(y[:, None], factor, axis=1).reshape(-1, 1)

    result = walk_forward_lagged_hierarchy(
        fine,
        y,
        factor,
        lead_blocks=1,
        min_train_blocks=30,
        test_block_size=10,
    )

    assert result.status == "COMPLETE"
    assert abs(result.delta_r2_vs_last) < 1e-10


def test_lagged_hierarchy_refuses_insufficient_blocks():
    fine = np.arange(40, dtype=float)[:, None]
    y = np.arange(4, dtype=float)
    result = walk_forward_lagged_hierarchy(
        fine,
        y,
        factor=10,
        lead_blocks=1,
        min_train_blocks=10,
        test_block_size=5,
    )
    assert result.status == "REFUSED_INSUFFICIENT_BLOCKS"


def test_lagged_hierarchy_requires_future_lead():
    fine = np.arange(100, dtype=float)[:, None]
    y = np.arange(10, dtype=float)
    try:
        walk_forward_lagged_hierarchy(fine, y, factor=10, lead_blocks=0)
    except ValueError as exc:
        assert "lead_blocks" in str(exc)
    else:
        raise AssertionError("lead_blocks=0 should be refused")

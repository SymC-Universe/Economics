import numpy as np

from market_chi.temporal_inheritance import summarize_fine_blocks, walk_forward_inheritance


def test_block_summary_shapes():
    x = np.arange(40.0).reshape(20, 2)
    full, last = summarize_fine_blocks(x, factor=5)
    assert full.shape == (4, 12)
    assert last.shape == (4, 2)


def test_structured_fast_state_adds_over_last_value_for_known_truth():
    rng = np.random.default_rng(7)
    factor = 8
    blocks = 140
    fine = rng.normal(size=(blocks * factor, 1))
    shaped = fine.reshape(blocks, factor)
    target = 1.7 * shaped.mean(axis=1) + 0.8 * shaped.std(axis=1)
    out = walk_forward_inheritance(fine, target, factor, min_train_blocks=40, test_block_size=10)
    assert out.status == "COMPLETE"
    assert out.full_r2 > 0.90
    assert out.delta_r2 > 0.25


def test_permuted_target_does_not_fake_strong_inheritance():
    rng = np.random.default_rng(8)
    factor = 8
    blocks = 140
    fine = rng.normal(size=(blocks * factor, 1))
    shaped = fine.reshape(blocks, factor)
    target = shaped.mean(axis=1)
    rng.shuffle(target)
    out = walk_forward_inheritance(fine, target, factor, min_train_blocks=40, test_block_size=10)
    assert out.status == "COMPLETE"
    assert out.full_r2 < 0.30


def test_insufficient_blocks_refuse():
    x = np.arange(40.0)
    y = np.arange(8.0)
    out = walk_forward_inheritance(x, y, factor=5, min_train_blocks=10, test_block_size=5)
    assert out.status == "REFUSED_INSUFFICIENT_BLOCKS"

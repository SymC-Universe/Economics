import numpy as np

from market_chi.modal_identifiability import (
    canonical_depth_bases,
    semantic_capture_table,
    spectral_metrics,
    strongest_mode,
    subspace_capture,
)
from tools.mnq_may28_modal_identifiability import specs


def test_rank_migration_is_recovered_by_wider_fixed_subspace():
    A = np.eye(4)
    basis = np.array([0.0, 0.0, 1.0, 0.0])
    assert subspace_capture(A, basis, k=2) == 0.0
    assert subspace_capture(A, basis, k=3) == 1.0


def test_subspace_capture_is_rotation_invariant():
    theta = 0.61
    A = np.eye(4)
    B = np.eye(4)
    B[:2] = np.array([
        [np.cos(theta), np.sin(theta), 0.0, 0.0],
        [-np.sin(theta), np.cos(theta), 0.0, 0.0],
    ])
    basis = np.array([1.0, 0.0, 0.0, 0.0])
    assert np.isclose(subspace_capture(A, basis, k=2), 1.0)
    assert np.isclose(subspace_capture(B, basis, k=2), 1.0)


def test_canonical_depth_bases_are_unit_norm():
    bases = canonical_depth_bases(10)
    assert set(bases) == {
        "symmetric_depth",
        "bid_ask_imbalance",
        "depth_gradient",
        "side_gradient",
    }
    for v in bases.values():
        assert len(v) == 20
        assert np.isclose(np.linalg.norm(v), 1.0)


def test_semantic_capture_table_uses_fixed_requested_k():
    A = np.eye(20)
    bases = {"first": np.eye(20)[0], "seventh": np.eye(20)[6]}
    out = semantic_capture_table(A, bases, ks=(2, 6, 10))
    assert out["first"] == {"2": 1.0, "6": 1.0, "10": 1.0}
    assert out["seventh"]["2"] == 0.0
    assert out["seventh"]["6"] == 0.0
    assert out["seventh"]["10"] == 1.0


def test_spectral_metrics_distinguish_flat_from_concentrated():
    flat = spectral_metrics([0.25, 0.25, 0.25, 0.25], ks=(2, 3))
    concentrated = spectral_metrics([0.7, 0.1, 0.1, 0.1], ks=(2, 3))
    assert np.isclose(flat["entropy_normalized"], 1.0)
    assert flat["effective_rank"] > concentrated["effective_rank"]
    assert concentrated["gaps"]["1_2"] > flat["gaps"]["1_2"]


def test_strongest_mode_reports_rank_not_sign():
    A = np.eye(4)
    basis = np.array([0.0, -1.0, 0.0, 0.0])
    out = strongest_mode(A, basis)
    assert out["pc"] == 2
    assert np.isclose(out["alignment"], 1.0)


def test_identifiability_windows_are_frozen_wall_clock():
    assert len(specs(60)) == 21
    assert len(specs(30)) == 42
    assert specs(60)[0]["start"] == "2026-05-28T00:00:00.000000000Z"
    assert specs(30)[-1]["end"] == "2026-05-28T21:00:00.000000000Z"

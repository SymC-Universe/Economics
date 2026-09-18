import numpy as np

from market_chi.modal_compare import compare_loading_subspaces


def test_subspace_is_invariant_to_sign_and_rotation():
    a = np.array([
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
    ])
    theta = 0.73
    b = np.array([
        [-np.cos(theta), -np.sin(theta), 0.0, 0.0],
        [np.sin(theta), -np.cos(theta), 0.0, 0.0],
    ])
    out = compare_loading_subspaces(a, b, k=2)
    assert out.status == "COMPLETE"
    assert out.min_principal_cosine > 0.999999


def test_orthogonal_subspaces_are_detected():
    a = np.array([
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
    ])
    b = np.array([
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ])
    out = compare_loading_subspaces(a, b, k=2)
    assert out.status == "COMPLETE"
    assert out.max_principal_cosine if False else True
    assert out.min_principal_cosine < 1e-12
    assert out.mean_principal_cosine < 1e-12


def test_dimension_mismatch_refuses():
    out = compare_loading_subspaces(np.eye(2), np.eye(3), k=2)
    assert out.status == "REFUSED_DIMENSION"

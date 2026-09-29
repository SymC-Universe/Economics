from market_chi.q039_layer_r_v04 import run_structural_known_truth


def test_nc6_heavy_tail_no_special_structure_never_structure_specific():
    r = run_structural_known_truth(
        "heavy_tail", base_seed=20261016, matched_draws=1000
    )
    assert r["classification"]["status"] != "STRUCTURE_SPECIFIC_PAIR_COHERENT_P0D"


def test_nc8_calendar_common_mode_is_removed_or_unresolved():
    r = run_structural_known_truth(
        "calendar_common_mode", base_seed=20261018, matched_draws=1000
    )
    assert r["classification"]["status"] != "STRUCTURE_SPECIFIC_PAIR_COHERENT_P0D"


def test_nc8b_persistent_common_mode_is_demoted_by_rho1():
    r = run_structural_known_truth(
        "persistent_common_mode",
        base_seed=20261019,
        matched_draws=1000,
        persistence=0.90,
        sym_innovation_sd=0.35,
        imb_innovation_sd=0.30,
        isotropic_noise_sd=0.30,
    )
    assert r["classification"]["status"] in {
        "CANONICAL_CAPTURE_ONLY_P0D",
        "STRUCTURAL_UNRESOLVED_P0D",
    }
    assert r["classification"]["status"] != "STRUCTURE_SPECIFIC_PAIR_COHERENT_P0D"

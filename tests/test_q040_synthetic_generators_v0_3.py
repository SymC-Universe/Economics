import json
from pathlib import Path
import numpy as np

from market_chi.q040_synthetic_generators_v0_3 import audit_generator, generate_control


def test_all_v03_generator_contracts_pass():
    root = Path(__file__).resolve().parents[1]
    m = json.loads(
        (root / "qualification" / "Q040_SYNTHETIC_KNOWN_TRUTH_MANIFEST_v0.3_2026-10-02.json").read_text()
    )
    base = int(m["base_seed"])
    for item in m["controls"]:
        seed = int(
            np.random.SeedSequence([base, int(item["ordinal"])])
            .generate_state(1, dtype=np.uint32)[0]
        )
        data = generate_control(
            item["id"], seed=seed, n=int(m["generator_contract_points"])
        )
        audit = audit_generator(item["id"], data)
        assert audit.pass_invariant, (item["id"], audit.details)


def test_v03_manifest_semantics():
    root = Path(__file__).resolve().parents[1]
    m = json.loads(
        (root / "qualification" / "Q040_SYNTHETIC_KNOWN_TRUTH_MANIFEST_v0.2_2026-10-02.json").read_text()
    )
    by_id = {x["id"]: x for x in m["controls"]}
    assert "clustered" in by_id["NC-R2"]["generator"]
    assert by_id["NC-R3"]["generator"] == "true_erosion"
    assert "within_scale_history_no_cross_scale" == by_id["NC-R10"]["generator"]
    assert "latent_regime" in by_id["NC-R17"]["generator"]
    assert m["sparse_tail_min_qualifying_episodes_per_stratum"] == 10


def test_v03_support_floor():
    root = Path(__file__).resolve().parents[1]
    m = json.loads(
        (root / "qualification" / "Q040_SYNTHETIC_KNOWN_TRUTH_MANIFEST_v0.3_2026-10-02.json").read_text()
    )
    base = int(m["base_seed"])
    for item in m["controls"]:
        seed = int(
            np.random.SeedSequence([base, int(item["ordinal"])])
            .generate_state(1, dtype=np.uint32)[0]
        )
        data = generate_control(item["id"], seed=seed, n=int(m["generator_contract_points"]))
        if item["id"] == "NC-R21":
            assert int(np.count_nonzero(data["shock"])) == 9
        elif "shock" in data:
            assert int(np.count_nonzero(data["shock"])) >= 40

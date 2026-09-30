import json
from pathlib import Path
import numpy as np

from market_chi.q040_synthetic_generators_v0_1 import audit_generator, generate_control


def test_all_frozen_generator_contracts_pass():
    root=Path(__file__).resolve().parents[1]
    m=json.loads((root/"qualification"/"Q040_SYNTHETIC_KNOWN_TRUTH_MANIFEST_v0.1_2026-09-30.json").read_text())
    base=int(m["base_seed"])
    for item in m["controls"]:
        seed=int(np.random.SeedSequence([base,int(item["ordinal"])]).generate_state(1,dtype=np.uint32)[0])
        data=generate_control(item["id"],seed=seed,n=int(m["generator_contract_points"]))
        audit=audit_generator(item["id"],data)
        assert audit.pass_invariant, (item["id"], audit.details)


def test_sparse_tail_threshold_is_frozen_at_ten():
    root=Path(__file__).resolve().parents[1]
    m=json.loads((root/"qualification"/"Q040_SYNTHETIC_KNOWN_TRUTH_MANIFEST_v0.1_2026-09-30.json").read_text())
    assert m["sparse_tail_min_qualifying_episodes_per_stratum"] == 10

from __future__ import annotations

import json
import pytest

from market_chi.q039_production_gate_v04 import (
    NC7_RULE_SCHEMA,
    load_nc7_context_rule,
)
from market_chi.q039_source_v04 import PREREG_COMMIT


def test_nc7_rule_requires_frozen_bound_scientific_adjudication(tmp_path):
    p = tmp_path / "nc7.json"
    p.write_text(json.dumps({
        "schema_version": NC7_RULE_SCHEMA,
        "prereg_commit": PREREG_COMMIT,
        "status": "FROZEN",
        "context_rule": "reviewer-prescribed prospective NC7 context construction",
        "adjudication_source": "external APQ return / prospective Plan Delta",
    }))
    r = load_nc7_context_rule(p)
    assert r["status"] == "FROZEN"

    bad = dict(r)
    bad["status"] = "DRAFT"
    p.write_text(json.dumps(bad))
    with pytest.raises(ValueError):
        load_nc7_context_rule(p)


def test_nc7_rule_cannot_float_to_another_preregistration(tmp_path):
    p = tmp_path / "nc7.json"
    p.write_text(json.dumps({
        "schema_version": NC7_RULE_SCHEMA,
        "prereg_commit": "wrong",
        "status": "FROZEN",
        "context_rule": "x",
        "adjudication_source": "y",
    }))
    with pytest.raises(ValueError):
        load_nc7_context_rule(p)

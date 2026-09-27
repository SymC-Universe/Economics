import gzip
import hashlib
import json
from pathlib import Path

from market_chi.microstructure_v2 import validate_feature_gzip
from tools.mnq_development_sweep import verify_cached_features, quarantine


def _write_feature(path: Path) -> None:
    with gzip.open(path, "wt", encoding="utf-8", newline="") as f:
        f.write("bin_start_ns,value\n")
        f.write("1000000000,1\n")
        f.write("2000000000,2\n")


def _sha(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def test_valid_feature_gzip_passes_crc_and_contract(tmp_path):
    p = tmp_path / "features.csv.gz"
    _write_feature(p)
    out = validate_feature_gzip(p)
    assert out["valid"] is True
    assert out["rows"] == 2


def test_truncated_feature_gzip_is_rejected(tmp_path):
    p = tmp_path / "features.csv.gz"
    _write_feature(p)
    data = p.read_bytes()
    p.write_bytes(data[:-8])
    out = validate_feature_gzip(p)
    assert out["valid"] is False
    assert out["rows"] >= 0


def test_cached_feature_hash_mismatch_is_rejected(tmp_path):
    p = tmp_path / "features.csv.gz"
    s = tmp_path / "summary.json"
    _write_feature(p)
    s.write_text(json.dumps({"output_sha256": "0" * 64}), encoding="utf-8")
    out = verify_cached_features(p, s)
    assert out["valid"] is False
    assert out["reason"] == "summary_hash_mismatch"


def test_quarantine_preserves_bad_cache_as_evidence(tmp_path):
    p = tmp_path / "features.csv.gz"
    _write_feature(p)
    target = quarantine(p)
    assert target is not None
    assert not p.exists()
    assert Path(target).exists()
    assert ".corrupt" in Path(target).name

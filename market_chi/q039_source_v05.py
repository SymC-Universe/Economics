from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import csv
import gzip
import hashlib
import json
from pathlib import Path

DATES = ("20260527", "20260528", "20260529", "20260601", "20260602")
FORBIDDEN_DATES = ("20260609", "20260610", "20260611")
PLAN_REVIEWED_COMMIT = "1611705aa2ee75176207387598082d08a8ce56d8"
PLAN_DOCUMENTATION_CLOSURE_COMMIT = "d696bb26637392b6689460c151f77894952b54c1"
RECHECK_ADJUDICATION_COMMIT = "79e039dbea4ae33e73fd0ad7e83d8298e18178e9"
SOURCE_SCHEMA = "q039-v0.5-source-freeze-v1"
SESSION_SECONDS = 21 * 60 * 60
NS = 1_000_000_000


@dataclass(frozen=True)
class SourceSpec:
    date: str
    feature_file: str
    feature_sha256: str
    instrument_id: str
    symbol: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


def sha256_file(path: str | Path, block_size: int = 8 * 1024 * 1024) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(block_size), b""):
            h.update(block)
    return h.hexdigest()


def date_start_ns(date_text: str) -> int:
    dt = datetime.strptime(date_text, "%Y%m%d").replace(tzinfo=timezone.utc)
    return int(dt.timestamp() * NS)


def load_source_manifest(path: str | Path) -> dict[str, SourceSpec]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if raw.get("schema_version") != SOURCE_SCHEMA:
        raise ValueError("wrong Q039 v0.5 source manifest schema")
    if raw.get("reviewed_plan_commit") != PLAN_REVIEWED_COMMIT:
        raise ValueError("reviewed plan binding mismatch")
    if raw.get("documentation_closure_commit") != PLAN_DOCUMENTATION_CLOSURE_COMMIT:
        raise ValueError("documentation closure binding mismatch")
    if raw.get("recheck_adjudication_commit") != RECHECK_ADJUDICATION_COMMIT:
        raise ValueError("recheck adjudication binding mismatch")
    if raw.get("q038_dates_allowed") is not False:
        raise ValueError("source manifest must explicitly prohibit Q038 dates")
    if raw.get("real_outcomes_opened") is not False:
        raise ValueError("source freeze cannot claim real outcomes opened")

    rows = raw.get("sources")
    if not isinstance(rows, list) or len(rows) != len(DATES):
        raise ValueError("source manifest must contain exactly five development sources")

    specs: dict[str, SourceSpec] = {}
    for item in rows:
        spec = SourceSpec(
            date=str(item["date"]),
            feature_file=str(item["feature_file"]),
            feature_sha256=str(item["feature_sha256"]),
            instrument_id=str(item["instrument_id"]),
            symbol=str(item["symbol"]),
        )
        if spec.date in specs:
            raise ValueError("duplicate source date")
        specs[spec.date] = spec

    if tuple(sorted(specs)) != tuple(sorted(DATES)):
        raise ValueError("source dates do not exactly match frozen Q039 development dates")
    if any(d in specs for d in FORBIDDEN_DATES):
        raise ValueError("Q038 holdout date present in Q039 manifest")
    return specs


def verify_source_spec(spec: SourceSpec) -> Path:
    p = Path(spec.feature_file).expanduser().resolve()
    if not p.exists():
        raise FileNotFoundError(str(p))
    if spec.date not in p.name:
        raise ValueError("feature filename does not contain frozen date")
    low = str(p).lower()
    if "q038" in low or "holdout" in low:
        raise ValueError("Q038/holdout path is prohibited")
    if not p.name.endswith(".features.v2.csv.gz"):
        raise ValueError("Q039 requires validated MBP10 v2 feature gzip")
    if sha256_file(p) != spec.feature_sha256:
        raise ValueError("feature SHA-256 does not match frozen source manifest")
    return p


def load_selected_session_rows(spec: SourceSpec) -> list[dict[str, str]]:
    """Load only the frozen 00:00-21:00 UTC segment identity."""
    p = verify_source_spec(spec)
    lo = date_start_ns(spec.date)
    hi = lo + SESSION_SECONDS * NS
    rows: list[dict[str, str]] = []

    with gzip.open(p, "rt", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        required = {
            "bin_start_ns", "instrument_id", "symbol", "valid_book_rows",
            "event_rows", "trade_volume", "signed_trade_volume",
            "spread_last", "microprice_offset_last", "l10_imbalance_last",
        }
        required.update(
            name
            for level in range(10)
            for name in (f"bid_sz_{level:02d}_last", f"ask_sz_{level:02d}_last")
        )
        if reader.fieldnames is None or not required.issubset(set(reader.fieldnames)):
            raise ValueError("feature file is missing required v0.5 fields")

        for row in reader:
            t = int(row["bin_start_ns"])
            if not (lo <= t < hi):
                continue
            if str(row.get("instrument_id", "")).strip() != spec.instrument_id:
                continue
            if str(row.get("symbol", "")).strip() != spec.symbol:
                continue
            rows.append(row)

    rows.sort(key=lambda x: int(x["bin_start_ns"]))
    if not rows:
        raise ValueError("frozen source segment has no rows in 00:00-21:00 UTC")
    return rows

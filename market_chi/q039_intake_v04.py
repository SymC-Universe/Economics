from __future__ import annotations

from dataclasses import dataclass, asdict
import math
from typing import Iterable

import numpy as np

LEVELS = 10
DIM = 20
NS = 1_000_000_000


@dataclass(frozen=True)
class IntakeAudit:
    n_seconds: int
    feature_rows: int
    valid_l10_updates: int
    first_valid_update_index: int | None
    prefirst_state_all_nan: bool
    bad_or_invalid_rows_ignored: int
    carried_seconds: int

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _float(row: dict[str, str], key: str, default: float = math.nan) -> float:
    v = row.get(key)
    if v in (None, ""):
        return default
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def _int(row: dict[str, str], key: str, default: int = 0) -> int:
    v = row.get(key)
    if v in (None, ""):
        return default
    try:
        return int(float(v))
    except (TypeError, ValueError):
        return default


def l10_size_names() -> list[str]:
    return [
        name
        for level in range(LEVELS)
        for name in (f"bid_sz_{level:02d}_last", f"ask_sz_{level:02d}_last")
    ]


def _valid_l10_update(row: dict[str, str]) -> tuple[bool, np.ndarray | None]:
    """Return a new valid L10 state only when the extractor reports one.

    valid_book_rows > 0 is the authoritative one-second update indicator.
    Feature rows with no valid book state are not allowed to overwrite the
    carried state even though last-state fields may contain placeholders.
    """
    if _int(row, "valid_book_rows", 0) <= 0:
        return False, None
    vals = np.asarray([_float(row, k) for k in l10_size_names()], dtype=float)
    if vals.shape != (DIM,) or np.any(~np.isfinite(vals)) or np.any(vals < 0):
        return False, None
    return True, vals


def dense_q039_state(
    rows: Iterable[dict[str, str]],
    start_ns: int,
    end_ns: int,
) -> tuple[dict[str, np.ndarray], IntakeAudit]:
    """Build the frozen Q039 one-second source state.

    Rules:
    - ordinary UTC wall-clock seconds;
    - alternating bid/ask L10 coordinate order;
    - accept a new L10 state only when valid_book_rows > 0 and all 20 sizes are
      finite/nonnegative;
    - invalid/bad rows never overwrite the prior valid state;
    - carry only within the supplied day/session;
    - never backfill before the first valid state;
    - derive l10_update_indicator and staleness_age_s from true valid updates;
    - log1p transform is applied after carry-forward.
    """
    if end_ns <= start_ns:
        raise ValueError("end_ns must exceed start_ns")

    times = np.arange(start_ns, end_ns, NS, dtype=np.int64)
    n = len(times)
    pos = {int(t): i for i, t in enumerate(times)}

    feature_present = np.zeros(n, dtype=bool)
    update = np.zeros(n, dtype=bool)
    raw = np.full((n, DIM), np.nan, dtype=float)

    event_rows = np.zeros(n, dtype=float)
    trade_volume = np.zeros(n, dtype=float)
    signed_trade_volume = np.zeros(n, dtype=float)

    spread = np.full(n, np.nan, dtype=float)
    micro = np.full(n, np.nan, dtype=float)
    l10_imb = np.full(n, np.nan, dtype=float)

    feature_count = 0
    invalid_ignored = 0

    for row in rows:
        try:
            t = int(row["bin_start_ns"])
        except Exception:
            continue
        i = pos.get(t)
        if i is None:
            continue
        feature_count += 1
        feature_present[i] = True

        event_rows[i] += max(0.0, _float(row, "event_rows", 0.0))
        trade_volume[i] += max(0.0, _float(row, "trade_volume", 0.0))
        signed_trade_volume[i] += _float(row, "signed_trade_volume", 0.0)

        ok, vals = _valid_l10_update(row)
        if ok and vals is not None:
            update[i] = True
            raw[i] = vals

            sp = _float(row, "spread_last")
            mp = _float(row, "microprice_offset_last")
            imb = _float(row, "l10_imbalance_last")
            spread[i] = sp if math.isfinite(sp) else math.nan
            micro[i] = mp if math.isfinite(mp) else math.nan
            l10_imb[i] = imb if math.isfinite(imb) else math.nan
        elif _int(row, "valid_book_rows", 0) > 0:
            invalid_ignored += 1

    last_depth: np.ndarray | None = None
    last_spread = math.nan
    last_micro = math.nan
    last_imb = math.nan
    last_update_idx: int | None = None

    carried_seconds = 0
    staleness = np.full(n, np.nan, dtype=float)

    for i in range(n):
        if update[i]:
            last_depth = raw[i].copy()
            last_update_idx = i
            if math.isfinite(spread[i]):
                last_spread = float(spread[i])
            if math.isfinite(micro[i]):
                last_micro = float(micro[i])
            if math.isfinite(l10_imb[i]):
                last_imb = float(l10_imb[i])
            staleness[i] = 0.0
        elif last_depth is not None:
            raw[i] = last_depth
            spread[i] = last_spread
            micro[i] = last_micro
            l10_imb[i] = last_imb
            staleness[i] = float(i - int(last_update_idx))
            carried_seconds += 1

    first_idx = int(np.flatnonzero(update)[0]) if np.any(update) else None
    if first_idx is None:
        prefirst_all_nan = bool(np.all(np.isnan(raw)))
    else:
        prefirst_all_nan = bool(np.all(np.isnan(raw[:first_idx])))

    log_depth = np.log1p(raw)

    out = {
        "times_ns": times,
        "feature_present": feature_present,
        "l10_update_indicator": update.astype(float),
        "staleness_age_s": staleness,
        "depth20_raw": raw,
        "depth20_log1p": log_depth,
        "event_rows": event_rows,
        "trade_volume": trade_volume,
        "signed_trade_volume": signed_trade_volume,
        "spread": spread,
        "microprice_offset": micro,
        "l10_imbalance": l10_imb,
    }

    audit = IntakeAudit(
        n_seconds=n,
        feature_rows=feature_count,
        valid_l10_updates=int(update.sum()),
        first_valid_update_index=first_idx,
        prefirst_state_all_nan=prefirst_all_nan,
        bad_or_invalid_rows_ignored=invalid_ignored,
        carried_seconds=carried_seconds,
    )
    return out, audit


def semantic_state(depth20_log1p: np.ndarray) -> np.ndarray:
    """Raw semantic functionals D and I from alternating bid/ask L10 log depth."""
    x = np.asarray(depth20_log1p, dtype=float)
    if x.ndim != 2 or x.shape[1] != DIM:
        raise ValueError("depth20_log1p must have shape (n,20)")
    sym = np.ones(DIM, dtype=float)
    imb = np.tile(np.asarray([1.0, -1.0]), LEVELS)
    sym /= np.linalg.norm(sym)
    imb /= np.linalg.norm(imb)
    return np.column_stack([x @ sym, x @ imb])

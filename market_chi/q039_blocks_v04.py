from __future__ import annotations

from dataclasses import dataclass, asdict
import math
import numpy as np

from .q039_intake_v04 import DIM, semantic_state

SESSION_SECONDS = 21 * 60 * 60
SCALES = (15, 30, 60, 300)


@dataclass(frozen=True)
class BlockRecord:
    status: str
    scale_seconds: int
    block_index: int
    start_ns: int
    end_ns: int
    valid_state_seconds: int
    depth20_mean: tuple[float, ...] | None
    D: float
    I: float
    log_event_rows: float
    log_trade_volume: float
    signed_log_trade_volume: float
    mean_spread: float
    mean_microprice_offset: float
    mean_l10_imbalance: float
    mean_staleness_age_s: float
    max_staleness_age_s: float
    l10_update_fraction: float

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def signed_log1p(x: float) -> float:
    return math.copysign(math.log1p(abs(float(x))), float(x)) if x != 0 else 0.0


def session_phase_features(block_index: int, scale_seconds: int) -> np.ndarray:
    if scale_seconds not in SCALES:
        raise ValueError("scale outside frozen Q039 hierarchy")
    seconds = block_index * scale_seconds
    phase = seconds / SESSION_SECONDS
    return np.asarray([
        math.sin(2 * math.pi * phase),
        math.cos(2 * math.pi * phase),
        math.sin(4 * math.pi * phase),
        math.cos(4 * math.pi * phase),
    ], dtype=float)


def _finite_mean(x: np.ndarray) -> float:
    v = np.asarray(x, dtype=float)
    v = v[np.isfinite(v)]
    return float(v.mean()) if len(v) else math.nan


def _finite_max(x: np.ndarray) -> float:
    v = np.asarray(x, dtype=float)
    v = v[np.isfinite(v)]
    return float(v.max()) if len(v) else math.nan


def build_scale_blocks(
    dense: dict[str, np.ndarray],
    *,
    scale_seconds: int,
    session_start_ns: int,
) -> list[BlockRecord]:
    if scale_seconds not in SCALES:
        raise ValueError("scale outside frozen Q039 hierarchy")
    if SESSION_SECONDS % scale_seconds:
        raise ValueError("scale must divide 21-hour session")

    required = (
        "times_ns", "depth20_log1p", "event_rows", "trade_volume",
        "signed_trade_volume", "spread", "microprice_offset",
        "l10_imbalance", "staleness_age_s", "l10_update_indicator",
    )
    missing = [k for k in required if k not in dense]
    if missing:
        raise ValueError("missing dense fields: " + ",".join(missing))

    t = np.asarray(dense["times_ns"], dtype=np.int64)
    if len(t) != SESSION_SECONDS:
        raise ValueError("dense state must contain exactly 21 hours of one-second samples")
    expected = session_start_ns + np.arange(SESSION_SECONDS, dtype=np.int64) * 1_000_000_000
    if not np.array_equal(t, expected):
        raise ValueError("dense state is not the frozen literal one-second wall-clock grid")

    x = np.asarray(dense["depth20_log1p"], dtype=float)
    if x.shape != (SESSION_SECONDS, DIM):
        raise ValueError("depth20_log1p shape mismatch")

    sem = semantic_state(x)
    n_blocks = SESSION_SECONDS // scale_seconds
    out: list[BlockRecord] = []

    for b in range(n_blocks):
        lo = b * scale_seconds
        hi = lo + scale_seconds
        state_mask = np.all(np.isfinite(x[lo:hi]), axis=1)
        valid_n = int(state_mask.sum())
        start_ns = int(t[lo])
        end_ns = int(t[hi - 1] + 1_000_000_000)

        event_sum = float(np.nansum(np.asarray(dense["event_rows"][lo:hi], dtype=float)))
        vol_sum = float(np.nansum(np.asarray(dense["trade_volume"][lo:hi], dtype=float)))
        signed_sum = float(np.nansum(np.asarray(dense["signed_trade_volume"][lo:hi], dtype=float)))
        update_fraction = float(np.mean(np.asarray(dense["l10_update_indicator"][lo:hi], dtype=float)))

        if valid_n == 0:
            out.append(BlockRecord(
                "REFUSED_NO_VALID_STATE_YET",
                scale_seconds, b, start_ns, end_ns, 0, None,
                math.nan, math.nan,
                math.log1p(max(0.0, event_sum)),
                math.log1p(max(0.0, vol_sum)),
                signed_log1p(signed_sum),
                math.nan, math.nan, math.nan,
                math.nan, math.nan, update_fraction,
            ))
            continue

        depth_mean = np.mean(x[lo:hi][state_mask], axis=0)
        di = np.mean(sem[lo:hi][state_mask], axis=0)

        out.append(BlockRecord(
            "COMPLETE",
            scale_seconds, b, start_ns, end_ns, valid_n,
            tuple(float(v) for v in depth_mean),
            float(di[0]), float(di[1]),
            math.log1p(max(0.0, event_sum)),
            math.log1p(max(0.0, vol_sum)),
            signed_log1p(signed_sum),
            _finite_mean(np.asarray(dense["spread"][lo:hi], dtype=float)),
            _finite_mean(np.asarray(dense["microprice_offset"][lo:hi], dtype=float)),
            _finite_mean(np.asarray(dense["l10_imbalance"][lo:hi], dtype=float)),
            _finite_mean(np.asarray(dense["staleness_age_s"][lo:hi], dtype=float)),
            _finite_max(np.asarray(dense["staleness_age_s"][lo:hi], dtype=float)),
            update_fraction,
        ))
    return out


def block_map(blocks: list[BlockRecord]) -> dict[int, BlockRecord]:
    return {b.block_index: b for b in blocks if b.status == "COMPLETE"}


def coarse_native_N(
    current: BlockRecord,
    previous: BlockRecord,
) -> np.ndarray:
    if current.status != "COMPLETE" or previous.status != "COMPLETE":
        raise ValueError("N requires complete current and previous blocks")
    phase = session_phase_features(current.block_index, current.scale_seconds)
    vals = np.asarray([
        current.D, current.I,
        previous.D, previous.I,
        *phase,
        current.log_event_rows,
        current.log_trade_volume,
        current.signed_log_trade_volume,
        current.mean_spread,
        current.mean_microprice_offset,
        current.mean_l10_imbalance,
        current.mean_staleness_age_s,
        current.max_staleness_age_s,
        current.l10_update_fraction,
    ], dtype=float)
    if not np.all(np.isfinite(vals)):
        raise ValueError("N contains non-finite predictor")
    return vals


def child_slope(values: np.ndarray) -> np.ndarray:
    a = np.asarray(values, dtype=float)
    if a.ndim == 1:
        a = a[:, None]
    n = len(a)
    if n < 2:
        raise ValueError("slope requires at least two children")
    tt = np.arange(n, dtype=float)
    tt -= tt.mean()
    denom = float(np.sum(tt * tt))
    centered = a - a.mean(axis=0, keepdims=True)
    return np.sum(centered * tt[:, None], axis=0) / denom


def factor2_models(
    coarse_current: BlockRecord,
    coarse_previous: BlockRecord,
    children: list[BlockRecord],
) -> tuple[np.ndarray, np.ndarray]:
    if len(children) != 2 or any(x.status != "COMPLETE" for x in children):
        raise ValueError("factor2 requires two complete fine children")
    N = coarse_native_N(coarse_current, coarse_previous)
    c1, c2 = children
    A2 = np.concatenate([
        N,
        np.asarray([
            c2.log_event_rows,
            c2.log_event_rows - c1.log_event_rows,
            c2.l10_update_fraction,
            c2.l10_update_fraction - c1.l10_update_fraction,
            c2.signed_log_trade_volume - c1.signed_log_trade_volume,
        ], dtype=float),
    ])
    F2 = np.concatenate([
        A2,
        np.asarray([c2.D - c1.D, c2.I - c1.I], dtype=float),
    ])
    return A2, F2


def factor5_models(
    coarse_current: BlockRecord,
    coarse_previous: BlockRecord,
    children: list[BlockRecord],
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    if len(children) != 5 or any(x.status != "COMPLETE" for x in children):
        raise ValueError("factor5 requires five complete fine children")
    N = coarse_native_N(coarse_current, coarse_previous)

    ev = np.asarray([x.log_event_rows for x in children], dtype=float)
    up = np.asarray([x.l10_update_fraction for x in children], dtype=float)
    sem = np.asarray([[x.D, x.I] for x in children], dtype=float)

    A = np.concatenate([
        N,
        np.asarray([
            ev[-1], float(np.std(ev, ddof=0)), float(child_slope(ev)[0]),
            up[-1], float(np.std(up, ddof=0)), float(child_slope(up)[0]),
        ], dtype=float),
    ])
    L = np.concatenate([A, sem[-1]])
    U = np.concatenate([L, np.std(sem, axis=0, ddof=0)])
    S = np.concatenate([U, child_slope(sem)])
    return A, L, U, S

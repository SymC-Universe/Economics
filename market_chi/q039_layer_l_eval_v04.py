from __future__ import annotations

from dataclasses import dataclass, asdict
import math
from typing import Sequence

import numpy as np

from .q039_blocks_v04 import (
    BlockRecord,
    block_map,
    factor2_models,
    factor5_models,
)

SESSION_SECONDS = 21 * 60 * 60
INITIAL_TRAIN_SECONDS = 5 * 60 * 60
REFIT_SECONDS = 60 * 60
CONDITION_LIMIT = 1e8
BOOTSTRAP_SEED = 20260929
PRIMARY_CI = 0.98333


@dataclass(frozen=True)
class RefitDiagnostic:
    chunk_start_ns: int
    chunk_end_ns: int
    n_train: int
    p_small: int
    p_large: int
    rank_small: int
    rank_large: int
    condition_small: float
    condition_large: float
    status: str
    reason: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class DayNestedSummary:
    status: str
    small_name: str
    large_name: str
    fine_seconds: int
    coarse_seconds: int
    p_max: int
    n_observations: int
    n_primary_predictions: int
    valid_oos_hours: int
    point_contrast: float
    clark_west_point: float
    mae_small_d: float
    mae_large_d: float
    mae_small_i: float
    mae_large_i: float
    r2_small_d: float
    r2_large_d: float
    r2_small_i: float
    r2_large_i: float
    excluded_refit_utc_hours: tuple[int, ...]
    reason: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _r2(y: np.ndarray, pred: np.ndarray) -> float:
    yy = np.asarray(y, dtype=float)
    pp = np.asarray(pred, dtype=float)
    ss_res = float(np.sum((yy - pp) ** 2))
    ss_tot = float(np.sum((yy - yy.mean()) ** 2))
    return math.nan if ss_tot <= 0 else 1.0 - ss_res / ss_tot


def _standardize_frozen(
    train_x: np.ndarray,
    test_x: np.ndarray,
    *,
    cyclic_columns: Sequence[int],
) -> tuple[np.ndarray, np.ndarray] | None:
    tr = np.asarray(train_x, dtype=float).copy()
    te = np.asarray(test_x, dtype=float).copy()
    if tr.ndim != 2 or te.ndim != 2 or tr.shape[1] != te.shape[1]:
        raise ValueError("predictor shape mismatch")
    if np.any(~np.isfinite(tr)) or np.any(~np.isfinite(te)):
        return None

    cyc = set(int(i) for i in cyclic_columns)
    for j in range(tr.shape[1]):
        if j in cyc:
            continue
        mu = float(np.mean(tr[:, j]))
        sd = float(np.std(tr[:, j], ddof=0))
        if not math.isfinite(sd) or sd <= 1e-12:
            return None
        tr[:, j] = (tr[:, j] - mu) / sd
        te[:, j] = (te[:, j] - mu) / sd
    return tr, te


def _fit_one(
    train_x: np.ndarray,
    train_y: np.ndarray,
    test_x: np.ndarray,
    *,
    cyclic_columns: Sequence[int],
) -> tuple[np.ndarray | None, dict[str, object]]:
    scaled = _standardize_frozen(
        train_x, test_x, cyclic_columns=cyclic_columns
    )
    p = int(train_x.shape[1] + 1)
    if scaled is None:
        return None, {
            "status": "REFUSED_SCALING",
            "rank": 0,
            "p": p,
            "condition": math.inf,
        }

    tr, te = scaled
    X = np.column_stack([np.ones(len(tr)), tr])
    Xt = np.column_stack([np.ones(len(te)), te])
    rank = int(np.linalg.matrix_rank(X))
    cond = float(np.linalg.cond(X))

    if rank < p:
        return None, {
            "status": "RANK_DEFICIENT",
            "rank": rank,
            "p": p,
            "condition": cond,
        }

    beta, *_ = np.linalg.lstsq(X, train_y, rcond=None)
    pred = Xt @ beta
    status = "NUMERICALLY_ILL_CONDITIONED" if cond > CONDITION_LIMIT else "OK"
    return pred, {
        "status": status,
        "rank": rank,
        "p": p,
        "condition": cond,
    }


def build_pair_observations(
    fine_blocks: list[BlockRecord],
    coarse_blocks: list[BlockRecord],
    *,
    fine_seconds: int,
    coarse_seconds: int,
) -> dict[str, np.ndarray]:
    if coarse_seconds % fine_seconds:
        raise ValueError("coarse_seconds must be an integer multiple of fine_seconds")
    factor = coarse_seconds // fine_seconds
    if factor not in (2, 5):
        raise ValueError("Q039 supports only frozen factor-2 and factor-5 pairs")

    fmap = block_map(fine_blocks)
    cmap = block_map(coarse_blocks)

    source_block = []
    source_start_ns = []
    target_end_ns = []
    y = []
    model_data: dict[str, list[np.ndarray]] = {}

    names = ("A2", "F2") if factor == 2 else ("A", "L", "U", "S")
    for name in names:
        model_data[name] = []

    for cb in sorted(cmap):
        if cb - 1 not in cmap or cb + 1 not in cmap:
            continue
        child_ids = [cb * factor + k for k in range(factor)]
        if any(k not in fmap for k in child_ids):
            continue

        cur = cmap[cb]
        prev = cmap[cb - 1]
        target = cmap[cb + 1]
        children = [fmap[k] for k in child_ids]

        if factor == 2:
            A2, F2 = factor2_models(cur, prev, children)
            model_data["A2"].append(A2)
            model_data["F2"].append(F2)
        else:
            A, L, U, S = factor5_models(cur, prev, children)
            model_data["A"].append(A)
            model_data["L"].append(L)
            model_data["U"].append(U)
            model_data["S"].append(S)

        source_block.append(cb)
        source_start_ns.append(cur.start_ns)
        target_end_ns.append(target.end_ns)
        y.append([target.D, target.I])

    out: dict[str, np.ndarray] = {
        "source_block": np.asarray(source_block, dtype=int),
        "source_start_ns": np.asarray(source_start_ns, dtype=np.int64),
        "target_end_ns": np.asarray(target_end_ns, dtype=np.int64),
        "y": np.asarray(y, dtype=float),
    }
    for name, values in model_data.items():
        out[name] = np.asarray(values, dtype=float)
    return out


def evaluate_nested_day(
    obs: dict[str, np.ndarray],
    *,
    small_name: str,
    large_name: str,
    fine_seconds: int,
    coarse_seconds: int,
    day_start_ns: int,
    cyclic_columns: Sequence[int] = (4, 5, 6, 7),
) -> tuple[DayNestedSummary, dict[str, np.ndarray | list[dict[str, object]]]]:
    small_x = np.asarray(obs[small_name], dtype=float)
    large_x = np.asarray(obs[large_name], dtype=float)
    y = np.asarray(obs["y"], dtype=float)
    source_start = np.asarray(obs["source_start_ns"], dtype=np.int64)
    target_end = np.asarray(obs["target_end_ns"], dtype=np.int64)
    source_block = np.asarray(obs["source_block"], dtype=int)

    n = len(y)
    if not (len(small_x) == len(large_x) == len(source_start) == len(target_end) == n):
        raise ValueError("observation length mismatch")
    if n == 0:
        summary = DayNestedSummary(
            "INVALID_TEST_INSUFFICIENT_IDENTIFICATION",
            small_name, large_name, fine_seconds, coarse_seconds,
            max(small_x.shape[1] if small_x.ndim == 2 else 0,
                large_x.shape[1] if large_x.ndim == 2 else 0) + 1,
            0, 0, 0,
            math.nan, math.nan,
            math.nan, math.nan, math.nan, math.nan,
            math.nan, math.nan, math.nan, math.nan,
            (), "no complete lagged observations",
        )
        return summary, {}

    p_max = int(max(small_x.shape[1], large_x.shape[1]) + 1)
    pred_small = np.full_like(y, np.nan)
    pred_large = np.full_like(y, np.nan)
    raw_delta = np.full(n, np.nan)
    cw_delta = np.full(n, np.nan)
    primary_mask = np.zeros(n, dtype=bool)
    descriptive_mask = np.zeros(n, dtype=bool)
    diagnostics: list[RefitDiagnostic] = []
    valid_hours = 0
    excluded_hours: list[int] = []

    first_hour_ns = day_start_ns + INITIAL_TRAIN_SECONDS * 1_000_000_000
    session_end_ns = day_start_ns + SESSION_SECONDS * 1_000_000_000
    hour_ns = REFIT_SECONDS * 1_000_000_000

    chunk_start = first_hour_ns
    while chunk_start < session_end_ns:
        chunk_end = min(session_end_ns, chunk_start + hour_ns)
        test_mask = (source_start >= chunk_start) & (source_start < chunk_end)
        if not np.any(test_mask):
            chunk_start = chunk_end
            continue

        first_test_source = int(np.min(source_start[test_mask]))
        train_mask = target_end <= first_test_source
        n_train = int(np.sum(train_mask))

        if n_train < 5 * p_max:
            diagnostics.append(RefitDiagnostic(
                int(chunk_start), int(chunk_end), n_train,
                small_x.shape[1] + 1, large_x.shape[1] + 1,
                0, 0, math.inf, math.inf,
                "REFUSED_N_OVER_P",
                f"n_train={n_train} < 5*p_max={5*p_max}",
            ))
            chunk_start = chunk_end
            continue

        train_y = y[train_mask]
        target_sd = np.std(train_y, axis=0, ddof=0)
        if np.any(~np.isfinite(target_sd)) or np.any(target_sd <= 1e-12):
            diagnostics.append(RefitDiagnostic(
                int(chunk_start), int(chunk_end), n_train,
                small_x.shape[1] + 1, large_x.shape[1] + 1,
                0, 0, math.inf, math.inf,
                "REFUSED_TARGET_SCALING",
                "training target SD is non-finite or zero",
            ))
            chunk_start = chunk_end
            continue

        ps, ds = _fit_one(
            small_x[train_mask], train_y, small_x[test_mask],
            cyclic_columns=cyclic_columns,
        )
        pl, dl = _fit_one(
            large_x[train_mask], train_y, large_x[test_mask],
            cyclic_columns=cyclic_columns,
        )

        if ps is None or pl is None:
            status = "REFUSED_REFIT"
            reason = f"{ds['status']} / {dl['status']}"
            diagnostics.append(RefitDiagnostic(
                int(chunk_start), int(chunk_end), n_train,
                int(ds["p"]), int(dl["p"]),
                int(ds["rank"]), int(dl["rank"]),
                float(ds["condition"]), float(dl["condition"]),
                status, reason,
            ))
            chunk_start = chunk_end
            continue

        idx = np.flatnonzero(test_mask)
        pred_small[idx] = ps
        pred_large[idx] = pl
        descriptive_mask[idx] = True

        yy = y[idx]
        es = (yy - ps) / target_sd
        el = (yy - pl) / target_sd
        raw = 0.5 * np.sum(es * es - el * el, axis=1)
        pdiff = (pl - ps) / target_sd
        cw = raw + 0.5 * np.sum(pdiff * pdiff, axis=1)
        raw_delta[idx] = raw
        cw_delta[idx] = cw

        ill = (
            ds["status"] == "NUMERICALLY_ILL_CONDITIONED"
            or dl["status"] == "NUMERICALLY_ILL_CONDITIONED"
        )
        if ill:
            utc_hour = int(((chunk_start - day_start_ns) // hour_ns) % 24)
            excluded_hours.append(utc_hour)
            status = "NUMERICALLY_ILL_CONDITIONED"
            reason = "predictions retained descriptively; excluded from primary"
        else:
            primary_mask[idx] = True
            valid_hours += 1
            status = "OK"
            reason = "primary-eligible refit"

        diagnostics.append(RefitDiagnostic(
            int(chunk_start), int(chunk_end), n_train,
            int(ds["p"]), int(dl["p"]),
            int(ds["rank"]), int(dl["rank"]),
            float(ds["condition"]), float(dl["condition"]),
            status, reason,
        ))
        chunk_start = chunk_end

    if valid_hours < 8 or int(np.sum(primary_mask)) == 0:
        summary = DayNestedSummary(
            "INVALID_TEST_INSUFFICIENT_IDENTIFICATION",
            small_name, large_name, fine_seconds, coarse_seconds,
            p_max, n, int(np.sum(primary_mask)), valid_hours,
            math.nan, math.nan,
            math.nan, math.nan, math.nan, math.nan,
            math.nan, math.nan, math.nan, math.nan,
            tuple(excluded_hours),
            "fewer than 8 valid wall-clock OOS hours remain after frozen refit refusals",
        )
        return summary, {
            "source_block": source_block,
            "primary_mask": primary_mask,
            "descriptive_mask": descriptive_mask,
            "raw_delta": raw_delta,
            "clark_west_delta": cw_delta,
            "pred_small": pred_small,
            "pred_large": pred_large,
            "refits": [d.to_dict() for d in diagnostics],
        }

    mask = primary_mask
    yy = y[mask]
    ps = pred_small[mask]
    pl = pred_large[mask]
    mae_s = np.mean(np.abs(yy - ps), axis=0)
    mae_l = np.mean(np.abs(yy - pl), axis=0)

    summary = DayNestedSummary(
        "COMPLETE",
        small_name, large_name, fine_seconds, coarse_seconds,
        p_max, n, int(np.sum(mask)), valid_hours,
        float(np.mean(raw_delta[mask])),
        float(np.mean(cw_delta[mask])),
        float(mae_s[0]), float(mae_l[0]),
        float(mae_s[1]), float(mae_l[1]),
        _r2(yy[:, 0], ps[:, 0]), _r2(yy[:, 0], pl[:, 0]),
        _r2(yy[:, 1], ps[:, 1]), _r2(yy[:, 1], pl[:, 1]),
        tuple(excluded_hours),
        "frozen Q039 v0.4 walk-forward nested comparison",
    )
    return summary, {
        "source_block": source_block,
        "source_start_ns": source_start,
        "target_end_ns": target_end,
        "primary_mask": primary_mask,
        "descriptive_mask": descriptive_mask,
        "raw_delta": raw_delta,
        "clark_west_delta": cw_delta,
        "pred_small": pred_small,
        "pred_large": pred_large,
        "y": y,
        "refits": [d.to_dict() for d in diagnostics],
    }


def _contiguous_block_starts(block_ids: np.ndarray, block_len: int) -> np.ndarray:
    ids = np.asarray(block_ids, dtype=int)
    if block_len < 1 or len(ids) < block_len:
        return np.empty(0, dtype=int)
    starts = []
    expected = np.arange(block_len, dtype=int)
    for s in range(len(ids) - block_len + 1):
        if np.array_equal(ids[s:s + block_len], ids[s] + expected):
            starts.append(s)
    return np.asarray(starts, dtype=int)


def _resample_day_non_circular(
    values: np.ndarray,
    block_ids: np.ndarray,
    *,
    block_len: int,
    rng: np.random.Generator,
) -> np.ndarray:
    v = np.asarray(values, dtype=float)
    ids = np.asarray(block_ids, dtype=int)
    if len(v) != len(ids):
        raise ValueError("values/block_ids length mismatch")
    starts = _contiguous_block_starts(ids, block_len)
    if len(starts) == 0:
        raise ValueError("no valid contiguous bootstrap block starts")
    chunks = []
    total = 0
    while total < len(v):
        s = int(starts[int(rng.integers(0, len(starts)))])
        chunks.append(v[s:s + block_len])
        total += block_len
    return np.concatenate(chunks)[:len(v)]


def equal_day_noncircular_bootstrap(
    values_by_day: Sequence[np.ndarray],
    block_ids_by_day: Sequence[np.ndarray],
    *,
    coarse_seconds: int,
    block_seconds: int = 3600,
    reps: int = 10_000,
    seed: int = BOOTSTRAP_SEED,
    ci_level: float = PRIMARY_CI,
) -> dict[str, object]:
    if len(values_by_day) != len(block_ids_by_day) or not values_by_day:
        raise ValueError("day array mismatch")
    if block_seconds % coarse_seconds:
        raise ValueError("bootstrap block must be integer coarse blocks")
    block_len = block_seconds // coarse_seconds

    arrays = []
    ids_list = []
    for v, ids in zip(values_by_day, block_ids_by_day):
        a = np.asarray(v, dtype=float)
        b = np.asarray(ids, dtype=int)
        mask = np.isfinite(a)
        a = a[mask]
        b = b[mask]
        if len(a) == 0:
            raise ValueError("empty day")
        if len(_contiguous_block_starts(b, block_len)) == 0:
            raise ValueError("day has no valid contiguous bootstrap block")
        arrays.append(a)
        ids_list.append(b)

    point = float(np.mean([a.mean() for a in arrays]))
    rng = np.random.default_rng(seed)
    vals = np.empty(reps, dtype=float)

    for r in range(reps):
        day_means = []
        for a, b in zip(arrays, ids_list):
            rs = _resample_day_non_circular(
                a, b, block_len=block_len, rng=rng
            )
            day_means.append(float(np.mean(rs)))
        vals[r] = float(np.mean(day_means))

    alpha = 1.0 - ci_level
    lo, hi = np.quantile(vals, [alpha / 2.0, 1.0 - alpha / 2.0])
    return {
        "point": point,
        "lower": float(lo),
        "upper": float(hi),
        "ci_level": ci_level,
        "reps": reps,
        "seed": seed,
        "block_seconds": block_seconds,
        "block_length_observations": block_len,
        "equal_day_weighting": True,
        "circular": False,
    }

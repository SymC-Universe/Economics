from __future__ import annotations

import argparse
import csv
import gzip
import json
import math
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from market_chi.engine import EngineConfig, analyze_series

LEVELS = 10
NS = 1_000_000_000


def iso_to_ns(text: str) -> int:
    t = text.strip().replace('Z', '+00:00')
    dt = datetime.fromisoformat(t)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return int(dt.timestamp() * NS)


def rankdata_average(x: np.ndarray) -> np.ndarray:
    order = np.argsort(x, kind='mergesort')
    ranks = np.empty(len(x), dtype=float)
    sx = x[order]
    i = 0
    while i < len(x):
        j = i + 1
        while j < len(x) and sx[j] == sx[i]:
            j += 1
        rank = 0.5 * ((i + 1) + j)
        ranks[order[i:j]] = rank
        i = j
    return ranks


def spearman(x: np.ndarray, y: np.ndarray) -> float:
    mask = np.isfinite(x) & np.isfinite(y)
    if mask.sum() < 3:
        return math.nan
    rx = rankdata_average(x[mask])
    ry = rankdata_average(y[mask])
    if np.std(rx) == 0 or np.std(ry) == 0:
        return math.nan
    return float(np.corrcoef(rx, ry)[0, 1])


def load_rows(path: Path, start_ns: int, end_ns: int) -> list[dict[str, str]]:
    opener = gzip.open if path.suffix.lower() == '.gz' else open
    out: list[dict[str, str]] = []
    with opener(path, 'rt', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            t = int(row['bin_start_ns'])
            if start_ns <= t < end_ns:
                out.append(row)
    out.sort(key=lambda r: int(r['bin_start_ns']))
    return out


def f(row: dict[str, str], key: str) -> float:
    v = row.get(key, '')
    return float(v) if v not in ('', None) else math.nan


def dense_state(rows: list[dict[str, str]], start_ns: int, end_ns: int) -> dict[str, np.ndarray]:
    times = np.arange(start_ns, end_ns, NS, dtype=np.int64)
    n = len(times)
    pos = {int(t): i for i, t in enumerate(times)}
    state_names = ['mid_last', 'spread_last', 'l1_imbalance_last', 'l10_imbalance_last']
    size_names = [name for level in range(LEVELS) for name in (f'bid_sz_{level:02d}_last', f'ask_sz_{level:02d}_last')]
    arrays = {name: np.full(n, np.nan) for name in state_names + size_names}
    event_rows = np.zeros(n)
    trade_volume = np.zeros(n)
    signed_trade_volume = np.zeros(n)
    present = np.zeros(n, dtype=bool)
    for row in rows:
        i = pos.get(int(row['bin_start_ns']))
        if i is None:
            continue
        present[i] = True
        for name in arrays:
            arrays[name][i] = f(row, name)
        event_rows[i] = f(row, 'event_rows')
        trade_volume[i] = f(row, 'trade_volume')
        signed_trade_volume[i] = f(row, 'signed_trade_volume')
    for name, x in arrays.items():
        last = math.nan
        for i in range(n):
            if math.isfinite(x[i]):
                last = x[i]
            elif math.isfinite(last):
                x[i] = last
    return {
        'times': times,
        'present': present,
        'event_rows': event_rows,
        'trade_volume': trade_volume,
        'signed_trade_volume': signed_trade_volume,
        **arrays,
    }


def pca_depth(d: dict[str, np.ndarray]) -> tuple[np.ndarray, np.ndarray, np.ndarray, list[str]]:
    names = [name for level in range(LEVELS) for name in (f'bid_sz_{level:02d}_last', f'ask_sz_{level:02d}_last')]
    X = np.column_stack([d[name] for name in names])
    X = np.log1p(X)
    mu = X.mean(axis=0)
    sd = X.std(axis=0)
    if np.any(sd <= 0):
        raise ValueError('constant depth column in selected interval')
    Z = (X - mu) / sd
    _, s, vt = np.linalg.svd(Z, full_matrices=False)
    ratio = s * s
    ratio = ratio / ratio.sum()
    scores = Z @ vt.T
    return ratio, vt, scores, names


def basis_alignment(vt: np.ndarray) -> list[dict[str, float]]:
    sym = np.ones(20)
    imbalance = np.array([1.0, -1.0] * 10)
    level = np.repeat(np.linspace(-1.0, 1.0, 10), 2)
    skew = level * imbalance
    bases = {'symmetric_depth': sym, 'bid_ask_imbalance': imbalance, 'depth_gradient': level, 'side_gradient': skew}
    bases = {k: v / np.linalg.norm(v) for k, v in bases.items()}
    out = []
    for i in range(min(6, len(vt))):
        v = vt[i] / np.linalg.norm(vt[i])
        row = {'pc': i + 1}
        for k, b in bases.items():
            row[k] = float(abs(v @ b))
        out.append(row)
    return out


def half_subspace_stability(d: dict[str, np.ndarray], names: list[str], k: int = 2) -> dict[str, object]:
    n = len(d['times'])
    mats = []
    ratios = []
    for sl in (slice(0, n // 2), slice(n // 2, n)):
        X = np.column_stack([d[name][sl] for name in names])
        X = np.log1p(X)
        Z = (X - X.mean(axis=0)) / X.std(axis=0)
        _, s, vt = np.linalg.svd(Z, full_matrices=False)
        r = s * s
        ratios.append((r / r.sum())[:6].tolist())
        mats.append(vt)
    sv = np.linalg.svd(mats[0][:k] @ mats[1][:k].T, compute_uv=False)
    return {
        'first_half_variance_ratio': ratios[0],
        'second_half_variance_ratio': ratios[1],
        'top2_principal_cosines': [float(x) for x in sv],
        'top2_min_principal_cosine': float(sv.min()),
    }


def chi_screen(series: dict[str, np.ndarray], steps: list[int]) -> list[dict[str, object]]:
    rows = []
    for step in steps:
        for name, x in series.items():
            xx = np.asarray(x[::step], dtype=float)
            result = analyze_series(xx, EngineConfig(dt=float(step), min_points=100, min_ar2_bic_gain=6.0, standardize=True))
            rows.append({
                'series': name,
                'sample_interval_s': step,
                'n': int(len(xx)),
                'status': result.status,
                'chi_status': result.chi_status,
                'chi': None if not math.isfinite(result.chi) else float(result.chi),
                'chi_regime': result.chi_regime,
                'model_family': result.model_family,
                'ar2_bic_gain_vs_best_simple': None if not math.isfinite(result.ar2_bic_gain_vs_best_simple) else float(result.ar2_bic_gain_vs_best_simple),
                'discrete_poles': [{'real': float(z.real), 'imag': float(z.imag)} for z in result.discrete_poles],
                'reason': result.reason,
            })
    return rows


def forward_risk_correlations(d: dict[str, np.ndarray], scores: np.ndarray) -> list[dict[str, object]]:
    bid = np.column_stack([d[f'bid_sz_{i:02d}_last'] for i in range(LEVELS)])
    ask = np.column_stack([d[f'ask_sz_{i:02d}_last'] for i in range(LEVELS)])
    bid_depth = bid.sum(axis=1)
    ask_depth = ask.sum(axis=1)
    total_depth = bid_depth + ask_depth
    depth_imbalance = (bid_depth - ask_depth) / np.maximum(total_depth, 1.0)
    predictors = {
        'l1_imbalance': d['l1_imbalance_last'],
        'l10_imbalance': d['l10_imbalance_last'],
        'total_depth': total_depth,
        'depth_imbalance': depth_imbalance,
        'spread': d['spread_last'],
        'signed_trade_volume': d['signed_trade_volume'],
        'depth_pc1': scores[:, 0],
        'depth_pc2': scores[:, 1],
        'depth_pc3': scores[:, 2],
    }
    mid = d['mid_last']
    one_step = np.diff(mid, prepend=mid[0])
    out = []
    for h in (1, 5, 10, 30, 60):
        change = np.full(len(mid), np.nan)
        change[:-h] = mid[h:] - mid[:-h]
        rv = np.full(len(mid), np.nan)
        sq = one_step * one_step
        for i in range(len(mid) - h):
            rv[i] = math.sqrt(float(sq[i + 1:i + h + 1].sum()))
        for name, x in predictors.items():
            out.append({
                'predictor': name,
                'horizon_s': h,
                'spearman_forward_change': spearman(x, change),
                'spearman_forward_risk': spearman(x, rv),
                'n': int(np.isfinite(x[:-h]).sum()),
            })
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('features')
    ap.add_argument('--start', required=True)
    ap.add_argument('--end', required=True)
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    src = Path(args.features)
    start_ns, end_ns = iso_to_ns(args.start), iso_to_ns(args.end)
    rows = load_rows(src, start_ns, end_ns)
    d = dense_state(rows, start_ns, end_ns)
    if not np.all(np.isfinite(d['mid_last'])):
        raise ValueError('selected interval must begin with an observed valid book state')
    ratio, vt, scores, names = pca_depth(d)
    bid = np.column_stack([d[f'bid_sz_{i:02d}_last'] for i in range(LEVELS)])
    ask = np.column_stack([d[f'ask_sz_{i:02d}_last'] for i in range(LEVELS)])
    total_depth = bid.sum(axis=1) + ask.sum(axis=1)
    depth_imbalance = (bid.sum(axis=1) - ask.sum(axis=1)) / np.maximum(total_depth, 1.0)
    series = {
        'log_total_depth': np.log1p(total_depth),
        'depth_imbalance': depth_imbalance,
        'spread': d['spread_last'],
        'depth_pc1': scores[:, 0],
        'depth_pc2': scores[:, 1],
        'depth_pc3': scores[:, 2],
    }
    result = {
        'schema_version': 'mnq-modal-discovery-v1',
        'source_file': str(src),
        'interval_start': args.start,
        'interval_end_exclusive': args.end,
        'dense_seconds': int(len(d['times'])),
        'observed_event_seconds': int(d['present'].sum()),
        'carried_forward_seconds': int((~d['present']).sum()),
        'coverage_fraction': float(d['present'].mean()),
        'depth_pca_variance_ratio_first10': [float(x) for x in ratio[:10]],
        'depth_pca_cumulative_first10': [float(x) for x in np.cumsum(ratio[:10])],
        'basis_alignment': basis_alignment(vt),
        'mode_semantic_correlations': {
            'pc1_vs_total_depth_spearman': spearman(scores[:, 0], total_depth),
            'pc2_vs_depth_imbalance_spearman': spearman(scores[:, 1], depth_imbalance),
        },
        'half_stability': half_subspace_stability(d, names, k=2),
        'chi_screen': chi_screen(series, [1, 2, 5, 10, 15, 30, 60]),
        'exploratory_forward_associations': forward_risk_correlations(d, scores),
        'epistemic_status': {
            'modal_structure': 'P0-D discovery',
            'chi': 'P0-Q screening only; refusal is a valid result',
            'forward_associations': 'P0-D exploratory; no iid p-values and no predictive claim',
        },
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps({
        'out': str(out),
        'dense_seconds': result['dense_seconds'],
        'coverage_fraction': result['coverage_fraction'],
        'pc1_variance': result['depth_pca_variance_ratio_first10'][0],
        'pc2_variance': result['depth_pca_variance_ratio_first10'][1],
        'top2_min_principal_cosine': result['half_stability']['top2_min_principal_cosine'],
        'chi_admissions': sum(1 for r in result['chi_screen'] if r['chi_status'] == 'ADMITTED'),
    }, indent=2))


if __name__ == '__main__':
    main()

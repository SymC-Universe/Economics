#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

import numpy as np

from market_chi.q040_estimator_stage1_v01 import (
    BASELINE_CANDIDATES,
    BaselineCandidateScore,
    baseline_error,
    baseline_rank_key,
    horizon_qualification,
    metric_rank_key,
    rank_event_tuples,
)
from market_chi.q040_observation_episode_v01 import (
    SCALES,
    build_observation_episode_world,
    nc20_cells,
)


def seed_for(*parts: int) -> int:
    return int(np.random.SeedSequence([20261001, *parts]).generate_state(1, dtype=np.uint32)[0])


def baseline_worlds():
    worlds = []
    for ci, control in enumerate(("NC-R5", "NC-R15", "NC-R16"), start=1):
        for scale in SCALES:
            worlds.append(build_observation_episode_world(
                control, seed=seed_for(1, ci, scale), scale_seconds=scale
            ))
    for scale in SCALES:
        for j, cell in enumerate(nc20_cells()):
            worlds.append(build_observation_episode_world(
                "NC-R20",
                seed=seed_for(1, 20, scale, j),
                scale_seconds=scale,
                nc20_cell=cell,
            ))
    return worlds


def event_worlds():
    controls = (
        "NC-R1", "NC-R2", "NC-R3", "NC-R4", "NC-R5", "NC-R6", "NC-R7",
        "NC-R11", "NC-R12", "NC-R13", "NC-R15", "NC-R16", "NC-R17",
        "NC-R17b", "NC-R18", "NC-R21",
    )
    worlds = []
    for ci, control in enumerate(controls, start=1):
        for scale in SCALES:
            worlds.append(build_observation_episode_world(
                control, seed=seed_for(2, ci, scale), scale_seconds=scale
            ))
    # Include the full matched-timing grid because measurement mechanics are a
    # required event/recovery challenge, not a one-cell sensitivity.
    for scale in SCALES:
        for j, cell in enumerate(nc20_cells()):
            worlds.append(build_observation_episode_world(
                "NC-R20",
                seed=seed_for(2, 20, scale, j),
                scale_seconds=scale,
                nc20_cell=cell,
            ))
    return worlds


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    print('STAGE1 baseline worlds start', flush=True)
    bw = baseline_worlds()
    print(f'STAGE1 baseline worlds built: {len(bw)}', flush=True)
    baseline_scores = []
    for kind, horizon in BASELINE_CANDIDATES:
        errors = []
        unavail = []
        for w in bw:
            e, u = baseline_error(w, kind, horizon)
            errors.append(e)
            unavail.append(u)
        baseline_scores.append(BaselineCandidateScore(
            kind=kind,
            horizon=horizon,
            median_error=float(np.median(errors)),
            n_cells=len(errors),
            unavailable_fraction=float(np.mean(unavail)),
        ))
    baseline_scores = sorted(baseline_scores, key=baseline_rank_key)
    selected_baseline = baseline_scores[0]
    print(f'STAGE1 baseline selected: {selected_baseline}', flush=True)

    print('STAGE1 event worlds start', flush=True)
    ew = event_worlds()
    print(f'STAGE1 event worlds built: {len(ew)}', flush=True)
    metric_results = {}
    best_by_metric = {}
    for metric in ("D1", "D2"):
        print(f'STAGE1 metric ranking start: {metric}', flush=True)
        ranked = rank_event_tuples(
            ew,
            baseline_kind=selected_baseline.kind,
            baseline_horizon=selected_baseline.horizon,
            metric=metric,
        )
        best_by_metric[metric] = ranked[0]
        metric_results[metric] = [asdict(x) for x in ranked[:20]]
        print(f'STAGE1 metric ranking done: {metric} best={ranked[0]}', flush=True)

    metric_best = sorted(best_by_metric.values(), key=metric_rank_key)
    selected_metric = metric_best[0]

    print('STAGE1 horizon qualification start', flush=True)
    horizon = horizon_qualification(ew)
    print(f'STAGE1 horizon={horizon["horizon"]} qualifier={horizon["qualifier"]}', flush=True)

    result = {
        "schema_version": "q040-estimator-stage1-v0.1",
        "real_q040_outcomes_opened": False,
        "baseline_ranking": [asdict(x) for x in baseline_scores],
        "selected_baseline_pre_full_pipeline_gate": asdict(selected_baseline),
        "metric_best": {k: asdict(v) for k, v in best_by_metric.items()},
        "metric_top20": metric_results,
        "selected_metric_event_tuple_pre_full_pipeline_gate": asdict(selected_metric),
        "horizon": horizon,
        "disposition": "Q040_STAGE1_SYNTHETIC_SELECTION_COMPLETE_PRE_FULL_PIPELINE_GATE",
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "disposition": result["disposition"],
        "selected_baseline": result["selected_baseline_pre_full_pipeline_gate"],
        "selected_metric_event_tuple": result["selected_metric_event_tuple_pre_full_pipeline_gate"],
        "horizon": result["horizon"]["horizon"],
        "horizon_qualifier": result["horizon"]["qualifier"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

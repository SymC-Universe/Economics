#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import numpy as np

from market_chi.q040_baseline_selection_v01 import (
    BASELINE_CONTROLS,
    WINDOWS,
    rank_candidates,
    score_baseline_candidate,
    summarize_candidate,
)
from market_chi.q040_observation_episode_v02 import (
    build_observation_episode_world,
    nc20_cells,
)

ORDINAL = {
    "NC-R5": 5,
    "NC-R15": 15,
    "NC-R16": 16,
    "NC-R20": 21,
}


def selection_seed(control: str, scale: int, replica: int, cell_ordinal: int = 0) -> int:
    return int(
        np.random.SeedSequence([
            20261002,
            ORDINAL[control],
            scale,
            100 + replica,
            cell_ordinal,
        ]).generate_state(1, dtype=np.uint32)[0]
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scale", type=int, required=True)
    ap.add_argument("--replica-start", type=int, default=0)
    ap.add_argument("--replica-stop", type=int, default=14)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    if args.scale not in (15, 30, 60, 300):
        raise SystemExit("invalid scale")
    if not (0 <= args.replica_start < args.replica_stop <= 14):
        raise SystemExit("invalid replica range")

    raw = []
    for control in BASELINE_CONTROLS:
        cells = nc20_cells() if control == "NC-R20" else [None]
        for cell_ord, cell in enumerate(cells):
            cell_key = None if cell is None else cell.key()
            for rep in range(args.replica_start, args.replica_stop):
                seed = selection_seed(control, args.scale, rep, cell_ord)
                world = build_observation_episode_world(
                    control,
                    seed=seed,
                    scale_seconds=args.scale,
                    nc20_cell=cell,
                )
                for kind in ("K1", "K2"):
                    for window in WINDOWS:
                        score = score_baseline_candidate(
                            world,
                            kind=kind,
                            window=window,
                            replica=rep,
                            cell_key=cell_key,
                        )
                        raw.append(score.to_dict())

    payload = {
        "schema_version": "q040-baseline-selection-shard-v1",
        "scale_seconds": args.scale,
        "replica_start": args.replica_start,
        "replica_stop": args.replica_stop,
        "real_q040_outcomes_opened": False,
        "scores": raw,
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "scale_seconds": args.scale,
        "replicas": [args.replica_start, args.replica_stop],
        "score_rows": len(raw),
        "status": "COMPLETE",
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

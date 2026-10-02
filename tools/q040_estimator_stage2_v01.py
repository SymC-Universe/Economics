#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path

import numpy as np

from market_chi.q040_estimator_stage2_v01 import (
    build_episode_records,
    qualify_m0_m2_world_panel,
    qualification_disposition,
    selected_config_from_stage1,
)
from market_chi.q040_observation_episode_v01 import (
    EXPECTED,
    build_observation_episode_world,
    nc20_cells,
)


ORDINAL = {name: i + 1 for i, name in enumerate(EXPECTED)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage1", required=True)
    ap.add_argument("--control", required=True)
    ap.add_argument("--scale", required=True, type=int)
    ap.add_argument("--output", required=True)
    ap.add_argument("--nc20-cell", default=None)
    args = ap.parse_args()

    stage1 = json.loads(Path(args.stage1).read_text())
    config = selected_config_from_stage1(stage1)

    cell = None
    cell_ordinal = -1
    if args.control == "NC-R20":
        cells = nc20_cells()
        if args.nc20_cell is None:
            raise SystemExit("NC-R20 requires --nc20-cell")
        matches = [(i, c) for i, c in enumerate(cells) if c.key() == args.nc20_cell]
        if not matches:
            raise SystemExit("unknown NC-R20 cell")
        cell_ordinal, cell = matches[0]

    records_by_world = []
    diagnostics = []
    for wi in range(200):
        seed = int(np.random.SeedSequence([
            20261001,
            ORDINAL[args.control],
            args.scale,
            cell_ordinal + 1,
            wi,
        ]).generate_state(1, dtype=np.uint32)[0])
        world = build_observation_episode_world(
            args.control,
            seed=seed,
            scale_seconds=args.scale,
            nc20_cell=cell,
        )
        records, diag = build_episode_records(world, config, world_index=wi)
        records_by_world.append(records)
        diagnostics.append(diag)

    summary = qualify_m0_m2_world_panel(
        records_by_world,
        horizon=config["horizon"],
    )
    disposition = qualification_disposition(args.control, summary)

    payload = {
        "schema_version": "q040-estimator-stage2-v0.1",
        "real_q040_outcomes_opened": False,
        "control": args.control,
        "scale": args.scale,
        "nc20_cell": None if cell is None else cell.key(),
        "selected_config": config,
        "world_count": 200,
        "episode_diagnostics": diagnostics,
        "summary": summary,
        "qualification": disposition,
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "control": args.control,
        "scale": args.scale,
        "nc20_cell": payload["nc20_cell"],
        "summary_status": summary["status"],
        "support_fraction": summary.get("support_fraction"),
        "add_rate": summary.get("add_rate"),
        "erosion_direction_rate_among_adds": summary.get("erosion_direction_rate_among_adds"),
        "adaptation_direction_rate_among_adds": summary.get("adaptation_direction_rate_among_adds"),
        "qualification": disposition,
    }, indent=2))
    return 0 if disposition["pass"] else 3


if __name__ == "__main__":
    raise SystemExit(main())

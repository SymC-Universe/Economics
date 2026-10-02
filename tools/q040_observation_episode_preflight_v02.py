#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from market_chi.q040_observation_episode_v02 import (
    EXPECTED,
    SCALES,
    build_observation_episode_world,
    determinism_check,
    nc20_cells,
    validate_world,
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    results = []
    faults = []
    base = 20261001

    for ci, control in enumerate(EXPECTED):
        if control == "NC-R20":
            continue
        for scale in SCALES:
            seed = int(np.random.SeedSequence([base, ci + 1, scale]).generate_state(1, dtype=np.uint32)[0])
            world = build_observation_episode_world(
                control, seed=seed, scale_seconds=scale
            )
            audit = validate_world(world)
            audit["deterministic"] = determinism_check(
                control, seed=seed, scale_seconds=scale
            )
            if not audit["pass"] or not audit["deterministic"]:
                faults.append({"control": control, "scale": scale, "audit": audit})
            results.append(audit)

    for scale in SCALES:
        for j, cell in enumerate(nc20_cells()):
            seed = int(np.random.SeedSequence([base, 20, scale, j]).generate_state(1, dtype=np.uint32)[0])
            world = build_observation_episode_world(
                "NC-R20",
                seed=seed,
                scale_seconds=scale,
                nc20_cell=cell,
            )
            audit = validate_world(world)
            audit["nc20_cell"] = cell.key()
            audit["deterministic"] = determinism_check(
                "NC-R20",
                seed=seed,
                scale_seconds=scale,
                nc20_cell=cell,
            )
            if not audit["pass"] or not audit["deterministic"]:
                faults.append({"control": "NC-R20", "scale": scale, "cell": cell.key(), "audit": audit})
            results.append(audit)

    payload = {
        "schema_version": "q040-synthetic-observation-episode-preflight-v2",
        "real_q040_outcomes_opened": False,
        "worlds_checked": len(results),
        "failed_worlds": len(faults),
        "faults": faults,
        "results": results,
        "disposition": (
            "Q040_SYNTHETIC_OBSERVATION_EPISODE_CONTRACT_PASS"
            if not faults
            else "Q040_SYNTHETIC_OBSERVATION_EPISODE_CONTRACT_FAIL"
        ),
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "disposition": payload["disposition"],
        "worlds_checked": payload["worlds_checked"],
        "failed_worlds": payload["failed_worlds"],
    }, indent=2))
    return 0 if not faults else 2


if __name__ == "__main__":
    raise SystemExit(main())

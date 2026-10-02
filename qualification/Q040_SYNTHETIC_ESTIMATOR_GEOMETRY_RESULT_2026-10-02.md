# Q040 Synthetic Estimator Geometry Result — 2026-10-02

**Governance:** SymC GOM v1.0 + Research Continuity and Execution Protocol  
**Branch:** `market-chi-architecture`  
**Evidence class:** synthetic-only estimator geometry qualification  
**Real Q040 outcomes opened:** NO  
**Geometry freeze commit:** `bfe84c38016a62b03822120416413f9b8b9576da`  
**Mechanical seed-sentinel repair commit:** `bd335ee4146fa03d3b19c9efe21fe3b08191f366`  
**Local result:** `C:\Users\CCGTi\OneDrive\Desktop\SymC_Economics\SymC_TF\Data\_symc_q040_estimator_geometry_v01\result_fix2.json`  
**Completed:** 2026-10-02T12:48:52.740Z  
**SHA-256:** `D3004347493262D46EEF8C6740FA4C3354BD1EB1CE489CA5D2DA0FC292CE5BC3`

## Preserved mechanical failure

The first post-freeze geometry invocation failed mechanically before scientific evaluation because the seed-sentinel encoding supplied a negative integer to `numpy.random.SeedSequence`, raising `ValueError: expected non-negative integer`. The failure remains preserved in the local `run.log`. The repair at `bd335ee4146fa03d3b19c9efe21fe3b08191f366` changed only seed encoding and did not alter the frozen estimator geometry, thresholds, candidate windows, controls, or real-data firewall.

## Post-repair frozen result

The completed post-repair artifact has disposition `Q040_SYNTHETIC_ESTIMATOR_GEOMETRY_REFUSED`.

For K1, all frozen baseline windows are ineligible under the preregistered all-required-world coverage floor: window 10 minimum coverage = 0.10107421875, window 20 = 0.1650390625, window 40 = 0.28857421875. Each candidate was evaluated over 864 baseline worlds.

For K2, all frozen baseline windows are likewise ineligible: window 10 minimum coverage = 0.0, window 20 = 0.0, window 40 = 0.134765625, again over 864 baseline worlds.

Therefore `baseline.ranked=[]`; metric qualification terminates as `BASELINE_OPERATOR_REFUSED`; event-definition selection is `REFUSED`; no K1/K2 candidate is promoted. The separately computed finite-time horizon diagnostic selected 20 samples across 272 worlds, but its qualifier is null and it cannot rescue the failed baseline gate.

## Scientific disposition

This is a valid synthetic refusal, not an execution crash and not a license to retune. No threshold change, 10/20/40 grid extension, K1/K2 rescue, D1/D2 continuation, event/history continuation, or real-Q040 outcome opening is authorized from this result.

The next scientific state is:

`SCIENTIFIC_GATE / Q040_BASELINE_REFUSAL_FAILURE_OUTLIER_AUDIT`

The audit may interpret the refusal and define a prospective successor, but any successor estimator geometry or baseline family must be frozen prospectively with disjoint qualification evidence before execution. Real Q040 outcomes remain sealed.

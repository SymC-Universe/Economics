# Q040 Repaired Synthetic Lineage Qualification v0.2
**Date:** 2026-10-02
**Higher authority:** Q040 Recoverability Plan Packet v0.6
**Semantic defect audit:** `qualification/Q040_SYNTHETIC_KNOWN_TRUTH_SEMANTIC_CONFORMANCE_AUDIT_2026-10-02.md`
**Manifest:** `qualification/Q040_SYNTHETIC_KNOWN_TRUTH_MANIFEST_v0.2_2026-10-02.json`
**Generator:** `market_chi/q040_synthetic_generators_v0_2.py`
**Observation contract amendment:** `qualification/Q040_SYNTHETIC_OBSERVATION_EPISODE_CONTRACT_v0.2_2026-10-02.md`
**Real Q040 outcomes:** SEALED

## Failure lineage preserved

The first repaired-generator pass exposed two synthetic construction failures before estimator fitting:

1. NC-R2 stochastic clustering under-realized its own frozen clustering invariant. The invariant was not relaxed; the known-truth event construction was repaired to deterministic immigrant-plus-aftershock clusters. Failure record: `qualification/Q040_V0_2_NCR2_GENERATOR_FAILURE_INVESTIGATION_2026-10-02.md`.
2. NC-R19 shared regime strongly controlled proxies and the slower target but did not control actual event frequency under the frozen seed. The invariant was not relaxed; event timing was repaired to a deterministic regime-gated schedule. Failure record: `qualification/Q040_V0_2_NCR19_GENERATOR_FAILURE_INVESTIGATION_2026-10-02.md`.

No estimator result had been observed during either repair.

## Generator contract

Final v0.2 generator-contract result:

`Q040_SYNTHETIC_GENERATOR_CONTRACT_V02_PASS`

Controls passed: 22/22.

Local generator-contract artifact SHA-256:

`C2B1BB8C106E2AD268BF377B86B11D012032598279A7411EB7257D4EA95E01AF`

Selected repaired invariants:
- NC-R2: 48 shocks, 0.68085 of inter-shock intervals <=32 samples, rate span 0;
- NC-R3: true erosion rate delta -0.0192;
- NC-R6: burden-rate correlation -1.0 in positive direction and +1.0 in negative direction;
- NC-R10: within-scale erosion rate delta -0.016 with burden-slower correlation -0.0117;
- NC-R17: event rate 0.01025 in high regime vs 0.00146 in low regime;
- NC-R19: event rate 0.01465 in high regime vs 0.00244 in low regime;
- NC-R21: exactly 9 events, below the frozen sparse-tail floor.

## Observation/episode contract

v0.2 common-interface tests:

`5 passed in 28.95s`

Full repaired preflight:

`worlds_checked=180`

`failed_worlds=0`

`Q040_SYNTHETIC_OBSERVATION_EPISODE_CONTRACT_PASS`

Local preflight artifact SHA-256:

`0B107B79B1708AD870F119480FF31032E69CEDD4EA7FCC1578AD0C78CE0EC953`

## Disposition

The v0.1 semantic lineage is superseded for estimator qualification.

`Q040_REPAIRED_SYNTHETIC_LINEAGE_V0_2=QUALIFIED`

`Q040_ESTIMATOR_QUALIFICATION=AUTHORIZED_SYNTHETIC_ONLY`

`Q040_REAL_OUTCOMES=SEALED`

`NEXT=FREEZE_REMAINING_ESTIMATOR_IMPLEMENTATION_DETAILS_AND_EXECUTE_SYNTHETIC_ESTIMATOR_QUALIFICATION`

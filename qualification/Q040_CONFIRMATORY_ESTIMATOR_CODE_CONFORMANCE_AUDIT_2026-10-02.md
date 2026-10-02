# Q040 Confirmatory Estimator Code Conformance Audit
**Date:** 2026-10-02
**Authority:** `qualification/Q040_SYNTHETIC_ESTIMATOR_IMPLEMENTATION_CLOSURE_v0.1_2026-10-02.md`
**Audited code:** `market_chi/q040_estimator_stage2_v01.py`, `tools/q040_estimator_stage2_v01.py`
**Real Q040 outcomes:** SEALED

## Finding

The legacy stage-2 implementation predates the final frozen estimator closure and is not authorized for confirmatory Q040 history qualification.

Material mismatches are:

1. **Penalty mismatch.** The legacy fitter uses ridge regularization (default `ridge=1e-4`). The frozen primary model is unpenalized multinomial logistic discrete-time hazard.

2. **Time-basis mismatch.** The legacy code uses continuous linear/quadratic/log time features. The frozen model uses eight equal-width piecewise-constant time bins with seven dummy columns.

3. **Confirmatory-bank mismatch.** The legacy tool constructs 200 worlds and five 160/40 world folds. The frozen confirmatory history bank is 30 replicas with grouped folds `replica mod 5`, training on 24 and testing on 6 whole replicas.

4. **Scoring mismatch.** The legacy `episode_brier` omits the frozen training-only Kaplan-Meier censoring model and IPCW integrated Brier construction.

5. **Censoring qualification mismatch.** The legacy implementation does not enforce `G(k) >= 0.05` across the scoring grid.

6. **Semantic-lineage mismatch.** Legacy control disposition logic treats NC-R2 as erosion and NC-R3 as a null control, which conflicts with the repaired v0.4 known-truth lineage where NC-R2 is clustered shocks with constant recovery and NC-R3 is true erosion.

7. **Source-lineage mismatch.** The legacy tool imports the old stage-1 and observation v0.1 implementations rather than the repaired v0.4 observation/episode lineage and the prospective B2 baseline result.

## Disposition

`Q040_ESTIMATOR_STAGE2_V01=SUPERSEDED_NOT_AUTHORIZED`

No result produced by this legacy stage-2 code may qualify M0/M2, history direction, or a real-data gate.

The newer metric/event module `market_chi/q040_metric_event_selection_v01.py` is mechanically consistent with the frozen D1/D2 and upward-crossing event definitions and has passed its local unit tests, but it does not itself implement confirmatory M0/M2 qualification.

## Required successor

After B2 freezes the global baseline and the metric/event/horizon selection is completed on a fresh prospective bank, implement a new confirmatory engine directly from the frozen closure:
- unpenalized multinomial logistic competing-risk hazard;
- eight frozen time bins;
- 30-replica C bank;
- grouped `r mod 5` folds;
- training-only KM censoring survival;
- IPCW integrated Brier score;
- paired 10,000-replicate bootstrap and four-scale Holm family;
- repaired v0.4 control semantics;
- NC-R17b oracle diagnostic;
- NC-R6 direction-interaction secondary diagnostic.

`Q040_REAL_OUTCOMES=SEALED`

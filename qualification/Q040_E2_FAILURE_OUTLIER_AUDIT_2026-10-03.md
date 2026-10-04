# Q040 E2 Failure / Outlier Audit — 2026-10-03

**Authority:** SymC GOM v1.0 + Research Continuity and Execution Protocol
**Parent result:** `qualification/Q040_METRIC_EVENT_E2_RESULT_2026-10-02.md`
**Parent disposition:** `Q040_EVENT_DEFINITION_REFUSED_E2`
**Real Q040 outcomes:** SEALED
**Scope:** Interpret the frozen E2 refusal, preserve failures/outliers, and determine whether a genuinely new prospective plan is warranted. No E2 tuple is retuned, rescued, or reclassified.

## Findings

The frozen E2 refusal remains valid independently of the return-truth issue below. The leading D1 family has no metric-fit refusals but fails the frozen entry gates: overall median recall is 0.75 against the 0.80 floor and minimum cell median recall is 0.026542160660028458 against the 0.60 floor. The leading D2 family reaches overall median recall 0.875 but has 567 refused metric-fit folds where zero are allowed, and also fails cellwise support/performance requirements. These failures remain preserved.

A separate truth-contract defect is present in the return/horizon component. The E2 horizon diagnostic contains 32 declared horizon units per scale across four scales, 128 control/scale units total. Every unit has positive perturbation-episode support, but every unit has `sr20=0`, `sr40=0`, and `sr80=0`. The E2 bank therefore supplies no positive sustained-return truth for the horizon diagnostic despite abundant perturbation events.

The v0.4 synthetic-lineage qualification established generator conformance, observation/episode structural validity, determinism, and recurrent-event support, including the non-NC-R21 >=40-event floor. It did not require positive sustained-return truth support. In the frozen observation/episode contract, true sustained return requires three consecutive samples inside the true return radius before the next perturbation. The opened E2 bank consequently cannot support a scientific inference about sustained-return timing or terminal-state recovery performance because no positive sustained-return cases exist in the relevant truth bank. This audit does not infer which generator parameter should change from the opened E2 outcomes.

The E2 horizon combiner also has a deterministic nonvacuity defect. The 90% retention test is applied only when `cif80 > 0`. When `cif20=cif40=cif80=0`, the retention test is skipped and the <0.02 saturation condition is trivially satisfied, so the all-zero bank returns horizon 20 with `horizon_qualifier=null`. That 20-sample horizon is vacuous and has no promotion meaning.

## Interpretation and gate

`Q040_EVENT_DEFINITION_REFUSED_E2` remains preserved. D1 and D2 are not rehabilitated, confirmatory C is not authorized, and real Q040 outcomes remain sealed. However, return-timing, terminal-state, and horizon failures may not be promoted as evidence that recovery itself is absent, slow, or unidentifiable because the synthetic truth bank supplied no positive sustained-return outcomes.

A genuinely new prospective synthetic plan is warranted before any successor estimator qualification. Before a fresh disjoint bank is generated, the program must prospectively freeze: (1) a nonvacuous sustained-return truth-support contract; (2) nonvacuous horizon semantics that refuse an all-zero recovery bank rather than selecting a horizon; and (3) any generator/truth-definition changes from first principles and/or external scientific justification rather than parameter tuning against opened E2 outcomes.

This audit does not choose a new return radius, sustain duration, perturbation density, noise level, horizon threshold, or estimator threshold. Those remain scientific degrees of freedom.

`Q040_E2_FAILURE_OUTLIER_AUDIT=COMPLETE`
`Q040_EVENT_DEFINITION_REFUSED_E2=PRESERVED`
`Q040_HORIZON_20=NONPROMOTABLE_VACUOUS_ALL_ZERO_RETURN_TRUTH`
`Q040_REAL_OUTCOMES=SEALED`
`NEXT=SCIENTIFIC_GATE/Q040_SYNTHETIC_RETURN_TRUTH_CONTRACT_DECISION`

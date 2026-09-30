# Q039 + Q040 BOUNDED REVISED-PLAN RECHECK PACKET
**Date:** 2026-09-30  
**Governance:** SymC GOM v1.0 §15.4.7–15.4.9  
**Purpose:** Bounded second-pass verification that the mediated Plan Deltas resolved the identified defects without introducing new scientific flexibility, weakening falsifiability, or contaminating the outcome firewall.

## Authority binding

Repository:

`SymC-Universe/Economics`

Branch:

`market-chi-architecture`

### Q039 revised authority

Path:

`qualification/MNQ_TEMPORAL_HIERARCHY_PREREGISTRATION_DRAFT_v0.5_2026-09-30.md`

Exact revised commit:

`1611705aa2ee75176207387598082d08a8ce56d8`

Superseded authority:

`b757d0dd65a700be1bf1d2cb5233c75c83086308`

The upstream Q039 feature contract is explicitly bound inside §8.1 to:

`market_chi/microstructure_v2.py`

blob:

`9bdfa33400f613b59b9e9be2f0b1fd682bf9ad08`

### Q040 revised authority

Path:

`qualification/Q040_RECOVERABILITY_PLAN_PACKET_v0.6_2026-09-30.md`

Exact revised commit:

`50e8587d9b440370dc13dcd170178fbce123c3fb`

Superseded v0.5 authority:

`84f5c5fa0e6be7ac85593c0d9098334979acdbe1`

### Mediation authority

Path:

`qualification/Q039_Q040_APQ_EVIDENCE_RESOLUTION_AND_PLAN_DELTA_DRAFT_2026-09-30.md`

Commit introducing mediation record:

`5efd3888bd262543b2af6f9cac027d6d906b8b1a`

## Outcome firewall

Do not inspect real Q039 NC7/Layer-R/Layer-L outcomes or any real Q040 outcome.

Do not select thresholds, models, source segments, controls, representations, or refusal rules from real outcome behavior.

This is a revised-plan recheck, not a new broad APQ review.

## Required reviewer task

Read the exact revised authorities above and answer only whether the revisions:

1. resolved the objections they were designed to resolve;
2. introduced a new discretionary degree of freedom;
3. weakened an existing refusal/falsification route;
4. changed a previously qualified object that now requires synthetic recomputation;
5. created an implementation ambiguity that would allow two competent implementers to diverge materially;
6. preserved the outcome firewall and the stated claim ceilings.

Do not reopen already resolved v0.4/v0.5 questions unless the revision itself reintroduces them.

---

# Q039 v0.5 targeted recheck

Verify the following.

## R39-1 NC7 derivation-graph partition

Confirm that §8.0 now gives one outcome-independent rule:

- real timing/flow/session-phase/spread context remains real;
- any quantity that contracts the real L10 size state is recomputed from the isotropic replacement;
- no real L10 size state or function of it enters an NC7 model matrix, contrast, or target;
- the scope is explicitly limited to destruction of the L10 size-semantic channel rather than pretending timing/price context is statistically independent.

Disposition:

`PASS / FAIL / NEED_MORE_INFO`

Evidence:

____________________________________________________________________

## R39-2 upstream formula binding

Confirm that §8.1 uniquely binds:

- `spread_last`;
- `l10_imbalance_last`;
- `microprice_offset_last`;
- the upstream feature-builder contract/blob.

Check that the formulas stated in §8.1 are consistent with the bound feature builder.

Disposition:

`PASS / FAIL / NEED_MORE_INFO`

Evidence:

____________________________________________________________________

## R39-3 physical-cone and fallback rule

Confirm that §8.2 freezes:

\[
x^{NC7}_{i,+}=\max(x^{NC7}_{i},0),
\qquad
q_i^{NC7}=\operatorname{expm1}(x^{NC7}_{i,+}),
\]

for **derived native-context covariates only**.

Verify specifically:

- semantic \(D/I\) remain on the unprojected Gaussian NC7 state;
- native L10 imbalance zero-denominator fallback is exactly `0.0`;
- synthetic microprice uses real prices + projected synthetic L1 sizes;
- zero L1 synthetic size gives contemporaneous midprice, hence offset `0.0`;
- spread remains real and has no synthetic-size fallback;
- bid/ask treatment is symmetric;
- no post hoc rescaling, amplitude matching, renormalization, or repair is permitted;
- the supplemental preflight can refuse via `NC7_DERIVED_CONTEXT_PREFLIGHT_REFUSED`.

Disposition:

`PASS / FAIL / NEED_MORE_INFO`

Evidence:

____________________________________________________________________

## R39-4 source freeze

Confirm that §23.1 freezes one five-date source manifest with file SHA-256, instrument ID, symbol, and an outcome-independent deterministic source-resolution rule before real outcome exposure.

Disposition:

`PASS / FAIL / NEED_MORE_INFO`

Evidence:

____________________________________________________________________

## R39-5 recomputation boundary

Does any v0.5 revision alter the already-qualified NC1–NC6, NC8, NC8b, or the NC7 generator/timing plumbing?

`YES / NO`

If YES, identify exactly what must be rerun.

If NO, confirm that only the new derived-context supplemental preflight is scientifically required before the real NC7 gate.

Evidence:

____________________________________________________________________

## Q039 recheck status

Choose exactly one:

`Q039_V0_5_RECHECK=PASS`

`Q039_V0_5_RECHECK=PASS_WITH_MINOR_DOCUMENTATION`

`Q039_V0_5_RECHECK=REVISE`

`Q039_V0_5_RECHECK=BLOCKED`

A PASS does not open real outcomes. It authorizes the frozen synthetic/implementation qualification steps that precede real execution.

---

# Q040 v0.6 targeted recheck

Verify the following.

## R40-1 native measurement contract and NC-R20

Confirm that §5.1 requires the \(Z_S(t)\) measurement contract to freeze source fields, valid-update logic, carry-forward, staleness, session boundaries, missing/invalid refusal behavior, and causal aggregation order.

Confirm NC-R20 now has two distinct prospective uses:

1. synthetic qualification using a frozen schedule family/grid;
2. later sealed development-day artifact screening using the actual valid update timestamps while replacing native state updates with the frozen null process.

Disposition:

`PASS / FAIL / NEED_MORE_INFO`

Evidence:

____________________________________________________________________

## R40-2 primary history family and score

Confirm §17.1 freezes:

- primary history extension = M2 cumulative burden;
- primary probabilistic score = competing-risk integrated Brier score for sustained-return cumulative incidence;
- time grid/horizon and censoring-weight implementation must be frozen before real outcomes;
- M1/M3 are ordered secondary/adjudication routes;
- M4 cannot rescue a failed M2 route;
- four scale-level primary tests are controlled by Holm at two-sided familywise \(\alpha=0.05\);
- secondary metrics cannot rescue a failed primary score.

Disposition:

`PASS / FAIL / NEED_MORE_INFO`

Evidence:

____________________________________________________________________

## R40-3 K1/K2 operator selection

Confirm §9.1.1 is deterministic and outcome-independent:

- both operators face numerical/identifiability checks;
- both face the frozen curvature × noise × update-density/gap synthetic grid including NC-R5, NC-R15, NC-R16, NC-R20;
- a failed operator is ineligible;
- one survivor is frozen;
- two survivors are resolved by median normalized baseline-location error;
- exact tie defaults to K1;
- zero survivors returns `BASELINE_OPERATOR_REFUSED`.

Disposition:

`PASS / FAIL / NEED_MORE_INFO`

Evidence:

____________________________________________________________________

## R40-4 event-history comparator calibration

Confirm §16.1 freezes simulation-based diagnostics/acceptance envelopes before real fitting and retains `NATIVE_HISTORY_MODEL_NOT_QUALIFIED` if the real fitted comparator fails the envelope.

Check whether any materially discretionary calibration choice remains.

Disposition:

`PASS / FAIL / NEED_MORE_INFO`

Evidence:

____________________________________________________________________

## R40-5 known-truth hard gates

Confirm that NC-R17b, NC-R20, and NC-R21 are mandatory pre-real-outcome qualification gates, not optional robustness analyses.

Confirm:

- NC-R17b attacks correlated omitted-native-state confounding;
- NC-R20 attacks update/carry-forward measurement artifacts;
- NC-R21 attacks sparse-tail false history signals.

Disposition:

`PASS / FAIL / NEED_MORE_INFO`

Evidence:

____________________________________________________________________

## R40-6 refusal and reorganization logic

Confirm that:

- `RECOVERY_NOT_IDENTIFIABLE` can be returned when no coherent recovery object is supportable;
- stable migration to a new operating baseline has its own disposition rather than being forced into failed recovery;
- \(A_{\mathrm{transient}}\) and NC-R12 explicitly preserve non-normal transient amplification as distinct from instability;
- \(\chi\), \(\Chi\), and \(\Chi_{\mathrm{arc}}\) retain independent admission/refusal paths.

Disposition:

`PASS / FAIL / NEED_MORE_INFO`

Evidence:

____________________________________________________________________

## R40-7 exogenous forcing

Confirm \(\xi(t)\) is prospectively frozen as:

- scheduled/time-stamped event indicator in primary M0;
- required event/non-event sensitivity;
- narrow exclusions sensitivity-only;
- unobserved/unscheduled news remains a residual confound.

Disposition:

`PASS / FAIL / NEED_MORE_INFO`

Evidence:

____________________________________________________________________

## R40-8 new-flexibility audit

List any new choice introduced by v0.6 that is not already frozen or routed to an explicit refusal state.

____________________________________________________________________

## Q040 recheck status

Choose exactly one:

`Q040_V0_6_RECHECK=PASS`

`Q040_V0_6_RECHECK=PASS_WITH_MINOR_DOCUMENTATION`

`Q040_V0_6_RECHECK=REVISE`

`Q040_V0_6_RECHECK=BLOCKED`

A PASS does not authorize real Q040 outcomes. It authorizes synthetic-known-truth freezing/implementation and synthetic qualification under the guarded conveyor.

---

# Required final return

Return:

`Q039_V0_5_RECHECK=<status>`

`Q040_V0_6_RECHECK=<status>`

Then list only:

- any remaining BLOCKER;
- any remaining MATERIAL issue;
- the smallest required correction, if any;
- whether previously qualified synthetic work must be recomputed.

Do not provide a new broad plan unless the revised architecture actually fails.
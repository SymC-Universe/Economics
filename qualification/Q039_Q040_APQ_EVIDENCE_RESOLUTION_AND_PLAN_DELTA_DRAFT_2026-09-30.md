# Q039 + Q040 APQ Evidence Resolution and Plan Delta Draft
**Date:** 2026-09-30  
**Status:** Post-first-pass mediation under GOM v1.0 §15.4.5–15.4.9  
**Outcome firewall:** Real Q039 NC7 and Q040 scientific outcomes remain sealed.

## 1. Review set and independence

The current APQ evidence set contains:

- **Claude:** isolated source-bound first pass against the exact pinned Q039/Q040 authorities.
- **Kimi K3:** isolated source-bound first pass against the same pinned authorities. Kimi disclosed prior participation in Q039 v0.2/v0.3 review, but no prior exposure to Q039 v0.4, Q040, or another current Q039/Q040 review before this pass.
- **Two unique secondary adversarial first passes:** logic/falsification/leakage/review-instrument attacks without source authority.
- **One duplicate secondary upload:** preserved but not counted as additional independent evidence.
- **ChatGPT:** mediator/source verifier only after seeing Claude; not counted as an isolated first-pass reviewer.

Per GOM, reviewer count and majority agreement do not qualify a plan. The purpose of this document is evidence-mediated resolution of objections and construction of the smallest prospective Plan Delta.

## 2. High-level adjudication

### Q039

**Current v0.4 status: `REVISE` before real NC7 execution.**

Claude and Kimi agree on the substantive defect even though they assign different gate labels. The preregistration does not freeze the treatment of nonsemantic Layer-L context variables inside NC7. Both reviews independently converge on the same scientific rule:

- keep real timing/flow variables;
- keep real spread because it is price-only with respect to the replaced L10 size state;
- recompute native L10 imbalance from the same isotropic replacement state;
- recompute the size-weighting part of microprice offset from the isotropic replacement state while retaining the required real prices;
- do not allow any function of the real L10 size state to enter an NC7 predictor, contrast, or target.

The handoff itself states that F.1 must be resolved before any real Q039 point contrast is opened. Under the GOM sequence, that means v0.4 is not execution-qualified as written. The correct mediation state is therefore **REVISE**, not a vote between `NOT_QUALIFIED` and `QUALIFIED_WITH_DELTA`. A prospective Plan Delta can repair it, followed by a bounded targeted recheck.

### Q040

**Current v0.5 status: adequate to advance to Plan Delta, but not yet execution-qualified.**

Both primary reviewers independently return `QUALIFIED_WITH_PLAN_DELTA` and find no irreparable blocker. Their MATERIAL objections are complementary rather than contradictory. Under GOM §15.4.7–15.4.9, Q040 now advances to plan revision and revised-plan recheck; it does **not** advance directly to real outcomes.

## 3. Objection mediation

### Q039 objections

| Issue | Claude | Kimi | Mediator disposition | Resolution |
|---|---|---|---|---|
| NC7 nonsemantic context rule | BLOCKER; current v0.4 not qualified | MATERIAL; qualifies with prospective delta | `ACCEPTED_MODIFIED` | Treat current v0.4 as `REVISE`; adopt a single frozen derivation-graph rule before any real NC7 outcome. |
| Native L10 imbalance leakage | Recompute from isotropic state | Recompute from isotropic state | `ACCEPTED_MODIFIED` | Consensus supported by prereg §8/§9.2 and handoff F.1. |
| Microprice offset | Recompute size-weighted component | Recompute from synthetic L1 sizes + retained real L1 prices | `ACCEPTED_MODIFIED` | Same scientific rule; implementation must bind the exact upstream formula. |
| Spread | Keep real, caveat residual joint-process dependence | Keep real; price-only with respect to replaced size state | `ACCEPTED_MODIFIED` | Keep real. Treat residual price/size co-determination as a bounded limitation, not a size-state leakage path. |
| Flow/timing variables | Keep real | Keep real | `ACCEPTED_MODIFIED` | Preserve event rows, trade volume, signed volume, update fraction, staleness, and session phase. |
| Upstream formula provenance | Exact formulas should be confirmed | Upstream formulas not pinned; bind contract/hash | `ACCEPTED_MODIFIED` | Bind feature-builder contract/version and formula identities before execution. |
| Gaussian isotropic states vs physical size-derived covariates | Not separately raised | Requires frozen valid-cone and zero-size conventions | `ACCEPTED_MODIFIED` | Add prospective derived-covariate convention without changing the already-qualified NC7 generator. |
| Source manifest timing/segment rule | Minor provenance | Freeze/hash manifest before exposure; deterministic candidate rule | `ACCEPTED_MODIFIED` | Freeze source manifest before outcomes and record deterministic source-resolution rule. |

### Q040 objections

| Issue | Claude | Kimi | Mediator disposition | Resolution |
|---|---|---|---|---|
| Measurement/carry-forward artifact on \(Z_S\) | Not raised | MATERIAL; freeze measurement contract + NC-R20 | `ACCEPTED_TEST_ADDED` | Strong source-specific concern. Q039 shows the same data family has carry-forward/staleness mechanics capable of manufacturing persistence. Add direct Q040 measurement-contract null. |
| History-model multiplicity | Not raised | MATERIAL; M1–M4 × scales × scores lacks frozen family rule | `ACCEPTED_MODIFIED` | Freeze one primary history extension, one primary scoring metric, scale-family multiplicity rule, and secondary gate order before synthetic qualification. |
| M0 omitted-variable/shared-premise risk | MATERIAL; add explicit omitted-covariate stress test | Residual confounding acknowledged by claim ceiling; NC-R17 exists | `ACCEPTED_TEST_ADDED` | Do not create a wholly separate generic control. Strengthen NC-R17 with a deliberately withheld correlated native covariate variant and require false-history refusal. |
| K1/K2 baseline operator | MATERIAL; current rule too open | MINOR delegated degree of freedom, but must freeze | `ACCEPTED_MODIFIED` | Treat as MATERIAL because APQ question 5 explicitly delegates this decision and operator choice can change the recovery object. Freeze a deterministic synthetic-only operator/refusal rule. |
| Hawkes/event-history comparator calibration | MATERIAL; diagnostics named but not defined | Not separately material | `ACCEPTED_MODIFIED` | Freeze calibration diagnostics using a synthetic known-truth acceptance envelope before real use; comparator refusal remains available. |
| Sparse-tail recurrent-event stability | MATERIAL; no synthetic refusal test | Not raised | `ACCEPTED_TEST_ADDED` | Add a low-event-count known-truth control to prove `INSUFFICIENT_REPEATED_EVENTS` triggers rather than unstable significance. |
| \(\xi(t)\) treatment | Not resolved | Explicit APQ choice supplied | `ACCEPTED_MODIFIED` | Primary M0 includes scheduled-event indicator; report event/non-event stratified sensitivity; narrow exclusion windows are sensitivity-only, not primary. |
| Stable reorganization vs literal return | Secondary reviewers flag it | Q040 already separates baseline migration and R3 reorganization | `ACCEPTED_MODIFIED` | Existing architecture substantially covers it; add an explicit within-scale stable-reorganization disposition so nonreturn to the old state is not automatically failure. |
| \(\chi/\Chi/\Chi_{\mathrm{arc}}\) notation and transport | MINOR glossary/refusal-token suggestion | MINOR glossary/transport note | `ACCEPTED_MODIFIED` | Add one-line notation glossary and explicit architecture refusal tokens. |
| Q040 stand-alone provenance | MINOR Plan Packet cross-reference | Measurement contract concern stronger | `ACCEPTED_MODIFIED` | Cross-reference the Stage Q040-3 source/data freeze directly in the Plan Packet. |

## 4. Q039 exact prospective Plan Delta

Create **Q039 preregistration v0.5** from the pinned v0.4 authority with no real NC7 outcome exposure.

### PD-Q039-1: frozen NC7 context rule

Insert:

> In every NC7 null world, covariates whose frozen derivations do not contract the L10 size state — event rows, trade volume, signed trade volume, session-phase harmonics, spread, and the timing-derived update fraction and staleness age — retain their exact real pipeline values, while every quantity whose derivation contracts the L10 size state — all semantic predictors and targets, the signed microprice offset, and the native L10 imbalance — is computed from the isotropic replacement states carried forward under the frozen state rule through the identical derivation and aggregation pathway, with real prices retained where required; no real L10 size state or function of it may enter any NC7 model matrix, contrast, or target.

### PD-Q039-2: upstream formula binding

Before real NC7 execution, bind by text or immutable contract/hash:

- `spread_last`;
- `microprice_offset_last`;
- `l10_imbalance_last`;
- the upstream feature-builder version that creates them.

If a required derivation cannot be established uniquely, return:

`NC7_CONTEXT_RULE_UNCLASSIFIABLE`

and hold the affected NC7 comparison.

### PD-Q039-3: synthetic-state derived-covariate convention

Do not change the qualified isotropic generator, seed, world count, or timing logic.

For size-derived covariates only:

1. invert the synthetic log-state coordinate with the frozen production-domain mapping;
2. enforce the physical nonnegative size cone prospectively;
3. define the zero-total-size fallback prospectively;
4. run a synthetic-only preflight verifying all recomputed NC7 covariates are finite and non-constant across all 200 worlds.

The exact projection/fallback implementation is frozen before the targeted recheck.

### PD-Q039-4: source freeze

Freeze and hash the five-date source manifest before real outcome exposure, including the deterministic candidate/source-resolution rule. No source segment may be selected from Q039 outcome behavior.

### Q039 recheck requirement

A bounded second pass verifies only:

- the new §8 NC7 rule;
- formula/contract binding;
- the derived-covariate convention;
- source-manifest freeze;
- that no new tunable degree of freedom was introduced.

If those pass, Q039 may freeze and execute the real NC7 gate. No completed synthetic core needs to be recomputed unless the Plan Delta changes a previously qualified synthetic object.

## 5. Q040 prospective Plan Delta

Create **Q040 Plan Packet v0.6** from v0.5 while keeping real outcomes sealed.

### PD-Q040-1: freeze the \(Z_S\) measurement contract and add NC-R20

The plan must explicitly freeze:

- source fields;
- valid-state/update definition;
- carry-forward rule;
- staleness rule;
- session-boundary rule;
- missing/invalid-state refusal behavior;
- causal aggregation/standardization order.

Add:

**NC-R20 matched-update-timing measurement-artifact null**

Preserve a realistic/prespecified update schedule and carry-forward mechanics while replacing the native state updates with a known-truth null process that has no history-dependent recovery law. The full frozen Q040 recovery pipeline must not produce an erosion/adaptation/history-adds disposition beyond the frozen false-positive tolerance. Failure means the measurement contract or recovery object is not qualified.

### PD-Q040-2: freeze primary history-testing family and multiplicity

Before synthetic qualification, freeze:

- one primary history extension per scale;
- one primary probabilistic recovery score;
- fixed ordering of secondary M1/M3/M4 tests;
- familywise treatment across the four scales;
- secondary metrics as diagnostics rather than alternative success routes.

**Recommended scientific choice for PI sign-off:** M2 cumulative burden as the primary history extension because it tests repeated burden without treating attempt count as mechanism; M1 remains ordinal/descriptive, M3 adjudicates incomplete-recovery alternatives, and M4 opens only after independent justification.

**Recommended primary score for PI sign-off:** integrated Brier score over the frozen finite-time recovery horizon, with survival log loss/partial likelihood, calibration, and discrimination secondary.

### PD-Q040-3: deterministic K1/K2 qualification/refusal rule

Use synthetic known truths only.

Required sequence:

1. K1 and K2 must each pass numerical/identifiability checks.
2. Each must correctly refuse false recovery-law change on the moving-baseline / changing-noise / heteroskedastic-coordinate controls, including NC-R5, NC-R15, NC-R16, and NC-R20.
3. Any operator that fails a required known-truth disposition is ineligible.
4. If exactly one remains eligible, freeze it.
5. If both remain eligible, freeze the operator with the lower median normalized baseline-location error across the frozen synthetic grid; exact ties default to K1 as the lower-complexity operator.
6. If neither qualifies, return `BASELINE_OPERATOR_REFUSED`.

No real Q040 outcome may influence this choice.

### PD-Q040-4: native event-history comparator qualification

Freeze the Hawkes/queue-reactive comparator calibration route prospectively.

Use simulation-based known-truth calibration rather than a threshold selected from real outcomes:

- define the time-rescaling / event-count / background-intensity diagnostics;
- obtain their acceptance envelope from frozen synthetic worlds in which the event-history model is correctly specified;
- require the real fitted comparator to satisfy the frozen diagnostic envelope;
- otherwise return `NATIVE_HISTORY_MODEL_NOT_QUALIFIED`.

### PD-Q040-5: strengthen confound/refusal known truths

**NC-R17b correlated omitted-native-covariate variant**

Construct a known-truth world in which a native covariate drives both apparent perturbation history and recovery duration but is deliberately withheld from M0. The pipeline must not return an unconditional history-mechanism claim; it must expose comparator insufficiency, ambiguity, or the frozen claim limitation.

**NC-R21 sparse-tail recurrent-event refusal**

Construct a memoryless world with deliberately low repeated-event counts in one or more history strata. The frozen pipeline must return `INSUFFICIENT_REPEATED_EVENTS` rather than a nominally significant history effect.

### PD-Q040-6: exogenous forcing and reorganization states

Freeze \(\xi(t)\):

- scheduled/time-stamped events enter M0 as a primary event indicator;
- event/non-event stratified analysis is a required sensitivity;
- narrow event-window exclusions are sensitivity-only and may not define the primary sample;
- unscheduled/unobserved news remains a residual confound.

Add an explicit within-scale disposition for reproducible stable reorganization to a new baseline/state so that failure to return to the old state is not automatically classified as failed stability.

### PD-Q040-7: auditability/documentation cleanup

- add explicit \(\Chi_{\mathrm{arc}}\) refusal tokens such as `ARCHITECTURE_NOT_QUALIFIED` and `ARCHITECTURE_REDUNDANT_WITH_NATIVE`;
- add a one-line \(\chi\) / \(\Chi\) / \(\Chi_{\mathrm{arc}}\) notation glossary;
- fix malformed \(T_{\mathrm{sep},S}^{*}\) and \(F_j\) rendering;
- cross-reference the Stage Q040-3 source/data-identity freeze from the Plan Packet itself;
- freeze the \(T_{\mathrm{sep},S}^{*}\) tolerance and \(\Chi\)-information-loss criterion before any real outcomes.

## 6. Shared-premise challenge

The convergence between Claude, Kimi, and the secondary reviews is useful but not treated as proof.

The most important shared-premise risk is that all reviewers are reasoning from the same representation and comparator vocabulary supplied by the Plan Packets. The revised-plan recheck therefore must attack two questions directly:

1. Can the strongest native/current-state model make the proposed \(\chi\), \(\Chi\), or history layers scientifically unnecessary?
2. Can the same apparent recovery/history effect be generated entirely by measurement timing, baseline/noise migration, correlated omitted state, or sparse-event instability?

NC-R20, strengthened NC-R17, and NC-R21 are the evidence-linked checks that answer those shared-premise attacks prospectively.

## 7. Current checkpoint

`TASK_ID=Q039_Q040_APQ_MEDIATION_2026-09-30`

`AUTHORITATIVE_INPUTS=Q039_PREREG_COMMIT_b757d0dd65a700be1bf1d2cb5233c75c83086308; Q039_HANDOFF_84f4d930ad5b417e9c3b7a8cb1d1c19287d39eb8; Q040_PLAN_COMMIT_84f5c5fa0e6be7ac85593c0d9098334979acdbe1; Q040_HANDOFF_23ea36c5d5a1785581f49f8d461cd11900d68d4d; CLAUDE_FIRST_PASS; KIMI_FIRST_PASS; TWO_UNIQUE_SECONDARY_FIRST_PASSES`

`COMPLETED_VERIFIED_STATE=isolated primary first passes complete; secondary first passes frozen; objections mediated; prospective Plan Delta drafted`

`OPEN_ISSUES=PI sign-off on Q040 primary history extension and primary scoring metric; exact Q039 physical-cone projection/fallback implementation; revised-plan second pass`

`NEXT_EXACT_ACTION=freeze PI choices -> write Q039 v0.5 and Q040 v0.6 Plan Deltas -> targeted revised-plan recheck -> qualified plan freeze -> synthetic qualification -> only then real outcome exposure`

`SAFE_RESUME_POINT=this document`

`SCIENTIFIC_STATE_CHANGED=YES`

## 8. Execution hold

No real Q039 NC7 or Q040 outcome should be opened yet.

The APQ first-pass stage is complete. The current active stage is:

**Evidence Resolution -> Plan Revision**

The next scientific action is not another broad first-pass review. It is the smallest prospective revision above followed by a bounded revised-plan recheck.
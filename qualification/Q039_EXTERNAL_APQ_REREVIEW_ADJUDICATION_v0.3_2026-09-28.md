# Q039 External APQ Re-Review Adjudication v0.3

Date: 2026-09-28
Governance: SymC GOM v1.0
Reviewed preregistration commit: `fde9121072694338c5c097984e6a417a993fee3a`
External reviewer: Kimi, isolated adversarial re-review
External return filename: `Q039_APQ_EXTERNAL_REREVIEW_RETURN_2026-09-28.md`
External return SHA-256: `2ee28a05ee5f6723be5d98e51cdd6af37ef8e14d8795a554861620d45abf9e59`
External disposition: `APQ_EXTERNAL_STATUS=REVISE`

## Adjudication rule

Objections are resolved by mathematical and methodological validity, not reviewer vote. No real Q039 outcome has been opened for this adjudication. Q038 June 9-11 remains prohibited for Q039 tuning.

## R1: persistent non-calendar common-mode can earn top Layer-R status

**Reviewer severity:** MATERIAL  
**Adjudication:** ACCEPTED MATERIAL.

The objection is valid. The v0.3 phase adjustment challenges low-order calendar structure, while the matched same-sign random-direction family asks whether the canonical direction is more concentrated than random same-sign directions. Neither control excludes a persistent one-factor or two-factor non-calendar common-mode world aligned with the canonical semantic directions. The reviewer supplied a synthetic NC8b demonstration in which such a world earns `STRUCTURE_SPECIFIC_PAIR_COHERENT_P0D`.

### Required v0.4 correction

1. Add NC8b as a frozen known-truth world. It must not earn `STRUCTURE_SPECIFIC_PAIR_COHERENT_P0D`.
2. For every canonical direction and for both ordinary and phase-adjusted PCA, decompose fixed-k capture:
   [
   C_6(b)=sum_{j=1}^{6} |u_j^T b|^2.
   ]
   Define the largest single-PC share:
   [
   ho_1(b)=rac{max_{1le jle 6}|u_j^T b|^2}{C_6(b)}
   ]
   when (C_6(b)>0).
3. A direction is `COMMON_MODE_DOMINATED` when (ho_1>0.80) on at least 4/5 architecture-development days in ordinary analysis and independently on at least 4/5 days in phase-adjusted analysis.
4. `COMMON_MODE_DOMINATED` directions cannot earn structure-specific status and are demoted to `CANONICAL_CAPTURE_ONLY_P0D`.
5. The structural claim is narrowed to "structure-specific under the frozen calendar, matched-family, heavy-tail, and single-PC-dominance challenges." No claim of generic common-mode exclusion is permitted beyond those controls.

The 0.80 threshold is externally proposed, outcome-independent with respect to Q039 real data, and frozen prospectively for synthetic qualification before any real outcome exposure.

## R2: matched-percentile ambiguity

**Reviewer severity:** MINOR  
**Adjudication:** ACCEPTED.

v0.4 will require matched-family percentile >0.95 on at least 4/5 days **separately in both ordinary and phase-adjusted analyses** for every lineage and functional direction.

## R3: condition-number exclusions may concentrate by time of day

**Reviewer severity:** MINOR  
**Adjudication:** ACCEPTED REPORTING REQUIREMENT.

v0.4 will predeclare reporting of excluded refits by UTC hour, pair, and day, plus the exact number of invalid pair-days. No exclusion threshold changes.

## R4: NC7 isotropic-amplitude null is lenient

**Reviewer severity:** MINOR  
**Adjudication:** ACCEPTED AS LIMITATION; NULL DEFINITION RETAINED.

Changing NC7 amplitudes after the current review would broaden the null beyond the prospectively frozen measurement-timing question. v0.4 retains the exact update-timing isotropic-state null, labels it explicitly as a timing/carry-forward artifact screen rather than a full amplitude-matched market null, and states that its leniency cannot strengthen a positive claim.

## R5: factor-2 fine-native activity omits signed-volume contrast

**Reviewer severity:** MINOR  
**Adjudication:** ACCEPTED.

v0.4 A2 adds the child2-minus-child1 signed-log signed-trade-volume contrast. The dynamic (n_{train}ge5p_{max}) rule automatically absorbs the resulting parameter-count change.

## R6: Layer-R multiplicity

**Reviewer severity:** MINOR  
**Adjudication:** ACCEPTED DISCLOSURE.

Layer R is a descriptor/coherence layer. Its 4/5-day rules are not familywise-error-controlled hypothesis tests. v0.4 will say this explicitly.

## Independent audit of the delivered reviewer harness

The supplied `q039_known_truth_harness_v1.1.py` and result file are useful adversarial diagnostics but are **not accepted as the canonical Q039 implementation qualification**.

Two implementation issues were identified during local source audit:

1. The harness computes matched-family percentiles only for the lineage symmetric/imbalance directions. In `pct_coh(key)`, functional keys use the raw capture field rather than a functional matched-family percentile. This does not implement the intended v0.3 requirement for both lineage and functional readings.
2. The NC6 gate is set to `True` unconditionally, while the delivered result reports zero ordinary/winsorized verdict flips at every scale. The run therefore demonstrates execution/reporting but does not itself prove a discriminating NC6 known-truth gate.

These findings do not invalidate the reviewer's R1 demonstration. They prevent the external harness from being treated as the final conformant implementation proof.

External harness SHA-256: `503811cebffe9fc0baecc3ece3ea6c68719f59692c271cbf4af20dda4c1e207b`  
External result SHA-256: `b0cfa0c2b446f16f2b09cff02337481f6466b6b0298925a83c52a430d480a619`

## Disposition

The external `REVISE` disposition is accepted.

Q039 v0.3 is superseded for future execution by a v0.4 candidate incorporating R1-R6 and the implementation clarifications above. Because R1 is material, v0.4 requires a new preregistration identity and external re-binding. Real Q039 outcomes remain closed.

Status: `REVISE_ACCEPTED_V0_4_REQUIRED`.

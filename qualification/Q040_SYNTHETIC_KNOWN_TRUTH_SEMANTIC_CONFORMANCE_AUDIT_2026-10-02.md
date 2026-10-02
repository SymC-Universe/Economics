# Q040 Synthetic Known-Truth Semantic Conformance Audit
**Date:** 2026-10-02
**Higher authority:** `qualification/Q040_RECOVERABILITY_PLAN_PACKET_v0.6_2026-09-30.md`
**Audited manifest:** `qualification/Q040_SYNTHETIC_KNOWN_TRUTH_MANIFEST_v0.1_2026-09-30.json`
**Audited generator:** `market_chi/q040_synthetic_generators_v0_1.py`
**Real Q040 outcomes opened:** NO
**Disposition:** MATERIAL SYNTHETIC-LINEAGE DEFECT; PROSPECTIVE REPAIR REQUIRED

## Finding

The v0.1 manifest/generator passed its own invariant checks, but several invariant definitions do not match the scientific known truths required by Q040 Plan Packet v0.6. Generator-contract PASS therefore proved internal consistency, not semantic conformance to the higher plan authority.

### NC-R2 / NC-R3 numbering and truth mismatch

Plan v0.6 requires:

- NC-R2: clustered shocks/self-excitation with unchanged recovery law; native clustering controls must absorb the apparent slowing.
- NC-R3: true cumulative-load degradation; history must add in the erosion direction.

Manifest v0.1 instead encoded:

- NC-R2: true erosion.
- NC-R3: generic false-positive null.

The required clustered-shock control was absent.

### NC-R6 direction-asymmetric history mismatch

Plan v0.6 requires a history effect whose direction differs by perturbation sign.

The current generator changes recovery rate by sign but does not make the history effect itself sign-dependent.

### NC-R10 within-scale-positive / cross-scale-null mismatch

Plan v0.6 requires within-scale history to exist while slower-scale propagation remains absent.

The current NC-R10 generator makes the slower target null but leaves the within-scale recovery law memoryless.

### NC-R17 latent-regime clustering mismatch

Plan v0.6 requires one latent regime to jointly change shock clustering, baseline motion, and recovery duration.

The current generator changes baseline/rate and exposes a shock-intensity proxy, but the common observation bridge supplies a periodic default shock train. The regime therefore does not actually control event clustering.

### NC-R17b omitted-covariate history mismatch

The omitted covariate must drive both apparent perturbation history and recovery duration. The current generator creates an `apparent_history` proxy correlated with the omitted covariate, but the actual injected perturbation history remains periodic under the common bridge.

### NC-R19 common-regime pseudo-propagation weakness

The current fast-history proxy and slower target share a regime, but the actual perturbation-history stream used by Q040-W/Q040-H is not regime-driven. This weakens the intended pseudo-propagation challenge.

### NC-R21 sparse-tail implementation mismatch

The manifest declares fewer than 10 qualifying episodes in a required history stratum, but the common observation bridge currently receives the ordinary periodic event train. The sparse-support refusal is metadata-only rather than guaranteed by the event stream.

## Controls without a material semantic mismatch in this audit

NC-R1, R4, R5, R7, R8, R9, R11, R12, R13, R14, R15, R16, R18, and R20 remain consistent with their Plan v0.6 roles at the present synthetic-contract level.

They remain subject to full estimator qualification.

## Required repair

Create a v0.2 synthetic manifest and generator lineage with:

1. NC-R2 restored as clustered/self-exciting perturbations with a constant local recovery law.
2. NC-R3 restored as true cumulative-load erosion.
3. NC-R6 given a sign × history interaction in the true restoring law.
4. NC-R10 given true within-scale history dependence while its slower target remains independent.
5. NC-R17 perturbation timing made regime-dependent in addition to baseline/rate dependence.
6. NC-R17b perturbation timing made dependent on the deliberately withheld native covariate.
7. NC-R19 perturbation-history timing made dependent on the shared regime that also drives the slower target.
8. NC-R21 given an event stream that guarantees the frozen sparse-support refusal condition.

The repaired controls must be frozen before their outcomes are rerun.

## Consequence for completed synthetic work

The completed Q040 observation/episode contract remains structurally valid as an interface, but its scientific qualification result is superseded for the repaired control set.

After v0.2 generator freeze:
- rerun generator-contract qualification;
- rerun the 180-world observation/episode preflight under v0.2 semantics;
- only then resume estimator selection.

No real-data gate is opened by this repair.

`Q040_SYNTHETIC_SEMANTIC_CONFORMANCE=FAIL_V0_1`

`Q040_REAL_OUTCOMES=SEALED`

`NEXT=FREEZE_V0_2_KNOWN_TRUTH_LINEAGE_AND_REQUALIFY`

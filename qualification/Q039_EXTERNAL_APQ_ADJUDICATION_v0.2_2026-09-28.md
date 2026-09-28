# Q039 External APQ Adjudication: Preregistration v0.2

Date: 2026-09-28
Governance: SymC GOM v0.8.8
Reviewed preregistration: `32efaa69879131889965d71ab799d42e7d291548`
Status: **REVISE. REAL Q039 DATA REMAIN CLOSED.**

## Review corpus

The external review set contains:

1. A structured external APQ return with `APQ_EXTERNAL_STATUS=REVISE`.
2. A stricter static APQ return with `APQ_EXTERNAL_STATUS=BLOCKED`.
3. A Kimi isolated APQ review with independent synthetic reimplementation, `APQ_EXTERNAL_STATUS=REVISE`.
4. A non-adjudicative tool/schema response. This is useful engineering input but is not counted as an APQ disposition because it did not return the required status/binding footer.

Uploaded artifact SHA-256 values:
- engineering/known-truth code text: `865e73129731244162a08c847fc493eb44f48b323705ff878d078e4bad0b4921`
- external REVISE return: `9aae2f35163ea4660cd74549d9e2b9e1cb2c56059cd99bc904c3d0405af7c62d`
- external BLOCKED return: `2b232a8eca1ee144f90a34d6973f1fb026ae5aff90db02143a5481d1cf0fd57f`
- Kimi review bundle: `b350247e6c545abed8748c20ca75ed6b7aa461ac68142c7b1c8085014284bfc2`
- Kimi harness: `dab789625bc2bcf730abdceffd62de963ef5d556dc3df0df3fcdb3d4d2912118`
- Kimi result JSON: `80f0d6599c9e23140a3d74ef41165fec877e42733821876b58250ac3a3a9f57b`
- Kimi review: `1429c797c00d77936f60d38083ff34226bb19dca729629457e72382798506656`

The Kimi harness was rerun locally without market data. It exited 0 and reproduced NC1-NC5, the isotropic null calibration, the seasonality-only null failure, and the moderate-effect 60->300 power limitation.

## Adjudication rule

Objections are resolved by mathematical validity, synthetic discrimination, and claim discipline. Reviewer vote count is not used.

## Objection dispositions

### A. Commit-hash ambiguity

External BLOCKED review claimed the package contained inconsistent preregistration hashes.

**Disposition: REJECTED AS REVIEWER TRANSCRIPTION ERROR.**

A direct audit of every packaged review file found the canonical preregistration hash consistently recorded as:

`32efaa69879131889965d71ab799d42e7d291548`

The malformed hashes occur in the reviewer return itself, not in the package. No scientific revision is required. The v0.3 review package will nevertheless repeat the canonical binding prominently.

### B. Beta(3,7) threshold applied to Core6

The BLOCKED review correctly notes that `min(C6_sym,C6_imb)` is not itself Beta(3,7).

**Disposition: PARTLY ACCEPTED.**

The v0.2 decision `Core6 > q95` is mathematically equivalent to requiring **both** individual captures to exceed the single-direction Beta(3,7) q95. It was therefore conservative, not an invalid joint test. However, calling q95 an "exact Core6 null" would be incorrect.

v0.3 will:
- apply Beta(3,7) q95 separately to `C6_sym` and `C6_imb`;
- retain `Core6=min(...)` only as a descriptive shorthand;
- add structured and phase-adjusted nulls because isotropic orientation is not the scientifically strongest competing explanation.

### C. Generic common-mode / Perron-Frobenius / seasonality null

Two reviews independently argue that symmetric-depth capture can be high under generic positive cross-level covariance or calendar structure. Kimi's seasonality-only known-truth world qualified at rate 1.0 under the v0.2 Layer-R rule.

**Disposition: ACCEPTED, MATERIAL.**

v0.3 adds:
1. phase-adjusted residual Layer R;
2. matched-structure random-direction controls for the positive symmetric and bid/ask-antisymmetric sign families;
3. a stronger structural status that cannot be earned from isotropic capture alone.

### D. Canonical direction coordinate-system ambiguity

The BLOCKED review correctly distinguishes raw log-depth functionals from directions in standardized PCA coordinates.

**Disposition: ACCEPTED, MATERIAL.**

v0.3 explicitly separates:
- the Q037/Q038 **standardized-coordinate lineage direction**;
- the covector-consistent image of the raw semantic functional, `normalize(sigma * b_raw)`.

Both are reported. Architecture-bridge language requires agreement.

### E. Carry-forward / staleness / activity confounding

Multiple reviews identify state carry-forward as a potential structure-manufacturing channel, especially in thin overnight periods.

**Disposition: ACCEPTED, MATERIAL.**

v0.3:
- preserves carry-forward because an unchanged book is still the standing book state;
- adds update fraction and staleness to the native comparator;
- adds fine-native activity/staleness structure before semantic fine features;
- adds NC7, a matched-update-timing carry-forward null using observed update times but randomized book states;
- forbids semantic-specific language if the matched-density null or fine-native comparator explains the effect.

### F. 300 s OLS identification/power

Two static reviews and the independent Kimi known-truth harness converge on inadequate early identification under the five-hour burn-in.

**Disposition: ACCEPTED, MATERIAL.**

v0.3 replaces the fixed five-hour-only rule with:
`first refit when both elapsed training >= 5 h and n_train >= 5 * p_max`
where `p_max` includes the intercept and is the parameter count of the largest model in that pair. At least eight wall-clock hours of OOS evaluation must remain.

This rule is applied identically to every nested model within a pair.

### G. SUBTRACTS semantics / scale-dependent power

The Kimi harness shows that a true zero-information world can produce a tiny but statistically resolved negative loss difference at 15->30 due to ordinary estimation cost of a nested larger model.

**Disposition: ACCEPTED, BUT RESOLVED DIFFERENTLY THAN PROPOSED.**

v0.3 does **not** introduce an arbitrary practical-effect epsilon.

Instead:
- `SUBTRACTS_P0D` is retired as a primary scientific classification;
- negative OOS penalties remain reported honestly as descriptive values;
- the primary question becomes one-sided incremental gain;
- Clark-West-style adjusted nested-model contrasts are reported as a predeclared diagnostic of parameter-estimation penalty;
- cross-scale pair labels are never ranked against one another.

This removes the false semantic implication that a tiny estimation penalty proves active negative information.

### H. Factor-2 interpretation

Factor-2 contrast is algebraically equivalent to the last fine semantic state conditional on the parent mean.

**Disposition: ACCEPTED.**

v0.3 renames the positive classification:
`LAST_FAST_SEMANTIC_ADDS_P0D`

No "path" or higher-order organization language is permitted at 15->30 or 30->60.

### I. P60_300 multiplicity and ambiguous intermediate label

The BLOCKED review correctly notes that `FINE_VARIABILITY_OR_LAST_ONLY_P0D` was underdefined. The multiplicity objection can be simplified by changing the nesting.

**Disposition: ACCEPTED, REDESIGNED.**

v0.3 uses:
- `A`: coarse context + fine native activity/staleness structure;
- `L`: A + last fine semantic state;
- `U`: L + semantic dispersion;
- `S`: U + semantic slope.

The familywise primary P60_300 test is `A -> S`.

Conditional ordered-path characterization is `U -> S`, the immediate nested test that isolates semantic slope. `L -> U` and `A -> L` are descriptive decomposition steps.

The ambiguous `FINE_VARIABILITY_OR_LAST_ONLY_P0D` label is retired. If A->S passes but U->S does not, use:
`FINE_SEMANTIC_INFO_ADDS_ORDER_NOT_RESOLVED_P0D`.

### J. Day-stratified bootstrap pooling and circular wrapping

Reviews identify both unspecified pooling and artificial 21:00->00:00 wrapping.

**Disposition: ACCEPTED.**

v0.3:
- uses non-circular moving blocks;
- resamples independently within each day;
- computes a mean contrast within each resampled day;
- combines the five day means with equal day weights;
- uses percentile intervals;
- keeps 1 h primary, 30 min and 2 h sensitivities.

### K. Full-day Layer R gating Layer L

The BLOCKED review identifies interpretive gating by a full-day structural analysis.

**Disposition: ACCEPTED.**

v0.3 decouples the layers:
- Layer R is a full-development-day structural descriptor;
- Layer L is a strictly walk-forward predictive experiment;
- Layer R cannot authorize, veto, rescue, or relabel the Layer-L primary classification;
- the final structural/predictive map is a mechanically generated Cartesian combination after both result objects are frozen.

No "inheritance" classification exists in v0.3.

### L. 4-of-5 days as replication

The architecture-development days are not independent replication.

**Disposition: ACCEPTED.**

v0.3 calls 4/5 a **development-day coherence criterion**, never replication. P1 requires new untouched evidence.

### M. Winsorization disagreement rule, NC5 count/rule, MAE scope

**Disposition: ACCEPTED, MECHANICAL.**

v0.3 fixes:
- exact disagreement rule;
- fixed permutation count/seed and order-specificity rule;
- pooled-OOS MAE gate with day-specific MAE reported.

### N. Prior-art delta table

**Disposition: ACCEPTED.**

v0.3 adds a direct delta table against Golub et al., Elomari-Kessab et al., Eisler et al., Corradi et al., Cont et al., HLOB/Briola et al., and Zhang/Zohren multi-horizon forecasting.

## Current gate

The external v0.2 review objective has succeeded: it found material pre-outcome weaknesses.

No Q039 real-data execution is authorized.

Next:
1. issue full preregistration v0.3 with these resolutions;
2. bind a new external APQ packet to the exact v0.3 commit;
3. build/requalify a v0.3 synthetic harness;
4. return v0.3 to external cognitions;
5. freeze only after remaining BLOCKER/MATERIAL objections are resolved.

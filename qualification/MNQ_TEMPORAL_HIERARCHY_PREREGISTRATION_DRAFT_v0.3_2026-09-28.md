# MNQ Temporal Hierarchy Preregistration Draft v0.3

Date: 2026-09-28
Governance: SymC GOM v0.8.8
Stage: P0-D development preregistration
Status: APQ-REVISED, NOT YET EXTERNALLY REQUALIFIED
Supersedes: v0.2
External adjudication: `qualification/Q039_EXTERNAL_APQ_ADJUDICATION_v0.2_2026-09-28.md`

## 1. Purpose

This preregistration asks two separate questions about the previously qualified MNQ L10 semantic architecture across fixed wall-clock scales:

1. **Structural question:** do the predeclared symmetric-depth and bid-ask-imbalance semantic directions remain specifically represented across 15 s, 30 s, 60 s, and 300 s embeddings after generic calendar/common-mode alternatives are challenged?
2. **Lagged-information question:** does fine semantic state add strictly out-of-sample information about the next coarse semantic state beyond coarse persistence, current native context, and fine native activity/staleness structure?

The two layers are adjudicated independently. Neither can rescue, authorize, veto, or relabel the other.

No causal, physical-inheritance, trading, scalar-chi, or market-wide claim is tested here.

## 2. Evidence class and firewall

Evidence class: P0-D development.

Allowed dates:
- 2026-05-27
- 2026-05-28
- 2026-05-29
- 2026-06-01
- 2026-06-02

Session:
- 00:00:00 through 21:00:00 UTC
- ordinary wall-clock time
- no business-time or activity-time rescaling

Q038 dates 2026-06-09 through 2026-06-11 are prohibited from feature, threshold, model, scale, lead, null, sensitivity, and claim tuning.

The five allowed dates are **architecture-development days**. Cross-day consistency on them is a development-day coherence check, not independent replication.

No Q039 real-data outcome may be opened until:
- this v0.3 plan passes external APQ requalification;
- implementation matches the frozen plan;
- known-truth and null controls pass;
- source identity and hashes are frozen.

## 3. Prior-art boundary

The following are not novelty claims:
- LOB state and order flow can predict short-horizon outcomes;
- deeper book levels can add information;
- multi-horizon LOB forecasting exists;
- symmetric and antisymmetric microstructure modes exist;
- PCA/modal structure can persist or reorganize with scale;
- multiscale liquidity and multiscale information flow exist;
- aggregation/filtering can alter inferred dependence;
- functional/factor models forecast LOB curves.

The residual question is narrower:

> Does a predeclared two-direction L10 semantic state show structure-specific cross-scale representation and semantic-specific fine-to-coarse incremental predictability under fixed wall-clock embeddings after coarse persistence, native flow/activity, update staleness, generic common-mode/calendar structure, and nested-model estimation cost are explicitly challenged?

### 3.1 Prior-art delta table

| Prior work | Already established | What Q039 does differently |
| --- | --- | --- |
| Golub et al., multiscale liquidity | multiscale representation and predictive information can be separated | fixed adjacent 15/30/60/300 s L10 semantic directions plus explicit nested coarse/fine controls |
| Elomari-Kessab et al., Microstructure Modes | symmetric/antisymmetric modes and temporal predictability; semantics can persist under coarse-graining | freezes a previously qualified semantic pair, separates lineage-pattern capture from raw-functional bridge, and tests future coarse semantic state |
| Eisler, Kertesz & Lillo | qualitative LOB mechanism changes with time scale | allows scale-local structural refusal rather than presuming invariance |
| Corradi, Zaccaria & Pietronero | liquidity-fragility mechanisms change across horizons | distinguishes structural state description from semantic-specific incremental forecasting |
| Cont, Kukanov & Stoikov | OFI/impact relation remains robust over aggregation intervals | tests lagged fine-to-future-coarse state, not contemporaneous aggregation robustness |
| Briola, Bartolucci & Aste, HLOB | information structure/persistence degrades across prediction horizons in learned LOB representations | uses fixed interpretable semantic coordinates and adversarial native/staleness comparators rather than learned black-box features |
| Zhang & Zohren, multi-horizon LOB forecasting | future paths can be forecast jointly over multiple horizons | Q039 is an adjacent-scale state-transfer experiment with fixed semantics and explicit aggregation/confound controls |

The table defines the current residual target. It does not prove novelty.

## 4. Fixed hierarchy

Scales:
- 15 s
- 30 s
- 60 s
- 300 s

Adjacent primary pairs:
- P15_30
- P30_60
- P60_300

Primary lead:
- exactly one future coarse block

Secondary descriptive leads, only after all lead-1 primary objects are frozen:
- lead 2
- lead 3

No new scale or lead can become primary after outcome exposure.

## 5. Source state and carry-forward

### 5.1 L10 state lineage

Use validated MBP10 v2 feature files.

Coordinate order:
`bid_00, ask_00, bid_01, ask_01, ..., bid_09, ask_09`.

Use L10 `*_last` size state fields.

Within a day:
- accept only finite nonnegative valid L10 states;
- carry the last valid book state forward through seconds without a valid new book update;
- never backfill before the first valid state;
- never carry across the session/day boundary;
- bad update rows do not replace the last valid state.

Carry-forward is treated as a measurement convention that must itself be challenged, not as a neutral assumption.

### 5.2 Update/staleness state

For every second derive:
- `l10_update_indicator`: 1 when a new valid L10 state is observed at that second, otherwise 0;
- `staleness_age_s`: elapsed seconds since the most recent valid L10 update.

These variables are predeclared controls.

### 5.3 Transform

For each valid/carried state:
[
x_t = \log(1 + \mathrm{L10Size}_t)
]

coordinate-wise.

Temporal aggregation occurs after this transform.

## 6. Canonical semantic objects

Raw-space unit vectors:
- `b_sym_raw`: equal positive weights on all 20 coordinates;
- `b_imb_raw`: alternating positive bid / negative ask weights.

Layer-L raw semantic state:
[
D_t = b_{sym,raw}^T x_t,
qquad
I_t = b_{imb,raw}^T x_t.
]

Layer R distinguishes two coordinate meanings.

### 6.1 Standardized lineage directions

`b_sym_lineage` and `b_imb_lineage` are the same equal-weight sign patterns in standardized coordinate space used by the Q037/Q038 modal lineage.

### 6.2 Covector-consistent raw-functional directions

If a day/scale block matrix has coordinate standard deviations (sigma), then the raw functional (b_{raw}^T x) is represented in standardized coordinates by:

[
b_{functional,z} =
\frac{sigma \odot b_{raw}}
{\|\sigma \odot b_{raw}\|}.
]

Layer R reports both lineage capture and functional capture. They are not silently treated as the same vector.

## 7. Layer R: structural representation descriptor

Layer R is computed on full development days and is **not** a predictive gate for Layer L.

### 7.1 Block state

For each day and scale S:
- partition 00:00-21:00 UTC into non-overlapping S-second blocks;
- average the 20-dimensional one-second log-depth state within each block;
- report block update fraction and staleness diagnostics;
- refuse a block if no valid state has yet appeared in the day.

### 7.2 PCA

For each day x scale:
- coordinate-wise population standardization;
- refuse constant/non-finite coordinates;
- full SVD/PCA;
- fixed k=6;
- no adaptive k.

Report:
- `C6_sym_lineage`, `C6_imb_lineage`;
- `C6_sym_functional`, `C6_imb_functional`;
- `Core6_*` as descriptive minima only;
- strongest PC rank/alignment;
- full spectrum and effective rank;
- adjacent-scale k=6 principal cosines.

### 7.3 Isotropic single-direction benchmark

For one fixed unit direction in d=20 and a Haar-random rank-6 subspace:

[
C_6 \sim \mathrm{Beta}(3,7)
]

with:
[
q_{.95}=0.5496416495066101.
]

This q95 applies **separately to each canonical direction**.

No claim is made that `Core6=min(C6_sym,C6_imb)` itself follows Beta(3,7).

### 7.4 Heavy-tail sensitivity

Repeat Layer R after coordinate-wise 1st/99th percentile winsorization before standardization.

A heavy-tail disagreement occurs if either canonical direction changes its above/below-q95 coherence verdict between ordinary and winsorized analysis.

### 7.5 Phase-adjusted sensitivity

For each day/scale and coordinate, regress the block series on:
- intercept;
- sin/cos first session harmonic;
- sin/cos second session harmonic.

Run the same standardized k=6 PCA on residuals.

This tests whether calendar structure alone explains canonical capture.

### 7.6 Matched-structure random-direction null

For each day/scale, ordinary and phase-adjusted top-6 subspaces are compared with M=5000 frozen-seed control directions.

Seed:
- 20260930 + scale_seconds

Symmetric family:
- draw 20 iid Exp(1) positive weights;
- normalize to unit length.

Imbalance family:
- preserve bid-positive / ask-negative sign assignment;
- draw iid Exp(1) magnitudes;
- normalize to unit length.

For each canonical direction report its percentile within the matched-family capture distribution.

### 7.7 Layer-R statuses

A direction has `ISOTROPIC_CAPTURE_COHERENT_P0D` when:
- it exceeds Beta q95 on at least 4/5 architecture-development days;
- its five-day median exceeds q95;
- the same is true under winsorization.

A direction has `STRUCTURE_SPECIFIC_CAPTURE_COHERENT_P0D` when, in addition:
- phase-adjusted capture exceeds Beta q95 on at least 4/5 days with median > q95;
- matched-structure percentile exceeds 0.95 on at least 4/5 days.

The semantic pair has `STRUCTURE_SPECIFIC_PAIR_COHERENT_P0D` only when both symmetric and imbalance directions satisfy the structure-specific rule for:
- standardized lineage directions;
- covector-consistent functional directions.

Otherwise report exactly which layer failed:
- isotropic capture unresolved;
- heavy-tail sensitivity unresolved;
- phase-adjusted unresolved;
- matched-structure specificity unresolved;
- lineage/functional bridge unresolved.

These are development-day structural descriptors, not replication claims.

## 8. NC7 carry-forward matched-timing null

Before any semantic-specific claim, run a matched-update-timing null.

For each real development day:
- preserve the exact valid L10 update timestamps;
- generate iid isotropic 20-dimensional update states independent across updates;
- carry them forward using the exact preregistered state rule;
- preserve the real update timing but not real book values or targets.

Generate 200 null worlds with seed 20261001.

Apply:
- Layer R structural summaries;
- Layer L primary point contrasts without using real semantic values.

Report real statistics relative to the NC7 distributions.

If a claimed real effect does not exceed the 95th percentile of the relevant NC7 null:
- append `CARRY_FORWARD_ARTIFACT_NOT_EXCLUDED`;
- do not use semantic-specific structural or fine-information language for that result.

NC7 cannot rescue a failed primary test.

## 9. Layer L: lagged incremental information

Layer L is strictly walk-forward.

### 9.1 Target

For each pair, target:
- raw semantic state ((D,I)) of the next non-overlapping coarse block.

Lead zero is forbidden.

### 9.2 Coarse native comparator N

For each current coarse block, N contains:

Semantic persistence:
- current coarse D, I;
- previous coarse D, I.

Session phase:
- sin/cos first harmonic;
- sin/cos second harmonic.

Current coarse native context:
- log1p event rows;
- log1p trade volume;
- signed-log1p signed trade volume;
- mean spread;
- mean signed microprice offset;
- mean native L10 imbalance.

Carry-forward controls:
- mean L10 staleness age;
- maximum L10 staleness age;
- L10 update fraction.

All non-cyclic continuous predictors are standardized on training data only at each refit.

## 10. Factor-2 pairs: P15_30 and P30_60

Each parent has exactly two fine children.

Let:
[
Delta z = z_2-z_1.
]

Conditional on the parent mean, (Delta z) is algebraically equivalent to the last fine semantic state. Therefore no higher-order path claim is permitted.

### 10.1 Fine-native comparator A2

A2 contains all N predictors plus, from fine-child update/activity state:
- last-child log event rows;
- child2-child1 log event-row contrast;
- last-child L10 update fraction;
- child2-child1 update-fraction contrast.

### 10.2 Semantic model F2

F2 contains A2 plus:
- Delta D;
- Delta I.

Primary contrast:
[
Delta L_{A2,F2}=L_{A2}-L_{F2}.
]

Positive values favor added last-fast semantic information beyond fine native activity/update timing.

## 11. Factor-5 pair: P60_300

Each 300 s parent has five 60 s children.

### 11.1 Fine-native activity model A

A contains all N predictors plus, across the five child blocks:

For log event rows:
- last child;
- child standard deviation;
- child least-squares slope versus wall-clock child position.

For L10 update fraction:
- last child;
- child standard deviation;
- child least-squares slope.

A is the strong fine-native comparator.

### 11.2 Semantic nesting

L:
- A + last child D/I.

U:
- L + child SD of D/I.

S:
- U + child least-squares slope of D/I.

Primary pair contrast:
[
Delta L_{A,S}=L_A-L_S.
]

Ordered-semantic-path characterization:
[
Delta L_{U,S}=L_U-L_S.
]

The descriptive decomposition also reports:
- A->L;
- L->U;
- L->S;
- N->A;
- N->S.

Only A->S belongs to the three-pair primary family.

## 12. Model class and identification

All models:
- OLS with intercept;
- no tuned regularization;
- no feature search;
- no PCA-score predictors;
- no price-return or trading target.

For each pair let `p_max` be the total parameter count, **including the intercept**, of the largest model used for that pair.

First walk-forward refit occurs only when both are satisfied:
1. elapsed training history >= 5 wall-clock hours;
2. `n_train >= 5 * p_max`.

The same first-refit boundary is used for all nested models within that pair.

At least 8 wall-clock hours of eligible OOS evaluation must remain. Otherwise:
`INVALID_TEST_INSUFFICIENT_IDENTIFICATION`.

At every refit report:
- matrix rank;
- condition number;
- training n;
- p;
- n/p.

Rank deficiency is a refusal for that refit, not silently repaired by dropping predictors.

A refit with condition number > 1e8 is flagged `NUMERICALLY_ILL_CONDITIONED`; its predictions are retained only descriptively and excluded from primary aggregation. If excluding such chunks leaves <8 OOS hours, the pair/day is invalid.

## 13. Walk-forward firewall

Evaluation is separate by day.

At each hourly test chunk:
- training expands through past data only;
- a training observation is eligible only if its target block ends at or before the first source timestamp of the test chunk;
- no overnight fitting;
- no test target enters preprocessing or scaling;
- all predictor means/SDs and target SDs are training-only.

## 14. Loss and diagnostics

At each refit, target D/I errors are divided by training-only target SD.

Joint loss:
[
L=0.5(e_D^2+e_I^2).
]

Report:
- joint loss;
- D and I MAE;
- D and I R2;
- per-day and pooled values;
- raw nested loss contrast.

Pooled MAE gates use all eligible OOS observations across the five development days. Day-specific MAEs are also reported.

### 14.1 Clark-West diagnostic

For every nested comparison, report the Clark-West-style adjusted squared-error contrast that adds back the squared prediction difference between the smaller and larger model.

This diagnostic addresses known nested-model estimation-cost bias.

It is not allowed to rescue a failed raw OOS gain test.

## 15. Dependence-aware uncertainty

Use a **non-circular** moving-block bootstrap.

Within each day:
- block starts are sampled uniformly from valid contiguous start positions;
- blocks never wrap across the 21:00->00:00 boundary;
- sampled blocks are concatenated until the day's original OOS length is reached, then truncated.

Across days:
- compute one mean contrast per resampled day;
- combine the five day means with **equal day weights**.

Interval:
- percentile bootstrap.

Replicates:
- 10,000.

Seed:
- 20260929.

Primary block length:
- 1 wall-clock hour.

Sensitivity block lengths:
- 30 minutes;
- 2 hours.

## 16. Multiplicity and primary family

The three primary pair hypotheses are:
1. P15_30: A2->F2;
2. P30_60: A2->F2;
3. P60_300: A->S.

Each uses a two-sided 98.333% percentile interval, corresponding to Bonferroni familywise alpha=0.05 across the three pair-level primary questions.

P60_300 ordered-path characterization uses U->S after the A->S primary gate passes.

This is a conditional **intersection-union-style characterization** of the type of fine semantic information, not a fourth primary pair hypothesis.

## 17. Development-day coherence and classification

A positive primary pair classification requires:
- lower 98.333% CI of the raw primary contrast > 0;
- positive primary point contrast on at least 4/5 architecture-development days;
- pooled OOS MAE improves for both D and I;
- corresponding NC7 carry-forward null does not explain the real point contrast at the 95th percentile;
- required known-truth controls pass.

### 17.1 Factor-2 label

If all gates pass:
`LAST_FAST_SEMANTIC_ADDS_P0D`.

If upper 98.333% CI <= 0:
`NO_INCREMENTAL_SEMANTIC_GAIN_DETECTED_P0D`.

Otherwise:
`NEED_MORE_INFO_OR_MIXED_P0D`.

No `SUBTRACTS` primary label exists.

### 17.2 P60_300 label

If A->S passes the primary gates and lower 95% CI for U->S > 0:
`ORDERED_SEMANTIC_PATH_ADDS_P0D`.

If A->S passes but U->S does not:
`FINE_SEMANTIC_INFO_ADDS_ORDER_NOT_RESOLVED_P0D`.

If upper 98.333% CI for A->S <= 0:
`NO_INCREMENTAL_SEMANTIC_GAIN_DETECTED_P0D`.

Otherwise:
`NEED_MORE_INFO_OR_MIXED_P0D`.

A negative raw loss contrast is still reported quantitatively. It is not interpreted as active negative information.

## 18. NC1-NC8 known-truth suite

NC1 phase-only:
- future state determined by session phase;
- semantic fine terms must not classify ADD.

NC2 coarse-sufficient:
- current/previous coarse state sufficient;
- fine semantic terms must not classify ADD.

NC2b latent-regime:
- latent activity regime drives both fine variability and future coarse state with no semantic fine channel;
- fine semantic terms must not classify ADD after native activity controls.

NC3 factor-2 semantic recency:
- target contains incremental Delta D/I information beyond A2;
- factor-2 ADD must be recovered.

NC4 ordered semantic path:
- target contains semantic child slope beyond A/U;
- P60_300 ORDERED label must be recovered at a predeclared moderate synthetic effect.

NC5 order-destroyed:
- P60_300 only;
- preserve child values and last-child position;
- randomly permute the first four children within each parent;
- M=200 permutations;
- seed=20261002;
- compare U->S point contrast.

If true-order U->S does not exceed the 95th percentile of the permutation distribution:
append `ORDER_SPECIFICITY_NOT_RESOLVED`.

NC6 heavy-tail:
- generate heavy-tailed coordinates with no special canonical structure;
- ordinary/winsorized disagreement rule is a verdict flip or an above/below-q95 coherence flip for either canonical direction.

NC7 matched-update-timing carry-forward null:
- defined in Section 8.

NC8 generic two-factor calendar/common-mode world:
- canonical directions driven only by session phase/common-mode factors;
- Layer R may show isotropic capture but must **not** earn the full structure-specific pair status after phase-adjusted and matched-structure controls.

All known-truth/random-null seeds and effect sizes must be frozen in the implementation manifest before execution.

## 19. Layer-R / Layer-L joint map

Only after both result objects are independently frozen, generate a mechanical Cartesian map from fixed statuses.

Layer R axis:
- `STRUCTURE_SPECIFIC_PAIR_COHERENT_P0D`;
- `CANONICAL_CAPTURE_ONLY_P0D`;
- `STRUCTURAL_UNRESOLVED_P0D`.

Layer L axis:
- pair-specific ADD;
- NO_INCREMENTAL_GAIN_DETECTED;
- NEED_MORE_INFO_OR_MIXED.

The map is generated by code from statuses. No hand-assigned narrative cell is permitted.

The map does not use the word "inheritance."

## 20. Failure and outlier discipline

Every failure remains evidence.

Preserve and investigate:
- unusual day effects;
- Layer-R lineage/functional disagreement;
- phase-adjusted failure;
- matched-structure null failure;
- carry-forward null overlap;
- numerical instability;
- invalid chunks/days;
- extreme block-bootstrap influence;
- fine-native comparator absorption of apparent semantic gain;
- rank migration and broader modal reorganization.

Distinguish:
- transport/implementation;
- measurement convention;
- statistical leverage/power;
- genuine market-state behavior;
- representation failure.

No day is excluded because its result is inconvenient.

## 21. Explicit nonclaims

Q039 does not establish:
- causal substrate inheritance;
- physical transmission across scales;
- universal market hierarchy;
- fractality;
- scale invariance;
- scalar chi inheritance;
- event prediction;
- profitable trading;
- cross-instrument transfer;
- market-wide Chi universality;
- independent replication on the five development days.

## 22. P0-D consequence rules

If no pair supports incremental semantic gain:
- retire the current fixed semantic hierarchy as an incremental predictive tool at P0-D;
- retain structural/limit-map findings;
- do not claim the semantic state has no information in principle.

If only some pairs support gain:
- retain a scale-local result;
- refuse universal ladder language.

If one or more pairs support gain:
- report only the exact scale-local development-day result;
- require untouched evidence before P1.

## 23. P1 path

P1 requires new untouched evidence.

Prospective selection rule:
- after final v0.3+ freeze, use the first three chronologically available eligible MNQ trading sessions after 2026-06-11 that are acquired under the same raw MBP10 contract and have not been opened for Q039 outcome inspection.

Dates are chosen by chronological data availability, not by market behavior.

Before P1:
- external APQ fully qualified;
- implementation and hashes frozen;
- P1 data identity frozen before opening;
- P1 analysis executes without retuning.

## 24. Current gate

This v0.3 document is a candidate preregistration.

Real Q039 development data remain closed.

Next required steps:
1. bind external APQ re-review to the exact commit that first introduces this file;
2. implement v0.3 exactly;
3. run NC1-NC8 and null calibration without market outcomes;
4. resolve any new BLOCKER/MATERIAL review objections;
5. freeze final preregistration and implementation;
6. only then open the five Q039 development days.

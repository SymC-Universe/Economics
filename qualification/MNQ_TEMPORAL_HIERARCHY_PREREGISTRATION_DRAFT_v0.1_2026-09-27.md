# MNQ Temporal Hierarchy Preregistration Draft v0.1

Date: 2026-09-27
Governance: SymC GOM v0.8.8
Stage: P0-D development preregistration draft
Status: DRAFT, NOT YET FROZEN
Foundation: `qualification/MNQ_TEMPORAL_HIERARCHY_LITERATURE_HYPOTHESIS_FOUNDATION_2026-09-27.md`

## 1. Purpose

This preregistration tests whether the previously qualified MNQ L10 semantic architecture is preserved, reorganized, lost, or refused across fixed wall-clock temporal embeddings, and whether fine-scale organization contains incremental lagged information about the next coarser semantic state beyond strong native comparators.

The preregistration deliberately separates:

1. **Representation qualification:** is the same semantic architecture licensed at each scale?
2. **Lagged incremental information:** does fine organization add future coarse-state information?
3. **Joint interpretation:** how do preservation, rank migration, reorganization, and predictive gain relate after the first two layers are adjudicated independently?

This is not a generic multiscale prediction experiment.

## 2. Prior-art-constrained claims

The following are treated as established neighboring results and are not novelty claims:
- LOB state and order flow can predict short-horizon outcomes.
- deeper LOB levels can add information beyond top of book;
- high-frequency LOB prediction can operate at multiple horizons;
- low-dimensional/PCA microstructure modes exist;
- bid-ask symmetric and antisymmetric mode families exist;
- modal structure can survive some forms of coarse-graining;
- multiscale information transfer and multiscale Granger causality exist;
- temporal aggregation/filtering can alter or spuriously create apparent causal structure.

Residual target:

> Does an already-qualified, interpretable L10 semantic architecture remain licensed across the fixed 15 s / 30 s / 60 s / 300 s MNQ hierarchy, and does fine organization at each adjacent transition carry incremental lagged information about the next coarser semantic state beyond the already-formed coarse state and native context?

## 3. Evidence class and firewall

This is P0-D development work.

Allowed dates:
- 2026-05-27
- 2026-05-28
- 2026-05-29
- 2026-06-01
- 2026-06-02

Fixed session:
- 00:00:00 through 21:00:00 UTC.

Q038 dates 2026-06-09 through 2026-06-11 are prohibited from:
- feature selection;
- threshold selection;
- model selection;
- scale selection;
- lead selection;
- null selection;
- tuning;
- rescue.

Q038 may motivate only the already-established semantic directions and fixed k=6 representation rule.

No current development result may be promoted to P1.

## 4. Fixed wall-clock hierarchy

Elapsed time remains ordinary physical wall-clock time.

Scales:
- 15 s
- 30 s
- 60 s
- 300 s

Adjacent transitions:
- P15_30: 15 s -> 30 s
- P30_60: 30 s -> 60 s
- P60_300: 60 s -> 300 s

Primary lead:
- one future target coarse block.

Secondary descriptive leads:
- two target coarse blocks;
- three target coarse blocks.

No additional scale or lead may be introduced after primary outcomes are exposed.

## 5. Source representation

### 5.1 Source

Use only validated MBP10 v2 feature files corresponding to the five development dates.

Segment by actual `(instrument_id, symbol)`.

Exactly one mature-session segment must be selected per day under the already-qualified development data contract.

### 5.2 L10 state continuity

Preserve the Q037/Q038 state lineage.

For levels 0 through 9, coordinate order is:

`bid_00, ask_00, bid_01, ask_01, ..., bid_09, ask_09`.

Use the `*_last` L10 size state fields.

Within a day:
- update state only from finite valid L10 state observations;
- carry the last valid state forward through seconds with no book update;
- do not backfill before the first valid state;
- never carry state across a day/session boundary.

An absence of events is not itself treated as missing data.

Bad/invalid update rows do not replace the last valid state.

### 5.3 Log-depth

At each valid second:

[
x_t = log(1 + mathrm{L10Size}_t)
]

coordinate-wise.

Temporal aggregation is performed **after** this transform.

## 6. Canonical semantic coordinates

Fixed canonical unit vectors:
- symmetric depth `b_sym`: equal positive weight on all 20 coordinates;
- bid-ask imbalance `b_imb`: alternating positive bid / negative ask weights.

Native semantic coordinates:

[
D_t = b_{sym}^T x_t,
qquad
I_t = b_{imb}^T x_t.
]

These are fixed coordinates derived from the already-qualified semantic directions. They are not PCA scores and do not require refitting.

## 7. Layer R: representation qualification across scales

Layer R must be adjudicated before any lagged result is interpreted as inheritance of the same semantic architecture.

### 7.1 Scale construction

For each day and each S in {15, 30, 60, 300} s:
- partition 00:00-21:00 UTC into non-overlapping S-second blocks;
- compute each block's 20-dimensional vector as the arithmetic mean of its valid 1-second log-depth states;
- require a defined carried state for every second of the block;
- no interpolation other than the predeclared within-day state carry-forward.

### 7.2 Scale-specific modal decomposition

For each day x scale matrix:
- standardize each of the 20 coordinates within that day/scale using population mean and standard deviation;
- refuse if any coordinate is constant or non-finite;
- compute full SVD/PCA;
- fixed k = 6;
- no adaptive k.

Compute:
- `C6_sym`;
- `C6_imb`;
- `Core6 = min(C6_sym, C6_imb)`;
- strongest PC rank/alignment for each canonical direction;
- adjacent-scale k=6 principal cosines;
- full eigenvalue spectrum and effective rank.

Exact isotropic orientation benchmark:
[
C_6 sim mathrm{Beta}(3,7)
]
under random orientation in d=20.

Frozen q95:
[
q_{.95}=0.5496416495066101.
]

### 7.3 Robust sensitivity

Repeat Layer R after coordinate-wise 1st/99th percentile winsorization within each day/scale before standardization.

This is a robustness sensitivity motivated by heavy-tail concerns in PCA-based liquidity analysis.

### 7.4 Scale qualification

A scale is `SEMANTIC_REPRESENTATION_QUALIFIED` only if:
- ordinary PCA Core6 exceeds q95 on at least 4 of 5 days;
- winsorized-PCA Core6 exceeds q95 on at least 4 of 5 days;
- the median Core6 across five days exceeds q95 in both ordinary and winsorized analyses.

Otherwise:
- `SEMANTIC_REPRESENTATION_NEED_MORE_INFO`.

A change in strongest individual PC rank does not constitute representation failure if fixed-k semantic capture remains qualified.

An adjacent predictive pair may be analyzed numerically when a scale is unqualified, but it may not be interpreted as inheritance of the already-qualified semantic architecture.

## 8. Layer L: lagged incremental information

### 8.1 Coarse target state

For each target scale C:
- compute coarse semantic state as the arithmetic mean of 1-second `D_t, I_t` over the block.

Target:
- semantic state of the next non-overlapping coarse block.

Lead zero is forbidden.

### 8.2 Native coarse-context comparator N

For every current coarse block, fixed predictors are:

Semantic/context:
- current coarse D;
- current coarse I;
- session phase sin(2*pi*p);
- session phase cos(2*pi*p);
- session phase sin(4*pi*p);
- session phase cos(4*pi*p).

Native activity/flow:
- log1p(total event rows in current coarse block);
- log1p(total trade volume);
- signed_log1p(total signed trade volume);
- mean spread state;
- mean signed microprice-offset state;
- mean native L10 imbalance state.

All non-cyclic continuous predictors are standardized from training data only at each refit.

This model is the primary native comparator.

### 8.3 Pair P15_30 and P30_60: two-child contrast test

Each current coarse block contains exactly two fine blocks.

Let fine semantic child states be `z1=(D1,I1)` and `z2=(D2,I2)`.

Fine contrast:
[
Delta z = z_2-z_1.
]

Model `F2`:
- all N predictors;
- Delta D;
- Delta I.

Because the parent coarse mean plus the last child is algebraically equivalent to the two-child path, `F2` is explicitly treated as equivalent in information content to adding the last-fast semantic state. No claim of higher-order path shape is permitted for factor-2 pairs.

Primary contrast:
[
Delta L_{N,F2}=L_N-L_{F2}.
]

### 8.4 Pair P60_300: five-child organization test

Each 300 s current block contains five 60 s child semantic states.

Comparator `L`:
- all N predictors;
- last child D;
- last child I.

Comparator `U`, unordered fine variability:
- all L predictors;
- standard deviation of child D;
- standard deviation of child I.

Model `S`, ordered organization:
- all U predictors;
- least-squares slope of child D versus child wall-clock position;
- least-squares slope of child I versus child wall-clock position.

This nested sequence separates:
- coarse state/context;
- last-fast state;
- unordered fine variability;
- ordered fine trajectory.

Primary 60->300 contrasts:
[
Delta L_{N,S}=L_N-L_S
]
[
Delta L_{L,S}=L_L-L_S
]
[
Delta L_{U,S}=L_U-L_S.
]

## 9. Model class

All models use ordinary least squares with intercept.

No model-family search.
No regularization tuning.
No feature selection.
No PCA-score predictors.
No scalar chi.
No event labels.
No price-return target.
No trading target.

If numerical rank deficiency occurs:
- use Moore-Penrose least-squares solution as implemented by NumPy `lstsq`;
- report matrix rank and condition number;
- do not drop predictors based on observed performance.

## 10. Walk-forward evaluation

Evaluation is performed separately by day.

For every pair:
- first 5 wall-clock hours are minimum training history;
- thereafter predictions are strictly out of sample;
- models refit on expanding past-only data at one-hour wall-clock boundaries;
- training observation is eligible only if its target block ends at or before the first source timestamp of the current test chunk;
- test chunks preserve chronological order;
- no overnight fitting;
- no target from the test chunk enters preprocessing, scaling, or model fitting.

Minimum valid OOS evaluation:
- at least 8 wall-clock hours after the training period.

Otherwise the day/pair is refused.

## 11. Loss

At each refit, target components are standardized using training-only target standard deviations.

For future target y=(D,I):

[
L=0.5(e_D^2+e_I^2)
]

where each error is divided by its training-only target-component standard deviation.

Report additionally:
- target-specific MAE;
- target-specific R2;
- day-specific mean loss contrast;
- number of OOS predictions.

## 12. Dependence-aware uncertainty

For every primary loss contrast:
- stratify by day;
- circular moving-block bootstrap within each day;
- 10,000 replicates;
- primary dependence block = 1 wall-clock hour;
- sensitivity blocks = 30 minutes and 2 hours;
- seed = 20260929;
- never resample across day boundaries.

Primary familywise interval:
- use 98.333% two-sided bootstrap intervals for the three adjacent-pair primary classifications, corresponding to Bonferroni control of familywise alpha=0.05 across the three primary pair questions.

The 95% intervals are reported descriptively as well.

## 13. Pair classifications

### 13.1 P15_30 and P30_60

`FINE_CONTRAST_ADDS_P0D` only if:
- lower 98.333% CI for mean `Delta L_N,F2` > 0;
- day-specific point contrast is positive on at least 4 of 5 days;
- F2 improves point MAE over N for both D and I.

`SUBTRACTS_P0D` if:
- upper 98.333% CI < 0.

Otherwise:
- `NEED_MORE_INFO_OR_MIXED`.

If either participating scale fails Layer R:
- append `REPRESENTATION_UNQUALIFIED`;
- do not use inheritance language.

### 13.2 P60_300

`ORDERED_PATH_ADDS_P0D` only if:
- lower 98.333% CI for `Delta L_N,S` > 0;
- lower 95% CI for `Delta L_L,S` > 0;
- lower 95% CI for `Delta L_U,S` > 0;
- N-to-S day point contrast positive on at least 4 of 5 days;
- S improves point MAE over N for both D and I.

`FINE_VARIABILITY_OR_LAST_ONLY_P0D` if:
- S beats N under the familywise rule;
- but S does not clearly beat L and U.

`SUBTRACTS_P0D` if:
- upper 98.333% CI for N-to-S < 0.

Otherwise:
- `NEED_MORE_INFO_OR_MIXED`.

If 60 s or 300 s fails Layer R:
- append `REPRESENTATION_UNQUALIFIED`;
- do not use inheritance language.

## 14. Secondary leads

Only after all primary lead-1 result objects are frozen:
- repeat identical models at lead 2;
- repeat identical models at lead 3.

Secondary leads:
- cannot rescue a failed primary pair;
- cannot change model features;
- cannot change scale qualification;
- cannot change primary classifications.

## 15. Negative controls and failure diagnostics

### NC1: session-phase-only synthetic known truth
Implementation must not assign fine-organization gain when future state is generated entirely by session phase.

### NC2: coarse-sufficiency known truth
Implementation must not assign gain when current coarse state fully determines the future target and fine path contains no additional information.

### NC3: fine-contrast known truth
For factor-2 pairs, implementation must recover known incremental information encoded only in the two-child signed contrast.

### NC4: five-child ordered-path known truth
For 60->300, implementation must recover known information encoded in temporal slope beyond coarse state, last-fast state, and dispersion.

### NC5: order-destroyed sensitivity
For 60->300 only, perform a frozen-seed within-parent permutation sensitivity that preserves the five child values but destroys their temporal order. This is descriptive and cannot rescue the primary outcome. If the ordered S result is indistinguishable from order-destroyed inputs, ordered-path language is weakened even if S beats N.

### NC6: representation robustness
If ordinary and winsorized Layer R disagree materially on scale qualification, label the scale `SEMANTIC_REPRESENTATION_NEED_MORE_INFO`.

## 16. Failure and outlier handling

Every failure/outlier remains evidence.

For:
- unusual day effects;
- representation failures;
- numerical instability;
- missing/refused blocks;
- strong rank migration;
- discordant robust sensitivity;
- extreme bootstrap influence;

preserve the case and distinguish:
- mechanical/data cause;
- statistical leverage;
- genuine market-state behavior;
- representation failure.

Do not exclude a day because it is inconvenient.

The primary result table must show all five days for every pair.

## 17. Multiplicity and search accounting

Primary search space is exactly:
- four representation scales;
- three adjacent lead-1 pair questions;
- one fixed semantic pair;
- fixed k=6;
- fixed model family;
- pair-specific predeclared predictor sets.

Primary pair family uses Bonferroni-adjusted 98.333% CIs.

Secondary leads, rank-migration tables, cross-scale principal cosines, effective rank, and joint structural/predictive interpretation are descriptive or explicitly secondary.

No post-outcome scale, feature, or lead may become primary.

## 18. Joint structural/predictive interpretation

Only after Layers R and L are independently frozen, construct a joint map describing each pair as combinations such as:
- semantics preserved + lagged information adds;
- semantics preserved + no incremental lagged information;
- rank migration + semantics preserved + gain;
- broader modal reorganization + gain/no gain;
- representation unqualified.

No direction is preregistered for the relationship between structural preservation and predictive gain.

This map is part of the broader uppercase-Chi investigation. It is not reduced to a scalar.

## 19. Scalar chi

Lowercase chi remains excluded from the temporal-hierarchy test.

No eigengap, effective rank, PCA capture, loss contrast, or temporal scale is converted into chi.

A scalar chi can enter this branch only under a separately qualified dynamical-model admission procedure.

## 20. Preregistered falsifiers

The current temporal-hierarchy hypothesis is weakened if:
- semantic representation fails qualification at one or more required scales;
- factor-2 fine contrast does not add beyond the native coarse comparator;
- 60->300 ordered model does not add beyond native context and simpler fine-information comparators;
- effects are isolated to one development day;
- robust representation sensitivity materially reverses scale qualification;
- apparent ordered-path gain survives equally after temporal order is destroyed.

If all three adjacent pairs fail their primary ADD classification:
- retire the current fixed semantic hierarchy as an incremental predictive tool;
- retain descriptive nested-scale structure only.

If only some pairs add:
- retain a scale-local architecture;
- refuse universal temporal inheritance.

If all three pairs add:
- promote only a P0-D claim that fine-scale semantic information adds across the tested MNQ transitions;
- do not claim causal inheritance;
- require new untouched evidence before P1.

## 21. Explicit nonclaims

This preregistration does not establish:
- causal substrate inheritance;
- universal market hierarchy;
- fractality;
- scale invariance;
- scalar chi inheritance;
- event prediction;
- profitable trading;
- cross-instrument transfer;
- market-wide Chi universality.

## 22. P1 promotion path

No result from the five development days is confirmatory.

Before P1:
1. close prior-art conglomeration;
2. complete external-cognition APQ against this preregistration;
3. resolve all BLOCKER/MATERIAL objections without looking at new decisive outcomes;
4. freeze implementation and hashes;
5. designate a new untouched MNQ date block or a prospectively frozen cross-instrument validation set;
6. execute without retuning.

June 9-11 cannot be reused as untouched temporal-hierarchy confirmation because Q038 has already opened those records under a different decisive question.

## 23. Current freeze state

This document is a draft until:
- the active comprehensive literature search closes;
- literature-derived changes are incorporated;
- APQ attacks the full preregistration;
- the resulting Plan Delta is resolved.

No real temporal-hierarchy development execution is authorized by this draft.

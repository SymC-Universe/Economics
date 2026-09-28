# External-Cognition APQ Attack Packet: MNQ Temporal Hierarchy

Date: 2026-09-27
APQ level: APQ-2
Frozen plan commit: `b58b95f2ec9d722e0343c4f961e849d720f8f1be`
Implementation commit under test lineage: `fa8a81d9cc941bebdeadaec9ac3e072225fd21e7`
CI run: `36371753558` SUCCESS

## Reviewer instruction

Perform an isolated first-pass adversarial review. Do not optimize the plan, make it more likely to succeed, or assume SymC/Stability Architecture is correct.

Return every objection as:
- BLOCKER
- MATERIAL
- MINOR

For every BLOCKER or MATERIAL objection, state:
1. the exact threatened inference;
2. why the existing control does not resolve it;
3. the smallest discriminating test or design change that would resolve it;
4. whether the change is outcome-independent and safe before real-data execution.

Explicitly attack shared premises rather than voting with the current plan.

## Frozen question

Does fine-scale organization of the already-established MNQ L10 symmetric-depth / bid-ask-imbalance semantic state contain lagged information about the next slower semantic state beyond the slower state's current state, ordinary session phase, and the last fast state?

## Frozen evidence scope

Development only:
- May 27, 28, 29, 2026
- June 1, 2, 2026
- 00:00-21:00 UTC

June 9-11 Q038 is prohibited for tuning.

## Fixed hierarchy

Primary:
- 15 s -> 30 s
- 30 s -> 60 s
- 60 s -> 300 s
- one future coarse-block lead

Secondary only:
- lead 2
- lead 3

Time is never rescaled.

## Representation

From each valid 1-second L10 book:
- log1p ten bid sizes + ten ask sizes;
- fixed symmetric-depth projection;
- fixed bid-minus-ask projection.

No PCA is refit.

For each current coarse block:
baseline B receives:
- current coarse depth state;
- current coarse imbalance state;
- session-phase sine/cosine.

last-fast L receives:
- last fine depth state;
- last fine imbalance state;
- same phase terms.

structured S receives every B predictor plus:
- fine-block SD of depth;
- fine-block SD of imbalance;
- fine-block slope of depth;
- fine-block slope of imbalance.

Future target:
- next coarse depth state;
- next coarse imbalance state.

OLS only. No hyperparameter search.

## Walk-forward

Per day:
- first 5 wall-clock hours minimum training;
- expanding past-only training;
- refit hourly;
- training observation excluded unless its future target ends before first test-source block begins;
- no cross-day fitting.

## Primary metric

Training-standardized joint squared error.

`Delta_B = Loss_B - Loss_S`

Positive favors fine-scale organization.

Day-stratified circular moving-block bootstrap:
- 10,000 reps
- one-hour wall-clock blocks
- seed 20260929.

ADDS P0-D at a scale pair only if:
- lower 95% bootstrap bound of mean Delta_B > 0;
- positive day point effect on at least 4/5 days;
- both target-component point MAEs favor S.

SUBTRACTS if upper bound < 0.
Otherwise NEED_MORE_INFO / MIXED.

## Existing internal attacks already resolved

- lead-zero aggregation identity -> refused;
- unfair rich comparator -> nested coarse-context baseline;
- time-of-day confounding -> same phase terms in B and S;
- unequal elapsed training across scales -> same 5 h training and 1 h refit cadence;
- future-target leakage -> explicit target-end < test-source guard;
- adaptive PCA/feature selection -> fixed semantic axes and four additions;
- multiplicity -> only three primary adjacent pairs at lead 1;
- Q038 contamination -> firewall;
- causal overreach -> only incremental lagged-information language.

## Prior-art collision already acknowledged

The plan does not claim novelty for:
- generic multiscale causality;
- LOB predictive power;
- microstructure modes;
- multiresolution liquidity;
- transfer entropy;
- generic lead-lag.

Relevant literature already surfaced includes:
- Bechler & Ludkovski 2017, LOB resiliency/predictability on meso scales;
- Golub et al. 2014, multiscale liquidity and predictive stress information;
- Elomari-Kessab et al. 2024, symmetric/antisymmetric microstructure modes + VAR predictability;
- multiscale transfer-entropy work.

## Specific attack targets

At minimum evaluate:
- mathematical dependence created by nested aggregation;
- whether B is actually the strongest fair native comparator;
- whether linear OLS architecture prejudges the answer;
- whether session-phase sin/cos is sufficient;
- whether the fixed semantic projections are licensed across scales;
- whether loss normalization leaks;
- whether block bootstrap dependence length is defensible;
- whether five days support the classification rule;
- whether multiple scale-pair classifications require multiplicity control;
- whether 80% coverage can bias state selection;
- whether slope/SD are redundant at factor 2;
- whether cross-scale gains can arise from microstructure noise reduction rather than semantic inheritance;
- whether the residual novelty is scientifically meaningful;
- whether a simpler alternative explanation would make the proposed tool unnecessary.

## Required response footer

End with exactly one:
- `APQ_EXTERNAL_STATUS=QUALIFIED`
- `APQ_EXTERNAL_STATUS=REVISE`
- `APQ_EXTERNAL_STATUS=BLOCKED`

Also repeat:
`PLAN_PACKET_COMMIT=b58b95f2ec9d722e0343c4f961e849d720f8f1be`

# MNQ Temporal Hierarchy Plan Delta: Early APQ Scaffold -> Preregistration v0.2

Date: 2026-09-27
Governance: GOM v0.8.8
Status: PRE-OUTCOME PLAN DELTA
Old plan packet commit: `b58b95f2ec9d722e0343c4f961e849d720f8f1be`
Literature foundation closure commit: `8204a340a71b9e511cc06bd6b233a93a9adb1e84`
Active preregistration candidate commit: `32efaa69879131889965d71ab799d42e7d291548`

No real temporal-hierarchy outcome from May 27/28/29 or June 1/2 was opened between the old plan and this revision.

## Material scientific changes

### Representation continuity
Old:
- 1-second mean depth sizes as new semantic inputs.

v0.2:
- preserve Q037/Q038 L10 last-book state lineage;
- within-day state persistence, no backfill;
- log-depth before temporal aggregation;
- alternating bid/ask coordinate order.

Reason:
avoid changing the observation object while testing temporal inheritance.

### Structural layer added
Old:
- lagged prediction only.

v0.2:
- Layer R separately qualifies semantic representation at 15/30/60/300 s using fixed k=6 semantic capture;
- rank migration is explicitly separated from semantic loss;
- winsorized-PCA sensitivity added.

Reason:
literature and Q038 show that semantic meaning and PC rank are distinct, while scale changes can genuinely reorganize LOB structure.

### Stronger native comparator
Old:
- current coarse semantic state + first session harmonic.

v0.2:
- current and previous coarse semantic state;
- first two session harmonics;
- current native activity/flow/context.

Reason:
prior literature establishes persistence/long memory, intraday seasonality, and strong order-flow predictive content.

### Pair-specific identifiability
Old:
- same SD+slope structured additions at every transition.

v0.2:
- 15->30 and 30->60 treated as two-child contrast tests;
- explicitly record that parent mean + last child contains the full two-point path;
- 60->300 becomes the first ordered-path test with five child blocks.

Reason:
avoid claiming trajectory structure that is mathematically nonexistent at factor 2.

### Ordered versus unordered information
Old:
- structured model versus coarse/last comparators.

v0.2:
- 60->300 nested sequence N -> L -> U -> S distinguishes:
  - native coarse context;
  - last-fast state;
  - unordered fine dispersion;
  - ordered fine slope.

Reason:
separate fine-scale variability/noise reduction from temporal ordering.

### Multiplicity
Old:
- 95% bootstrap intervals per pair.

v0.2:
- 98.333% intervals for the three primary pair questions;
- 95% intervals retained descriptively;
- secondary leads cannot rescue primary.

Reason:
explicit familywise search accounting.

### Scale-local outcomes
Old:
- common hierarchy question.

v0.2:
- each scale and pair may qualify, mix, subtract, or refuse;
- universal temporal inheritance is explicitly not assumed.

Reason:
Eisler et al. and Corradi et al. show scale-dependent LOB mechanisms and qualitative reorganization.

## Mechanical consequence

The existing `market_chi/temporal_hierarchy_v2.py` and `tools/mnq_temporal_hierarchy_v2.py` implement the earlier scaffold and are **not authorized for real-data execution under preregistration v0.2**.

They remain preserved as pre-preregistration engineering lineage and known-truth prototypes.

A v0.2-conformant implementation may be built only against the active preregistration candidate and must pass APQ/known-truth requalification before real development execution.

## External APQ binding

External attack packet:
`qualification/MNQ_TEMPORAL_HIERARCHY_EXTERNAL_APQ_PACKET_PREREG_v0.2_2026-09-27.md`

It is bound to:
`PREREG_COMMIT=32efaa69879131889965d71ab799d42e7d291548`

Real development execution remains blocked until that external review is adjudicated and all BLOCKER/MATERIAL objections are resolved.

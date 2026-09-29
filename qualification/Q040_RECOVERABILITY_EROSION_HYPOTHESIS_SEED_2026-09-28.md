# Q040 Candidate: Repeated-Perturbation Recoverability Erosion

Date: 2026-09-28
Governance: SymC GOM v1.0
Status: HYPOTHESIS SEED / P0-N OPEN
Execution status: NO REAL-DATA EXECUTION AUTHORIZED
Relationship to Q039: SEPARATE LANE; Q039 outcomes and preregistration are not altered by this candidate.

## Origin

The hypothesis was independently observed by the researcher in market behavior before the current Stability Inheritance formulation and later recognized qualitatively in human/biological recovery behavior. It has not yet been prospectively tested in either domain.

The current Stability Inheritance record independently identifies a related unresolved target:
- exact return-to-baseline may be too narrow;
- history-dependent changes in accessible recovery architecture may be more informative;
- repeated perturbation/history may alter modal Chi and system-level Chi_arc;
- recovery-history/loss-of-recoverability remains promotion debt requiring untouched tests.

This Q040 candidate imports only the question, not an answer or SI confirmation.

## Preliminary market prior-art boundary

Established neighboring work includes:
- Large (2007), electronic LOB resiliency after large trades;
- Lo & Hall (2015), multivariate LOB recovery after liquidity shocks;
- Xu et al. (2016), spread/depth/intensity recovery after effective market orders;
- Clapham et al. (2020), HFT participation in LOB replenishment;
- Corradi et al. (2015), scale-dependent liquidity fragility;
- 2026 work on liquidity recovery/hysteresis and secondary-collapse susceptibility;
- 2026 agent-based work comparing single versus temporally clustered/cascading shocks.

Therefore novelty cannot rest on:
- markets recover after shocks;
- recovery time/resiliency is measurable;
- order books exhibit hysteresis/path dependence in theory;
- clustered shocks can recover differently in simulation.

Preliminary residual target:
> In an empirical live LOB, does recovery capacity change systematically across successive perturbation/recovery cycles relative to a **scale-local averaged baseline**, and do those recovery changes precede, accompany, or fail to propagate into migration of slower-scale baselines after controlling for perturbation magnitude, spacing, session phase, activity/liquidity state, and perturbation direction?

A dedicated Undermind prior-art search is active before any preregistration is built.

## Candidate hypothesis family

### H-R1: repeated-perturbation recoverability erosion

Within a predeclared recovery episode, later comparable perturbations may exhibit weaker recoverability than earlier perturbations after controlling for native state.

"Weaker" is not reduced to one scalar. Candidate recovery outputs are:
- lower probability of sustained reclaim;
- longer first-return time;
- longer sustained-recovery time;
- shorter dwell on the recovered side after reclaim;
- larger residual displacement at fixed horizon;
- lower recovery excursion relative to perturbation magnitude.

### H-R2: cumulative burden versus attempt number

Raw attempt number is not assumed to be the causal variable.

Compare:
- perturbation ordinal number;
- cumulative absolute perturbation load;
- cumulative time spent away from baseline;
- incomplete-recovery burden from preceding cycles.

The researcher's prior practical observation of roughly 3-5 attempts remains descriptive and must not become a threshold unless prospectively justified.

### H-R3: direction symmetry is testable, not assumed

Primary hypothesis is sign-agnostic in form.

Test interaction between recovery-history burden and perturbation direction.

Possible outcomes:
- similar erosion upward and downward;
- asymmetric erosion;
- one-direction-only effect;
- no erosion.

### H-R4: adaptation/strengthening is an explicit falsifier

Repeated perturbation may strengthen recovery through liquidity attraction, participant adaptation, or regime stabilization.

A systematic improvement of recovery metrics with repeated perturbation is a valid opposite-direction result and must not be relabeled as erosion.

### H-R5: baseline hierarchy rather than one fixed baseline

A single frozen episode baseline is too crude for the intended market observation.

For each timescale S, define a causal scale-local averaged state baseline:

[
B_S(t)
]

using only information available before the perturbation being scored.

Candidate starting ladder, inherited from the existing market hierarchy:
- 15 s;
- 30 s;
- 60 s;
- 300 s.

Longer scales may be added only prospectively after prior-art/APQ review; they are not frozen by this hypothesis seed.

Perturbation at scale S is defined relative to (B_S), not relative to one global horizontal reference.

The exact averaging kernel/window is not yet frozen. It must be:
- causal;
- scale matched;
- outcome blind;
- fixed before empirical scoring.

### H-R6: baseline migration across the hierarchy

Baseline motion is not merely a nuisance variable. It is itself a candidate state-transition object.

Test whether repeated failed or weakened recoveries at a faster scale:
1. leave slower baselines unchanged;
2. precede measurable displacement of the next slower baseline;
3. accompany simultaneous multiscale baseline migration;
4. fail to propagate upward.

This creates an explicit hierarchy:
[
B_{15s}(t) ightarrow B_{30s}(t) ightarrow B_{60s}(t) ightarrow B_{300s}(t) ightarrow cdots
]

without assuming causal transmission.

A fast-scale failure counts as a recovery failure only relative to its own scale-local baseline. A slower-scale transition is separately identified by movement/reorganization of the slower (B_S).

### H-R7: recoverability erosion versus baseline redefinition

An apparent weakening of recovery can be caused by genuine loss of recoverability **or** by the baseline itself moving.

The decisive design must distinguish:
- recovery back toward a stable (B_S);
- repeated incomplete recoveries around (B_S);
- drift of (B_S) while the next slower baseline remains stable;
- migration of multiple (B_S) levels together;
- full slower-scale regime transition.

The scientific target is therefore not "return to one fixed baseline" but the relationship between **scale-local recovery** and **cross-scale baseline migration**.

## Existing Market primitive

`market_chi/recovery.py` already provides a useful nondecisive primitive after a known break:
- active recovery;
- failed recovery;
- sustained reclaim;
- unresolved recovery;
- no qualifying recovery;
- failed-attempt count.

It explicitly does not discover the baseline/reference, select scale, or hard-code 3-5 attempts as special.

Q040 should extend this primitive rather than replace its semantics.

## Candidate experiment architecture

### A. Scale-local baseline hierarchy

The primary baseline object is a **native-state average at each timescale**, not one episode-wide fixed point.

For each scale S:
- construct a causal averaged/centroid state (B_S(t)) from that scale's own pre-perturbation history;
- score perturbation distance and recovery relative to (B_S(t_0)) for that perturbation;
- track subsequent motion of (B_S) separately from recovery toward it;
- compare (B_S) with the next slower (B_{S'}).

Candidate primary hierarchy begins with:
- 15 s;
- 30 s;
- 60 s;
- 300 s.

The exact averaging operator remains to be preregistered after prior-art/APQ work. Candidate operators include fixed trailing block mean or robust centroid; no operator may be selected from outcome performance.

A second, mechanistically distinct reference family may later compare trader-visible VWAP/EMA-style references under the existing shared-reference/placebo firewall. Those references must not define the primary native baseline.

### B. Perturbation definition

No post-outcome hand labeling.

A perturbation must be defined prospectively by signed distance from the **scale-local pre-perturbation baseline** (B_S(t_0)) using training-only scale/calibration.

For each perturbation retain:
- sign;
- amplitude;
- duration;
- integrated displacement;
- activity/order-flow state;
- spread/depth state;
- time since prior perturbation;
- state of the previous recovery.

### C. Recovery vector

For perturbation j, preserve a vector:
[
R_j = (T_{return}, T_{sustain}, P_{sustain}, D_{dwell}, E_H, G_{recovery}, ...)
]

No universal scalar "recovery strength" is assumed.

### D. Main contrast

Estimate whether the recovery vector changes with prior perturbation history after controlling for:
- current perturbation amplitude;
- duration;
- direction;
- inter-perturbation interval;
- session phase;
- activity;
- spread/depth;
- volatility/native risk state;
- current modal/semantic LOB state;
- scale-local baseline velocity/drift;
- distance/alignment between the current scale baseline and the next slower baseline.

The hierarchy adds a second family of outcomes:
- fast-baseline displacement after repeated failed recovery;
- time from fast-scale recovery erosion to slower-baseline displacement;
- number/load of perturbations before slower-scale migration;
- whether slower-scale migration occurs at all.

Candidate models compare:
- memoryless native recovery model;
- ordinal-history model;
- cumulative-load model;
- incomplete-recovery-burden model.

The strongest native model is the comparator. History earns admission only if it adds out-of-sample information.

A separate hierarchy test asks whether fast-scale recovery-history variables add information about future movement/reorganization of the next slower baseline beyond the slower baseline's own persistence and native context.

### E. Sequence integrity

Do not classify later perturbations as independent observations when they belong to the same episode.

Inference must account for:
- within-episode dependence;
- within-day dependence;
- repeated market-state regimes.

### F. Relationship to Stability Architecture

Potential interpretation if supported:
- the accessible recovery architecture is history-dependent;
- repeated perturbation changes the realized response/recovery landscape.

This would still not establish a universal Stability Inheritance law.

If the effect is fully explained by native activity, order-flow memory, baseline drift, volatility, or ordinary LOB hysteresis, classify as native market dynamics / EQUIVALENT, not SI added value.

## Strong falsifiers

The candidate is weakened or refused if:
- later perturbations recover equally well after native-state adjustment;
- apparent erosion vanishes after matching perturbation magnitude;
- result is entirely explained by shorter shock spacing;
- apparent erosion is entirely explained by scale-local baseline migration without any residual weakening relative to that moving baseline;
- only one hand-selected reference produces the effect;
- result is a session-time/activity artifact;
- the sign interaction reverses or eliminates the pooled effect;
- a native Markov/history model explains the sequence without any stability-specific representation;
- repeated perturbations improve rather than weaken recovery.

## Evidence firewall

Do not use Q038 June 9-11 as a new untouched confirmatory set.

Existing May/June MNQ records may be used only as development evidence after a separate preregistration/APQ plan is frozen.

A later P1 test requires prospectively untouched dates/instrument data.

## Next gates

1. close dedicated prior-art conglomeration;
2. define baseline/reference candidates and native comparators;
3. adversarially test whether "recovery erosion" is identifiable separately from drift, clustering, and ordinary order-flow memory;
4. only then construct a Q040 preregistration;
5. do not alter Q039 or reuse Q039 outcomes to choose Q040 rules.

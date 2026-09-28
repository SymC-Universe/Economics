# MNQ Temporal Hierarchy: Literature + Hypothesis Foundation

Date: 2026-09-27
Governance: SymC GOM v0.8.8
Stage: P0-N / A0 foundation before preregistration freeze
Repository: `SymC-Universe/Economics`
Branch: `market-chi-architecture`

## Purpose

This record conglomerates prior literature with the existing MNQ development lineage before a temporal-hierarchy preregistration is frozen. It is intentionally not a results document. The five development days have not been opened under the new temporal-hierarchy outcome definitions.

The research object is not generic multiscale market prediction. It is whether the already-qualified MNQ L10 semantic architecture is preserved, reorganized, lost, or refused across fixed wall-clock scales, and whether fine-scale organization contains incremental lagged information about the next coarser semantic state after stronger native controls.

## What prior literature already establishes

### 1. Native LOB state contains short-horizon information

Deep and shallow LOB state, imbalance, and order flow have repeatedly been shown to contain short-horizon information about future price or liquidity states.

- Bechler & Ludkovski (2017), DOI 10.1142/S2382626618500065, show that deeper LOB shape and limit-order flows can be more informative than top-level depth on meso scales. They control for time of day, bucket duration, lagged price change, lagged imbalance, and lagged limit flow.
- Xu, Gould & Howison (2018/2019), DOI 10.1142/S2382626619500114, show that multi-level order-flow imbalance improves out-of-sample performance relative to top-of-book OFI, with deeper levels materially contributing.
- Cont, Cucuringu & Zhang (2021/2023), DOI 10.1080/14697688.2023.2236159, show low-rank structure in order-flow imbalance and use rolling out-of-sample validation for predictive cross-impact.
- Sirignano & Cont (2018/2019), DOI 10.1080/14697688.2019.1622295, show broad cross-asset regularity in LOB-based next-price-move prediction and demonstrate that transferable book features exist.
- Kolm, Turiel & Westray (2023), DOI 10.1111/mafi.12413, explicitly forecast high-frequency returns at multiple horizons from granular order-book/order-flow inputs.
- Ntakaris et al. (2019), DOI 10.1109/ACCESS.2019.2924353, benchmark engineered and learned LOB features under fixed and event-based future horizons.

**Consequence:** no novelty claim may rest on "LOB data are predictive," "deeper levels matter," "multi-horizon forecasting works," or "fast book states contain future information."

### 2. Low-dimensional and semantically interpretable market modes already exist in the literature

- Elomari-Kessab et al. (2024), DOI 10.2139/ssrn.4831906, construct PCA microstructure modes that separate bid-ask symmetric liquidity activity from antisymmetric/directional structure. Their mode semantics remain qualitatively similar after coarse-graining, while eigenvalue weights change. VAR dynamics of these modes are predictive and exhibit long-memory/marginal-stability behavior.
- Ait-Sahalia & Xiu (2016/2017), DOI 10.1080/01621459.2017.1401542, show surprising consistency between high- and lower-frequency PCA structures in a different high-frequency finance setting.
- Tyurin (2004) uses PCA to identify pervasive factors in high-frequency limit-order-market dynamics and reports changes in which native variables dominate at different frequencies.
- Panayi, Peters & Kosmidis (2014/2015), DOI 10.1080/14697688.2015.1071075, warn that ordinary PCA-based liquidity commonality can be misleading under heavy-tailed data and motivate robustness checks.

**Consequence:** no novelty claim may rest on "there are liquidity modes," "symmetric/antisymmetric modes exist," or even simple "modal structure can survive coarse-graining." The new question must distinguish semantic preservation from rank identity and must protect against heavy-tail/PCA artifacts.

### 3. Multiscale representation and cross-scale information flow are established fields

- Golub et al. (2014/2016), DOI 10.3233/AF-160054, construct an intrinsically multiscale market-liquidity representation and explicitly distinguish structural nesting/coarse-graining from predictive information.
- Faes et al. (2017), DOI 10.1103/PhysRevE.96.042150, show that filtering/downsampling can alter or even spuriously create multiscale Granger-causal structure. They demonstrate that naive rescaling can be biased and that causal filtering and state-space treatment matter.
- Zhao et al. (2018), DOI 10.1016/J.CNSNS.2018.02.027, develop multiscale transfer entropy specifically to estimate scale-dependent directional information flow while addressing finite-size and spurious-causality problems.
- Saadaoui (2025), DOI 10.1080/07474938.2025.2471913, reviews/formalizes multiresolution causality tests and their limitations in nonstationary financial settings.

**Consequence:** no novelty claim may rest on "information flows across scales" or "causality is scale dependent." Any fixed-scale inheritance test must explicitly distinguish arithmetic nesting, persistence, filtering/noise reduction, and directional incremental information.

### 4. Direct time-scale comparisons show both preservation and reorganization

The comprehensive prior-art search identified closer predecessors that materially constrain the hypothesis.

- Eisler, Kertesz & Lillo (2007), DOI 10.1117/12.724817, compare the LOB across monthly, daily, intraday, and tick scales and conclude that the qualitative picture changes with scale. Microstructure variables can become negligible at long scales while imbalance, liquidity fluctuation, and event-level effects dominate at shorter scales. They do not perform the conditional fine-to-coarse lagged-state test proposed here.
- Cont, Kukanov & Stoikov (2010/2014), DOI 10.1093/jjfinec/nbt003, show that the contemporaneous OFI/price-impact relation is robust over aggregation intervals ranging from sub-second quote-update scales to roughly 10 minutes. This establishes aggregation robustness of a native relation, not incremental lagged information from fine state to future coarse state.
- Corradi, Zaccaria & Pietronero (2015), DOI 10.1103/PhysRevE.92.062802, show that the effective mechanism of liquidity fragility changes with scale: static book depletion is informative around 30 s, whereas dynamic compensation failure between market/limit-order flows dominates at 15 min. This directly motivates scale-local outcomes and refusal of a universal hierarchy.
- Hardle/Hautsch/Mihoci factor models and Chen/Chua/Hardle functional autoregressive models forecast LOB supply-demand curves over multiple horizons, demonstrating that curve-level LOB dynamics and multi-horizon liquidity forecasting are already established.
- The completed deep search therefore narrows the residual gap to a conditional cross-scale state-transfer question rather than a generic scale comparison.

**Consequence:** the preregistration must allow genuine representation change with scale, include coarse-history persistence controls, and avoid interpreting any one successful transition as a universal hierarchy.

## Existing MNQ evidence that may motivate but not decide the new test

Q037 development and Q038 frozen holdout established a predeclared L10 semantic pair:
- symmetric depth;
- bid-ask imbalance.

Q038 showed that this pair can remain jointly captured by a fixed wider k=6 subspace even when top-two PC rank identity fails locally. This motivates a temporal-hierarchy question in which semantic meaning and modal rank are treated separately.

Q038 does not establish temporal inheritance, cross-scale prediction, causal transmission, or cross-market invariance.

Canonical scalar chi remains unlicensed in the current MNQ production screens and is excluded from the temporal-hierarchy preregistration.

## Residual scientific gaps after prior-art collision

### Gap G1: semantic architecture versus horizon-specific forecasting

Existing multi-horizon work mainly asks whether LOB variables forecast price or returns at multiple horizons. The unresolved target here is whether a **previously qualified semantic book architecture itself** remains licensed as the observation scale changes.

### Gap G2: semantic preservation versus modal rank preservation

Prior work and Q038 both indicate that semantic directions may persist while PCA rank changes. A fixed-scale hierarchy therefore needs to measure:
- semantic capture;
- rank migration;
- cross-scale subspace organization;
without defining failure as a change in PC number.

### Gap G3: fine-path information beyond the already-formed coarse state and its own recent history

Because each coarse block is built from fine observations, contemporaneous reconstruction is partly arithmetic. The scientifically useful question is whether **within-parent fine organization at time t adds information about the next coarse state** beyond:
- current coarse semantic state;
- previous coarse semantic state / coarse trend;
- current native book/flow context;
- session phase;
- last fast state;
- unordered fine variability.

### Gap G4: ordered organization versus noise reduction

Aggregation can improve signal simply by suppressing noise. A stronger inheritance interpretation requires separating:
- unordered within-parent dispersion;
from
- temporally ordered fine-path structure.

### Gap G5: scale-local success versus universal hierarchy

Prior literature shows scale dependence and aggregation sensitivity. The hypothesis must allow:
- one adjacent transition to add;
- another to be equivalent;
- another to subtract or refuse.
A universal 15s->30s->60s->300s ladder is not assumed.

### Gap G6: structural preservation and predictive usefulness need not coincide

A semantic architecture can remain geometrically identifiable without carrying incremental future information, or vice versa. The preregistration therefore requires separate structural and lagged-information layers and a later joint interpretation.

## Hypothesis architecture

### H-TH1: representation preservation

Across 15 s, 30 s, 60 s, and 300 s fixed wall-clock aggregation, the predeclared symmetric-depth and bid-ask-imbalance directions remain preferentially represented in the broader L10 modal subspace often enough to license the same semantic interpretation at that scale.

This is a representation-qualification hypothesis, not a predictive claim.

### H-TH2: rank migration is not semantic failure

Changes in the strongest individual PC carrying a canonical direction do not by themselves constitute architecture loss. Fixed-k semantic capture and cross-scale subspace geometry are the relevant structural objects.

### H-TH3: incremental fine-organization hypothesis

At an adjacent scale transition, ordered/unordered fine semantic organization within the current coarse block may reduce out-of-sample error for the next coarse semantic state beyond a strong nested native comparator containing:
- current coarse semantic state;
- session phase;
- current native activity/flow/context.

This hypothesis may fail independently at each adjacent scale pair.

### H-TH4: ordered-path discrimination

If the full ordered model adds beyond the native comparator, test whether it also adds beyond an otherwise matched model containing unordered fine-scale dispersion but not temporal slope. This distinguishes ordered path information from mere fine-scale variability/noise reduction.

### H-TH5: scale-local/refusal hypothesis

Inheritance is not presumed to be universal across the ladder. Each scale pair can be classified independently as:
- ORDERED_PATH_ADDS;
- FINE_VARIABILITY_ONLY;
- EQUIVALENT_OR_MIXED;
- SUBTRACTS;
- REPRESENTATION_REFUSED;
- INVALID_TEST.

### H-TH6: structural-predictive joint meaning

After the structural and lagged layers are frozen separately, investigate whether added lagged information co-occurs with:
- high semantic preservation;
- rank migration without semantic loss;
- broader modal reorganization;
or no systematic structural pattern.

No directional relationship is preregistered for this joint layer. It is an explicit post-primary interpretation target, not a rescue criterion.

## Design consequences inherited from the literature

1. Use fixed wall-clock scales because the scientific hypothesis concerns the user's 15 s / 30 s / 1 min / 5 min hierarchy. Do not convert elapsed time into business time or instrument-dependent time.
2. Use deeper L10 state rather than top-of-book only.
3. Include native flow/context controls because order flow is a strong established predictor.
4. Include previous coarse semantic state because persistence and long-memory are established competing explanations.
5. Include session phase because intraday nonstationarity is established and already visible in MNQ development.
6. Use strictly future, non-overlapping targets and target-time leakage guards.
7. Use expanding past-only evaluation.
8. Treat current + previous coarse state as the primary persistence/nesting comparator.
9. Separate unordered variability from ordered fine-path information.
10. Use fixed semantic directions and fixed k=6 rather than adaptive PCA rank selection.
11. Add a robust modal sensitivity because heavy tails can distort PCA interpretation.
12. Use dependence-aware uncertainty within day and preserve day-level effects.
13. Do not infer causality from predictive gain.
14. Do not infer market-wide or cross-instrument universality from MNQ.
15. Keep scalar chi separate and refused unless independently licensed.
16. Require new untouched evidence for any promotion beyond P0-D.

## Representation continuity correction before preregistration

The earlier APQ Plan Packet proposed constructing the new semantic input from 1-second mean depth sizes. That would unnecessarily change the observation object relative to Q037/Q038.

The preregistration will instead preserve the established state lineage:
- use the L10 last-book state fields;
- preserve the existing no-backfill / state-persistence treatment;
- compute log-depth before temporal aggregation;
- preserve the canonical alternating bid/ask coordinate order used by the modal engine.

This change is pre-outcome and is made for representation continuity, not because of any temporal-hierarchy result.

## Novelty boundary

The strongest defensible residual novelty target is not generic multiscale prediction. It is the **joint qualification of a previously established semantic L10 architecture across fixed wall-clock temporal embeddings, with explicit separation of semantic preservation from modal rank migration and explicit tests of whether fine-scale organization adds future coarse-state information beyond the already-formed coarse state and native context.**

Even this remains a hypothesis-level novelty target until the comprehensive prior-art search closes and the external APQ review attacks the final preregistration.


## Comprehensive prior-art search closure

Undermind deep search `MNQ temporal hierarchy prior art` completed on 2026-09-27/28 with 131 surfaced papers. Its synthesis independently converged on the same residual gap: existing studies establish multiscale impact, forecasting, modal structure and scale-dependent mechanisms, but do not directly test whether a harmonized interpretable LOB state adds out-of-sample lagged information from fine to coarse fixed-clock bins after controlling for coarse-state persistence, intraday effects, native context and aggregation artifacts.

The closest collision papers were explicitly incorporated above. No paper surfaced that performs the full proposed combination of:
- prequalified semantic L10 directions;
- semantic-vs-rank separation;
- fixed 15/30/60/300 s adjacent wall-clock transitions;
- representation qualification before inheritance language;
- current + previous coarse-state and native-context comparators;
- factor-2 algebraic equivalence handling;
- five-child ordered-path discrimination;
- explicit preservation/reorganization/loss/refusal outcomes.

This does not prove novelty. It defines the current residual novelty target to be attacked in APQ and later manuscript-level novelty review.

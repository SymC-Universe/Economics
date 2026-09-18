# Market Χ Engine Qualification Ledger

Status: P0-Q active
Branch: `market-chi-architecture`
GOM baseline: v0.8.0

This ledger records qualification work for the native-model-first rebuild. It does not convert synthetic or previously viewed evidence into P1 confirmation.

| ID | Target | Test | Current status | Promotion consequence |
|---|---|---|---|---|
| Q001 | scalar χ licensing | derive χ from known discrete complex pole pair | PASS / implemented | required for second-order complex branch |
| Q002 | scalar χ licensing | derive χ from known positive real pole pair | PASS / implemented | required for overdamped real-pole branch |
| Q003 | refusal | white noise must not receive χ | PASS in current baseline sweep | blocks release if violated materially |
| Q004 | refusal | ordinary AR(1) must not receive χ merely from persistence | PASS in current baseline sweep | blocks release if violated materially |
| Q005 | model admission | known AR(2) complex factor selected against AR0/AR1 | PASS in current baseline sweep | qualifies first local modal path |
| Q006 | model admission | known AR(2) real factor selected against AR0/AR1 | PASS in current baseline sweep | qualifies first overdamped path |
| Q007 | legacy ACF route | correct position-versus-velocity kernel mismatch and re-test | OPEN | legacy results remain historical/P0-Q until resolved |
| Q008 | exact simulation | replace Euler known-truth oscillator with exact or production-qualified discretization | OPEN | required before oscillator known-truth campaign |
| Q009 | non-oscillator alternatives | GARCH/SV/jump/regime-switching adversarial families | PARTIAL | stochastic-volatility false-admission tail remains; broader alternatives still required |
| Q010 | uncertainty | calibrate coverage for the exact production estimator | OPEN | required before uncertainty claim |
| Q011 | multivariate/modal | qualify modal layer separately from χ | PASS P0-D REPLICATION ON 2 DEVELOPMENT DAYS | liquidity + imbalance geometry replicated on May 27 and May 31; more days/session phases required before freeze |
| Q012 | local-to-embedded | test whether local dynamical structure survives sector/market embedding | OPEN | substrate-inheritance target; current corpus is single-instrument MNQ |
| Q013 | real-data input gate | inventory and schema-profile local corpus before scale | PASS | corpus identified as MNQ trades + MBP-10; loader contract fixed |
| Q014 | MBP-10 data contract | raw price/timestamp semantics, flags, 10-level fields, continuous-symbol handling | PASS / documented | licenses native microstructure extraction |
| Q015 | MBP-10 first-pass code | synthetic fixture verifies price scale, contract segmentation, snapshot-flow exclusion | PASS | permitted first real development-file run |
| Q016 | real MBP-10 loader | run extractor on development files and audit outputs | PASS ON MAY 31 + MAY 27 | May 27 v2: 37,491,279 rows -> 82,713 1-s bins; zero event-time disorder; one bad-receive-time flag only |
| Q017 | future holdout independence | freeze 2026-06-09 through 2026-06-11 MBP-10 observation files by provider hashes without inspecting rows | PASS / SEALED | preserves candidate P1 evidence |
| Q018 | contract-roll safeguard | prevent calendar continuous-contract rollover from appearing as physical return/Χ/χ transition | IMPLEMENTED; SINGLE-INSTRUMENT REAL CHECK PASS | rollover-specific real case still required before multi-contract claims |
| Q019 | signed microprice channel | detect v1 sign-loss defect; preserve negative/zero offsets in v2 and regression-test identity | PASS IN V2; V1 QUARANTINED FOR MICROPRICE | v2 required for all new raw extractions |
| Q020 | native depth geometry | recover interpretable L10 modal structure without using χ | PASS P0-D REPLICATION | PC1 liquidity + PC2 side-imbalance geometry reproduced May 27 after May 31 discovery |
| Q021 | χ refusal on real native modes | apply production χ gate to discovered modes across 1-60 s sampling | PASS AS REPLICATED REFUSAL BEHAVIOR | 0/42 χ admissions on May 27 after 0 admissions on May 31; protects against oscillator-first interpretation |
| Q022 | forward-risk discovery | compare depth modes/native scalars with future path movement | P0-D CHANNEL FOUND; SIGN NOT STABLE | May 27 reverses depth/spread risk signs vs May 31; session-phase map required before any portable rule |
| Q023 | session-phase control | compare like-for-like fixed Globex phases across development days | OPEN / NEXT GATE | required before freezing any forward-risk direction or capacity interpretation |
| Q024 | failed-recovery trajectory primitive | distinguish active recovery, failed sustain, sustained reclaim, unresolved recovery, and refusal on known-truth paths | PASS / IMPLEMENTED; 5 KNOWN-TRUTH TESTS | licenses P0-D event construction after scale/reference rules are separately frozen |
| Q025 | temporal substrate-inheritance scaffold | reconstruct slower target from structured fast-substrate summaries versus last-fast-state baseline using walk-forward evaluation | PASS / IMPLEMENTED; 4 KNOWN-TRUTH TESTS | licenses P0-Q inheritance feasibility tests; does not establish inheritance on market data |
| Q026 | shared-reference hypothesis | compare broker-default EMA/MACD/VWAP references against nearby matched perturbations/placebos | DESIGN FROZEN; PLATFORM DEFAULTS PENDING | required before attributing any response to shared trader visibility |
| Q027 | cross-day modal comparison | compare same-phase top-k loading subspaces with sign/rotation-invariant principal cosines | PASS / IMPLEMENTED | permits rigorous development replication once sweep phase index is available |
| Q028 | continuous qualification CI | install package and run production pytest suite on branch pushes | PASS / ACTIVE | catches packaging/test regressions before local empirical use |

## Current P0-Q rule

The initial executable scalar scaffold compares AR(0), AR(1), and AR(2) using BIC and emits χ only when AR(2) wins by a configurable qualification margin and its poles admit a canonical continuous second-order mapping.

The default BIC margin of 6 is a P0-Q qualification setting, **not** a frozen physical boundary and not a P1 decision rule. It may change during controlled qualification with the search history preserved.

Real-market development no longer begins at that scalar scaffold. The native path starts from the Databento MNQ MBP-10 book and trade fields, preserves ten-level vector structure, separates synthetic snapshots from endogenous flow, segments actual contracts, and defers χ until downstream model admission.

The first two real analyses now establish a stronger architecture result than the original oscillator-first framing: the native L10 order book repeatedly produces an interpretable liquidity/imbalance modal geometry while canonical scalar χ is refused. The exact modal variance concentration changes across market/session states, and the first forward-risk sign pattern does not generalize from May 31 to May 27. That failure is retained as evidence and creates the session-phase control gate Q023 rather than being tuned away.

The trader-observation lineage has now produced two executable but still non-empirical qualification primitives. Q024 models the trajectory of an active recovery after a known break and explicitly allows a partial/full reclaim to fail if it cannot sustain the recovered side; attempt count is descriptive and 3-5 is not hard-coded. Q025 tests temporal substrate inheritance as an incremental reconstruction question: do structured summaries of the faster substrate reconstruct the slower target out of sample better than simply carrying the last fast state forward? Both remain P0-Q scaffolds until applied under frozen market definitions.

Development comparison rules are frozen in `qualification/MNQ_DEVELOPMENT_P0Q_COMPARISON_PLAN_2026-09-18.md`. Shared-reference and cross-market extension questions have separate pre-outcome design records. GitHub Actions now continuously verifies package installation and the production test suite.

See:

- `qualification/ADVERSARIAL_BASELINE_2026-09-14.md`
- `qualification/admission_sensitivity_2026-09-14.csv`
- `qualification/HOLDOUT_FREEZE_2026-09-14.md`
- `qualification/MNQ_2026-05-31_MODAL_DISCOVERY.md`
- `qualification/MNQ_2026-05-27_WEEKDAY_REPLICATION.md`
- `data_contract/MNQ_DATABENTO_CONTRACT_2026-09-14.md`

# Q039 v0.4 Production Implementation Checkpoint

Date: 2026-09-29
Governance: SymC GOM v1.0
Canonical preregistration:
\`b757d0dd65a700be1bf1d2cb5233c75c83086308\`

Real Q039 market outcomes opened during implementation: **NO**

## Overall disposition

\`Q039_V0_4_PRODUCTION_CORE_IMPLEMENTED_EXTERNAL_NC7_RULE_AND_SOURCE_FREEZE_PENDING\`

The prior legacy runner is not v0.4-conformant and has been quarantined. The replacement production components are implemented and CI-qualified without opening real Q039 outcomes.

## Implemented components

### Exact L10 source-state intake

File:
\`market_chi/q039_intake_v04.py\`

Introduced:
\`face09b680af8e74bc1d0446527b567b22d04d42\`

Qualified behavior:
- literal one-second UTC grid;
- alternating bid/ask L10 ordering;
- \`valid_book_rows > 0\` defines a valid new L10 state;
- all 20 L10 sizes must be finite and nonnegative;
- invalid/bad rows do not overwrite prior valid state;
- no backfill before first valid L10 state;
- no cross-day carry by construction;
- update indicator and staleness age are derived from true valid-L10 updates;
- \(\log(1+\mathrm{size})\) is applied after carry-forward;
- raw semantic \(D/I\) functionals use the frozen directions.

Tests:
\`tests/test_q039_intake_v04.py\`

### Fixed wall-clock block hierarchy

File:
\`market_chi/q039_blocks_v04.py\`

Introduced:
\`636038ed115b333a28022154c3c9b63762c8fe2e\`

Qualified behavior:
- fixed 15/30/60/300 s wall-clock blocks;
- no invented coverage threshold;
- block refused only when no valid state has yet appeared;
- exact native flow/update/staleness summaries;
- first/second session harmonics;
- exact N/A2/F2/A/L/U/S construction.

Frozen predictor dimensions:
- N: 17 predictors;
- A2: 22;
- F2: 24;
- A: 23;
- L: 25;
- U: 27;
- S: 29.

Including intercept:
- factor-2 \(p_{\max}=25\);
- factor-5 \(p_{\max}=30\).

Tests:
\`tests/test_q039_blocks_v04.py\`

### Production Layer L evaluator

File:
\`market_chi/q039_layer_l_eval_v04.py\`

Introduced:
\`81975e916148110c4fe579cb22a07ecde0062b99\`

Leakage-diagnostic repair:
\`021f81aa57fa1a794aa78126c095b5cb0b8c6c6d\`

Corrected test:
\`154a6e9aefb5d924ed54f236467f8867ba19af03\`

Qualified behavior:
- expanding within-day walk-forward only;
- first test no earlier than 5 wall-clock hours;
- \(n_{\mathrm{train}}\ge5p_{\max}\);
- training target end <= first test source time;
- training-only scaling of non-cyclic continuous predictors;
- no silent predictor dropping;
- rank-deficient refit refusal;
- condition number >1e8 retained descriptively but excluded from primary;
- >=8 valid wall-clock OOS hours required;
- target-SD-standardized joint loss;
- raw D/I MAE and R2;
- Clark-West-style nested diagnostic that cannot rescue raw failure;
- non-circular contiguous moving-block bootstrap;
- equal-day weighting;
- frozen-seed percentile intervals.

CI after direct leakage-firewall correction: PASS.

### Production Layer R descriptor

File:
\`market_chi/q039_layer_r_production_v04.py\`

Introduced:
\`7a66f5070fa3e78018e6b157ad4db97981aaa61b\`

Tests:
\`tests/test_q039_layer_r_production_v04.py\`

Qualified behavior:
- ordinary fixed-k6 PCA;
- lineage and covector-consistent functional directions;
- matched-family percentiles;
- winsorized sensitivity;
- phase-adjusted sensitivity using **actual wall-clock block indices**;
- per-PC canonical contributions;
- strongest-PC rank/alignment;
- \(\rho_1\);
- full spectrum and effective rank;
- measurement/update/staleness diagnostics;
- adjacent-scale k6 principal cosines.

CI: PASS.

### Deterministic v0.4 classification

File:
\`market_chi/q039_classification_v04.py\`

Introduced:
\`1645330dad1054234e901519457dc8922b591751\`

Tests:
\`tests/test_q039_classification_v04.py\`

Qualified behavior:
- exact factor-2 labels;
- exact P60 labels;
- no SUBTRACTS primary label;
- positive result requires CI + 4/5 day + pooled D/I MAE + NC7 + known-truth gates;
- NC7 failure appends \`CARRY_FORWARD_ARTIFACT_NOT_EXCLUDED\`;
- Layer-R/Layer-L joint map is mechanical and does not use inheritance language.

CI: PASS.

### Frozen source-identity contract

File:
\`market_chi/q039_source_v04.py\`

Introduced:
\`efe32c93302a79fa48d200e01d2f36eb2fb8026a\`

Tests:
\`tests/test_q039_source_v04.py\`

Identity scanner:
\`tools/q039_source_identity_preflight_v04.py\`
introduced at:
\`6343a22c3e9db205dff20a2bc637fed246920f05\`

Production execution requires exactly five frozen development sources with:
- v2 feature-file SHA-256;
- instrument_id;
- symbol;
- exact canonical dates;
- explicit Q038 prohibition.

The production code cannot choose an instrument from outcomes.

CI: PASS.

### Hard production gate

File:
\`market_chi/q039_production_gate_v04.py\`

CLI:
\`tools/q039_production_preflight_v04.py\`

Tests:
\`tests/test_q039_production_gate_v04.py\`

Final test commit:
\`21372aae1d36e27fac5f9f89b586296a89142371\`

The gate cannot pass without:
1. exact external status \`APQ_EXTERNAL_STATUS=QUALIFIED\`;
2. exact prereg binding \`PREREG_COMMIT=b757d0dd65a700be1bf1d2cb5233c75c83086308\`;
3. frozen five-day source manifest;
4. frozen NC7 context rule bound to the same preregistration with adjudication provenance.

CI: PASS.

## Preserved failure and repair

The first Layer-L production test expected a four-hour delayed-target fixture to leave <8 OOS hours. That expectation was wrong: the 21-hour session still allowed a later valid refit/evaluation period.

The implementation itself had preserved the correct leakage rule.

The test was repaired to verify directly, for every refit:

\[
\max(t_{\mathrm{train,target\,end}})
\le
\min(t_{\mathrm{test,source}})
\]

rather than requiring a particular refusal outcome.

No scientific threshold or gate was weakened.

## Legacy runner quarantine

Legacy file:
\`tools/mnq_temporal_hierarchy_development.py\`

Quarantine commit:
\`c1e6afaf3cddd3fc79027839be9c3d9f65988c4d\`

It now refuses ordinary execution unless the caller explicitly supplies the historical-engineering acknowledgement flag. It cannot be mistaken for Q039 v0.4 evidence.

## Remaining scientific/external gates

### 1. Conformant external APQ

Still required.

The current transport-safe handoff with the implementation clarification is:

\`qualification/Q039_EXTERNAL_APQ_SINGLE_FILE_HANDOFF_v0.4_IMPLEMENTATION_CLARIFIED_2026-09-29.md\`

Commit:
\`84f4d930ad5b417e9c3b7a8cb1d1c19287d39eb8\`

### 2. NC7 Layer-L context rule

The preregistration does not explicitly resolve which real nonsemantic native covariates remain fixed when the L10 semantic state/targets are replaced by the isotropic matched-update-timing null.

This is now an explicit pre-outcome external-review question.

No internal choice will be made.

### 3. Frozen source identities

Run the mechanical source identity scanner on the development feature root, then freeze exactly one already-justified segment identity per date without outcome inspection.

### 4. Final production orchestration

The top-level real-data runner is intentionally not finalized across the NC7 bridge until the exact context rule is prospectively frozen.

This is a scientific firewall, not unfinished accidental plumbing.

## Current hold

Real Q039 outcomes remain CLOSED.

Q038 June 9-11 remain prohibited for Q039 tuning.

No further internal scientific work is licensed across the NC7/source/APQ gate without the external return and frozen source identity.

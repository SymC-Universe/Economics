# Q039 v0.4 Production Implementation Conformance Audit

Date: 2026-09-29
Governance: SymC GOM v1.0
Canonical preregistration:
\`b757d0dd65a700be1bf1d2cb5233c75c83086308\`

Real Q039 outcome exposure during audit: NO

## Scope

This audit compares the current repository's real-data-capable temporal-hierarchy runners against the frozen Q039 v0.4 preregistration.

Synthetic qualification modules are audited separately and remain valid only for their declared synthetic role.

## 1. Existing synthetic modules

The following are qualified synthetic/implementation components:

- \`market_chi/q039_layer_l_v04.py\`
- \`market_chi/q039_layer_r_v04.py\`
- \`market_chi/q039_nc7_v04.py\`

They implement and qualify:
- Layer-L known truths NC1-NC5;
- Layer-R known truths NC6, NC8, NC8b;
- NC7 timing/isotropic-state plumbing.

They are **not** real-data ingestion/production runners.

## 2. Existing real-data runner is not v0.4 conformant

The legacy runner:

\`tools/mnq_temporal_hierarchy_development.py\`

is an earlier development scaffold and is not authorized for Q039 v0.4 execution.

Concrete mismatches:

1. **Wrong source-state semantics**
   - reads \`bid_sz_*_mean\` / \`ask_sz_*_mean\`;
   - v0.4 requires validated L10 \`*_last\` state lineage with within-day carry-forward.

2. **Wrong coordinate ordering/semantic construction**
   - reduces directly to mean depth and side contrast;
   - v0.4 requires alternating bid/ask L10 state lineage for Layer R and raw semantic functionals \(D,I\) for Layer L.

3. **No exact carry-forward implementation**
   - v0.4 requires valid-update state retention, no pre-first backfill, no overnight carry, bad rows not overwriting state.

4. **No update/staleness state**
   - lacks \`l10_update_indicator\` and \`staleness_age_s\` controls.

5. **No Layer R production path**
   - lacks ordinary/winsorized/phase-adjusted PCA;
   - lacks lineage versus covector-consistent functional directions;
   - lacks matched-family null percentiles;
   - lacks \(\rho_1\) single-PC common-mode demotion;
   - lacks adjacent-scale k6 principal-cosine reporting.

6. **No NC7 real timing null**
   - does not preserve exact development-day update timestamps across 200 isotropic carry-forward worlds.

7. **Wrong Layer-L model stack**
   - does not implement frozen N, A2/F2, A/L/U/S nesting;
   - lacks signed-log signed-trade-volume child contrast;
   - lacks five-child P60 path decomposition.

8. **Wrong identification gate**
   - uses fixed \`min_train_blocks=30\`;
   - v0.4 requires both >=5 wall-clock hours and \(n_{train}\ge5p_{max}\).

9. **No rank/condition refusal**
   - v0.4 requires rank reporting and condition-number >1e8 descriptive exclusion.

10. **Wrong uncertainty**
    - lacks non-circular moving-block bootstrap with equal-day means;
    - lacks 30m/1h/2h sensitivity;
    - lacks 98.333% Bonferroni primary intervals.

11. **Wrong classification logic**
    - outputs R2/MAE-style development summaries;
    - does not implement frozen v0.4 pair labels or Layer-R/Layer-L independent status map.

12. **No external APQ binding**
    - runner can currently be invoked without a conformant external v0.4 APQ return.

## 3. Safety disposition

The legacy runner must not be used as Q039 v0.4 production evidence.

Disposition:

\`Q039_V0_4_PRODUCTION_RUNNER_NOT_YET_CONFORMANT\`

This is an implementation status, not a scientific result.

## 4. Required production implementation

Before any real Q039 outcome is opened, a new production runner must:

1. verify exact external APQ clearance bound to:
   \`PREREG_COMMIT=b757d0dd65a700be1bf1d2cb5233c75c83086308\`;
2. verify exact development date identities;
3. reject Q038 June 9-11;
4. reconstruct the one-second L10 \`*_last\` carry-forward state and update/staleness variables;
5. execute Layer R with the corrected v0.4 lineage/functional gates;
6. execute real-timing NC7;
7. execute Layer L with exact frozen native/semantic model nests;
8. enforce walk-forward, dynamic \(n/p\), rank, and condition-number rules;
9. freeze primary results before secondary leads/sensitivities;
10. generate a machine-readable result with explicit refusals and nonclaims.

## 5. Next licensed work

The following may proceed without real outcome exposure:

- quarantine the legacy development runner against accidental v0.4 use;
- implement a new v0.4 production runner and unit tests against synthetic fixtures;
- perform source-level conformance audit;
- run CI on synthetic fixtures only;
- freeze implementation identity after conformant external APQ return.

Real market execution remains blocked.

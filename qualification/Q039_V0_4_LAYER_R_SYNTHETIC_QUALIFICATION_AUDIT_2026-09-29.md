# Q039 v0.4 Synthetic Layer-R Qualification Audit

Date: 2026-09-29
Governance: SymC GOM v1.0
Real market outcomes used: NO
Canonical preregistration: `b757d0dd65a700be1bf1d2cb5233c75c83086308`

## Initial Layer-R run

Workflow run:
`36569170413`

Job:
`109408540330`

Initial disposition:
`LAYER_R_KNOWN_TRUTHS_PASS`

Initial artifact:
- ID `11032494725`
- SHA-256 `86b74810761c4ee0352f298931fe04e4b51de54ab2fda1d88c662dabf9d903dd`

## Post-run conformance audit

A source-level conformance audit found that the first Layer-R implementation was narrower than the frozen v0.4 preregistration.

The first implementation:
- computed functional matched-family percentiles;
- but applied phase-adjusted capture, (ho_1), and winsorized coherence effectively through the lineage direction only.

The preregistration requires structure-specific coherence for both:
- standardized-lineage directions;
- covector-consistent functional directions.

Therefore the initial PASS was preserved as execution lineage but **not accepted as final qualification evidence**.

## Correction

Correction commit:
`57e3018f0f192d68635c247a9c9f0c65c66cc152`

The corrected implementation now evaluates separately for each of:
- symmetric lineage;
- imbalance lineage;
- symmetric functional;
- imbalance functional;

including:
- ordinary capture;
- winsorized capture;
- phase-adjusted capture;
- ordinary and phase-adjusted matched-family percentile;
- ordinary and phase-adjusted (ho_1) common-mode dominance.

The pair can earn `STRUCTURE_SPECIFIC_PAIR_COHERENT_P0D` only when all four required direction/representation cells pass.

## Corrected rerun

Workflow run:
`36580967179`

Job:
`109448725669`

Unit tests:
`3 passed`

Frozen known-truth disposition:
`LAYER_R_KNOWN_TRUTHS_PASS`

Passed:
- NC6 heavy-tail no-special-structure refusal: PASS;
- NC8 calendar/common-mode refusal: PASS;
- NC8b persistent non-calendar common-mode refusal/demotion: PASS.

Corrected artifact:
- ID `11039198585`
- SHA-256 `7e1edcd0944868bb8e48ed9fc675a8cf38ffb37cd23c3976be39f7c05325f3ac`

## Disposition

`Q039_LAYER_R_SYNTHETIC_QUALIFIED_AFTER_CONFORMANCE_REPAIR`

The earlier narrower pass remains in the audit trail and is superseded as qualification evidence by the corrected rerun.

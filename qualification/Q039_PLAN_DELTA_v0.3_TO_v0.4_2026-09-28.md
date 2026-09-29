# Q039 Plan Delta v0.3 -> v0.4

Date: 2026-09-28
Governance: SymC GOM v1.0
Source preregistration: v0.3 at `fde9121072694338c5c097984e6a417a993fee3a`
Superseding candidate: `qualification/MNQ_TEMPORAL_HIERARCHY_PREREGISTRATION_DRAFT_v0.4_2026-09-28.md`
External re-review adjudication: `qualification/Q039_EXTERNAL_APQ_REREVIEW_ADJUDICATION_v0.3_2026-09-28.md`
Real Q039 outcome exposure during delta: NONE

## Material change

The v0.3 Layer-R controls did not exclude persistent non-calendar common-mode structure aligned with the canonical semantic directions. v0.4 adds a new falsifier and demotion rule before any real Q039 outcome is opened.

### NC8b

Add a persistent non-calendar common-mode known-truth world with symmetric and imbalance latent factors, no session-harmonic/calendar term, and isotropic noise.

Required outcome: it must **not** earn `STRUCTURE_SPECIFIC_PAIR_COHERENT_P0D`.

### Single-PC dominance demotion

For each canonical direction (b),

[
C_6(b)=sum_{j=1}^{6}|u_j^T b|^2,
qquad
ho_1(b)=rac{max_j |u_j^T b|^2}{C_6(b)}.
]

A direction is `COMMON_MODE_DOMINATED` when (ho_1>0.80) on at least 4/5 days in ordinary analysis and independently on at least 4/5 days in phase-adjusted analysis.

A common-mode-dominated direction cannot earn structure-specific status.

## Minor / implementation-tightening changes

1. Matched-family percentile >0.95 must hold on at least 4/5 days separately in **both** ordinary and phase-adjusted analyses for every lineage and functional direction.
2. A2 adds child2-minus-child1 signed-log signed-trade-volume contrast.
3. Report UTC-hour distribution of condition-number-excluded refits and invalid pair-days.
4. NC7 is explicitly bounded as a timing/carry-forward screen, not a full amplitude-matched market null.
5. Layer-R 4/5 rules are explicitly descriptive/coherence rules, not familywise-error-controlled tests.
6. NC6 must not grant structure-specific status to a heavy-tail world with no special canonical structure; ordinary/winsorized flips remain diagnostics rather than mandatory synthetic outcomes.
7. Mathematical notation normalized without scientific change.

## External-harness audit consequence

The supplied external v1.1 harness is retained as adversarial diagnostic evidence, not canonical implementation qualification, because functional matched-family percentiles were not actually computed and NC6 was unconditionally marked PASS.

## Scientific consequence

No Q039 claim is promoted or demoted from real data because no Q039 real outcome has been opened.

v0.4 requires:
- new external APQ binding;
- a conformant internal NC1-NC8b harness;
- frozen implementation identity;
- only then real development execution.

# Q039 + Q040 BOUNDED RECHECK ADJUDICATION
**Date:** 2026-09-30  
**Governance:** SymC GOM v1.0 + Research Continuity and Execution Protocol  
**Outcome firewall:** SEALED throughout adjudication.

## Inputs

- Claude isolated bounded recheck return, user-upload SHA-256:
  `c5bc4e9f808d3d9ca546e0eed7bf3b05fa058c435aea9ba11523ca565f989e56`
- Kimi K3 isolated bounded recheck return, archive deliverable SHA-256:
  `1d09eaaee2574a941c8a42a0e4a63ce5ac95f380a5cdb87164641e30edb60953`
- Reviewed Q039 authority:
  `1611705aa2ee75176207387598082d08a8ce56d8`
- Reviewed Q040 authority:
  `50e8587d9b440370dc13dcd170178fbce123c3fb`
- Recheck packet:
  `c7aaeeb458b0f52600610610e4f1d4904ed2c049`

Reviewer count is not used as a vote. Disagreements are resolved against the authoritative implementation chain.

## Q039 evidence resolution

Claude returned `Q039_V0_5_RECHECK=REVISE` because §9.2 names `mean spread`, `mean signed microprice offset`, and `mean native L10 imbalance`, which Claude interpreted as direct use of the extractor columns `spread_mean`, `microprice_offset_mean`, and `l10_imbalance_mean`.

That factual premise is not the Q039 production pathway.

Authoritative source verification shows:

1. `market_chi/q039_source_v04.py` requires and loads `spread_last`, `microprice_offset_last`, and `l10_imbalance_last`; it does not load the extractor `*_mean` fields.
2. `market_chi/q039_intake_v04.py` writes those `*_last` values only at valid L10 update seconds and carries them forward on the literal one-second grid.
3. `market_chi/q039_blocks_v04.py` computes `BlockRecord.mean_spread`, `mean_microprice_offset`, and `mean_l10_imbalance` as `_finite_mean` over the dense one-second carried series inside each coarse block.
4. `coarse_native_N()` consumes those `BlockRecord.mean_*` values.

Therefore §9.2's word "mean" refers to block-level means over the frozen dense carried `*_last` pathway, not to `microstructure_v2.py`'s separate row-level `*_mean` extractor columns.

**Disposition of Claude R39-2 MATERIAL objection:** `REJECTED_BY_SOURCE / DOCUMENTATION_CLARIFIED`.

No scientific redesign and no synthetic-core recomputation are required.

Kimi returned `Q039_V0_5_RECHECK=PASS_WITH_MINOR_DOCUMENTATION` and identified one genuine implementation-documentation ambiguity: how real price context is sampled for synthetic microprice recomputation.

That concern is accepted. The reviewed production formula has the exact algebraic identity

\[
m_{\mathrm{off}}
=
\frac{s}{2}
\frac{q_b-q_a}{q_b+q_a},
\]

where (s) is scaled real spread. Because Q039 already retains/carries real `spread_last`, the synthetic NC7 offset can be recomputed exactly from carried real spread plus projected synthetic L1 sizes without inventing a new price field or price model.

The Q039 v0.5 text was updated documentation-only at:

`d696bb26637392b6689460c151f77894952b54c1`

The update explicitly freezes:
- the `*_last -> dense carry -> block mean` production chain;
- the fact that extractor `*_mean` columns are not Q039 Layer-L inputs;
- the algebraically equivalent dense-grid synthetic microprice formula;
- the same one-second carry-forward rule for synthetic derived context;
- preflight coverage of the dense fields and block-level means.

**Final Q039 recheck disposition:**  
`Q039_V0_5_RECHECK=PASS_WITH_MINOR_DOCUMENTATION_CLOSED`

## Q040 evidence resolution

Claude returned:

`Q040_V0_6_RECHECK=PASS`

Kimi returned:

`Q040_V0_6_RECHECK=PASS_WITH_MINOR_DOCUMENTATION`

Kimi identified no BLOCKER or MATERIAL scientific issue. The accepted documentation corrections were:

1. restore the truncated §31 external-review transport/refusal tail;
2. repair the (T_{\mathrm{sep},S}^{*}) and (F_j) rendering in M3;
3. record the already-given PI approval of M2 + competing-risk integrated Brier score before treating R40-2 as closed.

These documentation-only corrections were applied at:

`aac0e4c57114affe86088bc26f43855e6273eaca`

No Q040 hypothesis, estimand, representation gate, refusal rule, threshold, control family, or claim ceiling was changed by this closure.

**Final Q040 recheck disposition:**  
`Q040_V0_6_RECHECK=PASS_WITH_MINOR_DOCUMENTATION_CLOSED`

## Recomputation decision

No previously qualified Q039 synthetic work is invalidated:
- NC1-NC6 remain qualified;
- NC8 and NC8b remain qualified;
- NC7 generator/timing/seed plumbing remains qualified.

Only the not-yet-run Q039 v0.5 supplemental derived-context preflight is required.

Q040 has no prior full synthetic known-truth qualification to rerun. It may now proceed into the already-authorized synthetic definition/seed freeze, implementation, and synthetic-only guarded conveyor.

## Continuity transition

The prior `EXTERNAL_BLOCK` is closed.

New lane states:

- Q039: `ADVANCED_CHECKPOINT -> SUPPLEMENTAL_DERIVED_CONTEXT_PREFLIGHT_AND_SOURCE_FREEZE`
- Q040: `ADVANCED_CHECKPOINT -> SYNTHETIC_KNOWN_TRUTH_FREEZE_AND_IMPLEMENTATION`

Real Q039/Q040 outcomes remain SEALED.

## Execution ceiling

Continue automatically through already-authorized synthetic/mechanical work.

Stop only if:
- a synthetic known-truth failure creates a scientific ambiguity;
- a required implementation parameter is not prospectively frozen and cannot be resolved mechanically from the plan;
- source/data identity cannot be established;
- a real-outcome boundary would be crossed;
- or another GOM scientific gate appears.

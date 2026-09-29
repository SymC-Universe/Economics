# Q039 v0.4 Synthetic Layer-L Qualification Audit

Date: 2026-09-29
Governance: SymC GOM v1.0
Real market outcomes used: NO
Canonical preregistration: \`b757d0dd65a700be1bf1d2cb5233c75c83086308\`

## First run: failed as evidence

Workflow run:
\`36570150590\`

Initial implementation commit:
\`aad8215d68b1fea9b1a2955ceb7fac6d68e2d1d1\`

Observed failures:
- NC2b incorrectly classified semantic ADD;
- NC4 returned an invalid/no-label path because the synthetic construction was rank deficient;
- NC5 order-specificity failed downstream of the invalid ordered-path construction.

These failures were not treated as evidence against the preregistered hypotheses because source inspection identified known-truth generator defects.

### Root cause NC2b

The declared truth is that a native activity regime drives both fine semantic variability and the future coarse state, with no semantic fine channel after native activity controls.

The first generator made the semantic contrast a relatively clean proxy for the latent regime while the native activity observables were noisy proxies. This accidentally created genuine incremental semantic information in the synthetic world, contradicting the known truth that NC2b was supposed to encode.

Repair:
- retain the latent generator;
- expose the regime exactly through one observed native-activity coordinate already present in A2;
- drive the target through that observed native coordinate;
- preserve semantic variability correlated with the same activity state.

This changes the synthetic DGP to match the frozen known truth. It does not alter the real-data model or acceptance gate.

### Root cause NC4/NC5

The first ordered-path generator constrained child paths to have zero parent-mean displacement **and** zero last-child displacement. This made the last semantic child exactly equal to the current coarse parent, causing exact collinearity when L/U/S added that child to A.

Repair:
- preserve zero-mean five-child paths so the parent mean remains fixed;
- remove the zero-last-child constraint;
- generate genuinely ordered centered paths;
- retain NC5's rule that permutations reorder only the first four children while leaving the last child fixed.

This restores identifiability while preserving the intended truth: semantic slope contains ordered information beyond last child and unordered child variability.

Repair commit:
\`2d99b9f95ce0cb2ba8fee824e374c84bd2f98117\`

## Re-run: pass

Workflow run:
\`36570658853\`

Job:
\`109413538857\`

Unit tests:
\`6 passed\`

Frozen known-truth disposition:
\`LAYER_L_KNOWN_TRUTHS_PASS\`

Passed:
- NC1 phase-only: PASS;
- NC2 coarse-sufficient: PASS;
- NC2b native activity-regime absorption: PASS;
- NC3 factor-2 semantic recency: PASS;
- NC4 ordered five-child semantic path: PASS;
- NC5 order-destruction specificity: PASS.

Artifact:
- ID \`11034246849\`;
- SHA-256 \`211020982a118808fd9faf06413a03fb81aa2828cefc39ddd21e264b352fa992\`.

## Disposition

\`Q039_LAYER_L_SYNTHETIC_QUALIFIED_AFTER_GENERATOR_REPAIR\`

The failed first run remains part of the evidence lineage. No real-data definition, threshold, or acceptance criterion was changed.

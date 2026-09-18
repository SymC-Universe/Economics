# Cross-Market Cycle Extension Plan

Date: 2026-09-18
Status: P0-D design; MNQ remains current data testbed

## Question

Does the broad break -> recovery -> sustain/fail -> transition architecture recur across materially different traded instruments while retaining ordinary wall-clock time?

The user reports the pattern across markets with different characteristic speeds and amplitudes. Small-cap/daily-high-gainer equities can move materially faster than MNQ, while instruments such as GLD may express comparable sequences more slowly.

## Time rule

Elapsed time is never rescaled. Fifteen seconds is fifteen seconds in every market.

Primary reporting remains in wall-clock units. A secondary dimensionless cycle-position or phase coordinate may be explored later if independently justified, but it never replaces the elapsed-time record.

## Minimum contrast set

A future cross-market test should include materially different market behaviors rather than several nearly interchangeable index futures. The target contrast is:
- fast episodic equity behavior, such as liquid small-cap/daily-high-gainer episodes;
- intermediate highly liquid index-futures behavior represented by MNQ;
- slower highly liquid instrument behavior represented by a GLD-like case.

Exact instruments/dates/data sources must be frozen by eligibility rules rather than selected for favorable SymC appearance.

## Common objects

Across markets, preserve the same conceptual objects where the native data permit:
- reference/baseline state;
- break/departure;
- active recovery;
- successful sustain versus failed sustain;
- repeated transition/retest;
- native flow/liquidity state;
- wall-clock duration of each state and transition.

Do not require identical microstructure fields when venues differ. The cross-market claim concerns mapped relational structure, not identical raw schemas.

## Tests

1. Compare event-state ordering and transition probabilities.
2. Compare the wall-clock duration distributions of analogous states.
3. Test whether faster local dynamics inherit/reorganize into slower chart states within each market.
4. Separate market-specific structure from any recurrent relational structure.
5. Preserve outright failures rather than forcing a universal cycle.

## Claim ceiling

MNQ can establish feasibility and development behavior only. A market-wide claim requires multiple materially different instruments and at least one system not used to design the mapping.

Cross-market normalization, if later used for a secondary phase comparison, cannot erase the primary wall-clock differences that are part of the phenomenon.

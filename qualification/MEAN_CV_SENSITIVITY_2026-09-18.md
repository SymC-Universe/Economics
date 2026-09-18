# Walk-Forward Mean-Persistence Sensitivity Map

Date: 2026-09-18
Stage: P0-Q synthetic qualification
Production chi admission changed: NO

## Purpose

Stress the promising walk-forward conditional-mean diagnostic across sample length and harder legitimate second-order cases before considering any production threshold.

## Design

Sample lengths: 300, 600, 1200, 2400.
Replicates: 50 per cell.
Existing production BIC margin: 6.

Null/non-second-order families included white noise, AR1, GARCH, pure stochastic volatility, jumps, and regime-switching AR1.

Legitimate second-order cases included baseline complex/real poles plus low-frequency, near-critical, fast-decaying, near-repeated, weak-second-root, and slow-pair cases. Each was tested with homoskedastic, GARCH, and stochastic-volatility innovations.

## Main result

Walk-forward AR2 gain remains a useful diagnostic, but **no single positive-gain threshold is scientifically valid**.

Rare production false admissions occurred among null families at every tested scale:
- n=300: 1/50 AR1 and 1/50 GARCH;
- n=600: 1/50 AR1;
- n=1200: 1/50 pure stochastic volatility;
- n=2400: 1/50 AR1.

Most of those false admissions had negative out-of-sample AR2 gain. The n=300 AR1 false admission was a near-zero positive exception (+0.00133).

However, legitimate but difficult second-order cases overlap the same region. Admitted fast-decaying complex AR2 realizations reached negative OOS gain at n=300, 600, and 1200. At n=2400 the fast-decaying complex cases became much more consistently identifiable, but an admitted weak-second-root real AR2 + GARCH realization still reached OOS gain -0.01055.

Therefore a rule such as `AR2 OOS gain > 0` would reject some legitimate second-order dynamics.

## Identifiability finding

The hard cases also expose a useful separation between **physical truth** and **finite-sample identifiability**.

The weak-second-root real case is often not admitted by the existing BIC gate at all:
- homoskedastic admission rates ranged from 0-4% across the tested sample sizes;
- GARCH/SV versions were similarly rarely admitted.

The fast-decaying complex case improved strongly with sample length, progressing from low admission at n=300 to full admission by n=2400.

This is not a failure of the refusal architecture. It shows that some true second-order systems are not identifiable as such from short/noisy windows and should legitimately be refused until sufficient evidence exists.

## Consequence

Walk-forward persistence should remain a **secondary qualification dimension**, not an independent veto. The next discrimination test is blockwise pole stability / pole-class reproducibility. A candidate future admission architecture may require multiple pieces of evidence rather than one threshold:

1. in-sample native model admission;
2. licensed pole mapping;
3. evidence that the conditional-mean structure and/or pole geometry persists across independent blocks;
4. explicit refusal when finite-sample identifiability is weak.

No production rule is changed until those pieces are jointly stress-tested.

## Provenance

Workflow: `mean-cv-sensitivity-map`
Workflow commit: `ff1735bc7ea45936638b6a05ad59d5693e63c096`

Artifacts:
- n=300 digest `sha256:32484d39a903f69e12fa7a7922b708dfe41a86df0c7565c7f71e9c70201422f4`
- n=600 digest `sha256:c965a49eb008efe074d300911e304d5207dec562e8830290e478cfd5a9f2db76`
- n=1200 digest `sha256:b9dd86812e3df64deb7494657bd845850bd563b9aa573ceedaadd1c0213bb941`
- n=2400 digest `sha256:f2bed90662a71f78775b718179d1223c915a06444f7688f69e17d9a36c96a602`

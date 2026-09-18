# Blockwise Pole-Stability Admission Audit

Date: 2026-09-18
Stage: P0-Q synthetic qualification
Production chi admission changed: NO

## Question

When the full window admits a canonical chi, does the inferred second-order pole structure recur in contiguous subwindows?

## First campaign

Configuration:
- n = 1200;
- 200 replicates per family;
- 4 contiguous blocks;
- existing BIC margin = 6;
- production engine unchanged.

The audit records blockwise AR2 support, pole-class agreement, chi licensing, and distance between block and full-window AR2 roots.

## Result

In this independently seeded campaign, the null/adversarial families produced one false chi admission: 1/200 jump-contaminated iid simulations.

That false admission had:
- block AR2 support fraction = 0.25;
- block chi-licensed fraction = 0.75;
- pole-class agreement = 0.75;
- median block/full pole distance = 0.1069.

The baseline true complex AR2 family, including GARCH and stochastic-volatility innovations, had:
- 200/200 full-window admissions;
- block AR2 support fraction = 1.0 in every replicate;
- block pole-class agreement = 1.0;
- median block/full pole distance near 0.013-0.015.

The baseline true real-pole AR2 family, including heteroskedastic innovations, also had block AR2 support fraction = 1.0 in every replicate. Its exact pole-class label was less stable: median class agreement 0.75 and some replicates as low as 0.25. This reflects finite-sample difficulty distinguishing two real roots from a nearby complex estimate and shows that exact pole-class replication would be an overly strict gate.

## Interpretation

**Blockwise AR2 support persistence is promising; exact pole-class identity is not a safe standalone criterion.**

The false jump admission failed to reproduce model support across most blocks, whereas the tested baseline true second-order processes did. But one false case is insufficient evidence for a production rule, and the baseline truths are comparatively easy.

The next step is a sensitivity map across shorter/longer samples and the harder legitimate second-order cases already used in the mean-CV campaign.

No production threshold is changed.

## Provenance

Workflow: `pole-stability-admission-audit`
Workflow commit: `e5786fa1d6ba1d2394f8384d369629a536dedec6`
Artifact digest: `sha256:a50bfb278f26d163c44dbf7bacd4e9a5f0b92698ef1f8496bdc76d2b07cbea46`

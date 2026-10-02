# Q040 Baseline Selection B2 Result

**Date:** 2026-10-02
**Authority:** Q040 Baseline Operator Plan Delta v0.2
**Authority commit:** `81f028bd7659b40dea4aed00a844a1ee36b4a36b`
**Selection bank:** B2, seed namespace `1100+r`
**Real Q040 outcomes opened:** NO
**Disposition:** `Q040_BASELINE_SELECTION_B2_PASS`

All four scale shards (15, 30, 60, 300 s) completed with exit code 0. The B2 combiner evaluated 1,512 required worlds per global candidate across the complete frozen control/scale bank.

The selected global baseline is:

- class: `K1` causal trailing robust-location baseline;
- window: `640` samples;
- refused worlds: `0`;
- minimum coverage: `1.0`;
- median coverage: `1.0`;
- median normalized baseline error: `0.867545306746059`.

The other eligible global candidates, in frozen rank order, were K1-480, K2-640, and K2-480. B2 therefore fixes **one global baseline, K1-640**, for all subsequent synthetic D1/D2 and event-definition qualification.

Combined local artifact:
`C:\Users\CCGTi\SymC_runs\q040_b2_5cf576_retry1_20261002\combined.json`

SHA-256:
`AD4C7E88B9184D36AEF1CCFAB7794E98F8A37100DD80E091E95633BA44AC1F24`

The gated successor controller verified this B2 PASS and launched the prospectively frozen E2 metric/event bank. Real Q040 outcomes remain sealed.

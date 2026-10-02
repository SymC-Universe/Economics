# Q040 Synthetic Recurrent-Event Support Audit
**Date:** 2026-10-02
**Authority:** Q040 Plan Packet v0.6 + repaired synthetic lineage v0.2
**Real Q040 outcomes:** SEALED

The repaired v0.2 semantic lineage passes its generator and observation/episode contracts, but a pre-estimator support audit found that many ordinary controls produce only 16 episodes over 4096 samples. This is not enough to support the frozen recurrent-event history comparison robustly once burden/history support is stratified, while NC-R21 is explicitly intended to be the sparse-support refusal world.

## Frozen support rule

Before estimator qualification, every non-NC-R21 synthetic control must satisfy:

- at least 40 true perturbation episodes per 4096-sample world;
- at least 10 episodes in each of four ordinal burden-support quartiles;
- for NC-R6, at least 20 positive-direction and 20 negative-direction events;
- for NC-R17, NC-R17b, and NC-R19, at least 15 events in both high- and low-regime halves of the declared driver;
- the support rule must hold at every frozen analysis scale.

NC-R21 remains frozen at 9 events and must return `INSUFFICIENT_REPEATED_EVENTS`.

This amendment changes synthetic event density only. It does not change the scientific known truth, restoring-law direction, measurement mechanics, estimator candidate grids, or real-data firewall.

`Q040_SYNTHETIC_SUPPORT_V0_2=INSUFFICIENT_FOR_FULL_ESTIMATOR`

`NEXT=FREEZE_V0_3_SUPPORT_DENSITY_AND_REQUALIFY`

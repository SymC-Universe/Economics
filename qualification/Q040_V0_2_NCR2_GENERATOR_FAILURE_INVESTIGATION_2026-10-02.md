# Q040 v0.2 Generator Failure Investigation — NC-R2
**Date:** 2026-10-02
**Stage:** repaired synthetic known-truth generator contract
**Real Q040 outcomes:** SEALED

The first v0.2 generator-contract test failed before estimator qualification.

Observed NC-R2 invariant result:
- shock count: 20;
- fraction of inter-shock intervals <=32 samples: 0.05263;
- recovery-rate span: 0.

The frozen adequacy requirement was short-interval fraction >=0.15 while preserving a constant recovery law.

This is a **synthetic truth construction failure**, not evidence about Q040. The stochastic self-excitation parameters were too weak under the frozen seed to guarantee that the world actually represented the required clustered-shock known truth.

The invariant threshold is not changed.

## Prospective repair

Replace the NC-R2 stochastic-clustering construction with a deterministic cluster topology:

- immigrant events at the ordinary base schedule (128+256k);
- each immigrant receives aftershocks at +8 and +24 samples where in bounds;
- the immigrant sign is seed-determined and inherited by its two aftershocks;
- local recovery rate remains exactly constant;
- the observed clustering-intensity proxy is a causal exponentially decayed count with decay 0.85 and no future information.

This makes clustering a property of the known truth rather than a probabilistic accident while retaining seed-dependent direction.

All downstream v0.2 generator tests restart after this repair. No estimator threshold or result has been observed.

`NC_R2_FAILURE_CLASS=SYNTHETIC_TRUTH_UNDERREALIZED`

`INVARIANT_THRESHOLD_CHANGED=NO`

`REAL_OUTCOMES_OPENED=NO`

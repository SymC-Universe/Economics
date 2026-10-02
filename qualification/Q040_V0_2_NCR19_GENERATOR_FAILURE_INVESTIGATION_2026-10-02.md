# Q040 v0.2 Generator Failure Investigation — NC-R19
**Date:** 2026-10-02
**Real Q040 outcomes:** SEALED

After the NC-R2 repair, the v0.2 generator contract advanced to NC-R19 and failed its event-history invariant.

Observed NC-R19:
- regime -> fast-history proxy correlation: 0.98989;
- regime -> observed regime proxy correlation: 0.99097;
- regime -> slower target correlation: 0.99622;
- event rate in high-regime half: 0.007324;
- event rate in low-regime half: 0.007324.

Thus the common regime strongly controlled the proxy and slower outcome but, for the frozen seed, did **not** control the actual perturbation-event rate. This would weaken the intended common-regime pseudo-propagation challenge.

The invariant is not relaxed.

## Prospective repair

NC-R19 event timing is changed to a deterministic regime-gated schedule:
- candidate event opportunities occur every 64 samples;
- an event is injected only when the latent regime is positive at that opportunity;
- signs remain seed-determined;
- the causal event-intensity proxy remains available;
- the same latent regime continues to drive the slower target and local recovery variation;
- there remains no causal fast-history -> slower-state transmission.

This guarantees that actual faster-scale perturbation history shares the common regime with slower migration.

No estimator result has been observed.

`NC_R19_FAILURE_CLASS=COMMON_CAUSE_DID_NOT_ENTER_ACTUAL_EVENT_STREAM`

`INVARIANT_CHANGED=NO`

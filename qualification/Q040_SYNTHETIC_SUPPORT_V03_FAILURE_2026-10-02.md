# Q040 Synthetic Support v0.3 Failure Record
**Date:** 2026-10-02
**Real Q040 outcomes:** SEALED

The v0.3 support-hardened candidate failed its pre-estimator test suite on NC-R19 only.

Under the frozen v0.3 seed:
- total NC-R19 events: 35;
- high-regime event rate: 0.0146484375;
- low-regime event rate: 0.00244140625.

The frozen support rule requires at least 40 total events and at least 30 high-driver / 20 low-driver events for regime controls.

All other audited controls satisfied their generator invariant and support roles. No estimator was fit and no threshold/model selection occurred.

Disposition:
`Q040_SYNTHETIC_SUPPORT_V03=FAIL_NC_R19_LOW_REGIME_SUPPORT`

Repair scope is restricted to the NC-R19 event-opportunity schedule.
# Q040 Event-History Comparator Implementation Gap Audit

**Date:** 2026-10-02
**Authority:** Q040 Recoverability Plan Packet v0.6 + Q040 Synthetic Estimator Implementation Closure v0.1
**Stage:** pre-H-bank implementation
**Real Q040 outcomes opened:** NO
**H-bank realizations opened:** NO
**Disposition:** SCIENTIFIC CONTRACT GAP / PARAMETERIZED CORE MAY PROCEED / H-BANK EXECUTION NOT YET AUTHORIZED

The final October 2 implementation closure supersedes the older decay-search language. It defines three correctly specified calibration cells: H0 background-only, H1 exponential self-excitation, and H2 queue-reactive self-excitation. It further states that kernel decay is fixed to the generator value in each cell, so H qualification tests comparator structure rather than selecting a decay.

The authoritative records do not, however, define the numerical generator values required to instantiate those cells. No frozen values were found for:
- H0 session/background coefficients or target event-rate regime;
- H1 excitation coefficient and cell-specific decay;
- H2 queue/regime coefficient, queue-proxy construction, excitation coefficient, or decay.

The records also do not uniquely define the discrete-time time-rescaling transform used for the required KS diagnostic. A continuous-time Hawkes transform cannot be silently substituted because the frozen first-cycle comparator is Bernoulli/logit in discrete time.

A sequencing ambiguity also remains. The closure requires an H configuration to produce no false M2/history-adds disposition in its corresponding null family, while §21 orders H qualification before the separate confirmatory C-bank M0/M2 stage. H structural calibration can therefore be implemented and run only after its generator contract is frozen, but final H admission cannot silently depend on an as-yet-unexecuted C-bank result unless the authority explicitly defines a two-part H qualification or reorders that check.

## Mechanically licensed implementation

The following objects are already frozen and may be implemented without opening H outcomes:
- causal excitation state `C_t = rho*C_{t-1} + I_{t-1}`;
- H0 feature family: intercept + four session-phase terms + observed activity/noise proxy;
- H1: H0 + causal excitation state;
- H2: H1 + observed queue/regime proxy;
- Bernoulli-logit event-arrival model;
- fixed ridge `1e-4`;
- diagnostics for event-rate error, excitation-coefficient error, background-intensity normalized RMSE, and probability-decile calibration.

No H-bank generator realization may be produced until the missing cell parameters and time-rescaling convention are prospectively frozen. No real Q040 outcome may be opened.

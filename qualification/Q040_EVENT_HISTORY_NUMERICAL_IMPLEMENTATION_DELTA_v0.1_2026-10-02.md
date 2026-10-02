# Q040 Event-History Numerical Implementation Delta v0.1

**Date:** 2026-10-02
**Authority:** Q040 Synthetic Estimator Implementation Closure v0.1
**Stage:** pre-H-bank implementation
**Real Q040 outcomes opened:** NO
**H-bank realizations opened:** NO

This delta closes numerical solver conventions for the already-authorized discrete-time Bernoulli/logit event-history comparator. It does not supply or alter the still-missing H0/H1/H2 generator truths, decay values, queue-proxy truth, or discrete-time time-rescaling diagnostic.

The fitted comparator uses:
- fixed ridge `1e-4` exactly as already frozen;
- intercept excluded from the ridge penalty;
- maximum 100 Newton iterations;
- convergence when gradient max-norm is <= `1e-8`;
- Newton step halving until penalized log likelihood is non-decreasing;
- refusal if information/Hessian condition number exceeds `1e10`;
- refusal on rank-deficient design, failed linear solve, nonfinite probability, absent improving step, or nonconvergence.

These solver conventions match the numerical discipline used by the frozen confirmatory competing-risk core where the model families overlap. No H-bank realization or outcome selected them.

The H-bank execution ceiling remains unchanged: the comparator core may be implemented and tested, but calibration-bank generation/execution remains blocked until the scientific contract gaps recorded in `Q040_EVENT_HISTORY_COMPARATOR_IMPLEMENTATION_GAP_AUDIT_2026-10-02.md` are prospectively closed.

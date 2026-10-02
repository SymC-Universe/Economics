# Q040 Baseline Selection Failure / Identifiability-Boundary Audit
**Date:** 2026-10-02
**Frozen selection authority:** `qualification/Q040_SYNTHETIC_ESTIMATOR_IMPLEMENTATION_CLOSURE_v0.1_2026-10-02.md`
**Real Q040 outcomes:** SEALED

## Frozen result

All four scale shards completed.

Each scale produced 2,268 baseline candidate-world scores across:
- K1/K2;
- windows 10/20/40 samples;
- NC-R5, NC-R15, NC-R16;
- all 24 NC-R20 measurement cells;
- 14 selection replicas.

The frozen combiner returned:

`Q040_BASELINE_OPERATOR_REFUSED_OR_INCOMPLETE`

with:
- no eligible candidate at 15 s;
- no eligible candidate at 30 s;
- no eligible candidate at 60 s;
- no eligible candidate at 300 s.

The provisional numerical leader at every scale was K1, 40-sample window, but it remained ineligible.

Worst K1-W40 coverage:
- 15 s: 0.34961;
- 30 s: 0.28613;
- 60 s: 0.38574;
- 300 s: 0.40869.

The global median coverage was 1.0 at each scale, demonstrating that the failure is localized rather than universal.

## Localization

Refusals are concentrated in NC-R20 cells with:
- update density = 0.20;
- gap structure = CLUSTERED.

The frozen clustered schedule has:

[
P(U_t=1mid U_{t-1}=1)=0.92.
]

For stationary update density (pi=0.20), the frozen complementary transition is:

[
P(U_t=1mid U_{t-1}=0)
=
rac{pi(1-0.92)}{1-pi}
=
0.02.
]

Thus, conditional on being in the no-update state, the expected no-update run is approximately:

[
1/0.02=50
]

samples.

The largest frozen baseline window is only 40 samples.

K1 requires at least five distinct valid updates. K2 requires at least ten. Therefore the worst-cell failure is structurally expected under the frozen measurement grid and does not arise from a numerical instability or poor median baseline error alone.

## Scientific interpretation

This result establishes a genuine measurement-identifiability boundary:

> under sufficiently sparse, clustered updates, the frozen 10/20/40-sample baseline family cannot support a baseline estimate with the required 90% coverage.

The 90% coverage criterion is not relaxed.

The failed cells are not deleted.

The current baseline family is not promoted.

## Failure investigation authorized

Before deciding whether Q040 must globally return `BASELINE_OPERATOR_REFUSED` or whether a new prospective baseline family is scientifically justified, run an **exploratory synthetic-only failure investigation** on the failed measurement regime.

Diagnostic windows:

[
Win{40,60,80,120,160,240}.
]

Evaluate both K1 and K2 on:
- the four NC-R20 20%-density clustered cells (curvature × noise grid);
- NC-R5 moving-baseline truth as the lag/bias adversary;
- all four Q040 scales.

This diagnostic is not promotion-eligible.

It asks:
1. whether 90% coverage can be recovered at all;
2. the minimum window at which it is recovered;
3. whether longer-history coverage causes unacceptable moving-baseline error.

If a defensible new family emerges, it requires:
- a documented estimator Plan Delta;
- a new frozen candidate grid;
- a **new disjoint synthetic seed bank**;
- complete requalification before D1/D2.

No completed frozen baseline result may be relabeled PASS.

`Q040_BASELINE_V0_1=REFUSED`

`FAILURE_CLASS=SPARSE_CLUSTERED_MEASUREMENT_IDENTIFIABILITY`

`NEXT=EXPLORATORY_BASELINE_WINDOW_FAILURE_SWEEP`

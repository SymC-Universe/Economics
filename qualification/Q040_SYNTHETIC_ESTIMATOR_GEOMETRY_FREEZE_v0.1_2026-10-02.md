# Q040 Synthetic Estimator Geometry Qualification Freeze v0.1
**Date:** 2026-10-02
**Authority:** Q040 Recoverability Plan Packet v0.6; Q040 Synthetic Estimator-Qualification Specification Freeze v0.1; Q040 Synthetic Lineage v0.4 Qualification
**Real Q040 outcomes:** SEALED

This freeze closes implementation details for the first half of estimator qualification only:
K1/K2 baseline -> D1/D2 metric -> event/return tuple -> finite horizon.

No M0/M2 history model is fit until this stage passes.

## 1. Synthetic lineage

Use:
- `qualification/Q040_SYNTHETIC_KNOWN_TRUTH_MANIFEST_v0.4_2026-10-02.json`;
- `market_chi/q040_synthetic_generators_v0_4.py`;
- `market_chi/q040_observation_episode_v04.py`.

All selection uses synthetic worlds only.

## 2. Replicate seeds

Geometry base seed: `20261005`.

For control ordinal (c), scale (S), replicate (r), and optional NC-R20 cell (j):

[
seed=mathrm{SeedSequence}([20261005,c,S,r,j]).
]

Baseline qualification uses 8 replicates per non-NC-R20 control/cell requested below. Event/metric qualification uses 4 replicates per control/scale. These are selection replicates, not real-data uncertainty estimates.

## 3. K1/K2 baseline implementation

Candidate horizons remain ({10,20,40}) samples.

**K1:** coordinate-wise median of actual update observations in the trailing horizon, excluding the current sample. Require at least 3 actual updates in the horizon.

**K2:** coordinate-wise OLS of actual update observations on sample time in the trailing horizon; extrapolate the fitted local line to the current sample. Require at least 10 actual updates, i.e. 5 effective observations per fitted coefficient.

Carry-forward repeats are not counted as new effective observations.

A baseline estimate is unavailable when its update-support rule fails.

Baseline velocity is the first difference of consecutive finite baseline estimates.

## 4. Baseline numerical/support gate

Evaluate candidate windows on NC-R5, NC-R15, NC-R16, and every NC-R20 measurement cell at all four scales.

Use test samples 2048–4095.

For each candidate:
- coverage = fraction of test samples with a finite baseline;
- normalized location error is
[
e_B(t)=
sqrt{rac1{8}sum_k
left[
rac{hat B_k(t)-B_{k,mathrm{true}}(t)}
{sqrt{(Sigma_0)_{kk}}}
ight]^2}.
]

A window is eligible only if coverage is at least 0.90 in every required world.

Within each class, choose the eligible window with lowest median (e_B) across all required worlds; exact ties choose the shorter horizon.

Rank surviving K1/K2 classes by that same median error; exact ties choose K1.

The ranked list is preserved. A later full-pipeline null failure may disqualify the first class and move once to the next pre-ranked class; no window is retuned.

## 5. D1

At each expanding fold, use training samples that are finite and are actual updates.

Training residual:
[
r_t=Z_{mathrm{observed}}(t)-hat B(t).
]

Coordinate center is the training median residual.

Scale is training MAD × 1.4826 with floor (10^{-8}).

Distance is robust standardized Euclidean distance.

Refuse a fold if any required center/scale is nonfinite.

## 6. D2

Use the same training residuals.

Center by training coordinate median.

Let (S=X^	op X/n), (mu=mathrm{tr}(S)/p), and (F=mu I).

Use deterministic linear shrinkage:
[
eta=
rac1{n^2}
sum_i
|x_ix_i^	op-S|_F^2,
qquad
delta=|S-F|_F^2,
]
[
alpha=
egin{cases}
1,&deltale10^{-15}\
min(1,max(0,eta/delta)),&	ext{otherwise}.
end{cases}
]

Then:
[
Sigma_{mathrm{shrunk}}
=(1-alpha)S+alpha F.
]

Refuse if:
- nonfinite;
- effective rank (<0.5p), where effective rank is entropy rank of covariance eigenvalues;
- condition number (>10^6);
- fewer than (5p) actual-update training samples.

## 7. Metric ranking

Use the highest-ranked surviving baseline class.

Metric qualification controls:
NC-R1, R2, R3, R4, R5, R6, R11, R12, R13, R15, R16, R17, R18, and R20.

For NC-R20 use the four corner cells:
- density 0.20 / IID / curvature 0 / noise 0.75;
- density 0.20 / CLUSTERED / curvature (5	imes10^{-8}) / noise 1.50;
- density 0.80 / IID / curvature (5	imes10^{-8}) / noise 1.50;
- density 0.80 / CLUSTERED / curvature 0 / noise 0.75.

Use four replicates per control/scale/cell.

For each metric and entry quantile (qin{0.95,0.975,0.99}):
- freeze the threshold from samples 0–2047;
- detect upward threshold crossings in samples 2048–4095;
- enforce a provisional 5-sample minimum separation;
- match detections one-to-one to true injected entries within ±5 samples;
- unmatched true entry penalty = 10 samples;
- false detection rate = unmatched detections / max(1, true entries).

Metric score is lexicographically:
1. median entry timing error across all q/worlds;
2. median false detection rate.

A metric must be numerically valid in at least 95% of required folds. Rank D1/D2 by score; exact ties choose D1.

The ranked metric list is preserved for one deterministic fallback after later full-pipeline null testing.

## 8. Event/return tuple

Use the highest-ranked baseline and metric.

Frozen grid:
- entry q: 0.95, 0.975, 0.99;
- return q: 0.50, 0.60, 0.70;
- sustain: 2, 3, 5 samples;
- minimum event separation: 2, 5, 10 samples.

Training thresholds use samples 0–2047 only.

Entry is an upward crossing of the frozen entry threshold satisfying minimum separation.

While an episode is active:
- sustained return is the first declared sustain run at or below the return threshold;
- a new qualifying entry before sustained return is `INTERRUPTED_BY_NEW_PERTURBATION`;
- otherwise the 80-sample provisional horizon or world end is right censoring.

Selection controls:
NC-R1–R7, R9–R13, R15–R20.

Use four replicates per control/scale; NC-R20 uses the same four corner cells.

Match estimated and true entries one-to-one within ±5 samples.

Tuple score is lexicographically:
1. median entry absolute error, with unmatched truth penalty 10;
2. median sustained-return timing absolute error, with incompatible return/nonreturn classification penalty 80;
3. median false detection rate.

Exact ties choose:
1. less-extreme entry threshold;
2. return quantile closest to 0.60, then lower numerical value;
3. shorter sustain;
4. longer minimum separation.

No outcome-specific tuple is allowed.

## 9. Horizon

Use generator truth, independent of candidate event detection.

Stable-recovery controls:
NC-R1, R2, R5, R15, R16, R20.

Evaluate CIF of true sustained return under the observed competing-event process at 20, 40, and 80 samples, excluding only entries whose full 80-sample administrative window would leave the synthetic world.

Choose 20 if, in every required world:
- (|CIF_{20}-CIF_{40}|<0.02);
- (CIF_{20}ge0.90,CIF_{80}).

Otherwise choose 40 if, in every required world:
- (|CIF_{40}-CIF_{80}|<0.02);
- (CIF_{40}ge0.90,CIF_{80}).

Otherwise freeze 80 and append:
`HORIZON_SATURATION_NOT_ESTABLISHED`.

## 10. Geometry pass/fail

PASS requires:
- at least one eligible baseline class;
- at least one eligible metric;
- a finite selected event tuple;
- a finite frozen horizon.

This stage does not establish recovery-history dependence.

Output:
`Q040_SYNTHETIC_ESTIMATOR_GEOMETRY_RESULT_v0.1.json`.

Only a PASS authorizes M0/M2 implementation and synthetic history qualification.

`Q040_REAL_OUTCOMES=SEALED`

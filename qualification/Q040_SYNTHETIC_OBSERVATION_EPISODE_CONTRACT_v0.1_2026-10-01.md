# Q040 Synthetic Observation and Episode Contract v0.1
**Date:** 2026-10-01  
**Authority:** Q040 Recoverability Plan Packet v0.6 + Q040 Synthetic Estimator-Qualification Specification Freeze v0.1  
**Stage:** synthetic-only estimator qualification  
**Real Q040 outcomes:** SEALED  
**Purpose:** map every frozen Q040 known-truth world into one common estimator-facing observed native state, event truth, recovery truth, history object, and measurement object without using real recovery outcomes.

## 1. Governing principle

The synthetic truth generator and the estimator under qualification are separated.

The generator owns:
- latent native dynamics;
- true baseline motion;
- true shock injection;
- true recovery dynamics;
- true noise law;
- true update/carry-forward law;
- true event-entry times;
- true return/interruption/censoring outcomes.

The estimator sees only the declared observed state and causal covariates.

Candidate K1/K2 baselines, D1/D2 perturbation metrics, event thresholds, return thresholds, sustain rules, horizons, and M0/M2 estimators may be scored against generator truth but may not define or alter that truth.

No Q039 outcome and no real Q040 outcome may select any parameter in this contract.

## 2. Common estimator-facing schema

Every synthetic world at every analysis scale \(S\in\{15,30,60,300\}\) seconds must return the same schema.

Required arrays:

- \`time_index[n]\`;
- \`time_seconds[n]\`;
- \`Z_latent[n,8]\`;
- \`Z_observed[n,8]\`;
- \`baseline_true[n,8]\`;
- \`displacement_true[n,8]\`;
- \`noise_cov_true[n,8,8]\` or a deterministic compact representation reconstructing it exactly;
- \`update_mask[n]\`;
- \`staleness_samples[n]\`;
- \`shock_input[n]\`;
- \`shock_direction[n,8]\`;
- \`exogenous_forcing[n]\`;
- \`session_phase[n,4]\`;
- \`native_covariates[n,k]\`;
- \`withheld_native_covariates[n,k_w]\` where a known truth requires omission;
- \`true_distance[n]\`;
- \`event_entry_true[n]\`;
- \`sustained_return_true[n]\`;
- \`interruption_true[n]\`;
- \`right_censor_true[n]\`;
- \`episode_id[n]\`;
- \`burden_count_true[n]\`;
- \`burden_amplitude_true[n]\`;
- \`burden_away_time_true[n]\`;
- \`incomplete_recovery_burden_true[n]\`.

Required metadata:

- control id;
- scale seconds;
- seed lineage;
- state dimension;
- true state-transition family;
- expected scientific disposition;
- whether exogenous forcing is observed;
- whether any native covariate is intentionally withheld;
- whether cross-scale companion truth is present;
- whether the world is a sparse-support refusal world.

If a control cannot populate the common schema coherently, it returns \`SYNTHETIC_WORLD_NOT_IDENTIFIABLE\`; no estimator rescue is allowed.

## 3. Native state dimension and coordinate roles

Primary synthetic native dimension is fixed at:

\[
p=8.
\]

The eight normalized generator coordinates are not renamed market observables, but they are assigned fixed roles matching the frozen Q040 native families:

1. depth/liquidity level;
2. depth-shape / queue-shape;
3. imbalance / directional order flow;
4. spread / microprice pressure;
5. event/activity intensity;
6. trade-volume / signed-flow pressure;
7. volatility / conditional-noise state;
8. residual native background state.

This is an estimator-qualification geometry, not a claim that real MNQ is intrinsically eight-dimensional.

The real Q040 \(Z_S(t)\) remains separately frozen at Stage Q040-3 from actual MBP10 fields.

## 4. Common latent dynamics

For ordinary controls, define latent state:

\[
Z_t^{\mathrm{latent}} = B_t + X_t,
\]

with displacement dynamics:

\[
X_{t+1}
=
A_t X_t
+
q_{t+1}u_{t+1}
+
G_\xi\,\xi_{t+1}
+
\varepsilon_{t+1}.
\]

The baseline \(B_t\), restoring operator \(A_t\), shock input \(q_tu_t\), exogenous forcing \(\xi_t\), and stochastic noise \(\varepsilon_t\) are separate generator objects.

### 4.1 Base restoring geometry

For controls not explicitly replacing the restoring law:

\[
A_t
=
Q\,
\mathrm{diag}\!\left[
\exp(-c_k r_t)
\right]_{k=1}^{8}
Q^\top,
\]

where:
- \(r_t\) is the frozen control-specific recovery-rate truth already emitted by the Q040 known-truth generator;
- \(c=(0.65,0.78,0.90,1.00,1.10,1.22,1.35,1.50)\);
- \(Q\) is a fixed deterministic orthogonal matrix generated once from seed \`20261001\` and stored in the implementation manifest.

This produces stable multirate native recovery without making one coordinate the recovery object.

### 4.2 Non-normal control

NC-R12 replaces the ordinary \(A_t\) law with the frozen stable non-normal 2D truth already present in the generator, embedded into coordinates 1–2. Coordinates 3–8 remain stable nuisance modes.

The estimator must preserve transient amplification without relabeling it instability.

## 5. Baseline truth

Unless a control declares baseline motion:

\[
B_t=0.
\]

A scalar baseline truth emitted by an existing generator is mapped along fixed normalized baseline direction:

\[
v_B
=
\frac{(1,\ 0.6,\ -0.4,\ 0.3,\ 0.2,\ -0.15,\ 0.1,\ 0.05)}
{\|\cdot\|},
\]

so that:

\[
B_t=b_t v_B.
\]

NC-R5 therefore moves the baseline while retaining the local restoring law.

Latent-regime controls may add their already-frozen baseline truth through the same \(v_B\) mapping.

No candidate K1/K2 estimate modifies \`baseline_true\`.

## 6. Noise truth

Base coordinate standard deviations are:

\[
\sigma_0
=
(0.16,0.18,0.17,0.15,0.20,0.18,0.22,0.19).
\]

Base correlation is Toeplitz:

\[
C_{ij}=0.35^{|i-j|}.
\]

For ordinary controls:

\[
\Sigma_t
=
s_t^2
\operatorname{diag}(\sigma_0)\,
C\,
\operatorname{diag}(\sigma_0),
\]

where \(s_t\) is the control-specific \`noise_scale\` divided by its nominal 0.05 reference.

If a control does not expose \`noise_scale\`, set \(s_t=1\).

NC-R16 replaces the ordinary scale law with its frozen heteroskedastic covariance-scale truth while retaining the same base correlation.

The noise law is generator truth and is never estimated from test data.

## 7. Shock truth

Existing generator \`shock[t]\` is the authoritative injected-event sequence where available.

Define base shock magnitude:

\[
Q_0=4.0.
\]

For nonzero \`shock[t]\`:

\[
q_t=Q_0|\mathrm{shock}[t]|.
\]

The signed market-direction label is:

\[
s_t=\operatorname{sign}(\mathrm{shock}[t]).
\]

Shock directions cycle deterministically through four frozen unit vectors \(u^{(1)}\ldots u^{(4)}\) generated from seed \`20261002\`, with alternating signed orientation. The vectors are stored in the implementation manifest.

NC-R6 applies its direction-specific restoring law after the signed shock enters.

No candidate perturbation metric defines true event entry.

## 8. Exogenous forcing

Where \`exog[t]\` exists, it is observed and included in the native comparator.

Its state forcing is:

\[
G_\xi \xi_t,
\]

with fixed normalized forcing direction:

\[
v_\xi
=
\frac{(0.2,-0.1,0.4,0.2,0.5,-0.3,0.15,0.1)}
{\|\cdot\|},
\]

and coefficient \(0.25\).

NC-R7 uses this observed forcing and must not produce an unconditional history claim after M0 includes it.

Unobserved forcing is not created in synthetic controls unless explicitly declared.

## 9. Latent-regime and omitted-covariate controls

NC-R17:
- the frozen latent regime drives its declared rate/baseline/shock-intensity pathways;
- \`shock_intensity_proxy\` is included in \`native_covariates\`;
- the pipeline must absorb or expose the shared-regime explanation.

NC-R17b:
- \`omitted_covariate\` drives the declared state/recovery pathways;
- it is placed in \`withheld_native_covariates\`, not in M0;
- \`apparent_history\` remains observable;
- the required outcome is comparator insufficiency/ambiguity or claim restriction, never unconditional history mechanism.

NC-R19:
- the shared regime produces both faster history and slower truth;
- cross-scale propagation must not be promoted after the frozen shared-regime comparator.

## 10. Measurement and carry-forward contract

Ordinary controls are fully observed:

\[
m_t=1.
\]

NC-R20 uses its frozen synthetic update schedule family.

Primary NC-R20 measurement grid is the Cartesian product:

- update density: \(\{0.20,\ 0.50,\ 0.80\}\);
- gap structure: \(\{\mathrm{IID},\mathrm{CLUSTERED}\}\);
- baseline curvature: \(\{0,\ 2\times10^{-5}\}\) normalized units/sample\(^2\);
- noise multiplier: \(\{0.75,\ 1.50\}\).

This yields 24 frozen cells per scale.

IID schedules use independent Bernoulli updates at the declared density.

CLUSTERED schedules use a two-state Markov update process with:
- persistence of update state \(P(U_t=1|U_{t-1}=1)=0.92\);
- the complementary transition chosen deterministically to match the declared stationary update density.

At an update, all eight native coordinates refresh together. Between updates, the previous observed state is carried forward exactly.

Before the first valid update:
- \`Z_observed\` is NaN;
- samples are invalid for estimator use.

Staleness is the integer number of samples since the last update.

No synthetic interpolation is permitted.

## 11. Generator-truth event coordinate

Candidate D1/D2 metrics do not define truth.

Define the generator-whitened displacement:

\[
d_{\mathrm{true}}(t)
=
\sqrt{
X_t^\top
\Sigma_{0}^{-1}
X_t
},
\]

where \(\Sigma_0\) is the nominal base covariance before time-varying noise multipliers.

This coordinate exists only for synthetic truth labeling.

True event entry is the injected-shock timestamp, not a threshold crossing in \(d_{\mathrm{true}}\).

## 12. True return and episode states

Freeze generator return radius:

\[
d_{\mathrm{return,true}}=1.0.
\]

Freeze generator sustain duration:

\[
K_{\mathrm{return,true}}=3
\]

consecutive samples.

For each true injected event at \(t_j\):

1. start an episode at \(t_j\);
2. search causally after entry;
3. if another true injected shock arrives before sustained return, classify the first episode \`INTERRUPTED_BY_NEW_PERTURBATION\`;
4. otherwise, the first run of 3 consecutive samples with \(d_{\mathrm{true}}\le1.0\) defines \`SUSTAINED_RETURN\`;
5. if world end occurs first, classify \`RIGHT_CENSORED\`.

True first-return time is the first sample with \(d_{\mathrm{true}}\le1.0\); true sustained-return time is the end of the first qualifying 3-sample run.

This truth rule is fixed independently of candidate return quantiles \(\{0.50,0.60,0.70\}\) and candidate sustain durations \(\{2S,3S,5S\}\).

## 13. True recovery summaries

For every episode record:

- entry displacement;
- \(T_{\mathrm{return,true}}\);
- \(T_{\mathrm{sustain,true}}\);
- interruption time;
- right-censor time;
- maximum transient amplification:
  \[
  A_{\mathrm{transient,true}}
  =
  \max_t d_{\mathrm{true}}(t)/d_{\mathrm{true}}(t_j);
  \]
- integrated true displacement until terminal event;
- recovered-side dwell where defined;
- residual true displacement at 20, 40, and 80 samples.

These are scoring truths, not estimator covariates.

## 14. History and burden truth

For episode \(j\):

\[
N_j=j-1,
\]

\[
L_j=\sum_{k<j}q_k,
\]

\[
U_j=\sum_{k<j}T_{\mathrm{away},k},
\]

where \(T_{\mathrm{away},k}\) is true time outside the generator return set before terminal event.

Freeze incomplete-recovery burden:

\[
F_j
=
\sum_{k<j}
\mathbf{1}(\text{episode }k\text{ interrupted or censored})
\,
d_{\mathrm{true}}(t_k^{\mathrm{terminal}}).
\]

These quantities are derived only from prior true episodes.

For estimator fitting, the analogous observed-history features must be constructed from prior **estimated/frozen observed episodes**, never from truth labels. Truth burdens exist only for synthetic scoring and known-disposition checks.

## 15. Native comparator covariates

The common M0 synthetic covariate object contains only information available at or before event entry:

- current observed \(Z_S(t_j)\);
- estimated baseline position and velocity from the candidate baseline;
- current candidate event amplitude;
- perturbation direction vector;
- signed market-direction label;
- previous-event elapsed time;
- session phase sin/cos terms;
- observed update/staleness state;
- current noise/activity proxy;
- observed exogenous forcing where declared;
- observed regime proxy where declared;
- recent injected/observed event intensity estimated causally from past event times.

Truth-only variables are never supplied to M0.

NC-R17b deliberately withholds its named native covariate.

## 16. Scale convention

One synthetic sample equals one analysis-scale interval.

Thus:
- at \(S=15\) s, one sample = 15 s;
- at \(S=30\) s, one sample = 30 s;
- at \(S=60\) s, one sample = 60 s;
- at \(S=300\) s, one sample = 300 s.

The normalized dynamical truth is held constant in sample units for primary qualification. This asks whether the estimator behaves correctly across the declared wall-clock scale ladder without changing the known mechanism.

A later transport test may alter rate laws by physical time, but it cannot change first-cycle qualification.

## 17. Synthetic world length and folds

Preserve the frozen generator length:

\[
n=4096
\]

samples unless a control explicitly requires otherwise.

Freeze expanding out-of-sample folds:

- initial training: samples 0–2047;
- fold 1 test: 2048–2559;
- fold 2 test: 2560–3071;
- fold 3 test: 3072–3583;
- fold 4 test: 3584–4095.

Every test fold uses only information available before its first test sample for global training objects; causal baseline updates within test folds may use past observed samples only, never future samples.

Candidate selection aggregates all required control/scale/fold cells with the already-frozen refusal and tie-break rules.

## 18. Special controls

### NC-R8 scalar refusal
Embed its frozen vector-pair truth into coordinates 1–2 and add six stable nuisance coordinates. The scalar collision is retained as a separate truth object. This control qualifies scalar refusal, not D3; first-cycle D3 remains \`NOT_APPLICABLE\`.

### NC-R12 transient amplification
Use the frozen stable non-normal 2D trajectory in coordinates 1–2 with six stable nuisance coordinates. Inject no false instability label.

### NC-R14 nested aggregation artifact
Provide paired fast and slower companion states. The slower observed process is the frozen mechanical aggregation of the fast process with no independent propagation law.

### NC-R16 heteroskedastic coordinate drift
Embed its frozen heteroskedastic 2D process in coordinates 1–2 and retain six stable nuisance coordinates with fixed covariance.

### NC-R20 measurement artifact
Use the complete 24-cell measurement grid in §10 and a recovery-memoryless latent law.

### NC-R21 sparse-tail refusal
Construct event support so at least one required primary history stratum has fewer than 10 qualifying episodes. The required result remains \`INSUFFICIENT_REPEATED_EVENTS\`.

## 19. Expected dispositions

The bridge implementation must preserve the scientific known truth of every manifest control.

At minimum:

- NC-R1: native/current state sufficient; no history ADD;
- NC-R2: true erosion direction;
- NC-R3: false-positive null; no history ADD;
- NC-R4: adaptation direction;
- NC-R5: baseline migration, not erosion;
- NC-R6: direction-dependent/mixed;
- NC-R7: exogenous/common forcing explanation;
- NC-R8: scalar refusal;
- NC-R9: true cross-scale propagation;
- NC-R10: no cross-scale propagation;
- NC-R11: slower recovery with increased resistance, not generic fragility;
- NC-R12: transient amplification with stable return;
- NC-R13: incomplete recovery/re-perturbation explanation;
- NC-R14: nested aggregation explanation;
- NC-R15: changing noise, not recovery-law change;
- NC-R16: heteroskedastic-coordinate artifact refusal;
- NC-R17: latent/shared-regime ambiguity absorbed/exposed by observed proxy;
- NC-R17b: comparator insufficiency/ambiguity due omitted native covariate;
- NC-R18: recovery and re-perturbation association handled as competing risk;
- NC-R19: shared-regime pseudo-propagation refused;
- NC-R20: matched-update-timing artifact refused;
- NC-R21: sparse-tail refusal.

## 20. Qualification gates for this contract

Before estimator selection:

1. schema passes for every control at every scale;
2. all ordinary restoring operators are stable;
3. all declared baseline/noise/shock truths are finite;
4. true event entries exactly match injected shock times;
5. episode states are mutually exclusive and exhaustive;
6. no future sample enters observed covariates;
7. NC-R20 carry-forward and staleness are exact;
8. NC-R17b withheld covariate is absent from M0-facing arrays;
9. truth labels are inaccessible from estimator-facing fields;
10. repeated generation with identical seed is byte-equivalent for numeric arrays.

Any failure returns:

\`Q040_SYNTHETIC_OBSERVATION_EPISODE_CONTRACT_FAIL\`.

Only a full pass authorizes estimator implementation.

## 21. Real-data firewall

This contract does not freeze the eventual real MNQ native vector, source dates, real perturbation thresholds, or real outcomes.

It authorizes synthetic estimator qualification only.

\`Q040_REAL_OUTCOMES=SEALED\`.

## 22. Current disposition

\`Q040_SYNTHETIC_OBSERVATION_EPISODE_CONTRACT=v0.1_FROZEN\`

\`Q040_D3=NOT_APPLICABLE_FIRST_CYCLE\`

\`NEXT=IMPLEMENT_CONTRACT_AND_RUN_SYNTHETIC_CONTRACT_PREFLIGHT\`

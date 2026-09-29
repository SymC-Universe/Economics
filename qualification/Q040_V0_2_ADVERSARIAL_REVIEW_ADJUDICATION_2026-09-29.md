# Q040 v0.2 Adversarial Review Adjudication

Date: 2026-09-29
Governance: SymC GOM v1.0
Plan reviewed: \`33c3c033b62e3f9343cdcbe768239a12f94bdbfa\`
Real Q040 outcome exposure: NONE

## Review provenance

Two independent Undermind literature agents were launched against the v0.2 APQ request:

1. \`Q040 v0.2 adversarial APQ review\`
2. \`Q040 v0.2 statistical identifiability attack\`

Both agents returned useful literature-grounded objections, but neither return is accepted as conformant external APQ clearance because the agents reported that they could not verify the supplied plan files clause by clause. Neither produced the exact required APQ footer bound to the plan identity.

Disposition of the external review process itself:

\`NONCONFORMANT_EXTERNAL_RETURN_NO_CLEARANCE\`.

The scientific objections below are nevertheless adjudicated on their merits.

## A1. Adaptive covariance can create a false perturbation/recovery signal

**Severity:** MATERIAL  
**Adjudication:** ACCEPTED.

The v0.2 candidate Mahalanobis coordinate

\[
d_S(t)
=
\sqrt{r_S(t)^\top\Sigma^{-1}r_S(t)}
\]

can change merely because the estimated covariance/noise field changes. A state-dependent or time-varying diffusion can therefore alter event entry, direction, and apparent recovery even when the deterministic restoring law is unchanged.

This is especially serious in a high-dimensional LOB where conditional variance and covariance are themselves market-state dependent.

### Required v0.3 fix

- no adaptive covariance estimated after event entry may alter that event's geometry;
- event geometry must be frozen from pre-event information;
- deterministic drift/recovery and stochastic diffusion/noise must be estimated or challenged separately;
- add a covariance/noise-drift known truth in which the restoring law is fixed but \(\Sigma_t\) changes;
- a Mahalanobis metric becomes sensitivity/candidate geometry rather than an automatically privileged primary event definition.

Relevant literature:
- Morr et al., "Anticipating critical transitions in multidimensional systems driven by time- and state-dependent noise," Phys. Rev. Research 6, 033251 (2024), DOI 10.1103/PhysRevResearch.6.033251.
- Boettner & Boers, "Critical slowing down in dynamical systems driven by nonstationary correlated noise," Phys. Rev. Research 4, 013230 (2022).

## A2. Native self-excitation comparator is too weak if its background rate is rigid

**Severity:** MATERIAL  
**Adjudication:** ACCEPTED.

A simple Hawkes-like event-history term can overstate endogenous memory when session nonstationarity, state-dependent base rates, news, or regime changes are not flexibly represented.

### Required v0.3 fix

The native history comparator must contain two distinct challenges:

1. state-dependent event-history/self-excitation;
2. flexible time-varying/background intensity or equivalent nonstationary native baseline.

History-dependent recovery earns admission only beyond both.

Relevant literature:
- Morariu-Patrichi & Pakkanen, "State-dependent Hawkes processes and their application to limit order book modelling."
- Omi, Hirata & Aihara, "Hawkes process model with a time-dependent background rate and its application to high-frequency financial data," arXiv:1702.04443.

## A3. Recurrent-event survival dependence must be explicit

**Severity:** MATERIAL  
**Adjudication:** ACCEPTED.

Repeated perturbations within an episode/day cannot be treated as independent first-event survival observations. Ignoring recurrent-event dependence can narrow uncertainty and create false precision.

### Required v0.3 fix

The final preregistration must use a recurrent-event risk-set structure appropriate to the ordered perturbation problem, with clustered/robust dependence and a frailty/random-effect sensitivity where identifiable.

The v0.3 preferred candidate is:
- gap-time ordered recurrent-event risk sets for successive perturbations;
- cluster-robust inference at minimum;
- shared-frailty sensitivity;
- explicit right censoring and competing/new-perturbation rules.

Relevant literature:
- Amorim & Cai (2015), "Modelling recurrent events: a tutorial for analysis in epidemiology," DOI 10.1093/ije/dyu222.
- Panayi & Peters (2014), survival models for bid-ask spread deviations.

## A4. Independence time is not directly identified from observational LOB trajectories

**Severity:** MATERIAL  
**Adjudication:** ACCEPTED.

The theoretical \(T_{\mathrm{ind}}\) of finite-time basin-stability theory assumes an autonomous dynamical system, a perturbation distribution, an attractor/return surface, and access to asymptotic basin stability. These are not automatically available in observational market data.

### Required v0.3 fix

- \(T_{\mathrm{ind}}\) is removed as a mandatory empirical covariate;
- the primary empirical comparator becomes **observable incomplete-recovery state** at the next perturbation;
- an empirical independence-time estimate is allowed only if a separately qualified dynamical model licenses it;
- otherwise report \`INDEPENDENCE_TIME_NOT_IDENTIFIED\`.

Relevant literature:
- Schultz et al. (2017), "Bounding the first exit from the basin: Independence times and finite-time basin stability," DOI 10.1063/1.5013127.

## A5. Non-normal transient amplification needs model-level rather than variance-only treatment

**Severity:** MATERIAL  
**Adjudication:** ACCEPTED.

Transient amplification may occur in a stable non-normal system. Raw variance or radial excursion does not identify a changing restoring law.

### Required v0.3 fix

For any dynamical recovery interpretation beyond descriptive return trajectories:
- estimate or challenge local drift/Jacobian geometry separately from diffusion;
- preserve perturbation direction;
- report transient gain/reactivity separately from asymptotic/local restoring rate;
- scalar \(\chi\) cannot be inferred from radial recovery alone.

Relevant literature:
- Arnoldi, Loreau & Haegeman (2015), DOI 10.1016/j.jtbi.2015.10.012.
- Saiprasad, Troude & Sornette (2026), "Inferring Non-Normal Amplification Geometry from Multivariate Time Series."

## A6. Cross-scale dependence needs a common-forcing null in addition to overlap controls

**Severity:** MATERIAL  
**Adjudication:** ACCEPTED.

Non-overlap or leave-child-out controls can remove mechanical aggregation leakage, but they do not exclude a common latent regime or external forcing that drives both fast recovery and slower baseline movement.

### Required v0.3 fix

Q040-H must include:
- mechanical-overlap null/control;
- common-latent-regime/common-forcing synthetic null;
- slower-scale native history;
- identifiable \(\xi(t)\) controls;
- claim wording limited to incremental temporal information, not transmission, unless stronger evidence is separately obtained.

## A7. First-cycle claim ceiling is too ambitious if it reaches basin/resistance language

**Severity:** MATERIAL  
**Adjudication:** ACCEPTED.

Observational repeated LOB trajectories can support finite-time recovery statements more readily than basin-size, transition-resistance, or global resilience claims.

### Required v0.3 fix

First-cycle primary claim ceiling is lowered to \(R_1\):

> history-dependent finite-time recovery under the frozen observation/model class.

\(R_2\) is optional and requires an independently qualified finite-shock return/escape object. Basin language is prohibited unless a native model justifies it.

\(R_3\) is outside the first-cycle primary test.

## A8. Plan-file visibility failure

**Severity:** MECHANICAL / EXTERNAL-REVIEW FAILURE  
**Adjudication:** PRESERVE.

The external literature agents did not ingest the plan in a way that permits clause-level qualification. Their results cannot unlock Q040.

A conformant external reviewer still must receive the exact v0.3 plan and return a bound disposition.

## Minor tightenings

- preserve calendar/time-of-day nonstationarity in every event-history comparator;
- explicit competing-event definition when a new perturbation arrives before recovery/censoring;
- predeclare treatment of zero/near-zero recovery duration;
- report event counts by perturbation ordinal and day before interpreting late attempts;
- retain state-dependent diffusion diagnostics even when the main recovery result is null.

## Disposition

Q040 v0.2 is superseded for plan construction.

\`REVISE_ACCEPTED_V0_3_REQUIRED\`

No real outcome has been opened and no scientific claim has been promoted.

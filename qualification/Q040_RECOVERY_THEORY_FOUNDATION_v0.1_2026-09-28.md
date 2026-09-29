# Q040 Recovery Theory Foundation v0.1

Date: 2026-09-28
Governance: SymC GOM v1.0
Stage: P0-N / A0 theory synthesis
Status: THEORY FOUNDATION COMPLETE FOR APQ REVISION; exact χ-collision search still active
Real Q040 outcome exposure: NONE

## 1. Why a recovery-theory foundation is required

Q040 does not ask a generic question about whether markets recover after shocks. It asks whether repeated perturbation changes recoverability, whether that change is distinguishable from baseline migration and ordinary state dependence, and whether any change propagates across a wall-clock hierarchy.

The recovery literature shows that "recovery" is not a single mathematical property. At minimum, a decisive design must keep distinct:

1. local/asymptotic return rate;
2. finite-time return trajectory;
3. transient amplification/reactivity;
4. resistance to displacement;
5. finite-shock basin/viability resilience;
6. repeated-shock resilience;
7. history/memory effects;
8. baseline/set-point migration;
9. adaptation versus deterioration across successive perturbations;
10. cross-scale propagation/reorganization.

Collapsing these into one scalar would reproduce a known failure mode in resilience theory.

## 2. Core dynamical-systems distinction: local recovery is not global resilience

For a local linearization around an attracting state,

\[
\dot{\mathbf{x}} = A\mathbf{x},
\]

the asymptotic recovery rate is

\[
\mathcal{R}_{\infty}
=
-\operatorname{Re}\lambda_{\mathrm{dom}}(A).
\]

This is the dominant-eigenvalue / engineering-resilience quantity.

Krakovská, Kuehn, and Longo review a wider family of resilience measures and show that local recovery measures, basin-distance measures, nonlinear return times, and parameter-change resilience can rank the same system differently. Their characteristic local return time is approximately

\[
T_R
=
\frac{1}{-\operatorname{Re}\lambda_{\mathrm{dom}}}.
\]

But basin stability under a perturbation distribution \(\rho\) is a different quantity:

\[
S_{\mathcal{B}(\mathcal{A})}(\rho)
=
\int
\chi_{\mathcal{B}(\mathcal{A})}(x)\rho(x)\,dx,
\]

the probability that a perturbed state remains in or returns to the basin of attractor \(\mathcal{A}\).

A nonlinear trajectory-aware return measure can instead integrate distance to the attractor across the whole recovery:

\[
\bar T_R(\mathcal{A},x_p)
=
\frac{1}{\operatorname{dist}(x_p,\mathcal{A})}
\int_0^\infty
\operatorname{dist}(\phi(t,x_p),\mathcal{A})\,dt.
\]

Key consequence for Q040:

> A slower observed return trajectory can establish a change in effective local recovery dynamics, but does not by itself establish a smaller basin, a lower transition threshold, or a changed global stability architecture.

Core sources:
- Holling (1973), "Resilience and Stability of Ecological Systems," DOI 10.1146/ANNUREV.ES.04.110173.000245.
- Krakovská, Kuehn & Longo, "Resilience of dynamical systems," DOI 10.1017/s0956792523000141.
- Dakos & Kéfi (2022), "Ecological resilience: what to measure and how," DOI 10.1088/1748-9326/ac5767.
- Menck et al. (2013), "How basin stability complements the linear-stability paradigm," DOI 10.1038/nphys2516.

## 3. Finite-time recovery is modal and perturbation-direction dependent

Arnoldi et al. show that multidimensional recovery cannot generally be represented by one asymptotic scalar.

For a perturbation vector \(\mathbf{u}\),

\[
\mathbf{x}(t)
=
e^{At}\mathbf{u}.
\]

They define:

\[
\mathcal{R}^{\mathrm{ins}}_t
=
-\frac{d}{dt}\ln \|\mathbf{x}(t)\|,
\]

and

\[
\mathcal{R}^{\mathrm{avg}}_t
=
-\frac{
\ln\|\mathbf{x}(t)\|
-
\ln\|\mathbf{x}(0^+)\|
}{t}.
\]

Unlike \(\mathcal{R}_\infty\), finite-time recovery depends on perturbation direction and modal composition.

Different modes can dominate different portions of the trajectory. Short-term recovery can therefore disagree with long-term asymptotic recovery.

This is especially important for Q040 because the Market program already has evidence that modal rank identity can migrate while a broader subspace remains preserved.

Theoretical implication:

> \(Χ_S(t)\) should be allowed to recover, reorganize, or transiently amplify in ways that no single scalar \(\chi_S(t)\) can faithfully represent.

Source:
- Arnoldi et al., "How ecosystems recover from pulse perturbations: A theory of short- to long-term responses," DOI 10.1101/115048.

## 4. Reactivity and non-normal transient amplification

A linearly asymptotically stable system may initially move farther away from its attractor.

Arnoldi et al. define initial resilience / reactivity through

\[
\mathcal{R}_0
=
-\frac{1}{2}\lambda_{\mathrm{dom}}(A+A^\top).
\]

For a non-normal system, \(\mathcal{R}_0\) may be negative while \(\mathcal{R}_\infty>0\).

The related numerical abscissa is

\[
\omega(A)
=
\sup \sigma
\left(
\frac{A+A^\ast}{2}
\right).
\]

If \(\omega(A)>0\), transient growth is possible even if all eigenvalues imply eventual decay.

Arnoldi et al. further define stochastic and deterministic invariability and prove, for stable linear systems,

\[
\mathcal{R}_0
\le
I_S
\le
I_D
\le
\mathcal{R}_\infty.
\]

The measures coincide for normal systems but can separate strongly in non-normal systems.

Q040 consequence:

> A temporary increase in displacement after a perturbation cannot automatically be labeled failed recovery. It may be lawful transient amplification within a still-stable modal architecture.

Sources:
- Arnoldi, Loreau & Haegeman (2015), "Resilience, reactivity and variability: A mathematical comparison of ecological stability measures," DOI 10.1016/j.jtbi.2015.10.012.
- Asllani et al., "Topological resilience in non-normal networked systems" (2017).

## 5. Repeated disturbances require a different theory from isolated shocks

Meyer et al. explicitly model repeated perturbations as a flow-kick process.

Let \(\phi_\tau(x)\) be the undisturbed flow for recovery time \(\tau\), and \(\kappa\) the discrete perturbation. Then:

\[
G_{\tau,\kappa}(x)
=
\phi_\tau(x)+\kappa.
\]

Repeated perturbation is represented by iterating \(G_{\tau,\kappa}\).

The resulting resilience boundary in \((\tau,\kappa)\) space separates disturbance sequences that remain in a basin from those that escape.

Key theoretical results:

- shock magnitude and spacing jointly determine repeated-disturbance resilience;
- distance-to-threshold can overestimate resilience when disturbances recur before full recovery;
- longer spacing is not always safer in multidimensional systems;
- repeated kicks can create an effective stability boundary that differs from the single-shock basin threshold.

Q040 consequence:

> Perturbation magnitude and inter-perturbation spacing cannot be nuisance covariates only. They are part of the native repeated-disturbance geometry and must be explicitly modeled.

Source:
- Meyer et al. (2018), "Quantifying resilience to recurrent ecosystem disturbances using flow-kick dynamics," DOI 10.1038/s41893-018-0168-z.

## 6. Independence time and incomplete recovery

Schultz et al. define finite-time basin stability:

\[
\beta_S(T)
=
\int
\mathbf{1}_{B}(x)
\Theta(T-V_S(x))
\rho(x)\,dx.
\]

This is the probability that a perturbed trajectory returns to a specified attractor neighborhood \(S\) within time \(T\).

They define an independence time:

\[
T_{\mathrm{ind}}(\epsilon,\delta)
=
\inf
\left\{
T>0
\mid
\beta-\beta_S(T)
\le\delta
\right\}.
\]

If a new perturbation arrives before \(T_{\mathrm{ind}}\), the next response is not independent of the previous recovery.

Key implication for Q040:

> "Repeated perturbation weakening recovery" cannot be inferred before distinguishing genuine changed recoverability from the simpler fact that the next perturbation arrived before the previous one had become dynamically independent.

This gives Q040 a strong native comparator: an **incomplete-recovery / independence-time burden**.

Source:
- Schultz et al. (2017), "Bounding the first exit from the basin: Independence times and finite-time basin stability," DOI 10.1063/1.5013127.

## 7. Resistance and recovery are separate components

Isbell et al. formalize resistance and recovery as distinct contributors to longer-term resilience.

Using normal level \(Y_n\), perturbed level \(Y_e\), and post-perturbation level \(Y_{e+1}\), one recovery definition is:

\[
\Delta_2
=
1-
\frac{Y_n-Y_{e+1}}
{Y_n-Y_e}.
\]

Resistance instead concerns the displacement produced by the perturbation.

The 2026 results reinforce that:
- a system can resist displacement well but recover slowly;
- a system can be displaced strongly but recover rapidly;
- long-term temporal stability and post-shock resilience need not depend on resistance/recovery in the same way.

Q040 consequence:

> Perturbation magnitude and recovery trajectory must be modeled separately. A small displacement is not evidence of strong recovery, and rapid return does not imply strong resistance.

Source:
- Isbell et al. (2026), "Predicting temporal stability and resilience from resistance and recovery," DOI 10.1038/s41586-026-10498-4.

## 8. Critical slowing down is useful but non-diagnostic

Near some bifurcations, the dominant local restoring eigenvalue approaches zero, producing slower recovery.

This motivates indicators such as:
- increased lag-1 autocorrelation;
- increased variance;
- spectral reddening;
- longer return times.

But the literature is explicit that these are not universal signatures.

False or misleading signals can arise from:
- changing noise amplitude;
- colored noise;
- nonstationarity/trend;
- multiple changing drivers;
- stepwise forcing;
- extreme-event transitions;
- stochastic resonance;
- non-normal/transient dynamics;
- cycles or chaotic dynamics.

Jäger & Füllsack show that ordinary growth/decay trends can create systematic false-positive increases in both variance and autocorrelation.

Nazarimehr et al. show that recovery rate and basin resilience can move out of harmony.

Q040 consequence:

> Increasing autocorrelation or slowing return cannot be used alone to label a market state as approaching a transition.

Sources:
- Nazarimehr et al. (2020), "Critical slowing down indicators."
- Jäger & Füllsack (2019), "Systematically false positives in early warning signal analysis," DOI 10.1371/journal.pone.0211072.
- Kuehn (2011), "A mathematical framework for critical transitions," DOI 10.1016/j.physd.2011.02.012.
- Dakos et al. (2024), "Tipping point detection and early warnings in climate, ecological, and human systems," DOI 10.5194/esd-15-1117-2024.

## 9. Moving baselines must be separated from changing recovery

A 2026 regression-based resilience framework for nonstationary systems writes:

\[
\frac{\Delta x_i}{\Delta t_i}
\approx
-\lambda x_i
+
\left[
\lambda\mu(t_i)
+
\frac{d\mu}{dt}(t_i)
\right]
+
\epsilon_i,
\]

where:
- \(\lambda\) is the recovery rate;
- \(\mu(t)\) is the moving attractor/baseline.

This directly formalizes the distinction Q040 needs:

\[
\text{changing baseline}
\neq
\text{changing recovery rate}.
\]

Q040 consequence:

> \(B_S^{(r)}(t)\) should not merely be detrended away. Baseline motion and recovery toward the pre-perturbation baseline should be estimated as separate objects.

Source:
- Smith et al. (2026), "Estimating the Resilience of Non-Stationary Systems," arXiv:2604.24345.

## 10. Memory can slow recovery while increasing resistance

This is one of the most important theoretical warnings for Q040.

Khalighi et al. model memory using a Caputo fractional derivative:

\[
\mathcal{D}^{\alpha}x
=
F(x,t),
\qquad
0<\alpha\le1,
\]

with stronger memory as \(\alpha\) decreases.

They report that memory can:
- flatten basin floors;
- slow recovery;
- increase the perturbation threshold required for a regime transition;
- broaden hysteresis;
- generate delayed collapse;
- generate delayed recovery;
- produce rebound after apparent recovery.

Therefore:

\[
\text{slower recovery}
\not\Rightarrow
\text{less resistance to state transition}.
\]

A system can recover more slowly while being harder to knock into another basin.

This directly blocks an overstrong Q040 interpretation.

Source:
- Khalighi et al. (2026), "Memory reshapes stability landscapes: resilience-resistance tradeoffs and critical transitions," arXiv:2602.20365.
- Khalighi et al. (2021/2022), "Quantifying the impact of ecological memory on the dynamics of interacting communities," DOI 10.1371/journal.pcbi.1009396.

## 11. Successive disruptions can show adaptation, deterioration, or regime changes in learning

Steijn et al. introduce an adaptation metric across successive disruptions.

For a disruption-level performance measure fitted as:

\[
f(n)
=
a e^{-bn}+c,
\]

they define an adaptation direction/rate:

\[
\alpha
=
\operatorname{sgn}(a)b.
\]

Positive and negative \(\alpha\) distinguish improvement from deterioration across successive disruptions.

Their framework emphasizes:
- at least three disruptions for this parametric fit;
- event segmentation is itself a major source of uncertainty;
- adaptation need not be monotonic;
- one metric can show adaptation while another shows deterioration.

Q040 consequence:

> The experiment must preserve adaptation/strengthening as an explicit opposite-direction outcome, and no "3-5 attempts" threshold may be hard-coded from trader experience.

Source:
- van Steijn et al. (2026), "A metric for quantifying adaptation to successive disruptions," DOI 10.1038/s41598-026-52678-2.

## 12. Homeostasis/allostasis supports moving operating points, not simple return-to-old-state

The allostasis literature distinguishes:
- homeostasis: maintaining essential regulated variables;
- allostasis: stability through change;
- allostatic state: operation at a shifted set point/operating level;
- allostatic load/overload: cumulative cost of repeated adaptation.

This literature is relevant to the user's prior human observation but cannot be directly imported as a market mechanism.

Its useful theoretical lesson is:

> "Recovery" need not mean exact restoration of the old baseline. A stable system may reorganize to a new operating state.

Q040 consequence:

- exact return-to-old-baseline is one outcome;
- stable baseline migration is another;
- maladaptive drift is another;
- these must not be conflated.

Source:
- McEwen & Wingfield (2010), "What's in a name? Integrating homeostasis, allostasis and stress," DOI 10.1016/j.yhbeh.2009.09.011.

## 13. Market-specific prior art already contains phase transitions and multiscale fragility

The market literature removes several broad novelty claims.

Fosset, Bouchaud & Benzaquen report a second-order phase transition from stable to unstable liquidity under feedback in a stylized order-book model.

Corradi, Zaccaria & Pietronero show that liquidity fragility behaves differently at 30 s and 15 min scales.

Novotný (2026) maps a liquidity-stress crossover in an order-book agent model with a scalar order parameter defined by one-sided book events.

Therefore Q040 cannot claim novelty for:
- a scalar market order parameter;
- a market stability threshold;
- market phase-transition language;
- multiscale liquidity fragility;
- a recovering/refilling order book.

Sources:
- Fosset, Bouchaud & Benzaquen (2019), "Endogenous liquidity crises," DOI 10.1088/1742-5468/ab7c64.
- Corradi, Zaccaria & Pietronero (2015), "Liquidity crises on different time scales," DOI 10.1103/PhysRevE.92.062802.
- Novotný (2026), "Herding and Liquidity in Order-Book Markets I: A Robust Liquidity-Stress Crossover and its Reflexive Mechanism," arXiv:2607.08907.

## 14. Existing SymC / \(\chi\) prior art must be counted as prior art

Christensen (2026) already establishes the dimensionless damping coordinate

\[
\chi
\equiv
\frac{\gamma}{2|\omega|}
\]

as an exceptional-point / critical-damping stability coordinate in the physical systems treated there, with

\[
\chi=1
\]

marking the critical boundary for that admitted class.

Therefore Q040 cannot claim novelty for inventing \(\chi\) as a stability-phase coordinate.

The unresolved Market question is much narrower:

> Does Market admit any scalar \(\chi_S(t)\) with a mathematically licensed phase/recovery interpretation at all, and if it does, does it add nonredundant information alongside modal/vector \(Χ_S(t)\) and architecture-level \(Χ_{\mathrm{arc},S}(t)\)?

Current MNQ production evidence still REFUSES the canonical scalar \(\chi\).

Source:
- Christensen (2026), "Exceptional-point stability boundaries from quantum dissipation to cosmological acceleration," DOI 10.1038/s41598-026-56887-7.

## 15. Recovery-theory implications for \(\chi\), \(Χ\), and \(Χ_{\mathrm{arc}}\)

The literature suggests a natural anti-circular qualification structure.

### 15.1 Candidate \(\chi_S^*(t)\)

A scalar candidate may encode a local transition/recovery coordinate only if:
- a native low-dimensional model licenses scalarization;
- the scalar has prospective relation to regime/recovery outcomes;
- it remains informative beyond trivial price displacement/volatility;
- scalar admission survives perturbation-direction and moving-baseline controls.

No scalar is admitted by analogy.

### 15.2 \(Χ_S(t)\)

Recovery theory strongly motivates a modal/vector layer because:
- finite-time recovery is direction dependent;
- different modes dominate different times;
- non-normal systems can transiently amplify;
- scalar asymptotic recovery can miss the actual transient path.

### 15.3 \(Χ_{\mathrm{arc},S}(t)\)

Architecture-level organization should only be invoked if:
- multiple admitted components interact in a reproducible way;
- the conglomerate adds out-of-sample value beyond its components/native baselines;
- it is constructed entirely from information available before the outcome.

Future rejection/rebound/transition remains the test target:

\[
Y_S(t+\Delta),
\]

not part of the definition of \(Χ_{\mathrm{arc},S}(t)\).

## 16. Claim ladder justified by theory

### Level A: changing observed recovery

Supported if later matched perturbations show different recovery trajectories after current-state controls.

Allowed statement:
> Effective finite-time recovery dynamics changed across successive perturbations.

### Level B: history-dependent recoverability

Requires history variables to add prospective value beyond:
- current perturbation state;
- spacing;
- baseline motion;
- order-flow memory/self-excitation;
- activity/liquidity/volatility;
- direction.

Allowed statement:
> Recovery is history-dependent under the frozen observation/model class.

### Level C: changing finite-shock resilience

Requires additional nonlocal evidence such as:
- changed probability of return within \(T\);
- changed transition/escape threshold;
- changed finite-time basin/viability measure;
- changed exit-time distribution.

Allowed statement:
> Finite-shock recoverability/resilience changed.

### Level D: stability-architecture reorganization

Requires:
- admitted representation change in \(\chi\), \(Χ\), and/or \(Χ_{\mathrm{arc}}\);
- nonredundant relation to recovery/transition outcomes;
- controls against moving baseline, forcing, and memory-only alternatives;
- prospective evidence that the architecture change precedes the later recovery/transition difference.

Only then may Q040 discuss:
> Stability Architecture reorganization.

Repeated slower recovery alone does **not** license Level D.

## 17. Required Q040 Plan Delta

Before external APQ freeze, Q040 should add:

1. a formal distinction between resistance, recovery rate, finite-time return, and finite-shock resilience;
2. reactivity/transient amplification metrics for \(Χ\);
3. an independence-time or incomplete-recovery burden comparator;
4. simultaneous moving-baseline/recovery estimation or a strong equivalent challenge;
5. a history/memory comparator that can produce slower recovery with greater transition resistance;
6. explicit finite-time basin/return-probability criteria before using "loss of resilience" language;
7. adaptation/strengthening as a symmetric alternative;
8. a claim ladder matching Section 16;
9. a known-truth world in which recovery slows while the transition threshold increases;
10. a known-truth world in which transient amplification occurs but asymptotic recovery remains stable;
11. a known-truth world in which baseline migration mimics slowing recovery;
12. a known-truth world in which shocks arrive before the independence time and create apparent cumulative degradation without a changed local return law.

## 18. Current theoretical disposition

The theory **supports using successive recovery trajectories as evidence about changing effective dynamics**, provided perturbations and state are made comparable.

The theory **does not support treating slower successive recoveries as proof of a shrinking basin, lower phase threshold, or global stability loss without additional evidence**.

The most defensible Q040 target is therefore:

> determine whether repeated perturbation produces a prospective, nonredundant change in finite-time recovery dynamics; determine whether that change is explained by incomplete recovery, moving baselines, memory, clustering, or native state; and only then test whether independently qualified \(\chi\), \(Χ\), or \(Χ_{\mathrm{arc}}\) representations change in a way that precedes finite-shock resilience or slower-scale baseline reorganization.

This is narrower than the original intuitive claim and substantially more falsifiable.


## 19. Provenance and intended role of \(\chi\)

The use of \(\chi\) in this program is not motivated by a novelty claim about the symbol or the damping-ratio mathematics.

The research origin is the opposite: an already established mathematical stability coordinate was adopted deliberately because the researcher observed a continuous qualitative pattern and wanted the interpretation anchored to existing dynamical mathematics rather than defined retrospectively from the observed outcomes.

Accordingly, the Market question is a **transport/qualification problem**:

> Does the native market system admit a mathematically defensible dynamical reduction in which an established \(\chi\)-type stability coordinate retains its legitimate meaning?

For the canonical physical form,

\[
\chi
=
\frac{\gamma}{2|\omega|},
\]

the quantities \(\gamma\) and \(\omega\) must be independently identifiable from a native dynamical model. EMA, VWAP, MACD, L2 variables, or price patterns cannot simply be renamed \(\gamma\), \(\omega\), or \(\chi\).

A valid Market \(\chi_S(t)\) therefore requires one of the following:

1. a native market model that genuinely yields the same damping/frequency structure and therefore the canonical coordinate directly; or
2. a mathematically explicit generalized coordinate whose relationship to the canonical \(\chi\) is derived rather than asserted.

If neither route survives model qualification, scalar \(\chi\) remains REFUSED and the Market architecture proceeds through \(Χ\) and, if earned, \(Χ_{\mathrm{arc}}\).

The potential scientific novelty is therefore not "using \(\chi\)." It would lie, if supported, in demonstrating that established stability mathematics transports nontrivially into a new empirical system and interacts prospectively with repeated recovery, modal organization, and cross-scale dynamics. That novelty remains subject to the dedicated collision search and must not be presumed.

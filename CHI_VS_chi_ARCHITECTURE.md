# Chi vs chi in SymC Market Research

Status: Working architecture note
Branch: `market-chi-architecture`
GOM baseline: v0.8.0

## 1. Working distinction

### lowercase chi

`chi` is a local, scalar, or mode-specific coordinate that is emitted only when a licensed dynamical construction supports it.

For a licensed second-order factor,

`chi = gamma / (2 omega_0)`.

Equivalent pole form for an admitted stable complex-conjugate pair `lambda = a +/- ib`:

`chi = -Re(lambda) / |lambda|`.

Lowercase chi therefore answers a relatively narrow question:

> Where does this admitted dynamical factor lie relative to its own stability structure?

It does not by itself answer how the entire market is organized.

### capitalized Chi

`Chi` is the working name for the broader reconstructed stability architecture of the market system.

It is not presently defined as one scalar equation. It is a structured scientific object reconstructed from the relationships among admitted lower-level representations and may include, where supported:

- scalar coordinates, including lowercase chi where licensed;
- modal/vector structure;
- conglomerate/network organization;
- coupling and participation;
- inheritance and transformation across scale;
- feedback and propagation;
- recovery and resilience;
- emergence and suppression;
- function and limit structure.

Open-channel residuals, uncertainty, observability, and identifiability remain mandatory Tool outputs and safeguards, but they are not automatically declared components of Chi.

Working conceptual direction:

`native market observables -> admitted local/modal structure -> lowercase chi where licensed -> coupling and system organization -> emergent/reconstructed Chi`

This is an investigation path, not an asserted closed-form identity.

## 2. Why the oscillator cannot remain the foreground

The earlier market framework treated damped oscillation as the main organizing model. That was useful because a second-order system gives an explicit stability coordinate and a clear boundary, but it is too restrictive as the ontology of the market project.

The revised interpretation is:

> damped oscillation is one possible consequence of an admitted local dynamical factor inside the larger Chi architecture.

If the native market data support a second-order factor, lowercase chi becomes available for that factor. If they do not, the Engine may still return valid modal, network, coupling, regime, and recovery structure while refusing scalar chi.

This prevents the framework from forcing every market state into an oscillator merely because the original SymC mathematics began there.

## 3. Literature collision supports this change

Oscillator-based financial models already exist, so oscillator-first framing is neither necessary nor a strong residual novelty target.

Examples:

1. Sandoval Junior and Franca (2011), *Shocks in financial markets, price expectation, and damped harmonic oscillators*, models post-shock market response using a modified damped oscillator.
   - https://arxiv.org/abs/1103.1992

2. A 2020 Physica A paper, *Forecast model for financial time series: An approach based on harmonic oscillators*, uses a damped driven harmonic oscillator with restoring force, inertia, and dissipation for price forecasting.
   - https://doi.org/10.1016/j.physa.2020.124365

3. Oliveira, Raad, and de Magalhaes (2026), *Coupled Harmonic Oscillators Model for Financial Time Series*, uses linearly coupled dissipative harmonic oscillators for Ibovespa assets and estimates damping coefficients and spring constants.
   - https://doi.org/10.63801/rmat.v1i1.8528

These works make damped dynamics legitimate prior art to compare against, but they also show why the broader SymC contribution should not be reduced to an oscillator analogy.

## 4. Native market science already contains the other architecture layers

The literature independently supports several structures that align naturally with a broader Chi investigation without assuming they are SymC-specific.

### Modal/vector structure

Random-matrix and correlation-spectrum work shows that return correlation matrices contain a noisy bulk plus non-random eigenmodes, including collective market and sector structure. This gives a native route to modal participation and system organization.

Representative sources:

- Plerou et al. (2000), *A random matrix theory approach to financial cross-correlations*.
  https://doi.org/10.1016/S0378-4371(00)00376-9
- Bouchaud and Potters, *Financial applications of random matrix theory: a short review*.
  https://doi.org/10.1093/oxfordhb/9780198744191.013.40

### Conglomerate/network structure

Financial-network research treats stability and systemic risk as properties of interacting institutions and markets rather than isolated scalar states. Links can diversify risk or propagate shocks, and higher-order/network-of-networks structure can materially alter system behavior.

Representative sources:

- Jackson and Pernoud (2021), *Systemic Risk in Financial Networks: A Survey*.
  https://doi.org/10.1146/annurev-economics-083120-111540
- Bardoscia et al. (2021), *The physics of financial networks*.
  https://doi.org/10.1038/s42254-021-00322-5
- Gofman, Herskovic, and Segal (2026), *Networks in Finance: Foundations and Frontiers*.
  https://doi.org/10.1146/annurev-financial-111824-015225

### Native directional and microstructure channels

Order-flow imbalance has a direct empirical relation to short-horizon price changes and market depth. This supports treating direction/flow as a native channel rather than assuming sign is encoded by scalar stability magnitude.

- Cont, Kukanov, and Stoikov, *The Price Impact of Order Book Events*.
  https://doi.org/10.1093/jjfinec/nbt003

### Regime and transition structure

Financial regime detection is a large native field using Markov-switching, hidden-state, change-point, volatility, liquidity, and other definitions. A 2026 systematic review highlights severe definitional and validation heterogeneity, reinforcing the need to freeze the exact target and comparator rather than using an undefined 'market regime'.

- Jalil, Jabbar, and Fayyaz (2026), *What Are Market Regimes? Definitional Chaos, Validation Failure, and a Path Toward Methodological Convergence*.
  https://doi.org/10.2139/ssrn.6493762

## 5. Provisional architecture

The current working representation is not a final decomposition. It is a scaffold for investigation.

### Layer S: scalar/local

Possible contents:

- mode-specific lowercase chi where licensed;
- local decay or recovery rates;
- native volatility/liquidity coordinates;
- scalar proxies explicitly labeled as such.

### Layer M: modal/vector

Possible contents:

- poles/eigenvalues;
- characteristic frequencies and timescales;
- modal damping/decay;
- eigenvectors;
- participation factors;
- factor/correlation modes;
- order-flow or liquidity modes where supported.

### Layer C: conglomerate/system

Possible contents:

- cross-asset coupling;
- sector and market modes;
- correlation/network topology;
- higher-order interactions;
- liquidity synchronization;
- contagion/propagation pathways;
- feedback and concentration.

### Relational structure

The primary Chi research questions are then relational:

- Which local properties survive embedding in the market?
- Which are transformed by coupling?
- Which disappear?
- Which system properties emerge only after interaction?
- When is scalar compression adequate?
- When must the Tool remain modal or network-valued?
- What changes first as resilience erodes?
- Which structures predict recovery, transition, or failure beyond native baselines?

## 6. Working mathematical representation

Do not define capitalized Chi as an arithmetic average or a fixed weighted score.

A safe working representation is a structured state object:

`Chi_t = Architecture(S_t, M_t, C_t; relationships, hierarchy, validity regime)`

where:

- `S_t` is the admitted scalar/local representation;
- `M_t` is the admitted modal/vector representation;
- `C_t` is the admitted conglomerate/system representation.

The `Architecture` operator is intentionally not assigned a closed form yet. Discovering whether a valid compression, manifold, graph object, tensor object, state-space representation, or other relation is supported is part of P0-D/P0-Q research.

This preserves the GOM rule that scalar, vector/modal, and conglomerate are starting representation components rather than a final decomposition of chi.

## 7. Consequence-first oscillator interpretation

The oscillator route now becomes conditional:

`native system identification -> admitted second-order factor -> poles/omega/gamma -> lowercase chi -> contribution to Chi`

not:

`assume oscillator -> compute chi -> call result market stability`.

If a second-order factor is not admitted, the correct output is not an invented chi. The correct result may be modal structure without chi, another native stability object, or refusal.

## 8. Research tests created by the distinction

The distinction itself becomes falsifiable through several questions:

1. Does lowercase chi add information beyond the full native pole/modal representation, or is it merely equivalent compression?
2. Do modal and conglomerate features improve diagnosis or prediction beyond lowercase chi alone?
3. Are there market states where scalar chi fails but modal/network organization remains stable and informative?
4. Does local chi survive embedding into sector and market coupling, or is it transformed?
5. Can a higher-level system scalar ever be derived without unacceptable information loss?
6. Does the combined architecture improve a frozen native task beyond standard financial methods on untouched evidence?
7. Does a damped-oscillator factor emerge only in particular regimes, horizons, instruments, or post-shock recoveries?

## 9. Current claim ceiling

At this stage:

- lowercase chi: dynamically derived only where an admitted model licenses it;
- capitalized Chi: working project-level architecture concept, not yet a validated physical quantity or universal law;
- damped oscillator: candidate special case / consequence;
- market-wide scalar Chi: not established;
- predictive value of Chi architecture: not tested prospectively;
- common mechanism across markets and other SymC domains: not established by mathematical resemblance alone.

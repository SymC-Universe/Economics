# χ, Χ, and Χ_arc in SymC Market Research

Status: Working architecture note
Branch: `market-chi-architecture`
GOM baseline: v1.0

## 1. Working distinction

### χ

χ is a local, scalar, or mode-specific coordinate that is emitted only when a licensed dynamical construction supports it.

For a licensed second-order factor:

`χ = γ / (2ω₀)`.

For an admitted stable complex-conjugate pole pair `λ = a ± ib`:

`χ = -Re(λ) / |λ|`.

χ answers a relatively narrow question: where does this admitted dynamical factor lie relative to its own stability structure? It does not by itself describe the organization of the entire market.

### Χ

Χ is the modal/vector stability representation. It is the capital-chi object used to represent admitted multi-coordinate modal structure when scalar compression to χ is inadequate or refused.

Χ may include, where supported, eigenmodes/eigenvectors, characteristic timescales, modal decay or damping, participation, semantic directions, fixed-k subspaces, and other qualified vector-valued structure. Χ is not the whole-system architecture and must not be used as a synonym for overall organization.

### Χ_arc

Χ_arc is the higher-level architecture/conglomerate representation: the overall organization of the system across admitted scalar, modal/vector, relational, coupling, hierarchy, network, recovery, inheritance, and reorganization structure.

Χ_arc is not presently defined as one scalar equation. It is a structured scientific object reconstructed only where the lower-level objects and their relationships are independently qualified.

Open-channel residuals, uncertainty, observability, and identifiability remain mandatory outputs and safeguards, but they are not automatically declared components of Χ or Χ_arc.

Canonical working direction:

`native market observables -> χ where locally licensed + Χ where modal/vector structure is admitted -> relational/coupling organization -> Χ_arc where overall architecture is independently qualified`

This is an investigation path, not an asserted closed-form identity.

## 2. Why the oscillator cannot remain the foreground

The earlier market framework treated damped oscillation as the main organizing model. That was useful because a second-order system provides an explicit stability coordinate and a clear boundary, but it is too restrictive as the ontology of the market program.

The revised interpretation is: damped oscillation is one possible consequence of an admitted local dynamical factor. Such a factor may contribute to modal/vector Χ, which may in turn contribute to a separately qualified Χ_arc architecture.

If native market data support a second-order factor, χ becomes available for that factor. If they do not, the Engine may still return valid modal, network, coupling, regime, and recovery structure while refusing scalar χ.

## 3. Prior-art collision reinforces the change

Oscillator-based financial models already exist, so oscillator-first framing is neither necessary nor a strong residual novelty target.

Representative examples:

1. Sandoval Junior and Franca (2011), *Shocks in financial markets, price expectation, and damped harmonic oscillators*. https://arxiv.org/abs/1103.1992
2. *Forecast model for financial time series: An approach based on harmonic oscillators* (Physica A, 2020). https://doi.org/10.1016/j.physa.2020.124365
3. Oliveira, Raad, and de Magalhaes (2026), *Coupled Harmonic Oscillators Model for Financial Time Series*. https://doi.org/10.63801/rmat.v1i1.8528

These works make damped dynamics legitimate prior art to compare against, while leaving modal/vector Χ and the separately qualified Χ_arc architecture as the broader research targets.

## 4. Native market science already supplies candidate architecture layers

### Modal/vector structure

Random-matrix and correlation-spectrum work shows that return correlation matrices contain collective non-random modes in addition to noisy structure.

Representative sources:

- Plerou et al. (2000), *A random matrix theory approach to financial cross-correlations*. https://doi.org/10.1016/S0378-4371(00)00376-9
- Bouchaud and Potters, *Financial applications of random matrix theory: a short review*. https://doi.org/10.1093/oxfordhb/9780198744191.013.40

### Conglomerate/network structure

Financial-network research treats systemic behavior as a property of interacting institutions and markets rather than isolated scalar states.

Representative sources:

- Jackson and Pernoud (2021), *Systemic Risk in Financial Networks: A Survey*. https://doi.org/10.1146/annurev-economics-083120-111540
- Bardoscia et al. (2021), *The physics of financial networks*. https://doi.org/10.1038/s42254-021-00322-5
- Gofman, Herskovic, and Segal (2026), *Networks in Finance: Foundations and Frontiers*. https://doi.org/10.1146/annurev-financial-111824-015225

### Native directional and microstructure channels

Order-flow imbalance has a direct empirical relation to short-horizon price changes and market depth. This supports treating direction/flow as a native channel rather than assuming sign is encoded by scalar stability magnitude.

- Cont, Kukanov, and Stoikov, *The Price Impact of Order Book Events*. https://doi.org/10.1093/jjfinec/nbt003

## 5. Provisional architecture

The current working representation is not a final decomposition.

### S: scalar/local
Possible contents include mode-specific χ where licensed, local decay/recovery rates, native volatility/liquidity coordinates, and explicitly labeled proxies.

### M: modal/vector
Possible contents include poles/eigenvalues, characteristic frequencies/timescales, modal damping/decay, eigenvectors, participation, factor/correlation modes, and order-flow or liquidity modes where supported.

### C: conglomerate/system
Possible contents include cross-asset coupling, sector and market modes, correlation/network topology, higher-order interactions, liquidity synchronization, contagion pathways, feedback, and concentration.

### Relational structure
The primary Χ_arc questions are relational: which local properties survive embedding, which transform through coupling, which disappear, which emerge only after interaction, when scalar compression is adequate, when the Tool must remain modal/network-valued, what changes first as resilience erodes, and which structures predict recovery, transition, or failure beyond native baselines.

## 6. Working representation

Do not define Χ or Χ_arc as an arithmetic average or fixed weighted score.

A safe working distinction is:

`Χ_t = ModalVector(M_t; admitted modes, subspaces, participation, validity regime)`

`Χ_arc,t = Architecture(S_t, Χ_t, C_t; relationships, hierarchy, coupling, recovery, validity regime)`

The `ModalVector` and `Architecture` operators intentionally have no universal closed form yet. Determining whether a valid compression, manifold, graph object, tensor object, state-space representation, or other relation is supported is part of P0-D/P0-Q research.

## 7. Consequence-first oscillator route

`native system identification -> admitted second-order factor -> poles/ω/γ -> χ -> contribution to Χ where modal/vector embedding is supported -> possible contribution to Χ_arc`

not:

`assume oscillator -> compute χ -> call result market stability`.

If a second-order factor is not admitted, the correct output may be modal structure without χ, another native stability object, or refusal.

## 8. Research tests created by the distinction

1. Does χ add information beyond the full native pole/modal representation, or is it merely equivalent compression?
2. Does modal/vector Χ improve diagnosis or prediction beyond χ alone, and does Χ_arc add beyond χ and Χ?
3. Are there market states where scalar χ fails but modal/vector Χ remains stable and informative?
4. Does local χ survive embedding into sector and market coupling, or is it transformed?
5. Can a higher-level system scalar ever be derived without unacceptable information loss?
6. Does reconstructed Χ_arc improve a frozen native task beyond native and modal/vector Χ alternatives on untouched evidence?
7. Does a damped second-order factor emerge only in particular regimes, horizons, instruments, or post-shock recoveries?

## 9. Current claim ceiling

- χ: dynamically derived only where an admitted model licenses it;
- Χ: modal/vector stability representation, admitted only when multi-coordinate modal structure is independently supported;
- Χ_arc: overall architecture/conglomerate representation, separately qualified above χ and Χ and not yet a validated universal physical quantity or law;
- damped oscillator: candidate special case / consequence;
- market-wide scalar Χ or Χ_arc: not established;
- predictive value of Χ and Χ_arc: not established prospectively outside their bounded qualified tasks;
- common mechanism across markets and other SymC domains: not established by mathematical resemblance alone.

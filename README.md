# SymC Market Stability Architecture

Branch: `market-chi-architecture`
GOM baseline: v0.8.0
Stage: P0-D / P0-Q

This branch rebuilds the SymC economics and financial-market program around **Χ**, the broader reconstructed market stability architecture. The project no longer begins from the assumption that markets are damped oscillators. Damped second-order behavior is retained as one scientifically testable special case that may emerge from an admitted native market System Model.

## Χ versus χ

- **χ** is a scalar or mode-specific stability coordinate emitted only when a licensed dynamical construction supports it. For a licensed second-order factor, `χ = γ/(2ω₀)`.
- **Χ** is the broader reconstructed stability architecture. It concerns the relationships among scalar/local coordinates, modal/vector structure, conglomerate/system organization, coupling, inheritance, feedback, hierarchy, recovery, emergence, suppression, and failure structure where those objects are supported by native market science.

Χ is not currently asserted to be one scalar equation, an arithmetic combination of lower-level χ values, or a universal physical quantity. Its structure is part of the investigation.

Preferred construction path:

`native market observables -> native statistical/dynamical structure -> admitted modes and couplings -> χ where licensed -> conglomerate/system organization -> reconstructed Χ`

A damped oscillator appears only conditionally:

`system identification -> admitted second-order factor -> poles / ω / γ -> χ -> contribution to Χ`

not:

`assume oscillator -> compute χ -> call the result market stability`.

## Current executable scaffold

The first P0-Q engine does not assume an oscillator. It compares AR(0), AR(1), and AR(2), inspects the admitted second-order poles, and emits χ only when a canonical continuous second-order mapping is licensed. Otherwise χ is refused while the native model result is retained.

This AR-family layer is only the first qualification scaffold. Heteroskedastic, stochastic-volatility, jump, long-memory, regime-switching, multivariate, order-flow, and network alternatives must be allowed to win as the System Model expands.

## Current research targets

### Scalar/local

- licensed mode-specific χ where available;
- native volatility, liquidity, decay, recovery, and other scalar coordinates;
- explicit refusal when scalar reduction is unsupported.

### Modal/vector

- poles and eigenvalues;
- characteristic frequencies and timescales;
- damping/decay rates;
- factor and correlation modes;
- eigenvectors and participation;
- order-flow or liquidity modes where supported.

### Conglomerate/system

- cross-asset and cross-sector coupling;
- market-wide modes;
- correlation and network topology;
- contagion and propagation;
- liquidity synchronization;
- feedback, concentration, and higher-order organization.

### Relational Χ questions

- What local properties survive market embedding?
- What is transformed by coupling?
- What disappears?
- What emerges only at the system level?
- When is scalar χ adequate, and when must the Tool remain modal or network-valued?
- What changes first as recovery capacity or resilience erodes?
- Does reconstructed Χ add diagnostic or predictive value beyond the strongest fair native financial methods?

## Tool goal

The project is being developed toward two earned milestones:

1. **Market Diagnostic Tool**: a refusal-capable System Model + Engine + Independent Market Stability Atlas that reports admitted local/modal/system structure, uncertainty, identifiability, Function Map position, Limit Map position, and open-channel residuals.
2. **Market Predictive Tool**: the frozen validated diagnostic architecture plus prospective testing showing whether its features add value for explicitly defined future tasks against strong native comparators.

Diagnosis and prediction are separate scientific claims. A diagnostic Tool may qualify even if a predictive claim later fails.

## Current files

- `MARKET_PROJECT_GUARDRAILS.md` - project-local scientific constraints.
- `CHI_VS_chi_ARCHITECTURE.md` - working Χ/χ architecture and claim ceiling.
- `QUALIFICATION_LEDGER.md` - P0-Q qualification state.
- `PROJECT_STATUS.md` - current execution status.
- `market_chi/` - executable native-model-first scaffold.
- `tests/` - known-truth and refusal tests.
- `qualification/` - preserved qualification outputs.
- `tools/` - local data inventory and qualification utilities.
- `LOCAL_DATA_HANDOFF.md` - metadata-first intake procedure for the user's existing market corpus.

The legacy `main` branch remains preserved as the historical oscillator-first MarketFW baseline. Findings from it are retained as research lineage and qualification evidence but are not automatically inherited as confirmed market facts.

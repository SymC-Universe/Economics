# Native Microstructure Feature Map for Χ / χ

Status: P0-D working map
Purpose: preserve native market structure before any scalar compression.

This document maps the currently available Databento `trades` and `mbp-10` schemas into candidate SymC market representations. It is a research scaffold, not a frozen feature set.

## 1. Observation layers

### Trades layer

Native observables may include:

- event timestamp;
- instrument identifier;
- aggressor side where specified;
- execution price;
- execution size;
- event sequence;
- inter-trade duration;
- signed and unsigned trade intensity;
- realized price movement and return over explicitly defined horizons.

### MBP-10 layer

Native observables may include:

- event timestamp;
- action and side;
- changed price and size;
- top-ten bid prices;
- top-ten ask prices;
- top-ten bid sizes;
- top-ten ask sizes;
- top-ten bid order counts;
- top-ten ask order counts;
- sequence information;
- contemporaneous trades embedded in the schema.

This provides a time-evolving depth surface rather than only a one-dimensional price series.

## 2. Scalar / local candidates

These are candidates, not automatically χ.

- best bid-ask spread;
- midprice;
- microprice or depth-weighted mid variants;
- total bid depth and total ask depth;
- top-N depth imbalance;
- order-count imbalance;
- signed trade-flow imbalance;
- trade intensity;
- cancellation / modification intensity if recoverable from actions;
- realized volatility;
- realized jump proxies;
- local price impact;
- replenishment rate;
- depletion rate;
- local recovery time after a depth or price perturbation;
- decay rates in admitted response models;
- lowercase χ only when an admitted second-order dynamical factor licenses it.

## 3. Modal / vector candidates

The ten-level bid/ask book is naturally vector-valued. Candidate representations include:

- 20-dimensional depth-size state vectors;
- 20-dimensional order-count state vectors;
- bid/ask price-shape vectors;
- liquidity-surface principal components;
- covariance / correlation eigenmodes;
- state-space poles and eigenvectors;
- participation factors;
- depth-level response modes;
- fast/slow liquidity-recovery modes;
- trade-flow / depth coupled modes;
- frequency- or timescale-specific modes where supported.

A central P0-D question is whether these modes contain information that disappears when the order book is compressed to spread, imbalance, or lowercase χ.

## 4. Conglomerate / system candidates

If the metadata confirms multiple instruments or contract families, candidate system-level structure includes:

- cross-instrument return coupling;
- cross-instrument order-flow coupling;
- cross-instrument liquidity synchronization;
- lead-lag structure;
- common market / sector / contract-family modes;
- correlation-network topology;
- concentration of modal participation;
- propagation of depth depletion or recovery across instruments;
- event synchronization;
- contagion / spillover paths;
- higher-order interaction candidates if pairwise structure proves insufficient.

If the dataset contains only one underlying instrument family, the first conglomerate layer can still be constructed across book depth, timescale, and contract maturities, but any claim of broader market-wide Χ must remain refused until wider data are available.

## 5. Relational Χ targets

The broader Χ investigation should test relationships rather than presuppose a final scalar:

- Does local χ survive embedding into book-depth and cross-instrument structure?
- Are observed second-order factors stable across liquidity states?
- Does the same local coordinate have different realized consequences under different system coupling?
- Which modes dominate before and after perturbations?
- Does liquidity depletion propagate coherently across levels or remain local?
- Which variables control recovery speed after shocks?
- Do scalar coordinates lose information needed to distinguish elastic recovery from plastic state change?
- Can a valid higher-level stability compression be derived without circularly using future outcomes or Atlas labels?

## 6. Initial diagnostic target map

### Function Map candidates

- ordinary spread/depth equilibrium;
- routine liquidity replenishment;
- normal intraday intensity cycles;
- stable bid/ask depth asymmetry;
- ordinary price discovery;
- cross-level coordination;
- contract or instrument coupling under normal conditions.

### Limit Map candidates

- abrupt depth depletion;
- spread expansion;
- large order-flow imbalance;
- jump / gap response;
- transient liquidity vacuum;
- recovery failure;
- persistent post-shock reconfiguration;
- coupling concentration;
- abnormal synchronization;
- state-transition boundaries.

## 7. Prediction targets remain downstream

No predictive endpoint is frozen yet. Candidate endpoints for later comparison include:

- future realized volatility;
- large-move / tail probability;
- liquidity deterioration;
- spread/depth stress;
- transition hazard;
- recovery time after a perturbation.

Directional price prediction remains a separate question and should use native directional channels rather than assuming scalar stability determines sign.

## 8. Admission rule

No feature becomes part of Χ merely because it is available or correlates with an outcome.

Promotion requires:

1. native definition;
2. independent derivation from the evaluation target;
3. reproducibility;
4. uncertainty / identifiability assessment;
5. non-circular comparison against plausible alternatives;
6. contribution to Function Map, Limit Map, or a frozen predictive endpoint;
7. explicit failure and refusal behavior.

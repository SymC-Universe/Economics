# Shared-Reference Development Test Design

Date: 2026-09-18
Status: P0-D design; no empirical result
Holdout: not applicable until development definitions are frozen

## Question

Do conventional broker-default market references show response structure beyond nearby matched alternative settings, after controlling for ordinary price path and native book/flow state?

The user's reason for leaving EMA, MACD, VWAP and Time & Sales at broker defaults is observational: many traders may view the same conventional constructions. The causal proposition that shared visibility changes market response is unproven.

## Firewall

Do not assume that a default setting is special. Broker/platform identity and exact default definitions must be recovered before numerical testing. No default parameter is guessed from convention.

## Required comparison families

For each recoverable default reference:
1. exact broker-default construction;
2. nearby parameter perturbations chosen before outcome inspection;
3. matched alternative smoothers/references with similar effective memory where feasible;
4. placebo/reference levels that preserve ordinary price-path geometry but are not the displayed default;
5. native book/flow covariates.

The same break/recovery/failure event definition must be used for default and alternative references.

## Primary development outputs

Report:
- event count and refusal count;
- recovery/failure trajectory distributions;
- response magnitude and persistence after comparable events;
- incremental value of the default reference after native price/book/flow variables are included;
- sensitivity to small parameter perturbations.

A default reference is not considered special merely because it predicts price better than a grossly mismatched alternative. It must outperform fair nearby/matched controls.

## Interpretation ceiling

Possible outcomes are:
- ADDS candidate: default retains incremental development value against matched controls;
- EQUIVALENT: nearby/matched references perform similarly;
- SUBTRACTS: default is worse or misleading;
- INDETERMINATE: data/definition cannot distinguish the alternatives.

Even an ADDS candidate does not establish that traders collectively cause the response. Shared visibility remains one possible mechanism among endogenous trend geometry, autocorrelation, microstructure, and other explanations.

## Open dependency

Exact broker/platform identity and its historical default settings remain required before the numerical parameter family can be frozen.

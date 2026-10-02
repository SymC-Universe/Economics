# Q040 Synthetic Lineage v0.2 Requalification Record
**Date:** 2026-10-02
**Higher scientific authority:** Q040 Recoverability Plan Packet v0.6
**Semantic-conformance audit:** `qualification/Q040_SYNTHETIC_KNOWN_TRUTH_SEMANTIC_CONFORMANCE_AUDIT_2026-10-02.md`
**Repaired manifest:** `qualification/Q040_SYNTHETIC_KNOWN_TRUTH_MANIFEST_v0.2_2026-10-02.json`
**Generator implementation:** `market_chi/q040_synthetic_generators_v0_2.py`
**Observation/episode bridge:** `market_chi/q040_observation_episode_v02.py`
**Execution:** local Home computer, Python 3.12, zero-cost
**Real Q040 outcomes opened:** NO

## Repaired lineage tests

Local combined test suite:

`7 passed in 26.01s`

## Generator-contract requalification

Disposition:

`Q040_SYNTHETIC_GENERATOR_CONTRACT_V02_PASS`

Controls checked: 22  
Failed controls: 0

Durable local result:
`qualification/results/q040_synthetic_generator_contract_v02/result.json`

SHA-256:
`C2B1BB8C106E2AD268BF377B86B11D012032598279A7411EB7257D4EA95E01AF`

## Observation/episode requalification

The repaired v0.2 observation/episode preflight checked:
- every repaired known-truth control at all four scales;
- the complete NC-R20 measurement grid.

Worlds checked: 180  
Failed worlds: 0

Disposition:

`Q040_SYNTHETIC_OBSERVATION_EPISODE_CONTRACT_PASS`

Durable local result:
`C:\Users\CCGTi\OneDrive\Desktop\SymC_Economics\SymC_TF\Data\_symc_q040_observation_episode_v02\preflight.json`

SHA-256:
`0B107B79B1708AD870F119480FF31032E69CEDD4EA7FCC1578AD0C78CE0EC953`

## Scientific consequence

The v0.1 semantic-lineage defect is repaired and independently requalified. The earlier v0.1 180/180 interface pass remains historical lineage only and is not used as scientific authority.

The repaired v0.2 lineage now authorizes the already-frozen estimator-qualification chain:
K1/K2 -> D1/D2 -> event/return tuple -> horizon -> M0/M2 competing-risk score -> native event-history/Hawkes diagnostic.

The real-data firewall remains sealed.

`Q040_SYNTHETIC_LINEAGE_V0_2=QUALIFIED`

`Q040_ESTIMATOR_QUALIFICATION=AUTHORIZED_SYNTHETIC_ONLY`

`Q040_REAL_OUTCOMES=SEALED`

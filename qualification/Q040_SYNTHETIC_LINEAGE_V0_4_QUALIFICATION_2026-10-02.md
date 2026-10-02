# Q040 Synthetic Lineage v0.4 Qualification Record
**Date:** 2026-10-02
**Authority:** Q040 Recoverability Plan Packet v0.6
**Real Q040 outcomes opened:** NO

The v0.4 synthetic lineage is the first lineage to satisfy all three pre-estimator requirements simultaneously:
1. semantic conformance to the v0.6 plan;
2. common observation/episode contract conformance;
3. recurrent-event support adequacy.

## Local tests

Combined generator + observation tests:

`7 passed in 24.49s`

## Generator contract

`Q040_SYNTHETIC_GENERATOR_CONTRACT_V04_PASS`

Controls checked: 22  
Failed controls: 0

Local result:
`qualification/results/q040_synthetic_generator_contract_v04/result.json`

SHA-256:
`43A1AE81AF1382764354C790700EC2BC0190BABF48ADFC8F5D7475FCC31F58CC`

## Observation/episode contract

Worlds checked: 180  
Failed worlds: 0

`Q040_SYNTHETIC_OBSERVATION_EPISODE_CONTRACT_PASS`

Local result:
`C:\Users\CCGTi\OneDrive\Desktop\SymC_Economics\SymC_TF\Data\_symc_q040_observation_episode_v04\preflight.json`

SHA-256:
`BA938433BE9A20F5218FF1E2DC1575DA68375771F94763A669FA58FD3B510ABD`

## Recurrent-event support

Minimum episode counts over the four scale realizations:
- ordinary/default controls: 62 where generator-specific density is not higher;
- NC-R2: 48;
- NC-R17: 50;
- NC-R17b: 50;
- NC-R19: 53;
- NC-R21: exactly 9, preserved as the deliberate sparse-support refusal.

Every non-NC-R21 control satisfies the frozen >=40-event support floor.

## Failed predecessor preserved

v0.3 remains a failed candidate because NC-R19 produced only 35 events with inadequate low-regime support. It was not patched in place.

## Disposition

`Q040_SYNTHETIC_LINEAGE_V0_4=QUALIFIED_FOR_FULL_ESTIMATOR_QUALIFICATION`

`Q040_ESTIMATOR_SELECTION=AUTHORIZED_SYNTHETIC_ONLY`

`Q040_REAL_OUTCOMES=SEALED`

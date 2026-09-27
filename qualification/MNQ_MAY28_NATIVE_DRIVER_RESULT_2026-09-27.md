# MNQ May 28 Native-Driver Localization Result

Date: 2026-09-27
Stage: P0-D development follow-up
Source artifact SHA-256: `274cf710d86da51504c13cfa04938d9d68ab4667a95d4f89b08f58541088d638`
Source code commit: `3a589c64ccccb14dde84994ea35d86d18985f0cf`
Holdout: `SEALED_NOT_ACCESSED`
Time basis: ordinary UTC wall-clock

## Frozen analysis executed

The received artifact contains all 21 primary 60-minute windows and all 42 sensitivity 30-minute windows as COMPLETE. Structural localization used L10 modal geometry only. Forward-risk overlays were not used to select transitions.

## Primary result

No single native scalar jump explains the modal transitions.

Across adjacent windows, absolute changes in total depth, spread, event rate, trade volume, signed flow, active-trade fraction, and imbalance dispersion do not show a strong, resolution-consistent positive association with top-two subspace dissimilarity. Several of the largest structural transitions occur with only modest native-scalar changes.

The strongest explanatory signal found in this follow-up is instead the **shape of the modal spectrum itself**.

### Spectral separation

Using the stored first-six variance fractions, top-two similarity to the full May 28 mature reference is strongly associated with the PC2-PC3 eigengap:

- 60-minute windows: Spearman rho = 0.9078.
- 30-minute windows: Spearman rho = 0.8255.

After rank-residualizing both variables against monotonic time-of-day, the association remains:

- 60-minute windows: partial rank correlation = 0.8814.
- 30-minute windows: partial rank correlation = 0.8036.

For adjacent-window change, structural dissimilarity `1 - min principal cosine` is inversely associated with the mean PC2-PC3 eigengap of the pair:

- 60-minute transitions: rho = -0.6812.
- 30-minute transitions: rho = -0.7784.

This is mathematically important because individual PCA directions become rank-unstable when neighboring eigenvalues approach degeneracy.

### Semantic directions often persist while rank changes

The apparent top-two failures are not equivalent to disappearance of the native semantic directions.

Examples:

- 07:00-08:00 UTC: top-two similarity to the full-day reference falls to 0.0505, while the strongest symmetric-depth direction is still found at PC6 with alignment 0.7477 and imbalance is retained at PC1 with alignment 0.7926.
- 15:00-16:00 UTC: top-two similarity is 0.0417, yet symmetric depth remains PC1 with alignment 0.9946 and imbalance is PC3 with alignment 0.9718.
- 19:00-20:00 UTC: top-two similarity is 0.3793, symmetric depth remains PC1 with alignment 0.9921, imbalance is PC3 with alignment 0.8399, and PC2 instead aligns with the depth-gradient basis at 0.8027.

These cases are consistent with modal rank redistribution and/or identifiability loss rather than wholesale loss of the underlying native architecture.

## Native state associations

State-level associations are present, but they should not be called causal drivers.

Canonical top-two similarity co-varies positively with L10 imbalance dispersion at both resolutions:

- 60-minute windows: rho = 0.6571.
- 30-minute windows: rho = 0.6012.

At 30 minutes, canonical similarity also co-varies with active-trade fraction, absolute signed-trade volume, and total trade volume. After a simple monotonic time-of-day rank adjustment, depth variability, trade activity, and imbalance dispersion all remain associated with stronger top-two concentration.

The direction of interpretation is therefore not established. A plausible alternative is that higher excitation/variance makes stable semantic modes more observable, while quiet or spectrally flat periods make modal rank less identifiable.

## Correction to the prior May 28 interpretation

The earlier phrase "sequence of native modal reorganizations" is too strong without an identifiability control.

The current P0-D description is:

> **May 28 exhibits repeated top-rank modal redistribution under periods of spectral flattening. The underlying semantic depth/imbalance directions often remain detectable outside the leading two modes. Whether this represents genuine broader Χ reorganization or reduced modal identifiability is unresolved.**

This correction preserves the empirical finding while removing an unsupported mechanism-level interpretation.

## Scalar χ

Nothing in this follow-up licenses scalar χ. The scalar result remains refusal under the existing production rules.

## Next experiment

The next experiment must distinguish **architecture loss** from **rank migration under near-degeneracy**.

For each fixed 60-minute and 30-minute May 28 window, compute the full 20-mode spectrum and sign/rotation-invariant semantic-basis capture for fixed subspaces k = 2, 3, 4, 6, and 10. Also compare adjacent fixed-k subspaces and the full-day reference.

If top-two similarity collapses while wider fixed-k semantic capture and wider subspace similarity remain high, the evidence favors rank redistribution / identifiability loss. If the broader fixed subspaces also lose the semantic architecture, the evidence supports a genuine higher-dimensional reorganization.

No adaptive k or post-result threshold is permitted in this test.

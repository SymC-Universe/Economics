# MNQ May 28 Modal Identifiability / Rank-Migration Result

Date: 2026-09-27
Stage: P0-D development follow-up
Source artifact SHA-256: `f9f9d3ba3a03c4df2ad61bc753b95464c07465a03a1138bbe102ed53e059c25a`
Source code commit: `9181c4ab852c3c790105b72df30714936774a706`
Holdout: `SEALED_NOT_ACCESSED`
Time basis: ordinary UTC wall-clock

## Frozen analysis executed

The received artifact contains 21/21 complete 60-minute windows and 42/42 complete 30-minute windows. Fixed leading subspaces were evaluated at k = 2, 3, 4, 6, and 10. No adaptive k was used.

The experiment asked whether the apparent top-rank reorganizations preserve the native semantic architecture in wider fixed modal subspaces when the spectrum flattens.

## Result

**Disposition: MIXED, RANK-MIGRATION DOMINANT.**

The strongest May 28 anomaly is not well described as wholesale loss of the native market architecture. The semantic backbone is substantially more stable than individual PC rank labels.

### Core semantic pair

Define the core semantic pair descriptively as the weaker of:
- symmetric-depth capture;
- bid/ask-imbalance capture.

This is not a new admission threshold. It is a compact way to report whether both canonical directions remain represented.

At 60-minute resolution:
- median core capture rises from 0.8792 at k=2 to 0.9426 at k=6 and 0.9615 at k=10;
- minimum core capture rises from 0.0041 at k=2 to 0.7062 at k=6 and 0.8676 at k=10;
- symmetric-depth capture at k=6 has median 0.9863 and minimum 0.7062;
- imbalance capture at k=6 has median 0.9426 and minimum 0.8270;
- at k=10, the minimum hourly symmetric-depth and imbalance captures are 0.9205 and 0.8676 respectively.

At 30-minute resolution:
- median core capture rises from 0.8170 at k=2 to 0.9270 at k=6 and 0.9536 at k=10;
- minimum core capture rises from 0.0008 at k=2 to 0.2866 at k=6 and 0.7541 at k=10;
- symmetric-depth capture at k=6 has median 0.9812 but minimum 0.2866;
- imbalance capture at k=6 has median 0.9294 and minimum 0.7928;
- at k=10, minimum symmetric-depth and imbalance captures are 0.7541 and 0.8287.

Thus the PC rank labels are far less stable than the underlying semantic directions.

## Localized partial architecture disturbance

The 30-minute sensitivity pass does not support pure invariance everywhere.

The clearest exception is 09:00-09:30 UTC:
- effective rank 18.13;
- symmetric-depth capture 0.0028 at k=2, 0.2866 at k=6, 0.7541 at k=10;
- imbalance capture 0.0069 at k=2, 0.8656 at k=6, 0.9087 at k=10;
- strongest symmetric-depth alignment appears only at PC10 (0.5502);
- strongest imbalance alignment appears at PC5 (0.9177).

This is stronger than a simple PC2/PC3 swap. The semantic architecture is still substantially recovered by k=10, but symmetric-depth organization is genuinely weakened across the first six modes.

The following 09:30-10:00 UTC interval already partially reconstructs:
- symmetric-depth capture 0.7349 at k=6 and 0.9190 at k=10;
- imbalance capture 0.9464 at k=6 and 0.9680 at k=10.

The local disturbance is therefore retained as evidence rather than averaged away.

## Wider subspace behavior

Full fixed-k subspace similarity is more variable than semantic-basis capture. This means not every higher-order mode is preserved even when the core semantic axes are.

At 60 minutes, median mean principal-cosine similarity to the full-day reference is:
- k=2: 0.9521;
- k=6: 0.8399;
- k=10: 0.9117.

At 30 minutes:
- k=2: 0.9165;
- k=6: 0.8176;
- k=10: 0.8709.

This combination is consistent with a stable semantic backbone embedded inside a reorganizing higher-order modal complement.

## Interpretation

The earlier binary framing, "rank migration versus broader architecture loss," is too coarse.

The May 28 evidence supports a layered interpretation:

1. **Top-rank identity is unstable under spectral flattening.**
2. **The core symmetric-depth / imbalance semantic backbone usually persists in wider fixed subspaces.**
3. **Higher-order modal organization is more variable than the core semantic backbone.**
4. **A localized 09:00-09:30 UTC interval shows genuine partial semantic weakening, especially for symmetric depth.**

Accordingly the current P0-D description is:

> **May 28 is dominated by modal rank migration and identifiability loss around a persistent semantic backbone, with localized partial architecture disturbance rather than wholesale Χ collapse.**

This is a refinement of the prior "sequence of native modal reorganizations" language, not a return to it.

## Scalar χ

Nothing in Q036 licenses scalar χ. The canonical scalar result remains refusal under the existing production rules.

## Next gate

The next test must determine whether this layered pattern is specific to the May 28 outlier or is a recurrent property of mature-session MNQ.

Apply the identical fixed k = 2, 3, 4, 6, 10 semantic-capture and subspace metrics to May 27, May 29, June 1, and June 2 mature development data.

Add a prospectively frozen isotropic semantic-basis control on those unseen cross-day outcomes:
- dimension d = 20;
- fixed random seed;
- fixed random-direction count;
- compare the canonical semantic directions against random orientation capture at each k;
- no p-value promotion and no post-result threshold tuning.

May 28 may be shown against that control only as a post-hoc contextual comparison. Cross-day conclusions must come from the four still-uninspected identifiability outputs.

June 9-11 remains sealed.

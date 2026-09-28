# MNQ Q038 Sealed Holdout Result

Date: 2026-09-27
Claim: `Q038-P1-v1`
Epistemic status: **P1 frozen holdout execution**
Frozen execution commit: `d8a44204514a8111f524ef122d110714d9bafa29`
Uploaded decisive-result SHA-256: `fb13ae917955c1a32200105226d4edd7881aa1bb630abed29b7519c3a5bf207c`

## Frozen primary adjudication

**Outcome: `EMPIRICAL_CLAIM_SURVIVES_FROZEN_TEST`**

Frozen claim:

> In the sealed June 9-11 MNQ mature sessions, the predeclared L10 symmetric-depth / bid-ask-imbalance semantic backbone remains jointly preferentially represented in the leading six-dimensional standardized log-depth PCA subspace relative to isotropic orientation.

All primary coverage gates passed:
- 2026-06-09: 42/42 primary 30-minute windows COMPLETE
- 2026-06-10: 42/42 COMPLETE
- 2026-06-11: 42/42 COMPLETE

Exact frozen null:
- dimension: 20
- fixed k: 6
- isotropic capture distribution: Beta(3,7)
- q95: 0.5496416495066101

Primary statistic:
- point margin: 0.4119953787584348
- 95% block-bootstrap interval: [0.3990332284529543, 0.4272589632610951]
- block length: 4 x 30-minute windows = 2 h
- valid replicates: 10,000/10,000
- seed: 20260927

Mandatory block sensitivities agree:
- 1 h blocks: [0.4026359728423950, 0.42448319697400394]
- 3 h blocks: [0.39656501897965335, 0.4275354327377939]

The lower bound is positive under the primary rule and both mandatory sensitivity block lengths. The precommitted survival criterion is therefore met without rescue, retuning, adaptive k, or alternate thresholds.

## Hierarchical secondary

**Outcome: `EMPIRICAL_SECONDARY_SURVIVES_FROZEN_TEST`**

Frozen estimand:
median(Core6-Core2) inside the 08:30, 09:00, 09:30, 10:00, 10:30 UTC corridor minus the median outside the corridor.

Result:
- point contrast: 0.05927168101371172
- 95% interval: [0.02214193399979314, 0.15740518115889712]
- block length: 4
- requested replicates: 10,000
- valid replicates: 9,987
- seed: 20260928

The 13 invalid replicates are mechanically explained by circular block resamples that contained no corridor slots at all, making the inside/outside contrast undefined. There were zero all-corridor replicates. This is a bootstrap-geometry consequence, not a data failure. The 9,987 valid replicates exceed the frozen >=95% validity floor.

## Descriptive robustness and failure structure

These observations did not determine the P1 decision and are recorded as descriptive interpretation only.

Across all 126 primary 30-minute windows:
- median Core6 = 0.9616370282650448
- minimum Core6 = 0.7465674203451188
- 5th percentile Core6 = 0.8690073233857591
- every primary window individually had Core6 above the exact frozen k=6 isotropic q95
- median Core2 = 0.9055175634012707
- minimum Core2 = 0.002063452100865392
- median Core6-Core2 gain = 0.06254410919579745
- maximum gain = 0.8607706240971587

Per-day 30-minute Core6:
- June 9: median 0.9499484584250462; minimum 0.7465674203451188
- June 10: median 0.9608508410872938; minimum 0.8448689906895053
- June 11: median 0.9771922953216545; minimum 0.8608219165625858

Five primary windows show the strongest canonical symmetric-depth or imbalance direction outside the top two PCs:
- June 9 10:30 UTC
- June 9 11:00 UTC
- June 9 11:30 UTC
- June 10 07:00 UTC
- June 10 07:30 UTC

Those same five windows also have Core2 below the exact d=20, k=2 isotropic q95. This is a compact holdout replication of rank migration: top-rank semantic identity can fail severely while the fixed k=6 semantic backbone remains above the frozen isotropic threshold.

The weakest k=6 holdout interval is June 9 11:30 UTC:
- Core2 = 0.15012683972322244
- Core6 = 0.7465674203451188
- Core10 = 0.9744914736715342
- primary margin = 0.1969257708385087
- imbalance strongest at PC3

The most extreme top-rank failures recover strongly by k=6:
- June 9 11:00: Core2 0.00206345 -> Core6 0.83972677
- June 10 07:00: Core2 0.05191683 -> Core6 0.91268746
- June 10 07:30: Core2 0.00754282 -> Core6 0.86747396

The holdout does not reproduce the deepest development-stage k=6 semantic collapses. Its minimum primary Core6 is 0.746567, so localized partial semantic disturbance remains a development-observed failure mode rather than a P1-replicated recurrent feature.

The fixed 60-minute sensitivity windows are also descriptively consistent:
- 63/63 COMPLETE
- median Core6 = 0.9676789405207393
- minimum Core6 = 0.8587532623753376
- all 63 have positive k=6 margins against the same exact q95

## Source integrity

All three source files were processed by the frozen runner and all feature caches passed gzip EOF/CRC and CSV contract validation.

Raw SHA-256:
- June 9: `738853dc7fe01c48c313df2b960a0e6f7c979573ded25a9055310613e8256107`
- June 10: `a24db4cd6361442be1d2110f47abdf68203dc7be6f099f033aa17045ea570e29`
- June 11: `9d57eccc1358d6431406883060386b302b332db9149b280dbd3be0663763295d`

Feature SHA-256:
- June 9: `5b42913af5f9aec286765accabd229fae8a61495e8ee88b36370d58164d68295`
- June 10: `aa79164e6a380159cbb4b8a3071e77e296582458e9f714083f8c395687132a62`
- June 11: `cc3be7ff2147eaa0c3e4fbcc073109c31bebaf085757436c7ca1c740391ed94e`

## Promotion consequence

Q038 licenses only the bounded MNQ mature-session claim tested here. It does **not** establish:
- market-wide Χ universality;
- cross-instrument transfer;
- a scalar χ;
- a hidden χ transition;
- a universal rank-migration law;
- a trading rule.

Canonical scalar χ remains separately refused under the existing production screen.

The promoted structural interpretation is:

> In the frozen June 9-11 MNQ mature-session holdout, the predeclared symmetric-depth / bid-ask-imbalance semantic backbone remained jointly represented in the fixed leading six-dimensional L10 depth subspace above the exact isotropic-orientation control. Top-two rank identity still failed locally, including severe rank-migration intervals, but those failures did not erase the broader fixed-k semantic architecture.


# Variance-Diagnostic Stress Result

Date: 2026-09-18
Stage: P0-Q synthetic qualification
Production chi admission changed: NO

## Question

Can residual volatility clustering be used as a simple refusal gate for the stochastic-volatility false chi admissions seen in the AR0/AR1/AR2 scaffold?

## Baseline adversarial result

At BIC margin 6 with 200 simulations per family and n=1200:
- pure stochastic-volatility family: 3/200 chi admissions (1.5%);
- median squared-residual ACF energy among those three admissions: 0.34897;
- homoskedastic known complex AR2: 200/200 admissions, median energy 0.01589;
- homoskedastic known real AR2: 200/200 admissions, median energy 0.01595.

This initially suggested that volatility clustering might distinguish the false admissions.

## Required stress test

A legitimate second-order conditional-mean process can itself have heteroskedastic innovations. Therefore the same diagnostic was applied to known complex and real AR2 dynamics driven by GARCH and stochastic-volatility innovations.

Results, 200 simulations per family:
- complex AR2 + GARCH noise: 200/200 chi admissions, median energy 0.27780;
- complex AR2 + SV noise: 200/200 chi admissions, median energy 0.28354;
- real AR2 + GARCH noise: 200/200 chi admissions, median energy 0.27388;
- real AR2 + SV noise: 200/200 chi admissions, median energy 0.28733.

The heteroskedastic known-truth AR2 families therefore overlap strongly with the variance-structure range of the false pure-SV admissions.

## Conclusion

Residual variance structure is **not a valid standalone chi refusal gate**. Using a threshold on squared-residual autocorrelation or block-variance variation would reject legitimate second-order conditional-mean dynamics whenever their innovations are heteroskedastic.

The diagnostic remains useful as a descriptive flag: it identifies that a second process is present in the conditional variance, but it does not determine whether the conditional mean has legitimate second-order structure.

Q009 therefore remains open. The next discriminating qualification should test whether the AR2 conditional-mean advantage survives out of sample / across time blocks. The target distinction is:

- pure volatility-state process: any AR2 mean advantage should be unstable or fail out of sample;
- true AR2 mean dynamics with heteroskedastic innovations: second-order mean predictability should persist despite variance clustering.

No production threshold or chi admission rule is changed from this result.

## Provenance

GitHub Actions workflow: `variance-admission-audit`
Stress workflow commit: `941ff496901dd99c13f688078497efe38f2b374f`
Artifact digest: `sha256:19756d2f3b21f0b2247ee010b78b3f9395f19d5a19611addc433932ef2cfb6cb`

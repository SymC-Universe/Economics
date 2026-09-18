# Walk-Forward Conditional-Mean Admission Audit

Date: 2026-09-18
Stage: P0-Q synthetic qualification
Production chi admission changed: NO

## Question

Can out-of-sample persistence of the AR2 conditional mean distinguish false in-sample chi admissions caused by non-mean structure from legitimate second-order mean dynamics, including when the innovations are heteroskedastic?

## Method

For each synthetic series, the existing production engine was run unchanged. Separately, AR0/AR1/AR2 models were compared using expanding walk-forward one-step prediction:
- n = 1200;
- initial training prefix = 400;
- test blocks = 100;
- loss = one-step squared prediction error;
- AR2 gain = relative MSE improvement over the better of AR0/AR1.

No walk-forward threshold was used to alter production admission.

## Key results

Pure/no-second-order families:
- white: median AR2 OOS gain -0.0030;
- AR1: -0.00125;
- GARCH: -0.00395;
- stochastic volatility: -0.00379 overall;
- jumps: -0.00278 overall.

In this independently seeded campaign, the production engine admitted chi in 1/200 stochastic-volatility simulations and 1/200 jump simulations. Their AR2 OOS gains were:
- admitted stochastic-volatility case: -0.02138;
- admitted jump case: -0.00129.

Known second-order families:
- complex AR2 homoskedastic: median gain about 0.818;
- complex AR2 + GARCH noise: about 0.817;
- complex AR2 + SV noise: about 0.816;
- real AR2 homoskedastic: about 0.363;
- real AR2 + GARCH noise: about 0.364;
- real AR2 + SV noise: about 0.362.

All six known second-order families were admitted 200/200 times and had median AR2 fold-win fraction 1.0.

A regime-switching AR1 family showed positive AR2 OOS gain (~0.169 median) but received zero chi admissions from the existing production gate. This is important: out-of-sample AR2 gain is not sufficient by itself and should remain secondary to native model/pole admission.

## Interpretation

Walk-forward conditional-mean persistence is a substantially better discriminator than residual variance clustering in this first qualification campaign. It distinguishes the observed false admissions from the tested legitimate AR2 mean dynamics even when those dynamics are driven by heteroskedastic innovations.

However, a production threshold is **not yet justified**. The current known-truth AR2 cases are relatively clear. Before any OOS persistence rule is added to chi admission, qualification must cover:
- weaker second-order effects;
- near-repeated/near-degenerate poles;
- multiple sample lengths;
- additional stochastic-volatility/jump parameters;
- near-boundary cases where AR2 is physically legitimate but hard to identify;
- sensitivity of the fold construction itself.

The next qualification target is therefore a threshold-free sensitivity map, not immediate gate insertion.

## Provenance

GitHub Actions workflow: `mean-cv-admission-audit`
Workflow commit: `c3566eb0dfa0042c1194737002fc3fe9c6e39f07`
Artifact digest: `sha256:3c207d4d7980aecad87f62b3a24aa956b80cb7e0d6b5341e189e2eae10fb15bc`

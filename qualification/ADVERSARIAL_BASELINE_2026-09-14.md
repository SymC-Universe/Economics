# P0-Q Adversarial Admission Baseline - 2026-09-14

Purpose: qualify the first native-model-first χ admission scaffold before exposure to the user's market corpus.

Configuration:

- 200 independent simulations per family per BIC margin;
- 1,200 retained observations per simulation;
- seeds 2000-2199;
- candidate scaffold: AR(0), AR(1), AR(2);
- χ emitted only after AR(2) admission and pole-licensing checks;
- exploratory margins scanned: 0, 2, 4, 6, 8, 10, 12.

These are P0-Q method results, not empirical evidence about financial markets.

## Result at the current exploratory default margin = 6

| Synthetic family | χ admission rate |
|---|---:|
| white noise | 0.0% |
| AR(1), phi=0.8 | 0.0% |
| GARCH(1,1) | 0.0% |
| stochastic volatility | 1.5% |
| jump-contaminated iid | 0.0% |
| regime-switching AR(1) | 0.0% |
| known complex AR(2) second-order factor | 100.0% |
| known positive-real AR(2) second-order factor | 100.0% |

The full sensitivity surface is stored in `admission_sensitivity_2026-09-14.csv`.

## Interpretation

The new scaffold eliminates the gross failure observed in the legacy production path, where ordinary AR(1) structure could frequently receive a χ estimate. The current scaffold also rejects the tested white-noise, jump, and regime-switching AR(1) families in this qualification sweep while retaining both known second-order families.

The remaining stochastic-volatility false-admission tail is scientifically important. It means AR0/AR1/AR2 competition is not sufficient as a final market admission system. Heteroskedastic and volatility-state alternatives must enter the native model competition or a separate residual/variance-structure gate before broad real-data χ interpretation.

No BIC margin is frozen by this exercise. Margin tuning remains P0-Q and its search history must remain visible.

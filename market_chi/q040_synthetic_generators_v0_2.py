from __future__ import annotations

from dataclasses import asdict, dataclass
import numpy as np


@dataclass(frozen=True)
class GeneratorAudit:
    control_id: str
    pass_invariant: bool
    details: dict[str, float | int | bool | str]

    def to_dict(self):
        return asdict(self)


def _rng(seed: int) -> np.random.Generator:
    return np.random.default_rng(int(seed))


def _base_shock(n: int, rng: np.random.Generator) -> np.ndarray:
    shock = np.zeros(n, dtype=float)
    idx = np.arange(128, n, 256)
    shock[idx] = rng.choice([-1.0, 1.0], size=len(idx))
    return shock


def _self_exciting_shocks(
    n: int,
    rng: np.random.Generator,
    *,
    base_prob: np.ndarray | float,
    decay: float,
    excitation_gain: float,
) -> tuple[np.ndarray, np.ndarray]:
    base = np.asarray(base_prob, dtype=float)
    if base.ndim == 0:
        base = np.full(n, float(base))
    if len(base) != n:
        raise ValueError("base_prob length mismatch")
    shock = np.zeros(n, dtype=float)
    intensity_proxy = np.zeros(n, dtype=float)
    excitation = 0.0
    for i in range(n):
        intensity_proxy[i] = excitation
        p = float(np.clip(base[i] + excitation_gain * excitation, 0.0, 0.35))
        if rng.random() < p:
            shock[i] = rng.choice([-1.0, 1.0])
            excitation += 1.0
        excitation *= decay
    return shock, intensity_proxy


def _event_rate_by_regime(shock: np.ndarray, regime: np.ndarray) -> tuple[float, float]:
    high = regime > np.median(regime)
    low = ~high
    return float(np.mean(shock[high] != 0)), float(np.mean(shock[low] != 0))


def generate_control(control_id: str, *, seed: int, n: int = 4096) -> dict[str, np.ndarray | float | int]:
    r = _rng(seed)
    t = np.arange(n, dtype=float)
    shock = _base_shock(n, r)

    rate = np.full(n, 0.08, dtype=float)
    baseline = np.zeros(n, dtype=float)
    noise_scale = np.full(n, 0.05, dtype=float)
    exog = np.zeros(n, dtype=float)
    slow = np.zeros(n, dtype=float)
    resistance = np.full(n, 1.0, dtype=float)
    required_episodes = 20

    if control_id == "NC-R1":
        pass

    elif control_id == "NC-R2":
        # Deterministic immigrant-plus-aftershock clusters with unchanged recovery law.
        shock = np.zeros(n, dtype=float)
        clustering = np.zeros(n, dtype=float)
        state = 0.0
        immigrants = np.arange(128, n, 256)
        signs = r.choice([-1.0, 1.0], size=len(immigrants))
        for base_i, sign in zip(immigrants, signs):
            for lag in (0, 8, 24):
                j = int(base_i + lag)
                if j < n:
                    shock[j] = float(sign)
        for i in range(n):
            clustering[i] = state
            state = 0.85 * state + abs(float(shock[i]))
        burden = np.cumsum(np.abs(shock))
        return {
            "t": t,
            "shock": shock,
            "burden": burden,
            "rate": rate,
            "baseline": baseline,
            "noise_scale": noise_scale,
            "exog": exog,
            "slow": slow,
            "resistance": resistance,
            "required_episodes": required_episodes,
            "shock_intensity_proxy": clustering,
        }

    elif control_id == "NC-R3":
        burden = np.cumsum(np.abs(shock))
        rate = np.maximum(0.02, 0.09 - 0.0012 * burden)

    elif control_id == "NC-R4":
        burden = np.cumsum(np.abs(shock))
        rate = np.minimum(0.18, 0.06 + 0.0015 * burden)

    elif control_id == "NC-R5":
        baseline = 0.00008 * t

    elif control_id == "NC-R6":
        # Opposite history direction by perturbation sign.
        shock = np.zeros(n, dtype=float)
        idx = np.arange(128, n, 256)
        shock[idx] = np.where(np.arange(len(idx)) % 2 == 0, 1.0, -1.0)
        burden = np.cumsum(np.abs(shock))
        direction = np.ones(n, dtype=float)
        last_sign = 1.0
        for i in range(n):
            if shock[i] != 0.0:
                last_sign = float(np.sign(shock[i]))
            direction[i] = last_sign
        pos_rate = np.maximum(0.025, 0.105 - 0.0014 * burden)
        neg_rate = np.minimum(0.18, 0.050 + 0.0014 * burden)
        rate = np.where(direction > 0.0, pos_rate, neg_rate)
        return {
            "t": t,
            "shock": shock,
            "burden": burden,
            "direction": direction,
            "rate": rate,
            "baseline": baseline,
            "noise_scale": noise_scale,
            "exog": exog,
            "slow": slow,
            "resistance": resistance,
            "required_episodes": required_episodes,
        }

    elif control_id == "NC-R7":
        exog = np.sin(2*np.pi*t/700.0)
        shock = shock + (exog > 0.92).astype(float)
        slow = 0.7 * exog

    elif control_id == "NC-R8":
        v1 = np.column_stack([np.sin(t/40.0), np.cos(t/40.0)])
        v2 = np.column_stack([np.cos(t/40.0), np.sin(t/40.0)])
        scalar = v1.sum(axis=1)
        return {"t": t, "v1": v1, "v2": v2, "scalar": scalar}

    elif control_id == "NC-R9":
        burden = np.cumsum(np.abs(shock))
        rate = np.maximum(0.025, 0.09 - 0.0010 * burden)
        slow = 0.012 * burden + r.normal(scale=0.02, size=n)

    elif control_id == "NC-R10":
        # Genuine within-scale history dependence, no slower propagation.
        burden = np.cumsum(np.abs(shock))
        rate = np.maximum(0.025, 0.09 - 0.0010 * burden)
        slow = r.normal(scale=0.02, size=n)

    elif control_id == "NC-R11":
        burden = np.cumsum(np.abs(shock))
        rate = np.maximum(0.025, 0.08 - 0.0008 * burden)
        resistance = 1.0 + 0.01 * burden

    elif control_id == "NC-R12":
        A = np.array([[-0.08, 0.55], [0.0, -0.12]])
        x = np.zeros((n, 2))
        x[0] = [1.0, 0.4]
        dt = 0.25
        for i in range(1, n):
            x[i] = x[i-1] + dt * (A @ x[i-1])
        return {"t": t, "x": x, "eig_real": np.real(np.linalg.eigvals(A))}

    elif control_id == "NC-R13":
        idx = np.arange(128, n, 64)
        shock = np.zeros(n, dtype=float)
        shock[idx] = r.choice([-1.0, 1.0], size=len(idx))

    elif control_id == "NC-R14":
        fast = r.normal(size=n)
        slow_mech = np.convolve(fast, np.ones(5)/5.0, mode="same")
        return {"t": t, "fast": fast, "slow_mechanical": slow_mech}

    elif control_id == "NC-R15":
        noise_scale = 0.03 + 0.06 * (t / max(1.0, t[-1]))

    elif control_id == "NC-R16":
        cov_scale = 0.5 + 1.5*(t/t[-1])
        x = r.normal(size=(n, 2)) * cov_scale[:, None]
        return {"t": t, "x": x, "cov_scale": cov_scale}

    elif control_id == "NC-R17":
        regime = np.sin(2*np.pi*t/1000.0)
        base_prob = 0.0015 + 0.0060 * (regime + 1.0) / 2.0
        shock, clustering = _self_exciting_shocks(
            n, r, base_prob=base_prob, decay=0.88, excitation_gain=0.055
        )
        burden = np.cumsum(np.abs(shock))
        shock_intensity_proxy = 0.9 * regime + r.normal(scale=0.08, size=n)
        rate = np.clip(0.07 + 0.02 * regime, 0.03, 0.14)
        baseline = 0.3 * regime
        return {
            "t": t,
            "shock": shock,
            "burden": burden,
            "latent_regime": regime,
            "shock_intensity_proxy": shock_intensity_proxy,
            "clustering_truth": clustering,
            "rate": rate,
            "baseline": baseline,
        }

    elif control_id == "NC-R17b":
        z = np.sin(2*np.pi*t/850.0) + r.normal(scale=0.1, size=n)
        scaled = 1.0 / (1.0 + np.exp(-z))
        base_prob = 0.0015 + 0.0080 * scaled
        shock, clustering = _self_exciting_shocks(
            n, r, base_prob=base_prob, decay=0.86, excitation_gain=0.045
        )
        burden = np.cumsum(np.abs(shock))
        apparent_history = 0.85 * z + r.normal(scale=0.08, size=n)
        rate = np.clip(0.08 + 0.02 * z, 0.03, 0.14)
        slow = 0.25 * z + r.normal(scale=0.02, size=n)
        return {
            "t": t,
            "shock": shock,
            "burden": burden,
            "omitted_covariate": z,
            "apparent_history": apparent_history,
            "clustering_truth": clustering,
            "rate": rate,
            "slow": slow,
        }

    elif control_id == "NC-R18":
        unresolved = np.zeros(n)
        last = 0.0
        for i in range(n):
            last *= 0.97
            last += abs(shock[i])
            unresolved[i] = last
        extra = (unresolved > np.quantile(unresolved, 0.8)) & (r.random(n) < 0.06)
        shock = shock + extra.astype(float)

    elif control_id == "NC-R19":
        regime = np.sin(2*np.pi*t/900.0)
        shock = np.zeros(n, dtype=float)
        opportunities = np.arange(64, n, 64)
        active = opportunities[regime[opportunities] > 0.0]
        shock[active] = r.choice([-1.0, 1.0], size=len(active))
        clustering = np.zeros(n, dtype=float)
        state = 0.0
        for i in range(n):
            clustering[i] = state
            state = 0.87 * state + abs(float(shock[i]))
        burden = np.cumsum(np.abs(shock))
        fast_history_proxy = 0.8 * regime + r.normal(scale=0.08, size=n)
        shock_intensity_proxy = 0.85 * regime + r.normal(scale=0.08, size=n)
        slow = 0.5 * regime + r.normal(scale=0.03, size=n)
        rate = np.clip(0.075 + 0.015 * regime, 0.04, 0.12)
        return {
            "t": t,
            "shock": shock,
            "burden": burden,
            "latent_regime": regime,
            "fast_history_proxy": fast_history_proxy,
            "shock_intensity_proxy": shock_intensity_proxy,
            "clustering_truth": clustering,
            "slow": slow,
            "rate": rate,
        }

    elif control_id == "NC-R20":
        latent = np.zeros(n)
        for i in range(1, n):
            latent[i] = 0.7*latent[i-1] + r.normal(scale=0.2)
        update = r.random(n) < (0.18 + 0.12*(np.sin(2*np.pi*t/600.0) > 0))
        observed = np.full(n, np.nan)
        last = np.nan
        for i in range(n):
            if update[i]:
                last = latent[i]
            if np.isfinite(last):
                observed[i] = last
        return {
            "t": t,
            "latent": latent,
            "observed": observed,
            "update": update.astype(float),
            "rate": rate,
        }

    elif control_id == "NC-R21":
        shock = np.zeros(n, dtype=float)
        idx = np.linspace(256, n - 256, 9, dtype=int)
        shock[idx] = np.where(np.arange(len(idx)) % 2 == 0, 1.0, -1.0)
        required_episodes = 9

    else:
        raise ValueError(control_id)

    burden = np.cumsum(np.abs(shock))
    return {
        "t": t,
        "shock": shock,
        "burden": burden,
        "rate": rate,
        "baseline": baseline,
        "noise_scale": noise_scale,
        "exog": exog,
        "slow": slow,
        "resistance": resistance,
        "required_episodes": required_episodes,
    }


def audit_generator(control_id: str, data: dict[str, np.ndarray | float | int]) -> GeneratorAudit:
    d: dict[str, float | int | bool | str] = {}
    passed = True

    if control_id == "NC-R1":
        rate = np.asarray(data["rate"])
        passed = bool(np.allclose(rate, rate[0]))
        d["rate_span"] = float(np.ptp(rate))

    elif control_id == "NC-R2":
        rate = np.asarray(data["rate"])
        shock = np.asarray(data["shock"])
        idx = np.flatnonzero(shock != 0)
        isi = np.diff(idx) if len(idx) > 1 else np.asarray([])
        short_fraction = float(np.mean(isi <= 32)) if len(isi) else 0.0
        passed = bool(np.allclose(rate, rate[0]) and len(idx) >= 12 and short_fraction >= 0.15)
        d["shock_count"] = int(len(idx))
        d["short_isi_fraction_le32"] = short_fraction
        d["rate_span"] = float(np.ptp(rate))

    elif control_id == "NC-R3":
        rate = np.asarray(data["rate"])
        passed = bool(rate[-1] < rate[0])
        d["rate_delta"] = float(rate[-1] - rate[0])

    elif control_id == "NC-R4":
        rate = np.asarray(data["rate"])
        passed = bool(rate[-1] > rate[0])
        d["rate_delta"] = float(rate[-1] - rate[0])

    elif control_id == "NC-R5":
        rate = np.asarray(data["rate"])
        baseline = np.asarray(data["baseline"])
        passed = bool(np.allclose(rate, rate[0]) and np.ptp(baseline) > 0)
        d["baseline_span"] = float(np.ptp(baseline))

    elif control_id == "NC-R6":
        rate = np.asarray(data["rate"])
        burden = np.asarray(data["burden"])
        direction = np.asarray(data["direction"])
        pos = direction > 0
        neg = direction < 0
        cp = float(np.corrcoef(burden[pos], rate[pos])[0, 1])
        cn = float(np.corrcoef(burden[neg], rate[neg])[0, 1])
        passed = bool(cp < -0.8 and cn > 0.8)
        d["positive_direction_history_corr"] = cp
        d["negative_direction_history_corr"] = cn

    elif control_id == "NC-R7":
        exog = np.asarray(data["exog"])
        slow = np.asarray(data["slow"])
        shock = np.asarray(data["shock"])
        corr = float(np.corrcoef(exog, slow)[0, 1])
        event_exog = float(np.mean(exog[shock != 0]))
        passed = bool(corr > 0.99 and event_exog > float(np.mean(exog)))
        d["exog_slow_corr"] = corr
        d["mean_exog_at_events"] = event_exog

    elif control_id == "NC-R8":
        v1 = np.asarray(data["v1"])
        v2 = np.asarray(data["v2"])
        scalar = np.asarray(data["scalar"])
        passed = bool(np.max(np.abs(v1-v2)) > 0 and np.std(scalar) > 0)
        d["vector_difference"] = float(np.mean(np.abs(v1-v2)))

    elif control_id == "NC-R9":
        burden = np.asarray(data["burden"])
        slow = np.asarray(data["slow"])
        rate = np.asarray(data["rate"])
        corr = float(np.corrcoef(burden, slow)[0, 1])
        passed = bool(corr > 0.8 and rate[-1] < rate[0])
        d["burden_slow_corr"] = corr
        d["rate_delta"] = float(rate[-1] - rate[0])

    elif control_id == "NC-R10":
        burden = np.asarray(data["burden"])
        slow = np.asarray(data["slow"])
        rate = np.asarray(data["rate"])
        corr = float(np.corrcoef(burden, slow)[0, 1])
        passed = bool(abs(corr) < 0.2 and rate[-1] < rate[0])
        d["burden_slow_corr"] = corr
        d["rate_delta"] = float(rate[-1] - rate[0])

    elif control_id == "NC-R11":
        rate = np.asarray(data["rate"])
        resistance = np.asarray(data["resistance"])
        passed = bool(rate[-1] < rate[0] and resistance[-1] > resistance[0])
        d["rate_delta"] = float(rate[-1] - rate[0])
        d["resistance_delta"] = float(resistance[-1] - resistance[0])

    elif control_id == "NC-R12":
        x = np.asarray(data["x"])
        eig = np.asarray(data["eig_real"])
        norm = np.linalg.norm(x, axis=1)
        passed = bool(np.all(eig < 0) and np.max(norm) > norm[0] and norm[-1] < norm[0])
        d["peak_ratio"] = float(np.max(norm)/norm[0])

    elif control_id == "NC-R13":
        shock = np.asarray(data["shock"])
        passed = bool(np.count_nonzero(shock) > 40)
        d["shock_count"] = int(np.count_nonzero(shock))

    elif control_id == "NC-R14":
        fast = np.asarray(data["fast"])
        slow = np.asarray(data["slow_mechanical"])
        corr = float(np.corrcoef(fast, slow)[0, 1])
        passed = bool(corr > 0.2)
        d["mechanical_corr"] = corr

    elif control_id == "NC-R15":
        rate = np.asarray(data["rate"])
        noise = np.asarray(data["noise_scale"])
        passed = bool(np.allclose(rate, rate[0]) and noise[-1] > noise[0])
        d["noise_delta"] = float(noise[-1] - noise[0])

    elif control_id == "NC-R16":
        cs = np.asarray(data["cov_scale"])
        passed = bool(cs[-1] > cs[0])
        d["cov_scale_ratio"] = float(cs[-1]/cs[0])

    elif control_id == "NC-R17":
        z = np.asarray(data["latent_regime"])
        proxy = np.asarray(data["shock_intensity_proxy"])
        baseline = np.asarray(data["baseline"])
        rate = np.asarray(data["rate"])
        shock = np.asarray(data["shock"])
        ch = float(np.corrcoef(z, proxy)[0, 1])
        cb = float(np.corrcoef(z, baseline)[0, 1])
        cr = float(np.corrcoef(z, rate)[0, 1])
        high_rate, low_rate = _event_rate_by_regime(shock, z)
        passed = bool(abs(ch) > 0.8 and abs(cb) > 0.95 and abs(cr) > 0.95 and high_rate > low_rate)
        d["regime_to_proxy_corr"] = ch
        d["regime_to_baseline_corr"] = cb
        d["regime_to_rate_corr"] = cr
        d["event_rate_high_regime"] = high_rate
        d["event_rate_low_regime"] = low_rate

    elif control_id == "NC-R17b":
        z = np.asarray(data["omitted_covariate"])
        h = np.asarray(data["apparent_history"])
        slow = np.asarray(data["slow"])
        shock = np.asarray(data["shock"])
        ch = float(np.corrcoef(z, h)[0, 1])
        cs = float(np.corrcoef(z, slow)[0, 1])
        high_rate, low_rate = _event_rate_by_regime(shock, z)
        passed = bool(abs(ch) > 0.8 and abs(cs) > 0.8 and high_rate > low_rate)
        d["omitted_to_history_corr"] = ch
        d["omitted_to_recovery_corr"] = cs
        d["event_rate_high_omitted"] = high_rate
        d["event_rate_low_omitted"] = low_rate

    elif control_id == "NC-R18":
        shock = np.asarray(data["shock"])
        passed = bool(np.count_nonzero(shock) > 15)
        d["shock_count"] = int(np.count_nonzero(shock))

    elif control_id == "NC-R19":
        z = np.asarray(data["latent_regime"])
        h = np.asarray(data["fast_history_proxy"])
        proxy = np.asarray(data["shock_intensity_proxy"])
        slow = np.asarray(data["slow"])
        shock = np.asarray(data["shock"])
        ch = float(np.corrcoef(z, h)[0, 1])
        cp = float(np.corrcoef(z, proxy)[0, 1])
        cs = float(np.corrcoef(z, slow)[0, 1])
        high_rate, low_rate = _event_rate_by_regime(shock, z)
        passed = bool(abs(ch) > 0.8 and abs(cp) > 0.8 and abs(cs) > 0.8 and high_rate > low_rate)
        d["regime_to_fast_history_corr"] = ch
        d["regime_to_proxy_corr"] = cp
        d["regime_to_slow_corr"] = cs
        d["event_rate_high_regime"] = high_rate
        d["event_rate_low_regime"] = low_rate

    elif control_id == "NC-R20":
        latent = np.asarray(data["latent"])
        observed = np.asarray(data["observed"])
        update = np.asarray(data["update"])
        passed = bool(np.count_nonzero(update) < len(update) and np.count_nonzero(np.isfinite(observed)) > 0)
        d["update_fraction"] = float(np.mean(update))

    elif control_id == "NC-R21":
        shock = np.asarray(data["shock"])
        n_events = int(np.count_nonzero(shock))
        required = int(data["required_episodes"])
        passed = bool(n_events == 9 and required < 10)
        d["shock_count"] = n_events
        d["episodes_per_sparse_stratum"] = required

    else:
        passed = False
        d["error"] = "unknown_control"

    return GeneratorAudit(control_id, passed, d)

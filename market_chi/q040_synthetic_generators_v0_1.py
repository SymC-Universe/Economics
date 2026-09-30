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


def generate_control(control_id: str, *, seed: int, n: int = 4096) -> dict[str, np.ndarray | float | int]:
    """Generate normalized known-truth fixtures.

    These fixtures qualify generator semantics only. They are not the final
    Q040 estimator qualification and contain no market data.
    """
    r = _rng(seed)
    t = np.arange(n, dtype=float)
    shock = np.zeros(n, dtype=float)
    idx = np.arange(128, n, 256)
    shock[idx] = r.choice([-1.0, 1.0], size=len(idx))
    burden = np.cumsum(np.abs(shock))

    rate = np.full(n, 0.08, dtype=float)
    baseline = np.zeros(n, dtype=float)
    noise_scale = np.full(n, 0.05, dtype=float)
    exog = np.zeros(n, dtype=float)
    slow = np.zeros(n, dtype=float)
    resistance = np.full(n, 1.0, dtype=float)
    required_episodes = 20

    if control_id == "NC-R2":
        rate = np.maximum(0.02, 0.09 - 0.0012 * burden)
    elif control_id == "NC-R4":
        rate = np.minimum(0.18, 0.06 + 0.0015 * burden)
    elif control_id == "NC-R5":
        baseline = 0.00008 * t
    elif control_id == "NC-R6":
        # Explicit bidirectional known truth: alternate perturbation direction so
        # both sign-conditioned recovery laws are represented deterministically.
        shock = np.zeros(n, dtype=float)
        idx = np.arange(128, n, 256)
        shock[idx] = np.where(np.arange(len(idx)) % 2 == 0, 1.0, -1.0)
        direction = np.ones(n, dtype=float)
        last_sign = 1.0
        for i in range(n):
            if shock[i] != 0.0:
                last_sign = float(np.sign(shock[i]))
            direction[i] = last_sign
        rate = np.where(direction > 0.0, 0.10, 0.055)
        burden = np.cumsum(np.abs(shock))
    elif control_id == "NC-R7":
        exog = np.sin(2*np.pi*t/700.0)
        shock = shock + (exog > 0.92).astype(float)
        slow = 0.7 * exog
    elif control_id == "NC-R9":
        slow = 0.012 * burden + r.normal(scale=0.02, size=n)
    elif control_id == "NC-R10":
        slow = r.normal(scale=0.02, size=n)
    elif control_id == "NC-R11":
        rate = np.maximum(0.025, 0.08 - 0.0008 * burden)
        resistance = 1.0 + 0.01 * burden
    elif control_id == "NC-R13":
        idx = np.arange(128, n, 64)
        shock = np.zeros(n)
        shock[idx] = r.choice([-1.0, 1.0], size=len(idx))
        burden = np.cumsum(np.abs(shock))
    elif control_id == "NC-R15":
        noise_scale = 0.03 + 0.06 * (t / max(1.0, t[-1]))
    elif control_id == "NC-R17":
        regime = np.sin(2*np.pi*t/1000.0)
        rate = 0.07 + 0.02 * regime
        shock = shock + (regime > 0.8).astype(float)
        slow = 0.3 * regime
    elif control_id == "NC-R17b":
        z = np.sin(2*np.pi*t/850.0) + r.normal(scale=0.1, size=n)
        rate = 0.08 + 0.02 * z
        burden = burden + np.maximum(z, 0)
        slow = 0.25 * z
    elif control_id == "NC-R18":
        # High interruption pressure when a deterministic recovery proxy is unresolved.
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
        burden = burden + np.maximum(regime, 0)
        slow = 0.5 * regime
    elif control_id == "NC-R20":
        # Underlying latent state is memoryless AR(1); observed state is sparse carry-forward.
        latent = np.zeros(n)
        for i in range(1,n):
            latent[i] = 0.7*latent[i-1] + r.normal(scale=0.2)
        update = r.random(n) < (0.18 + 0.12*(np.sin(2*np.pi*t/600.0)>0))
        observed = np.full(n, np.nan)
        last = np.nan
        for i in range(n):
            if update[i]:
                last = latent[i]
            if np.isfinite(last):
                observed[i] = last
        return {"t":t,"latent":latent,"observed":observed,"update":update.astype(float),"rate":rate}
    elif control_id == "NC-R21":
        required_episodes = 9

    if control_id == "NC-R12":
        # Stable non-normal 2D linear system with transient amplification.
        A = np.array([[-0.08, 0.55],[0.0,-0.12]])
        x = np.zeros((n,2))
        x[0] = [1.0,0.4]
        dt = 0.25
        for i in range(1,n):
            x[i] = x[i-1] + dt * (A @ x[i-1])
        return {"t":t,"x":x,"eig_real":np.real(np.linalg.eigvals(A))}
    if control_id == "NC-R8":
        # Same scalar sum, different vector state.
        v1 = np.column_stack([np.sin(t/40.0), np.cos(t/40.0)])
        v2 = np.column_stack([np.cos(t/40.0), np.sin(t/40.0)])
        scalar = v1.sum(axis=1)
        return {"t":t,"v1":v1,"v2":v2,"scalar":scalar}
    if control_id == "NC-R14":
        fast = r.normal(size=n)
        slow_mech = np.convolve(fast, np.ones(5)/5.0, mode="same")
        return {"t":t,"fast":fast,"slow_mechanical":slow_mech}
    if control_id == "NC-R16":
        cov_scale = 0.5 + 1.5*(t/t[-1])
        x = r.normal(size=(n,2)) * cov_scale[:,None]
        return {"t":t,"x":x,"cov_scale":cov_scale}

    return {
        "t":t,"shock":shock,"burden":burden,"rate":rate,"baseline":baseline,
        "noise_scale":noise_scale,"exog":exog,"slow":slow,"resistance":resistance,
        "required_episodes":required_episodes,
    }


def audit_generator(control_id: str, data: dict[str, np.ndarray | float | int]) -> GeneratorAudit:
    d: dict[str, float | int | bool | str] = {}
    passed = True

    if control_id in {"NC-R1","NC-R3"}:
        rate=np.asarray(data["rate"]); passed=bool(np.allclose(rate,rate[0])); d["rate_span"]=float(np.ptp(rate))
    elif control_id=="NC-R2":
        rate=np.asarray(data["rate"]); passed=bool(rate[-1] < rate[0]); d["rate_delta"]=float(rate[-1]-rate[0])
    elif control_id=="NC-R4":
        rate=np.asarray(data["rate"]); passed=bool(rate[-1] > rate[0]); d["rate_delta"]=float(rate[-1]-rate[0])
    elif control_id=="NC-R5":
        rate=np.asarray(data["rate"]); baseline=np.asarray(data["baseline"]); passed=bool(np.allclose(rate,rate[0]) and np.ptp(baseline)>0); d["baseline_span"]=float(np.ptp(baseline))
    elif control_id=="NC-R6":
        rate=np.asarray(data["rate"]); passed=bool(np.ptp(rate)>0); d["rate_span"]=float(np.ptp(rate))
    elif control_id=="NC-R7":
        exog=np.asarray(data["exog"]); slow=np.asarray(data["slow"]); passed=bool(np.corrcoef(exog,slow)[0,1]>0.99); d["exog_slow_corr"]=float(np.corrcoef(exog,slow)[0,1])
    elif control_id=="NC-R8":
        v1=np.asarray(data["v1"]); v2=np.asarray(data["v2"]); scalar=np.asarray(data["scalar"]); passed=bool(np.max(np.abs(v1-v2))>0 and np.std(scalar)>0); d["vector_difference"]=float(np.mean(np.abs(v1-v2)))
    elif control_id=="NC-R9":
        burden=np.asarray(data["burden"]); slow=np.asarray(data["slow"]); corr=float(np.corrcoef(burden,slow)[0,1]); passed=bool(corr>0.8); d["burden_slow_corr"]=corr
    elif control_id=="NC-R10":
        burden=np.asarray(data["burden"]); slow=np.asarray(data["slow"]); corr=float(np.corrcoef(burden,slow)[0,1]); passed=bool(abs(corr)<0.2); d["burden_slow_corr"]=corr
    elif control_id=="NC-R11":
        rate=np.asarray(data["rate"]); resistance=np.asarray(data["resistance"]); passed=bool(rate[-1]<rate[0] and resistance[-1]>resistance[0]); d["rate_delta"]=float(rate[-1]-rate[0]); d["resistance_delta"]=float(resistance[-1]-resistance[0])
    elif control_id=="NC-R12":
        x=np.asarray(data["x"]); eig=np.asarray(data["eig_real"]); norm=np.linalg.norm(x,axis=1); passed=bool(np.all(eig<0) and np.max(norm)>norm[0] and norm[-1]<norm[0]); d["peak_ratio"]=float(np.max(norm)/norm[0])
    elif control_id=="NC-R13":
        shock=np.asarray(data["shock"]); passed=bool(np.count_nonzero(shock)>40); d["shock_count"]=int(np.count_nonzero(shock))
    elif control_id=="NC-R14":
        fast=np.asarray(data["fast"]); slow=np.asarray(data["slow_mechanical"]); corr=float(np.corrcoef(fast,slow)[0,1]); passed=bool(corr>0.2); d["mechanical_corr"]=corr
    elif control_id=="NC-R15":
        rate=np.asarray(data["rate"]); noise=np.asarray(data["noise_scale"]); passed=bool(np.allclose(rate,rate[0]) and noise[-1]>noise[0]); d["noise_delta"]=float(noise[-1]-noise[0])
    elif control_id=="NC-R16":
        cs=np.asarray(data["cov_scale"]); passed=bool(cs[-1]>cs[0]); d["cov_scale_ratio"]=float(cs[-1]/cs[0])
    elif control_id in {"NC-R17","NC-R17b","NC-R19"}:
        burden=np.asarray(data["burden"]); slow=np.asarray(data["slow"]); corr=float(np.corrcoef(burden,slow)[0,1]); passed=bool(abs(corr)>0.15); d["shared_cause_corr"]=corr
    elif control_id=="NC-R18":
        shock=np.asarray(data["shock"]); passed=bool(np.count_nonzero(shock)>15); d["shock_count"]=int(np.count_nonzero(shock))
    elif control_id=="NC-R20":
        latent=np.asarray(data["latent"]); observed=np.asarray(data["observed"]); update=np.asarray(data["update"]); passed=bool(np.count_nonzero(update)<len(update) and np.count_nonzero(np.isfinite(observed))>0); d["update_fraction"]=float(np.mean(update))
    elif control_id=="NC-R21":
        n=int(data["required_episodes"]); passed=bool(n<10); d["episodes_per_sparse_stratum"]=n
    else:
        passed=False; d["error"]="unknown_control"

    return GeneratorAudit(control_id, passed, d)

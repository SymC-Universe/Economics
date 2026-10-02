from __future__ import annotations

from dataclasses import dataclass
import math
import numpy as np

M0_WIDTH=42
M2_WIDTH=44

@dataclass(frozen=True)
class ConfirmatoryFeatures:
    m0:np.ndarray
    m2:np.ndarray
    oracle_withheld:np.ndarray|None
    entry_index:int


def _native_map(world:dict)->dict[str,int]:
    names=list(world["metadata"]["native_covariate_names"])
    return {str(name):i for i,name in enumerate(names)}


def _native_value(world:dict,name:str,entry:int)->float:
    mapping=_native_map(world)
    if name not in mapping:
        raise KeyError(f"missing native covariate {name}")
    value=float(world["arrays"]["native_covariates"][entry,mapping[name]])
    if not math.isfinite(value):
        raise ValueError(f"nonfinite native covariate {name}")
    return value
def build_confirmatory_features(
    world:dict,
    *,
    entry:int,
    baseline:np.ndarray,
    baseline_velocity:np.ndarray,
    candidate_event_amplitude:float,
    previous_interval_log1p:float,
    trailing_native_difference_rms:float,
    prior_incomplete_indicator:float,
    cumulative_event_amplitude:float,
    cumulative_time_outside_return:float,
)->ConfirmatoryFeatures:
    a=world["arrays"]
    z=np.asarray(a["Z_observed"],dtype=float)
    b=np.asarray(baseline,dtype=float)
    v=np.asarray(baseline_velocity,dtype=float)
    if z.shape!=b.shape or z.shape!=v.shape:
        raise ValueError("state/baseline/velocity shape mismatch")
    if not 0<=int(entry)<len(z):
        raise ValueError("entry out of range")
    e=int(entry)
    if np.any(~np.isfinite(z[e])) or np.any(~np.isfinite(b[e])) or np.any(~np.isfinite(v[e])):
        raise ValueError("entry state objects nonfinite")
    residual=z[e]-b[e]
    norm=float(np.linalg.norm(residual))
    if not math.isfinite(norm) or norm<=1e-12:
        raise ValueError("perturbation direction undefined")
    direction=residual/norm
    amp=float(candidate_event_amplitude)
    prev=float(previous_interval_log1p)
    rms=float(trailing_native_difference_rms)
    prior_incomplete=float(prior_incomplete_indicator)
    lobs=float(cumulative_event_amplitude)
    uobs=float(cumulative_time_outside_return)
    for name,value in (
        ("candidate_event_amplitude",amp),
        ("previous_interval_log1p",prev),
        ("trailing_native_difference_rms",rms),
        ("prior_incomplete_indicator",prior_incomplete),
        ("cumulative_event_amplitude",lobs),
        ("cumulative_time_outside_return",uobs),
    ):
        if not math.isfinite(value):
            raise ValueError(f"nonfinite {name}")

    phase=np.asarray(a["session_phase"][e],dtype=float)
    if phase.shape!=(4,) or np.any(~np.isfinite(phase)):
        raise ValueError("invalid session phase")

    velocity_norm=float(np.linalg.norm(v[e]))
    velocity_projection=float(np.dot(v[e],direction))
    directional_sign=float(np.sign(residual[3]))
    update=_native_value(world,"update_indicator",e)
    staleness=_native_value(world,"staleness_samples",e)
    exog=_native_value(world,"exogenous_forcing",e)
    regime=_native_value(world,"observed_regime_proxy",e)
    apparent=_native_value(world,"apparent_history",e)
    noise=_native_value(world,"noise_scale_proxy",e)
    event_intensity=_native_value(world,"past_event_intensity",e)

    m0=np.concatenate([
        residual.astype(float),
        b[e].astype(float),
        direction.astype(float),
        np.asarray([
            amp,
            velocity_norm,
            velocity_projection,
            prev,
        ],dtype=float),
        phase,
        np.asarray([
            update,
            math.log1p(max(0.0,staleness)),
            exog,
            regime,
            apparent,
            noise,
            event_intensity,
            rms,
            directional_sign,
            prior_incomplete,
        ],dtype=float),
    ])
    if m0.shape!=(M0_WIDTH,):
        raise AssertionError(f"M0 width {m0.shape} != {M0_WIDTH}")
    if np.any(~np.isfinite(m0)):
        raise ValueError("nonfinite M0")

    m2=np.concatenate([m0,np.asarray([lobs,uobs],dtype=float)])
    if m2.shape!=(M2_WIDTH,):
        raise AssertionError(f"M2 width {m2.shape} != {M2_WIDTH}")

    withheld=np.asarray(a["withheld_native_covariates"],dtype=float)
    oracle=None
    if withheld.ndim==2 and withheld.shape[1]>0:
        row=withheld[e].astype(float)
        if np.any(~np.isfinite(row)):
            raise ValueError("nonfinite withheld oracle covariate")
        oracle=np.concatenate([m0,row])

    return ConfirmatoryFeatures(
        m0=m0,
        m2=m2,
        oracle_withheld=oracle,
        entry_index=e,
    )

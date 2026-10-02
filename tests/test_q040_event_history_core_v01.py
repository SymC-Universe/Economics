import numpy as np

from market_chi.q040_event_history_core_v01 import (
    absolute_relative_event_rate_error,
    build_event_history_design,
    causal_excitation,
    excitation_relative_error,
    fit_event_history_logit,
    normalized_background_rmse,
    predict_event_probability,
    probability_decile_calibration,
)


def _phase(n):
    t=np.arange(n,dtype=float)
    a=2*np.pi*t/n
    return np.column_stack([np.sin(a),np.cos(a),np.sin(2*a),np.cos(2*a)])


def test_causal_excitation_uses_prior_event_only():
    y=np.array([0,1,0,0,1],dtype=float)
    c=causal_excitation(y,0.9)
    assert np.allclose(c,[0,0,1,0.9,0.81])


def test_h0_h1_h2_design_dimensions():
    n=100
    phase=_phase(n)
    activity=np.linspace(-1,1,n)
    events=np.zeros(n); events[20]=1; events[60]=1
    assert build_event_history_design(phase,activity,events,config="H0").shape==(n,6)
    assert build_event_history_design(
        phase,activity,events,config="H1",rho=0.96
    ).shape==(n,7)
    q=np.sin(np.arange(n)/11)
    assert build_event_history_design(
        phase,activity,events,config="H2",rho=0.96,queue_proxy=q
    ).shape==(n,8)


def test_logit_fit_is_finite_on_known_h1_model():
    rng=np.random.default_rng(7)
    n=4000
    phase=_phase(n)
    activity=rng.normal(size=n)
    events=np.zeros(n,dtype=float)
    rho=0.96
    c=0.0
    for t in range(1,n):
        c=rho*c+events[t-1]
        eta=-3.3+0.15*phase[t,0]-0.1*phase[t,1]+0.12*activity[t]+0.35*c
        p=1/(1+np.exp(-eta))
        events[t]=rng.random()<p
    X=build_event_history_design(phase,activity,events,config="H1",rho=rho)
    fit=fit_event_history_logit(X,events,config="H1",rho=rho)
    assert fit.status=="COMPLETE", fit.reason
    pred=predict_event_probability(X,fit)
    assert np.all(np.isfinite(pred))
    assert np.all((pred>0)&(pred<1))
    assert absolute_relative_event_rate_error(pred,events)<0.20
    err=excitation_relative_error(fit,0.35)
    assert np.isfinite(err)


def test_background_rmse_and_decile_calibration():
    truth=np.linspace(0.05,0.25,100)
    pred=truth.copy()
    assert normalized_background_rmse(pred,truth)==0.0
    observed=(np.arange(100)%5==0).astype(float)
    rows=probability_decile_calibration(pred,observed)
    assert len(rows)==10
    assert sum(x["n"] for x in rows)==100
    assert all(np.isfinite(x["absolute_calibration_error"]) for x in rows)


def test_rank_deficient_event_history_design_refuses():
    n=200
    X=np.ones((n,3),dtype=float)
    y=np.zeros(n,dtype=float)
    y[::20]=1
    fit=fit_event_history_logit(X,y,config="H0")
    assert fit.status=="REFUSED"
    assert fit.reason=="rank_deficient"

import numpy as np

from market_chi.q040_confirmatory_core_v01 import (
    OUTCOME_CENSOR,
    OUTCOME_INTERRUPT,
    OUTCOME_RETURN,
    estimate_censoring_km,
    fit_competing_risk_hazard,
    grouped_confirmatory_folds,
    holm_adjust,
    ipcw_integrated_brier,
    paired_bootstrap_summary,
    predict_hazards,
    sustained_return_cif,
    time_bin_index,
)


def test_grouped_folds_are_24_6_and_disjoint():
    folds=grouped_confirmatory_folds()
    assert len(folds)==5
    seen=[]
    for train,test in folds:
        assert len(train)==24
        assert len(test)==6
        assert set(train).isdisjoint(set(test))
        seen.extend(test.tolist())
    assert sorted(seen)==list(range(30))
def test_eight_equal_width_time_bins():
    assert time_bin_index(1,80)==0
    assert time_bin_index(10,80)==0
    assert time_bin_index(11,80)==1
    assert time_bin_index(80,80)==7


def test_rank_deficient_design_is_refused():
    x=np.zeros((40,2),dtype=float)
    durations=np.ones(40,dtype=int)
    outcomes=np.tile(
        np.array([OUTCOME_RETURN,OUTCOME_INTERRUPT,OUTCOME_CENSOR,OUTCOME_RETURN]),
        10,
    )
    fit=fit_competing_risk_hazard(x,durations,outcomes,horizon=8)
    assert fit.status=="REFUSED"
    assert fit.reason=="rank_deficient_after_zero_variance_removal"


def test_competing_risk_fit_and_cif_are_finite_monotone():
    rng=np.random.default_rng(20261002)
    n=400
    x=rng.normal(size=(n,3))
    durations=np.tile(np.arange(1,17,dtype=int),25)
    outcomes=rng.choice(
        np.array([OUTCOME_CENSOR,OUTCOME_RETURN,OUTCOME_INTERRUPT]),
        size=n,
        p=[0.20,0.40,0.40],
    )
    fit=fit_competing_risk_hazard(x,durations,outcomes,horizon=16)
    assert fit.status=="COMPLETE", fit.reason
    hazards=predict_hazards(fit,x[:12],16)
    assert hazards.shape==(12,16,2)
    assert np.all(np.isfinite(hazards))
    assert np.all(hazards>=0)
    assert np.all(hazards.sum(axis=2)<=1.0+1e-12)
    cif=sustained_return_cif(hazards)
    assert np.all(np.isfinite(cif))
    assert np.all(np.diff(cif,axis=1)>=-1e-12)
    assert np.all((cif>=0)&(cif<=1.0+1e-12))


def test_censoring_km_no_censor_and_weight_refusal():
    d=np.array([2,3,4,4],dtype=int)
    o=np.array([OUTCOME_RETURN,OUTCOME_INTERRUPT,OUTCOME_RETURN,OUTCOME_INTERRUPT])
    km=estimate_censoring_km(d,o,horizon=4)
    assert km.status=="COMPLETE"
    assert np.allclose(km.g_after,1.0)
    assert np.allclose(km.g_left,1.0)
    d2=np.ones(20,dtype=int)
    o2=np.full(20,OUTCOME_CENSOR,dtype=int)
    bad=estimate_censoring_km(d2,o2,horizon=4)
    assert bad.status=="REFUSED"
    assert bad.reason=="CENSORING_WEIGHT_NOT_QUALIFIED"


def test_ipcw_brier_is_zero_for_perfect_cif():
    d=np.array([2,3],dtype=int)
    o=np.array([OUTCOME_RETURN,OUTCOME_INTERRUPT],dtype=int)
    km=estimate_censoring_km(d,o,horizon=4)
    pred=np.array([
        [0.0,1.0,1.0,1.0],
        [0.0,0.0,0.0,0.0],
    ])
    ibs,by_time=ipcw_integrated_brier(pred,d,o,km)
    assert ibs==0.0
    assert np.allclose(by_time,0.0)


def test_bootstrap_is_deterministic_and_positive():
    x=np.full(30,0.1,dtype=float)
    a=paired_bootstrap_summary(x,15)
    b=paired_bootstrap_summary(x,15)
    assert a==b
    assert a.point>0
    assert a.ci_low>0
    assert a.positive_count==30
    assert a.n_boot==10_000
    assert 0<a.p_two_sided<0.001


def test_holm_adjustment_four_scale_family():
    out=holm_adjust({15:0.01,30:0.02,60:0.03,300:0.04})
    assert np.isclose(out[15],0.04)
    assert np.isclose(out[30],0.06)
    assert np.isclose(out[60],0.06)
    assert np.isclose(out[300],0.06)

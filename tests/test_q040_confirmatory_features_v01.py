import numpy as np

from market_chi.q040_baseline_selection_v01 import estimate_k1
from market_chi.q040_confirmatory_features_v01 import (
    M0_WIDTH,
    M2_WIDTH,
    build_confirmatory_features,
)
from market_chi.q040_observation_episode_v04 import build_observation_episode_world


def _baseline(world):
    a=world["arrays"]
    return estimate_k1(
        np.asarray(a["Z_observed"],dtype=float),
        np.asarray(a["update_mask"],dtype=bool),
        window=640,
        start=1,
    )


def _build(world,entry=1000):
    b,v=_baseline(world)
    return build_confirmatory_features(
        world,
        entry=entry,
        baseline=b,
        baseline_velocity=v,
        candidate_event_amplitude=4.2,
        previous_interval_log1p=np.log1p(64),
        trailing_native_difference_rms=0.35,
        prior_incomplete_indicator=0.0,
        cumulative_event_amplitude=12.0,
        cumulative_time_outside_return=18.0,
    )


def test_m0_m2_width_and_finiteness_on_v04_world():
    world=build_observation_episode_world("NC-R1",seed=1234,scale_seconds=15)
    f=_build(world)
    assert f.m0.shape==(M0_WIDTH,)
    assert f.m2.shape==(M2_WIDTH,)
    assert M0_WIDTH==42
    assert M2_WIDTH==44
    assert np.all(np.isfinite(f.m0))
    assert np.all(np.isfinite(f.m2))
    assert f.oracle_withheld is None
    assert np.allclose(f.m2[-2:],[12.0,18.0])


def test_coordinate4_direction_sign_is_literal_sign():
    world=build_observation_episode_world("NC-R1",seed=2234,scale_seconds=30)
    b,_=_baseline(world)
    entry=1000
    residual=world["arrays"]["Z_observed"][entry]-b[entry]
    f=_build(world,entry)
    assert f.m0[40]==np.sign(residual[3])


def test_nc17b_withheld_covariate_is_oracle_only():
    world=build_observation_episode_world("NC-R17b",seed=3234,scale_seconds=60)
    f=_build(world)
    withheld=world["arrays"]["withheld_native_covariates"][1000]
    assert withheld.shape==(1,)
    assert f.oracle_withheld is not None
    assert f.oracle_withheld.shape==(M0_WIDTH+1,)
    assert np.allclose(f.oracle_withheld[-1],withheld[0])
    assert not np.any(np.isclose(f.m0,withheld[0],rtol=0,atol=0))


def test_previous_interval_and_rms_are_caller_frozen_inputs():
    world=build_observation_episode_world("NC-R1",seed=4234,scale_seconds=300)
    b,v=_baseline(world)
    f=build_confirmatory_features(
        world,
        entry=1000,
        baseline=b,
        baseline_velocity=v,
        candidate_event_amplitude=3.0,
        previous_interval_log1p=2.75,
        trailing_native_difference_rms=0.625,
        prior_incomplete_indicator=1.0,
        cumulative_event_amplitude=9.0,
        cumulative_time_outside_return=11.0,
    )
    assert f.m0[27]==2.75
    assert f.m0[39]==0.625
    assert f.m0[41]==1.0

import numpy as np

from market_chi.q040_observation_episode_v02 import (
    SCALES,
    build_observation_episode_world,
    determinism_check,
    nc20_cells,
    validate_world,
)


def test_common_schema_across_all_controls_and_scales():
    controls = [f"NC-R{i}" for i in range(1, 22) if i != 17] + ["NC-R17", "NC-R17b"]
    controls = list(dict.fromkeys(controls))
    for ci, control in enumerate(controls):
        for scale in SCALES:
            if control == "NC-R20":
                cell = nc20_cells()[0]
            else:
                cell = None
            world = build_observation_episode_world(
                control,
                seed=20261001 + 100 * ci + scale,
                scale_seconds=scale,
                nc20_cell=cell,
            )
            audit = validate_world(world)
            assert audit["pass"], (control, scale, audit["faults"])


def test_nc20_all_measurement_cells_pass_contract():
    for scale in SCALES:
        for j, cell in enumerate(nc20_cells()):
            world = build_observation_episode_world(
                "NC-R20",
                seed=20262000 + 100 * scale + j,
                scale_seconds=scale,
                nc20_cell=cell,
            )
            audit = validate_world(world)
            assert audit["pass"], (scale, cell.key(), audit["faults"])
            observed = world["arrays"]["Z_observed"]
            mask = world["arrays"]["update_mask"]
            if np.any(~mask[1:]):
                idx = np.flatnonzero(~mask[1:])[0] + 1
                if np.all(np.isfinite(observed[idx - 1])):
                    assert np.array_equal(observed[idx], observed[idx - 1])


def test_nc17b_withheld_covariate_does_not_leak():
    world = build_observation_episode_world(
        "NC-R17b", seed=20263001, scale_seconds=60
    )
    assert world["arrays"]["withheld_native_covariates"].shape[1] == 1
    assert "omitted_native_covariate" not in world["metadata"]["native_covariate_names"]
    assert world["metadata"]["intentionally_withheld_native_covariate"]


def test_event_truth_is_injected_shock_truth():
    world = build_observation_episode_world(
        "NC-R2", seed=20263002, scale_seconds=60
    )
    assert np.array_equal(
        world["arrays"]["event_entry_true"],
        world["arrays"]["shock_input"] != 0,
    )


def test_determinism():
    assert determinism_check("NC-R5", seed=20263003, scale_seconds=30)
    assert determinism_check(
        "NC-R20",
        seed=20263004,
        scale_seconds=300,
        nc20_cell=nc20_cells()[7],
    )

from tools.mnq_may28_reorganization import sign_label, window_specs


def test_three_hour_windows_cover_frozen_mature_interval():
    w = window_specs(3)
    assert len(w) == 7
    assert w[0]["start"] == "2026-05-28T00:00:00.000000000Z"
    assert w[-1]["end"] == "2026-05-28T21:00:00.000000000Z"
    for a, b in zip(w, w[1:]):
        assert a["end"] == b["start"]


def test_seven_hour_sensitivity_windows_cover_same_clock_time():
    w = window_specs(7)
    assert len(w) == 3
    assert w[0]["start"] == "2026-05-28T00:00:00.000000000Z"
    assert w[-1]["end"] == "2026-05-28T21:00:00.000000000Z"


def test_sign_label_requires_consistency_across_all_horizons():
    assert sign_label({"1": 0.1, "5": 0.2}) == "positive"
    assert sign_label({"1": -0.1, "5": -0.2}) == "negative"
    assert sign_label({"1": -0.1, "5": 0.2}) == "mixed"

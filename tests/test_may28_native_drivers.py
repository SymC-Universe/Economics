from tools.mnq_may28_native_drivers import delta, specs


def test_hourly_windows_cover_mature_interval():
    w = specs(60)
    assert len(w) == 21
    assert w[0]["start"] == "2026-05-28T00:00:00.000000000Z"
    assert w[-1]["end"] == "2026-05-28T21:00:00.000000000Z"
    for a, b in zip(w, w[1:]):
        assert a["end"] == b["start"]


def test_half_hour_sensitivity_windows_cover_same_interval():
    w = specs(30)
    assert len(w) == 42
    assert w[0]["start"] == "2026-05-28T00:00:00.000000000Z"
    assert w[-1]["end"] == "2026-05-28T21:00:00.000000000Z"


def test_native_delta_is_directional_b_minus_a():
    assert delta({"x": 2.0, "y": 5.0}, {"x": 3.5, "y": 1.0}) == {"x": 1.5, "y": -4.0}

from tools.q040_baseline_selection_v02 import WINDOWS, selection_seed

def test_b2_windows_frozen():
    assert WINDOWS == (480,640)

def test_b2_seed_namespace_disjoint():
    a=selection_seed("NC-R5",15,0,0)
    b=selection_seed("NC-R5",15,1,0)
    c=selection_seed("NC-R5",30,0,0)
    assert len({a,b,c}) == 3

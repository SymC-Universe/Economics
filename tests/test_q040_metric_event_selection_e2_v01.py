from tools.q040_metric_event_selection_e2_v01 import candidate_table, seed_for

def test_e2_candidate_grid_size():
    table=candidate_table()
    assert len(table)==162
    assert len({x["index"] for x in table})==162

def test_e2_seed_namespace_unique():
    a=seed_for("NC-R1",15,0,0)
    b=seed_for("NC-R1",15,1,0)
    c=seed_for("NC-R1",30,0,0)
    assert len({a,b,c})==3

import csv,gzip,math
from pathlib import Path
from market_chi.microstructure_v2 import aggregate_mbp10_stream,EXPECTED_MBP10_COLUMNS

def row(ts,bid_sz0,ask_sz0):
    bid0=20_000_000_000_000; ask0=20_000_250_000_000
    r={c:'0' for c in EXPECTED_MBP10_COLUMNS}; r.update({'ts_recv':str(ts+1000),'ts_event':str(ts),'rtype':'10','publisher_id':'1','instrument_id':'11','action':'M','side':'B','depth':'0','price':str(bid0),'size':'1','flags':'0','ts_in_delta':'100','sequence':str(ts),'symbol':'MNQM6'})
    for i in range(10):
        r[f'bid_px_{i:02d}']=str(bid0-i*250_000_000); r[f'ask_px_{i:02d}']=str(ask0+i*250_000_000)
        r[f'bid_sz_{i:02d}']=str(bid_sz0 if i==0 else 10+i); r[f'ask_sz_{i:02d}']=str(ask_sz0 if i==0 else 10+i); r[f'bid_ct_{i:02d}']='2'; r[f'ask_ct_{i:02d}']='2'
    return r

def test_signed_microprice_and_streaming(tmp_path:Path):
    src=tmp_path/'x.csv'; rows=[row(1_000_000_100,10,6),row(2_000_000_100,8,8),row(3_000_000_100,6,10)]
    with src.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(EXPECTED_MBP10_COLUMNS)); w.writeheader(); w.writerows(rows)
    out=tmp_path/'o.csv.gz'; summary=tmp_path/'s.json'; s=aggregate_mbp10_stream(src,out,summary,1000)
    assert s['bins_written']==3
    with gzip.open(out,'rt',encoding='utf-8',newline='') as f: data=list(csv.DictReader(f))
    vals=[float(r['microprice_offset_last']) for r in data]
    assert vals[0]>0 and abs(vals[1])<1e-15 and vals[2]<0
    for r in data:
        expected=0.5*float(r['spread_last'])*float(r['l1_imbalance_last'])
        assert math.isclose(float(r['microprice_offset_last']),expected,rel_tol=0,abs_tol=1e-12)

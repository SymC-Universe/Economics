#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from market_chi.microstructure_v2 import aggregate_mbp10_stream

def main():
    p=argparse.ArgumentParser(); p.add_argument('--input',required=True); p.add_argument('--out-dir',required=True); p.add_argument('--interval-ms',type=int,default=1000); a=p.parse_args()
    src=Path(a.input).expanduser().resolve(); out=Path(a.out_dir).expanduser().resolve(); out.mkdir(parents=True,exist_ok=True)
    stem=src.name
    for suffix in ('.zst','.gz','.csv'):
        if stem.endswith(suffix): stem=stem[:-len(suffix)]
    features=out/f'{stem}.{a.interval_ms}ms.features.v2.csv.gz'; summary=out/f'{stem}.{a.interval_ms}ms.summary.v2.json'
    r=aggregate_mbp10_stream(src,features,summary,a.interval_ms)
    print('WEEKDAY PASS COMPLETE'); print('Rows read:',r['rows_read']); print('Bins written:',r['bins_written']); print('Summary:',summary); print('Features:',features)
if __name__=='__main__': main()

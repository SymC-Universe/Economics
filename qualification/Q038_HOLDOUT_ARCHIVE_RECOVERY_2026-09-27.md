# Q038 Holdout Archive Recovery Record

Date: 2026-09-27
Claim: Q038-P1-v1
Scientific freeze status: unchanged

## Recovery finding

Filename-only archive inspection identified the sealed Q038 holdout inside:

`C:\Users\CCGTi\OneDrive\Desktop\SymC_Economics\SymC_TF\Data\GLBX-20260707-MJC5YBJBLU.zip`

The archive member-name listing shows the exact three frozen decisive files:

- `glbx-mdp3-20260609.mbp-10.csv.zst`
- `glbx-mdp3-20260610.mbp-10.csv.zst`
- `glbx-mdp3-20260611.mbp-10.csv.zst`

No market records were opened during recovery. Only archive member names were listed.

## Mechanical recovery rule

The recovery runner may extract only those three exact archive members to the canonical Q038 raw-data directory.

It must refuse if:
- the archive is absent;
- any of the three exact member names is absent;
- extraction fails;
- the extracted filenames differ from the frozen names.

No additional archive member may be selected based on content or outcome.

After extraction, the existing frozen Q038-P1-v1 analysis executes unchanged.

## Scientific freeze remains unchanged

Unchanged:
- dates: June 9-11, 2026;
- mature session: 00:00-21:00 UTC;
- primary windows: 30 minutes;
- fixed k=6;
- symmetric-depth / bid-ask-imbalance semantic pair;
- exact isotropic null Beta(3,7);
- q95 = 0.5496416495066101;
- 10,000-replicate day-stratified circular moving-block bootstrap;
- primary block length 4 windows;
- sensitivity block lengths 2 and 6;
- hierarchical secondary corridor;
- falsifier and precommitted failure consequence.

This record resolves only the raw-file transport location.

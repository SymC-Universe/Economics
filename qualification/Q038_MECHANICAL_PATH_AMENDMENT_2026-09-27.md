# Q038 Mechanical Path-Resolution Amendment

Date: 2026-09-27
Claim: Q038-P1-v1
Scientific freeze status: unchanged
Holdout status at failure: SEALED_NOT_ACCESSED

## Trigger

The first Q038 package stopped before holdout access because the BAT preflight required this exact Windows path:

`Data\MBR10_Data\glbx-mdp3-20260609.mbp-10.csv.zst`

The user's holdout file was not present at that exact location.

No June 9-11 raw file was opened, decompressed, hashed, parsed, or analyzed before the stop. The failure occurred at file-existence checking.

## Classification

`MECHANICAL / TRANSPORT PATH ASSUMPTION FAILURE`

This is not a scientific failure and does not alter:
- Q038-P1-v1 claim text;
- 30-minute primary windows;
- 00:00-21:00 UTC mature-session definition;
- fixed k=6;
- symmetric-depth / imbalance semantic pair;
- exact Beta(3,7) isotropic null;
- q95 = 0.5496416495066101;
- bootstrap design;
- hierarchical secondary corridor;
- uncertainty rule;
- falsifier;
- failure consequence.

## Mechanical correction

The frozen runner now:

1. checks the original canonical path first;
2. if absent, enumerates filenames only under the user's `Data` directory;
3. accepts only paths whose filename contains the exact holdout date and `mbp-10` and ends in `.zst`;
4. excludes the Q038 output directory;
5. requires exactly one candidate for each date;
6. refuses when zero or multiple candidates are present.

Filename/path enumeration does not inspect holdout scientific content.

## Verification

Mechanical code commit:
`ab0d8b18baedd5c798a107d3e69bff5b4a594b82`

Path-recovery tests commit:
`ce855c86b62ed1ac8a6b42024d48e2f93c12dc51`

CI run:
`36353261026`

CI conclusion:
`success`

Known-truth tests verify:
- fallback discovery finds one uniquely date-matched MBP10 file;
- multiple candidates are refused rather than selected.

## Execution identity

The corrected Q038 package uses code commit:
`ce855c86b62ed1ac8a6b42024d48e2f93c12dc51`

The scientific freeze remains Q038-P1-v1. This amendment changes only path discovery and does not reopen the scientific plan.

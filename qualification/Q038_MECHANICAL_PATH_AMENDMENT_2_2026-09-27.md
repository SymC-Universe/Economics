# Q038 Mechanical Path-Resolution Amendment 2

Date: 2026-09-27
Claim: Q038-P1-v1
Scientific freeze status: unchanged
Holdout status after second failed run: SEALED_NOT_ACCESSED

## Second trigger

The v1.1 Q038 runner searched the complete configured `Data` tree for a filename containing the exact holdout date, `mbp-10`, and `.zst`.

For 2026-06-09 it found zero candidates and stopped.

The stop occurred before source hashing, decompression, parsing, feature extraction, PCA, semantic capture, or any other scientific inspection of June 9-11.

## Classification

`MECHANICAL / RAW-FILE LOCATION UNRESOLVED`

This remains outside the scientific Q038 adjudication.

## Mechanical extension

The locator now searches filenames only under existing roots derived mechanically from the configured Data path and user profile:

- Data;
- Data parent;
- Data grandparent;
- OneDrive/Desktop/SymC_Economics;
- OneDrive/Desktop;
- local Desktop;
- Downloads.

The scientific contents of candidate files are not opened during search.

Exactly one date-matched MBP10 .zst candidate is still required. Zero or multiple candidates cause refusal.

## Verification

Search-root code commit:
`84e7c3b337420d8e7c0ea4dcce671d55440f17b2`

Final test-adjustment / execution commit:
`2c57558e23ab3989664deb3f83d497e4d1c05325`

CI run:
`36354557290`

CI conclusion:
`success`

The scientific Q038-P1-v1 freeze is unchanged.

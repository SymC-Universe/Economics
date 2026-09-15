# MNQ MBP-10 Holdout Freeze — 2026-09-14

Status: **SEALED / NOT USED FOR MODEL DEVELOPMENT**

## Dataset identity

- Provider: Databento
- Dataset: `GLBX.MDP3`
- Input smart symbol: `MNQ.c.0`
- Input symbology: continuous, calendar-roll, rank 0
- Output symbology: `instrument_id`
- Schema: `mbp-10`
- Encoding/compression: CSV / Zstandard
- Query interval: `[2026-06-09T00:00:00Z, 2026-06-12T00:00:00Z)`
- Observation dates returned: 2026-06-09, 2026-06-10, 2026-06-11
- Databento job ID: `GLBX-20260707-MJC5YBJBLU`

The user folder label `MBR_10_June 9-12` is therefore interpreted as a half-open query interval, not four observation dates.

## Sealed observation files

| Date | File | Databento SHA-256 | Bytes |
|---|---|---|---:|
| 2026-06-09 | `glbx-mdp3-20260609.mbp-10.csv.zst` | `738853dc7fe01c48c313df2b960a0e6f7c979573ded25a9055310613e8256107` | 2,498,418,523 |
| 2026-06-10 | `glbx-mdp3-20260610.mbp-10.csv.zst` | `a24db4cd6361442be1d2110f47abdf68203dc7be6f099f033aa17045ea570e29` | 2,344,279,725 |
| 2026-06-11 | `glbx-mdp3-20260611.mbp-10.csv.zst` | `9d57eccc1358d6431406883060386b302b332db9149b280dbd3be0663763295d` | 2,036,662,238 |

## Freeze rule

Until an explicit qualification/preregistration record is frozen:

1. do not decompress the three observation files;
2. do not inspect rows, distributions, symbols resolved inside the files, outcomes, or summary statistics;
3. do not tune feature definitions, admission thresholds, models, χ rules, Χ architecture, or prediction targets using these observations;
4. metadata, filenames, byte sizes, provider condition status, and provider hashes may be used only for provenance and integrity;
5. the data may be released from quarantine only through an explicit gate record stating the frozen question, endpoints, comparator, exclusions, uncertainty method, and failure criteria.

The ZIP directory was inspected to confirm the files exist. Observation-level contents were not read by ChatGPT during the 2026-09-14 intake.

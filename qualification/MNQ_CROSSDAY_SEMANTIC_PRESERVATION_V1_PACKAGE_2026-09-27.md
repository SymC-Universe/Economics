# MNQ Cross-Day Semantic Preservation v1 Package

Date: 2026-09-27
Qualification gate: Q037
Stage: P0-D
Holdout: `SEALED_NOT_ACCESSED`

## Frozen package

Archive:
`MNQ_CrossDay_Semantic_Preservation_v1.zip`

SHA-256:
`3a20dbd288b3f4ac52c7ce0c30ca3efe99aa5aacd54f9d8530989506f1b6523a`

Frozen code commit:
`31b949d75efe5ba3010737193864f52a8245a47c`

The package runs the fixed cross-day semantic-preservation analysis on:
- 2026-05-27;
- 2026-05-29;
- 2026-06-01;
- 2026-06-02.

It uses ordinary UTC wall-clock time, fixed k = 2, 3, 4, 6, 10, and the prospectively frozen 256-direction isotropic control with seed 20260927.

The same random directions are reused everywhere. Their empirical percentiles are descriptive controls, not p-values.

## Checkpoint behavior

The runner writes a checkpoint after every completed or skipped window. If interrupted, rerunning the BAT resumes from the stored checkpoint.

## Expected return artifact

Upload only:

`CROSSDAY_SEMANTIC_PRESERVATION_INDEX.json`

June 9-11 is not referenced or opened by the runner.

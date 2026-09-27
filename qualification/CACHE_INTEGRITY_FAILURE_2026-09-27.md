# Development Sweep Cache-Integrity Failure

Date: 2026-09-27
Stage: P0-D/P0-Q infrastructure qualification
Scientific result affected: NO
Holdout affected: NO

## Observed failure

The MNQ Development Sweep v2 stopped during phase coverage scanning with:

`EOFError: Compressed file ended before the end-of-stream marker was reached`

The exception was raised while Python's gzip reader traversed a cached
`.features.v2.csv.gz` file.

## Root cause

The v2 extractor wrote directly to the final feature-cache filename. The sweep
treated the simultaneous existence of the feature file and summary file as
sufficient evidence that the cache was reusable. A previously interrupted or
otherwise truncated gzip could therefore retain a plausible final filename and
be trusted until a later full read reached the damaged stream tail.

This is an implementation/cache-integrity failure. It does not indicate a
problem with the underlying Databento observations, the modal result, chi
licensing, or the sealed June 9-11 holdout.

## Corrections

1. Feature extraction now writes to temporary paths.
2. The temporary gzip is read through EOF/CRC before promotion.
3. Final feature and summary paths are populated by atomic replacement only
   after successful extraction and validation.
4. Cached development feature files are fully gzip-validated before reuse.
5. When a summary exists, its recorded output SHA-256 is checked against the
   cached feature file.
6. Broken sweep-owned caches are preserved under a `.corrupt` suffix and only
   the affected day is rebuilt.
7. The external earlier May 27 feature cache is never modified if corrupt;
   May 27 is rebuilt inside the sweep workspace from raw development data.
8. Missing May 27 reusable output now also falls back to raw May 27 development
   data.
9. Regression tests include a deliberately truncated gzip and summary-hash
   mismatch.

## Verification

Relevant frozen repair commits:
- atomic extraction: `c3a04b8a19edeec2f8765028b66506c54fa13818`
- self-healing cache validation: `80fdd3989fbf523bb4f484c8354620b040b1ed9c`
- truncated-cache regression tests: `9c0a50ade8a4ae4fadaf2ad9625ae36b98237a27`
- May 27 missing-cache fallback: `22dbccf2cb7f1921598c72715f4d7c232932c456`

GitHub Actions passed on all four commits.

## Replacement package

Package: `MNQ_Development_Sweep_v3.zip`
Frozen code commit: `22dbccf2cb7f1921598c72715f4d7c232932c456`
SHA-256: `48b2ee1476afd315049500cccc19cbc321065759ad4a5745923ba9e46cbc6c8e`

The output workspace remains unchanged so valid prior work can be reused. The
package references development dates May 27, May 28, May 29, June 1 and June 2
only. June 9-11 remains sealed and is not referenced or opened.

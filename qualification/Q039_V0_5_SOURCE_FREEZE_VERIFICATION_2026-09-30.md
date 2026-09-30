# Q039 v0.5 Source Freeze Verification

**Date:** 2026-09-30  
**Outcome firewall:** No Q039 Layer R, Layer L, or scientific NC7 outcome was opened.

The five development feature files were located on the connected authorized research computer under:

`C:\Users\CCGTi\OneDrive\Desktop\SymC_Economics\SymC_TF\Data\_symc_development_sweep_v1\features`

Each file was hashed directly with PowerShell `Get-FileHash -Algorithm SHA256`. The direct hashes matched the previously generated v2 extraction summary identities exactly.

| Date | Bytes | Direct SHA-256 | Instrument | Symbol |
|---|---:|---|---|---|
| 20260527 | 36277483 | `58bbd2a2d9e26e84c3428abaa8ce8602f2f9dae16abb140bedd78926533b09c1` | 42004936 | MNQ.c.0 |
| 20260528 | 36376205 | `3c6413eefec9a186376510c614643001fcb2303713af8cbfc5a234b3161e2f25` | 42004936 | MNQ.c.0 |
| 20260529 | 33409002 | `c417754c6c7eca49f5cbd9b7f057266be4b357c8e6de0778e02e8f38a253e40e` | 42004936 | MNQ.c.0 |
| 20260601 | 36093079 | `9a7554e2053283d7fb3a65d14268a3be59ef31efe5a86186d39f7bb0d3a1033d` | 42004936 | MNQ.c.0 |
| 20260602 | 36180166 | `d836d67dd663e91413be48d056a9da5b84bcb3373beaec549f9600c8d3c8b972` | 42004936 | MNQ.c.0 |

The five corresponding extraction summaries each report one instrument only (`42004936`), one symbol only (`MNQ.c.0`), and no multiple-instrument or multiple-symbol condition.

This is provenance/identity work only. It does not compute a Q039 scientific statistic.

**Disposition:** `Q039_V0_5_SOURCE_FREEZE_VERIFIED`

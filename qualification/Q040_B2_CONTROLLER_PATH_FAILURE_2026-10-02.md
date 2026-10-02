# Q040 B2 Controller Path Failure

**Date:** 2026-10-02
**Stage:** disjoint B2 baseline qualification launch
**Scientific authority:** Q040 Baseline Operator Plan Delta v0.2
**Original controller commit:** `5cf576cd6ab2e23c6f951a1967c22a1e2e2ffbc4`
**Mechanical repair commit:** `c697471fabd01b2ce97879f84f395dc9205187fe`
**Real Q040 outcomes opened:** NO
**Classification:** MECHANICAL IMPLEMENTATION FAILURE

The first durable-controller invocation launched all four B2 shard processes, but every child exited before scientific evaluation with `ModuleNotFoundError` because the repository root was not propagated to child `PYTHONPATH`.

No scientific result was produced. No threshold, seed namespace, candidate window, control set, qualification rule, or outcome firewall changed.

The failed run remains preserved locally at:
`C:\Users\CCGTi\SymC_runs\q040_b2_5cf576_20261002`.

The mechanical repair prepended the frozen repository root to child `PYTHONPATH`. The repaired retry used the identical B2 science and completed successfully.

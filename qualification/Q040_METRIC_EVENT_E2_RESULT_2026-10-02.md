# Q040 Metric/Event E2 Synthetic Qualification Result — 2026-10-02

## Authority and scope

This record preserves the completed, prospectively frozen Q040 E2 metric/event/horizon selection bank executed locally on `Home` under SymC GOM v1.0 and the Research Continuity and Execution Protocol. It is synthetic-only. Q040 real outcomes remained SEALED throughout.

Scientific authority:
- B2 baseline result commit: `d796fa2b9ad482ea087eafa543d520475fbe89b8`
- E2 freeze commit: `a2080983e1688101eae2e99bf02582c03c8e624c`
- E2 shard implementation commit: `d34dbbacdfb4016160a9b9c24c79f7c1582f29a5`
- E2 combiner commit: `fa8bb7888d22f2a76518bf4fa94bfcc3cbda6894`
- Successor-controller commit: `1e8af484b7dabbb3a8b8ab892654fdce3b6d68dc`
- Frozen global baseline: K1, 640 samples
- E2 seed namespace: `1200+r`

## Execution result

Run directory:
`C:\Users\CCGTi\SymC_runs\q040_e2_successor_1e8af48_20261002`

Controller completion:
- started: `2026-10-02T18:45:46.694797+00:00`
- completed: `2026-10-02T19:33:49.884857+00:00`
- scales completed: 15, 30, 60, 300 seconds
- scale exit codes: 0, 0, 0, 0
- failed scales: none
- combine exit code: 2
- combine stderr: empty
- combined artifact SHA-256: `70AFED4781258AD8F32D6CFA44F78B870D6DF9A8C16389D94F0448D06EAF13FF`

The combiner's scientific disposition is:

`Q040_EVENT_DEFINITION_REFUSED_E2`

No metric/event tuple satisfied the frozen eligibility gates. `selected_metric_event_tuple=null`. The separate horizon calculation returned 20 samples, but `horizon_qualifier=null`; because the metric/event gate refused, that horizon has no promotion effect.

## Failure / outlier preservation

The highest-ranked D2 family member was the 0.95 entry quantile, 0.50 return quantile, sustain 2, minimum separation 2 candidate. It had overall median recall 0.875 but failed support with 567 refused folds, minimum cell median recall 0.25, infinite median return error, maximum cell median false ratio 3.625, and median terminal concordance 0.125. It is ineligible.

The leading D1 candidates had no fit-refused folds and support could be satisfied, but the best displayed family still failed the frozen performance gates. For example, D1 with entry 0.95, return 0.50, sustain 2, separation 5 had overall median recall 0.75, minimum cell median recall 0.026542160660028458, infinite median return error, maximum cell median false ratio 1.0, and median terminal concordance 0.0. It is ineligible.

These failures are preserved as scientific evidence. They are not to be rescued by threshold relaxation, post hoc tuple selection, grid expansion, support-rule changes, or use of Q040 real outcomes.

## Disposition and gate

Q040 E2 is CLOSED with scientific refusal. The separate confirmatory C bank is NOT authorized. Real Q040 outcomes remain SEALED.

The exact next stage is:

`SCIENTIFIC_GATE / Q040_E2_EVENT_DEFINITION_REFUSAL_FAILURE_OUTLIER_AUDIT`

The audit may interpret why the frozen D1/D2 event family failed, identify failure structure and outliers, and determine whether a genuinely new prospective plan is scientifically warranted. It may not retune this E2 bank or reclassify any tested tuple as confirmatory evidence.

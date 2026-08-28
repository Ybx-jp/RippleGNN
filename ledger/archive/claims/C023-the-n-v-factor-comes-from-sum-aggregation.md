---
id: C023-the-n-v-factor-comes-from-sum-aggregation
kind: error-model
grade: measured
credence:
stated: 2026-08-27
author: backfill
source: "lab/005:12, 46"
inventory_ref: B23
fingerprint: "Under mean aggregation the error is exactly degree-invariant at fixed stale fraction,"
locator:
  metric: "centre-node output error under a fixed 0.1 perturbation, mean vs sum aggr"
  cohort: "star graph, one centre with deg neighbours, 16 dim, one layer, eval() mode"
  condition: "UNTRAINED weights; degree 5-2000; stale fraction 5/25/50%; one layer only, so cross-layer compounding is not measured"
---

## Statement

"the |N(v)| factor comes from **sum** aggregation… mean or max admits a much tighter bound" → measured: "Under mean aggregation the error is **exactly degree-invariant at fixed stale fraction**, to six significant figures across two orders of magnitude of degree."

## Depends on this

Threatens A2 and A4; reframes dl's R1; makes the target claim degree-independent if it survives

<!-- FROZEN ABOVE. Everything above this line is written once and never edited. -->

## Verdicts

- **2026-08-27** · `corroborated` · grade `measured`
  - evidence: `lab/005`
  - read-in: `lab/claims-inventory-draft.md`
  - note: Standing, with lab/005's four stated threats (one layer, one perturbation magnitude, star graph, untrained weights). The mechanism is called "exact and structural"; the magnitudes are explicitly not load-bearing.

- **2026-08-27** · `corroborated` · grade `measured`
  - evidence: `lab/005-mean-aggregation-makes-it-a-fraction-not-a-count.md`, compared directly against this statement
  - read-in: direct text comparison, 2026-08-27 quotation audit
  - note: Quotation verified verbatim against the source this entry names, allowing only markdown emphasis and sentence-case. No words added, dropped or reordered, and no unmarked elision.

## References

Where this claim is restated outside the ledger. Appended at write time; the referencing
document never names this entry: a claim's status lives here and nowhere else, and an id
copied into a document goes stale the moment that status changes, silently, because
nothing checks it from that side.
When status tips to `refuted` or `superseded`, every row here is work to do.

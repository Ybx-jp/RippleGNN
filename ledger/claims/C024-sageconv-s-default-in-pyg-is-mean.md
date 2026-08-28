---
id: C024-sageconv-s-default-in-pyg-is-mean
kind: error-model
grade: measured
credence:
stated: 2026-08-27
author: backfill
source: "lab/005:18-21"
inventory_ref: B24
fingerprint: "SAGEConv's default in PyG is mean"
locator:
  metric: "SAGEConv.__init__ default aggr"
  cohort: "PyG source, installed version"
  condition: "read from code, not benchmarked"
---

## Statement

"SAGEConv's default in PyG is mean"

## Depends on this

Everything in B23 applies to the project as configured

<!-- FROZEN ABOVE. Everything above this line is written once and never edited. -->

## Verdicts

- **2026-08-27** · `corroborated` · grade `argued`
  - evidence: none found: 2026-08-27 sweep of the repo and the four consultation exchanges surfaced nothing bearing on this claim
  - read-in: `lab/claims-inventory-draft.md`
  - note: Standing.

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

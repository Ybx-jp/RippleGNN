---
id: C005-full-recompute-timings-for-named-benchmarks-cora-0
kind: resource-model
grade: measured
credence:
stated: 2026-08-27
author: backfill
source: "lab/004:22-28"
inventory_ref: B5
fingerprint: "Full-recompute timings for named benchmarks: Cora 0.504 ms, CiteSeer 0.519 ms, tgbl-wiki"
locator:
  metric: "full-recompute wall-clock, ms"
  cohort: "synthetic random graphs at published benchmark sizes, NOT the real datasets loaded"
  condition: "2-layer GraphSAGE; 128 dim; published approximate mean degrees"
---

## Statement

Full-recompute timings for named benchmarks: Cora 0.504 ms, CiteSeer 0.519 ms, tgbl-wiki 1.729 ms, Reddit-JODIE 2.099 ms, PubMed 2.047 ms; Reddit and ogbn-products OOM

## Depends on this

The refutation of eval-methodology's primary (A8) and the confirmation of dl's tier C

<!-- FROZEN ABOVE. Everything above this line is written once and never edited. -->

## Verdicts

- **2026-08-27** · `corroborated` · grade `argued`
  - evidence: none found: 2026-08-27 sweep of the repo and the four consultation exchanges surfaced nothing bearing on this claim
  - read-in: `lab/claims-inventory-draft.md`
  - note: Standing with the stated caveat.

## References

Where this claim is restated outside the ledger. Appended at write time; the referencing
document never names this entry: a claim's status lives here and nowhere else, and an id
copied into a document goes stale the moment that status changes, silently, because
nothing checks it from that side.
When status tips to `refuted` or `superseded`, every row here is work to do.

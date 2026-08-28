---
id: C003-the-ceiling-is-an-edge-count-0-51
kind: resource-model
grade: measured
credence:
stated: 2026-08-27
author: backfill
source: "lab/004:41"
inventory_ref: B3
fingerprint: "the ceiling is an edge count… ~0.51 GiB per million edges at"
locator:
  metric: "peak VRAM at OOM, GiB"
  cohort: "synthetic random graphs, one SAGEConv layer"
  condition: "hidden dim 128; edges varied 5M-20M"
---

## Statement

"the ceiling is an edge count… ~0.51 GiB per million edges at 128-dim; between 15M and 20M edges"

## Depends on this

The admissible band (5M–15M edges at 128-dim); the choice of Reddit-at-64; the refutation of both experts' primaries

<!-- FROZEN ABOVE. Everything above this line is written once and never edited. -->

## Verdicts

- **2026-08-27** · `corroborated` · grade `argued`
  - evidence: none found: 2026-08-27 sweep of the repo and the four consultation exchanges surfaced nothing bearing on this claim
  - read-in: `lab/claims-inventory-draft.md`
  - note: Standing. Caveat B41.

## References

Where this claim is restated outside the ledger. Appended at write time; the referencing
document never names this entry: a claim's status lives here and nowhere else, and an id
copied into a document goes stale the moment that status changes, silently, because
nothing checks it from that side.
When status tips to `refuted` or `superseded`, every row here is work to do.

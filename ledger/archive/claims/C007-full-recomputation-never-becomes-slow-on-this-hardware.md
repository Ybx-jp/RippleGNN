---
id: C007-full-recomputation-never-becomes-slow-on-this-hardware
kind: resource-model
grade: measured
credence:
stated: 2026-08-27
author: backfill
source: "lab/001:39, `CLAUDE.md`, public README"
inventory_ref: B7
fingerprint: "Full recomputation never becomes slow on this hardware. It becomes impossible."
locator:
  metric: "full-graph inference wall-clock and peak VRAM"
  cohort: "synthetic random graphs"
  condition: "mean degree 10; 128 dim; 200k / 1M / 4M nodes"
---

## Statement

"Full recomputation never becomes slow on this hardware. It becomes *impossible*."

## Depends on this

The reframing of the cost axis from latency to residency; dl's R3; eval-meth's R5

<!-- FROZEN ABOVE. Everything above this line is written once and never edited. -->

## Verdicts

- **2026-08-27** · `corroborated` · grade `measured`
  - evidence: `lab/003`
  - read-in: `lab/claims-inventory-draft.md`
  - note: Standing, and independently predicted by dl in R1 §2 from NBFNet's published wall-clock (lab/003 calls this the convergence-from-two-directions result).

- **2026-08-27** · `corroborated` · grade `measured`
  - evidence: `CLAUDE.md`, compared directly against this statement
  - read-in: direct text comparison, 2026-08-27 quotation audit
  - note: Quotation verified verbatim against the source this entry names, allowing only markdown emphasis and sentence-case. No words added, dropped or reordered, and no unmarked elision.

## References

Where this claim is restated outside the ledger. Appended at write time; the referencing
document never names this entry: a claim's status lives here and nowhere else, and an id
copied into a document goes stale the moment that status changes, silently, because
nothing checks it from that side.
When status tips to `refuted` or `superseded`, every row here is work to do.

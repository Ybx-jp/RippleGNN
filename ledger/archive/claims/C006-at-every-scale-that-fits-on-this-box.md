---
id: C006-at-every-scale-that-fits-on-this-box
kind: resource-model
grade: measured
credence:
stated: 2026-08-27
author: backfill
source: "lab/001:51-55"
inventory_ref: B6
fingerprint: "at every scale that fits on this box, exact nearest-neighbor search is"
locator:
  metric: "exact kNN wall-clock, s"
  cohort: "embedding matrices 100k and 250k x 128"
  condition: "chunked so the similarity matrix never fully materializes; measured only to 250k"
---

## Statement

"at every scale that fits on this box, exact nearest-neighbor search is affordable, so no ANN index is needed… Exact search removes a confound rather than merely saving a dependency."

## Depends on this

Every rank-survival metric in the project; the removal of ANN recall error as a confound; dl's ANN-as-second-cache framing

<!-- FROZEN ABOVE. Everything above this line is written once and never edited. -->

## Verdicts

- **2026-08-27** · `contested` · grade `argued`
  - evidence: none found: 2026-08-27 sweep of the repo and the four consultation exchanges surfaced nothing bearing on this claim
  - read-in: `lab/claims-inventory-draft.md`
  - note: **Under-examined.** Measured only to 250k. Reddit-at-64 has 232,965 nodes, so the chosen operating point sits at the measured edge, and the primary metric needs a kNN pass *per episode per arm*. See P8.

- **2026-08-27** · `corroborated` · grade `measured`
  - evidence: `lab/001-full-recompute-is-a-memory-wall-not-a-time-wall.md`, compared directly against this statement
  - read-in: direct text comparison, 2026-08-27 quotation audit
  - note: Quotation verified verbatim against the source this entry names, allowing only markdown emphasis and sentence-case. No words added, dropped or reordered, and no unmarked elision.

## References

Where this claim is restated outside the ledger. Appended at write time; the referencing
document never names this entry: a claim's status lives here and nowhere else, and an id
copied into a document goes stale the moment that status changes, silently, because
nothing checks it from that side.
When status tips to `refuted` or `superseded`, every row here is work to do.

- `lab/001-full-recompute-is-a-memory-wall-not-a-time-wall.md` · record · seeded by the 2026-08-27 backfill

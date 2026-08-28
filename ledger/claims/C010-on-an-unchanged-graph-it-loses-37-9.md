---
id: C010-on-an-unchanged-graph-it-loses-37-9
kind: fidelity-measurement
grade: measured
credence:
stated: 2026-08-27
author: backfill
source: "lab/002:19-27"
inventory_ref: B10
fingerprint: "on an unchanged graph it loses 37.9% of each node's top-20 neighborhood"
locator:
  metric: "mean cosine and mean kNN@20 overlap, sampled seed 1 vs seed 2"
  cohort: "50k nodes / 500k edges uniform random, 64 dim"
  condition: "UNTRAINED weights; num_neighbors=[10,10]; batch 1024; K=20"
---

## Statement

"on an unchanged graph it loses 37.9% of each node's top-20 neighborhood on average, with a worst case of 19 of 20 neighbors changed" while cosine reads 0.991

## Depends on this

The rank-primary rule in `experiments/README.md`; dl's instruction to carry it forward as a standalone methodological finding; eval-meth's rejection of a cosine-drift sweep

<!-- FROZEN ABOVE. Everything above this line is written once and never edited. -->

## Verdicts

- **2026-08-27** · `corroborated` · grade `measured`
  - evidence: `lab/002`
  - read-in: `lab/claims-inventory-draft.md`
  - note: Standing, and **corroborated from literature** by eval-meth R2 Correction 3 (sampling-order seed instability comparable to a real data change, on *trained* models) — which upgrades it past the "qualitative only" caveat lab/002 itself imposed.

- **2026-08-27** · `corroborated` · grade `measured`
  - evidence: `lab/002-the-noise-floor-is-a-rank-metric-problem.md`, compared directly against this statement
  - read-in: direct text comparison, 2026-08-27 quotation audit
  - note: Quotation verified verbatim against the source this entry names, allowing only markdown emphasis and sentence-case. No words added, dropped or reordered, and no unmarked elision.

## References

Where this claim is restated outside the ledger. Appended at write time; the referencing
document never names this entry: a claim's status lives here and nowhere else, and an id
copied into a document goes stale the moment that status changes, silently, because
nothing checks it from that side.
When status tips to `refuted` or `superseded`, every row here is work to do.

- `lab/002-the-noise-floor-is-a-rank-metric-problem.md` · record · seeded by the 2026-08-27 backfill

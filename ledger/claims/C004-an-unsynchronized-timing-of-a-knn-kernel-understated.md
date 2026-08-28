---
id: C004-an-unsynchronized-timing-of-a-knn-kernel-understated
kind: resource-model
grade: measured
credence:
stated: 2026-08-27
author: backfill
source: "`CLAUDE.md`:78, `experiments/README.md`"
inventory_ref: B4
fingerprint: "an unsynchronized timing of a kNN kernel understated it by 173x, because"
locator:
  metric: "kNN kernel wall-clock, synchronized vs not"
  cohort: "this box, RTX 3060"
  condition: "CUDA; torch.cuda.synchronize() on both sides"
---

## Statement

"an unsynchronized timing of a kNN kernel understated it by 173x, because it timed queue submission rather than compute"

## Depends on this

The always-synchronize rule in both durable docs; every timing in lab/001 and lab/004

<!-- FROZEN ABOVE. Everything above this line is written once and never edited. -->

## Verdicts

- **2026-08-27** · `corroborated` · grade `argued`
  - evidence: none found: 2026-08-27 sweep of the repo and the four consultation exchanges surfaced nothing bearing on this claim
  - read-in: `lab/claims-inventory-draft.md`
  - note: Standing.

## References

Where this claim is restated outside the ledger. Appended at write time; the referencing
document never names this entry: a claim's status lives here and nowhere else, and an id
copied into a document goes stale the moment that status changes, silently, because
nothing checks it from that side.
When status tips to `refuted` or `superseded`, every row here is work to do.

- `CLAUDE.md` · standing · seeded by the 2026-08-27 backfill

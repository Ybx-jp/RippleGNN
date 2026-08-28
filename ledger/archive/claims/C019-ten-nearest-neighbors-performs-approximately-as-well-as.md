---
id: C019-ten-nearest-neighbors-performs-approximately-as-well-as
kind: fidelity-measurement
grade: argued
credence:
stated: 2026-08-27
author: backfill
source: "eval-meth R2 §0"
inventory_ref: B19
fingerprint: "Ten nearest neighbors performs approximately as well as a higher number"
locator:
---

## Statement

"Ten nearest neighbors performs approximately as well as a higher number" / k=5 top-performing as predictor of downstream disagreement

## Depends on this

The choice of K in every rank metric

<!-- FROZEN ABOVE. Everything above this line is written once and never edited. -->

## Verdicts

- **2026-08-27** · `open` · grade `measured`
  - evidence: `lab/002`
  - read-in: `lab/claims-inventory-draft.md`
  - note: lab/002 used K=20 and nothing has changed it.

- **2026-08-27** · `contested` · grade `measured`
  - evidence: the eval-meth round-2 exchange §0, read in full; and `lab/002`
  - read-in: direct text comparison, 2026-08-27 quotation audit
  - note: Two defects. The elision drops "of nearest neighbors (e.g., 100)", which is the comparator that gives the claim its content, and the upstream source is unidentified on both sides — the expert named no paper, and context places it in word-embedding stability, not graphs. Separately, this entry's earlier verdict cites `lab/002` as corroborating evidence, but lab/002 used K=20, which is what the claim argues against; the cited evidence is the target of the claim, not support for it.

## References

Where this claim is restated outside the ledger. Appended at write time; the referencing
document never names this entry: a claim's status lives here and nowhere else, and an id
copied into a document goes stale the moment that status changes, silently, because
nothing checks it from that side.
When status tips to `refuted` or `superseded`, every row here is work to do.

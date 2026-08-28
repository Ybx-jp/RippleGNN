---
id: C025-the-influence-distribution-ix-for-any-node-x
kind: error-model
grade: argued
credence:
stated: 2026-08-27
author: backfill
source: "dl R2 §2"
inventory_ref: B25
fingerprint: "the influence distribution I_x for any node x is equivalent, in expectation,"
locator:
---

## Statement

"the influence distribution I_x for any node x is equivalent, in expectation, to the k-step random walk distribution" (JKNet Thm 1)

## Depends on this

dl's R1 design (influence mass computable with sparse mat-vecs, no model); "predicts the fidelity curve before you run a single GNN forward pass"

<!-- FROZEN ABOVE. Everything above this line is written once and never edited. -->

## Verdicts

- **2026-08-27** · `corroborated` · grade `argued`
  - evidence: none found: 2026-08-27 sweep of the repo and the four consultation exchanges surfaced nothing bearing on this claim
  - read-in: `lab/claims-inventory-draft.md`
  - note: Standing.

- **2026-08-27** · `open` · grade `measured`
  - evidence: the dl round-2 exchange §2, read in full
  - read-in: direct text comparison, 2026-08-27 quotation audit
  - note: Third-party result, attributed here to the expert who relayed it. The expert named it: "That is Theorem 1 of JKNet." The quotation also drops `∈V` from `x∈V` with no elision, and stops before the condition "on the self-loop-augmented graph", so the theorem reads as holding on the raw graph.

## References

Where this claim is restated outside the ledger. Appended at write time; the referencing
document never names this entry: a claim's status lives here and nowhere else, and an id
copied into a document goes stale the moment that status changes, silently, because
nothing checks it from that side.
When status tips to `refuted` or `superseded`, every row here is work to do.

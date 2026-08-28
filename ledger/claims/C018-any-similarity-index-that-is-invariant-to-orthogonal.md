---
id: C018-any-similarity-index-that-is-invariant-to-orthogonal
kind: fidelity-measurement
grade: argued
credence:
stated: 2026-08-27
author: backfill
source: "eval-meth R2 §0"
inventory_ref: B18
fingerprint: "any similarity index that is invariant to orthogonal transformation can be made"
locator:
---

## Statement

"any similarity index that is invariant to orthogonal transformation can be made invariant to invertible linear transformation by orthogonalizing the columns" → "a QR/whitening step before comparison silently destroys your measurement"

## Depends on this

The pre-registration prohibition on whitening / fitted general-linear alignment

<!-- FROZEN ABOVE. Everything above this line is written once and never edited. -->

## Verdicts

- **2026-08-27** · `open` · grade `argued`
  - evidence: unresolved: the record asserts something bears on this claim and names no artifact for it
  - read-in: `lab/claims-inventory-draft.md`
  - note: Wired to nothing in the repo.

- **2026-08-27** · `corroborated` · grade `argued`
  - evidence: "Similarity of Neural Network Representations Revisited" (https://arxiv.org/html/1905.00414), Appendix B, Proposition 1 — the quoted sentence appears verbatim.
  - read-in: primary source located by literature search; the earlier verdict's chain ended at `lab/claims-inventory-draft.md`.
  - note: Provenance repair, not new evidence. Only the first half of the statement is the source's: the proposition is a proof about orthogonalizing columns via QR. The consequence drawn here — "a QR/whitening step before comparison silently destroys your measurement" — is this project's inference from it and carries no separate source. Still wired to nothing in the repo.

## References

Where this claim is restated outside the ledger. Appended at write time; the referencing
document never names this entry: a claim's status lives here and nowhere else, and an id
copied into a document goes stale the moment that status changes, silently, because
nothing checks it from that side.
When status tips to `refuted` or `superseded`, every row here is work to do.

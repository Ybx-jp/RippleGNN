---
id: C001-4-cores-not-the-gpu-is-the-binding
kind: resource-model
grade: asserted
credence:
stated: 2026-08-27
author: backfill
source: "Former `CLAUDE.md` / public README; **passed to both experts as a settled operator constraint** inside modelling consultation, round 1 and measurement consultation, round 1"
inventory_ref: B1
fingerprint: "4 cores, not the GPU, is the binding constraint, because neighborhood sampling"
locator:
---

## Statement

"4 cores, not the GPU, is the binding constraint, because neighborhood sampling and mutation replay are CPU-bound."

## Depends on this

Propagated into *both* round-1 answers. dl built probe L2 to "prove it with a profile before designing around it". eval-meth built its entire §4e cost-axis ruling on it (B35).

<!-- FROZEN ABOVE. Everything above this line is written once and never edited. -->

## Verdicts

- **2026-08-27** · `refuted` · grade `measured`
  - evidence: `lab/001`
  - read-in: `lab/claims-inventory-draft.md`
  - note: **Refuted** by lab/001. Corrected in both documents. The downstream contamination of two consultations is not itself ledgered anywhere.

## References

Where this claim is restated outside the ledger. Appended at write time; the referencing
document never names this entry: a claim's status lives here and nowhere else, and an id
copied into a document goes stale the moment that status changes, silently, because
nothing checks it from that side.
When status tips to `refuted` or `superseded`, every row here is work to do.

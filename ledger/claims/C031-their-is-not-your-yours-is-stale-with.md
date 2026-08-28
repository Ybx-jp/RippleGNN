---
id: C031-their-is-not-your-yours-is-stale-with
kind: error-model
grade: argued
credence:
stated: 2026-08-27
author: backfill
source: "dl R2 §1"
inventory_ref: B31
fingerprint: "Their ε is not your ε… Yours is stale with respect to"
locator:
---

## Statement

"Their ε is not your ε… Yours is stale with respect to *graph mutation*. Weight drift is global and smooth; mutation drift is sparse and heavy-tailed."

## Depends on this

The claim that anything remains after the novelty withdrawal

<!-- FROZEN ABOVE. Everything above this line is written once and never edited. -->

## Verdicts

- **2026-08-27** · `open` · grade `argued`
  - evidence: unresolved: the record asserts something bears on this claim and names no artifact for it
  - read-in: `lab/claims-inventory-draft.md`
  - note: Untested and it is the load-bearing survivor of the withdrawal.

- **2026-08-27** · `open` · grade `argued`
  - evidence: none found: a literature search for a source asserting that graph-mutation drift is sparse and heavy-tailed, or contrasting it with weight drift, returned nothing. The referent of "their ε" does resolve — it is the historical-embedding staleness bound of "GNNAutoScale" (https://arxiv.org/html/2106.05609), Lemma 1, where ε bounds staleness under weight drift during training.
  - read-in: referent located by literature search; the earlier verdict's chain ended at `lab/claims-inventory-draft.md`.
  - note: Provenance half-resolved. What is being contrasted against is now identifiable; the contrast itself is this project's own argument, with no primary artifact and no measurement. It remains the load-bearing survivor of the novelty withdrawal, and it is the entry in this ledger most worth measuring first.

## References

Where this claim is restated outside the ledger. Appended at write time; the referencing
document never names this entry: a claim's status lives here and nowhere else, and an id
copied into a document goes stale the moment that status changes, silently, because
nothing checks it from that side.
When status tips to `refuted` or `superseded`, every row here is work to do.

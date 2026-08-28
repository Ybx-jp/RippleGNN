---
id: C039-ppi-reddit-and-amazon2m-are-saturated-83-65
kind: experiment-contract
grade: argued
credence:
stated: 2026-08-27
author: backfill
source: "eval-meth R2 §2"
inventory_ref: B39
fingerprint: "PPI, Reddit and Amazon2M are saturated — 83%/65%/90% of nodes used for"
locator:
---

## Statement

"PPI, Reddit and Amazon2M are saturated — 83%/65%/90% of nodes used for training, an artificially small distribution shift; there is no headroom for a refresh effect to live in."

## Depends on this

The rejection of Reddit

<!-- FROZEN ABOVE. Everything above this line is written once and never edited. -->

## Verdicts

- **2026-08-27** · `contested` · grade `measured`
  - evidence: `lab/004`
  - read-in: `lab/claims-inventory-draft.md`
  - note: **Live unresolved conflict.** lab/004 chose Reddit-at-64 on cost grounds and states explicitly: "That objection stands and is unaddressed." lab/004's own resolution is conditional — "either a task on Reddit that is not saturated, or accepting that the fidelity probes carry the result and the downstream task is decoration."

- **2026-08-27** · `contested` · grade `measured`
  - evidence: the eval-meth round-2 exchange §2, read in full
  - read-in: direct text comparison, 2026-08-27 quotation audit
  - note: Two number sets are fused and the load-bearing one is deleted. In the source, 83/65/90% are training fractions (a third-party quotation) and the saturation evidence is separate — 99.5 F1 / 97.0 / 90.4%. This entry keeps "saturated" attached to the training fractions and drops the saturation figures entirely, so a reader takes the percentages to be the evidence for "no headroom". They are not. "There is no headroom for a refresh effect to live in" is the expert's inference, presented here inside the same quotation marks as the third-party clause.

## References

Where this claim is restated outside the ledger. Appended at write time; the referencing
document never names this entry: a claim's status lives here and nowhere else, and an id
copied into a document goes stale the moment that status changes, silently, because
nothing checks it from that side.
When status tips to `refuted` or `superseded`, every row here is work to do.

---
id: C035-on-4-shared-cores-wall-clock-is-a
kind: experiment-contract
grade: argued
credence:
stated: 2026-08-27
author: backfill
source: "eval-meth R1 §4e, restated as R5 in R2"
inventory_ref: B35
fingerprint: "on 4 shared cores, wall-clock is a measurement of your box's scheduler,"
locator:
---

## Statement

"on 4 shared cores, wall-clock is a measurement of your box's scheduler, not of the algorithm. Report FLOPs, nodes-revisited, and messages-passed as the primary cost axes"

## Depends on this

Nothing in the repo. The conclusion is separately supported by lab/001 (memory binds), but the argument as given rests on the four-cores claim

<!-- FROZEN ABOVE. Everything above this line is written once and never edited. -->

## Verdicts

- **2026-08-27** · `open` · grade `argued`
  - evidence: none found: 2026-08-27 sweep of the repo and the four consultation exchanges surfaced nothing bearing on this claim
  - read-in: `lab/claims-inventory-draft.md`
  - note: **Accepted nowhere.** `experiments/README.md` requires no cost instrumentation at all. The cost half of a cost/fidelity trade-off currently has no contract. See P9.

## References

Where this claim is restated outside the ledger. Appended at write time; the referencing
document never names this entry: a claim's status lives here and nowhere else, and an id
copied into a document goes stale the moment that status changes, silently, because
nothing checks it from that side.
When status tips to `refuted` or `superseded`, every row here is work to do.

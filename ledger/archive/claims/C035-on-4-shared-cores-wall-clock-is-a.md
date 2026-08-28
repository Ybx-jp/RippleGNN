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

- **2026-08-27** · `contested` · grade `measured`
  - evidence: the eval-meth round-1 exchange §4e and the round-2 exchange R5, both read in full
  - read-in: direct text comparison, 2026-08-27 quotation audit
  - note: `source:` is wrong as to round 2, and the round-1 quotation is cut where it matters. The elision removes the disposition of wall-clock: the full sentence continues "and wall-clock only as a serialized distribution on an idle box, explicitly labelled as this-machine-only." As stored the entry reads "do not use wall-clock", which appears to conflict with `CLAUDE.md`'s instruction to record wall-clock as a measured quantity; with the clause restored it does not. §4e's enclosing bullet is "What is NOT affordable" — a calibrated cost/latency Pareto frontier — so the claim is scoped to that, not to cost instrumentation generally. Round 2's R5 contains no sentence about 4 shared cores or a scheduler and does not make these the primary axes; it names different ones — "the honest cost axis is peak resident memory and fraction-of-graph-touched, not seconds" — from a memory premise, not a cores premise. The restatement this entry cites does not exist.

## References

Where this claim is restated outside the ledger. Appended at write time; the referencing
document never names this entry: a claim's status lives here and nowhere else, and an id
copied into a document goes stale the moment that status changes, silently, because
nothing checks it from that side.
When status tips to `refuted` or `superseded`, every row here is work to do.

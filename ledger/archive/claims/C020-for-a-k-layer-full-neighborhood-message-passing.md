---
id: C020-for-a-k-layer-full-neighborhood-message-passing
kind: error-model
grade: argued
credence:
stated: 2026-08-27
author: backfill
source: "dl R1 §1"
inventory_ref: B20
fingerprint: "For a k-layer full-neighborhood message-passing model, this never happens, and the answer"
locator:
---

## Statement

"For a k-layer full-neighborhood message-passing model, this never happens, and the answer is not empirical — it is definitional. Exact k-hop refresh does not *approximate* global recomputation; it *equals* it, bit for bit."

## Depends on this

**The entire accepted reframe.** MANIFEST's locality question declared to have no empirical content; the r-sweep replaces it; lab/003 records the acceptance as one of round one's two headline corrections

<!-- FROZEN ABOVE. Everything above this line is written once and never edited. -->

## Verdicts

- **2026-08-27** · `open` · grade `argued`
  - evidence: none found: 2026-08-27 sweep of the repo and the four consultation exchanges surfaced nothing bearing on this claim
  - read-in: `lab/claims-inventory-draft.md`
  - note: Accepted without independent verification on this box. It is scoped to *full-neighborhood deterministic* aggregation and is **false under sampling** — dl says so in the same section ("with sampling turned on, 'exact' stops existing"), but the reframe is carried forward without the scope restriction attached. See P10.

- **2026-08-27** · `corroborated` · grade `measured`
  - evidence: the dl round-1 exchange §1, read in full
  - read-in: direct text comparison, 2026-08-27 quotation audit
  - note: Verbatim, including emphasis. Two things the entry does not carry: the antecedent of "this" is `MANIFEST.md`'s phrase "when local refresh ceases to approximate global recomputation", without which the sentence is unintelligible; and the expert disclaimed novelty for it — "it is folklore that follows immediately from the definition of k-layer message passing… Do not claim novelty anywhere near it." It follows from GraphSAGE's Algorithm 2 and was never measured there.

## References

Where this claim is restated outside the ledger. Appended at write time; the referencing
document never names this entry: a claim's status lives here and nowhere else, and an id
copied into a document goes stale the moment that status changes, silently, because
nothing checks it from that side.
When status tips to `refuted` or `superseded`, every row here is work to do.

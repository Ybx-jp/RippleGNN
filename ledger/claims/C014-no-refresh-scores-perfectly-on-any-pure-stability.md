---
id: C014-no-refresh-scores-perfectly-on-any-pure-stability
kind: fidelity-measurement
grade: argued
credence:
stated: 2026-08-27
author: backfill
source: "`experiments/README.md`; eval-meth R1 §3a"
inventory_ref: B14
fingerprint: "No-refresh… scores perfectly on any pure stability metric — it is maximally"
locator:
---

## Statement

"No-refresh… scores perfectly on any pure stability metric — it is maximally self-consistent because it does nothing. Any metric on which no-refresh wins is degenerate and must be discarded."

## Depends on this

The falsifier-arm requirement for every probe

<!-- FROZEN ABOVE. Everything above this line is written once and never edited. -->

## Verdicts

- **2026-08-27** · `open` · grade `argued`
  - evidence: none found: 2026-08-27 sweep of the repo and the four consultation exchanges surfaced nothing bearing on this claim
  - read-in: `lab/claims-inventory-draft.md`
  - note: Deductively sound *for a pure self-consistency metric under deterministic inference*. Under sampled inference the reference itself resamples, so no-refresh does **not** score perfectly — the claim is stated in the contract without that scope restriction.

- **2026-08-27** · `contested` · grade `measured`
  - evidence: the eval-meth round-1 exchange §3a, read in full
  - read-in: direct text comparison, 2026-08-27 quotation audit
  - note: The second sentence inverts the instruction. The source says such a metric "must be reported as such, never as faithfulness" — kept and relabelled, and paired with a utility metric as a pre-registered joint criterion. This entry reads "is degenerate and must be discarded", which is not in the source and contradicts it; the source also wants no-refresh scored under every probe as the falsifier arm, which discarding would defeat. The first clause also drops the source's scope condition, metrics "of the form 'how much did the embedding space move'".

## References

Where this claim is restated outside the ledger. Appended at write time; the referencing
document never names this entry: a claim's status lives here and nowhere else, and an id
copied into a document goes stale the moment that status changes, silently, because
nothing checks it from that side.
When status tips to `refuted` or `superseded`, every row here is work to do.

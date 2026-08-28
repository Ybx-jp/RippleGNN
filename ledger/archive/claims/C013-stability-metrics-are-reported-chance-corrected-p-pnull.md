---
id: C013-stability-metrics-are-reported-chance-corrected-p-pnull
kind: fidelity-measurement
grade: argued
credence:
stated: 2026-08-27
author: backfill
source: "`experiments/README.md`; from eval-meth R1 §2"
inventory_ref: B13
fingerprint: "Stability metrics are reported chance-corrected… κ = (p − p_null)/(1 − p_null)"
locator:
---

## Statement

"Stability metrics are reported chance-corrected… κ = (p − p_null)/(1 − p_null)", null from k≥5 unchanged-graph reruns, "also the control for the rotation and alignment problem"

## Depends on this

Every stability reading

<!-- FROZEN ABOVE. Everything above this line is written once and never edited. -->

## Verdicts

- **2026-08-27** · `open` · grade `argued`
  - evidence: none found: 2026-08-27 sweep of the repo and the four consultation exchanges surfaced nothing bearing on this claim
  - read-in: `lab/claims-inventory-draft.md`
  - note: **Partly mooted by B9**: in the primary full-graph regime p_null = 0, so κ = p and the k≥5 rerun null costs five runs to produce a constant. The contract requires it unconditionally.

- **2026-08-27** · `contested` · grade `measured`
  - evidence: the eval-meth round-1 exchange, read in full
  - read-in: direct text comparison, 2026-08-27 quotation audit
  - note: Both quotations fail, and the second is the serious one. (1) No sentence "Stability metrics are reported chance-corrected" exists; the source says "Then report chance-corrected:" and requires it **beside the raw value**, a condition this entry drops. `p_null` is a renaming of the source's `p̄₀`. (2) "also the control for the rotation and alignment problem" appears nowhere, in any word order. The source explicitly declined to answer on geometry: "Not found in this scope's corpus: any claim about orthogonal Procrustes, CKA, CCA, rotation-invariance classes… I will not tell you what the literature says, because I do not hold it." The entry converts a stated non-answer into a claim of coverage.

## References

Where this claim is restated outside the ledger. Appended at write time; the referencing
document never names this entry: a claim's status lives here and nowhere else, and an id
copied into a document goes stale the moment that status changes, silently, because
nothing checks it from that side.
When status tips to `refuted` or `superseded`, every row here is work to do.

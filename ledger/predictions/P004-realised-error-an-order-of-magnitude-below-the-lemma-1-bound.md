---
id: P004-realised-error-an-order-of-magnitude-below-the-lemma-1-bound
kind: prediction
grade: argued
credence: 0.60
stated: 2026-08-27
author: backfill
predicted_by: dl
ticket: dl consultation round 2
source: "dl consultation round 2 §5"
inventory_ref: A4
resolves_when: |
  The crispest of the four. Measure realised error and the Lemma-1 bound at each r > 0 and take the ratio; resolves true if the ratio exceeds 10x at every r AND increases with endpoint degree. Both named substrates are partly unavailable (lab/004: ogbn-products and Reddit-at-128 both OOM), so the cohort must be restated before this can run.
resolved:
outcome:
locator:
---

## Statement

on ogbn-products and Reddit, realised error at refresh radius r will be more than an order of magnitude below the Lemma-1 bound at every r > 0, and the gap will widen with endpoint degree — because the bound's |N(v)| factor is worst-case over a neighbourhood whose realised contributions largely cancel.

## Depends on this

Scoring the consultation channel. This entry exists so the prediction can be resolved
against an outcome rather than remembered selectively.

<!-- FROZEN ABOVE. Everything above this line is written once and never edited. -->

## Verdicts

- **2026-08-27** · `contested` · grade `argued`
  - evidence: `lab/005` and `lab/004`
  - read-in: `lab/claims-inventory-draft.md`
  - note: Two independent things bear on it, both post-dating it. (i) lab/005: the |N(v)| factor is a sum-aggregator artifact and GraphSAGE/PyG default to mean, so the degree term drops out of Theorem 2 entirely — the stated mechanism is the wrong mechanism for the model in use, and 'the gap widens with endpoint degree' loses its basis, since under mean aggregation there is no degree factor left to be loose about. (ii) lab/004: the two named substrates OOM at 128-dim; Reddit-at-64 is the survivor. Scoreable only after deciding whether it is read against sum or mean aggregation, and that decision is unmade.

## References

Where this prediction is restated outside the ledger. Appended at write time; the
referencing document never names this entry.

---
id: C017-cka-requires-deleting-97-of-principal-components-before
kind: fidelity-measurement
grade: argued
credence:
stated: 2026-08-27
author: backfill
source: "eval-meth R2 §0 Correction 1"
inventory_ref: B17
fingerprint: "CKA requires deleting 97% of principal components before registering a detectable dissimilarity…"
locator:
---

## Statement

"CKA requires deleting 97% of principal components before registering a detectable dissimilarity… Use Orthogonal Procrustes distance instead."

## Depends on this

Metric selection for the geometric half of B12

<!-- FROZEN ABOVE. Everything above this line is written once and never edited. -->

## Verdicts

- **2026-08-27** · `open` · grade `argued`
  - evidence: unresolved: the record asserts something bears on this claim and names no artifact for it
  - read-in: `lab/claims-inventory-draft.md`
  - note: **Wired to nothing.** No repo document names Procrustes, CKA, or the no-whitening rule. See P9.

- **2026-08-27** · `corroborated` · grade `argued`
  - evidence: "Grounding Representation Similarity with Statistical Testing" (https://arxiv.org/html/2108.01661) — the 97% figure and the Orthogonal Procrustes threshold of ~85% are stated there directly.
  - read-in: primary source located by literature search; the earlier verdict's chain ended at `lab/claims-inventory-draft.md`.
  - note: Provenance repair, not new evidence. The source scopes the 97% figure to **BERT's last layer**, and pairs it with a probing-accuracy drop from 80% to 63%; this entry's statement drops that qualifier and so is broader than what the source supports. "Use Orthogonal Procrustes instead" is a recommendation derived from the comparison, not a quotation. Still wired to nothing in the repo (P9).

- **2026-08-27** · `contested` · grade `measured`
  - evidence: the eval-meth round-2 exchange §0 Correction 1, read in full
  - read-in: direct text comparison, 2026-08-27 quotation audit
  - note: **This corrects the earlier verdict of 2026-08-27 on this entry.** That verdict recorded that the primary source scopes the 97% figure to BERT's last layer, and presented it as something the literature search recovered. It was already in the exchange this entry quotes: the expert's own lead-in, immediately outside the quotation marks, reads "on BERT base's last layer, 'CKA requires deleting 97% of principal components…, by which point SST-2 probing accuracy has already dropped substantially from 80% to 63%'". So the scope was not lost upstream and then recovered here — it was stated to this project and dropped when the entry was written. The elision also swallows the 80%→63% clause. Separately, "Use Orthogonal Procrustes distance instead" flattens a three-way ordering: the expert wrote "we conclude PWCCA > Orthogonal Procrustes > CKA" and called PWCCA defensible too. The expert named no paper; the arXiv id came from this ledger's later search.

## References

Where this claim is restated outside the ledger. Appended at write time; the referencing
document never names this entry: a claim's status lives here and nowhere else, and an id
copied into a document goes stale the moment that status changes, silently, because
nothing checks it from that side.
When status tips to `refuted` or `superseded`, every row here is work to do.

---
id: C045-15-of-predictions-on-a-sentiment-analysis-task
kind: experiment-contract
grade: argued
credence:
stated: 2026-08-27
author: backfill
source: "eval-meth R2 §1/R3"
inventory_ref: B45
fingerprint: "15% of predictions on a sentiment analysis task can disagree due to"
locator:
---

## Statement

"15% of predictions on a sentiment analysis task can disagree due to training the embeddings on an accumulated dataset with just 1% more data" → full-recompute-vs-full-recompute churn is the denominator for every churn number

## Depends on this

The interpretability of any downstream-churn result

<!-- FROZEN ABOVE. Everything above this line is written once and never edited. -->

## Verdicts

- **2026-08-27** · `open` · grade `argued`
  - evidence: unresolved: the record asserts something bears on this claim and names no artifact for it
  - read-in: `lab/claims-inventory-draft.md`
  - note: Wired to nothing in the repo.

- **2026-08-27** · `corroborated` · grade `argued`
  - evidence: "Understanding the Downstream Instability of Word Embeddings" (https://arxiv.org/html/2003.04983) — the quoted sentence appears verbatim.
  - read-in: primary source located by literature search; the earlier verdict's chain ended at `lab/claims-inventory-draft.md`.
  - note: Provenance repair, not new evidence. The source measures word embeddings and bag-of-words sentiment classifiers (SST-2, MR, Subj, MPQA), not graph embeddings — the transfer to this project's setting is an assumption, not a finding. The second half of the statement, that full-recompute-vs-full-recompute churn is the denominator for every churn number, is this project's methodological consequence and carries no separate source. Still wired to nothing in the repo.

- **2026-08-27** · `corroborated` · grade `measured`
  - evidence: the eval-meth round-2 exchange §1/R3, read in full
  - read-in: direct text comparison, 2026-08-27 quotation audit
  - note: Faithful elision, and this entry is the one case in the audit where the ledger is more careful than its source. The expert supplied the sentence with no paper, no authors and no domain; the ledger's later verdict recovered the paper and recorded that the source measures word embeddings and bag-of-words sentiment classifiers, marking the transfer to graph embeddings as an assumption. No correction needed.

## References

Where this claim is restated outside the ledger. Appended at write time; the referencing
document never names this entry: a claim's status lives here and nowhere else, and an id
copied into a document goes stale the moment that status changes, silently, because
nothing checks it from that side.
When status tips to `refuted` or `superseded`, every row here is work to do.

---
id: C052-a-smaller-graph-replayed-dominates-the-largest-that-fits
kind: experiment-contract
grade: argued
credence:
stated: 2026-08-27
author: split
source: "measurement consultation, round 1 §4a; restated in `experiments/README.md`"
supersedes: C036-more-independent-mutation-episodes-and-more-seeds-buy
fingerprint: "A smaller graph replayed over many episodes dominates the largest graph"
locator:
---

## Statement

A smaller graph replayed over many episodes dominates the largest graph that fits in memory.

## Depends on this

Nothing, now. It drove dataset-size reasoning until 2026-08-27.

<!-- FROZEN ABOVE. Everything above this line is written once and never edited. -->

## Verdicts

- **2026-08-27** · `refuted` · grade `argued`
  - evidence: measurement consultation, round 2, Correction 2 — a cited third-party claim that commonly-used small graph benchmarks are "far smaller than real-world graphs, which limits rigorous evaluation of data-hungry models like GNNs and causes unstable, statistically near-identical performance across models"
  - read-in: the round-2 consultation answer, read in full and quoted
  - note: The fallen half of C036, refuted by its own author, who labelled it "partly refuted" and gave the correct form as "many episodes on one adequately-sized graph, not many tiny graphs". The refutation is CITED, not measured: nobody has measured the smaller-versus-larger tradeoff on this box, and round 2 offers no numeric threshold for adequately-sized -- it replaces size with a headroom criterion. `experiments/README.md` was corrected on 2026-08-27.

## References

Where this claim is restated outside the ledger. Appended at write time; the referencing
document never names this entry: a claim's status lives here and nowhere else, and an id
copied into a document goes stale the moment that status changes, silently, because
nothing checks it from that side.

- `experiments/README.md` · removed · corrected in place 2026-08-27; the document no
  longer states this. Kept as a row: that the correction happened is part of the record.

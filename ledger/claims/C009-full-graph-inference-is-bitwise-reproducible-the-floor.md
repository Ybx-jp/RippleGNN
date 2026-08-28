---
id: C009-full-graph-inference-is-bitwise-reproducible-the-floor
kind: fidelity-measurement
grade: measured
credence:
stated: 2026-08-27
author: backfill
source: "lab/002:25"
inventory_ref: B9
fingerprint: "Full-graph inference is bitwise reproducible: the floor is exactly zero."
locator:
  metric: "pairwise cosine and kNN@20 overlap, full-graph vs full-graph"
  cohort: "50k nodes / 500k edges uniform random, 64 dim"
  condition: "UNTRAINED weights; one driver state; one seed pair; not audited for cuDNN autotuning or atomic scatter-add nondeterminism"
---

## Statement

"Full-graph inference is bitwise reproducible: the floor is exactly zero."

## Depends on this

eval-meth's A11 ruling; `experiments/README.md`'s "Full-graph inference has a floor of zero and is preferred wherever it fits"; the argument that κ = p in the primary regime

<!-- FROZEN ABOVE. Everything above this line is written once and never edited. -->

## Verdicts

- **2026-08-27** · `contested` · grade `argued`
  - evidence: measurement consultation, round 1
  - read-in: `lab/claims-inventory-draft.md`
  - note: **Generalized past its evidence** in the public contract. eval-meth R1 §7 Gap 1 explicitly asked for a verified bitwise-determinism check naming cuDNN autotuning and atomic scatter-adds; no note records that audit. See P2.

## References

Where this claim is restated outside the ledger. Appended at write time; the referencing
document never names this entry: a claim's status lives here and nowhere else, and an id
copied into a document goes stale the moment that status changes, silently, because
nothing checks it from that side.
When status tips to `refuted` or `superseded`, every row here is work to do.

- `lab/002-the-noise-floor-is-a-rank-metric-problem.md` · record · seeded by the 2026-08-27 backfill

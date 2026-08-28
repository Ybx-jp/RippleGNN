---
id: C043-adequacy-is-claimable-over-the-declared-grid-never
kind: experiment-contract
grade: argued
credence:
stated: 2026-08-27
author: backfill
source: "eval-meth R2 §4"
inventory_ref: B43
fingerprint: "each mutation type must associate with at least k qualified probes drawn"
locator:
---

## Statement

"Adequacy is claimable over the declared grid, never over the domain of mutations." — with k-MR coverage instantiated as "each mutation type must associate with at least k qualified probes drawn from different estimand families", k=3

## Depends on this

The adequacy argument for the whole project

<!-- FROZEN ABOVE. Everything above this line is written once and never edited. -->

## Verdicts

- **2026-08-27** · `open` · grade `argued`
  - evidence: unresolved: the record asserts something bears on this claim and names no artifact for it
  - read-in: `lab/claims-inventory-draft.md`
  - note: **Wired to nothing.** No repo document names the grid, the coverage criterion, or the requirement that the mutation taxonomy be declared closed before the first run.

- **2026-08-27** · `corroborated` · grade `argued`
  - evidence: "Test Adequacy for Metamorphic Testing: Criteria, Measurement, and Implication" (https://arxiv.org/html/2412.20692) — states the k-MR coverage criterion, and argues adequacy must be relative because "it is impossible to effectively acquire all necessary properties of the SUT".
  - read-in: primary source located by literature search; the earlier verdict's chain ended at `lab/claims-inventory-draft.md`.
  - note: Provenance repair, not new evidence, and it covers only part of the statement. The source's criterion is that each *source input* associates with at least k mutually different *metamorphic relations*; this entry transposes that onto mutation types and probes. Both `k=3` and the requirement that the k probes be "drawn from different estimand families" are this project's instantiation — the source leaves k general and asks only that the relations differ. Still wired to nothing in the repo: no document names the grid, the coverage criterion, or the closed mutation taxonomy.

## References

Where this claim is restated outside the ledger. Appended at write time; the referencing
document never names this entry: a claim's status lives here and nowhere else, and an id
copied into a document goes stale the moment that status changes, silently, because
nothing checks it from that side.
When status tips to `refuted` or `superseded`, every row here is work to do.

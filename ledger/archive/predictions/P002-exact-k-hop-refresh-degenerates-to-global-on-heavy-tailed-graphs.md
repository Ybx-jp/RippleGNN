---
id: P002-exact-k-hop-refresh-degenerates-to-global-on-heavy-tailed-graphs
kind: prediction
grade: argued
credence: 0.78
stated: 2026-08-27
author: backfill
predicted_by: dl
ticket: dl consultation round 2
source: "dl consultation round 2 §5(a)"
inventory_ref: A2
resolves_when: |
  NOT FULLY STATED. 'Effectively-global' carries no threshold, so the prediction is not scoreable as worded. Reconstructed criterion: the median 2-hop reverse-reachable set exceeds some fixed fraction of |V| on a heavy-tailed graph — the fraction was never fixed and must be before this can resolve.
resolved:
outcome:
locator:
---

## Statement

Exact k-hop local refresh degenerates to effectively-global recomputation at k >= 2 on any heavy-tailed graph.

## Depends on this

Scoring the consultation channel. This entry exists so the prediction can be resolved
against an outcome rather than remembered selectively.

<!-- FROZEN ABOVE. Everything above this line is written once and never edited. -->

## Verdicts

- **2026-08-27** · `contested` · grade `argued`
  - evidence: `lab/005`
  - read-in: `lab/claims-inventory-draft.md`
  - note: Threatened by lab/005, not refuted. The 65->78 uplift rested on JKNet's expander result supplying a mechanism; the expander half is untouched. The degree-tail half is undercut: under mean aggregation error is exactly degree-invariant at fixed stale fraction, so hubs are the most robust node per stale neighbour, not the most fragile. The residual question is whether hub neighbourhoods acquire a higher stale fraction, which is an empirical question about mutation locality. Never put back to dl.

## References

Where this prediction is restated outside the ledger. Appended at write time; the
referencing document never names this entry.

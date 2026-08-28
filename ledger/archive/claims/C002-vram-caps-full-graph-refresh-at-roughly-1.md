---
id: C002-vram-caps-full-graph-refresh-at-roughly-1
kind: resource-model
grade: measured
credence:
stated: 2026-08-27
author: backfill
source: "lab/001 line 62; **still live in public `README.md` lines 66-67**"
inventory_ref: B2
fingerprint: "VRAM caps full-graph refresh at roughly 1-2M nodes"
locator:
  metric: "peak VRAM at OOM, GiB"
  cohort: "synthetic uniform random graphs"
  condition: "mean degree 10; hidden dim 128; 2-layer GraphSAGE"
---

## Statement

"VRAM caps full-graph refresh at roughly 1-2M nodes"

## Depends on this

Dataset tier rulings in both R2 tickets; the "full recompute becomes impossible" framing

<!-- FROZEN ABOVE. Everything above this line is written once and never edited. -->

## Verdicts

- **2026-08-27** · `superseded` · grade `measured`
  - evidence: `lab/004`
  - read-in: `lab/claims-inventory-draft.md`
  - note: **Superseded by lab/004** (governing quantity is `edges × hidden_dim`; at mean degree 99 the ceiling arrives at 233k nodes). lab/001 carries the supersession banner. **The public README does not** — see P4.

- **2026-08-27** · `corroborated` · grade `measured`
  - evidence: `README.md`, compared directly against this statement
  - read-in: direct text comparison, 2026-08-27 quotation audit
  - note: Quotation verified verbatim against the source this entry names, allowing only markdown emphasis and sentence-case. No words added, dropped or reordered, and no unmarked elision.

## References

Where this claim is restated outside the ledger. Appended at write time; the referencing
document never names this entry: a claim's status lives here and nowhere else, and an id
copied into a document goes stale the moment that status changes, silently, because
nothing checks it from that side.
When status tips to `refuted` or `superseded`, every row here is work to do.

- `lab/001-full-recompute-is-a-memory-wall-not-a-time-wall.md` · record · seeded by the 2026-08-27 backfill
- `lab/004-the-admissible-band-is-an-edge-count.md` · record · seeded by the 2026-08-27 backfill

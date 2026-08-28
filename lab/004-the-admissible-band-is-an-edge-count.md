# 004 — The admissible band is an edge count, and it refutes both experts' primary

**Date:** 2026-08-27 · **Component:** dataset selection · **Status:** measured.

## What was asked

The two round-2 consultations were run independently and returned incompatible dataset
rulings. `eval-methodology` (ticket measurement consultation, round 2) ranked tgbl-wiki primary at 9,227
nodes, with tgbl-review as contrast, rejecting Reddit and Amazon2M as saturated.
`dl` (ticket modelling consultation, round 2) put ogbn-products and Reddit in tier A and said the
temporal-GNN benchmarks at ~9-11k nodes sit three orders of magnitude below the cost
floor. Both were reasoning about the same box. It was cheaper to measure it than to
arbitrate.

## Observation

Full-graph two-layer GraphSAGE at 128-dim, synchronized timing, published approximate
degrees:

| dataset | nodes | edges | full recompute |
|---|---|---|---|
| Cora | 2,708 | 10,832 | 0.504 ms |
| CiteSeer | 3,327 | 9,981 | 0.519 ms |
| tgbl-wiki | 9,227 | 92,270 | 1.729 ms |
| Reddit-JODIE | 11,000 | 110,000 | 2.099 ms |
| PubMed | 19,717 | 78,868 | 2.047 ms |
| Reddit (full) | 232,965 | 23,063,535 | OOM |
| ogbn-products | 2,449,029 | 122,451,450 | OOM |

lab/001 concluded the ceiling was "roughly 1-2M nodes". That was measured at mean degree
10 and it names the wrong variable. Full-graph message passing materializes a tensor per
edge, so the ceiling is an edge count. Measured directly, one SAGEConv layer at 128-dim:

| edges | fits | peak GiB |
|---|---|---|
| 5,000,000 | yes | 2.75 |
| 10,000,000 | yes | 5.21 |
| 15,000,000 | yes | 7.67 |
| 20,000,000 | no | — |

Ceiling between 15M and 20M edges, scaling linearly at ~0.51 GiB per million edges at
128-dim. Since it scales with edges x dim, hidden dimension moves it. Reddit at full
scale, two layers:

| hidden dim | fits | peak GiB | full recompute |
|---|---|---|---|
| 128 | no | — | OOM |
| 96 | no | — | OOM |
| 64 | yes | 6.07 | 213.6 ms |
| 32 | yes | 3.25 | 148.5 ms |

## Interpretation

**Both primaries fail, for opposite reasons.** tgbl-wiki costs 1.729 ms to recompute
entirely. A refresh strategy cannot demonstrate a saving against that; anything measured
there is scheduling jitter, and `dl` is right. ogbn-products and Reddit at 128-dim cannot
have their reference point computed at all — the manifest fixes full recomputation as the
reference, and an arm that OOMs is not a reference, so `eval-methodology` is right to
refuse them even though its stated reason (saturation) was a different one.

**The admissible band is arithmetic, not a matter of taste.** A dataset is admissible when
`edges x hidden_dim` sits under roughly 15M x 128, and when full recompute is far enough
above a millisecond that a saving is measurable. That is a band of roughly 5M-15M edges at
128-dim, and it moves predictably with hidden dimension.

**Reddit at 64-dim lands in the band**: 213.6 ms, 6.07 GiB, heavy-tailed at mean degree 99,
which is the degree distribution `dl` wanted and which lab/002's uniform-random synthetic
removes by construction. 213.6 ms is 124x tgbl-wiki's full recompute.

This is a constructive resolution of the disagreement but **not a complete one**.
`eval-methodology`'s saturation objection is about the downstream task, not about cost,
and lowering the hidden dimension does not answer it: if the task scores near ceiling
there is no headroom in which degradation could show. That objection stands and is
unaddressed. Choosing Reddit-at-64 therefore requires either a task on Reddit that is not
saturated, or accepting that the fidelity probes carry the result and the downstream task
is decoration.

## What this corrects

lab/001's "VRAM caps full-graph refresh at roughly 1-2M nodes" is superseded. It was true
at mean degree 10 and false as a general statement: at Reddit's mean degree 99 the ceiling
arrives at 233k nodes. The governing quantity is edges x hidden_dim, and the constant is
~0.51 GiB per million edges per 128 dims. lab/001 is left in place with this note linked
from it, per the rule that negative and superseded findings are kept rather than deleted.

## Open

- The saturation objection is unresolved and is the live question for a round 3 or an
  operator decision.
- Degrees here are published approximate values applied to synthetic random graphs of the
  right size, not the real datasets loaded. The memory arithmetic is structural and will
  hold; the timings will move somewhat with real degree distributions, since a heavy tail
  changes the gather pattern.
- No claim is made about which of these graphs has a usable mutation stream. That is a
  separate axis and both experts treated it separately.

Raw probes: `lab/probe_benchmark_scales.py`, `lab/probe_edge_ceiling.py`.

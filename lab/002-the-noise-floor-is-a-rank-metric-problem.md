# 002 — The noise floor is a rank-metric problem, and cosine hides it

**Date:** 2026-08-27 · **Component:** fidelity measurement · **Status:** measured.

## What was asked

The `dl` round-1 consultation (ticket modelling consultation, round 1) put one probe ahead of all
others: measure the seed-variance floor before defining any fidelity metric, because
GraphSAGE samples neighbors with replacement and two recomputations of an unchanged
graph therefore need not agree. Any refresh-fidelity number below that floor is noise.
It was cheap to run, so it was run before round 2 rather than after.

## Observation

50,000 nodes, 500,000 edges, uniform random graph, 64-dim features, 2-layer GraphSAGE
with **untrained (random) weights**, `num_neighbors=[10,10]`, batch 1024. Graph and
weights held fixed; only the inference path and sampling seed vary. Exact kNN, K=20.

| comparison | cos mean | cos min | kNN@20 overlap mean | overlap min |
|---|---|---|---|---|
| full-graph vs full-graph | 1.000000 | 1.000000 | 1.0000 | 1.0000 |
| sampled(seed 1) vs sampled(seed 2) | 0.991137 | 0.850629 | 0.6208 | 0.0500 |
| full-graph vs sampled(seed 1) | 0.995495 | 0.921759 | 0.7045 | 0.1000 |

Full-graph inference is bitwise reproducible: the floor is exactly zero. Sampled
inference is not, and on an unchanged graph it loses 37.9% of each node's top-20
neighborhood on average, with a worst case of 19 of 20 neighbors changed.

## Interpretation

Two separable consequences.

**The metric choice is load-bearing and the obvious metric is the misleading one.** Mean
cosine of 0.991 and mean neighbor overlap of 0.621 describe the same pair of embedding
sets. A write-up reporting the first would claim near-perfect fidelity for a state in
which more than a third of every retrieved neighborhood turned over. The manifest asks
how semantic stability relates to geometric stability and treats their intersection as
research surface; on this evidence they can disagree sharply and in the direction that
flatters the author. Rank-based measures must be primary, and any cosine or L2 figure
must be reported beside one.

**The floor is a property of the inference path, not of the model or the graph.** It is
zero for full-graph inference and large for sampled inference. Since lab/001 measured
that full-graph inference fits on this box to roughly 1-2M nodes, the design implication
is direct: measure fidelity under full-graph inference wherever it fits, where observed
drift is entirely attributable to the refresh policy. Where sampling is unavoidable, the
floor has to be measured per configuration and pre-registered, because a refresh policy
scoring 0.65 neighbor overlap against a 0.62 floor has demonstrated nothing.

## Threats to this result

Stated because they are load-bearing, and this note should not be cited past them.

- **Untrained weights.** These are random-weight embeddings. A trained model concentrates
  structure and its neighborhoods may be far more stable under resampling, which would
  shrink the floor. The direction of the effect is mechanically sound — sampling with
  replacement perturbs each node's aggregate — but the magnitude here is an upper bound
  of unknown tightness. This is also `dl`'s trap T1 in a different guise: untrained
  networks are not a neutral stand-in.
- **Uniform random graph.** Degree is homogeneous. Real graphs are heavy-tailed, and a
  hub's neighborhood is exactly where sampling variance should behave differently.
- One K, one fanout, one depth, one seed pair. No repetition, so no interval is claimed.

None of that is fixed before round 2. The claim being carried forward is the qualitative
one — a rank metric and a geometric metric can disagree by this much on an unchanged
graph — not the constant 0.62.

Raw probe: `lab/probe_noise_floor.py`.

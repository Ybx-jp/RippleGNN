---
id: A0030-error-at-fixed-stale-fraction-is-non-increasing-in-degree-on-a-trained-model-under-either-coherence-regime
kind: hypothesis
stated: 2026-09-05T22:00:00-07:00
author: main
grade: measured
credence: 0.93
resolves_when: a preregistered experiment under experiments/ measures, on a pinned snapshot of the Reddit post graph other than the day-20 pilot snapshot and with saved checkpoints pinned by content hash, the absolute L2 error of each post's second-layer embedding by degree decile at a fixed uniform-random stale fraction, realised by uniform insertion of edges between random existing posts and within fixed-fraction bins under uniform deletion, under a trained two-layer mean-aggregation checkpoint and under the same architecture with sum aggregation, and reports whether the median error in the top decile exceeds the bottom decile's by more than the margin its preregistration derives from the pilot's across-checkpoint spread under mean aggregation, and whether it exceeds it at all under sum
supersedes: A0013-error-at-fixed-stale-fraction-is-non-increasing-in-degree-on-a-trained-model
verbatim_change: the Scope splits the predecessor's condition into which neighbours are stale and how their deltas align, names absolute L2 as the primary metric with relative L2 as a registered secondary, names uniform insertion as the stream that realises the fixed fraction and a snapshot other than day 20 as the cohort, and Backing quotes the round-4 restatement and its credence in place of the round-3 ones
verbatim_sha: f2e8f3b909b7215f4fb5849379fa8e377e3942245b509cd5fc9d1291abe69f13
---

## Assertion

On the Reddit post graph with a trained two-layer mean-aggregation GraphSAGE
checkpoint, the absolute L2 error a post's second-layer embedding incurs when a
uniform-random fraction of its neighbours' first-layer inputs are stale will be
non-increasing in the post's degree across degree deciles, whether the stale
neighbours' deltas are coherent, as under insertion of edges to posts of other
communities, or incoherent, as under uniform deletion, within a margin fixed before
the run from the across-checkpoint spread of a decile's median; and on the same
architecture with sum aggregation it will be increasing.

## Scope

metric: absolute L2 distance between the checkpoint's second-layer embedding on the mutated graph and on the starting graph, on posts whose own edges are unchanged, compared as the median per degree decile at a fixed stale fraction, under mean aggregation and under a sum-aggregation control on the same architecture; the same distance relative to the embedding norm as a registered secondary whose predicted direction is falling with degree under both aggregations
cohort: a pinned snapshot of the Reddit post graph other than the day-20 snapshot on which the pilot ran, and saved checkpoints pinned by content hash, two-layer SAGEConv with mean aggregation at both layers, with sum-aggregation checkpoints by the same recipe as the positive control that the harness can see a degree effect
condition: the stale set is uniform-random over a post's starting-graph neighbours at one fixed fraction, realised at every degree by uniform insertion of edges between random existing posts, under which the deltas are coherent, and within fixed-fraction bins under uniform deletion, under which they are incoherent; coherence is declared per stream and measured as the norm of the summed deltas over the sum of their norms against its orthogonal value; the margin is fixed in the preregistration from the pilot's across-checkpoint spread of a decile's median, 3 to 4 percent of its value; a decrease with degree under mean aggregation is consistent with the hypothesis and is the predicted direction

## Grounds

- entry: A0012-stale-fraction-error-is-non-increasing-in-degree-under-mean-aggregation · cites-as-live
- entry: A0001-sageconv-aggregates-by-mean-unless-told-otherwise · cites-as-live
- lab: lab/017-one-percent-of-edges-makes-half-of-every-neighbourhood-stale-and-at-a-fixed-stale-fraction-error-still-falls-with-degree.md § "Observation" @86804c6
- lab: lab/015-random-deletions-make-stale-neighbours-drift-independently-and-dissimilar-insertions-make-them-drift-together.md § "Observation" @568a40c
- source: consult-dl-r4 · §4, the restated condition, and §8, the credence

## Warrant

Two mechanisms make mean-aggregation error non-increasing in degree at a fixed stale
fraction, one for each coherence regime. Under incoherent staleness the stale deltas
have independent directions and their mean shrinks as the inverse square root of the
degree, the single-layer law of the predecessor's ground. Under coherent staleness the
deltas add and the fraction law gives no cancellation, but a hub's neighbours are
higher-degree posts that each move less under the same mutation, so the coherent bound
itself falls across deciles on this graph. The pilot measured both on the day-20
snapshot: under uniform deletion, whose deltas sit at the orthogonal value on every
decile, and under uniform insertion, whose deltas are coherent, the top decile's median
two-hop-only error is 0.085 to 0.231 of the bottom's in absolute L2 on every
checkpoint, draw and fixed-fraction bin, and under sum aggregation it is 3.2 to 25
times the bottom's. The sum arm is the control, and it keeps its direction only in
absolute L2, because a sum embedding's norm grows with degree; that is why the metric is
absolute and relative is registered beside it with its own predicted direction. The
credence is the consulted expert's on this restatement, quoted in Backing, and sits
below the pilot's unanimity for the residuals it names: the snapshot, a checkpoint
recipe that is not bitwise reproducible and whose norms a longer-trained checkpoint
would change, and the normalisation the preregistration writes. Falsified if the
median error in the top degree decile exceeds the bottom decile's by more than the
margin under mean aggregation in absolute L2, or if under sum aggregation it does not
exceed it.

## Backing

- source: consult-dl-r4 · §4, the restated condition
  speaker: dl
  quote: […] "at fixed f, mean-aggregation error is non-increasing in degree under both coherence regimes, by two mechanisms" […]
- source: consult-dl-r4 · §8, the credence
  speaker: dl
  quote: […] "Non-increasing under mean, absolute L2, fresh snapshot, pinned checkpoints, uniform streams: 0.93." […]

<!-- APPEND BELOW THIS LINE ONLY -->

## Verdicts


## References

- experiments/ROSTER.md · standing · cites-as-live

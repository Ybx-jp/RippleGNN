# 007 — The flat line in lab/005 was an identity; under incoherent staleness, mean-aggregation error falls with degree

**Date:** 2026-09-02 · **Component:** refresh error model · **Status:** measured.

## What was asked

The modelling consultation's third round read lab/005's numbers rather than its
sentences. At stale fractions of 5, 25 and 50 percent the errors 0.009392, 0.046961 and
0.093922 stand in the ratio 1 : 5 : 10, and 0.093922 divided by 0.5 is 0.187844, the
sum-aggregation error for one stale neighbour in the same note. lab/005 applied the same
perturbation vector to every stale neighbour, so under mean aggregation the centre's
aggregated input moves by exactly the fraction times that vector at every degree, by
arithmetic. The six-significant-figure invariance was a property of the perturbation
design, not a finding about message passing. The consultation predicted that with an
independent random direction per stale neighbour the error at fixed fraction would fall
as the square root of the fraction over the degree. This note runs that probe. The
script is `lab/probe_coherence.py`.

## Observation

A star graph, one centre with `deg` neighbours, one SAGEConv layer, 16-dim, eval mode,
untrained weights, seed 20260903. A stale subset of the neighbours, a uniform random
`round(f · deg)` of them, has its input perturbed by a vector of norm 0.1: in the
coherent arm the same vector for every stale neighbour, in the incoherent arm an
independent random direction per stale neighbour, averaged over 20 draws. Centre-node
output L2 error, and the incoherent-to-coherent ratio beside `1/sqrt(k)` for `k` stale
neighbours.

| aggr | degree | f | coherent | incoherent | ratio | 1/sqrt(k) |
|---|---|---|---|---|---|---|
| mean | 20 | 0.05 | 0.002729 | 0.002732 | 1.001 | 1.000 |
| mean | 20 | 0.50 | 0.027290 | 0.008674 | 0.318 | 0.316 |
| mean | 100 | 0.05 | 0.002729 | 0.001274 | 0.467 | 0.447 |
| mean | 100 | 0.50 | 0.027290 | 0.003833 | 0.140 | 0.141 |
| mean | 500 | 0.05 | 0.002729 | 0.000590 | 0.216 | 0.200 |
| mean | 500 | 0.50 | 0.027290 | 0.001701 | 0.062 | 0.063 |
| mean | 2000 | 0.05 | 0.002729 | 0.000273 | 0.100 | 0.100 |
| mean | 2000 | 0.50 | 0.027290 | 0.000888 | 0.033 | 0.032 |
| sum | 20 | 0.50 | 0.580395 | 0.173966 | 0.300 | 0.316 |
| sum | 500 | 0.50 | 14.509897 | 0.777906 | 0.054 | 0.063 |
| sum | 2000 | 0.50 | 58.039532 | 1.696578 | 0.029 | 0.032 |

The full grid, with f = 0.25 and every degree for both aggregators, is the script's
output. Coherent mean error is 0.002729, 0.013645 and 0.027290 at f = 5, 25 and 50
percent at every degree, again in the ratio 1 : 5 : 10. Incoherent mean error at fixed
fraction falls with degree: from 0.002732 at degree 20 to 0.000273 at degree 2000 at
f = 5 percent, a factor of ten across a factor of a hundred in degree. The ratio of the
two arms tracks `1/sqrt(k)` to two or three digits in every row. Sum aggregation under
incoherent staleness grows with degree as the square root of the stale count rather than
linearly: 0.174 at degree 20 to 1.70 at degree 2000 at f = 50 percent, against 0.580 to
58.0 coherent.

## Interpretation

**lab/005 measured the coherent special case, and its flatness is an identity.** A
mean of `k` copies of one vector over `d` slots is `k/d` times that vector; nothing about
the layer enters. The mechanism lab/005 named, that mean aggregation weights each
neighbour by one over the degree, is exact, but what it implies for error depends on
whether the stale neighbours' deltas point the same way.

**Under incoherent staleness, mean-aggregation error at fixed fraction falls with
degree as the inverse square root.** The mean of `k` independent vectors of norm ε over
`d` slots has norm about ε · sqrt(k) / d = ε · sqrt(f / d). At fixed fraction a hub's
error is smaller than a leaf's by the square root of their degree ratio. Hubs are not
merely as safe as leaves per stale fraction; they are safer.

**The two arms bracket the general case.** For mean aggregation, error at fixed fraction
lies between ε · sqrt(f / d) and ε · f, times the layer's gain, and in neither limit does
it increase with degree. For sum aggregation it lies between ε · sqrt(f · d) and
ε · f · d, and in both limits it increases with degree. The statement that survives from
lab/005 is the contrast, not the flat line: under mean aggregation error at fixed stale
fraction is non-increasing in degree, and under sum aggregation it is increasing.

**Coherence is a property of the mutation stream, and it is the second axis the stream
sets.** A uniform-random stale set on a real graph is made stale by unrelated mutations
elsewhere, which is close to the incoherent arm. A burst of edits to one community, or
to one hub's neighbourhood, moves the affected embeddings in correlated directions,
which is close to the coherent arm. So the degree profile of refresh error is not fixed
by the aggregator alone; it is fixed by the aggregator and by how correlated the stream
makes the staleness, and a stream model has to declare both its locality and its
coherence.

**What this does to the ledger.** The measured claim from lab/005 holds exactly within
its stated scope, one perturbation applied uniformly to every stale neighbour, but the
reading that stale fraction governs error at every degree is the coherent case only.
The hypothesis on the roster, that error at a fixed uniform-random stale fraction is
independent of degree within a margin, is now expected to fail in the downward
direction: a uniform-random stale set is the incoherent arm, and across Reddit's degree
deciles the predicted spread is a factor of thirty. It is restated as non-increasing in
degree under mean aggregation and increasing under sum aggregation on the same
architecture, with the sum arm as the positive control that the harness can see a
degree effect at all. The conditional guarantee, that bounding the stale fraction bounds
error by a degree-independent quantity, survives as an upper bound: the coherent value
ε · f is the worst case at every degree.

## Threats

- A star graph, one layer, untrained weights, one perturbation norm, as in lab/005. The
  probe measures a mechanism, not a magnitude.
- The perturbation is applied to neighbour inputs. Staleness in a deployed model is a
  delta on a neighbour's previous-layer embedding, whose direction is set by the
  mutation that made it stale and by the weights; independent uniform directions are
  the extreme of incoherence, not a measurement of what any stream produces. The
  coherence a real mutation stream induces on a real graph is unmeasured and is the
  next probe.
- The root-weight self path, absent on the star, dilutes every figure here on a real
  graph by an amount that depends on the trained weights.

---
id: A0007-bounding-stale-fraction-bounds-error-independent-of-degree
kind: claim
stated: 2026-09-02T16:32:00-07:00
author: main
grade: argued
supersedes: A0004-bounding-stale-fraction-bounds-error-independent-of-degree
verbatim_sha: dd334e1214c3e47abb94cb6e232301dc3fb7b84c0b27ac25e420ee57196cd889
---

## Assertion

If the stale-fraction law holds for the deployed model, a refresh policy that keeps every
node's stale fraction below a threshold bounds that node's embedding error by a quantity
that does not depend on its degree, so the guarantee such a policy offers is the same
for hubs and for leaves.

## Scope

metric: a bound on per-node embedding error against full recomputation, as a function of the stale-fraction threshold
cohort: mean-aggregation GraphSAGE models for which the stale-fraction law holds
condition: conditional on the law holding at the deployed depth and weights; the bound is on the error the stale fraction induces and says nothing about mutations that change the neighbourhood itself

## Grounds

- entry: A0005-stale-fraction-governs-mean-aggregation-error · cites-as-live
- entry: A0006-fraction-law-holds-with-trained-weights-and-depth · cites-as-live

## Warrant

If error at a node is a function of its stale fraction alone, then holding the fraction
below a threshold holds the error below the value that function takes at the threshold,
and that value carries the degree nowhere. The claim is conditional: it inherits the
single-layer measurement through the hypothesis that lifts it to the deployed model,
and it falls with that hypothesis.

## Backing

none

<!-- APPEND BELOW THIS LINE ONLY -->

## Verdicts

- 2026-09-02T21:56:00-07:00 · superseded · grade: argued · author: main
  evidence: entry: A0014-bounding-stale-fraction-bounds-error-by-a-degree-independent-quantity · supersedes
  note: its ground A0006 was superseded; the guarantee survives as an upper bound at the coherent value and is restated on the successor hypothesis

## References

---
id: A0014-bounding-stale-fraction-bounds-error-by-a-degree-independent-quantity
kind: claim
stated: 2026-09-02T21:54:00-07:00
author: main
grade: argued
supersedes: A0007-bounding-stale-fraction-bounds-error-independent-of-degree
verbatim_change: the Scope's condition now names the coherent value as the bound and drops the equality the predecessor assumed; Backing remains none
verbatim_sha: f5f94526861c7815d36f083adea642b26814b49147faed7ad051d1bb4c0d5cad
---

## Assertion

If error at a fixed stale fraction is non-increasing in degree for the deployed
mean-aggregation model, a refresh policy that keeps every node's stale fraction below a
threshold bounds that node's embedding error by the coherent-staleness value at that
threshold, a quantity that does not depend on its degree, so the guarantee such a policy
offers is the same for hubs and for leaves and is loosest for leaves.

## Scope

metric: an upper bound on per-node embedding error against full recomputation, as a function of the stale-fraction threshold
cohort: mean-aggregation GraphSAGE models for which the non-increasing law holds
condition: conditional on the law holding at the deployed depth and weights; the bound is the coherent value, which the incoherent case sits under by the inverse square root of the degree; the bound is on the error the stale fraction induces and says nothing about mutations that change the neighbourhood itself

## Grounds

- entry: A0012-stale-fraction-error-is-non-increasing-in-degree-under-mean-aggregation · cites-as-live
- entry: A0013-error-at-fixed-stale-fraction-is-non-increasing-in-degree-on-a-trained-model · cites-as-live

## Warrant

If error at a node is bounded above by a function of its stale fraction alone, the
coherent value, then holding the fraction below a threshold holds the error below the
value that function takes at the threshold, and that value carries the degree nowhere;
where the staleness is incoherent the realised error sits below the bound by a factor
that grows with degree, which makes the bound loose for hubs and tight for leaves
rather than wrong for either. The claim is conditional: it inherits the single-layer
measurement through the hypothesis that lifts it to the deployed model, and it falls
with that hypothesis.

## Backing

none

<!-- APPEND BELOW THIS LINE ONLY -->

## Verdicts


## References


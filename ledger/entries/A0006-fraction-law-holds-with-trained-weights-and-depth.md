---
id: A0006-fraction-law-holds-with-trained-weights-and-depth
kind: hypothesis
stated: 2026-09-02T16:32:00-07:00
author: main
grade: argued
credence: 0.65
resolves_when: a preregistered experiment under experiments/ measures centre-node embedding error by degree decile at a fixed uniform-random stale fraction on a pinned real graph with a trained two-layer mean-aggregation checkpoint, and reports whether the spread across deciles stays within the margin its preregistration derives
supersedes: A0003-fraction-law-holds-with-trained-weights-and-depth
verbatim_sha: df453debb2cbca9812fff8e38687e54633614c7a93b25faf0b1b805a0fc7e6a8
---

## Assertion

On a real graph with a trained two-layer mean-aggregation GraphSAGE checkpoint, the
embedding error caused by a uniform-random stale fraction of a node's neighbourhood will
be independent of the node's degree, within a margin derived before the run from the
seed-variance floor.

## Scope

metric: node embedding L2 error against full recomputation at a fixed stale fraction, compared across degree deciles
cohort: a pinned real graph and a trained two-layer SAGEConv checkpoint, mean aggregation at both layers
condition: the stale set a uniform random subset of each node's neighbourhood at one fixed fraction; the margin fixed in the preregistration from the measured seed-variance floor

## Grounds

- entry: A0005-stale-fraction-governs-mean-aggregation-error · cites-as-live
- entry: A0001-sageconv-aggregates-by-mean-unless-told-otherwise · cites-as-live

## Warrant

The single-layer law rests on a mechanism that is exact for mean aggregation at any one
layer, and the project's model aggregates by mean at every layer, so composing a second
layer multiplies the error by a Lipschitz factor that is the same for every node and
reintroduces a degree dependence nowhere. The credence is below the mechanism's own
certainty because the two threats the lab note names are exactly what this
hypothesis lifts: compounding across layers, and trained weights whose Lipschitz
constants the single-layer probe never exercised. Falsified if the spread of error
across degree deciles exceeds the preregistered margin at the fixed stale fraction, in
which case either depth or training reintroduces a degree dependence and the
single-layer law does not scope up.

## Backing

none

<!-- APPEND BELOW THIS LINE ONLY -->

## Verdicts


## References

- experiments/ROSTER.md · standing · cites-as-live

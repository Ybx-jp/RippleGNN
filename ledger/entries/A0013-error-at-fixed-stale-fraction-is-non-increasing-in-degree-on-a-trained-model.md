---
id: A0013-error-at-fixed-stale-fraction-is-non-increasing-in-degree-on-a-trained-model
kind: hypothesis
stated: 2026-09-02T21:52:00-07:00
author: main
grade: argued
credence: 0.75
resolves_when: a preregistered experiment under experiments/ measures node embedding error by degree decile at a fixed uniform-random stale fraction on a pinned real graph with a trained two-layer mean-aggregation checkpoint and, on the same architecture with sum aggregation, and reports whether the median error in the top decile exceeds that of the bottom decile by more than the margin its preregistration derives under mean aggregation, and whether it exceeds it at all under sum
supersedes: A0006-fraction-law-holds-with-trained-weights-and-depth
verbatim_change: the Scope adds the sum-aggregation control and the direction of the comparison, and Backing now quotes the consultation whose restatement this is; the predecessor had none
verbatim_sha: ea4cb71da6fe0cac3f5bf2394c82bad4394bf5367e2e2045e4141f8f5044e3ce
---

## Assertion

On a real graph with a trained two-layer mean-aggregation GraphSAGE checkpoint, the
embedding error caused by a uniform-random stale fraction of a node's neighbourhood will
be non-increasing in the node's degree across degree deciles, within a margin derived
before the run from the seed-variance floor, and on the same architecture with sum
aggregation it will be increasing.

## Scope

metric: node embedding L2 error against full recomputation at a fixed stale fraction, compared as the median per degree decile, under mean aggregation and under a sum-aggregation control on the same architecture
cohort: a pinned real graph and a trained two-layer SAGEConv checkpoint, mean aggregation at both layers, with the sum-aggregation arm as the positive control that the harness can see a degree effect
condition: the stale set a uniform random subset of each node's neighbourhood at one fixed fraction, so the staleness is close to the incoherent arm of the single-layer probe; the margin fixed in the preregistration from the measured seed-variance floor; a decrease with degree under mean aggregation is consistent with the hypothesis and is the predicted direction

## Grounds

- entry: A0012-stale-fraction-error-is-non-increasing-in-degree-under-mean-aggregation · cites-as-live
- entry: A0001-sageconv-aggregates-by-mean-unless-told-otherwise · cites-as-live
- source: consult-dl-r3 · §5, the restatement and the credence it carries

## Warrant

The single-layer measurement gives two limits for mean aggregation, flat under coherent
staleness and falling with degree under incoherent, and a uniform-random stale set on a
real graph is made stale by unrelated mutations and so sits near the incoherent limit;
neither limit increases with degree, and the project's model aggregates by mean at
every layer, so composing a second layer multiplies the error by a factor that is the
same for every node and reintroduces a degree dependence nowhere. The sum arm is the
control: on the same architecture the single-layer rows rise with degree in both
limits, so a flat or falling mean result beside a rising sum result is a measurement
and not an insensitivity. The credence is the consulted expert's on this restatement,
quoted in Backing, and sits below the mechanism's own certainty for the threats the
predecessor named: compounding across layers, trained weights whose Lipschitz constants
the single-layer probe never exercised, and the root-weight self path, whose relative
norm on a trained checkpoint is unknown and could flatten everything for the
uninteresting reason that neighbour staleness barely enters. Falsified if the median
error in the top degree decile exceeds the bottom decile's by more than the margin
under mean aggregation, or if under sum aggregation it does not exceed it.

## Backing

- source: consult-dl-r3 · §5, the restated hypothesis
  speaker: dl
  quote: […] "error at fixed uniform-random stale fraction is non-increasing in degree across deciles under mean aggregation and increasing under sum aggregation, with the mean/sum ratio in the top decile below 0.05."
- source: consult-dl-r3 · §5, the credence on the predecessor's statement
  speaker: dl
  quote: […] "My credence: 0.35, and the number depends on the margin in a way the statement does not fix."

<!-- APPEND BELOW THIS LINE ONLY -->

## Verdicts


## References

- experiments/ROSTER.md · standing · cites-as-live

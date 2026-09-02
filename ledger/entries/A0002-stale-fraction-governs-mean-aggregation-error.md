---
id: A0002-stale-fraction-governs-mean-aggregation-error
kind: claim
stated: 2026-09-02T16:21:00-07:00
author: main
grade: measured
supersedes: none
verbatim_sha: 28e34503ff0505fd426438d48af5600309842b2bf8da49d4c9e54188e6466557
---

## Assertion

Under mean aggregation, the output error a node incurs from stale neighbour inputs is
governed by the fraction of its neighbourhood that is stale rather than by the count of
stale neighbours, and at a fixed stale fraction the error is the same at every degree.

## Scope

metric: centre-node output L2 error under a fixed perturbation of 0.1 applied to the inputs of the stale neighbours
cohort: star graphs with one centre and 5 to 2000 neighbours, one SAGEConv layer, 16-dim, eval mode, untrained weights
condition: a single layer, so compounding across depth is not measured; one perturbation magnitude, applied uniformly to every stale neighbour; the stale set a uniform random subset at fractions of 5, 25 and 50 percent; sum aggregation measured alongside for contrast

## Grounds

- lab: lab/005-mean-aggregation-makes-it-a-fraction-not-a-count.md § "Observation" @bab6d58

## Warrant

Mean aggregation weights each neighbour's message by one over the degree, so a fixed
perturbation on a fraction f of the neighbours contributes f times the per-neighbour
effect at every degree, while a single stale neighbour contributes less as the degree
grows. The sweep matches this at every degree to six significant figures, so the
direction is structural; the magnitudes belong to the probe's untrained weights and are
not load-bearing. The degree factor in the depth bound the project had been reading
comes from sum aggregation, which the remark quoted in Backing states and the
sum-aggregation column of the same sweep, growing linearly with degree, confirms.

## Backing

- source: gnnautoscale-2021 · §3, the remark after Theorem 1 that introduces Theorem 2
  speaker: Fey, Lenssen, Weichert and Leskovec
  quote: "Interestingly, sum aggregation, the most expressive aggregation function (Xu et al., 2019), introduces a factor of |N (v)| to the upper bound, while we can obtain a much tighter upper bound for mean or max aggregation, cf. its proof."

<!-- APPEND BELOW THIS LINE ONLY -->

## Verdicts


## References

- experiments/ROSTER.md · standing · cites-as-live

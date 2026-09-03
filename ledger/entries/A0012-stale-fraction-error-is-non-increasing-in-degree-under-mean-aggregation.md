---
id: A0012-stale-fraction-error-is-non-increasing-in-degree-under-mean-aggregation
kind: claim
stated: 2026-09-02T21:50:00-07:00
author: main
grade: measured
supersedes: A0005-stale-fraction-governs-mean-aggregation-error
verbatim_change: the Scope now carries the coherence condition lab/007 adds, the coherent and incoherent arms and the seed; the Backing block is unchanged
verbatim_sha: b611fe2bd7620e8f1af6002b80c7823fb619204860c043f8e83696221be7b6cc
---

## Assertion

Under mean aggregation, the output error a node incurs from stale neighbour inputs at a
fixed stale fraction is the same at every degree when the stale neighbours'
perturbations share a direction, and falls with degree as the inverse square root when
their directions are independent; under sum aggregation it rises with degree in both
cases. At a fixed stale fraction, mean-aggregation error is therefore non-increasing in
degree and sum-aggregation error is increasing.

## Scope

metric: centre-node output L2 error under a perturbation of norm 0.1 applied to the inputs of the stale neighbours, in a coherent arm where every stale neighbour receives the same vector and an incoherent arm where each receives an independent random direction, the latter averaged over 20 draws
cohort: star graphs with one centre and 20 to 2000 neighbours, one SAGEConv layer, 16-dim, eval mode, untrained weights, seed 20260903 in lab/007 and the lab/005 sweep before it; mean and sum aggregation measured side by side
condition: a single layer, so compounding across depth is not measured; one perturbation norm; the stale set a uniform random subset at fractions of 5, 25 and 50 percent; independent uniform directions are the extreme of incoherence, and the coherence a real mutation stream induces on a real graph is not measured

## Grounds

- lab: lab/005-mean-aggregation-makes-it-a-fraction-not-a-count.md § "Observation" @bab6d58
- lab: lab/007-the-flat-line-was-an-identity-incoherent-staleness-falls-with-degree.md § "Observation" @6720079

## Warrant

Mean aggregation weights each neighbour's message by one over the degree. A
perturbation shared by a fraction f of the neighbours moves the aggregate by f times
that vector at every degree, which the flat rows of lab/005 show and which is an
identity of the design rather than a property of the layer; independent perturbations
of norm ε on a fraction f of d neighbours move it by about ε times the square root of
f over d, which the incoherent rows of lab/007 track in the ratio one over the square
root of the stale count to two or three digits at every degree and fraction. Neither
limit increases with degree, and sum aggregation over the same rows grows as f times d
coherent and as the square root of f times d incoherent, so the contrast between the
aggregators is what the two notes establish. The remark quoted in Backing states the
same mechanism from the side of the error bound.

## Backing

- source: gnnautoscale-2021 · §3, the remark after Lemma 1 that introduces Theorem 2
  speaker: Fey, Lenssen, Weichert and Leskovec
  quote: "Interestingly, sum aggregation, the most expressive aggregation function (Xu et al., 2019), introduces a factor of |N (v)| to the upper bound, while we can obtain a much tighter upper bound for mean or max aggregation, cf. its proof."

<!-- APPEND BELOW THIS LINE ONLY -->

## Verdicts


## References

- experiments/ROSTER.md · standing · cites-as-live

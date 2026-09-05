---
id: A0028-the-reddit-checkpoints-root-matrices-carry-0-41-to-0-48-of-the-operator-norm-at-both-layers-and-the-second-layer-realises-0-75-to-1-07-of-a-1-85-spectral-norm
kind: claim
stated: 2026-09-05T13:22:00-07:00
author: main
grade: measured
supersedes: none
verbatim_sha: 36d8d0fd98157bf126ae0608ea831e542bba8af8aed30fd9475c0a5dcc5c569f
---

## Assertion

On the five Reddit-at-64 checkpoints the spectral norm of each layer's root matrix is
0.41 to 0.48 of the sum of the root and neighbour matrices' spectral norms at both
layers, so the self path carries about as much operator norm as the neighbour path and
does not swallow it; the neighbour matrices' spectral norms are 5.57 to 6.37 at layer
one and 1.77 to 1.94 at layer two, the head's 1.69 to 1.88; and the second
layer amplifies a real aggregated-input move on posts whose own input is unchanged by
0.75 to 1.07 across thirteen mutation arms and ten degree deciles, 0.41 to 0.58 of its
mean spectral norm of 1.85.

## Scope

metric: the largest singular value of SAGEConv's lin_l and lin_r weight matrices at each layer and of the head, per checkpoint; the root share lin_r over the sum of the two per layer; the realised gain as the norm of the second layer's output move over the norm of its aggregated-input move on posts touched at two hops only, mean over checkpoints per arm and degree decile
cohort: the five checkpoints of A0024 and A0027 (two-layer SAGEConv with mean aggregation, 602 to 64 to 64, linear head to 41 classes, Adam at 0.01 for 100 epochs, seeds 20260903 to 20260907, trained on the Reddit post graph before day 20); norms per seed: layer 1 neighbour 5.572, 6.118, 6.373, 6.332, 6.144 and root 5.071, 4.410, 4.484, 4.849, 4.956; layer 2 neighbour 1.839, 1.886, 1.944, 1.809, 1.772 and root 1.656, 1.562, 1.550, 1.533, 1.537; head 1.698, 1.875, 1.795, 1.771, 1.687; realised gain 1.02 to 1.07 under uniform deletion, 0.92 to 1.06 under uniform insertion and the hub arms, 0.95 to 1.05 under one day of growth, 0.75 to 1.05 under three and ten days
condition: the root share is a ratio of operator norms and not the share of a post's output contributed by its own input, which depends on the inputs on the two paths and is not measured; the realised gain is on the one stratum where the second layer's output move is exactly its neighbour matrix applied to the input move, and never exceeded the spectral norm in any cell; the first layer's realised gain is not measured; the checkpoints are the 100-epoch recipe, not a converged one

## Grounds

- lab: lab/016-the-root-path-carries-half-the-norm-and-the-second-layer-realises-half-its-spectral-norm.md § "Observation" @568a40c
- entry: A0027-on-the-reddit-graph-random-deletions-make-stale-neighbour-deltas-incoherent-dissimilar-insertions-make-them-coherent-and-the-real-stream-sits-between · cites-as-live

## Warrant

The table of lab/016 is the measurement, five checkpoints read once each with the
largest singular value computed by a dense SVD of matrices no larger than 64 by 602.
The realised gain is read from A0027's run on the stratum whose algebra makes the
output move exactly the neighbour matrix times the input move, so the ratio is bounded
by that matrix's singular values by construction and the reading is where a real move
falls in that range; it is cited as live because the deltas and the stratum are that
entry's. The root share prices the threat A0013's Warrant names as unpriced, the
relative norm of the self path, and does not resolve that hypothesis, which resolves
by preregistered experiment.

## Backing

none

<!-- APPEND BELOW THIS LINE ONLY -->

## Verdicts


## References

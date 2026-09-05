---
id: A0027-on-the-reddit-graph-random-deletions-make-stale-neighbour-deltas-incoherent-dissimilar-insertions-make-them-coherent-and-the-real-stream-sits-between
kind: claim
stated: 2026-09-05T13:20:00-07:00
author: main
grade: measured
supersedes: none
verbatim_sha: 577dbddae0506b027680175beef08840d286eab809842cc994ca49bd390e16dc
---

## Assertion

On the Reddit post graph with a trained two-layer mean-aggregation GraphSAGE, the
first-layer deltas of a post's stale neighbours are incoherent under uniform random
edge deletion, with the mean pairwise cosine at chance and the norm of their sum equal
to the orthogonal value on every degree decile, so that the second layer's
aggregated-input move equals the incoherent prediction of the single-layer probe; they
are coherent under insertion of edges to posts of another subreddit, with the sum of
the deltas at 0.53 to 0.81 of the sum of their norms across deciles and 0.47 to 0.54 on
the hubs against orthogonal values of 0.11 and 0.07, so that a hub's aggregated input
moves five to eight times what independent deltas would give; and under the real
arrival stream they sit between, at the orthogonal value on the bottom decile and 2.6
times it on the top, a quarter of the coherent bound.

## Scope

metric: per existing post with two or more stale starting-graph neighbours, the mean pairwise cosine between those neighbours' first-layer post-ReLU hidden-vector deltas between the starting and the mutated graph, the norm of the deltas' sum over the sum of their norms (R), and the orthogonal value of R (the root of the sum of squared norms over the sum of norms); unweighted cell means over posts, averaged over five checkpoints; on posts touched at two hops only, the norm of the second layer's aggregated-input move against the sum of the neighbours' delta norms over degree and the root of the sum of squares over degree; the chance band is the same quantities after permuting the deltas among the stale posts within each checkpoint
cohort: the paper's 11,606,919-edge Reddit graph restricted to posts before day 20 (153,430 posts, 5,376,616 edges) as the starting graph; checkpoints as in A0024 (two-layer SAGEConv with mean aggregation, 602 to 64 to 64, Adam at 0.01 for 100 epochs, seeds 20260903 to 20260907); A0024's thirteen arms from the same single draw (seed 20260904): uniform deletion at 1, 5 and 20 percent (cosine 0.005, 0.002, 0.001 against shuffled 0.003, 0.002, 0.001; R 0.268, 0.211, 0.199 against orthogonal 0.272, 0.214, 0.202), uniform insertion at 5 percent (cosine 0.283 against 0.064; R 0.620 against 0.247), hub-burst at 0.1, 0.5 and 1.0 (cosine 0.285, 0.372, 0.460 against 0.066, 0.099, 0.128; R on the hubs 0.468, 0.517, 0.541 against 0.086, 0.069, 0.065), hub-shift at 0.25, 0.5 and 1.0 (cosine 0.195, 0.232, 0.296 against 0.025, 0.034, 0.049; R on the hubs 0.365, 0.411, 0.453 against 0.072, 0.070, 0.071), the real stream for 1, 3 and 10 days (cosine 0.060, 0.065, 0.081 against 0.003, 0.002, 0.003; R on the top decile 0.227, 0.217, 0.233 against 0.087, 0.081, 0.078); RTX 3060, 607 s, 2.34 GiB
condition: the delta is the change in the post-ReLU first-layer hidden vector, the quantity the second layer aggregates; a post is stale when it is an endpoint of a changed edge, and every such post had a non-zero delta; deterministic full-graph inference on the sparse path with delta norms on untouched posts at most 1.1 × 10⁻⁵; the mutations are single draws and the shuffle one permutation per checkpoint; posts with fewer than two stale neighbours are excluded from the cells; the real stream is not split by whether the arriving edge stays within a subreddit; mean aggregation only; the known positive read cosine 1.0000 and R 1.0000, the known negative cosine 0.0000 and R 0.2702 against an orthogonal 0.2712

## Grounds

- lab: lab/015-random-deletions-make-stale-neighbours-drift-independently-and-dissimilar-insertions-make-them-drift-together.md § "Observation" @568a40c
- entry: A0012-stale-fraction-error-is-non-increasing-in-degree-under-mean-aggregation · cites-as-live
- entry: A0024-under-mutations-of-existing-reddit-posts-the-seed-band-rises-with-the-head-disagreement-gap-and-hubs-clear-it-only-under-full-community-replacement · cites-as-live

## Warrant

The four tables of lab/015 are the measurement, read off the same checkpoints and the
same mutation draws as A0024. Coherence is read as the pair of the mean pairwise cosine
against its shuffled value and R against its orthogonal value, and the bracket
assignment follows A0012: R equal to the orthogonal value is the incoherent arm of the
single-layer probe, R at 1 the coherent arm. On posts touched at two hops only the
aggregated-input move is exactly the mean of the neighbours' deltas, so the coherent
bound and the incoherent prediction are computed from the same deltas and the measured
move is placed between them without a model; under deletion it equals the incoherent
prediction within 1 percent in every cell. The known positive and known negative fix
the instrument's two ends before the real deltas are read. The shuffle is the chance
band because it keeps every delta and destroys only which neighbourhood it sits in.

## Backing

none

<!-- APPEND BELOW THIS LINE ONLY -->

## Verdicts


## References

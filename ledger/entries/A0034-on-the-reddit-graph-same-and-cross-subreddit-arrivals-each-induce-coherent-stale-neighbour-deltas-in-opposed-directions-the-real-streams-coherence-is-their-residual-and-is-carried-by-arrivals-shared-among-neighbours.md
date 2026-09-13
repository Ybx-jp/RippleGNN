---
id: A0034-on-the-reddit-graph-same-and-cross-subreddit-arrivals-each-induce-coherent-stale-neighbour-deltas-in-opposed-directions-the-real-streams-coherence-is-their-residual-and-is-carried-by-arrivals-shared-among-neighbours
kind: claim
stated: 2026-09-13T15:42:28-07:00
author: main
grade: measured
supersedes: none
verbatim_sha: 3b72f264f601cee7c0d74e8cc3862b155025e452a188487612cf6159edc7cce0
---

## Assertion

On the Reddit post graph with a trained two-layer mean-aggregation GraphSAGE, the
first-layer deltas that the real growth stream induces on a post's stale neighbours
are coherent under either half of the stream taken alone, more so than under the
whole: over ten days from day 20 the mean pairwise cosine among stale neighbours'
deltas is 0.081 under all arrivals, 0.113 under same-subreddit arrivals only and
0.291 under cross-subreddit arrivals only, against shuffled values of 0.003, 0.003
and 0.031, and the sum of the deltas over the orthogonal value on the top degree
decile is 3.0, 3.7 and 4.8; inside a post the same-only and foreign-only deltas are
each of the order of the full delta, 0.96 and 0.69 of its norm at the median, and
point apart, at a median cosine of minus 0.12 between them over all posts with both
kinds of arrival and minus 0.41 on the top decile, where the net same push and the
net foreign push at the pre-activation of layer one are negatively aligned on 82
percent of posts; and the coherence the whole stream has is carried by arrivals
shared among neighbours rather than by their subreddit, since a random quarter of
each existing post's arrivals drawn independently per post reads 0.036 and 1.75 while
a random quarter of each new post's edges, which keeps the posts a new post touches
sharing it, reads 0.104 and 3.49, at or above the whole stream's 0.081 and 3.0.

## Scope

metric: per existing post with two or more stale starting-graph neighbours, the mean pairwise cosine between those neighbours' first-layer post-ReLU hidden-vector deltas between the starting graph and a variant graph, the norm of the deltas' sum over the sum of their norms (R) and its orthogonal value (R_inc), unweighted cell means over posts averaged over five checkpoints, with the chance band from permuting the deltas among the stale posts within each checkpoint; per existing post that received both kinds of arrival, on the first checkpoint, the norm of the same-only and of the foreign-only delta over the full delta's norm and the cosines among the three, as medians by decile; per existing post, the norm of the sum over the sum of norms of the first-layer pre-activation pushes of its arrivals of a kind, a push being the neighbour weight matrix applied to the arriving post's features minus the mean feature of the post's starting-graph neighbours, against the orthogonal value, and the cosine between the net same push and the net foreign push as the median and the share below zero, mean over checkpoints
cohort: the paper's 11,606,919-edge Reddit graph restricted to posts before day 20 (153,430 posts, 5,376,616 edges) as the starting graph and its degree deciles; checkpoints as in A0027 (two-layer SAGEConv with mean aggregation, 602 to 64 to 64, Adam at 0.01 for 100 epochs, seeds 20260903 to 20260907); the real stream for one and ten days from day 20 (8,625 and 78,491 new posts; 510,805 and 4,535,051 new-to-old edges of which 117,127 and 1,075,731 cross subreddits; 35,547 and 1,623,964 new-to-new) in five variants, all arrivals, same-subreddit new-to-old only, cross-subreddit new-to-old only, a uniform random subset of each existing post's arrivals at its foreign count (seed 20260913) and a uniform random subset of each new post's edges at its foreign count (seed 20260914), every variant keeping the new posts and the new-to-new edges; ten days, all posts with two or more stale neighbours, cosine 0.081, 0.113, 0.291, 0.036, 0.104 against shuffled 0.003, 0.003, 0.031, 0.002, 0.012 and R 0.357, 0.387, 0.575, 0.330, 0.398 against R_inc 0.203, 0.200, 0.245, 0.255, 0.224; top decile R over R_inc 2.97, 3.71, 4.84, 1.75, 3.49 and bottom decile 1.07, 1.10, 1.16, 1.02, 1.07; one day cosine 0.060, 0.084, 0.184, 0.046, 0.062 and top decile R over R_inc 2.59, 2.93, 2.58, 1.54, 2.05; the split deltas over 85,064 posts with both kinds at ten days, medians 0.96 and 0.69 of the full delta's norm with cosine minus 0.12 between them, minus 0.41 on the top decile and plus 0.25 on the bottom, residual of the full delta minus the two 0.16, and over 30,159 posts at one day 0.82, 0.69, minus 0.11 and 0.03; net same against net foreign push at ten days, median cosine plus 0.24 on the bottom decile falling to minus 0.39 on the top with the share below zero from 0.27 to 0.82, minus 0.11 and 0.60 overall; within-post R over R_inc among foreign arrivals 1.30 at a mean count of 15.1 and among same arrivals 1.22 at 26.7, the per-post subset 1.07 and the per-new-post subset 1.08, with mean push norms per arrival 34.4 foreign and 30.8 same; RTX 3060, 450 s, 2.34 GiB
condition: the delta is the change in the post-ReLU first-layer hidden vector, the quantity the second layer aggregates, and the split deltas are on counterfactual graphs whose new degree is smaller than the full one, so each is larger than its share of the full delta and the three do not add, the residual being 0.16 at ten days and 0.03 at one; a post is stale when it received an included arrival, and every such post had a non-zero delta while the largest delta norm on a post with no included arrival was 1.1 × 10⁻⁵; deterministic full-graph inference on the sparse path; the all variant reproduces A0027's growth rows to the third digit; the push decomposition reproduces the measured pre-activation delta with a median relative error of 3 × 10⁻⁶ and a maximum of 3 × 10⁻⁴; the known positive read cosine 1.0000 and R 1.0000 and the known negative cosine 0.0001 and R 0.2286 against an orthogonal 0.2292; the two controls are one draw each, the per-post control breaking the sharing of a new post among the existing posts it attaches to and the per-new-post control keeping it, and the two touch 90,670 and 120,054 existing posts; the split-delta table is one checkpoint; R over R_inc grows with the count at fixed pairwise alignment and is read against the control at the same count; posts with fewer than two stale neighbours are excluded from the neighbour cells; mean aggregation, the paper edge set and the day-20 snapshot only; the hub constructions of A0024 and A0027 and the second layer's output are not measured here

## Grounds

- lab: lab/021-same-and-cross-subreddit-arrivals-each-move-stale-neighbours-together-in-opposed-directions-and-the-real-streams-coherence-is-their-residual.md § "Observation" @3af3b19
- entry: A0027-on-the-reddit-graph-random-deletions-make-stale-neighbour-deltas-incoherent-dissimilar-insertions-make-them-coherent-and-the-real-stream-sits-between · cites-as-live
- entry: A0033-a-quarter-of-the-edges-the-reddit-growth-stream-brings-to-existing-posts-cross-subreddits-a-hubs-arrivals-are-a-third-foreign-and-spread-over-many-and-each-neighbourhoods-foreign-share-is-preserved · cites-as-live
- entry: A0032-the-reddit-post-graph-densifies-with-exponent-1-8-a-new-post-brings-edges-in-proportion-to-the-graph-and-degree-assortativity-holds-at-0-10 · cites-as-live

## Warrant

The four tables of lab/021 are the measurement, made by the coherence entry's method
on the same checkpoints and the same starting graph, with the whole-stream variant
reproducing that entry's growth rows to the third digit before the split variants are
read. Coherence is read as the pair of the mean pairwise cosine against its shuffled
value and R against its orthogonal value, and the ordering of the variants is read off
those pairs in the same cells. The two controls hold the edge count at the foreign
variant's and differ in one thing, whether the existing posts a new post attaches to
still share it, so the difference between them is what sharing contributes and the
difference between the per-new-post control and the foreign variant is what
foreignness contributes at the same count and the same sharing; that a new post
attaches to many existing posts at once is the densification entry's reading of the
stream, which is what makes sharing available to carry the coherence. The opposition
of the two halves is read directly, as the cosine between the same-only and
foreign-only deltas of one post and between its net same and net foreign pushes; the
foreign-share entry supplies the condition under which the two net pushes are of the
same size, that a post's arrivals are foreign in the share its neighbourhood already
is, so that the neighbourhood mean sits between the home centroid and the foreign
ones and the two kinds of arrival move it in opposite senses along that axis. The
coherence entry's reading that the coherent part of the stream is the cross-subreddit
share is held to this split and found half right: the foreign arrivals are the more
coherent per edge, and the same-subreddit arrivals are not incoherent.

## Backing

none

<!-- APPEND BELOW THIS LINE ONLY -->

## Verdicts

## References

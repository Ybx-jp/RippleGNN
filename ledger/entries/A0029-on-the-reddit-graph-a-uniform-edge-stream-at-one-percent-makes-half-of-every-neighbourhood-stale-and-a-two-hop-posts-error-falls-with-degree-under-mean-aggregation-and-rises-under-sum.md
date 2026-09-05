---
id: A0029-on-the-reddit-graph-a-uniform-edge-stream-at-one-percent-makes-half-of-every-neighbourhood-stale-and-a-two-hop-posts-error-falls-with-degree-under-mean-aggregation-and-rises-under-sum
kind: claim
stated: 2026-09-05T14:20:00-07:00
author: main
grade: measured
supersedes: none
verbatim_sha: 33017620c8240589ff2ee0a4cb821cb339af25740fb3bee103e6090e6c31fd25
---

## Assertion

On the Reddit post graph before day 20, uniform random deletion of one percent of the
edges touches 41 percent of existing posts at one hop and leaves the median post with
57 percent of its neighbours stale, rising from 45 percent on the bottom degree decile
to 70 percent on the top, while uniform insertion of one percent as many edges between
random pairs of existing posts touches 50 percent of posts and leaves 50 percent of
every post's neighbours stale at every decile; on posts whose own edges are unchanged,
the median L2 error of a trained two-layer mean-aggregation GraphSAGE embedding falls
with degree on both streams at every rate measured, the top decile's median being 0.085
to 0.231 of the bottom's, and falls with degree within fixed stale-fraction bins, while
on the same architecture with sum aggregation it rises, the top decile's being 3.2 to
25 times the bottom's; the across-checkpoint spread of a decile's median is 3 to 4
percent of its value under mean aggregation, and two forward passes of one checkpoint
on the same graph on the CSR path differ by up to 2.7 × 10⁻⁷ of the embedding norm.

## Scope

metric: per existing post and draw, the share of its starting-graph neighbours that are stale (endpoints of a changed edge whose post-ReLU first-layer hidden vector differs between the starting and the mutated graph), as decile means pooled over draws beside the analytic expectation; per existing post, draw and checkpoint, the L2 distance between the checkpoint's second-layer embedding on the mutated graph and on the starting graph, as the median over the posts of a degree decile touched at two hops only (own edges unchanged), pooled over five draws and five checkpoints, and the same within stale-fraction bins; the top-minus-bottom decile difference of each checkpoint's median with a 95 percent t interval across the five checkpoints and the range of the top/bottom ratio; the share of existing posts and of the exact two-hop set whose relative error exceeds a tolerance
cohort: the paper's 11,606,919-edge Reddit graph restricted to posts before day 20 (153,430 posts, 5,376,616 edges; degree decile lower edges 0, 8, 21, 32, 41, 49, 59, 73, 96, 144) as the starting graph; ten checkpoints by A0024's recipe (two-layer SAGEConv, 602 to 64 to 64, linear head to 41 classes, Adam at 0.01 for 100 epochs, seeds 20260903 to 20260907), five with mean and five with sum aggregation at both layers, training accuracy 0.969 to 0.972 and 0.798 to 0.879; uniform deletion of 0.01, 0.1 and 1 percent of edges and uniform insertion of 0.1 and 1 percent as many edges between random pairs of existing posts, five draws each from seeds 20260905 to 20260909; strata shares at 1 percent: deletion 0.409 one-hop, 0.563 two-hop-only, 0.028 untouched, insertion 0.504, 0.484, 0.013; decile-mean stale fraction at 1 percent deletion 0.452, 0.522, 0.560, 0.573, 0.567, 0.571, 0.585, 0.622, 0.665, 0.704 and at 1 percent insertion 0.446 then 0.503 to 0.505; median two-hop-only error under mean aggregation from bottom to top decile 0.0133 to 0.0011 (delete 0.01 percent), 0.0224 to 0.0050 (0.1), 0.1024 to 0.0189 (1), 0.1210 to 0.0104 (insert 0.1), 0.3504 to 0.0808 (insert 1), ratios 0.085, 0.223, 0.185, 0.086, 0.231 with across-checkpoint ranges 0.084 to 0.086, 0.218 to 0.226, 0.183 to 0.188, 0.083 to 0.088, 0.221 to 0.241; under sum 2.83 to 8.52, 4.27 to 41.7, 11.9 to 289, 8.06 to 31.1, 14.0 to 112, ratios 3.23, 10.0, 25.3, 3.88, 8.02; at delete 1 percent within the 0.50 to 0.80 stale-fraction bin 0.104 to 0.019 and at insert 1 percent 0.376 to 0.085; relative error exceeding 0.01 at 1 percent on 0.214 (deletion) and 0.514 (insertion) of existing posts under mean aggregation; RTX 3060, 497 s, 2.93 GiB
condition: deterministic full-graph inference on the CSR sparse path, on which two forward passes of one checkpoint on the same graph differ by up to 1.8 × 10⁻⁵ in L2 and 2.7 × 10⁻⁷ of the embedding norm under mean aggregation (0.21 and 1.5 × 10⁻⁵ under sum), and posts beyond two hops of any change read at that floor (2.9 × 10⁻⁷ and 6.3 × 10⁻⁵ of the norm); the stale fraction's denominator is the starting-graph degree, so inserted neighbours are not in it; a checkpoint retrained by the recipe is not bitwise the same checkpoint and cell medians moved in the third or fourth significant digit across three runs; the error is absolute L2, and relative to the embedding norm the sum-aggregation error falls with degree too (0.0205 to 0.0103 at 1 percent deletion) because the norm grows with degree; medians are pooled over draws and checkpoints and the t interval treats the draws as fixed; the sum checkpoints' across-seed spread of a decile median is 30 to 40 percent; one starting snapshot, the uniform streams only, and no refresh of any kind

## Grounds

- lab: lab/017-one-percent-of-edges-makes-half-of-every-neighbourhood-stale-and-at-a-fixed-stale-fraction-error-still-falls-with-degree.md § "Observation" @86804c6
- entry: A0012-stale-fraction-error-is-non-increasing-in-degree-under-mean-aggregation · cites-as-live
- entry: A0027-on-the-reddit-graph-random-deletions-make-stale-neighbour-deltas-incoherent-dissimilar-insertions-make-them-coherent-and-the-real-stream-sits-between · cites-as-live

## Warrant

The five tables of lab/017 are the measurement, read on five draws of each stream over
the same starting graph and recipe as A0024 and A0027, with the sum checkpoints
trained beside the mean ones from the same seeds. The stale fraction is read against
its analytic expectation, which the decile means match to 0.002 on every stream, and
the error against the untouched stratum, which reads at the same-graph-twice floor;
the strata are drawn with the eight-bit count that misplaced up to four posts per arm
in A0024's run corrected. The two-hop-only stratum is the population where the error
is the neighbours' staleness alone, which is what A0012's brackets describe and what
A0013 is about; A0012 gives the reading that a fall with degree at fixed fraction is
the incoherent bracket's direction and a flat line the coherent one's, and A0027 gives
the reading that the insertion stream, the one whose fraction is flat across degree
and so realises A0013's condition, is the coherent one, so the fall on that stream is
the coherent bound itself falling with degree as A0027 found. The direction of the
result is A0013's predicted direction on the same snapshot; the entry does not resolve
A0013, which resolves by preregistered experiment, and is the pilot that experiment's
margin and floor are derived from.

## Backing

none

<!-- APPEND BELOW THIS LINE ONLY -->

## Verdicts


## References

---
id: A0021-full-recomputes-differing-only-in-seed-disagree-on-two-percent-of-reddit-posts-and-under-one-percent-of-hubs
kind: claim
stated: 2026-09-03T20:32:05-07:00
author: main
grade: measured
supersedes: none
verbatim_sha: 5d348d731cd6cfc161ba7580e87d64af7561fb69f0f65c77dbf0ac0bff42ee0b
---

## Assertion

Two full recomputes of the Reddit post graph by GraphSAGE checkpoints that differ only
in their training seed disagree on the predicted label of about 2 percent of the posts,
a fifth of what their error rates allow; the disagreement falls with degree by a factor
of about twenty, from about 10 percent on the lowest decile to 0.4 to 0.5 percent on
the seventh and eighth deciles, and rises to about 0.8 percent on the top decile;
within a degree decile, posts touched by an episode's arriving edges and posts not
touched disagree at the same rate; and the two checkpoints keep about 22 percent of a
post's twenty nearest cosine neighbours, so seed churn is a denominator for the
behavioural disagreement rate and not for neighbourhood survival.

## Scope

metric: per-node disagreement of the two heads' argmax labels and one minus the overlap of the node's 20 nearest cosine neighbours, each averaged over the ten pairs of five seeds, reported per stratum and per degree decile of the existing posts on the post-episode graph, with the range across pairs
cohort: the paper's 11,606,919-edge Reddit graph; checkpoints trained full-batch on the graph before the episode (two-layer SAGEConv with mean aggregation, 602 to 64 to 64, linear head to 41 classes, Adam at 0.01 for 100 epochs, no validation pass, seeds 20260903 to 20260907) and run once on the post-episode graph; three episodes, day 20 for one day (disagreement 0.0209 overall, 0.0329 on new posts, 0.0116 one hop, 0.0308 two hops only, 0.1802 untouched; deciles 0.0981, 0.0365, 0.0211, 0.0129, 0.0096, 0.0071, 0.0050, 0.0043, 0.0045, 0.0084; kNN loss 0.783 overall, 0.754 to 0.835 across deciles), day 25 for one day (0.0220 overall), day 20 for one hour (0.0202 overall; touched and untouched within a point of each other in every populated decile); each checkpoint at 96.9 to 97.3 percent on its training posts and 95.0 to 95.6 on the arriving posts; RTX 3060, 19 to 27 s per checkpoint
condition: nothing is refreshed and no embedding is stale, so the figures bound what a refreshed space is compared against and say nothing about drift; no dropout, weight decay or schedule, and no early stopping, so churn from a tuned training recipe may differ; posts absent before the episode's end are excluded; the second run of the day-20 episode reproduced every figure to within 0.001, so the figures carry that much run-to-run nondeterminism from the sparse path; the top-decile rise is recorded without an explanation

## Grounds

- lab: lab/011-one-day-of-the-real-stream-touches-the-whole-graph-and-seed-churn-is-two-percent.md § "Observation" @ce23495
- entry: A0020-a-day-of-the-reddit-growth-stream-touches-98-percent-of-existing-posts-within-two-hops · cites-as-live

## Warrant

The stratum and decile tables of lab/011 are the measurement, ten seed pairs on each
of three episodes agreeing within 0.4 points. Disagreement between two classifiers is
bounded by the sum of their error rates, 0.058 on the training posts and 0.092 on the
arriving posts, and the measured 0.02 sits at a fifth of that bound, which is the
compression a saturated task imposes on a disagreement denominator. That touched and
untouched posts of one decile churn alike, while one-hop posts churn less than
two-hop-only posts, is read with A0020: the stream lands on hubs, so touched status and
degree are confounded and the stratum difference is a degree difference. The
neighbourhood overlap across seeds, 0.22 against the 0.0001 two independent spaces
would share, is the reason seed churn cannot serve as the floor for a rank-survival
probe: a refresh that kept a quarter of a node's neighbourhood would pass it.

## Backing

none

<!-- APPEND BELOW THIS LINE ONLY -->

## Verdicts


## References

---
id: A0023-a-day-of-the-reddit-growth-stream-turns-over-a-ninth-of-every-existing-post-neighbourhood-under-no-refresh
kind: claim
stated: 2026-09-04T13:05:10-07:00
author: main
grade: measured
supersedes: none
verbatim_sha: bed3a2d1196d4b20acdb0f7f58fd243a29d2925f5d260cfd73953f26dbca6e88
---

## Assertion

On the Reddit post graph's real growth stream under mean aggregation, an existing
post's stale embedding loses about 11 percent of its twenty nearest cosine neighbours
among existing posts after a day of insertions, about 5 percent after six hours and
about 1.5 percent after an hour, relative to the full recompute of the same
checkpoint; the loss falls with degree, from about 14 percent on the lowest decile to
about 8 percent on the top decile at a day, and among one-hop-touched posts from about
52 percent to about 8 percent; and the loss is nonzero on untouched posts, about 8
percent at a day, because their neighbours moved while they did not; so on the
deterministic inference path, whose floor is zero, the neighbourhood probe has
headroom on every decile where the head-disagreement probe has none.

## Scope

metric: per existing post, one minus the overlap between its twenty nearest cosine neighbours among existing posts in the checkpoint's pre-episode embedding and in the same checkpoint's post-episode embedding, exact search, averaged per cell and over five seeds; and one minus the cosine and the relative L2 change of the post's own embedding
cohort: the paper's 11,606,919-edge Reddit graph with the growth stream of A0018; checkpoints as in A0021 (two-layer SAGEConv with mean aggregation, 602 to 64 to 64, seeds 20260903 to 20260907); episodes day 20 for one hour (loss 0.015 overall, 0.045 one-hop-touched, 0.010 untouched), six hours (0.049, 0.071, 0.031), one day (0.114, 0.127, 0.080; deciles 0.141 to 0.083; touched posts by decile 0.524, 0.233, 0.164, 0.140, 0.129, 0.119, 0.113, 0.106, 0.097, 0.083; relative L2 among touched posts 0.280 to 0.016) and day 25 for one day (0.097, 0.109, 0.063); sum aggregation on day 20 for a day 0.344; RTX 3060
condition: the kNN space is restricted to existing posts in both embeddings, so the arriving posts' entry into the neighbourhood is not counted as loss; nothing is refreshed; the zero floor is lab/002's for full-graph inference, and the sparse path's run-to-run nondeterminism, under 0.001 in lab/011 and lab/012, is the working floor; the 0.78 seed-churn overlap loss is not the floor for this probe, as A0021 records; K is 20 and the graph is the paper edge set only

## Grounds

- lab: lab/012-no-refresh-sits-inside-the-seed-band-on-nine-deciles-of-ten.md § "Observation" @98312cb
- lab: lab/002-the-noise-floor-is-a-rank-metric-problem.md § "Observation" @4563bb0
- entry: A0021-full-recomputes-differing-only-in-seed-disagree-on-two-percent-of-reddit-posts-and-under-one-percent-of-hubs · cites-as-live

## Warrant

The stratum and decile tables of lab/012 are the measurement, five seeds within 0.003
of each other on every cell. The floor is lab/002's: full-graph inference on a fixed
graph is bitwise reproducible, so a neighbourhood loss between two runs of one
checkpoint on two graphs is attributable to the graph change. A0021 is the reason the
seed band in the same tables is not read as this probe's floor: two seeds share a
fifth of a neighbourhood, so a band of 0.78 would pass any policy. That the loss is
nonzero on untouched posts while their own embeddings are unchanged to 10⁻⁷ is the
rank metric registering movement of the other points, which is what lab/002 found
makes cosine and rank disagree, here on a real stream.

## Backing

none

<!-- APPEND BELOW THIS LINE ONLY -->

## Verdicts


## References

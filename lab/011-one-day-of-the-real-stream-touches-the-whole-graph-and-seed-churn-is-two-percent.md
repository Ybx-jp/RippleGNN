# 011 — One day of the real stream touches the whole graph, and seed churn is two percent

**Date:** 2026-09-03 · **Component:** experiment design, the behavioural-consistency denominator · **Status:** measured.

## What was asked

lab/008's third probe. The measurement consultation made behavioural consistency the
downstream arm: the disagreement rate of a fixed head between the refreshed and the
fully recomputed space, stratified to the nodes a mutation touched, with
full-recompute-versus-full-recompute churn across seeds as the denominator, and a
warning that a saturated task compresses disagreement. This note measures that
denominator on real episodes of the growth stream lab/009 found. Script:
`lab/probe_seed_churn.py`, reading the edge sets `lab/probe_reddit_stream.py` writes.

Setup, on the paper edge set: five checkpoints are trained on the graph as it stands
before the episode, one per seed, identical in everything else (two-layer GraphSAGE
602 → 64 → 64, linear head, full-batch Adam at 0.01 for 100 epochs, lab/010's settings
without the validation pass). Each is then run once on the graph after the episode;
that is the full recompute. Between every pair of seeds, per node, the two heads'
argmax labels disagree or not, and the fraction of the node's 20 nearest cosine
neighbours that the other space does not keep. Old posts are stratified by whether an
arriving edge is incident to them (one hop), whether they neighbour such a post (two
hops only), or neither, and by degree decile on the post-episode graph. Seeds
20260903–20260907. The helpers were checked on known cases before the numbers were
read: overlap of an index set with itself is 1, of two random 20-sets from 1,000 is
0.020, and a 20,000-point embedding keeps 0.976 of its neighbours under one percent
noise and 0.001 against an independent draw.

## Observation

Three episodes: the first val/test day, the first hour of it, and a day five days on.

| episode | old posts | new posts | arriving edges | old touched 1-hop | 2-hop only | untouched | mean degree 1-hop / 2-hop / untouched |
|---|---|---|---|---|---|---|---|
| day 20, one day | 153,430 | 8,625 | 546,352 | 105,172 (68.5%) | 45,570 (29.7%) | 2,688 (1.8%) | 93.7 / 30.8 / 0.8 |
| day 20, one hour | 153,430 | 338 | 20,602 | 16,306 (10.6%) | 122,397 (79.8%) | 14,727 (9.6%) | 147.7 / 66.8 / 12.5 |
| day 25, one day | 192,455 | 8,475 | 660,956 | 132,686 (68.9%) | 56,949 (29.6%) | 2,820 (1.5%) | 113.2 / 35.7 / 1.0 |

Training took 19 s per seed on the day-19 graph (5.38M edges) and 27 s on the day-24
graph (8.21M). Accuracy of each checkpoint on the post-episode graph: 96.9 to 97.3
percent on the training posts, 95.0 to 95.6 on the new posts, on every episode.

Churn between full recomputes, mean over the ten seed pairs, with the range across
pairs, day-20 one-day episode:

| stratum | n | disagreement | range | kNN@20 loss | range |
|---|---|---|---|---|---|
| all present | 162,055 | 0.0209 | 0.0201–0.0214 | 0.783 | 0.775–0.788 |
| new posts | 8,625 | 0.0329 | 0.0307–0.0362 | 0.789 | 0.783–0.795 |
| old, touched 1-hop | 105,172 | 0.0116 | 0.0112–0.0120 | 0.775 | 0.768–0.780 |
| old, touched 2-hop only | 45,570 | 0.0308 | 0.0295–0.0320 | 0.799 | 0.790–0.804 |
| old, untouched | 2,688 | 0.1802 | 0.1674–0.1875 | 0.800 | 0.794–0.806 |

The day-25 episode gives the same picture within 0.4 points on every stratum
(overall 0.0220, one-hop 0.0125, two-hop-only 0.0347, untouched 0.1837). The one-hour
episode: overall 0.0202, new posts 0.0254 on 338 nodes, one-hop 0.0093, two-hop-only
0.0158, untouched 0.0684.

By degree decile among old posts, day-20 one-day episode:

| decile | degree | n | touched 1-hop | disagreement | kNN@20 loss | disagreement, touched 1-hop | disagreement, untouched |
|---|---|---|---|---|---|---|---|
| 0 | 0–8 | 14,287 | 0.107 | 0.0981 | 0.835 | 0.0837 | 0.1819 |
| 1 | 8–22 | 16,167 | 0.347 | 0.0365 | 0.808 | 0.0396 | 0.0333 |
| 2 | 22–34 | 15,057 | 0.570 | 0.0211 | 0.794 | 0.0229 | – |
| 3 | 34–43 | 15,462 | 0.680 | 0.0129 | 0.788 | 0.0133 | – |
| 4 | 43–52 | 15,655 | 0.729 | 0.0096 | 0.778 | 0.0103 | 0.0000 |
| 5 | 52–62 | 14,853 | 0.759 | 0.0071 | 0.767 | 0.0076 | – |
| 6 | 62–76 | 15,561 | 0.782 | 0.0050 | 0.765 | 0.0057 | – |
| 7 | 76–100 | 15,407 | 0.896 | 0.0043 | 0.770 | 0.0044 | – |
| 8 | 100–151 | 15,612 | 0.960 | 0.0045 | 0.768 | 0.0047 | – |
| 9 | 151–2,660 | 15,369 | 0.994 | 0.0084 | 0.754 | 0.0085 | – |

The one-hour episode's deciles, where the untouched stratum is populated at every
degree, put touched and untouched posts of the same decile within a point of each
other (decile 1: 0.0355 against 0.0251; decile 3: 0.0147 against 0.0031; deciles 6 to
9: 0.004 to 0.011 against 0.000). Each checkpoint's mean error on the new posts bounds
the pairwise disagreement there at 0.092 and on the training posts at 0.058. A second
run of the day-20 episode reproduced every figure above to within 0.001.

## Interpretation

**At one-day granularity the touched stratum is the graph.** Sixty-nine percent of the
existing posts receive a new neighbour in a day, ninety-eight percent are within two
hops of one, and the untouched two percent are the posts the paper edge set leaves
isolated or nearly so, with a mean degree under one. A two-layer model's receptive
field is two hops, so a day of the real stream changes the exact embedding of
ninety-eight percent of the nodes. That is the stream lab/009 measured, preferential
attachment at half a million edges a day, seen from the node's side. "Stratified to
the nodes a mutation touched" only stratifies if the episode is short: at one hour
(338 posts) the one-hop set is a tenth of the graph and the untouched set is
populated at every degree, and even then ninety percent of the graph is within two
hops. The episode length is a parameter the preregistration has to set, and it trades
against the number of independent episodes the month affords: thirty at a day,
seven hundred at an hour, with the touched set shrinking as the count grows.

**The denominator is two percent overall and under one percent on the hubs.** Two full
recomputes that differ only in seed disagree on 2.0 to 2.2 percent of the nodes on
every episode, a fifth of what their error rates would allow, which is the compression
the consultation predicted, now with a number. It falls with degree by a factor of
twenty, from ten percent on the bottom decile to four or five per thousand on deciles 7
and 8, and rises again to eight per thousand on the top decile, an uptick this note
records without an explanation. The old hubs that keep receiving neighbours, the nodes
the refresh question is about, therefore have a denominator of half a percent: a
refresh policy shows a behavioural effect on them only if a fixed head disagrees with
the full recompute on more than about one node in two hundred, and with fifteen
thousand nodes per decile that resolves to about seventy-five nodes.

**The stratum effect is a degree effect.** One-hop-touched posts churn less than
two-hop-only posts (1.2 against 3.1 percent) because the stream lands on hubs, and
within a degree decile touched and untouched posts churn alike. On this stream
touched status and degree are confounded by construction, so the preregistration
stratifies on both jointly or it will read a degree effect as an exposure effect.

**Seed churn is not the denominator for rank survival.** Two seeds keep 22 percent of
a node's twenty nearest neighbours, two thousand times the 0.01 percent that
independent spaces would share and a long way from stable. A refresh policy compared
against that band would pass by keeping a quarter of the neighbourhood, so the kNN
probes keep the fixed-weights no-op band lab/002 measured as their floor, and seed
churn is the denominator of the behavioural arm alone, which is what the consultation
said and what this note confirms the reason for. The kNN loss varies little with
degree, 0.75 to 0.83, against the twenty-fold fall in disagreement.

**What is not measured here.** No embedding was refreshed; the note bounds what a
refreshed space is compared against and says nothing about how far one drifts. The
accuracy on the new posts, 95 percent from checkpoints trained on the day-19 graph
without early stopping, reproduces lab/010's test number from a graph with half the
edges, which is consistent with A0019 and adds nothing to it.

## Open

- The episode length for the preregistration, and with it the touched fraction and the
  episode count; a question for the measurement consultation beside lab/010's.
- The top decile's uptick in seed disagreement.
- The remaining probes in lab/008's list: the gap pilot at three generator settings,
  the memorization check on the generator's deletions, the ogbn-arxiv episode count
  and recompute, mutation-induced coherence, the checkpoint's spectral norms, the
  uniform-stream stale-fraction distribution.

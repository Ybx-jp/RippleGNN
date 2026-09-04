# 012 — No refresh sits inside the seed band on nine deciles of ten: the gap pilot on the real stream

**Date:** 2026-09-04 · **Component:** experiment design, the margin denominator · **Status:** measured.

## What was asked

lab/008's fourth probe. The measurement consultation's margin ordering takes the
denominator as the lower confidence limit, across at least five seeds, of the gap
between doing nothing and full recomputation, with a pre-registered gap-floor
eligibility rule: a cell whose gap does not clear the no-op band has no headroom, and
is reported rather than dropped. lab/008 asked for the pilot at three generator
settings. lab/009 made the real arrival order the insertion stream and left the
generator only deletions, and whether the synthetic stream stays at all is a question
for the next modelling round, so this note runs the pilot at three lengths of the real
growth stream instead and leaves the generator's gap to the ruling. Script:
`lab/probe_gap.py`, reading the edge sets `lab/probe_reddit_stream.py` writes.

## Setup

**The task** is node classification. Each post in the Reddit post graph carries a
label, the subreddit it was posted to, one of 41. The model is a two-layer GraphSAGE
with mean aggregation (602 input features → 64 → 64) and a linear head on the
64-dimensional embedding that predicts the label. A checkpoint is the GraphSAGE and
its head together, trained full-batch with cross-entropy (Adam at 0.01, 100 epochs)
on the posts the dataset marks as training, restricted to those present in the
starting graph. Five checkpoints were trained, identical except for the seed
(20260903–20260907). No link prediction is run anywhere in this note.

**The starting graph** is every post created before day 20 and every edge of the
paper's 11.6M-edge set whose two endpoints are both such posts: 153,430 posts and
5.38M edges. Posts are ordered by creation time using the dataset's post ids, and day
20 is where the published train/validation split falls.

**The mutation** is the real arrival order, not a generator. An episode adds the posts
created in a window starting at day 20 (one hour: 338 posts; six hours: 2,042; one
day: 8,625) and every paper edge that has both endpoints present by the end of the
window. Every arriving edge has at least one new endpoint; the script asserts this,
and it holds because posts on this graph acquire edges only when they are created.
Nothing in the starting graph is altered: no edges are deleted or rewired, no
features or labels change, and no checkpoint is retrained or fine-tuned. The
post-episode graph is the starting graph plus the new posts and their edges. A
replication runs the same day-long episode from day 25 on the larger graph that
exists by then, and a control repeats the day-20 episodes with sum aggregation in
place of mean.

**What is compared.** For one checkpoint, the embeddings of the existing posts
computed on the starting graph, which is what those posts keep if nothing is
refreshed, against the embeddings of the same posts computed on the post-episode
graph, which is the full recompute. Four quantities per existing post: whether the
head's predicted label differs between the two, one minus the overlap of the post's
twenty nearest cosine neighbours among existing posts in the two embeddings, one
minus the cosine between the two embeddings, and the relative L2 change. This is the
gap. New posts have no starting-graph embedding and enter no figure. Disagreement is
between two predictions, not against ground truth; accuracy against ground truth is
printed once per run as a check on the checkpoints.

**The band** is a different comparison, computed in the same run on the same posts:
two checkpoints that differ only in seed, both run on the post-episode graph,
compared on the same four quantities, averaged over the ten pairs of five seeds. It
is how far two full recomputes disagree with each other for no reason but the seed.

**Cells and the rule.** Existing posts are grouped by whether an arriving edge lands
on them (touched at one hop), whether a starting-graph neighbour of theirs was
(touched at two hops only), or neither (untouched), and by degree decile on the
post-episode graph. Each gap cell reports the mean over the five seeds and the lower
limit of a 95 percent t interval; a cell is eligible when that limit exceeds the
band. Before any number was read, the untouched stratum served as the known
negative: a post with no arriving edge within two hops has an identical two-hop
neighbourhood on both graphs and so the same two-layer output, and its measured
cosine drift is at most 2.4 × 10⁻⁷ on every run; the one-hop stratum's drift is
positive on every seed.

## Observation

Each run trains its five checkpoints in 16 s each (23 s on the day-24 graph) and
scores an episode in 25 to 39 s; peak VRAM 5.8 GiB (7.2 on day 25). Full-recompute
accuracy on the post-episode graph under mean aggregation is 96.9 to 97.3 percent on
the training posts and 95.0 to 95.6 on the new posts, as in lab/011.

The gap under no refresh against the seed band, mean aggregation, existing posts, mean
over five seeds (the lower confidence limit is within 0.0005 of every disagreement
mean below):

| episode | stratum | n | gap: disagreement | band: seed churn | gap: kNN@20 loss | band | cosine drift | relative L2 |
|---|---|---|---|---|---|---|---|---|
| day 20, 1 h | all existing | 153,430 | 0.0002 | 0.0202 | 0.015 | 0.780 | 0.0000 | 0.002 |
|  | touched 1-hop | 16,306 | 0.0016 | 0.0092 | 0.045 | 0.764 | 0.0003 | 0.013 |
|  | touched 2-hop only | 122,397 | 0.0001 | 0.0158 | 0.011 | 0.780 | 0.0000 | 0.001 |
|  | untouched | 14,727 | 0.0000 | 0.0684 | 0.009 | 0.799 | 0.0000 | 0.000 |
| day 20, 6 h | all existing | 153,430 | 0.0011 | 0.0201 | 0.049 | 0.780 | 0.0002 | 0.008 |
|  | touched 1-hop | 55,677 | 0.0024 | 0.0095 | 0.071 | 0.766 | 0.0006 | 0.019 |
|  | touched 2-hop only | 92,714 | 0.0004 | 0.0208 | 0.036 | 0.787 | 0.0000 | 0.002 |
|  | untouched | 5,039 | 0.0000 | 0.1258 | 0.031 | 0.808 | 0.0000 | 0.000 |
| day 20, 24 h | all existing | 153,430 | 0.0035 | 0.0203 | 0.114 | 0.780 | 0.0010 | 0.024 |
|  | touched 1-hop | 105,172 | 0.0046 | 0.0116 | 0.127 | 0.772 | 0.0015 | 0.032 |
|  | touched 2-hop only | 45,570 | 0.0013 | 0.0308 | 0.086 | 0.796 | 0.0001 | 0.006 |
|  | untouched | 2,688 | 0.0000 | 0.1808 | 0.080 | 0.799 | 0.0000 | 0.000 |
| day 25, 24 h | all existing | 192,455 | 0.0028 | 0.0215 | 0.097 | 0.791 | 0.0007 | 0.019 |
|  | touched 1-hop | 132,686 | 0.0036 | 0.0125 | 0.109 | 0.785 | 0.0010 | 0.026 |

By degree decile on the day-20 one-day episode, all existing posts of the decile and
then the posts of the decile touched at one hop:

| decile | degree | n | gap: disagreement | band | gap: kNN@20 loss | relative L2 | 1-hop n | 1-hop gap: disagreement | lower limit | 1-hop band | 1-hop gap: kNN@20 loss | 1-hop relative L2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0–8 | 14,287 | 0.0152 | 0.0981 | 0.141 | 0.039 | 1,532 | 0.1131 | 0.1086 | 0.0836 | 0.524 | 0.280 |
| 1 | 8–22 | 16,167 | 0.0074 | 0.0364 | 0.138 | 0.032 | 5,609 | 0.0195 | 0.0182 | 0.0396 | 0.233 | 0.081 |
| 2 | 22–34 | 15,057 | 0.0046 | 0.0211 | 0.129 | 0.029 | 8,584 | 0.0075 | 0.0065 | 0.0230 | 0.164 | 0.047 |
| 3 | 34–43 | 15,462 | 0.0026 | 0.0130 | 0.121 | 0.026 | 10,507 | 0.0038 | 0.0032 | 0.0133 | 0.140 | 0.036 |
| 4 | 43–52 | 15,655 | 0.0020 | 0.0096 | 0.116 | 0.023 | 11,418 | 0.0026 | 0.0020 | 0.0103 | 0.129 | 0.031 |
| 5 | 52–62 | 14,853 | 0.0012 | 0.0071 | 0.109 | 0.020 | 11,275 | 0.0016 | 0.0011 | 0.0076 | 0.119 | 0.026 |
| 6 | 62–76 | 15,561 | 0.0009 | 0.0050 | 0.105 | 0.018 | 12,175 | 0.0011 | 0.0009 | 0.0056 | 0.113 | 0.022 |
| 7 | 76–100 | 15,407 | 0.0006 | 0.0043 | 0.103 | 0.018 | 13,806 | 0.0007 | 0.0005 | 0.0044 | 0.106 | 0.020 |
| 8 | 100–151 | 15,612 | 0.0007 | 0.0045 | 0.096 | 0.017 | 14,990 | 0.0007 | 0.0003 | 0.0047 | 0.097 | 0.018 |
| 9 | 151–2,660 | 15,369 | 0.0007 | 0.0085 | 0.083 | 0.016 | 15,276 | 0.0007 | 0.0004 | 0.0085 | 0.083 | 0.016 |

One cell of the forty clears the band: the bottom decile's one-hop-touched posts, at
six hours (0.0901, lower limit 0.0794, band 0.0775, 382 posts) and at a day (above,
1,532 posts); on day 25 it does not (0.0893, lower limit 0.0837, band 0.0867, 2,016
posts). At one hour that cell holds 61 posts and its lower limit, 0.0905, sits under
its band of 0.1213. Every other cell's gap is under half its band: among touched posts
the ratio falls from a half on decile 1 to a twelfth on decile 9 (0.0007 against
0.0085 at a day), and on the all-posts deciles it lies between a sixth and a twelfth.
A second run
of the day-20 episodes reproduced every mean-aggregation figure above to within 0.001.

Sum aggregation, day 20, existing posts:

| episode | stratum | gap: disagreement | band | gap: kNN@20 loss | band | relative L2 |
|---|---|---|---|---|---|---|
| 1 h | all existing | 0.0025 | 0.1572 | 0.059 | 0.732 | 0.006 |
|  | touched 1-hop | 0.0082 | 0.1362 | 0.120 | 0.721 | 0.024 |
| 6 h | all existing | 0.0086 | 0.1572 | 0.158 | 0.732 | 0.027 |
|  | touched 1-hop | 0.0126 | 0.1392 | 0.200 | 0.724 | 0.048 |
| 24 h | all existing | 0.0237 | 0.1567 | 0.344 | 0.730 | 0.090 |
|  | touched 1-hop | 0.0255 | 0.1376 | 0.370 | 0.728 | 0.111 |
| 24 h | decile 0, touched 1-hop | 0.2614 | 0.3956 | 0.719 | 0.861 | 0.406 |
| 24 h | decile 9, touched 1-hop | 0.0239 | 0.1883 | 0.287 | 0.750 | 0.089 |

Under sum aggregation no cell clears the band on any episode. The sum checkpoints score
79.9 to 88.0 percent on the training posts and 80.2 to 89.9 on the new posts, against
97 and 95 for mean, with the same recipe. The sum arm is also less reproducible: a
second run moved its band from 0.179 to 0.157 on the day-long episode while moving the
gap by under 0.001, so its band carries about 0.02 of run-to-run variation from the
sparse path's nondeterminism during training.

## Interpretation

Rewritten on the day of writing, after lab/013 ran the same pilot at the adversarial
end. The observation above is unchanged.

**This note measured the lower envelope, and its headline was foreseeable.** The real
growth stream adds posts and their edges and alters nothing that exists; the
arriving neighbours resemble the ones already there; aggregation is mean; and the
head is a subreddit classifier whose label the post's own features fix for most
posts (lab/010). A0012 and A0013 say that under those conditions the change to a
hub's aggregate at a fixed fraction of new neighbours is small and non-increasing in
degree. The pilot confirmed that with numbers: a day of the stream, half a million
edges on two thirds of the existing posts, moves the head's label on 0.35 percent of
them against a 2 percent seed band, a sixth overall and a twelfth on the top decile's
touched posts. What the note adds is the size of the effect and the one place it
shows: the lowest-degree posts that received a neighbour, where the new edge is a
large fraction of the neighbourhood and the relative embedding change is 0.28
against 0.016 on the top decile, a factor of seventeen, the fraction law on a real
stream. lab/008 ranked streams by how much they can hurt the claim, hot-hub first,
and this note ran the pilot on the least hurtful one. It is a result about where
refresh does not matter, at the easy edge of the question, and it should have been
delivered as such. lab/013 is the other edge.

**What it is usable for.** Three things. The gap-floor rule applied to this stream
under this head leaves the behavioural arm one eligible cell in forty, the bottom
decile's touched posts, and no hub cell, so preregistering that arm as specified on
this stream would preregister a null; lab/013 finds the same on nine arms of thirteen
at the adversarial end and says why. The neighbourhood loss under no refresh, 0.11 at
a day and 0.015 at an hour, falling with degree, against a zero floor on the
deterministic path (lab/002), is the scale a refresh policy competes over on the
geometric probe on this stream; the 0.78 seed band in the tables is not that probe's
floor (lab/011). And the sum control as specified is broken: sum checkpoints trained
by the mean recipe land at 80 to 88 percent, disagree with each other on 16 percent
of the posts, and vary by 0.02 on the band between runs, so the arm needs its own
recipe or is dropped.

**What is not measured here.** Any mutation of existing posts, which lab/013 runs;
the calibrated generator; sampled inference; a neighbourhood-dependent head; any
refresh policy, since a pilot of the denominator refreshes nothing.

## Open

- Whether the behavioural arm survives as designed, or narrows to the low-degree
  touched stratum, or changes head; the measurement consultation's question beside
  lab/010's and lab/011's.
- The generator's gap, after the modelling ruling on whether the synthetic stream stays.
- The remaining probes in lab/008's list: the memorization check on the generator's
  deletions, the ogbn-arxiv episode count and recompute, mutation-induced coherence,
  the checkpoint's spectral norms, the uniform-stream stale-fraction distribution.

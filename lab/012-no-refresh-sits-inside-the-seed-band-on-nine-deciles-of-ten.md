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

Setup as lab/011: five checkpoints trained on the paper edge set as it stands before
the episode (two-layer GraphSAGE 602 → 64 → 64, linear head, full-batch Adam at 0.01
for 100 epochs, seeds 20260903–20260907). For each episode, each checkpoint is run on
the pre-episode graph, which is the embedding an existing post keeps under no refresh,
and on the post-episode graph, which is the full recompute. The gap is the difference
between the two for the same checkpoint, per existing post: whether the head's argmax
label differs, one minus the overlap of the post's twenty nearest cosine neighbours
among existing posts, one minus the cosine, and the relative L2 change. The band is
lab/011's seed churn, recomputed in the same run on the same posts: full recompute
against full recompute between checkpoints, over the ten seed pairs. New posts have no
stale embedding and enter nothing. Cells are lab/011's touched strata and degree
deciles on the post-episode graph. Each gap cell reports the mean over seeds and the
lower limit of a 95 percent t interval; a cell is eligible when that limit clears the
band. Episodes: day 20 for one hour, six hours and one day; day 25 for one day as the
replication; and the day-20 episodes again with sum aggregation in both layers, the
design's sum control. Before the numbers were read, the untouched stratum served as
the known negative: a post with no arriving edge within two hops has the same two-layer
output on both graphs, and its measured cosine drift is at most 2.4 × 10⁻⁷ on every
run; the one-hop stratum's drift is positive on every seed.

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

**On the real stream, doing nothing is inside the seed band for the head.** A day of
the growth stream, half a million edges landing on two thirds of the existing posts,
moves the fixed head's label on 0.35 percent of them, and the five-seed band is 2
percent. The ratio is a sixth overall and a twelfth on the top decile's touched posts.
The gap-floor rule the consultation asked for, applied to this pilot, leaves the
behavioural arm one eligible cell in forty, the lowest-degree posts touched at one hop,
and that cell clears the band by a margin of a few thousandths on two of three
day-length episodes. Every hub cell, the cells the refresh question is about, is
ineligible. A refresh policy cannot show a behavioural effect where no refresh already
sits inside the noise of full recomputation, and the selection experiment, whether a
fidelity probe chooses the policy the head-based oracle would choose, has an oracle
that on nine deciles of ten cannot tell any policy from doing nothing.

**The reason is the fraction law read on real data.** Among touched posts the relative
L2 change under a day of insertions falls from 0.28 on the bottom decile to 0.016 on
the top, a factor of seventeen, while the number of arriving edges per post rises with
degree. Under mean aggregation an arriving neighbour moves the aggregate by its
distance from the mean divided by the new degree, and on this stream the arriving
neighbours are posts that resemble the ones already there: the cosine drift of a
hub's embedding after a day is a ten-thousandth. That is A0012 and A0013's
non-increasing curve with a real stream in place of a star graph, and it is the
behaviour those entries predicted for the model the roster's hypothesis favours.
Sum aggregation raises the gap sevenfold and the band eightfold, because five sum
checkpoints at 80 to 88 percent accuracy disagree with each other on 16 percent of the
posts, so the control arm has no headroom either, for the opposite reason.

**The kNN probe has headroom the head does not.** The neighbourhood loss under no
refresh is 0.11 at a day and 0.015 at an hour, and its floor on the deterministic path
is zero (lab/002), with the 0.001 run-to-run nondeterminism lab/011 measured on the
sparse path. The 0.78 seed band beside it in the tables is not its floor; lab/011
settled that. So the geometric probe sees a day of drift that turns over a ninth of
every neighbourhood, and the head sees nothing on nine deciles, which is lab/002's
finding, that semantic and geometric stability can disagree, in the direction that
matters for this design: the estimand the consultation kept as the downstream arm is
the one without headroom on this stream.

**What this does to the design.** Three readings, for the measurement consultation
with this table. The behavioural arm is a low-degree-touched-posts arm on this stream
and this head, and is stated as such. Or the head is the wrong instrument: a
41-way subreddit classifier at 95 percent, whose label a post's own features fix for
most posts (lab/010), is insensitive to neighbourhood drift by construction, and a
head whose output depends on the neighbourhood, link prediction over the arriving
edges or a neighbourhood-derived label, would have to be shown to have a gap before
it is named. Or the episode is longer than a day, which lab/011 already found trades
against the number of independent episodes and dissolves the touched stratum. What
the pilot rules out is running the behavioural arm as designed and reading a null.

**What is not measured here.** The gap under the generator's deletions, which waits
on the modelling ruling; the gap under sampled inference, where lab/002's floor is not
zero; the sum arm's accuracy against the mean arm's; and any refresh policy at all,
since a pilot of the denominator refreshes nothing.

## Open

- Whether the behavioural arm survives as designed, or narrows to the low-degree
  touched stratum, or changes head; the measurement consultation's question beside
  lab/010's and lab/011's.
- The generator's gap, after the modelling ruling on whether the synthetic stream stays.
- The remaining probes in lab/008's list: the memorization check on the generator's
  deletions, the ogbn-arxiv episode count and recompute, mutation-induced coherence,
  the checkpoint's spectral norms, the uniform-stream stale-fraction distribution.

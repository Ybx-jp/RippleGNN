# 021 — Same- and cross-subreddit arrivals each move a post's stale neighbours together, in opposed directions, and the real stream's coherence is their residual; most of it is arrivals shared among neighbours

**Date:** 2026-09-13 · **Component:** the mutation stream, the generator's coherence anchor · **Status:** measured.

## What was asked

lab/015 measured the coherence the real growth stream induces among a post's stale
neighbours' first-layer deltas (mean pairwise cosine 0.06 to 0.08 against a shuffled
0.003; the sum of the deltas 2.6 times its orthogonal value on the top decile) and read
the coherent part as the contribution of the cross-subreddit share of the arriving
edges, without splitting the stream by edge type. lab/020 measured the share (a quarter
of the edges the stream brings to an existing post cross subreddits, U-shaped in
degree, spread over many subreddits on a hub) and left the coherence half to the GPU:
the first-layer deltas split by same- and cross-subreddit arrivals, which both fourth
rounds (lab/018) asked for as what sets the generator's coherence anchor. This note is
that half. It runs lab/015's measurement on counterfactual graphs built from the same
stream with only one kind of arrival, adds two random-subset controls that separate
foreignness from the count and from the sharing of arrivals among neighbours, and
reads the same split inside each post, where the two kinds of push can be compared
directly. Script: `lab/probe_coherence_split.py`, 450 s at 2.34 GiB peak VRAM.

## Setup

**The task** is node classification. Each post in the Reddit post graph carries a
label, the subreddit it was posted to, one of 41. The model is a two-layer GraphSAGE
with mean aggregation (602 input features → 64 → 64) and a linear head on the
64-dimensional embedding that predicts the label. A checkpoint is the GraphSAGE and
its head together, trained full-batch with cross-entropy (Adam at 0.01, 100 epochs)
on the posts the dataset marks as training, restricted to those in the starting
graph. Five checkpoints were trained, identical except for the seed (20260903 to
20260907); they are lab/013's and lab/015's checkpoints, retrained by the same recipe
in 16 s each. The head is not used: the quantity measured is the change in a post's
first-layer hidden vector, the 64-dimensional vector after the ReLU that its
neighbours aggregate in the second layer. Nothing is compared to ground truth.

**The starting graph** is every post created before day 20 (posts are ordered by
creation using the dataset's post ids, and day 20 is where the published
train/validation split falls) and every edge of the paper's 11.6M-edge set whose two
endpoints are both such posts: 153,430 posts and 5,376,616 edges, 78 percent of them
joining two posts of the same subreddit. Degree deciles are on this graph.

**The mutations** are the real arrival stream for one day and for ten days from day
20, which adds the posts created in the window and the edges they bring and alters
nothing in the starting graph, and four counterfactual versions of it. Over ten days
the stream adds 78,491 posts, 4,535,051 edges joining a new post to an existing one
(*new-to-old*), of which 1,075,731 (23.7 percent) join posts of different subreddits
(*foreign*), and 1,623,964 edges joining two new posts; over one day 8,625 posts,
510,805 new-to-old edges of which 117,127 (22.9 percent) are foreign, and 35,547
new-to-new. The five variants, each a graph the same checkpoints are run on:

- *all*: the starting graph plus everything the stream brings (lab/015's growth arm);
- *same only*: plus the new posts, the new-to-new edges, and only the new-to-old
  edges whose two posts share a subreddit;
- *foreign only*: the same with only the new-to-old edges that cross subreddits;
- *count control*: for each existing post, a uniform random subset of its new-to-old
  arrivals of the same size as its foreign set, so every post has exactly its foreign
  count of arrivals but drawn without regard to subreddit (seed 20260913);
- *sharing control*: for each new post, a uniform random subset of its new-to-old
  edges of the same size as its foreign set, so the total and each new post's count
  match the foreign variant but the existing posts a new post touches still share it
  (seed 20260914).

New-to-new edges do not enter an existing post's first-layer vector, so on every
variant an existing post's delta is exactly what its included arrivals do to it. No
deletions, no feature or label changes.

**What was held fixed.** Weights, features, labels, the inference path (deterministic
full-graph inference on the CSR sparse path), the seed protocol. No checkpoint is
retrained or fine-tuned; the same five are run on every variant of both windows.

**What is compared.** Three measurements. *Among neighbours*: for one checkpoint and
one variant, every existing post's first-layer hidden vector on the starting graph
against the same post's on the variant graph; the difference is the post's delta. A
post is stale when it received an included arrival and its delta is non-zero (every
such post's delta was non-zero on every variant). For every existing post with two or
more stale starting-graph neighbours, three quantities over those neighbours' deltas,
as lab/015 defines them: the mean pairwise cosine (`cos`); the norm of the sum over
the sum of the norms (`R`), 1 when they all point the same way; and what `R` would be
if they were orthogonal, the root of the sum of squared norms over the sum of norms
(`R_inc`). Cells are unweighted means over posts, then the mean over five
checkpoints. *Inside a post, between the two halves*: on the first checkpoint, over
existing posts that received both kinds of arrival, the norm of the same-only delta
and of the foreign-only delta as a share of the full delta's, the cosine of the full
delta with each, and the cosine between the two, as medians by decile. *Inside a
post, among its arrivals*: the first layer's pre-activation moves by the mean over a
post's arrivals `j` of the push `W_l (x_j − m_u)`, where `W_l` is the neighbour weight
matrix, `x_j` the arriving post's features and `m_u` the mean feature of the post's
starting-graph neighbours (zero for an isolated post), over the post's new degree. For
each post the pushes of its foreign arrivals, of its same-subreddit arrivals, of all
its arrivals and of each control's subset are summed: `R_arr` is the norm of the sum
over the sum of norms and `R_inc` its orthogonal value, over posts with two or more
arrivals of the kind, by decile, mean over checkpoints; and the cosine between a
post's net same push and its net foreign push, as the median and the share below zero
over posts with an arrival of each kind.

**The noise band** for the neighbour measurement is lab/015's shuffle: within each
checkpoint the real deltas are permuted among the stale posts (seed 20260905 plus the
checkpoint's index), so each stale post keeps a real delta but some other stale
post's; `cos` and `R` on the shuffled deltas are what the delta distribution's
anisotropy produces by chance among neighbours that share nothing. For the
within-post measurement the band is `R_inc` itself, and the two controls are the
comparison for the foreign variant at the same count.

**The verifier check.** Known positive, every stale delta replaced by their common
mean: `cos` 1.0000, `R` 1.0000. Known negative, every stale delta replaced by an
independent random direction of the same norm: `cos` 0.0001, `R` 0.2286 against
`R_inc` 0.2292. The largest delta norm on a post with no included arrival was
1.1 × 10⁻⁵ on every variant, against stale deltas of order 0.1 to 3. The push
decomposition was held to the model: the mean push over the new degree reproduces the
measured pre-activation delta on every touched post with a median relative error of
1 × 10⁻⁵ (one day) and 3 × 10⁻⁶ (ten days), maximum 3 × 10⁻⁴. And the *all* variant
reproduces lab/015's growth rows to the third digit (`cos` 0.060 and 0.081, `R`
0.347 and 0.357, `R_inc` 0.230 and 0.203 for one and ten days).

## Observation

**Table 1. All existing posts with two or more stale neighbours, by variant.** `k` is
the mean stale-neighbour count, `f` the mean share of a post's neighbours that are
stale. The range of `cos` across the five checkpoints is within ±0.004 of the mean on
every row except *foreign only*, where it is within ±0.008.

| variant (ten days) | n | k | f | cos | cos, shuffled | R | R_inc | R, shuffled | R / R_inc |
|---|---|---|---|---|---|---|---|---|---|
| all | 148,758 | 71.1 | 0.98 | 0.081 | 0.003 | 0.357 | 0.203 | 0.239 | 1.76 |
| same only | 148,517 | 70.5 | 0.96 | 0.113 | 0.003 | 0.387 | 0.200 | 0.235 | 1.93 |
| foreign only | 147,192 | 55.2 | 0.73 | 0.291 | 0.031 | 0.575 | 0.245 | 0.331 | 2.35 |
| count control | 147,192 | 55.2 | 0.73 | 0.036 | 0.002 | 0.330 | 0.255 | 0.318 | 1.30 |
| sharing control | 148,003 | 65.4 | 0.88 | 0.104 | 0.012 | 0.398 | 0.224 | 0.292 | 1.78 |

| variant (one day) | n | k | f | cos | cos, shuffled | R | R_inc | R, shuffled | R / R_inc |
|---|---|---|---|---|---|---|---|---|---|
| all | 147,240 | 63.5 | 0.83 | 0.060 | 0.003 | 0.347 | 0.230 | 0.269 | 1.51 |
| same only | 146,391 | 60.9 | 0.79 | 0.084 | 0.004 | 0.382 | 0.238 | 0.275 | 1.60 |
| foreign only | 140,741 | 35.5 | 0.43 | 0.184 | 0.020 | 0.514 | 0.333 | 0.409 | 1.55 |
| count control | 140,741 | 35.5 | 0.43 | 0.046 | 0.006 | 0.400 | 0.341 | 0.403 | 1.18 |
| sharing control | 142,247 | 42.0 | 0.52 | 0.062 | 0.011 | 0.394 | 0.308 | 0.364 | 1.28 |

**Table 2. `R` / `R_inc` by degree decile on the starting graph, ten days**, with
`cos` in parentheses. Deciles hold 8,700 to 16,300 posts on every variant.

| decile (degree) | all | same only | foreign only | count control | sharing control |
|---|---|---|---|---|---|
| 0 (0–8) | 1.07 (0.069) | 1.10 (0.114) | 1.16 (0.219) | 1.02 (0.033) | 1.07 (0.087) |
| 1 (8–21) | 1.34 (0.089) | 1.42 (0.128) | 1.54 (0.273) | 1.12 (0.043) | 1.28 (0.103) |
| 2 (21–32) | 1.68 (0.097) | 1.83 (0.137) | 2.03 (0.296) | 1.22 (0.041) | 1.57 (0.109) |
| 3 (32–41) | 1.84 (0.090) | 2.06 (0.130) | 2.33 (0.293) | 1.27 (0.035) | 1.75 (0.101) |
| 4 (41–49) | 1.97 (0.089) | 2.17 (0.120) | 2.50 (0.297) | 1.31 (0.034) | 1.87 (0.099) |
| 5 (49–59) | 2.10 (0.088) | 2.28 (0.113) | 2.67 (0.318) | 1.38 (0.037) | 2.01 (0.106) |
| 6 (59–73) | 2.23 (0.087) | 2.35 (0.106) | 2.90 (0.359) | 1.50 (0.048) | 2.20 (0.127) |
| 7 (73–96) | 2.34 (0.074) | 2.56 (0.099) | 3.30 (0.328) | 1.55 (0.040) | 2.43 (0.114) |
| 8 (96–144) | 2.56 (0.067) | 3.00 (0.100) | 3.91 (0.285) | 1.55 (0.026) | 2.78 (0.097) |
| 9 (144–2502) | 2.97 (0.053) | 3.71 (0.085) | 4.84 (0.211) | 1.75 (0.019) | 3.49 (0.084) |

The shuffled `cos` is 0.002 to 0.004 on every decile of *all*, *same only* and the
count control, 0.012 on the sharing control and 0.030 to 0.032 on *foreign only*. The
one-day ordering is the same on every decile (top decile: 2.59, 2.93, 2.58, 1.54,
2.05), with *foreign only* and *all* equal in `R` / `R_inc` and apart in `cos` (0.116
against 0.047). On posts touched at two hops only under *foreign only* (57,465 posts),
the second layer's aggregated input moves 0.169 on the top decile against a coherent
bound of 0.277 and an incoherent prediction of 0.039, 4.3 times the incoherent value;
the full two-hop tables are in the run log.

**Table 3. Inside a post: the same-only and foreign-only deltas against the full
delta**, first checkpoint, ten days, medians over existing posts that received both
kinds of arrival. The last column is the norm of the full delta minus the two split
deltas, over the full delta's norm.

| decile (degree) | n | ‖d_same‖ / ‖d_all‖ | ‖d_foreign‖ / ‖d_all‖ | cos(d_all, d_same) | cos(d_all, d_foreign) | cos(d_same, d_foreign) | residual |
|---|---|---|---|---|---|---|---|
| 0 (0–8) | 1,657 | 0.87 | 0.84 | 0.83 | 0.81 | 0.25 | 0.33 |
| 1 (8–21) | 5,320 | 0.86 | 0.75 | 0.83 | 0.70 | 0.07 | 0.19 |
| 2 (21–32) | 6,944 | 0.92 | 0.70 | 0.87 | 0.59 | −0.01 | 0.18 |
| 3 (32–41) | 8,515 | 0.93 | 0.65 | 0.88 | 0.54 | −0.04 | 0.16 |
| 4 (41–49) | 7,864 | 0.94 | 0.63 | 0.89 | 0.53 | −0.06 | 0.14 |
| 5 (49–59) | 8,776 | 0.94 | 0.61 | 0.90 | 0.51 | −0.06 | 0.13 |
| 6 (59–73) | 9,038 | 0.96 | 0.60 | 0.90 | 0.49 | −0.09 | 0.13 |
| 7 (73–96) | 10,379 | 0.97 | 0.60 | 0.91 | 0.44 | −0.12 | 0.14 |
| 8 (96–144) | 12,190 | 0.99 | 0.63 | 0.90 | 0.40 | −0.17 | 0.15 |
| 9 (144–2502) | 14,381 | 1.05 | 0.97 | 0.74 | 0.41 | −0.41 | 0.20 |
| all | 85,064 | 0.96 | 0.69 | 0.87 | 0.50 | −0.12 | 0.16 |

Over one day (30,159 posts with both kinds) the same row is 0.82, 0.69, 0.78, 0.64,
−0.11 and a residual of 0.03; the top decile's cosine between the two halves is −0.18.

**Table 4. Inside a post: the alignment among its arrivals' pushes, ten days**, mean
over checkpoints, over posts with two or more arrivals of the kind. `k` is the mean
count, `‖p‖` the mean push norm per arrival.

| arrivals | decile | n | k | ‖p‖ | R_arr | R_inc | R_arr / R_inc |
|---|---|---|---|---|---|---|---|
| all | 0 (0–8) | 5,126 | 4.4 | 35.7 | 0.695 | 0.570 | 1.22 |
| all | 4 (41–49) | 13,776 | 18.0 | 31.3 | 0.345 | 0.292 | 1.18 |
| all | 9 (144–2502) | 15,408 | 116.8 | 29.9 | 0.147 | 0.116 | 1.26 |
| all | every | 135,776 | 33.4 | 31.9 | 0.332 | 0.277 | 1.20 |
| foreign | 0 (0–8) | 1,708 | 3.2 | 36.1 | 0.748 | 0.622 | 1.20 |
| foreign | 4 (41–49) | 5,911 | 6.1 | 34.4 | 0.625 | 0.505 | 1.24 |
| foreign | 9 (144–2502) | 13,814 | 46.1 | 32.0 | 0.396 | 0.249 | 1.59 |
| foreign | every | 70,089 | 15.1 | 34.4 | 0.568 | 0.437 | 1.30 |
| same | 0 (0–8) | 3,461 | 4.5 | 35.5 | 0.703 | 0.576 | 1.22 |
| same | 4 (41–49) | 13,396 | 15.6 | 30.5 | 0.380 | 0.322 | 1.18 |
| same | 9 (144–2502) | 15,403 | 75.5 | 29.1 | 0.226 | 0.144 | 1.56 |
| same | every | 129,170 | 26.7 | 30.8 | 0.360 | 0.296 | 1.22 |
| count control | 9 (144–2502) | 13,814 | 46.1 | 29.8 | 0.267 | 0.253 | 1.06 |
| count control | every | 70,089 | 15.1 | 31.3 | 0.471 | 0.441 | 1.07 |
| sharing control | 9 (144–2502) | 14,859 | 34.7 | 29.5 | 0.287 | 0.246 | 1.17 |
| sharing control | every | 98,776 | 10.7 | 30.5 | 0.500 | 0.461 | 1.08 |

**The net same push against the net foreign push**, ten days, over posts with an
arrival of each kind, mean over checkpoints: the median cosine runs +0.24, +0.08,
−0.01, −0.04, −0.05, −0.06, −0.08, −0.12, −0.17, −0.39 from the bottom decile to the
top, and the share of posts on which it is negative 0.27, 0.42, 0.51, 0.54, 0.55,
0.56, 0.58, 0.61, 0.66, 0.82; over all 85,064 posts −0.11 and 0.60. Over one day
−0.10 and 0.61 overall, −0.17 and 0.68 on the top decile, +0.13 and 0.34 on the
bottom.

## In plain terms

Nothing was refreshed. The question is whether a post's neighbours, when they change
their hidden vectors because new posts attached to them, move in the same direction so
their changes add up at the post, or in different directions so they partly cancel; and
now, which of the new posts are doing it: the ones from the post's own subreddit or the
ones from elsewhere. The table gives, for a post of each degree, how far the combined
change of its neighbours travelled over ten days of real arrivals as a percentage of
the worst case (every neighbour moving the same way), with the value independent
directions would give in parentheses. The bottom tenth of posts has degree 8 or less,
the middle fifth 41 to 59, the top tenth 144 and up.

| which arriving edges were kept | low-degree posts (bottom tenth) | median posts (middle fifth) | top decile (top tenth) |
|---|---|---|---|
| all of them (the real ten days) | 63 % (59 %) | 34 % (17 %) | 23 % (8 %) |
| only the ones from the post's own subreddit | 65 % (59 %) | 37 % (17 %) | 28 % (8 %) |
| only the ones from other subreddits | 72 % (62 %) | 57 % (22 %) | 45 % (9 %) |
| a random quarter of each post's arrivals | 65 % (63 %) | 31 % (23 %) | 17 % (10 %) |
| a random quarter of each new post's edges | 66 % (61 %) | 37 % (19 %) | 30 % (9 %) |

Either half of the stream on its own moves a post's neighbours more coherently than
the whole stream does. Keeping only the cross-subreddit arrivals moves a hub's
neighbours together at five times the independent value, and keeping only the
same-subreddit ones at three and a half times; the real stream, which is both, moves
them at three times. A random quarter of each post's arrivals, chosen without regard
to subreddit and independently per post, gives under twice the independent value at
every degree. A random quarter chosen per new post, so that the several existing
posts a new post attaches to still share it, gives what the whole stream gives.

Inside a single post the two halves push against each other. On a hub, the change its
own-subreddit arrivals would make on their own is as large as the change all its
arrivals make together, the change its foreign arrivals would make on their own is
nearly as large, and the two point 114 degrees apart; the full change is what is left
after they cancel. On four in five hubs the two net pushes have a negative cosine, on
the median post just over half, and on the lowest-degree posts they agree more often
than not.

Where refresh has something to do is therefore where one of the two halves is missing:
a burst of foreign arrivals with no same-subreddit arrivals beside it, or the reverse,
moves a post's neighbours together; the real stream brings both in each post's own
proportion and they largely undo each other.

## Interpretation

**Both halves of the real stream are coherent, and the whole is less coherent than
either.** Same-subreddit arrivals alone give `cos` 0.113 against a shuffled 0.003,
nearly forty times chance, and `R` 3.7 times `R_inc` on the top decile; the full stream
gives 0.081 and 3.0. Foreign arrivals alone give 0.291 and 4.8, with a shuffled 0.031,
ten times the other variants' chance value, because a foreign delta points away from a
community centroid and community centroids are not isotropic. lab/015's reading, that
the same-subreddit arrivals induce small deltas of random direction and the coherent
part is what the cross-subreddit share contributes, holds on the second clause and
fails on the first: a foreign arrival is the more coherent per edge, but a
same-subreddit arrival is not incoherent, and the sum of the two halves is less
aligned across neighbours than either.

**The two halves oppose each other inside a post, and the opposition grows with
degree.** Table 3 is the direct reading: on a hub the same-only delta is 1.05 of the
full delta and the foreign-only delta 0.97 of it, at a cosine of −0.41 between them,
and the net same push and net foreign push at the pre-activation are negatively aligned
on 82 percent of hubs. The mechanism is the neighbourhood mean. A post's starting-graph
neighbourhood already carries its foreign share, a quarter on a hub (lab/020), so its
mean feature sits between its home centroid and the foreign ones; an arriving
same-subreddit post pushes the mean back toward home and an arriving foreign post
pushes it away, and along that axis they cancel. lab/020 found the stream
composition-preserving, each post's arrivals foreign in the share its neighbourhood
already is, which is the condition under which the two net pushes are of the same size:
Table 4 has the net same push and the net foreign push equal within 1 percent on
average (0.360 × 26.7 × 30.8 against 0.568 × 15.1 × 34.4), from three times as many
same arrivals that are each 10 percent smaller and cancel more among themselves. On
low-degree posts the neighbourhood is small or empty, the mean is not yet a mix, and
the two pushes agree (+0.24 on the bottom decile).

**The coherence the real stream does have comes from arrivals shared among
neighbours, not from which subreddit they come from.** The two controls hold the
count at the foreign variant's and differ only in whether the existing posts a new post
attaches to still share it. Drawn per existing post, which breaks the sharing, the
quarter gives `cos` 0.036 and `R` / `R_inc` 1.30, half the real stream's; drawn per
new post, which keeps it, the same number of edges gives 0.104 and 1.78, the real
stream's 0.081 and 1.76 or above it. A new post attaches to many existing posts that
are neighbours of one another (lab/019: an arriving post's degree scales with the
graph, and lab/009: it attaches within its subreddit), and each of them receives the
same push from it. Foreignness adds on top of that, from 0.104 to 0.291 at the same
count and the same sharing, but the sharing alone reaches the stream's own value.
Within a single post the pushes of its arrivals are nearly independent whichever kind
they are (`R_arr` / `R_inc` 1.2 to 1.3 overall), and a hub's foreign arrivals are the
least aligned among themselves relative to their count (1.59 at 46 arrivals against
1.20 at 3 on the bottom decile, an implied pairwise alignment of 0.03 against 0.20),
which is lab/020's dispersal over subreddits read in the deltas.

**For the design.** The generator's coherence anchor is not the foreign share by
itself. A synthetic insertion arm that draws each existing post's new partners
independently, foreign with the neighbourhood's share, is the count control with a
foreign quarter: it would read near 0.04 to 0.1 in `cos` and reach the real stream's
`R` / `R_inc` only by accident of the foreign draws. An arm that inserts only foreign
partners at the real share is the foreign variant, at three and a half times the
stream's `cos`. What reproduces the anchor is an arrival-shaped generator: a new node
of degree scaling with the graph, attaching to a clustered set of existing posts,
foreign with each post's own neighbourhood share, so that its pushes are shared among
neighbours and its foreign and same pushes cancel inside each post as the real ones do.
That is the declaration lab/019 and lab/020 arrived at from the counts, and this note
supplies the reason it is the one that matters for coherence. The adversarial hub
constructions of lab/013 and lab/015 are one half without the other, foreign arrivals
with no same-subreddit arrivals beside them, and that, more than their size, is why
they sit at the coherent end.

## Threats

- The split deltas are on counterfactual graphs with a smaller new degree than the
  full one, so each split delta is larger than its share of the full delta, and the
  post-ReLU delta is not additive: the residual in Table 3 is 0.16 at ten days and
  0.03 at one. The cosine between the two halves does not depend on the scale.
- Table 3 is one checkpoint; the within-post rows and the neighbour tables are five.
  The two controls are one draw each.
- The count control changes which existing posts are stale on a given new post's
  edges, and the sharing control changes how many existing posts are touched
  (120,054 against 90,670); the two are read against each other and against the
  foreign variant at the same total, not against `all`.
- `R` / `R_inc` grows with the count at a fixed pairwise alignment, so a row of Table 4
  is read against the control at the same `k`, not across deciles; the implied
  pairwise values quoted assume equal norms.
- Paper edge set only; the full set's foreign share is two points higher (lab/020).
- The checkpoints are the 100-epoch recipe of lab/012 to lab/015; the delta is the
  post-ReLU first-layer vector, the quantity the second layer aggregates.

## Open

- The neighbour coherence split by whether two stale neighbours share an arriving
  post, which would read the sharing mechanism directly rather than through a control.
- The same split on arxiv, where the cross-area share of arrivals is a different
  fraction and the neighbourhood mix is not measured.
- Whether the cancellation holds at the second layer's output, where the head reads.

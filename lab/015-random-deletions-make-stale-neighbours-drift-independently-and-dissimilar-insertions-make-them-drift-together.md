# 015 — Random deletions make stale neighbours drift independently, dissimilar insertions make them drift together, and the real stream sits between, nearer the independent end

**Date:** 2026-09-05 · **Component:** refresh error model, the stream's coherence · **Status:** measured.

## What was asked

lab/007 showed on a star graph that mean-aggregation error at a fixed stale fraction has
two brackets. In the coherent one every stale neighbour's delta points the same way and
the centre's aggregated input moves by the fraction times the delta at every degree. In
the incoherent one the deltas are independent and the move falls as the square root of
fraction over degree, so a hub is safer than a leaf by the square root of their degree
ratio. Which bracket a real mutation on a real graph sits near was left unmeasured, and
lab/008's probe list carries it as mutation-induced coherence on a Reddit sample, the
mean pairwise cosine between stale neighbours' deltas per degree decile, under random
deletions and under a hot-hub burst. lab/009's sparse path fits the whole graph, so the
probe runs on the full starting graph of lab/013 and on all thirteen of lab/013's arms,
so that coherence is read on the same mutations whose no-refresh gap lab/013 measured.
Script: `lab/probe_coherence_real.py`, which imports lab/012's training recipe and
lab/013's mutation arms and reproduces their draws from the same seed. The same run
prints the checkpoints' spectral norms, which are lab/016.

## Setup

**The task** is node classification. Each post in the Reddit post graph carries a
label, the subreddit it was posted to, one of 41. The model is a two-layer GraphSAGE
with mean aggregation (602 input features → 64 → 64) and a linear head on the
64-dimensional embedding that predicts the label. A checkpoint is the GraphSAGE and
its head together, trained full-batch with cross-entropy (Adam at 0.01, 100 epochs)
on the posts the dataset marks as training, restricted to those in the starting
graph. Five checkpoints were trained, identical except for the seed
(20260903–20260907); they are lab/013's checkpoints, retrained by the same recipe in
16 s each. The head is not used in this note: the quantity measured is the change in a
post's first-layer hidden vector, the 64-dimensional vector after the ReLU that its
neighbours aggregate in the second layer, and the change in the second layer's output.
Nothing is compared to ground truth.

**The starting graph** is every post created before day 20 (posts are ordered by
creation using the dataset's post ids, and day 20 is where the published
train/validation split falls) and every edge of the paper's 11.6M-edge set whose two
endpoints are both such posts: 153,430 posts and 5,376,616 edges. 78 percent of those
edges join two posts of the same subreddit.

**The mutations** are lab/013's thirteen arms, each a single deterministic draw (seed
20260904) applied to the starting graph, reproduced here by the same code: uniform
deletion of 1, 5 and 20 percent of edges; insertion of 5 percent as many edges between
uniform random pairs of existing posts (a random pair is almost always two posts of
different subreddits); hub-burst, where the 1,534 highest-degree posts (one percent,
degree 416 and up) each gain round(f × degree) edges to uniform random existing posts of
a different subreddit, f = 0.1, 0.5 and 1.0; hub-shift, where the same hubs each lose a
Bernoulli(f) share of their same-subreddit edges and gain one edge to a uniform random
post of a different subreddit per edge lost, degree preserved, f = 0.25, 0.5 and 1.0;
and the real arrival order for 1, 3 and 10 days from day 20, which adds the posts
created in the window and the edges they bring and alters nothing in the starting
graph. The deletion, insertion and hub arms alter the starting graph's edges; no arm
changes a feature or a label.

**What was held fixed.** Weights, features, labels, the inference path (deterministic
full-graph inference on the CSR sparse path), and the seed protocol. No checkpoint is
retrained or fine-tuned; the same five are run on every graph.

**What is compared.** For one checkpoint and one arm, every existing post's first-layer
hidden vector on the starting graph against the same post's on the mutated graph; the
difference is the post's delta. A post is stale when it is an endpoint of a changed edge
and its delta is non-zero (every such post's delta was non-zero on every arm). For every
existing post v, its stale neighbours are the stale posts among its starting-graph
neighbours, and over the posts with two or more stale neighbours three quantities are
read: the mean pairwise cosine between the stale neighbours' deltas (`cos`); the norm of
the sum of the deltas over the sum of their norms (`R`), which is 1 when they all point
the same way; and what `R` would be if the deltas were orthogonal, the root of the sum
of squared norms over the sum of norms (`R_inc`), about one over the root of the stale
count for equal norms. `R` divided by `R_inc` is how many times further the sum of the
deltas travels than independent deltas of the same sizes would. Cells are all existing
posts with two or more stale neighbours, the touched strata of lab/013 (touched at one
hop, an endpoint of a changed edge; touched at two hops only, a starting-graph
neighbour of one with no changed edge of its own), the hubs in the hub arms, and degree
deciles on the starting graph. A cell is the unweighted mean over its posts, then the
mean over the five checkpoints; the range across checkpoints is reported beside `cos`.

For posts touched at two hops only, whose own neighbourhood and own hidden vector are
unchanged, the second layer's aggregated input moves by exactly the mean of the
neighbours' deltas over the starting-graph degree, and the output moves by exactly the
second layer's neighbour weight matrix times that. For those posts the note reports the
measured move of the aggregated input, the coherent bound (the sum of the neighbours'
delta norms over the degree, what the move would be if every delta pointed the same
way), the incoherent prediction (the root of the sum of squared norms over the degree),
and the realised gain, the output move over the input move, beside the spectral norm of
the second layer's neighbour matrix. The move over the coherent bound is `R` on this
stratum, so the two tables agree by construction; the second shows the size.

**The noise band** is a shuffle: within each checkpoint the real deltas are permuted
among the stale posts (seed 20260905 plus the checkpoint's index), so each stale post
keeps a real delta but some other stale post's. `cos` and `R` on the shuffled deltas are
what the delta distribution's anisotropy produces by chance among neighbours that share
nothing. It is computed in the same run on the same posts.

**The verifier check.** Known positive: every stale post's delta replaced by their
common mean; `cos` read 1.0000 and `R` read 1.0000. Known negative: every stale post's
delta replaced by an independent random direction of the same norm; `cos` read −0.0000
and `R` read 0.2702 against an `R_inc` of 0.2712. The untouched stratum is the known
negative for the delta itself: the largest delta norm on a post with no changed edge
was 1.1 × 10⁻⁵ on every arm (the sparse product rounding differently on two matrices),
against stale-post deltas of order 0.1 to 3.

## Observation

**Table 1. All existing posts with two or more stale neighbours, by arm.** `k` is the
mean stale-neighbour count, `f` the mean share of a post's neighbours that are stale.

| arm | n | k | f | cos | cos, shuffled | R | R_inc | R, shuffled |
|---|---|---|---|---|---|---|---|---|
| uniform-delete 1 % | 144,983 | 47.9 | 0.61 | 0.005 | 0.003 | 0.268 | 0.272 | 0.298 |
| uniform-delete 5 % | 148,037 | 69.2 | 0.93 | 0.002 | 0.002 | 0.211 | 0.214 | 0.247 |
| uniform-delete 20 % | 148,846 | 72.0 | 0.99 | 0.001 | 0.001 | 0.199 | 0.202 | 0.230 |
| uniform-insert 5 % | 149,065 | 70.0 | 0.97 | 0.283 | 0.064 | 0.620 | 0.247 | 0.385 |
| hub-burst 0.1 | 145,614 | 37.4 | 0.51 | 0.285 | 0.066 | 0.625 | 0.295 | 0.471 |
| hub-burst 0.5 | 149,023 | 69.0 | 0.96 | 0.372 | 0.099 | 0.684 | 0.241 | 0.427 |
| hub-burst 1.0 | 149,193 | 71.9 | 1.00 | 0.460 | 0.128 | 0.726 | 0.228 | 0.442 |
| hub-shift 0.25 | 147,209 | 54.8 | 0.71 | 0.195 | 0.025 | 0.560 | 0.277 | 0.405 |
| hub-shift 0.5 | 148,522 | 65.2 | 0.88 | 0.232 | 0.034 | 0.594 | 0.260 | 0.376 |
| hub-shift 1.0 | 149,077 | 70.7 | 0.98 | 0.296 | 0.049 | 0.640 | 0.254 | 0.364 |
| growth 1 day | 147,240 | 63.5 | 0.83 | 0.060 | 0.003 | 0.347 | 0.230 | 0.269 |
| growth 3 days | 148,297 | 69.3 | 0.94 | 0.065 | 0.002 | 0.341 | 0.211 | 0.250 |
| growth 10 days | 148,758 | 71.1 | 0.98 | 0.081 | 0.003 | 0.357 | 0.203 | 0.239 |

The range of `cos` across the five checkpoints is within ±0.001 of the mean on the
deletion and growth arms and within ±0.015 on the insertion and hub arms. The touched
strata read the same as the whole: on every arm the one-hop and two-hop-only rows are
within 0.01 of the all-posts row in `cos`, except the deletion arms where the two-hop
row is 0.004 to 0.009 against 0.000 to 0.004.

**Table 2. The hubs, in the hub arms** (1,534 posts, degree 416 and up).

| arm | k | f | cos | cos, shuffled | R | R_inc | R, shuffled |
|---|---|---|---|---|---|---|---|
| hub-burst 0.1 | 324 | 0.53 | 0.134 | 0.066 | 0.468 | 0.086 | 0.275 |
| hub-burst 0.5 | 589 | 0.95 | 0.168 | 0.099 | 0.517 | 0.069 | 0.321 |
| hub-burst 1.0 | 616 | 1.00 | 0.220 | 0.128 | 0.541 | 0.065 | 0.364 |
| hub-shift 0.25 | 538 | 0.88 | 0.063 | 0.025 | 0.365 | 0.072 | 0.211 |
| hub-shift 0.5 | 594 | 0.96 | 0.088 | 0.034 | 0.411 | 0.070 | 0.220 |
| hub-shift 1.0 | 614 | 1.00 | 0.127 | 0.049 | 0.453 | 0.071 | 0.240 |

**Table 3. `R` against `R_inc` by degree decile on the starting graph**, all existing
posts with two or more stale neighbours, six arms. Each cell is `R` / `R_inc`.

| decile (degree) | delete 5 % | insert 5 % | hub-burst 0.5 | hub-shift 0.5 | growth 1 d | growth 10 d |
|---|---|---|---|---|---|---|
| 0 (0–8) | 0.619 / 0.623 | 0.776 / 0.676 | 0.796 / 0.660 | 0.766 / 0.676 | 0.658 / 0.635 | 0.632 / 0.593 |
| 1 (8–21) | 0.366 / 0.372 | 0.650 / 0.409 | 0.700 / 0.388 | 0.639 / 0.419 | 0.467 / 0.402 | 0.450 / 0.336 |
| 2 (21–32) | 0.249 / 0.254 | 0.614 / 0.290 | 0.683 / 0.277 | 0.600 / 0.301 | 0.383 / 0.278 | 0.391 / 0.233 |
| 3 (32–41) | 0.208 / 0.211 | 0.602 / 0.245 | 0.671 / 0.237 | 0.581 / 0.260 | 0.353 / 0.228 | 0.360 / 0.195 |
| 4 (41–49) | 0.185 / 0.188 | 0.605 / 0.215 | 0.676 / 0.212 | 0.577 / 0.235 | 0.337 / 0.205 | 0.345 / 0.175 |
| 5 (49–59) | 0.165 / 0.169 | 0.619 / 0.194 | 0.690 / 0.192 | 0.591 / 0.215 | 0.327 / 0.189 | 0.338 / 0.161 |
| 6 (59–73) | 0.149 / 0.152 | 0.644 / 0.175 | 0.712 / 0.175 | 0.616 / 0.196 | 0.310 / 0.178 | 0.334 / 0.150 |
| 7 (73–96) | 0.131 / 0.135 | 0.617 / 0.159 | 0.690 / 0.160 | 0.589 / 0.179 | 0.283 / 0.151 | 0.307 / 0.131 |
| 8 (96–144) | 0.112 / 0.114 | 0.581 / 0.140 | 0.656 / 0.141 | 0.551 / 0.157 | 0.261 / 0.122 | 0.276 / 0.108 |
| 9 (144–2502) | 0.083 / 0.084 | 0.535 / 0.110 | 0.595 / 0.107 | 0.490 / 0.115 | 0.227 / 0.087 | 0.233 / 0.078 |

`cos` by decile on the insertion arm runs 0.219, 0.257, 0.270, 0.272, 0.288, 0.317,
0.362, 0.324, 0.274, 0.219 from the bottom decile to the top against a shuffled 0.064
to 0.065 on every decile; on one day of growth it runs 0.048, 0.059, 0.068, 0.070,
0.069, 0.068, 0.061, 0.053, 0.053, 0.047 against a shuffled 0.002 to 0.003. Deciles
here hold 6,600 to 16,300 posts each (the bottom decile fewer, since a post of degree
0 to 8 rarely has two stale neighbours on the mild arms).

**Table 4. The second layer's aggregated-input move on posts touched at two hops only,
by decile**, four arms with posts in every decile. `move` is measured; `coh.` is the
coherent bound and `inc.` the incoherent prediction; `n` is the cell's posts.

| decile (degree) | delete 1 %: n, move, coh., inc. | hub-burst 0.1 | hub-shift 0.25 | growth 1 d |
|---|---|---|---|---|
| 0 (0–8) | 10,148: 0.170, 0.208, 0.170 | 5,933: 0.897, 0.991, 0.850 | 5,757: 0.961, 1.096, 0.911 | 10,098: 0.406, 0.524, 0.400 |
| 1 (8–21) | 13,614: 0.094, 0.185, 0.094 | 8,579: 0.355, 0.498, 0.257 | 6,853: 0.427, 0.656, 0.314 | 9,939: 0.194, 0.426, 0.179 |
| 4 (41–49) | 9,114: 0.047, 0.182, 0.048 | 7,640: 0.206, 0.327, 0.092 | 5,373: 0.232, 0.421, 0.111 | 3,938: 0.111, 0.369, 0.080 |
| 7 (73–96) | 6,800: 0.031, 0.176, 0.032 | 8,469: 0.185, 0.287, 0.060 | 4,725: 0.221, 0.375, 0.074 | 1,942: 0.086, 0.306, 0.055 |
| 9 (144–2502) | 1,850: 0.019, 0.163, 0.019 | 7,572: 0.145, 0.267, 0.036 | 2,275: 0.152, 0.349, 0.047 | 128: 0.059, 0.253, 0.031 |

Under 5 percent uniform insertion the same row for the top decile (469 posts) is a
move of 0.415 against a coherent 0.774 and an incoherent 0.085; for the bottom decile
(401 posts) 2.41 against 2.85 and 2.17. The coherent bound itself falls with the
centre's degree on every insertion arm, from 2.85 at the bottom decile to 0.77 at the
top under uniform insertion, while the stale share `f` is 0.97 on both: a hub's
neighbours are themselves higher-degree posts, and each gains the same three or four
random edges as any post, so each moves less.

**The realised gain** of the second layer, the output move over the aggregated-input
move on posts touched at two hops only, is 0.92 to 1.07 on every decile of every arm
except three and ten days of growth, where it falls to 0.75 to 0.89 on deciles 6 to 8,
against a spectral norm of the second layer's neighbour matrix of 1.77 to 1.94 across
the five checkpoints (mean 1.850). The full per-decile output is the script's, and the
run is 607 s at 2.34 GiB peak VRAM.

## In plain terms

Nothing was refreshed. The question is: when a post's neighbours change their hidden
vectors because the graph changed around them, do those neighbours move in the same
direction, so their changes add up at the post, or in different directions, so their
changes partly cancel? The table gives, for a post of each degree, how far the
combined change of its neighbours actually travelled as a percentage of the worst case
(every neighbour moving the same way), with the value independent directions would give
in parentheses.

| what changed in the graph | low-degree posts (degree ≤ 8, the bottom tenth) | median posts (degree 41–59, the middle fifth) | top decile (degree 144+, the top tenth) | the 1,534 hubs (degree 416+, one percent) |
|---|---|---|---|---|
| delete 5 % of edges at random | 62 % (62 %) | 18 % (18 %) | 8 % (8 %) | — |
| insert 5 % edges between random pairs | 78 % (68 %) | 61 % (20 %) | 54 % (11 %) | — |
| each hub gains half its degree in foreign posts | 80 % (66 %) | 68 % (20 %) | 60 % (11 %) | 52 % (7 %) |
| each hub swaps half its own-community edges for foreign ones | 77 % (68 %) | 58 % (22 %) | 49 % (12 %) | 41 % (7 %) |
| one real day of new posts | 66 % (64 %) | 33 % (20 %) | 23 % (9 %) | — |
| ten real days of new posts | 63 % (59 %) | 34 % (17 %) | 23 % (8 %) | — |

Random deletion is the independent case to the last digit: a top-decile post's
neighbours cancel each other out and its input moves a twelfth of the worst case. Adding
dissimilar neighbours is not: the neighbours of a median post move six tenths of the
way to the worst case, three times what independence would give, and a hub's move
five to eight times. The real stream is in between and nearer the independent end: at
low degree it is indistinguishable from independence, and at the top decile it is two
and a half times the independent value and a quarter of the worst case.

Where refresh would have something to do is therefore not only where many neighbours
went stale but where they went stale the same way: a burst of foreign edges into a
community moves every post in it in one direction, and a hub sees that as a full-size
move rather than an averaged-out one.

## Interpretation

**Random deletion is the incoherent bracket, exactly.** `cos` is 0.000 to 0.009 against
a shuffled 0.001 to 0.003, `R` equals `R_inc` to the third digit on every decile, and
the aggregated-input move on two-hop-only posts equals the incoherent prediction to
within 1 percent in every cell, an eighth to a ninth of the coherent bound at the top
decile. Removing a random neighbour moves a post by the difference between that
neighbour and its neighbourhood's mean, divided by degree; over random neighbours the
direction is random, and two posts that share a centre share nothing about which of
their own neighbours they lost. lab/007's square-root-of-fraction-over-degree law is
the measured law under deletion on this graph.

**Inserting dissimilar neighbours is coherent, at six tenths of the worst case and
flat in degree.** `R` is 0.53 to 0.81 across deciles under uniform insertion and 0.60
to 0.80 under hub bursts, two to six times `R_inc`, and `cos` is 0.22 to 0.55 against
a shuffled 0.06 to 0.13. Adding a foreign post to a post's neighbourhood moves it by
the difference between the foreign post and its own neighbourhood's mean, divided by
degree; for the 78 percent of neighbours that share the centre's subreddit that mean
is nearly the same vector, so every stale neighbour's delta carries the same term with
the opposite sign, and they add. The shuffled values are well above zero on these arms
for the same reason one level up: every delta on the graph points away from a community
centroid, and community centroids are not isotropic. The hub-shift arms, which replace
rather than add, sit between the two at `R` 0.49 to 0.77.

**The real stream sits between, nearer the independent end, and its coherence grows
with degree.** One day of arrivals gives `cos` 0.05 to 0.07 against a shuffled 0.003,
twenty times chance but a fifth of the insertion arms, and `R` runs from equal to
`R_inc` on the bottom decile to 2.6 times it on the top; ten days reads the same. A new
post attaches mostly within its own subreddit (lab/009), so the delta it induces on an
existing neighbour is the difference between a typical community member and the
community mean, small and of random direction; the coherent share is what the
cross-subreddit fifth of the arriving edges contributes. This is a reading; the note
did not split the stream by edge type.

**Degree still protects a post under coherent staleness, but through its neighbours'
degrees, not through averaging.** Under uniform insertion the top decile's aggregated
input moves 0.42 against the bottom decile's 2.41 with the stale share at 0.97 on both,
a fall of six times across the deciles; but the coherent bound falls by the same
factor, because a hub's neighbours are higher-degree posts that each gain the same
handful of random edges and so each move less. The fraction law operates one hop out.
On a graph where a hub's neighbours were leaves, coherent staleness would move the hub
as far as a leaf.

**What this does to the design.** The preregistration's uniform-random stale set is
the incoherent bracket, and under deletion on this graph that is exactly what a real
mutation produces, so the restated hypothesis on the roster is tested where its
premise holds. The real growth stream is not that bracket, and a stream of dissimilar
insertions is far from it: a stream model has to declare its coherence, as lab/007
said, and this note gives the anchors the generator can be set to, `cos` of 0.00 under
random deletion, 0.06 to 0.08 under the real stream, 0.28 to 0.46 under dissimilar
insertion, with `R` on the hubs of 0.08, 0.23 and 0.47 to 0.54. Arm A's influence-mass
calculation, which propagates a stale fraction under a lazy walk, is a coherent-case
calculation and bounds the incoherent case from above by a factor that at the top
decile is eight to twelve under deletion and four under the real stream.

**What is not measured here.** A refresh policy; the band across mutation draws; the
split of the real stream's coherence by same-subreddit and cross-subreddit arrivals;
sum aggregation; the delta at the second layer's output as a coherence quantity (the
head's input), which would need a third layer to aggregate it.

## Threats

- The delta is this note's construction: the post-ReLU first-layer hidden vector, which
  is what the second layer aggregates. Under a deeper model the quantity would be the
  hidden vector at each layer below the top.
- One mutation draw per arm, as in lab/013; the shuffle is one draw per checkpoint.
- A cell is the unweighted mean over its posts; posts with fewer than two stale
  neighbours are excluded, which on the mild arms removes most of the bottom decile.
- `R` depends on the stale count, so it is read against `R_inc` in the same cell, not
  across cells.
- The two-hop-only stratum shrinks to tens of posts per decile on the strongest arms;
  Table 4 uses the four arms that keep it populated.
- The checkpoints are the 100-epoch recipe of lab/012 to lab/014, which underfits
  arxiv (lab/014) and may carry weights whose neighbour path is not the trained
  optimum's; the norms are in lab/016.

## Open

- The coherence of the real stream split by arrival type, and on arxiv, where a fifth
  of new-to-old edges cross subject areas is a different fraction.
- Whether the generator sets coherence by the mix of same-community and foreign
  partners, which this note suggests is the dial.

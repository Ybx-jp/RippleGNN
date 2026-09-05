# 017 — One percent of edges makes half of every neighbourhood stale, and at a fixed stale fraction the error still falls with degree under mean aggregation and rises under sum

**Date:** 2026-09-05 · **Component:** refresh error model, the margin · **Status:** measured.

## What was asked

lab/008's probe list ends with the uniform-stream stale-fraction distribution on
Reddit at one percent, as the pilot that sets the margin. The roster hypothesis says
that on a trained two-layer mean-aggregation GraphSAGE the embedding error at a fixed
uniform-random stale fraction of a post's neighbourhood is non-increasing in the post's
degree across degree deciles, within a margin the preregistration derives before the
run from the seed-variance floor, and increasing under sum aggregation on the same
architecture. Two things had to be measured before that margin can be written. The
first is what stale fraction a uniform edge stream actually hands each degree decile:
lab/005 left as the empirical question whether hub neighbourhoods acquire a higher
stale fraction than low-degree ones, and lab/007 added that a uniform-random stale set
is the incoherent bracket only if the stream makes it so. The second is how much the
per-decile error moves between checkpoints that differ only in seed, which on a
deterministic inference path is the only seed variance there is. The probe measures
both on the full starting graph of lab/013, with five draws of each stream instead of
lab/013's one, and with the sum-aggregation control trained beside the mean
checkpoints. Script: `lab/probe_stale_fraction.py`, which imports lab/012's training
recipe and lab/013's mutation code.

Two instrument findings came out of the known-negative check before any number was
read, and both are recorded here because they bear on earlier notes.

The first is a stratum defect. lab/011–014's scripts counted a post's one-hop-touched
neighbours with a sparse matrix–vector product in eight-bit integers, so a post with
exactly 256 or 512 such neighbours was counted as having none and placed in the
untouched stratum. lab/013 is the only affected note: 3 posts under uniform deletion at
1 percent, 3 under uniform insertion at 5 percent, 4 under hub-burst 0.5 and 1 under
hub-shift 0.25, all in the top decile; lab/011, lab/012 (day 20 and the day-25
replication) and lab/014 have none. The four arms were rerun with the count corrected:
the all-posts and hub rows reproduce at the printed precision and the untouched
stratum's drift falls to the rounding value on all four, so the drift of up to
3.6 × 10⁻⁴ that lab/013 read as the sparse product's rounding was those posts moving.
lab/013 carries a banner and the four scripts are corrected in this commit.

The second is the floor itself. lab/002 found full-graph inference bitwise
reproducible, on the edge-index gather path over a synthetic graph. On the CSR sparse
path over the Reddit graph it is not: two forward passes of one mean-aggregation
checkpoint on the same graph differ by up to 1.8 × 10⁻⁵ in a post's embedding, 2.7 × 10⁻⁷
of its norm; a sum-aggregation checkpoint by up to 0.21, 1.5 × 10⁻⁵ of its norm. The
floor of this note's measurement is that number, not zero, and the untouched stratum
reads at it.

## Setup

**The task** is node classification. Each post in the Reddit post graph carries a
label, the subreddit it was posted to, one of 41. The model is a two-layer GraphSAGE
(602 input features → 64 → 64) with a linear head on the 64-dimensional embedding
that predicts the label. A checkpoint is the GraphSAGE and its head together, trained
full-batch with cross-entropy (Adam at 0.01, 100 epochs) on the posts the dataset marks
as training, restricted to those in the starting graph. Ten checkpoints were trained:
five with mean aggregation at both layers (seeds 20260903–20260907, lab/012's recipe,
16 s each, training accuracy 0.969–0.970) and five with sum aggregation at both layers
from the same seeds (the positive control the hypothesis names, training accuracy
0.798–0.879). The head is not used in this note: the quantity measured is the change in a
post's 64-dimensional second-layer embedding, and the change in its first-layer hidden
vector. Nothing is compared to ground truth.

**The starting graph** is every post created before day 20 (posts are ordered by
creation using the dataset's post ids, and day 20 is where the published
train/validation split falls) and every edge of the paper's 11.6M-edge set whose two
endpoints are both such posts: 153,430 posts and 5,376,616 edges. Degree deciles are
on this graph; their lower edges are 0, 8, 21, 32, 41, 49, 59, 73, 96 and 144, and
the maximum degree is 2,502.

**The mutations** are two uniform edge streams, each drawn five times from the seeds
20260905–20260909 and applied to the starting graph by lab/013's code: uniform
deletion, where every edge of the starting graph is deleted independently with
probability r, at r = 0.01, 0.1 and 1 percent; and uniform insertion, where
round(r × 5,376,616) edges are added between uniform random pairs of existing posts
(a random pair is almost always two posts of different subreddits; duplicate and
self pairs are dropped), at r = 0.1 and 1 percent. One percent is the setting lab/008
named; the smaller rates show how the quantities scale with the rate. No post is
added or removed, and no feature or label changes. Both streams alter the starting
graph's edges, which is the point: they are the streams under which a post's
neighbours go stale for reasons unrelated to the post.

**What was held fixed.** Weights, features, labels, the inference path (deterministic
full-graph inference on the CSR sparse path) and the seed protocol. No checkpoint is
retrained or fine-tuned; the same ten are run on every mutated graph.

**What is compared.** For one checkpoint and one draw, every existing post's
embedding on the starting graph, which is what the post keeps under no refresh,
against the same checkpoint's embedding of the post on the mutated graph, the full
recompute. The error is the L2 distance between the two, reported also relative to
the norm of the recomputed embedding. A post is stale when it is an endpoint of a
changed edge and its first-layer hidden vector (after the ReLU, the vector its
neighbours aggregate) differs between the two graphs. A post's stale fraction is the
share of its starting-graph neighbours that are stale. Three strata: touched at one
hop (the post is itself an endpoint of a changed edge, so its own neighbourhood
changed); touched at two hops only (its own edges are unchanged and at least one
neighbour is stale, so its error is purely its neighbours' staleness, the quantity the
hypothesis is about); untouched (beyond two hops). Cells are these strata by degree
decile; a cell's error is the median over its posts, pooled over the five draws and
the five checkpoints of an aggregation, and the margin candidate is the spread across
the five checkpoints of the top-decile median minus the bottom-decile median, each
checkpoint's median pooled over draws.

**The noise band.** Full-graph inference on this path is bitwise reproducible
(lab/002), so the floor of the error itself is zero and a post beyond two hops of any
change must read exactly zero; what varies is the checkpoint, and the across-seed
spread of a decile's median is the only seed variance the measurement has. It is read
in the same run.

**The verifier check.** Known negative: the largest error on any untouched post,
over every draw, checkpoint and aggregation, was 2.3 × 10⁻⁵ under mean aggregation, 2.9 × 10⁻⁷ of the embedding norm, and 0.25 under sum, 6.3 × 10⁻⁵ of the norm: the same-graph-twice rounding above, so the strata are correctly drawn and a nonzero error is attributable to the mutation. Known positive for the
stale-fraction instrument: its analytic expectation. Under deletion at rate r a
neighbour of degree d is touched with probability 1 − (1 − r)^d, so a post's expected
stale fraction is the mean of that over its neighbours; under insertion of m edges
among n existing posts every post is touched with probability 1 − (1 − 2/n)^m
whatever its degree. The realised decile means are printed beside these expectations
and agree to 0.002 on every decile of every stream. The sum-aggregation arm is the known positive for the error
instrument: the hypothesis predicts it rises with degree, and it does.

## Observation

Peak VRAM 2.93 GiB; 497 s for the grid, 160 s of it training; 41–46 s per deletion arm
and 82–118 s per insertion arm (the deduplication of inserted pairs is on the CPU).
Training accuracy 0.969–0.972 (mean) and 0.798–0.879 (sum). A checkpoint retrained by
the same recipe is not the same checkpoint: the sparse backward is not deterministic,
and across three runs of this grid the cell medians below moved in the third or fourth
significant digit. The numbers are from the last run.

**Table 1. Who is touched.** Shares of the 153,430 existing posts, mean over five
draws. The exact two-hop set is everything but the untouched stratum.

| stream | changed edges | touched at one hop | two hops only | untouched |
|---|---|---|---|---|
| delete 0.01 % | 516–558 | 0.007 | 0.472 | 0.521 |
| delete 0.1 % | 5,343–5,421 | 0.065 | 0.827 | 0.108 |
| delete 1 % | 53,362–53,805 | 0.409 | 0.563 | 0.028 |
| insert 0.1 % | 5,373–5,377 | 0.068 | 0.793 | 0.140 |
| insert 1 % | 53,738–53,749 | 0.504 | 0.484 | 0.013 |

**Table 2. The stale fraction by degree decile.** For each decile (lower degree
bound in brackets; each decile is 14,300–16,300 posts), the mean stale fraction over
the decile's posts, pooled over draws, and in brackets the share of the decile touched
at one hop. The analytic expectation is within 0.002 of every mean entry and is not
repeated. Deletion's stale fraction rises with degree, because a neighbour is touched
with probability 1 − (1 − r)^degree and a hub's neighbours are high-degree posts;
insertion's is flat at 1 − (1 − 2/n)^m by construction.

| decile | delete 0.01 % | delete 0.1 % | delete 1 % | insert 0.1 % | insert 1 % |
|---|---|---|---|---|---|
| 0 (0) | 0.015 (0.000) | 0.120 (0.003) | 0.452 (0.031) | 0.061 (0.067) | 0.446 (0.505) |
| 1 (8) | 0.014 (0.002) | 0.124 (0.014) | 0.522 (0.128) | 0.067 (0.066) | 0.503 (0.503) |
| 2 (21) | 0.015 (0.003) | 0.129 (0.026) | 0.560 (0.230) | 0.068 (0.068) | 0.504 (0.503) |
| 3 (32) | 0.014 (0.004) | 0.126 (0.035) | 0.573 (0.302) | 0.068 (0.067) | 0.505 (0.503) |
| 4 (41) | 0.013 (0.004) | 0.118 (0.043) | 0.567 (0.359) | 0.068 (0.068) | 0.505 (0.504) |
| 5 (49) | 0.013 (0.005) | 0.115 (0.053) | 0.571 (0.414) | 0.067 (0.067) | 0.504 (0.503) |
| 6 (59) | 0.013 (0.007) | 0.115 (0.063) | 0.585 (0.479) | 0.067 (0.068) | 0.503 (0.502) |
| 7 (73) | 0.015 (0.008) | 0.129 (0.080) | 0.622 (0.563) | 0.068 (0.067) | 0.505 (0.504) |
| 8 (96) | 0.016 (0.011) | 0.146 (0.108) | 0.665 (0.681) | 0.068 (0.069) | 0.504 (0.506) |
| 9 (144) | 0.020 (0.025) | 0.171 (0.221) | 0.704 (0.877) | 0.068 (0.068) | 0.504 (0.505) |

The median stale count on two-hop-only posts runs from 2 on the bottom decile to 123 on
the top under deletion at 1 percent and from 2 to 103 under insertion at 1 percent: the
count rises fiftyfold across deciles while the fraction rises by half or not at all.
The interquartile range of the fraction narrows with degree on every stream (insertion
at 1 percent: 0.00–0.67 on decile 0, 0.48–0.53 on decile 9).

**Table 3. Median L2 error of a two-hop-only post, by decile.** The post's own edges
are unchanged; the error is its neighbours' staleness alone. Pooled over five draws
and five checkpoints of the aggregation. The across-checkpoint range of a decile's
median is ±3–4 percent of its value under mean aggregation (decile 9, delete 1 %:
0.0184–0.0195; decile 0: 0.0982–0.1062) and ±30–40 percent under sum (decile 9,
delete 1 %: 224–456).

| decile | mean, del 0.01 % | mean, del 0.1 % | mean, del 1 % | mean, ins 0.1 % | mean, ins 1 % | sum, del 1 % | sum, ins 1 % |
|---|---|---|---|---|---|---|---|
| 0 | 0.0133 | 0.0224 | 0.1024 | 0.1210 | 0.3504 | 11.9 | 14.0 |
| 1 | 0.0054 | 0.0134 | 0.0734 | 0.0474 | 0.2660 | 32.4 | 34.3 |
| 2 | 0.0035 | 0.0115 | 0.0571 | 0.0290 | 0.1910 | 59.6 | 50.3 |
| 3 | 0.0030 | 0.0109 | 0.0494 | 0.0238 | 0.1639 | 83.2 | 61.5 |
| 4 | 0.0030 | 0.0107 | 0.0448 | 0.0223 | 0.1569 | 112 | 73.3 |
| 5 | 0.0029 | 0.0101 | 0.0403 | 0.0209 | 0.1525 | 150 | 84.2 |
| 6 | 0.0025 | 0.0090 | 0.0349 | 0.0192 | 0.1452 | 207 | 97.1 |
| 7 | 0.0021 | 0.0081 | 0.0301 | 0.0162 | 0.1215 | 239 | 102 |
| 8 | 0.0016 | 0.0069 | 0.0250 | 0.0131 | 0.0991 | 273 | 107 |
| 9 | 0.0011 | 0.0050 | 0.0189 | 0.0104 | 0.0808 | 289 | 112 |
| top / bottom | 0.085 | 0.223 | 0.185 | 0.086 | 0.231 | 25.3 | 8.02 |

The top-minus-bottom difference of the median, each checkpoint's median pooled over
its five draws, with the 95 percent t interval across the five checkpoints, mean
aggregation: −0.0122 [−0.0126, −0.0117] at delete 0.01 %, −0.0174 [−0.0183, −0.0165]
at delete 0.1 %, −0.0836 [−0.0868, −0.0803] at delete 1 %, −0.1105 [−0.1152, −0.1059]
at insert 0.1 %, −0.2696 [−0.2829, −0.2564] at insert 1 %; the top/bottom ratio's range
across checkpoints is 0.084–0.086, 0.218–0.226, 0.183–0.188, 0.083–0.088 and
0.221–0.241. Sum aggregation: +5.9 [+4.6, +7.3], +38.4 [+26.5, +50.2], +295 [+177,
+413], +23.3 [+19.0, +27.5], +98.2 [+82.3, +114.1]; ratio ranges 2.79–3.56, 9.42–10.86,
22.9–28.3, 3.76–4.08, 7.62–8.54. The mean/sum ratio of the top decile's median is
0.0001 on the deletion arms and 0.0003–0.0007 on the insertion arms; on the bottom
decile 0.005–0.025.

Relative to the embedding's norm the picture differs for sum aggregation: the relative
error of a two-hop-only post falls with degree under both aggregations, 0.0032 → 0.0007
(mean) and 0.0205 → 0.0103 (sum) at delete 1 %, 0.0101 → 0.0031 and 0.0246 → 0.0036 at
insert 1 %, because a sum-aggregation embedding's norm grows with degree faster than its
error does.

On all existing posts of a decile (touched posts included) the mean-aggregation median
is not monotone under deletion at 1 percent, 0.068 on decile 0, 0.062 on deciles 4–5,
0.181 on decile 7 and 0.136 on decile 9, because the share of the decile touched at one
hop rises from 3 to 88 percent (Table 2) and a one-hop post's median error is 5.2 on
decile 0 and 0.148 on decile 9. Under insertion at 1 percent, where the touched share
is 50 percent at every degree, the all-posts median falls monotonically, 4.19 → 0.135,
ratio 0.032.

**Table 4. At a fixed stale fraction.** Median mean-aggregation error of two-hop-only
posts whose stale fraction falls in the row's bin, by decile; cells with fewer than
twenty posts omitted. Delete 1 % above, insert 1 % below.

| stale fraction | d0 | d1 | d2 | d3 | d4 | d5 | d6 | d7 | d8 | d9 |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.05–0.20 | 0.048 | 0.043 | 0.044 | 0.035 | 0.033 | – | – | – | – | – |
| 0.20–0.50 | 0.080 | 0.073 | 0.061 | 0.052 | 0.046 | 0.041 | 0.035 | 0.030 | 0.027 | 0.022 |
| 0.50–0.80 | 0.104 | 0.079 | 0.058 | 0.050 | 0.045 | 0.041 | 0.035 | 0.031 | 0.025 | 0.019 |
| 0.80–1.00 | 0.130 | 0.062 | 0.043 | 0.038 | 0.034 | 0.031 | 0.028 | 0.024 | 0.021 | 0.016 |
| 0.05–0.20 | 0.098 | 0.082 | 0.076 | – | – | – | – | – | – | – |
| 0.20–0.50 | 0.204 | 0.210 | 0.162 | 0.143 | 0.138 | 0.137 | 0.131 | 0.111 | 0.091 | 0.076 |
| 0.50–0.80 | 0.376 | 0.315 | 0.218 | 0.182 | 0.173 | 0.166 | 0.158 | 0.130 | 0.106 | 0.085 |
| 0.80–1.00 | 0.584 | 0.484 | 0.350 | – | – | – | – | – | – | – |

Within a bin the median falls with degree on every row that spans the deciles
(0.50–0.80: ratio 0.18 under deletion, 0.23 under insertion); within a decile it rises
with the fraction (decile 0 under deletion: 0.048, 0.080, 0.104, 0.130 across the four
bins). At insert 0.1 %, where the fraction is 0.068 everywhere, the 0.05–0.20 row runs
0.073 → 0.011, ratio 0.15.

**Table 5. The tolerance-invalidation set.** Share of existing posts whose relative
error exceeds τ, mean aggregation, and in brackets the same as a share of the exact
two-hop set.

| stream | τ = 10⁻⁴ | τ = 10⁻³ | τ = 10⁻² | τ = 10⁻¹ | exact set |
|---|---|---|---|---|---|
| delete 0.01 % | 0.167 (0.35) | 0.012 (0.026) | 0.002 (0.005) | 0.000 | 0.479 |
| delete 0.1 % | 0.802 (0.90) | 0.124 (0.14) | 0.022 (0.025) | 0.000 | 0.892 |
| delete 1 % | 0.971 (1.00) | 0.806 (0.83) | 0.214 (0.22) | 0.004 (0.004) | 0.972 |
| insert 0.1 % | 0.833 (0.97) | 0.264 (0.31) | 0.066 (0.076) | 0.010 (0.011) | 0.860 |
| insert 1 % | 0.987 (1.00) | 0.983 (1.00) | 0.514 (0.52) | 0.086 (0.087) | 0.987 |

At ten times the measured relative floor (τ = 1.8–2.9 × 10⁻⁶ under mean aggregation)
the set is 0.995–1.000 of the exact two-hop set on every arm; under sum aggregation
(τ = 3.6 × 10⁻⁵ to 6.3 × 10⁻⁴) it is 0.33 at delete 0.01 %, 0.81 at insert 0.1 % and
0.96–0.99 on the other three.

## In plain terms

Nothing was refreshed here; the numbers are what a post's stored embedding is wrong
by if the graph changes and the embedding is not recomputed. Deleting one edge in a
hundred at random leaves 41 percent of posts with a changed edge of their own and a
further 56 percent with a changed neighbour, and the typical post has 57 percent of
its neighbours stale; adding one edge in a hundred at random touches half of all posts
and makes half of every post's neighbours stale at every degree. The staleness a
uniform stream at one percent produces is not one percent of anything.

For a post whose own edges are intact, the error from its neighbours' staleness is
5 to 12 times smaller on the highest-degree tenth of posts than on the lowest, at the
same rate and at the same stale fraction, under the mean-aggregation model. Under the
sum-aggregation model it is 3 to 25 times larger on the highest tenth. Relative to how
large the embeddings are, a hub's error is under a tenth of a percent under mean and
about one percent under sum at one percent deletion, against a third of a percent and
two percent for the lowest tenth.

## Interpretation

**A uniform edge stream does not hand every degree the same stale fraction, and the
two uniform streams differ in which way.** Under deletion the probability that a
neighbour is stale is one minus (1 − r) to its degree, so a hub, whose neighbours are
high-degree posts (lab/015), gets a higher stale fraction than a leaf: 0.70 against 0.45
at one percent. Under insertion between uniform pairs every post is touched with the
same probability whatever its degree, so the fraction is flat to three digits. The
hypothesis's condition, a uniform-random stale set at one fixed fraction, is realised
on a real graph by uniform insertion and not by uniform deletion, and lab/015 found
insertion's deltas coherent and deletion's incoherent. The stream that gives the
fraction the hypothesis asks for is the one whose staleness is not the incoherent case
its Warrant assumes.

**At a fixed stale fraction the median error of a mean-aggregation post falls with
degree on both streams, and rises with degree under sum.** This is the hypothesis's
statement, measured in pilot form on the same graph and recipe the preregistration
would use. The falsifier was the top decile exceeding the bottom by more than the
margin under mean, or failing to exceed it under sum; the top decile is a fifth to a
twelfth of the bottom under mean and 3 to 25 times it under sum, and the sign is the
same on every checkpoint, every draw and every fraction bin with twenty posts. The size
of the fall, a factor of 4 to 12 across the deciles, is at or below what the incoherent
bracket's inverse square root of the degree ratio would give (lab/007). On the
insertion arms lab/015 found the deltas coherent, and the coherent bracket alone would
be flat at fixed fraction; the fall is there because the coherent bound itself falls
with degree, a hub's neighbours each moving less (lab/015), and that is the mechanism
that survives here.

**The margin the hypothesis asked for is small against the effect.** The seed variance
of a decile's median under mean aggregation is ±3–4 percent of its value; the
top-minus-bottom difference's 95 percent interval is a tenth of the difference wide.
A margin derived from it would be of order 0.003 to 0.01 in L2, and the predicted
direction clears it by an order of magnitude. Under sum aggregation the seed variance
is ±30–40 percent, so the sum control's margin is wide but its effect is wider.

**Which normalisation the preregistration fixes decides the sum control's direction.**
In absolute L2, the metric the hypothesis names, sum-aggregation error rises with degree.
Relative to the embedding norm it falls under sum as well as mean, because a sum
embedding's norm grows with degree. A preregistration that writes relative error will
lose its positive control; one that writes absolute L2 keeps it and must say why
absolute is the quantity a downstream consumer cares about.

**The tolerance-invalidation prediction is decided by the floor, and the floor is not
what it was stated against.** The modelling consultation predicted that the set of
posts moving by more than ten times the deterministic-inference floor would be under
five percent of the exact two-hop set under a uniform stream. On the CSR path the
floor is 2–3 × 10⁻⁷ of the embedding norm and ten times it is exceeded by essentially
every post the exact set contains, at every rate down to five hundred deleted edges. A
tolerance that separates anything has to be set by the consumer, not by the floor: at
one percent of the norm the set is a fifth of the exact set under deletion at one
percent and half under insertion, and at ten percent it is under one percent and nine
percent.

**Count and fraction come apart as lab/005 said they would.** The median stale count
on a two-hop post rises fiftyfold across the deciles while the fraction rises by half
or not at all, and the error follows neither: it falls. A count-based invalidation
ranks the hubs as most endangered; they are the safest per post at both fixed rate and
fixed fraction.

**What the pilot does to the preregistration.** The hypothesis's measurement has now
been run on the Reddit day-20 snapshot with this recipe, so a preregistration of it on
the same snapshot is not blind. It can pin a different snapshot (day 25, or the full
graph with the growth stream as the insertion arm), pin saved checkpoints rather than a
recipe, since the recipe does not reproduce a checkpoint bitwise, and state this pilot
as its prior. The margin and the floor it derives are this note's numbers.

## Threats

- The stale fraction is over the starting-graph neighbourhood; under insertion the
  inserted neighbours are extra and not in the denominator.
- Two-hop-only posts are the population where the error is purely neighbour
  staleness, and under deletion at one percent that stratum is 12 percent of the top
  decile and 68 percent of the bottom. The all-posts median mixes in the one-hop
  posts, whose error is the post's own edge change, and is not monotone under
  deletion for that reason.
- The stale-fraction bins pool draws and checkpoints, and a decile's posts within a
  bin are not a random sample of the decile: under deletion a post in the 0.80–1.00
  bin is one whose neighbours are high-degree.
- Five draws per stream, one starting snapshot, one recipe at 100 epochs; the sum
  checkpoints reach 80–88 percent training accuracy and their spread across seeds is
  ten times the mean checkpoints'.
- The medians are pooled; the t interval is over five checkpoint medians and treats
  the draws as fixed.

## Open

- Whether the preregistration measures the hypothesis on a fresh snapshot, and which
  normalisation it writes.
- The stale-fraction distribution under the calibrated generator, which waits on the
  modelling ruling; the uniform streams are the null and the flattering envelope of
  lab/008's ranking, not the hot-hub stream it ranks first.
- The per-post floor on the CSR path is a property of the sparse kernel and the
  matrix's shape; it is measured here for two graphs of one size and should be
  measured again on whatever graph the preregistration pins.

Raw probe: `lab/probe_stale_fraction.py [stream:rate ...]`.

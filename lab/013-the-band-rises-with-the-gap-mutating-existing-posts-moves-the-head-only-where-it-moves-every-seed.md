# 013 — The band rises with the gap: mutating existing posts moves the head only where it moves every seed

**Date:** 2026-09-04 · **Component:** experiment design, the margin denominator · **Status:** measured.

## What was asked

lab/012 ran the gap pilot on the real growth stream, which only adds posts and their
edges and is the least adversarial stream in lab/008's ranking, and found the head's
gap inside the seed band on nine deciles of ten. The operator's objection was that
the pilot had not created a condition under which a refresh is expected to matter.
This note runs the same pilot, on the same five checkpoints, at the adversarial end:
mutations that change the existing graph, coherent and hub-concentrated ones among
them, and the real stream at three and ten days. The question is whether the
behavioural arm has headroom anywhere on this dataset under this head, and if so
where. Script: `lab/probe_gap_adversarial.py`, importing lab/012's helpers.

## Setup

**The task** is node classification. Each post in the Reddit post graph carries a
label, the subreddit it was posted to, one of 41. The model is a two-layer GraphSAGE
with mean aggregation (602 input features → 64 → 64) and a linear head on the
64-dimensional embedding that predicts the label. A checkpoint is the GraphSAGE and
its head together, trained full-batch with cross-entropy (Adam at 0.01, 100 epochs)
on the posts the dataset marks as training, restricted to those in the starting
graph. Five checkpoints were trained, identical except for the seed
(20260903–20260907), scoring 96.9 to 97.2 percent on their training posts. They are
the checkpoints of lab/012, retrained by the same recipe. No link prediction is run.

**The starting graph** is every post created before day 20 (posts are ordered by
creation using the dataset's post ids, and day 20 is where the published
train/validation split falls) and every edge of the paper's 11.6M-edge set whose two
endpoints are both such posts: 153,430 posts and 5,376,616 edges. 78 percent of those
edges join two posts of the same subreddit.

**The mutations.** Thirteen arms, each a single deterministic draw (seed 20260904)
applied to the starting graph. Nothing else changes in any arm: features and labels
are fixed, no checkpoint is retrained or fine-tuned, and the same five checkpoints
are run on every graph.

- *uniform-delete f*: a uniform random fraction f of all edges is deleted, f = 1, 5
  and 20 percent. Incoherent, degree-neutral: the deleted neighbours are as similar to
  the post as the ones that remain.
- *uniform-insert f*: f × 5.38M edges are added between uniform random pairs of
  existing posts, f = 5 percent. A random pair is almost always two posts of
  different subreddits, so every added neighbour is dissimilar.
- *hub-burst f*: the 1,534 highest-degree posts (one percent of the graph, degree 416
  and up) each receive round(f × degree) new edges to uniform random existing posts
  of a different subreddit, f = 0.1, 0.5 and 1.0. The hub's neighbourhood is diluted
  by dissimilar posts, up to half of it at f = 1. The random partners are mostly
  low-degree posts, each of which gains one dissimilar hub as a neighbour.
- *hub-shift f*: the same hubs each lose a Bernoulli(f) share of their edges to
  same-subreddit neighbours, and each lost edge is replaced by an edge to a uniform
  random existing post of a different subreddit, f = 0.25, 0.5 and 1.0. Degree is
  preserved and the hub's community is replaced rather than diluted; at f = 1 the hub
  keeps no same-subreddit neighbour it had. The coherent, hub-concentrated corner.
- *growth d*: the real arrival order for d days from day 20, d = 1, 3 and 10, adding
  the posts created in the window and the edges they bring, with nothing in the
  starting graph altered. Day 20 plus 10 days is the end of the dataset. The one-day
  arm is lab/012's episode, rerun here as the anchor.

**What is compared.** For one checkpoint, the embeddings of the existing posts
computed on the starting graph, which is what those posts keep if nothing is
refreshed, against the embeddings of the same posts computed on the mutated graph,
the full recompute. Four quantities per existing post: whether the head's predicted
label differs between the two, one minus the overlap of the post's twenty nearest
cosine neighbours among existing posts in the two embeddings, one minus the cosine
between the two embeddings, and the relative L2 change. This is the gap. Posts that
arrive in the growth arms have no starting-graph embedding and enter no figure.
Disagreement is between two predictions of one checkpoint, not against ground truth.

**The band** is a different comparison on the same posts and the same run: two
checkpoints that differ only in seed, both run on the mutated graph, on the same
quantities, averaged over the ten pairs of five seeds. It is how far two full
recomputes of the mutated graph disagree for no reason but the seed.

**Cells and the rule.** Existing posts are grouped as targets (the hubs in the hub
arms; the endpoints of changed edges otherwise), touched at one hop (an endpoint of a
deleted, added or rewired edge), touched at two hops only (a starting-graph
neighbour of a one-hop post), and untouched; and by degree decile on the starting
graph, so the hubs are the same posts in every arm. Each gap cell reports the mean
over the five seeds and the lower limit of a 95 percent t interval; a cell is
eligible when that limit exceeds the band. The untouched stratum is the known
negative: a post with no changed edge within two hops has the same two-hop
neighbourhood on both graphs and so the same two-layer output. Its measured cosine
drift is at most 2.4 × 10⁻⁷ on nine arms and up to 3.6 × 10⁻⁴ on the three arms
that leave fewer than a hundred posts untouched, which is the sparse matrix product
rounding differently on two matrices of different shape and is the working floor.

## Observation

Peak VRAM 6.0 GiB; 544 s for the grid, 31 to 39 s per arm after 80 s of training.

The gap on all existing posts against the band, mean aggregation:

| arm | what changed | touched 1-hop | untouched | gap: disagreement | band | gap: kNN@20 loss | relative L2 |
|---|---|---|---|---|---|---|---|
| uniform-delete 0.01 | 54,259 edges deleted | 63,312 | 4,230 | 0.0011 | 0.0203 | 0.046 | 0.008 |
| uniform-delete 0.05 | 269,031 edges deleted | 123,204 | 2,371 | 0.0042 | 0.0209 | 0.118 | 0.026 |
| uniform-delete 0.2 | 1,076,115 edges deleted | 144,229 | 1,935 | 0.0124 | 0.0240 | 0.261 | 0.069 |
| uniform-insert 0.05 | 268,705 edges inserted | 148,823 | 61 | 0.0346 | 0.0390 | 0.284 | 0.139 |
| hub-burst 0.1 | 94,469 edges added to 1,534 hubs | 71,496 | 2,055 | 0.0106 | 0.0242 | 0.102 | 0.038 |
| hub-burst 0.5 | 471,934 edges added | 146,471 | 85 | 0.0279 | 0.0346 | 0.237 | 0.128 |
| hub-burst 1 | 942,552 edges added | 153,117 | 4 | 0.0396 | 0.0432 | 0.317 | 0.203 |
| hub-shift 0.25 | 104,469 same-subreddit edges rewired | 100,212 | 1,423 | 0.0128 | 0.0255 | 0.127 | 0.046 |
| hub-shift 0.5 | 207,533 rewired | 130,833 | 517 | 0.0204 | 0.0298 | 0.183 | 0.078 |
| hub-shift 1 | 408,022 rewired | 148,630 | 107 | 0.0323 | 0.0372 | 0.250 | 0.126 |
| growth 1 | 546,352 arriving edges, 8,625 new posts | 105,172 | 2,688 | 0.0035 | 0.0203 | 0.114 | 0.024 |
| growth 3 | 1,649,531 arriving, 23,736 new | 129,871 | 1,905 | 0.0073 | 0.0204 | 0.191 | 0.045 |
| growth 10 | 6,159,015 arriving, 78,491 new | 142,158 | 1,213 | 0.0144 | 0.0209 | 0.308 | 0.082 |

The hubs and the bottom decile, per arm (the targets row is the 1,534 hubs; decile 9
is the top 10 percent by starting-graph degree, 144 and up; decile 0 is degree 0 to 8):

| arm | cell | n | gap: disagreement | lower limit | band | clears | gap: kNN@20 loss | cosine drift | relative L2 |
|---|---|---|---|---|---|---|---|---|---|
| uniform-delete 0.01 | decile 9 | 15,410 | 0.0003 | 0.0001 | 0.0082 | no | 0.037 | 0.0000 | 0.006 |
| uniform-delete 0.01 | decile 0, touched | 459 | 0.0898 | 0.0820 | 0.0989 | no | 0.430 | 0.0362 | 0.256 |
| uniform-delete 0.05 | decile 9 | 15,410 | 0.0007 | 0.0004 | 0.0082 | no | 0.084 | 0.0001 | 0.014 |
| uniform-delete 0.05 | decile 0, touched | 2,160 | 0.1099 | 0.1044 | 0.1006 | yes | 0.480 | 0.0482 | 0.319 |
| uniform-delete 0.2 | decile 9 | 15,410 | 0.0015 | 0.0009 | 0.0085 | no | 0.176 | 0.0005 | 0.032 |
| uniform-delete 0.2 | decile 0, touched | 6,620 | 0.1413 | 0.1395 | 0.1266 | yes | 0.592 | 0.0658 | 0.393 |
| uniform-insert 0.05 | decile 9 | 15,410 | 0.0009 | 0.0006 | 0.0090 | no | 0.118 | 0.0002 | 0.027 |
| uniform-insert 0.05 | decile 0 | 14,763 | 0.2778 | 0.2720 | 0.2452 | yes | 0.803 | 0.1581 | 0.628 |
| hub-burst 0.1 | hubs | 1,534 | 0.0066 | 0.0048 | 0.0357 | no | 0.110 | 0.0012 | 0.072 |
| hub-burst 0.1 | decile 0, touched | 6,782 | 0.1938 | 0.1884 | 0.1696 | yes | 0.612 | 0.0894 | 0.422 |
| hub-burst 0.5 | hubs | 1,534 | 0.0503 | 0.0468 | 0.0771 | no | 0.355 | 0.0168 | 0.286 |
| hub-burst 0.5 | decile 9 | 15,410 | 0.0057 | 0.0053 | 0.0135 | no | 0.133 | 0.0019 | 0.055 |
| hub-burst 0.5 | decile 0 | 14,763 | 0.2201 | 0.2164 | 0.2043 | yes | 0.726 | 0.1058 | 0.570 |
| hub-burst 1 | hubs | 1,534 | 0.1248 | 0.1140 | 0.1402 | no | 0.534 | 0.0425 | 0.463 |
| hub-burst 1 | decile 9 | 15,410 | 0.0140 | 0.0129 | 0.0207 | no | 0.189 | 0.0048 | 0.094 |
| hub-burst 1 | decile 0 | 14,763 | 0.2736 | 0.2720 | 0.2412 | yes | 0.835 | 0.1390 | 0.759 |
| hub-shift 0.25 | hubs | 1,534 | 0.0248 | 0.0217 | 0.0537 | no | 0.210 | 0.0046 | 0.142 |
| hub-shift 0.25 | decile 0, touched | 7,585 | 0.2018 | 0.1943 | 0.1741 | yes | 0.622 | 0.0900 | 0.427 |
| hub-shift 0.5 | hubs | 1,534 | 0.1082 | 0.0940 | 0.1128 | no | 0.409 | 0.0216 | 0.313 |
| hub-shift 0.5 | decile 9 | 15,410 | 0.0115 | 0.0101 | 0.0171 | no | 0.129 | 0.0023 | 0.049 |
| hub-shift 0.5 | decile 0, touched | 11,281 | 0.2049 | 0.2022 | 0.1861 | yes | 0.666 | 0.0958 | 0.478 |
| hub-shift 1 | hubs | 1,534 | 0.5274 | 0.5170 | 0.3317 | yes | 0.688 | 0.1304 | 0.744 |
| hub-shift 1 | decile 9 | 15,410 | 0.0540 | 0.0529 | 0.0392 | yes | 0.190 | 0.0133 | 0.103 |
| hub-shift 1 | decile 0 | 14,763 | 0.2080 | 0.2038 | 0.2015 | yes | 0.710 | 0.1000 | 0.544 |
| growth 1 | decile 9 | 15,410 | 0.0007 | 0.0004 | 0.0084 | no | 0.082 | 0.0001 | 0.016 |
| growth 1 | decile 0, touched | 2,008 | 0.0970 | 0.0954 | 0.0761 | yes | 0.490 | 0.0470 | 0.248 |
| growth 3 | decile 9 | 15,410 | 0.0012 | 0.0008 | 0.0087 | no | 0.133 | 0.0004 | 0.026 |
| growth 3 | decile 0, touched | 4,462 | 0.1062 | 0.1042 | 0.0824 | yes | 0.535 | 0.0541 | 0.274 |
| growth 10 | decile 9 | 15,410 | 0.0021 | 0.0015 | 0.0089 | no | 0.210 | 0.0010 | 0.045 |
| growth 10 | decile 0, touched | 8,322 | 0.1279 | 0.1252 | 0.0924 | yes | 0.630 | 0.0687 | 0.329 |

Eligible cells per arm, out of the 25 populated (five strata, ten deciles, ten
touched deciles): none at uniform-delete 1 percent; one, the bottom decile's touched
posts, on nine arms; two, the bottom decile and its touched posts, at uniform-insert
5 percent and hub-burst 0.5 and 1; five at hub-shift 1: the hubs, the top decile, its
touched posts, the bottom decile and its touched posts. The band on the hubs rises
with the mutation: 0.008 on the starting graph and under the growth arms, 0.036,
0.077 and 0.140 under hub-burst at 0.1, 0.5 and 1, 0.054, 0.113 and 0.332 under
hub-shift. The kNN@20 seed band stays at 0.75 to 0.86 on every cell and every arm;
the kNN@20 gap ranges from 0.037 (top decile, uniform-delete 1 percent) to 0.836
(bottom decile, hub-burst 1), with 0.53 on the hubs under hub-burst 1 and 0.69 under
hub-shift 1.

## Interpretation

**The band rises with the gap, because they have one cause.** A mutation that makes
a post's neighbourhood disagree with its features makes the label ambiguous for every
checkpoint at once, and five seeds resolve an ambiguous post differently. So the
seed band, measured on the mutated graph as the estimand requires, grows from under
one percent on the hubs to 14 percent when their degree is doubled with foreign
posts and 33 percent when their community is replaced, and the gap grows beside it.
The ratio of gap to band on the hubs is 0.2 to 0.9 on every hub arm but one; only
complete replacement of a hub's community, where 53 percent of hubs change label
against a 33 percent band, clears the rule. A gap-floor rule with the post-mutation
seed band as its floor is therefore close to unpassable on the hubs by construction,
not by the stream: the more the stream hurts a hub, the more the floor rises with
it. The rule was designed for a band that stays put while the gap moves, and on this
head it does not.

**The head moves only where the mutation moves the post's majority.** A hub whose
degree doubles with dissimilar posts still has its own 602 features and half its
neighbourhood on its side, and 12 percent of hubs change label. A low-degree post
that gains one dissimilar hub as a neighbour has a neighbourhood that is now mostly
foreign, and 19 to 27 percent of the bottom decile change label under the hub arms,
which is why those arms light the bottom decile and not the hubs: the hubs' random
partners are the low-degree posts. Five percent uniform insertion moves 28 percent of
the bottom decile and 0.1 percent of the top; twenty percent uniform deletion, four
times as many edges, moves 7 percent and 0.15 percent, since a deleted neighbour was
similar and an inserted one is not. Ten days of the real stream, six million edges,
moves 0.2 percent of the top decile. Under this head the behavioural arm has
headroom on low-degree touched posts under every stream, on hubs only under complete
community replacement, and nowhere else, and that is a property of a subreddit
classifier whose label the post's features fix (lab/010), not of any stream.

**The geometric probe has headroom under every arm.** The kNN@20 gap is 0.05 to 0.32
across arms on all posts and 0.53 to 0.69 on the hubs under the strongest hub arms,
against a floor of zero on the deterministic path, and its seed band does not rise
with the mutation: it sits at 0.75 to 0.86 everywhere because two seeds already
share only a fifth of a neighbourhood (A0021). The cosine drift on the hubs is 0.004
under a doubled degree and 0.13 under replacement, both a hundred times lab/012's
growth-stream figure. This is the arm on which a refresh policy's residual can be
read against the no-refresh gap at every degree and under every stream tried.

**What this does to the design.** The behavioural arm's problem is the head, and the
choice is between a head whose output depends on the neighbourhood and a rule whose
floor does not rise with the mutation. The first is the measurement consultation's
question, with these tables beside lab/012's. The second has a candidate the pilot
did not run: the seed band on the starting graph, before the mutation, as the floor
for the gap after it. That band is the instrument's noise on an unambiguous graph,
0.8 percent on the hubs, and the hub-burst and hub-shift gaps of 5 to 53 percent
clear it at every setting. Whether that floor is legitimate, given that the estimand
is disagreement on the mutated graph, is the consultation's to rule on; the note
records that the two floors differ by a factor of forty on the hubs under the
strongest arm.

**What is not measured here.** A refresh policy; the mutations are single draws, not
five, so the band across mutation draws is not measured; the arms are this note's
constructions and not the calibrated generator lab/008 asked for, whose parameters
are still to be measured on the interaction graph; sum aggregation; a
neighbourhood-dependent head; sampled inference.

## Open

- Whether the band is taken on the starting graph or the mutated graph; and whether
  the behavioural arm changes head. For the measurement consultation.
- The band across mutation draws at a fixed setting.
- The calibrated generator, after the modelling ruling.

# 019 — The post graph densifies with exponent 1.8: a new post brings edges in proportion to the graph, and an existing post gains three a day

**Date:** 2026-09-06 · **Component:** the mutation stream · **Status:** measured.

## What was asked

The fourth modelling round (lab/018) read lab/009's stream as the Barabási–Albert
process to two digits, predicted from that reading that Leskovec's densification
exponent — the exponent `a` in edges ∝ nodes^a as the graph grows — would be 1 for a
degree tail exponent above 2, noted that lab/009 had not reported it, and asked for it
and for the degree assortativity over the thirty days before the preregistration
declares the real stream as its anchor. Both are cheap graph statistics on the arrival
stream lab/009 derived, and neither needs a model or the GPU, so they were run while
the claims audit held the card. Script: `lab/probe_densification.py`, 95 s on the CPU.

## Setup

**The task.** None. No model is trained or run; the quantities are properties of the
graph and its arrival order alone.

**The data and the starting state.** The Reddit post graph of the GraphSAGE release:
232,965 posts, each carrying an arrival day assigned from its post id at lab/009's
id-counter rate (156,892 ids a day, day 0 the earliest post, the last post at day
30.16). Both edge sets are used: the paper's graph of 11,606,919 undirected edges and
the full graph of 57,307,946 that the PyG copy ships. An edge exists from the moment
its later post exists, as in lab/009, so every edge has an arrival day and the graph at
the end of day `d` is every post with arrival day below `d` and every edge whose later
endpoint has arrival day below `d`. There is no starting snapshot in the sense of the
mutation pilots: the series runs from day 1 (7,207 posts) to day 30 (231,921 posts).

**The mutation.** The real arrival stream and nothing else: posts arrive, and each
brings the edges to earlier posts that the data records. No synthetic generator, no
deletions, no feature or label changes, no rewiring, and nothing in any earlier
snapshot is altered by a later one.

**What was held fixed.** The arrival order (the id clock) and the edge sets as lab/009
derived them. No seed enters the real-stream measurement; seed 20260906 draws the two
synthetic verifier streams and the endpoint shuffle.

**What is compared against what.** Three series over the thirty day-boundary
snapshots. The densification exponent is the least-squares slope of log edge count on
log post count over the snapshots, fitted over days 1–30, 10–30 and 20–30 (the early
days are small graphs and the fit's residual says how far a single power law holds).
The degree assortativity is Newman's coefficient — the Pearson correlation between the
degrees of the two endpoints of an edge, over all edges of the snapshot, with both
endpoint orders counted — on the whole snapshot, and separately on the edges that
arrived in the day just ended, split by whether both endpoints arrived that day or only
one did. The per-post rates are the edges a post arriving on day `d` brings with it
(edges arriving that day over posts arriving that day) and the edges an existing post
gains during day `d` (edges arriving that day with an older endpoint over posts that
existed at the day's start), each with its log-log slope against the post count over
days 10–30.

**The baseline or noise band.** For the exponent there is no noise band: the series is
deterministic given the clock. The reference values are the two limiting growth
processes: a new node attaching to a fixed number of existing nodes gives `a` = 1 (the
Barabási–Albert case), a new node attaching to a fixed fraction of them gives `a` = 2.
For the assortativity the null is the same edge set with one endpoint column
shuffled, which preserves the degree sequence of one side and destroys any pairing, and
reads at zero.

**The verifier check.** The exponent fit was read on two synthetic thirty-day streams of
30,000 nodes with known `a` before the real series: a fixed count of five attachments
per node gave 1.001 (days 1–30) and 1.000 (days 10–30); a fixed fraction of one percent
gave 2.017 and 2.006. The assortativity was read on each final edge set with one
endpoint column shuffled (known negative: −0.0000 and −0.0002) and with endpoints
re-paired by degree rank (known positive: 1.0000 on both).

## Observation

**The densification exponent is 1.8, not 1.** Edge count against post count over the
thirty snapshots gives `a` = 1.74 on the paper's graph and 1.83 on the full over days
1–30 (root-mean-square log residual 0.029 and 0.011), 1.80 and 1.85 over days 10–30
(0.008 both), and 1.85 and 1.89 over days 20–30. Edges per post rise from 4.1 to 49.7
on the paper's graph and from 14.0 to 245.7 on the full between day 1 and day 30 while
posts arrive at a flat 7,200–8,600 a day.

**A new post brings edges in proportion to the graph it joins.** Edges brought by a post
on its arrival day, at days 1, 5, 10, 15, 20, 25 and 30: 4, 19, 33, 48, 58, 78, 91 on
the paper's graph and 14, 88, 161, 235, 287, 388, 451 on the full; the log-log slope
of this count against the post count over days 10–30 is 0.90 and 0.93. A post arriving
on day 25 joins with about 0.04 percent of the posts that exist (78 of 192,455; 388 of
192,455 is 0.2 percent on the full), and that share is nearly flat over the month.

**An existing post gains about three edges a day, slowly falling.** Edges an existing
post gains during a day, at days 2, 5, 10, 15, 20, 25 and 30: 4.58, 4.16, 3.58, 3.28,
3.07, 3.03, 2.86 on the paper's graph and 19.9, 19.6, 17.6, 16.3, 15.2, 15.2, 14.3 on
the full; the log-log slope against the post count over days 10–30 is −0.12 and −0.10.

**Degree assortativity is 0.10 and flat from the second week.** On the paper's graph
the whole-snapshot coefficient is 0.49 on day 1 (7,207 posts), 0.25 on day 2, 0.09 by
day 5, and between 0.094 and 0.105 on every day from 9 to 30, 0.1035 on day 25 and
0.1008 on day 30. On the full graph it is 0.105 on day 1, 0.129 on day 2, 0.11–0.13
through day 10, and between 0.106 and 0.112 on every day from 11 to 30, 0.1097 on day
25 and 0.1057 on day 30. The edges arriving in a day are as assortative as the graph
(0.07–0.13 on both edge sets from day 3 on), and within them the edges between two
posts that both arrived that day are more so (0.10–0.23) than the edges from a new post
to an old one (0.06–0.13). Day 20's arrivals are the most assortative day of the second
half on both edge sets (0.122 and 0.134; new-to-new 0.223 and 0.233).

## Interpretation

**The prediction of 1 fell, and the Barabási–Albert reading with it.** The stream has
linear preferential attachment (lab/009's slope of 0.96–0.98 of gain on degree stands)
but not a constant number of edges per arriving node, which is the other half of the
Barabási–Albert process and the half that gives `a` = 1. A post's edges are fixed by
the users who comment on it, and a user's other posts are a roughly constant fraction
of all posts, so a new post attaches to a nearly fixed fraction of the existing graph:
that is the `a` = 2 process, and 1.8–1.9 over the last ten days is its finite-month
approach. The tail exponent above 2 that the prediction was conditioned on is real
(lab/009's Hill exponents are 2.9–3.9); the condition was on the wrong quantity.

**What is stationary and what is not, for an existing post.** The per-post arrival rate
onto existing posts is the quantity a refresh policy sees, and it is nearly flat: about
three new edges a day on the paper's graph and fifteen on the full, falling by ten
percent per e-fold of the graph. So the arrived fraction a day hands an existing post of
a given degree does not drift over the month in the way the round-three objection
feared, and the modelling round's dissolution of that objection survives on this
number even though its mechanism (a stationary Barabási–Albert process) does not. What
drifts is the degree at birth: a post arriving on day 25 starts with 78 edges where a
day-5 post started with 19, so the degree distribution's shape is not stationary, a
day-20 hub decile is a mixture of old posts that accumulated and young posts that
arrived large, and any generator declared as "the real stream's process" must carry
the growing arrival degree or it will under-populate the hubs it is calibrated to.

**Assortativity is a constant the preregistration can pin.** 0.10 on the paper's graph
and 0.11 on the full from the second week on, at day 25 as at day 20, with the daily
arrivals matching it. A generator that attaches uniformly by preference alone produces
zero, so a non-zero coefficient is one of the two numbers (with lab/015's coherence
anchors) that says whether a synthetic arm hit the real stream's structure. The
new-to-new excess (0.10–0.23) is the same-day co-commented cluster and is the part of
each day's arrivals a growth generator with independent attachments will miss.

**For the design.** The real stream stays primary and anchor; nothing here moves that.
The generator's declaration changes from a Barabási–Albert process with the measured
slope to a growth process with linear preferential attachment, an arrival degree that
scales with the graph (slope 0.9 in the post count), a per-existing-post rate of about
three a day, and assortativity 0.10 as a check. The densification exponent itself is a
reportable property of the anchor and an anchor for the "rates beyond the ten days the
data has" role the modelling round kept for the generator: extrapolating at `a` = 1
over a further month, in which the post count doubles, would under-count the edges
added by a factor of 1.8.

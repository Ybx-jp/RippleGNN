# 020 — A quarter of the edges the real stream brings cross subreddits, a hub's arrivals are a third foreign and spread over many, and the stream preserves each neighbourhood's mix

**Date:** 2026-09-06 · **Component:** the mutation stream, the generator's coherence anchor · **Status:** measured.

## What was asked

lab/015 measured the real stream's coherence among a post's stale neighbours as
sitting between the deletion and insertion brackets (cosine 0.05–0.10 against a
shuffled 0.003; the top decile's alignment 2.6 times its orthogonal value, a quarter of
the coherent bound) and read it as the contribution of the cross-subreddit share of
the arriving edges, without splitting the stream by edge type. The fourth modelling
round (lab/018) made coherence a generator parameter, the share of inserted partners
from another community, and named the real stream's own share as unmeasured and as
what sets that anchor; both fourth rounds asked for the stream's coherence split by
same- and cross-subreddit arrivals. This note is the half of that probe that needs no
model: the share itself, by degree, by day and per post, and how concentrated a
post's foreign arrivals are, on the CPU while the claims audit held the card. The
coherence half — the first-layer deltas split by edge type — waits for the GPU.
Script: `lab/probe_foreign_share.py`, 18 s.

## Setup

**The task.** None. No model is trained or run. The subreddit label each post carries
(41 subreddits, the largest holding 12.1 percent of posts) is used as the post's
community, which is what lab/013's and lab/015's hub constructions call "foreign".

**The data and the starting state.** The Reddit post graph of the GraphSAGE release,
232,965 posts with arrival days from lab/009's id clock, both edge sets (the paper's
11,606,919 edges and the full 57,307,946), with an edge arriving when its later post
does. The starting graph is the day-20 snapshot the mutation pilots use: 153,430 posts
and 5,376,616 edges on the paper's graph, 26,142,373 on the full, with each existing
post's degree decile taken from its day-20 degree.

**The mutation.** The real arrival stream from day 20 to day 30: 4,576,721 edges
joining a new post to an existing one and 1,653,582 joining two new posts on the
paper's graph, 23,413,669 and 7,751,904 on the full. No synthetic generator, no
deletions, no feature or label changes; nothing in the day-20 graph is altered.

**What was held fixed.** The labels as the dataset ships them, the clock, the edge
sets. No seed enters the measurement except 20260906 for the label shuffle below.

**What is compared against what.** An edge is *foreign* when its two posts carry
different labels. Reported: the foreign share of the day-20 graph's own edges; of the
edges arriving from day 20 on, by class (new-to-old, same-day) and by arrival day over
the whole month (a day's new-to-old edges are those whose earlier post arrived before
that day); of the new-to-old edges by the existing endpoint's day-20 degree decile;
per existing post, the share of its own day-20-to-30 arrivals that are foreign, as the
median and quartiles over the posts of a decile that received at least one arrival;
over posts that received at least ten foreign arrivals, the share of them carried by
the post's single most common foreign subreddit; and the median share of a post's
neighbourhood that is foreign at day 20 and at day 30, by decile.

**The baseline or noise band.** Chance is the foreign share under a random labelling,
one minus the sum of squared label frequencies: 0.955. A stream that attached without
regard to community would read there.

**The verifier check.** With the labels shuffled once, the day-20 graph's foreign
share reads 0.955 on the paper's graph and 0.956 on the full, at chance.

## Observation

**A quarter of the arriving edges cross subreddits, flat over the month.** The day-20
graph's own edges are foreign at 0.217 on the paper's graph and 0.246 on the full. The
edges arriving from day 20 on are foreign at 0.236 and 0.257 when they join a new post
to an existing one and at 0.173 and 0.202 when they join two posts of the same day. By
day, the new-to-old share is 0.16–0.20 over the first six days and 0.22–0.25 (paper)
and 0.24–0.27 (full) on every day from 7 to 29; the same-day share is 0.11–0.16 and
0.14–0.20. Day 30 is a sixth of a day and reads low (0.12 and 0.03) because the posts
that would complete its edges are past the dataset's end.

**The share is U-shaped in the existing post's degree.** Foreign share of the
new-to-old edges by the existing endpoint's day-20 decile, lowest to highest: 0.300,
0.222, 0.181, 0.166, 0.154, 0.142, 0.139, 0.149, 0.164, 0.353 on the paper's graph and
0.326, 0.256, 0.211, 0.181, 0.165, 0.154, 0.146, 0.147, 0.167, 0.361 on the full. Per
post, over the 92.7 and 94.8 percent of existing posts that received an arrival, the
median foreign share of a post's own arrivals is 0.05–0.07 on deciles 2–7, 0.10 on
decile 8 and 0.25 on the top decile (quartiles 0.10–0.43) on both edge sets; the
bottom decile's median is 0.00 on the paper's graph and 0.21 on the full with
quartiles from 0 to 1, since a post there has a handful of arrivals.

**A hub's foreign arrivals are spread across subreddits; a low-degree post's come from
one.** Over posts with at least ten foreign arrivals (25,226 on the paper's graph,
11,170 of them in the top decile; 57,025 and 13,875 on the full), the share of a post's
foreign arrivals carried by its single most common foreign subreddit has median 0.29
(quartiles 0.20–0.42) on the top decile on both edge sets, 0.40–0.47 on deciles 7–8,
0.50–0.64 on deciles 2–6, and 0.80–0.92 on the two lowest deciles.

**The stream preserves each neighbourhood's mix.** The median share of a post's
neighbourhood that is foreign is 0.25 on the top decile at day 20 and 0.24–0.25 at day
30 on both edge sets, 0.09–0.10 on decile 8 at both days, and 0.04–0.07 on deciles 2–7
at both days; the paper graph's bottom decile moves from 0.00 to 0.08 because its
day-20 neighbourhood is empty.

## Interpretation

**The generator's foreign-partner share is a per-post quantity, and it is the post's
own neighbourhood.** A post's ten days of arrivals are foreign in the same share its
existing neighbourhood already is, at every decile: the stream is composition-
preserving, and the "cross-subreddit fifth" lab/015 reasoned from is the graph-wide
average of a share that runs from a twentieth on the median post to a quarter on a hub.
A generator that draws each inserted partner foreign with one global probability will
give the median post four times its real foreign share and a hub two-thirds of it;
the declaration that hits the anchor is "foreign with the post's own neighbourhood's
share", which is a number the day-20 graph carries for every post.

**Why the real stream's coherence sits where lab/015 found it.** A foreign arrival
moves an existing post's aggregated input toward that foreign post's community, and
two foreign arrivals move it the same way only if they come from the same community.
On a hub, a third of the arrivals are foreign but the largest single foreign
subreddit carries under a third of those, so the coherent part of a hub's arrivals is
of order a tenth of them, spread over the rest in directions that partly cancel; on a
low-degree post the foreign arrivals are few and from one subreddit, which is the
coherent shape, but they are few. That is the shape lab/015 measured: alignment at
the orthogonal value on the bottom decile, 2.6 times it on the top and a quarter of
the coherent bound. The GPU half of this probe — the first-layer deltas split by
same- and cross-subreddit arrivals — tests that reading directly; this note fixes the
counts it will be read against.

**For the design.** The hub constructions of lab/013 and lab/015 insert foreign posts
drawn uniformly from other subreddits, which is the dispersed shape a real hub sees,
and at "half its degree in foreign posts" they are at twice a hub's real foreign share
(0.25 of its neighbourhood) and about three times the foreign arrivals a hub actually
receives in ten days (a third of a gain of about four-tenths of its degree, from
lab/019's three edges a day on a mean day-20 degree of 70); they stay the adversarial
corner and are now placed against the anchor. The generator's
synthetic insertion arm carries three declared numbers from this note and lab/019: the
foreign share per post equal to the post's neighbourhood's, the top foreign
subreddit's share of a hub's foreign arrivals near 0.3, and the arrival degree scaling
with the post count. The U-shape by decile is one more thing a uniformly-attached
generator will not produce and the preregistration can check it against.

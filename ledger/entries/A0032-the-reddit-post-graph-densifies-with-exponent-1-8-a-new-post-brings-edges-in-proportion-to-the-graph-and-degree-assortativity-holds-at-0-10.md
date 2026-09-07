---
id: A0032-the-reddit-post-graph-densifies-with-exponent-1-8-a-new-post-brings-edges-in-proportion-to-the-graph-and-degree-assortativity-holds-at-0-10
kind: claim
stated: 2026-09-06T19:40:00-07:00
author: main
grade: measured
supersedes: none
verbatim_sha: e688bd975dfe22dcd55ec2300a0da09576cc3d05ab57f77839a603f841fcca44
---

## Assertion

On the Reddit post graph ordered by post id, the edge count grows as a power of the
post count with exponent 1.80 on the paper's 11.6 million-edge graph and 1.85 on the
full 57.3 million-edge graph over days 10 to 30, rising to 1.85 and 1.89 over the last
ten days, not the exponent 1 of a growth process that attaches a fixed number of edges
per arriving node: a post arriving on day 25 brings 78 and 388 edges where a post
arriving on day 5 brought 19 and 88, the count scaling with the post count to the power
0.90 and 0.93, while an existing post gains about three and fifteen new edges a day
with a slope of −0.1 in the post count. The degree assortativity of the whole graph is
between 0.094 and 0.105 on the paper's graph and between 0.106 and 0.112 on the full on
every day from the eleventh to the thirtieth, 0.1035 and 0.1097 at day 25, and the
edges arriving in a day are as assortative as the graph they join.

## Scope

metric: the least-squares slope of log edge count on log post count over the day-boundary snapshots, fitted over days 1 to 30, 10 to 30 and 20 to 30; edges arriving on a day over posts arriving on it, and edges arriving on a day with an older endpoint over posts existing at its start, each with the log-log slope against the post count over days 10 to 30; Newman's degree assortativity, the Pearson correlation of the two endpoint degrees over the snapshot's edges with both endpoint orders counted, on the whole snapshot and on the edges that arrived in the day just ended, split by whether both endpoints arrived that day
cohort: both edge sets of the Reddit post graph, the paper's 11,606,919 edges and the full 57,307,946, over all 232,965 posts, with each post's day assigned from its id at the preceding clock entry's rate of 156,892 ids a day and an edge's arrival taken as the creation of its later post, at the thirty snapshots taken at the end of each day from day 1 (7,207 posts) to day 30 (231,921 posts); exponents 1.737 and 1.825 over days 1 to 30 with root-mean-square log residuals 0.029 and 0.011, 1.795 and 1.847 over days 10 to 30 with residuals 0.008, 1.849 and 1.887 over days 20 to 30; edges brought by an arriving post at days 1, 5, 10, 15, 20, 25 and 30 of 4, 19, 33, 48, 58, 78, 91 and 14, 88, 161, 235, 287, 388, 451; edges gained by an existing post in a day at days 2, 5, 10, 15, 20, 25 and 30 of 4.58, 4.16, 3.58, 3.28, 3.07, 3.03, 2.86 and 19.9, 19.6, 17.6, 16.3, 15.2, 15.2, 14.3 with slopes −0.12 and −0.10; whole-snapshot assortativity 0.1035 and 0.1097 at day 25 and 0.1008 and 0.1057 at day 30, the day's arrivals 0.07 to 0.13 from day 3 on, same-day pairs 0.10 to 0.23 and new-to-old edges 0.06 to 0.13
condition: no model and no seed enter the measurement; the clock is the id counter and inherits its linearity assumption, so the exponent is in the post count and not in wall-clock time; the fit is a single power law over the stated day ranges and the residual is reported rather than a test of the form; the exponent fit read 1.001 and 2.017 on synthetic fixed-count and fixed-fraction growth streams, and the assortativity read −0.0000 and −0.0002 with one endpoint column shuffled and 1.0000 with endpoints paired by degree rank, before the real series was read; the data carries no deletions and nothing here calibrates them; linear preferential attachment as measured by the preceding stream entry is unchanged by this entry, which measures the number of edges an arriving post brings and not how they are placed

## Grounds

- lab: lab/019-the-post-graph-densifies-with-exponent-1-8-a-new-post-brings-edges-in-proportion-to-the-graph-and-an-existing-post-gains-three-a-day.md § "Observation" @d9f5681
- entry: A0017-reddit-post-ids-order-posts-by-creation-and-the-published-split-is-an-id-threshold · cites-as-live
- entry: A0018-edges-arrive-on-the-reddit-post-graph-by-node-growth-with-linear-preferential-attachment · cites-as-live

## Warrant

The four tables of lab/019 are the measurement, on the same arrival stream and edge
sets as the preceding stream entry, and the numbers are read directly. The clock
entry gives the day of every post; the stream entry gives the reading that an edge
arrives with its later post and that edge arrivals per day grow with the graph, which
this entry quantifies as an exponent. The exponent separates the two halves of the
Barabási–Albert process that the stream entry's slope of 0.96 and 0.98 does not: that
process attaches a fixed number of edges per arriving node and gives an exponent of
1, and this graph does not, because a post's edges are fixed by the users who comment
on it and a user's other posts are a roughly fixed share of all posts, so an arriving
post attaches to a nearly fixed fraction of the graph, whose limiting exponent is 2.
The per-existing-post rate is the quantity that says whether the arrived fraction a
day hands a post of a given degree drifts over the month, and it does not by more
than ten percent per e-fold of the graph. The assortativity is stated as a constant
of the second half of the month because it is one to within 0.011 on either edge set
from day 11 on, and is reported as the check a generator must pass rather than as a
mechanism.

## Backing

none

<!-- APPEND BELOW THIS LINE ONLY -->

## Verdicts


## References

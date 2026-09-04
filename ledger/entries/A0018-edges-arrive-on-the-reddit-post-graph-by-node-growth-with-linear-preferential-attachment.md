---
id: A0018-edges-arrive-on-the-reddit-post-graph-by-node-growth-with-linear-preferential-attachment
kind: claim
stated: 2026-09-03T20:08:00-07:00
author: main
grade: measured
supersedes: none
verbatim_sha: c6eb2dd6d7ad828390e28f0475fd3d02dc8fd471e98355afe26c19b8a108462a
---

## Assertion

On the Reddit post graph ordered by post id, every edge arriving after the twenty-day
split has a newly created endpoint and none joins two existing posts; posts arrive at
a flat rate of about 7,700 a day while edge arrivals per day grow with the graph. Of
the arriving edges that join a new post to an existing one, the existing endpoint lies
in the top decile of degree at the split for 40 percent on the paper's 11.6 million-edge
graph and 48 percent on the full 57.3 million-edge graph, and the mean number of new
edges an existing post gains scales with its degree at the split with a log-log slope
of 0.96 and 0.98. The Hill exponent of the final degree tail above the 90th percentile
is 3.1 and 2.9, and per-node burstiness of edge arrivals in id-counter time has median
0.09 and 0.16 on a scale where 0 is Poisson and 1 is maximally bursty.

## Scope

metric: counts of arriving edges by whether zero, one or two endpoints are new; the share of new-to-old edges by the old endpoint's degree decile at the split; the slope of log mean degree gain against log degree at the split over log-spaced bins of at least fifty nodes; the Hill estimator of the degree tail above the 90th, 95th and 99th percentiles; the Goh and Barabasi burstiness of each node's inter-arrival gaps over nodes with at least twenty arrivals
cohort: both edge sets of the Reddit post graph, the paper's and the full, over all 232,965 nodes, with an edge's arrival taken as the creation of its later post and days assigned by the id-counter rate of the preceding entry
condition: arrival time is the later post's creation, which is what the construction implies for a graph whose edges are fixed by the users commenting on each post, and not the comment time, which neither copy records; degree at the split counts only edges between posts existing then; deletions do not occur in the data and nothing here calibrates them; the burstiness is in id-counter units and inherits the clock's linearity assumption

## Grounds

- lab: lab/009-the-reddit-post-ids-are-the-clock-and-the-stream-is-growth.md § "Observation" @7b19a39
- entry: A0017-reddit-post-ids-order-posts-by-creation-and-the-published-split-is-an-id-threshold · cites-as-live

## Warrant

With the ordering of the preceding entry, each edge's arrival is the creation of its
later endpoint, so the counts in lab/009's stream section are read directly: zero
arriving edges between existing posts on either edge set, decile shares of 0.396 and
0.478 at the top, log-binned slopes of 0.96 and 0.98, Hill exponents of 3.09 and 2.94
at the 90th percentile, and burstiness medians of 0.089 and 0.156. A slope near one is
the signature of linear preferential attachment, and the assertion names the mechanism
by that signature and not by a fitted model.

## Backing

none

<!-- APPEND BELOW THIS LINE ONLY -->

## Verdicts


## References


---
id: A0033-a-quarter-of-the-edges-the-reddit-growth-stream-brings-to-existing-posts-cross-subreddits-a-hubs-arrivals-are-a-third-foreign-and-spread-over-many-and-each-neighbourhoods-foreign-share-is-preserved
kind: claim
stated: 2026-09-06T20:10:00-07:00
author: main
grade: measured
supersedes: none
verbatim_sha: 6f03497c58fdf001d04441e4edb75569d71f4583ecdcfbdd8dfad7f46289d87e
---

## Assertion

On the Reddit post graph from day 20 to day 30, of the edges the growth stream brings
to an existing post, 24 percent on the paper's 11.6 million-edge graph and 26 percent
on the full 57.3 million-edge graph join it to a post of another subreddit, a share
that is flat by day from the seventh day of the month on and against a chance value
of 96 percent under a random labelling; by the existing post's degree decile at day 20
the share is U-shaped, 30 and 33 percent on the lowest decile, 14 to 15 percent on the
middle deciles and 35 and 36 percent on the top; per post, the median foreign share
of a post's own arrivals is 5 to 7 percent on deciles 2 to 7 and 25 percent on the top
decile, where the largest single foreign subreddit carries a median 29 percent of a
post's foreign arrivals against 80 to 92 percent on the two lowest deciles; and the
median foreign share of a post's neighbourhood is the same at day 30 as at day 20 on
every decile that has a day-20 neighbourhood.

## Scope

metric: the share of edges whose two posts carry different subreddit labels, over the day-20 graph's edges, over the edges arriving from day 20 that join a new post to an existing one and over those that join two posts of the same day, by arrival day over the month with a day's new-to-old edges those whose earlier post arrived before that day, and by the existing endpoint's day-20 degree decile; per existing post that received an arrival, the foreign share of its own day-20-to-30 arrivals as the median and quartiles over the posts of a decile; over posts with at least ten foreign arrivals, the share carried by the post's single most common foreign subreddit as the median and quartiles by decile; the median share of a post's neighbourhood that is foreign at day 20 and at day 30 by decile
cohort: both edge sets of the Reddit post graph over all 232,965 posts with days from the id clock and an edge arriving with its later post, the 41 subreddit labels as the dataset ships them with the largest at 12.1 percent of posts, the day-20 snapshot of 153,430 posts and 5,376,616 (paper) and 26,142,373 (full) edges as the starting graph and its degree deciles, and the stream of 4,576,721 and 23,413,669 new-to-old and 1,653,582 and 7,751,904 same-day edges over days 20 to 30; day-20 edges foreign at 0.217 and 0.246, new-to-old arrivals at 0.236 and 0.257, same-day at 0.173 and 0.202, the daily new-to-old share 0.22 to 0.25 and 0.24 to 0.27 on days 7 to 29 and 0.16 to 0.23 on days 1 to 6; by decile 0.300, 0.222, 0.181, 0.166, 0.154, 0.142, 0.139, 0.149, 0.164, 0.353 and 0.326, 0.256, 0.211, 0.181, 0.165, 0.154, 0.146, 0.147, 0.167, 0.361; per-post medians 0.05 to 0.07 on deciles 2 to 7, 0.10 on decile 8 and 0.25 with quartiles 0.10 to 0.43 on the top on both edge sets, the bottom decile 0.00 and 0.21 with quartiles 0 to 1, over 92.7 and 94.8 percent of existing posts; concentration over 25,226 and 57,025 posts of which 11,170 and 13,875 are top-decile, medians 0.29 with quartiles 0.20 to 0.42 on the top decile, 0.40 to 0.47 on deciles 7 and 8, 0.50 to 0.64 on deciles 2 to 6, 0.80 to 0.92 on deciles 0 and 1; neighbourhood foreign share by decile 0.25 to 0.24 or 0.25 on the top, 0.09 to 0.10 on decile 8, 0.04 to 0.07 unchanged on deciles 2 to 7, at days 20 and 30
condition: no model and no seed enter the measurement except one label shuffle for the chance reading, which gave 0.955 and 0.956 against the analytic 0.955; community is the subreddit label and nothing finer; the day-30 figures exclude the last sixth of a day, whose edges to posts past the dataset's end are absent and read low at 0.12 and 0.03; the bottom decile of the paper's graph has an empty day-20 neighbourhood, so its per-post shares are over a handful of arrivals each; the concentration is over posts with at least ten foreign arrivals, which are mostly top-decile posts; the data carries no deletions; the coherence of the first-layer deltas these arrivals induce, split by same- and cross-subreddit, is not measured here

## Grounds

- lab: lab/020-a-quarter-of-the-edges-the-real-stream-brings-cross-subreddits-a-hubs-arrivals-are-a-third-foreign-and-spread-over-many-and-the-stream-preserves-each-neighbourhoods-mix.md § "Observation" @92d5014
- entry: A0018-edges-arrive-on-the-reddit-post-graph-by-node-growth-with-linear-preferential-attachment · cites-as-live
- entry: A0027-on-the-reddit-graph-random-deletions-make-stale-neighbour-deltas-incoherent-dissimilar-insertions-make-them-coherent-and-the-real-stream-sits-between · cites-as-live

## Warrant

The four tables of lab/020 are the measurement, on the arrival stream and edge sets of
the stream entry and the day-20 starting graph of the mutation pilots, and the numbers
are read directly against a chance value the label shuffle reproduces. The stream
entry gives the reading that the arrivals to an existing post are the whole of what
the stream does to it, so the foreign share of those arrivals is the share of a
post's staleness that comes from another community. The coherence entry found the
real stream's stale-neighbour deltas between the incoherent and coherent brackets and
read that as the cross-subreddit share of the arrivals; this entry supplies the share
and adds two things the reading needs: that it is a per-post quantity equal to the
post's neighbourhood's existing share rather than a graph-wide constant, and that on
a hub the foreign arrivals are dispersed over subreddits so that the aligned part is
a fraction of the foreign part. The stated shares are of edges and of posts, not of
the deltas they induce; whether the aligned deltas follow the counts is the
measurement the coherence entry's method makes on this split, and it is named in the
conditions as not made here.

## Backing

none

<!-- APPEND BELOW THIS LINE ONLY -->

## Verdicts


## References

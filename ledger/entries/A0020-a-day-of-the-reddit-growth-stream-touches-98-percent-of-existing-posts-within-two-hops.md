---
id: A0020-a-day-of-the-reddit-growth-stream-touches-98-percent-of-existing-posts-within-two-hops
kind: claim
stated: 2026-09-03T20:32:05-07:00
author: main
grade: measured
supersedes: none
verbatim_sha: cbe29e6679a460f211c9466951cf1f91bb58f65fdd5d39cbda55dc461ccaa5a1
---

## Assertion

On the Reddit post graph's real arrival stream, one day of insertions puts about 69
percent of the existing posts one hop from an arriving edge and about 98 percent
within two hops, so a two-layer model's exact embedding changes on nearly every
existing node per day; the untouched remainder is the posts the edge set leaves
isolated or nearly so; one hour of insertions puts about 11 percent one hop away and
about 90 percent within two, with the untouched set then populated at every degree.

## Scope

metric: fraction of posts created before the episode that are an endpoint of an edge arriving in the episode (one hop), that neighbour such a post over pre-episode edges without being one (two hops only), or neither (untouched), with the mean degree of each stratum on the post-episode graph
cohort: the paper's 11,606,919-edge Reddit graph with post creation ordered by post id as in A0017; three episodes of the growth stream: day 20 for one day (153,430 existing posts, 8,625 arriving, 546,352 arriving edges: 68.5, 29.7 and 1.8 percent, mean degrees 93.7, 30.8 and 0.8), day 20 for one hour (338 arriving posts, 20,602 edges: 10.6, 79.8 and 9.6 percent, mean degrees 147.7, 66.8 and 12.5), day 25 for one day (192,455 existing, 8,475 arriving, 660,956 edges: 68.9, 29.6 and 1.5 percent)
condition: an episode is a half-open interval of the id-derived day clock and every arriving edge has an endpoint created in it, since the stream is node growth with no edges among existing posts as in A0018; the paper edge set only, not the full 57.3M-edge set; strata are exact set membership, not a model's sensitivity, so the two-hop figure is the receptive-field bound for a two-layer model and not a measured change in any embedding

## Grounds

- lab: lab/011-one-day-of-the-real-stream-touches-the-whole-graph-and-seed-churn-is-two-percent.md § "Observation" @ce23495

## Warrant

The first table of lab/011 is the measurement, three episodes with the stratum counts
read off the edge lists directly; the two-hop bound follows from the receptive field of
a two-layer message-passing model, whose output at a node depends on the two-hop
neighbourhood and nothing beyond it. The mean degree under one on the untouched stratum
at a day is what identifies it as the isolated posts rather than a stratum of the
graph a design could use; the one-hour episode is the one that shows the untouched set
becoming a stratum, at the cost of a thirtieth of the arriving posts per episode.

## Backing

none

<!-- APPEND BELOW THIS LINE ONLY -->

## Verdicts


## References

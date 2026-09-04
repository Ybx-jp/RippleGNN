---
id: A0017-reddit-post-ids-order-posts-by-creation-and-the-published-split-is-an-id-threshold
kind: claim
stated: 2026-09-03T20:07:00-07:00
author: main
grade: measured
supersedes: none
verbatim_sha: 517b604d72e36ad54450a9d8a30a6acb202af67886baba6a4c942fe3ebe8b650
---

## Assertion

The GraphSAGE release of the Reddit post graph keys its nodes by base-36 Reddit post
ids that order posts by creation: the published split, the opening twenty days of the
month for training and the rest for validation and test, is exactly the set of ids at
or below 2gzrfc against the set above it, with no exception on either side, and the id
counter runs at a rate that, taken from the train side, predicts the remaining span as
10.16 days against the 10 a thirty-day month gives. The PyG copy carries the same nodes
in the same order, with the same split and the same features standardized on the train
nodes, and no time field of its own.

## Scope

metric: the count of val and test nodes with an id at or below the largest train id and of train nodes above the smallest non-train id; the id-counter rate implied by the train side and the test-side span it predicts; equality of split flags and standardized features between the two copies
cohort: all 232,965 nodes of the Reddit post graph in the GraphSAGE release and the PyG copy, both identified by archive sha256 in lab/009
condition: the time calibration rests on one anchor, the published twenty-day train split, and assumes the month is thirty days; the ids give a creation order and a counter-linear clock, not a calendar timestamp inside the day, and nothing in either copy records when a comment, and hence an edge, appeared

## Grounds

- lab: lab/009-the-reddit-post-ids-are-the-clock-and-the-stream-is-growth.md § "Observation" @7b19a39

## Warrant

A split defined by time is a single threshold in any quantity monotone in time, so a
threshold with zero exceptions on 232,965 nodes is what the ordering premise predicts
and an arbitrary keying would not produce; the second check is independent of the
first, since a counter linear in time makes the ten days after the threshold the same
length in id units per day as the twenty before it, and 10.16 against 10 is within two
percent. Equality of split flags on every node present in both copies and of the
standardized features to the last bit on a sample carries the ordering from the
GraphSAGE release to the PyG index.

## Backing

none

<!-- APPEND BELOW THIS LINE ONLY -->

## Verdicts


## References


---
id: A0011-the-interaction-benchmarks-recompute-in-milliseconds
kind: claim
stated: 2026-09-02T22:07:00-07:00
author: main
grade: measured
supersedes: none
verbatim_sha: 063df082b5296666f817186be916ac4879ca50c9dcd6b6cf59baf91282748629
---

## Assertion

Full-graph two-layer GraphSAGE inference over graphs the size of the temporal
interaction benchmarks completes in about two milliseconds on the project's box, two
orders of magnitude below the same pass over the Reddit post graph at 64 dimensions.

## Scope

metric: synchronized wall-clock of one full-graph forward pass of two-layer GraphSAGE at 128 dimensions
cohort: synthetic random graphs at the published sizes of Cora, CiteSeer, tgbl-wiki, Reddit-JODIE and PubMed, between 2,708 and 19,717 nodes and between 9,981 and 110,000 edges; RTX 3060 with 12 GB
condition: synthetic random graphs at published node and edge counts with approximate degrees, not the datasets themselves; one configuration per row, no repetition; the comparison figure for the Reddit post graph is at 64 dimensions and comes from the same note

## Grounds

- lab: lab/004-the-admissible-band-is-an-edge-count.md § "Observation" @bab6d58

## Warrant

The five rows measure 0.504, 0.519, 1.729, 2.099 and 2.047 ms; the Reddit post graph at
64 dimensions measures 213.6 ms in the same note, which is 124 times tgbl-wiki's figure.
The rows are a cost floor for the reference arm on these graphs, and the assertion says
nothing about whether a refresh saving can be measured against it, which is a
conclusion for an entry that cites this one.

## Backing

none

<!-- APPEND BELOW THIS LINE ONLY -->

## Verdicts


## References


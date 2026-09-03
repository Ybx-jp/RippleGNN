---
id: A0010-the-full-graph-vram-ceiling-is-an-edge-count
kind: claim
stated: 2026-09-02T22:05:00-07:00
author: main
grade: measured
supersedes: none
verbatim_sha: 64b87514dddbcc5d75a6ba00d8986b03350448f884cf9118fda80d953e8638c7
---

## Assertion

On the project's box, full-graph GraphSAGE inference is bounded by memory in proportion
to the product of edge count and hidden dimension, at about half a gibibyte per million
edges at 128 dimensions, with the ceiling between fifteen and twenty million edges at
that width. The Reddit post graph, at twenty-three million edges, fits at 64 dimensions
and runs out of memory at 96 and 128.

## Scope

metric: peak CUDA memory allocated and the synchronized wall-clock of one full-graph forward pass
cohort: one SAGEConv layer at 128 dimensions over synthetic random graphs of 5, 10, 15 and 20 million edges; two-layer GraphSAGE at 128, 96, 64 and 32 dimensions over a synthetic random graph at the Reddit post graph's published size of 232,965 nodes and 23,063,535 edges; RTX 3060 with 12 GB
condition: synthetic random graphs at published node and edge counts, not the datasets themselves, so degree distributions are approximate and real gather patterns will move the timings; one configuration per row, no repetition; a limit on full-graph inference only, since sampled inference is bounded elsewhere; torch and CUDA versions as pinned in the repository at the commit named in Grounds

## Grounds

- lab: lab/004-the-admissible-band-is-an-edge-count.md § "Observation" @bab6d58

## Warrant

Full-graph message passing materializes a tensor per edge with the hidden width as its
second dimension, so peak memory scales with edges times width; the four-row sweep at
128 dimensions measures the constant, 2.75, 5.21 and 7.67 GiB at 5, 10 and 15 million
edges, and the out-of-memory at 20 million places the ceiling. The Reddit rows show the
same product moving the ceiling with width: 6.07 GiB and 213.6 ms at 64 dimensions,
3.25 GiB and 148.5 ms at 32, out of memory at 96 and 128. The measurement corrects an
earlier estimate of the ceiling as a node count, which had been taken at mean degree 10
and did not carry to mean degree 99.

## Backing

none

<!-- APPEND BELOW THIS LINE ONLY -->

## Verdicts


## References


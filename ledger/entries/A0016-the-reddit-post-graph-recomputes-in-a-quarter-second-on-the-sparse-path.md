---
id: A0016-the-reddit-post-graph-recomputes-in-a-quarter-second-on-the-sparse-path
kind: claim
stated: 2026-09-03T20:06:00-07:00
author: main
grade: measured
supersedes: none
verbatim_sha: 3eedf9ff95760ed3783ea189d441820978391180acfd25e72771b32f79b8c18c
---

## Assertion

On the project's box, full-graph two-layer GraphSAGE inference over the real Reddit
post graph with its 602-dim input, the adjacency passed as a compressed-sparse-row
tensor so that aggregation is a sparse-dense matrix product, takes 218 milliseconds at
64 hidden dimensions and 241 at 128 over the paper's 11.6 million undirected edges with
a peak of 2.37 GiB, and 953 and 1,044 milliseconds over the full 57.3 million edges
with a peak of 5.46 GiB. Peak memory on this path does not move with hidden width, and
both edge sets fit at both widths with room to spare.

## Scope

metric: synchronized wall-clock of one full-graph forward pass, median of five passes after one warm-up, and peak CUDA memory allocated
cohort: two-layer SAGEConv with mean aggregation, 602-dim standardized input from the PyG copy, hidden widths 64 and 128, over the paper's Reddit graph of 232,965 nodes and 11,606,919 undirected edges and over the full graph of 57,307,946 undirected edges, each passed in both directions as a torch sparse CSR tensor; RTX 3060 with 12 GB, torch 2.11.0 with CUDA 12.8 and PyTorch Geometric 2.8.0.post1
condition: fp32, untrained weights, eval mode, no gradient, one process with nothing else on the device; the edge sets are the two the pinned archives carry, identified by sha256 in lab/009; timings are of inference alone and exclude building the sparse tensor; a trained checkpoint is expected to cost the same, since the weights do not change the shapes

## Grounds

- lab: lab/009-the-reddit-post-ids-are-the-clock-and-the-stream-is-growth.md § "Observation" @7b19a39

## Warrant

The eight rows of lab/009's recompute table are the measurement, taken with CUDA
synchronized before and after each pass; the sparse path stores the adjacency as
indices and values rather than one gathered message per edge, so its peak is set by the
adjacency and the node tensors and not by the hidden width, which the equal peaks at 64
and 128 on each edge set show. The 218 milliseconds at 64 on the paper's graph is within
two percent of the 213.6 the same pass measured on a synthetic graph of that shape in
lab/004, so the cost ratios drawn from that figure carry over.

## Backing

none

<!-- APPEND BELOW THIS LINE ONLY -->

## Verdicts


## References


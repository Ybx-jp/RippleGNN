---
id: A0015-the-edge-count-vram-ceiling-is-a-property-of-the-per-edge-gather-path
kind: claim
stated: 2026-09-03T20:05:00-07:00
author: main
grade: measured
supersedes: A0010-the-full-graph-vram-ceiling-is-an-edge-count
verbatim_change: the Scope names the message-passing path the ceiling belongs to and adds the real-graph rows from lab/009; the predecessor's second sentence, that the Reddit post graph fits at 64 dimensions and runs out of memory at 96 and 128, is dropped because it was measured on a synthetic graph whose input was as wide as its hidden layer and does not hold on the real graph on either path
verbatim_sha: 5266943bd74dc17ab463fc8c08e0d6f63d82357e945407d04b2183bdcfc754ba
---

## Assertion

On the project's box, full-graph GraphSAGE inference on PyG's default edge-index path
is bounded by memory in proportion to the edge count times the width of the tensor
gathered per edge, which is the input width of the layer, at about half a gibibyte per
million directed edges per 128 dimensions of width. At 128 dimensions the ceiling on
that path lies between fifteen and twenty million edges, and on the real Reddit post
graph, whose input is 602 wide, the path runs out of memory at both the paper's 11.6
million undirected edges and the full 57.3 million, at hidden widths 64 and 128 alike.
The ceiling is a property of the gather path and not of full-graph inference as such.

## Scope

metric: peak CUDA memory allocated and the synchronized wall-clock of one full-graph forward pass, or an out-of-memory error, on the edge-index path where SAGEConv gathers one message per directed edge
cohort: one SAGEConv layer at 128 dimensions over synthetic random graphs of 5, 10, 15 and 20 million edges and two-layer GraphSAGE at 128, 96, 64 and 32 dimensions over a synthetic random graph at the Reddit post graph's published size, both with input width equal to hidden width, in lab/004; two-layer GraphSAGE with the real 602-dim input at hidden widths 64 and 128 over the paper's 11,606,919-edge Reddit graph and the full 57,307,946-edge graph the PyG copy ships, in lab/009; RTX 3060 with 12 GB
condition: fp32, untrained weights, eval mode, no gradient; a limit on the edge-index path only, and the sparse-matrix aggregation path over the same graphs is a separate entry; the synthetic rows have approximate degree distributions and one configuration per row without repetition; torch and CUDA versions as pinned at the commits named in Grounds

## Grounds

- lab: lab/004-the-admissible-band-is-an-edge-count.md § "Observation" @bab6d58
- lab: lab/009-the-reddit-post-ids-are-the-clock-and-the-stream-is-growth.md § "Observation" @7b19a39

## Warrant

The edge-index path materializes a tensor of shape edges by input width on every
layer, so peak memory scales with their product; lab/004's sweep at 128 dimensions
measures the constant, 2.75, 5.21 and 7.67 GiB at 5, 10 and 15 million edges, and its
out-of-memory at 20 million places the ceiling. The same constant predicts the real
graph: the paper's Reddit graph is 23.2 million directed edges at 602 wide on the first
layer, which at half a gibibyte per million edges per 128 dimensions is about 55 GiB,
and lab/009 measures the out-of-memory at 64 and 128 hidden on both edge sets. The
predecessor's Reddit rows, 6.07 GiB at 64 and out-of-memory at 96 and 128, were taken
with a 64-wide input and describe that synthetic configuration, not the dataset.

## Backing

none

<!-- APPEND BELOW THIS LINE ONLY -->

## Verdicts


## References


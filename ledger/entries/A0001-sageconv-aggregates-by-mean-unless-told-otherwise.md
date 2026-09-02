---
id: A0001-sageconv-aggregates-by-mean-unless-told-otherwise
kind: claim
stated: 2026-09-02T16:20:00-07:00
author: main
grade: measured
supersedes: none
verbatim_sha: 0962d2d49071d1d2158d726a9fbae19784d2e78253614b02069ba52bf91c4fd8
---

## Assertion

The SAGEConv layer in PyTorch Geometric aggregates neighbour messages by mean unless an
aggregator is passed explicitly, so a GraphSAGE model built from it without one is a
mean-aggregation model.

## Scope

metric: the default value of the aggr argument to SAGEConv.__init__ and the aggregation module it instantiates
cohort: torch_geometric 2.8.0.post1, the version pinned in this repository's uv.lock
condition: read from the installed source and confirmed by instantiating the layer; the aggregator was passed nowhere; other versions were not checked

## Grounds

- lab: lab/005-mean-aggregation-makes-it-a-fraction-not-a-count.md § "Observation" @bab6d58
- source: pyg-sage-conv-2.8.0.post1 · torch_geometric/nn/conv/sage_conv.py, the aggr parameter of SAGEConv.__init__

## Warrant

A library default is what the code does when the argument is omitted. The constructor's
default for the aggr parameter was read in the pinned source, and the lab probe
instantiated the layer without an aggregator and found a MeanAggregation module in
place, so the default was exercised as well as read.

## Backing

none

<!-- APPEND BELOW THIS LINE ONLY -->

## Verdicts


## References

- experiments/ROSTER.md · standing · cites-as-live

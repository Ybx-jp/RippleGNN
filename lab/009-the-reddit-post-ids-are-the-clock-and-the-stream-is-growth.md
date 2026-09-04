# 009 — The Reddit post ids are the clock, the stream is growth, and the real graph recomputes on the sparse path only

**Date:** 2026-09-03 · **Component:** dataset and experiment design · **Status:** measured.

## What was asked

lab/008's first probe: whether the Reddit post graph carries an arrival order in a
pinned copy, and if so what its real stream looks like, so that the preregistration's
insertion stream can be real rather than generated and the generator's parameters can
be measured on something real. Alongside it, the full recompute on the real graph,
since every Reddit cost figure the project holds (lab/004) came from a synthetic
random graph of Reddit's published shape. Scripts: `lab/probe_reddit_stream.py` and
`lab/probe_reddit_recompute.py`, run in that order; the first writes the edge sets
with their arrival days that the second reads.

Two copies were pinned. The PyG/DGL archive (`https://data.dgl.ai/dataset/reddit.zip`,
1,397,962,821 bytes, sha256
`9a16353c28f8ddd07148fc5ac9b57b818d7911ea0fbe9052d66d49fc32b372bf`) and the original
GraphSAGE release (`http://snap.stanford.edu/graphsage/reddit.zip`, 1,308,432,264
bytes, sha256 `25337a21540cd373e4cee3751e6600324ab6a7377ef3966bb49f57412a17ed02`).
Both hashes are of the archives as downloaded on 2026-09-03.

## Observation

**The PyG copy carries no time.** Its raw arrays are `feature`, `label`, `node_ids`
and `node_types`; `node_ids` is the identity permutation and `node_types` is the
train/val/test split. The GraphSAGE release keys its id map by the post's Reddit id, a
base-36 string. Decoded, the 232,965 ids are integers in [146,336,876, 151,067,957],
from `2f4i98` to `2hxws5`, and the PyG node index equals the id map's index: split
flags agree on every node present in both, and the PyG features are the GraphSAGE
features standardised per column on the train nodes, equal to the last bit on a sample.

**The published split is a single post-id threshold.** The paper's split is the first
twenty days of September 2014 for training and the rest for validation and test. Every
train node has an id at or below 149,474,712 (`2gzrfc`) and every val and test node an
id above it: zero exceptions on either side, in both copies. Taking the train side as
twenty days gives an id-counter rate of 156,892 ids per day, and at that rate the ids
above the threshold span 10.16 days, against the 10 a thirty-day month predicts. The
day assigned to every post below is `(id − min id) / 156,892`.

**Two edge sets exist over the same nodes.** `reddit-G.json` is the paper's graph:
231,443 nodes present, 11,606,919 undirected edges, mean degree 99.6, maximum 3,649,
and 1,522 nodes absent (isolated). `reddit-G_full.json` has all 232,965 nodes and
57,307,946 undirected edges, mean degree 492.0, maximum 21,657, no isolated node. The
PyG copy's 114,615,892 directed edges are exactly the full set, both directions; the
paper's edges are a subset of it. In `reddit-G.json` a link's `source` and `target` are
positions in the node list, not ids, and the probe maps them through the node's id;
read as ids they match 0.2 percent of the full set.

**The stream.** Posts arrive at a flat rate: 7,672 a day over the train days and 7,832
over the rest, with every day between 6,800 and 8,625. An edge exists from the moment
its later post exists, so edge arrivals grow with the graph: on the paper's graph from
29,777 on day 0 to 474,951 on day 19 and 708,931 on day 28; on the full graph from
100,830 to 2,329,212 and 3,581,178. Of the edges arriving from day 20 on, 6,230,303
(53.7 percent) on the paper's graph and 31,165,573 (54.4 percent) on the full, every one
has a new endpoint: 26.5 and 24.9 percent join two new posts, 73.5 and 75.1 percent join
a new post to an old one, and none joins two old posts, which is what the construction
implies since a post's edges are fixed by the users who comment on it. Of the edges that
join a new post to an old one, the old endpoint's day-20 degree decile receives, from the
lowest decile to the highest, 0.6, 2.3, 4.7, 5.5, 5.9, 6.6, 7.7, 10.8, 16.3 and 39.6
percent on the paper's graph, and 0.2, 0.7, 1.5, 2.4, 3.6, 5.2, 7.8, 12.0, 18.8 and 47.8
on the full. Counting a node as a hub by its final degree, 57.3 and 66.7 percent of
arriving edges touch a top-decile node; by its day-20 degree, 29.1 and 36.0 percent.
Mean new edges gained over days 20 to 30 against day-20 degree, log-binned, has slope
0.96 on the paper's graph and 0.98 on the full: linear preferential attachment. The Hill
tail exponent of final degree above the 90th percentile is 3.09 and 2.94, above the 95th
3.26 and 3.17, above the 99th 3.92 and 3.89. Per-node burstiness of edge arrivals in
id-counter time, over nodes with at least twenty arrivals, has median 0.089 (interquartile
0.026 to 0.183) on the paper's graph and 0.156 (0.080 to 0.272) on the full, where 0 is
a Poisson process and 1 is maximally bursty.

**Full recompute on the real graph.** Two-layer GraphSAGE, 602-dim input, untrained
weights, eval mode, fp32, median of five synchronized passes after a warm-up, on the
RTX 3060:

| edge set | path | hidden | ms | peak GiB |
|---|---|---|---|---|
| paper 11.6M | edge_index | 64 | OOM | – |
| paper 11.6M | edge_index | 128 | OOM | – |
| paper 11.6M | CSR | 64 | 217.8 | 2.37 |
| paper 11.6M | CSR | 128 | 241.1 | 2.37 |
| full 57.3M | edge_index | 64 | OOM | – |
| full 57.3M | edge_index | 128 | OOM | – |
| full 57.3M | CSR | 64 | 953.1 | 5.46 |
| full 57.3M | CSR | 128 | 1,043.9 | 5.46 |

The edge_index path is PyG's default, which gathers one message per edge; the CSR path
passes the adjacency as a `torch.sparse_csr_tensor` and SAGEConv aggregates by
sparse-dense matrix multiply. Peak memory on the CSR path does not move with hidden
width, and on both paths the first layer's per-edge tensor, when there is one, is 602
wide, not the hidden width.

## Interpretation

**The insertion stream can be real.** The post id orders posts by creation and is
linear in time to within two percent over the month, checked against the one anchor the
data carries. That is the condition the measurement consultation set for using the real
arrival order as the insertion stream and anchor arm, with the generator owning only
deletions. What the ids do not give is a calendar timestamp inside the day, or the
comment times that would say when an edge appeared in a user's activity rather than
when its later post was created.

**The real stream is growth, and the hot-hub model has no real counterpart in it.** No
arriving edge joins two existing posts. lab/008's ranking put a hot-hub bursty stream
first because it is the model under which the most-consumed nodes are also the most
endangered, with coherent staleness; on this graph the endangered nodes are the old hubs
that keep receiving new neighbours, and the mechanism is preferential attachment with a
slope of about one, not a burst of edges among existing nodes. The share of arriving
edges landing on the top decile, about 40 to 48 percent of old-endpoint edges, is the
hub concentration a calibrated generator should reproduce; burstiness in id time is low,
so a burst parameter set from this graph would be near zero. Whether the synthetic
hot-hub stream should stay in the design is a question for the modelling consultation:
it is the corner that can hurt the claim most, and it is also a corner the real stream
does not visit.

**The edge-count ceiling was a property of the gather path.** lab/004 and the claim it
grounds measured PyG's default path on inputs as wide as the hidden layer. On the real
graph that path does not fit at 64 dimensions on the paper's 11.6M edges, because the
first layer's per-edge tensor is 602 wide; and on the sparse path the full 57.3M-edge
graph fits at 128 with six gigabytes to spare. The admissible band as an edge count
stands for the gather path and does not bound the project: the reference arm's
implementation is the sparse path, and with it both Reddit edge sets and both widths are
admissible. The 217.8 ms at 64 on the paper's graph is within two percent of lab/004's
synthetic 213.6 ms, so the cost ratio against the interaction benchmarks holds.

**Which Reddit is the Reddit post graph is now a choice to declare.** The paper's number
(11.6M edges) and the copy every PyG user loads (57.3M) are different graphs with
different degree distributions. The preregistration names one by archive hash and edge
set, and the pinned checkpoint is trained on that one. The 97.0 F1 in the literature is
on the paper's graph.

## What this corrects

lab/004's Reddit-at-64 rows, and the assertion that Reddit runs out of memory at 96 and
128 dimensions, were true of a synthetic graph on the gather path and are not true of
the real graph on either path. The ledger entry that carries them is superseded in the
commit after this note; lab/004 stays as written.

## Open

- Whether the hot-hub synthetic stream stays in the design now that the real stream
  has no edges among existing nodes; a question for the modelling consultation, with
  these numbers as the calibration it asked for.
- Which edge set the preregistration pins. The paper's graph is the one the published
  F1 and the fidelity study's degree band both refer to; the full graph is what a PyG
  user gets by default.
- Deletions remain the generator's, and nothing here calibrates them: the data
  records no removals.
- The untrained-weights control, the seed-churn pilot and the remaining probes in
  lab/008's list.

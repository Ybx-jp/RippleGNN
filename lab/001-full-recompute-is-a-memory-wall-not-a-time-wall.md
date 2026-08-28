# 001 — Full recompute is a memory wall, not a time wall

**Date:** 2026-08-27 · **Component:** environment probe · **Status:** measured, partly superseded.

> **Superseded in part by lab/004.** The ceiling stated below as "roughly 1-2M nodes"
> was measured at mean degree 10 and names the wrong variable: the governing quantity is
> `edges x hidden_dim`, at ~0.51 GiB per million edges per 128 dims. At mean degree 99 the
> ceiling arrives at 233k nodes. Everything else here stands.

## What was asked

Before any dataset is chosen, does the manifest's premise hold on this box? The premise
is that recomputing every embedding after every change is expensive enough to be worth
avoiding. That is a measurable claim and it had not been measured.

## Observation

Two-layer GraphSAGE, 128-dim features, mean degree 10, full-graph inference on the
RTX 3060, timed with `torch.cuda.synchronize()` on both sides.

| nodes | edges | features | full recompute | peak VRAM |
|---|---|---|---|---|
| 200,000 | 2,000,000 | 0.10 GiB | 0.040 s | 1.38 GiB |
| 1,000,000 | 10,000,000 | 0.48 GiB | 0.204 s | 6.84 GiB |
| 4,000,000 | 40,000,000 | 1.91 GiB | — | OOM above 12 GiB |

Neighbor sampling, measured separately (`NeighborLoader`, `num_neighbors=[10,10]`,
batch 512, `num_workers=0`): 0.33 s per 20k-node epoch at 200k nodes, against 0.023 s
for full-graph inference on the same graph — 15x slower relatively, still sub-second
absolutely. The ratio narrows as the graph grows (53x at 10k, 36x at 50k, 15x at 200k).

Exact kNN over embeddings, chunked so the similarity matrix never fully materializes:
100k x 128 in 1.10 s at 1.6 GiB; 250k in 7.0 s.

## Interpretation

Kept separate from the observation deliberately, because this part is the arguable half.

Full recomputation never becomes slow on this hardware. It becomes *impossible*. Below
roughly 1-2M nodes it costs a fraction of a second; above that it does not fit in VRAM
and must be done by sampling or streaming, and that is where cost reappears. So the cost
dimension that bites here is memory residency and feature I/O, not FLOPs.

This has a sharp consequence for dataset selection. At the scale of the standard citation
benchmarks — Cora 2.7k, CiteSeer 3.3k, PubMed 19.7k nodes — full recompute is
microseconds. Any refresh strategy measured there would show a "speedup" that is
measurement noise and scheduling overhead, and it would look like a result. That is the
trap the `dl` round-1 ticket asked about, and it is now a measured trap rather than a
suspected one.

The corollary for exact kNN: at every scale that fits on this box, exact nearest-neighbor
search is affordable, so no ANN index is needed. That matters beyond convenience — an ANN
index used to measure neighborhood stability contributes its own recall error to the
metric it is being used to take. Exact search removes a confound rather than merely
saving a dependency.

## What this corrects

`CLAUDE.md` and the public README both asserted that 4 CPU cores, not the 12 GB of VRAM,
were the binding constraint, on the reasoning that sampling and mutation replay are
CPU-bound. As stated that was wrong, and it was written before it was measured. The
accurate version: VRAM caps full-graph refresh at roughly 1-2M nodes; past that, sampling
on 4 cores is the constraint. Both documents now say that instead.

## Open

The crossover was measured on synthetic uniform-degree random graphs. Real graphs are
heavy-tailed, and a hub node's neighborhood is where both sampling cost and refresh
locality should behave differently. The number to trust is the shape, not the constant.

Raw probes: `scratchpad/probe_knn.py`, `probe_sampling.py`, `probe_crossover.py`.

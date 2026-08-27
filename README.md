# RippleGNN

Investigating how to maintain useful graph representations as a graph evolves without
paying the full cost of recomputing every embedding after every change.

> Given an evolving graph and a trained inductive GNN, what is the cheapest refresh
> strategy that keeps its embedding space sufficiently faithful for downstream use?

The research contract is `MANIFEST.md`, and it
governs. This project is discovery first: it does not assume a production system ought to
exist, and it does not commit to an architecture before the behavior of the problem is
understood. Systems work is earned by experimental evidence.

Refresh cost is treated as multidimensional — latency, compute, availability,
consistency, tolerated staleness, and the fraction of the graph revisited — with no
presumption that those collapse into one scalar objective. Faithfulness is treated as an
empirical property to be characterized rather than a definition chosen in advance.

## Status

Session zero. The environment and the experimental protocol are in place; no experiment
has been run and no result is claimed.

## Layout

| Path | Role |
|---|---|
| `src/ripple_gnn/` | Library code. |
| `tests/` | pytest. One file per source module. |
| `experiments/` | Pre-registered studies. See `experiments/README.md`. |
| `outputs/` | Generated artifacts. Ignored except committed figures. |

The dependency direction is one-way: `experiments/` may import `src/`, never the reverse.

## Method

Every study under `experiments/` commits its `preregistration.md` before its first run
against real data, and never edits it afterward — the git history of that file is its
pre-registration timestamp. `run.py` takes a pinned dataset and a seed, regenerates
`results.json`, and contains no number that is not computed, so a hypothesis that fails
can falsify the write-up's own text.

Reproducibility is the triple `(pinned dataset, pinned checkpoint, seed)`; a seed alone
reproduces a draw, not a result. Baselines are full recomputation, no refresh, and naive
local refresh — a comparison omitting full recomputation is not a result. Negative and
null results are kept.

## Setup

    uv sync --extra dev
    uv run pytest
    uv run ruff check src tests

Python 3.12 for this checkout (`.python-version`); the package supports `>=3.11`. torch
resolves from an explicitly named CUDA 12.8 index so the lockfile records which build was
used.

Development box, against which all wall-clock measurements should be read: RTX 3060
(12 GB, sm_86), 4 CPU cores, 47 GB RAM.

Measured 2026-08-27 on this box, two-layer GraphSAGE at 128 dims and mean degree 10:
full-graph inference costs 0.040 s at 200k nodes and 0.204 s at 1M nodes, and runs out
of the 12 GiB of VRAM somewhere below 4M nodes. Full recomputation on this hardware
therefore does not become slow, it becomes impossible — VRAM caps full-graph refresh at
roughly 1-2M nodes, and past that, neighbor sampling on 4 cores is the constraint. Any
refresh result measured at citation-benchmark scale (Cora 2.7k, CiteSeer 3.3k, PubMed
19.7k) would be reporting scheduling noise.

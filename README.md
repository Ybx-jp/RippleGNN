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
| `lab/` | The working record: one dated page per thing tried, plus its probe scripts. |
| `ledger/` | Every load-bearing claim, typed and tracked. See `ledger/README.md`. |
| `outputs/` | Generated artifacts. Ignored except committed figures. |

The dependency direction is one-way: `experiments/` may import `src/`, never the reverse.

`lab/` and `experiments/` promise a reader different things and are not interchangeable.
A lab note is cheap, dated, allowed to be wrong, and stays wrong under a banner rather
than being rewritten; nothing in it should be cited as a result. An experiment is
pre-registered and regenerable. Both are published, because for a discovery project the
record of what was tried and discarded is part of the work, not scaffolding around it.

## Method

Every study under `experiments/` commits and **pushes** its `preregistration.md` before
its first run against real data, and never edits it afterward. The push is what
timestamps it: a local commit date is written by the machine that made it, so on a repo
its author controls it is not an independent witness, while the remote's record of when
it received the commit is. `run.py` takes a pinned dataset and a seed, regenerates
`results.json`, and contains no number that is not computed, so a hypothesis that fails
can falsify the write-up's own text.

Reproducibility is the triple `(pinned dataset, pinned checkpoint, seed)`; a seed alone
reproduces a draw, not a result. Baselines are full recomputation, no refresh, and naive
local refresh — a comparison omitting full recomputation is not a result. Negative and
null results are kept.

Claims are tracked rather than remembered. `ledger/` carries every statement something
downstream depends on, typed on two separate axes that are never combined into a score:
an **evidence grade** — how it was established, from `asserted` through `argued`,
`measured`, `controlled`, to `preregistered` — and a **credence**, recorded only where a
claim is genuinely a bet. Anything at `measured` or above names the metric, cohort and
conditions it held under, because the ledger exists to catch a specific failure: a real
measurement, generalized past the conditions it was taken in, read later as a broader
result than it was.

Entries are frozen when written and verdicts append below them, so a claim that falls
keeps its original text and its history. Refuted and superseded claims stay. Where a
claim is restated elsewhere in the repo, the ledger records where, and
`ledger/references.py` reports any standing document still carrying one that has fallen.

The ledger opens with the project's own overturned claims, which is the honest place for
it to start.

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
therefore does not become slow, it becomes impossible.

The ceiling is an edge count rather than a node count, because full-graph message
passing materializes a tensor per edge: measured at ~0.51 GiB per million edges per 128
dims, it arrives between 15M and 20M edges at 128 dims and moves with hidden dimension.
At mean degree 10 that is roughly 1.5M nodes; at mean degree 99 it is 233k. Past it,
neighbor sampling on 4 cores is the constraint. Any refresh result measured at
citation-benchmark scale (Cora 2.7k, CiteSeer 3.3k, PubMed 19.7k) would be reporting
scheduling noise.

"""lab/014 — the gap pilot on ogbn-arxiv's real arrival order, beside the Reddit anchor on the same bins.

The operator's hypothesis: sparse graphs need refresh more often. The fraction law (A0012,
A0013) says the change a node's mean-aggregated embedding suffers under no refresh is set
by the fraction of its neighbourhood that arrived, not by its degree, so it predicts
arxiv's median paper (pre-2018 degree 4) behaves like Reddit's bottom decile (degree 0 to
8), not like Reddit's median post (degree 49). This probe runs lab/012's gap pilot on
arxiv and on the Reddit anchor with one script, one recipe and one set of bins, so the two
graphs can be read side by side by absolute degree and by the fraction of the
neighbourhood that arrived.

Recipe (lab/012, lab/013): five checkpoints trained on the starting graph, one per seed
(two-layer GraphSAGE, mean aggregation, hidden 64, linear head, full-batch Adam at 0.01,
100 epochs). Per checkpoint and per existing node, the gap is the embedding on the
starting graph (what the node keeps under no refresh) against the embedding on the
post-episode graph (the full recompute): head disagreement, kNN@20 loss among existing
nodes, cosine drift and relative L2. The band is two checkpoints differing only in seed,
both on the post-episode graph, mean over the ten pairs. Cells report the mean over five
seeds and the lower 95 percent t limit; a cell whose limit exceeds the band is flagged.

arxiv: starting graph = papers with year <= 2017 (the published train split), undirected
citation edges among them. Episodes: the papers of 2018 (the published validation year),
2018-2019, 2018-2020 (the end of the dataset); and, because the dataset carries no
sub-year clock, two uniform random draws of 5.6 percent of the starting graph's size from
2018's papers, matching the node growth of one Reddit day (seeds 20260904, 20260905).
reddit: lab/012's anchor, the paper edge set before day 20 and one day of the real stream.

    uv run python lab/probe_gap_arxiv.py [arxiv|reddit|reference ...]

`reference` trains the same five checkpoints transductively on arxiv's final graph with the
published train split and reports validation and test accuracy, for comparison with the
published GraphSAGE row. The environment variable EPOCHS (default 100) overrides the
training length for a better-fit control; the recipe is otherwise lab/012's.
"""

import itertools
import os
import sys
import time
from pathlib import Path

import numpy as np
import scipy.sparse as sp
import torch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_gap  # noqa: E402
from probe_gap import K, SEEDS, cell, csr, dev, knn, overlap, train  # noqa: E402

probe_gap.EPOCHS = int(os.environ.get("EPOCHS", probe_gap.EPOCHS))

DATA = Path(__file__).resolve().parents[1] / "data"
SAMPLE_FRACTION = 8625 / 153430  # one Reddit day's new posts over the day-20 graph
SAMPLE_SEEDS = (20260904, 20260905)
DEGREE_BINS = ((0, 0), (1, 2), (3, 5), (6, 8), (9, 22), (23, 52), (53, 151), (152, 10**9))
FRACTION_BINS = ((0.0, 0.05), (0.05, 0.1), (0.1, 0.25), (0.25, 0.5), (0.5, 1.0))


def load(dataset):
    if dataset == "arxiv":
        d = np.load(DATA / "arxiv" / "derived" / "arxiv.npz")
        t = d["year"].astype(np.float64)
        lo, hi = d["lo"].astype(np.int64), d["hi"].astype(np.int64)
        x, y, trainable = d["x"], d["y"], d["split"] == 1
        old = t < 2018
        rng = [np.random.default_rng(s) for s in SAMPLE_SEEDS]
        pool = np.flatnonzero(t == 2018)
        m = int(round(SAMPLE_FRACTION * old.sum()))
        episodes = [("2018", t < 2019), ("2018-2019", t < 2020), ("2018-2020", t < 2021)]
        for s, r in zip(SAMPLE_SEEDS, rng):
            pick = np.zeros(len(t), bool)
            pick[r.choice(pool, m, replace=False)] = True
            episodes.append((f"2018, uniform draw of {m} papers (seed {s})", old | pick))
        return x, y, lo, hi, trainable, old, episodes, "papers"
    d = np.load(DATA / "reddit" / "pyg" / "raw" / "reddit_data.npz")
    st = np.load(DATA / "reddit" / "derived" / "reddit_stream.npz")
    t = st["day"]
    lo, hi = st["paper_lo"].astype(np.int64), st["paper_hi"].astype(np.int64)
    old = t < 20.0
    return (
        d["feature"].astype(np.float32),
        d["label"].astype(np.int64),
        lo,
        hi,
        d["node_types"] == 1,
        old,
        [("day 20 + 1 day", t < 21.0)],
        "posts",
    )


def episode(name, present, seeds, x, y, lo, hi, old, train_mask, adj_old, unit):
    n = len(old)
    new = present & ~old
    e_old = old[lo] & old[hi]
    e_ep = present[lo] & present[hi] & ~e_old
    assert (new[lo[e_ep]] | new[hi[e_ep]]).all(), "an arriving edge joins two existing nodes"
    touched1 = np.zeros(n, bool)
    touched1[lo[e_ep]] = True
    touched1[hi[e_ep]] = True
    touched1 &= old
    A_old = sp.coo_matrix(
        (
            np.ones(2 * int(e_old.sum()), np.int8),
            (np.r_[lo[e_old], hi[e_old]], np.r_[hi[e_old], lo[e_old]]),
        ),
        shape=(n, n),
    ).tocsr()
    touched2 = (A_old @ touched1.astype(np.int8)).astype(bool) & old & ~touched1
    untouched = old & ~touched1 & ~touched2
    deg_old = np.bincount(np.r_[lo[e_old], hi[e_old]], minlength=n)
    deg_ep = np.bincount(np.r_[lo[e_old | e_ep], hi[e_old | e_ep]], minlength=n)
    frac = np.where(deg_ep > 0, (deg_ep - deg_old) / np.maximum(deg_ep, 1), 0.0)
    print(
        f"\n=== {name}: new {unit} {int(new.sum())} ({100 * new.sum() / old.sum():.1f}% of the starting graph), "
        f"arriving edges {int(e_ep.sum())} ({100 * e_ep.sum() / e_old.sum():.1f}% of its edges); existing {unit} touched 1-hop "
        f"{int(touched1.sum())}, 2-hop only {int(touched2.sum())}, untouched {int(untouched.sum())}"
    )
    adj_ep = csr(lo[e_old | e_ep], hi[e_old | e_ep], n)
    idx = np.flatnonzero(old)
    idx_t = torch.from_numpy(idx).to(dev)
    new_t = torch.from_numpy(new).to(dev)
    dis, kl, cosd, rel, pf_all, nf_all, accs = [], [], [], [], [], [], []
    for sage, head in seeds:
        with torch.no_grad():
            zs = sage(x, adj_old)[idx_t]
            z_all = sage(x, adj_ep)
            p_all = head(z_all).argmax(1)
            accs.append(
                (
                    (p_all[train_mask] == y[train_mask]).float().mean().item(),
                    (p_all[new_t] == y[new_t]).float().mean().item(),
                )
            )
            zf = z_all[idx_t]
            ps, pf = head(zs).argmax(1), p_all[idx_t]
            del z_all, p_all
            c = 1 - torch.nn.functional.cosine_similarity(zs, zf, dim=1)
            r = (zf - zs).norm(dim=1) / zf.norm(dim=1)
        ns, nf = knn(zs, K), knn(zf, K)
        dis.append((ps != pf).cpu().numpy())
        kl.append(1 - overlap(ns, nf))
        cosd.append(c.cpu().numpy())
        rel.append(r.cpu().numpy())
        pf_all.append(pf.cpu().numpy())
        nf_all.append(nf)
        del zs, zf, ps, pf, c, r
        torch.cuda.empty_cache()
    del adj_ep
    torch.cuda.empty_cache()
    dis, kl, cosd, rel = (np.stack(a) for a in (dis, kl, cosd, rel))
    pairs = list(itertools.combinations(range(len(seeds)), 2))
    b_dis = np.stack([pf_all[i] != pf_all[j] for i, j in pairs])
    b_kl = np.stack([1 - overlap(nf_all[i], nf_all[j]) for i, j in pairs])
    accs = np.array(accs)
    print(
        f"full-recompute accuracy on the post-episode graph, range over seeds: training {unit} "
        f"{accs[:, 0].min():.4f}-{accs[:, 0].max():.4f}, new {unit} {accs[:, 1].min():.4f}-{accs[:, 1].max():.4f}"
    )
    un = untouched[idx]
    print(
        f"check: cosine drift on untouched {unit} max {cosd[:, un].max() if un.any() else float('nan'):.2e}; "
        f"on 1-hop {unit}, min over seeds of the mean {cosd[:, touched1[idx]].mean(1).min():.4f}"
    )
    hdr = (
        f"{'cell':<34} {'n':>7} {'deg':>6} {'frac':>5} | {'gap dis':>8} {'lcl':>7} {'band':>7} | "
        f"{'gap kNN':>8} {'band':>7} | {'cos':>7} {'relL2':>7}"
    )

    def row(label, m):
        sel = m[idx]
        if not sel.any():
            return
        g, q = cell(dis, sel), cell(kl, sel)
        bd, bq = b_dis[:, sel].mean(), b_kl[:, sel].mean()
        flag = " *" if g[3] > bd else ""
        print(
            f"{label:<34} {int(sel.sum()):>7} {deg_old[m].mean():>6.1f} {frac[m].mean():>5.2f} | "
            f"{g[0]:>8.4f} {g[3]:>7.4f} {bd:>7.4f} | {q[0]:>8.4f} {bq:>7.4f} | "
            f"{cosd[:, sel].mean():>7.4f} {rel[:, sel].mean():>7.4f}{flag}"
        )

    print(
        "* marks a cell whose disagreement lower limit clears the band; deg and frac are means over the cell"
    )
    print(hdr)
    for label, m in (
        ("existing, all", old),
        ("touched 1-hop", touched1),
        ("touched 2-hop only", touched2),
        ("untouched", untouched),
    ):
        row(label, m)
    print(f"\nby starting-graph degree, all existing {unit}; then those touched at one hop")
    print(hdr)
    for a, b in DEGREE_BINS:
        row(f"degree {a}-{b if b < 10**9 else 'up'}", old & (deg_old >= a) & (deg_old <= b))
    for a, b in DEGREE_BINS:
        row(
            f"degree {a}-{b if b < 10**9 else 'up'}, touched",
            old & touched1 & (deg_old >= a) & (deg_old <= b),
        )
    print(f"\nby the fraction of the post-episode neighbourhood that arrived, touched {unit}")
    print(hdr)
    for a, b in FRACTION_BINS:
        row(f"arrived fraction {a:g}-{b:g}", old & touched1 & (frac > a) & (frac <= b))
    print(f"\nthe same fraction bins, {unit} of starting degree 1-8 and 9 and up")
    print(hdr)
    for a, b in FRACTION_BINS:
        row(
            f"fraction {a:g}-{b:g}, degree 1-8",
            old & touched1 & (frac > a) & (frac <= b) & (deg_old >= 1) & (deg_old <= 8),
        )
    for a, b in FRACTION_BINS:
        row(
            f"fraction {a:g}-{b:g}, degree 9-up",
            old & touched1 & (frac > a) & (frac <= b) & (deg_old >= 9),
        )


def run(dataset):
    t0 = time.time()
    x_np, y_np, lo, hi, trainable, old, episodes, unit = load(dataset)
    n = len(old)
    e_old = old[lo] & old[hi]
    x = torch.from_numpy(x_np).to(dev)
    y = torch.from_numpy(y_np).to(dev)
    train_mask = torch.from_numpy(old & trainable).to(dev)
    adj_old = csr(lo[e_old], hi[e_old], n)
    print(
        f"\n##### {dataset}: checkpoints on the starting graph, {int(old.sum())} {unit}, {int(e_old.sum())} edges, "
        f"{x.shape[1]} features, {int(y.max()) + 1} classes, {int(train_mask.sum())} training {unit}, "
        f"{probe_gap.EPOCHS} epochs"
    )
    seeds = []
    for seed in SEEDS:
        t = time.time()
        sage, head = train(x, adj_old, y, train_mask, seed)
        with torch.no_grad():
            acc = (
                (head(sage(x, adj_old)).argmax(1)[train_mask] == y[train_mask])
                .float()
                .mean()
                .item()
            )
        seeds.append((sage, head))
        print(
            f"seed {seed}: trained {time.time() - t:.0f} s, training accuracy on the starting graph {acc:.4f}",
            flush=True,
        )
    for name, present in episodes:
        t = time.time()
        episode(name, present, seeds, x, y, lo, hi, old, train_mask, adj_old, unit)
        print(f"{name}: {time.time() - t:.0f} s", flush=True)
    print(
        f"{dataset}: peak VRAM {torch.cuda.max_memory_allocated() / 2**30:.2f} GiB; total {time.time() - t0:.0f} s"
    )
    del x, y, train_mask, adj_old, seeds
    torch.cuda.empty_cache()
    torch.cuda.reset_peak_memory_stats()


def reference():
    """Transductive: train on the final graph with the published split, score valid and test."""
    d = np.load(DATA / "arxiv" / "derived" / "arxiv.npz")
    lo, hi = d["lo"].astype(np.int64), d["hi"].astype(np.int64)
    x = torch.from_numpy(d["x"]).to(dev)
    y = torch.from_numpy(d["y"]).to(dev)
    split = torch.from_numpy(d["split"]).to(dev)
    adj = csr(lo, hi, len(d["y"]))
    print(
        f"\n##### arxiv reference: transductive on the final graph, published split, {probe_gap.EPOCHS} epochs"
    )
    for seed in SEEDS:
        sage, head = train(x, adj, y, split == 1, seed)
        with torch.no_grad():
            p = head(sage(x, adj)).argmax(1)
        acc = [(p[split == k] == y[split == k]).float().mean().item() for k in (1, 2, 3)]
        print(f"seed {seed}: train {acc[0]:.4f} valid {acc[1]:.4f} test {acc[2]:.4f}", flush=True)


def main():
    for dataset in sys.argv[1:] or ("arxiv", "reddit"):
        if dataset == "reference":
            reference()
        else:
            run(dataset)


if __name__ == "__main__":
    sys.exit(main())

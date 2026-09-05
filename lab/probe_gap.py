"""lab/012 — the gap pilot: no refresh against full recompute across five seeds, beside the seed-churn band.

lab/008's fourth probe. The measurement consultation's margin ordering takes the denominator
as the lower confidence limit, across at least five seeds, of the gap between doing nothing
and full recomputation, with a pre-registered gap-floor eligibility rule: a cell whose gap
does not clear the no-op band has no headroom and is reported, never dropped. lab/008
specified the pilot at three generator settings; lab/009 made the real arrival order the
insertion stream, so this probe runs it at three lengths of the real growth stream
instead, and the seed-churn band of lab/011 is recomputed in the same run on the same
nodes so that gap and band are read off one set of checkpoints.

Setup as lab/011: five checkpoints trained on the paper edge set as it stands before the
episode (two-layer GraphSAGE 602 -> 64 -> 64, linear head, full-batch Adam, 100 epochs),
one per seed. For each episode length, per checkpoint:

  stale   the checkpoint run on the pre-episode graph: the embedding an old post keeps
          under no refresh
  full    the checkpoint run on the post-episode graph: the full recompute

and per old post, between stale and full of the same checkpoint (the gap):

  disagreement   the head's argmax differs
  kNN@20 loss    1 - overlap of the post's 20 nearest cosine neighbours among old posts
  cosine drift   1 - cos(stale, full)
  relative L2    |full - stale| / |full|

and between full and full of two checkpoints (the band): disagreement and kNN@20 loss on
the same old posts. Cells are the touched strata of lab/011 and degree deciles on the
post-episode graph. Across seeds each gap cell reports mean, min, max and the lower
limit of a 95 percent t interval (n = 5); the band is the mean over the ten seed pairs.
Reads data/reddit/derived/reddit_stream.npz.

    python lab/probe_gap.py [start_day] [length_days ...]

Defaults: day 20; one hour, six hours, one day. The environment variable AGGR selects the
SAGEConv aggregation (mean, the default, or sum) for the sum-control arm of the design.
"""

import itertools
import os
import sys
import time
from pathlib import Path

import numpy as np
import scipy.sparse as sp
import torch
from torch_geometric.nn import SAGEConv
from torch_geometric.utils import to_torch_csr_tensor

ROOT = Path(__file__).resolve().parents[1] / "data" / "reddit"
SEEDS = (20260903, 20260904, 20260905, 20260906, 20260907)
EPOCHS = 100
LR = 0.01
HIDDEN = 64
K = 20
AGGR = os.environ.get("AGGR", "mean")
T95_4DF = 2.776  # two-sided 95 percent, four degrees of freedom
EPISODE_DAY = 20.0
EPISODE_LENS = (1 / 24, 0.25, 1.0)
CHUNK = 4096
dev = torch.device("cuda")


class Sage(torch.nn.Module):
    def __init__(self, d_in, d_h):
        super().__init__()
        self.c1 = SAGEConv(d_in, d_h, aggr=AGGR)
        self.c2 = SAGEConv(d_h, d_h, aggr=AGGR)

    def forward(self, x, adj):
        return self.c2(torch.relu(self.c1(x, adj)), adj)


def csr(lo, hi, n):
    ei = torch.from_numpy(np.stack([np.r_[lo, hi], np.r_[hi, lo]]).astype(np.int64)).to(dev)
    adj = to_torch_csr_tensor(ei, size=(n, n))
    del ei
    return adj


def train(x, adj, y, mask, seed):
    torch.manual_seed(seed)
    sage = Sage(x.shape[1], HIDDEN).to(dev).train()
    head = torch.nn.Linear(HIDDEN, int(y.max()) + 1).to(dev)
    opt = torch.optim.Adam(list(sage.parameters()) + list(head.parameters()), lr=LR)
    for _ in range(EPOCHS):
        opt.zero_grad()
        torch.nn.functional.cross_entropy(head(sage(x, adj))[mask], y[mask]).backward()
        opt.step()
    return sage.eval(), head.eval()


@torch.no_grad()
def knn(z, k):
    """Indices of the k nearest cosine neighbours of every row of z (self excluded), exact."""
    z = torch.nn.functional.normalize(z, dim=1)
    out = torch.empty(z.shape[0], k, dtype=torch.int32, device=dev)
    for s in range(0, z.shape[0], CHUNK):
        sim = z[s : s + CHUNK] @ z.T
        sim[
            torch.arange(sim.shape[0], device=dev), torch.arange(s, s + sim.shape[0], device=dev)
        ] = -2
        out[s : s + CHUNK] = sim.topk(k, dim=1).indices.to(torch.int32)
    return out.cpu().numpy()


def overlap(a, b):
    """Per-row |a ∩ b| / k for two [n, k] index arrays."""
    a = np.sort(a, axis=1)
    b = np.sort(b, axis=1)
    both = np.concatenate([a, b], axis=1)
    both.sort(axis=1)
    return (both[:, 1:] == both[:, :-1]).sum(1) / a.shape[1]


def cell(values, sel):
    """Mean of each seed's cell mean: values is [seeds, n]; returns (mean, min, max, lcl)."""
    if not sel.any():
        return (float("nan"),) * 4
    m = values[:, sel].mean(1)
    return m.mean(), m.min(), m.max(), m.mean() - T95_4DF * m.std(ddof=1) / np.sqrt(len(m))


def episode(length, seeds, st, day, lo, hi, x, y, old, train_mask, adj_old):
    n_all = len(day)
    present = day < EPISODE_DAY + length
    new = present & ~old
    e_old = old[lo] & old[hi]
    e_ep = present[lo] & present[hi] & ~e_old
    n_new = int(new.sum())
    touched1 = np.zeros(n_all, bool)
    touched1[lo[e_ep]] = True
    touched1[hi[e_ep]] = True
    touched1 &= old
    A_old = sp.coo_matrix(
        (
            np.ones(2 * int(e_old.sum()), np.int8),
            (np.r_[lo[e_old], hi[e_old]], np.r_[hi[e_old], lo[e_old]]),
        ),
        shape=(n_all, n_all),
    ).tocsr()
    touched2 = ((A_old @ touched1.astype(np.int32)) > 0) & old & ~touched1
    untouched = old & ~touched1 & ~touched2
    deg = np.bincount(np.r_[lo[e_old | e_ep], hi[e_old | e_ep]], minlength=n_all)
    hours = length * 24
    print(
        f"\n=== episode: day {EPISODE_DAY:g} for {hours:g} h: new posts {n_new}, arriving edges {int(e_ep.sum())}; "
        f"old posts touched 1-hop {int(touched1.sum())}, 2-hop only {int(touched2.sum())}, untouched {int(untouched.sum())}"
    )
    adj_ep = csr(lo[e_old | e_ep], hi[e_old | e_ep], n_all)
    idx = np.flatnonzero(old)  # every figure is on old posts; new posts have no stale embedding
    idx_t = torch.from_numpy(idx).to(dev)

    dis, kl, cosd, rel, preds_full, nbrs_full, accs = [], [], [], [], [], [], []
    new_t = torch.from_numpy(new).to(dev)
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
        preds_full.append(pf.cpu().numpy())
        nbrs_full.append(nf)
        del zs, zf, ps, pf, c, r
        torch.cuda.empty_cache()
    dis, kl, cosd, rel = (np.stack(a) for a in (dis, kl, cosd, rel))
    pairs = list(itertools.combinations(range(len(seeds)), 2))
    b_dis = np.stack([preds_full[i] != preds_full[j] for i, j in pairs])
    b_kl = np.stack([1 - overlap(nbrs_full[i], nbrs_full[j]) for i, j in pairs])
    del adj_ep
    torch.cuda.empty_cache()

    accs = np.array(accs)
    print(
        f"full-recompute accuracy on the post-episode graph, range over seeds: training posts "
        f"{accs[:, 0].min():.4f}-{accs[:, 0].max():.4f}, new posts {accs[:, 1].min():.4f}-{accs[:, 1].max():.4f}"
    )
    # verifier check: an untouched post's two-layer output cannot depend on the arriving edges
    un = untouched[idx]
    print(
        f"check: cosine drift on untouched posts max {cosd[:, un].max() if un.any() else float('nan'):.2e}, "
        f"on 1-hop posts min over seeds of the mean {cosd[:, touched1[idx]].mean(1).min():.4f}"
    )

    strata = {
        "old, all": old,
        "old, touched 1-hop": touched1,
        "old, touched 2-hop only": touched2,
        "old, untouched": untouched,
    }
    hdr = (
        f"{'cell':<26} {'n':>7} | {'gap dis':>8} {'min':>7} {'max':>7} {'lcl':>7} {'band':>7} | "
        f"{'gap kNN':>8} {'min':>7} {'max':>7} {'lcl':>7} {'band':>7} | {'cos':>7} {'relL2':>7}"
    )

    def row(name, m):
        sel = m[idx]
        g = cell(dis, sel)
        q = cell(kl, sel)
        bd = b_dis[:, sel].mean() if sel.any() else float("nan")
        bq = b_kl[:, sel].mean() if sel.any() else float("nan")
        c = cosd[:, sel].mean() if sel.any() else float("nan")
        r = rel[:, sel].mean() if sel.any() else float("nan")
        flag = "" if not sel.any() else (" *" if g[3] > bd else "")
        print(
            f"{name:<26} {int(sel.sum()):>7} | {g[0]:>8.4f} {g[1]:>7.4f} {g[2]:>7.4f} {g[3]:>7.4f} {bd:>7.4f} | "
            f"{q[0]:>8.4f} {q[1]:>7.4f} {q[2]:>7.4f} {q[3]:>7.4f} {bq:>7.4f} | {c:>7.4f} {r:>7.4f}{flag}"
        )

    print(
        "\ngap (stale vs full, same seed; mean/min/max/lcl over 5 seeds) beside band (full vs full across seeds, mean over 10 pairs)"
    )
    print("* marks a cell whose disagreement lcl clears the band")
    print(hdr)
    for name, m in strata.items():
        row(name, m)

    print(
        "\nby degree decile on the post-episode graph, old posts; then the 1-hop-touched posts of each decile"
    )
    print(hdr)
    d_old = deg[old]
    edges = np.quantile(d_old, np.linspace(0, 1, 11))
    band = np.clip(np.searchsorted(edges, deg, side="right") - 1, 0, 9)
    for b in range(10):
        row(f"decile {b} ({int(edges[b])}-{int(edges[b + 1])})", old & (band == b))
    for b in range(10):
        row(f"decile {b}, touched 1-hop", old & (band == b) & touched1)


def main():
    global EPISODE_DAY, EPISODE_LENS
    if len(sys.argv) > 1:
        EPISODE_DAY = float(sys.argv[1])
    if len(sys.argv) > 2:
        EPISODE_LENS = tuple(float(a) for a in sys.argv[2:])
    t0 = time.time()
    data = np.load(ROOT / "pyg" / "raw" / "reddit_data.npz")
    st = np.load(ROOT / "derived" / "reddit_stream.npz")
    day = st["day"]
    n_all = len(day)
    lo, hi = st["paper_lo"].astype(np.int64), st["paper_hi"].astype(np.int64)
    old = day < EPISODE_DAY
    e_old = old[lo] & old[hi]
    x = torch.from_numpy(data["feature"]).to(torch.float32).to(dev)
    y = torch.from_numpy(data["label"]).to(torch.long).to(dev)
    train_mask = torch.from_numpy(old & (data["node_types"] == 1)).to(dev)
    adj_old = csr(lo[e_old], hi[e_old], n_all)
    print(
        f"checkpoints on the graph before day {EPISODE_DAY:g}: {int(old.sum())} posts, {int(e_old.sum())} edges"
    )
    seeds = []
    for seed in SEEDS:
        t = time.time()
        seeds.append(train(x, adj_old, y, train_mask, seed))
        print(f"seed {seed}: trained {time.time() - t:.0f} s", flush=True)
    for length in EPISODE_LENS:
        t = time.time()
        episode(length, seeds, st, day, lo, hi, x, y, old, train_mask, adj_old)
        print(f"episode {length * 24:g} h: {time.time() - t:.0f} s", flush=True)
    print(
        f"\npeak VRAM {torch.cuda.max_memory_allocated() / 2**30:.2f} GiB; total {time.time() - t0:.0f} s"
    )


if __name__ == "__main__":
    sys.exit(main())

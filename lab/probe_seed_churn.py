"""lab/011 — seed churn on a pilot episode: full recompute against full recompute across five seeds.

lab/008's third probe. The measurement consultation made behavioural consistency the
downstream arm — the disagreement rate of a fixed head between the refreshed and the
fully recomputed space, stratified to the nodes a mutation touched — with
full-recompute-versus-full-recompute churn across seeds as its denominator, and warned
that a saturated task compresses disagreement. This probe measures that denominator on
one real episode of the Reddit post graph's growth stream.

Episode: the graph on the paper edge set at the end of day 19 (the training split,
153,430 posts) receives day 20 (the first val/test day: 8,625 posts and the edges they
bring). Five checkpoints are trained on the day-19 graph, one per seed, identical in
everything but the seed (two-layer GraphSAGE 602 -> 64 -> 64, linear head, full-batch
Adam, 100 epochs, the settings of lab/010). Each checkpoint is then run once on the
day-20 graph: that is the full recompute. Between every pair of seeds, per node:

  disagreement   the two heads' argmax labels differ
  kNN@20 loss    1 - overlap of the node's 20 nearest cosine neighbours in the two spaces

reported overall and by stratum — new posts, old posts touched at one hop (incident to
an arriving edge), old posts touched at two hops only, old posts untouched — and by
degree decile among old posts. Reads data/reddit/derived/reddit_stream.npz.

    python lab/probe_seed_churn.py [start_day] [length_days]

The checkpoints are trained on the graph before start_day; the episode inserts the posts
created in [start_day, start_day + length_days). Defaults: day 20, one day.
"""

import itertools
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
EPISODE_DAY = 20.0  # the first day past the published training split; argv[1] overrides
EPISODE_LEN = 1.0  # days of the growth stream in the episode; argv[2] overrides
CHUNK = 4096
dev = torch.device("cuda")


class Sage(torch.nn.Module):
    def __init__(self, d_in, d_h):
        super().__init__()
        self.c1 = SAGEConv(d_in, d_h)
        self.c2 = SAGEConv(d_h, d_h)

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


def main():
    global EPISODE_DAY, EPISODE_LEN
    if len(sys.argv) > 1:
        EPISODE_DAY = float(sys.argv[1])
    if len(sys.argv) > 2:
        EPISODE_LEN = float(sys.argv[2])
    t0 = time.time()
    data = np.load(ROOT / "pyg" / "raw" / "reddit_data.npz")
    st = np.load(ROOT / "derived" / "reddit_stream.npz")
    day = st["day"]
    n_all = len(day)
    lo, hi, ed = st["paper_lo"].astype(np.int64), st["paper_hi"].astype(np.int64), st["paper_day"]
    assert np.allclose(ed, np.maximum(day[lo], day[hi]), atol=1e-3), (
        "edge day is the later endpoint's day"
    )

    old = day < EPISODE_DAY
    present = day < EPISODE_DAY + EPISODE_LEN
    new = present & ~old
    e_old = old[lo] & old[hi]
    e_ep = present[lo] & present[hi] & ~e_old
    assert (new[lo[e_ep]] | new[hi[e_ep]]).all(), "every episode edge has a new endpoint"
    n_old, n_new = int(old.sum()), int(new.sum())
    print(
        f"episode: from day {EPISODE_DAY:g} for {EPISODE_LEN:g} days; old posts {n_old}, new posts {n_new}, "
        f"old edges {int(e_old.sum())}, arriving edges {int(e_ep.sum())} "
        f"(among which old-endpoint edges {int((old[lo[e_ep]] | old[hi[e_ep]]).sum())})"
    )

    # strata among old posts: touched at one hop, at two hops only, untouched
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
    touched2 = (A_old @ touched1.astype(np.int8)).astype(bool) & old & ~touched1
    untouched = old & ~touched1 & ~touched2
    deg21 = np.bincount(np.r_[lo[e_old | e_ep], hi[e_old | e_ep]], minlength=n_all)
    print(
        f"old posts touched at one hop {int(touched1.sum())}, at two hops only {int(touched2.sum())}, "
        f"untouched {int(untouched.sum())}"
    )
    print(
        f"mean degree on the day-{EPISODE_DAY:g} graph: one-hop {deg21[touched1].mean():.1f}, "
        f"two-hop {deg21[touched2].mean():.1f}, untouched {deg21[untouched].mean():.1f}, new {deg21[new].mean():.1f}"
    )

    x = torch.from_numpy(data["feature"]).to(torch.float32).to(dev)
    y = torch.from_numpy(data["label"]).to(torch.long).to(dev)
    split = data["node_types"]
    train_mask = torch.from_numpy(old & (split == 1)).to(dev)
    adj_old = csr(lo[e_old], hi[e_old], n_all)
    adj_ep = csr(lo[e_old | e_ep], hi[e_old | e_ep], n_all)

    # nodes absent on day 20 are isolated in both adjacencies; they are dropped from every figure
    idx = np.flatnonzero(present)
    preds, nbrs, accs = [], [], []
    for seed in SEEDS:
        t = time.time()
        sage, head = train(x, adj_old, y, train_mask, seed)
        with torch.no_grad():
            z = sage(x, adj_ep)  # the full recompute on the episode's graph
            p = head(z).argmax(1)
        acc = {
            name: (p[m] == y[m]).float().mean().item()
            for name, m in (
                ("train", train_mask),
                ("new", torch.from_numpy(new).to(dev)),
            )
        }
        preds.append(p.cpu().numpy()[idx])
        nbrs.append(knn(z[idx], K))
        accs.append(acc)
        print(
            f"seed {seed}: trained {time.time() - t:.0f} s; accuracy on the day-{EPISODE_DAY:g} graph: "
            f"train {acc['train']:.4f}, new posts {acc['new']:.4f}",
            flush=True,
        )
        del sage, head, z, p
        torch.cuda.empty_cache()

    # pairwise churn between seeds, per node
    pairs = list(itertools.combinations(range(len(SEEDS)), 2))
    dis = np.stack([preds[i] != preds[j] for i, j in pairs])  # [pairs, n_present]
    kl = np.stack([1 - overlap(nbrs[i], nbrs[j]) for i, j in pairs])
    strata = {
        "all present": present,
        "new posts": new,
        "old, touched 1-hop": touched1,
        "old, touched 2-hop only": touched2,
        "old, untouched": untouched,
        "old, all": old,
    }
    print(
        f"\nchurn between full recomputes across {len(SEEDS)} seeds ({len(pairs)} pairs), on the day-{EPISODE_DAY:g} graph"
    )
    print(
        f"{'stratum':<26} {'n':>7} {'disagree mean':>14} {'min':>7} {'max':>7} {'kNN@20 loss mean':>17} {'min':>7} {'max':>7}"
    )
    for name, m in strata.items():
        sel = m[idx]
        d = dis[:, sel].mean(1)
        q = kl[:, sel].mean(1)
        print(
            f"{name:<26} {int(sel.sum()):>7} {d.mean():>14.4f} {d.min():>7.4f} {d.max():>7.4f} {q.mean():>17.4f} {q.min():>7.4f} {q.max():>7.4f}"
        )

    # by degree decile among old posts, with the touched fraction of each decile
    print(f"\nold posts by degree decile on the day-{EPISODE_DAY:g} graph")
    print(
        f"{'decile':>6} {'deg range':>15} {'n':>7} {'touched1':>8} {'disagree':>9} {'kNN loss':>9} {'dis touched1':>12} {'dis untouched':>13}"
    )
    d_old = deg21[old]
    edges = np.quantile(d_old, np.linspace(0, 1, 11))
    band = np.clip(np.searchsorted(edges, deg21, side="right") - 1, 0, 9)
    for b in range(10):
        m = old & (band == b)
        sel = m[idx]
        t1 = (m & touched1)[idx]
        un = (m & untouched)[idx]
        print(
            f"{b:>6} {int(edges[b]):>7}-{int(edges[b + 1]):<7} {int(sel.sum()):>7} {t1.sum() / max(sel.sum(), 1):>8.3f} "
            f"{dis[:, sel].mean():>9.4f} {kl[:, sel].mean():>9.4f} "
            f"{dis[:, t1].mean() if t1.any() else float('nan'):>12.4f} {dis[:, un].mean() if un.any() else float('nan'):>13.4f}"
        )

    # the saturation bound: pairwise disagreement cannot exceed the sum of the two error rates
    print(
        f"\nmean pairwise error on new posts {np.mean([a['new'] for a in accs]):.4f} -> disagreement is bounded by "
        f"{2 * (1 - np.mean([a['new'] for a in accs])):.4f} there; on train posts by {2 * (1 - np.mean([a['train'] for a in accs])):.4f}"
    )
    print(f"total {time.time() - t0:.0f} s")


if __name__ == "__main__":
    sys.exit(main())

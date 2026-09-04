"""lab/013 — the gap pilot at the adversarial end: mutations of existing posts, and long horizons.

lab/012 ran the gap pilot on the real growth stream, which only adds posts and their edges
and is the least adversarial stream in lab/008's ranking. This probe runs the same pilot,
same five checkpoints, on mutations that change the existing graph — the corner of the
design where a refresh is expected to matter — and on the real stream at three and ten
days. The gap is a checkpoint's embedding of an existing post on the pre-mutation graph
against the same checkpoint's on the post-mutation graph; the band is two checkpoints
differing only in seed, both on the post-mutation graph. Metrics, strata and the
eligibility rule are lab/012's (lab/probe_gap.py, whose helpers this script imports).

Arms, all on the graph before day 20 (paper edge set), with the arm's random draw seeded
by MUTATION_SEED:

  uniform-delete f    delete a uniform random fraction f of all edges
  uniform-insert f    add f * |E| edges between uniform random pairs of existing posts
  hub-burst f         the top one percent of posts by degree each receive round(f * degree)
                      new edges to uniform random existing posts of a different subreddit
  hub-shift f         the same hubs each lose a Bernoulli(f) share of their edges to
                      same-subreddit neighbours, each replaced by an edge to a uniform random
                      existing post of a different subreddit (degree preserved)
  growth d            the real stream for d days from day 20 (lab/012's episode)

Targets are the hubs for the hub arms and the endpoints of the changed edges otherwise.
Strata: targets, touched at one hop (endpoint of a changed edge), touched at two hops only
(a pre-mutation neighbour of one), untouched; and degree deciles on the pre-mutation graph,
so that the hubs are the same posts in every arm.

    python lab/probe_gap_adversarial.py [arm ...]

Arms are given as name:setting, e.g. hub-burst:0.5 growth:3. Default: the full grid.
"""

import itertools
import sys
import time
from pathlib import Path

import numpy as np
import scipy.sparse as sp
import torch

sys.path.insert(0, str(Path(__file__).resolve().parent))
from probe_gap import EPISODE_DAY, K, SEEDS, cell, csr, dev, knn, overlap, train  # noqa: E402

ROOT = Path(__file__).resolve().parents[1] / "data" / "reddit"
MUTATION_SEED = 20260904
HUB_FRACTION = 0.01
GRID = (
    ("uniform-delete", 0.01),
    ("uniform-delete", 0.05),
    ("uniform-delete", 0.20),
    ("uniform-insert", 0.05),
    ("hub-burst", 0.1),
    ("hub-burst", 0.5),
    ("hub-burst", 1.0),
    ("hub-shift", 0.25),
    ("hub-shift", 0.5),
    ("hub-shift", 1.0),
    ("growth", 1.0),
    ("growth", 3.0),
    ("growth", 10.0),
)


def other_label_partners(rng, n_draw, label, pool, own_label):
    """Uniform random members of pool whose label differs from own_label, one per row."""
    w = rng.choice(pool, size=n_draw)
    for _ in range(20):
        bad = label[w] == own_label
        if not bad.any():
            break
        w[bad] = rng.choice(pool, size=int(bad.sum()))
    return w


def undirected_unique(lo, hi):
    a, b = np.minimum(lo, hi), np.maximum(lo, hi)
    keep = a != b
    pairs = np.unique(np.stack([a[keep], b[keep]], 1), axis=0)
    return pairs[:, 0], pairs[:, 1]


def mutate(arm, f, lo0, hi0, label, old, day, lo_all, hi_all, deg0, rng):
    """Return (lo, hi) of the post-mutation edge set, the targets mask, and a description."""
    n = len(label)
    pool = np.flatnonzero(old)
    if arm == "growth":
        present = day < EPISODE_DAY + f
        keep = present[lo_all] & present[hi_all]
        targets = np.zeros(n, bool)
        e_new = keep & ~(old[lo_all] & old[hi_all])
        targets[lo_all[e_new]] = True
        targets[hi_all[e_new]] = True
        targets &= old
        return (
            lo_all[keep],
            hi_all[keep],
            targets,
            f"{int(e_new.sum())} arriving edges, {int((present & ~old).sum())} new posts",
        )
    if arm == "uniform-delete":
        drop = rng.random(len(lo0)) < f
        targets = np.zeros(n, bool)
        targets[lo0[drop]] = True
        targets[hi0[drop]] = True
        return lo0[~drop], hi0[~drop], targets, f"{int(drop.sum())} edges deleted"
    if arm == "uniform-insert":
        m = int(round(f * len(lo0)))
        a, b = undirected_unique(rng.choice(pool, m), rng.choice(pool, m))
        targets = np.zeros(n, bool)
        targets[a] = True
        targets[b] = True
        lo, hi = undirected_unique(np.r_[lo0, a], np.r_[hi0, b])
        return lo, hi, targets, f"{len(lo) - len(lo0)} edges inserted"
    hubs = np.flatnonzero(old)[np.argsort(-deg0[old])[: int(round(HUB_FRACTION * old.sum()))]]
    is_hub = np.zeros(n, bool)
    is_hub[hubs] = True
    if arm == "hub-burst":
        counts = np.round(f * deg0[hubs]).astype(int)
        h = np.repeat(hubs, counts)
        w = other_label_partners(rng, len(h), label, pool, label[h])
        lo, hi = undirected_unique(np.r_[lo0, h], np.r_[hi0, w])
        return (
            lo,
            hi,
            is_hub,
            f"{len(hubs)} hubs (degree >= {deg0[hubs].min()}), {len(lo) - len(lo0)} edges added",
        )
    if arm == "hub-shift":
        # an edge is eligible once per hub endpoint; an edge between two hubs is eligible on either side
        same = label[lo0] == label[hi0]
        e_lo = is_hub[lo0] & same & (rng.random(len(lo0)) < f)
        e_hi = is_hub[hi0] & same & ~e_lo & (rng.random(len(lo0)) < f)
        drop = e_lo | e_hi
        h = np.where(e_lo[drop], lo0[drop], hi0[drop])
        w = other_label_partners(rng, len(h), label, pool, label[h])
        lo, hi = undirected_unique(np.r_[lo0[~drop], h], np.r_[hi0[~drop], w])
        return lo, hi, is_hub, f"{len(hubs)} hubs, {int(drop.sum())} same-subreddit edges rewired"
    raise ValueError(arm)


def run_arm(arm, f, seeds, x, y, old, adj0, lo0, hi0, deg0, band_idx, label, day, lo_all, hi_all):
    n = len(label)
    rng = np.random.default_rng(MUTATION_SEED)
    lo1, hi1, targets, desc = mutate(arm, f, lo0, hi0, label, old, day, lo_all, hi_all, deg0, rng)
    # changed edges: the symmetric difference of the two edge sets, restricted to existing posts
    key0 = np.minimum(lo0, hi0).astype(np.int64) * n + np.maximum(lo0, hi0)
    key1 = np.minimum(lo1, hi1).astype(np.int64) * n + np.maximum(lo1, hi1)
    changed = np.setxor1d(key0, key1)
    ca, cb = changed // n, changed % n
    touched1 = np.zeros(n, bool)
    touched1[ca] = True
    touched1[cb] = True
    touched1 &= old
    A0 = sp.coo_matrix(
        (np.ones(2 * len(lo0), np.int8), (np.r_[lo0, hi0], np.r_[hi0, lo0])), shape=(n, n)
    ).tocsr()
    touched2 = (A0 @ touched1.astype(np.int8)).astype(bool) & old & ~touched1
    untouched = old & ~touched1 & ~touched2
    print(
        f"\n=== {arm} {f:g}: {desc}; edges {len(lo0)} -> {len(lo1)}; targets {int(targets.sum())}, "
        f"touched 1-hop {int(touched1.sum())}, 2-hop only {int(touched2.sum())}, untouched {int(untouched.sum())}"
    )
    adj1 = csr(lo1, hi1, n)
    idx = np.flatnonzero(old)
    idx_t = torch.from_numpy(idx).to(dev)
    dis, kl, cosd, rel, pf_all, nf_all = [], [], [], [], [], []
    for sage, head in seeds:
        with torch.no_grad():
            zs = sage(x, adj0)[idx_t]
            zf = sage(x, adj1)[idx_t]
            ps, pf = head(zs).argmax(1), head(zf).argmax(1)
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
    del adj1
    torch.cuda.empty_cache()
    dis, kl, cosd, rel = (np.stack(a) for a in (dis, kl, cosd, rel))
    b_dis = np.stack([pf_all[i] != pf_all[j] for i, j in band_idx])
    b_kl = np.stack([1 - overlap(nf_all[i], nf_all[j]) for i, j in band_idx])
    un = untouched[idx]
    print(
        f"check: cosine drift on untouched posts max {cosd[:, un].max() if un.any() else float('nan'):.2e}"
    )
    hdr = (
        f"{'cell':<28} {'n':>7} | {'gap dis':>8} {'lcl':>7} {'band':>7} | "
        f"{'gap kNN':>8} {'lcl':>7} {'band':>7} | {'cos':>7} {'relL2':>7}"
    )

    def row(name, m):
        sel = m[idx]
        if not sel.any():
            return
        g, q = cell(dis, sel), cell(kl, sel)
        bd, bq = b_dis[:, sel].mean(), b_kl[:, sel].mean()
        flag = " *" if g[3] > bd else ""
        print(
            f"{name:<28} {int(sel.sum()):>7} | {g[0]:>8.4f} {g[3]:>7.4f} {bd:>7.4f} | "
            f"{q[0]:>8.4f} {q[3]:>7.4f} {bq:>7.4f} | {cosd[:, sel].mean():>7.4f} {rel[:, sel].mean():>7.4f}{flag}"
        )

    print(hdr)
    for name, m in (
        ("existing, all", old),
        ("targets", targets),
        ("touched 1-hop", touched1),
        ("touched 2-hop only", touched2),
        ("untouched", untouched),
    ):
        row(name, m)
    edges = np.quantile(deg0[old], np.linspace(0, 1, 11))
    band = np.clip(np.searchsorted(edges, deg0, side="right") - 1, 0, 9)
    for b in range(10):
        row(f"decile {b} ({int(edges[b])}-{int(edges[b + 1])})", old & (band == b))
    for b in range(10):
        row(f"decile {b}, touched 1-hop", old & (band == b) & touched1)


def main():
    arms = GRID
    if len(sys.argv) > 1:
        arms = tuple((a.split(":")[0], float(a.split(":")[1])) for a in sys.argv[1:])
    t0 = time.time()
    data = np.load(ROOT / "pyg" / "raw" / "reddit_data.npz")
    st = np.load(ROOT / "derived" / "reddit_stream.npz")
    day = st["day"]
    n = len(day)
    lo_all, hi_all = st["paper_lo"].astype(np.int64), st["paper_hi"].astype(np.int64)
    label = data["label"].astype(np.int64)
    old = day < EPISODE_DAY
    e_old = old[lo_all] & old[hi_all]
    lo0, hi0 = lo_all[e_old], hi_all[e_old]
    deg0 = np.bincount(np.r_[lo0, hi0], minlength=n)
    x = torch.from_numpy(data["feature"]).to(torch.float32).to(dev)
    y = torch.from_numpy(label).to(dev)
    train_mask = torch.from_numpy(old & (data["node_types"] == 1)).to(dev)
    adj0 = csr(lo0, hi0, n)
    print(
        f"checkpoints on the graph before day {EPISODE_DAY:g}: {int(old.sum())} posts, {len(lo0)} edges; mutation seed {MUTATION_SEED}"
    )
    seeds = []
    for seed in SEEDS:
        t = time.time()
        sage, head = train(x, adj0, y, train_mask, seed)
        with torch.no_grad():
            acc = (head(sage(x, adj0)).argmax(1)[train_mask] == y[train_mask]).float().mean().item()
        seeds.append((sage, head))
        print(
            f"seed {seed}: trained {time.time() - t:.0f} s, training accuracy on the pre-mutation graph {acc:.4f}",
            flush=True,
        )
    band_idx = list(itertools.combinations(range(len(SEEDS)), 2))
    for arm, f in arms:
        t = time.time()
        run_arm(
            arm, f, seeds, x, y, old, adj0, lo0, hi0, deg0, band_idx, label, day, lo_all, hi_all
        )
        print(f"{arm} {f:g}: {time.time() - t:.0f} s", flush=True)
    print(
        f"\npeak VRAM {torch.cuda.max_memory_allocated() / 2**30:.2f} GiB; total {time.time() - t0:.0f} s"
    )


if __name__ == "__main__":
    sys.exit(main())

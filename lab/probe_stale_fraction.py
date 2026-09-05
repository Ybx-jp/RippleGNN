"""lab/017 — the stale-fraction distribution a uniform edge stream induces on the Reddit post
graph, and the embedding error it produces by degree decile: the pilot that sets the margin.

lab/008's last probe. The roster hypothesis (A0013) says that on a trained two-layer
mean-aggregation GraphSAGE the embedding error at a fixed uniform-random stale fraction of a
post's neighbourhood is non-increasing in the post's degree across degree deciles, within a
margin the preregistration derives before the run, and increasing under sum aggregation on
the same architecture. Two things have to be measured before that margin can be derived:
what stale fraction a uniform edge stream actually hands each degree decile (lab/005 left
this as the empirical question that decides whether heavy tails hurt), and how much the
per-decile error moves between checkpoints that differ only in seed, which is the only
seed-variance the deterministic inference path has (lab/002's floor is exactly zero).

Starting graph: every post created before day 20 and every edge of the paper's edge set
between two such posts (lab/013's starting graph). Checkpoints: lab/012's recipe, five
seeds, trained once with mean aggregation and once with sum aggregation at both layers.

Streams, each drawn DRAWS times from seeds MUTATION_SEEDS, using lab/013's mutate():

  uniform-delete r   delete a uniform random fraction r of the starting graph's edges
  uniform-insert r   add r * |E| edges between uniform random pairs of existing posts

at the rates in GRID. One percent is lab/008's setting; the smaller rates show how the
stale fraction and the error scale with the rate.

Per draw and checkpoint, for every existing post v:

  stale(u)      u is the endpoint of a changed edge and its first-layer hidden vector
                (after the ReLU) differs between the starting and the mutated graph
  s(v)          the share of v's starting-graph neighbours that are stale (the stale fraction)
  err(v)        |z_full(v) - z_stale(v)|, the L2 distance between the checkpoint's
                second-layer embedding of v on the mutated graph and on the starting graph
  rel(v)        err(v) / |z_full(v)|

Strata: touched at one hop (v is itself an endpoint of a changed edge, so its own
neighbourhood changed), touched at two hops only (own neighbourhood unchanged, at least one
neighbour stale: the stratum where the error is purely the neighbours' staleness), and
untouched (beyond two hops, where the error must be exactly zero: the known-negative).
Degree deciles are on the starting graph. The known-positive for the stale-fraction
instrument is its analytic expectation: under deletion at rate r a neighbour of degree d is
touched with probability 1 - (1 - r)^d, under insertion of m edges among n posts with
probability 1 - (1 - 2/n)^m at every degree; the realised decile means are printed beside
these.

Printed per stream and rate: the strata sizes; the stale-fraction distribution per decile
(pooled over draws) against its expectation; per aggregation the median error per decile
on all existing posts, on the two-hop-only stratum and on the one-hop stratum, with the
across-checkpoint range of the two-hop-only median; the top-minus-bottom decile difference
of the median two-hop-only error across the five checkpoints with its 95 percent t interval
(the margin candidate) and the top/bottom ratio; the mean/sum error ratio in the top
decile; the median two-hop-only error at fixed stale-fraction bins per decile; and the
share of existing posts, and of the exact two-hop set, whose relative error exceeds each
of several tolerances.

    python lab/probe_stale_fraction.py [stream:rate ...]

Default: GRID.
"""

import sys
import time
from pathlib import Path

import numpy as np
import scipy.sparse as sp
import torch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_gap  # noqa: E402
from probe_gap import EPISODE_DAY, SEEDS, T95_4DF, csr, dev, train  # noqa: E402
from probe_gap_adversarial import mutate  # noqa: E402

ROOT = Path(__file__).resolve().parents[1] / "data" / "reddit"
MUTATION_SEEDS = (20260905, 20260906, 20260907, 20260908, 20260909)
GRID = (
    ("uniform-delete", 0.0001),
    ("uniform-delete", 0.001),
    ("uniform-delete", 0.01),
    ("uniform-insert", 0.001),
    ("uniform-insert", 0.01),
)
AGGRS = ("mean", "sum")
FRACTION_BINS = (0.0, 0.05, 0.2, 0.5, 0.8, 1.0001)
TOLERANCES = (1e-4, 1e-3, 1e-2, 1e-1)


@torch.no_grad()
def forward(sage, x, adj):
    h1 = torch.relu(sage.c1(x, adj))
    return h1, sage.c2(h1, adj)


def q(a, p):
    return float(np.quantile(a, p)) if len(a) else float("nan")


def med(a):
    return float(np.median(a)) if len(a) else float("nan")


def run(stream, rate, ckpts, x, old, adj0, A0, lo0, hi0, deg0, label, day, lo_all, hi_all, dec):
    n = len(label)
    idx = np.flatnonzero(old)
    idx_t = torch.from_numpy(idx).to(dev)
    n_old = len(idx)
    h1_0 = {a: [forward(s, x, adj0)[0] for s in ckpts[a]] for a in AGGRS}
    z_0 = {a: [forward(s, x, adj0)[1][idx_t] for s in ckpts[a]] for a in AGGRS}
    # accumulators over draws (combinatorics) and over draws x checkpoints (errors)
    frac, pred, t1, t2 = [], [], [], []
    err = {a: [] for a in AGGRS}  # list over draws of [ckpt, n_old]
    rel = {a: [] for a in AGGRS}
    floor = {a: [0.0, 0.0, []] for a in AGGRS}  # max abs, max rel, per-draw q999 rel
    n_changed = []
    for draw, mseed in enumerate(MUTATION_SEEDS):
        rng = np.random.default_rng(mseed)
        lo1, hi1, _, desc = mutate(
            stream, rate, lo0, hi0, label, old, day, lo_all, hi_all, deg0, rng
        )
        key0 = np.minimum(lo0, hi0).astype(np.int64) * n + np.maximum(lo0, hi0)
        key1 = np.minimum(lo1, hi1).astype(np.int64) * n + np.maximum(lo1, hi1)
        changed = np.setxor1d(key0, key1)
        n_changed.append(len(changed))
        touched1 = np.zeros(n, bool)
        touched1[changed // n] = True
        touched1[changed % n] = True
        touched1 &= old
        adj1 = csr(lo1, hi1, n)
        if stream == "uniform-delete":
            p_u = 1 - (1 - rate) ** deg0.astype(np.float64)
        else:
            p_u = np.full(n, 1 - (1 - 2 / n_old) ** len(changed))
        p_u[~old] = 0
        pred.append((A0 @ p_u)[idx] / np.maximum(deg0[idx], 1))
        stale_any = np.zeros(n, bool)
        for a in AGGRS:
            e_a, r_a = [], []
            for c, sage in enumerate(ckpts[a]):
                h1, z1 = forward(sage, x, adj1)
                stale = (h1 - h1_0[a][c]).norm(dim=1).cpu().numpy() > 0
                stale &= touched1
                stale_any |= stale
                if a == "mean" and c == 0:
                    frac.append((A0 @ stale.astype(np.int32))[idx] / np.maximum(deg0[idx], 1))
                d = (z1[idx_t] - z_0[a][c]).norm(dim=1)
                e_a.append(d.cpu().numpy())
                r_a.append((d / z1[idx_t].norm(dim=1)).cpu().numpy())
                del h1, z1, d
            err[a].append(np.stack(e_a))
            rel[a].append(np.stack(r_a))
        del adj1
        torch.cuda.empty_cache()
        touched2 = ((A0 @ stale_any.astype(np.int32)) > 0) & old & ~touched1
        untouched = old & ~touched1 & ~touched2
        t1.append(touched1[idx])
        t2.append(touched2[idx])
        un = untouched[idx]
        for a in AGGRS:
            if un.any():
                floor[a][0] = max(floor[a][0], float(err[a][-1][:, un].max()))
                floor[a][1] = max(floor[a][1], float(rel[a][-1][:, un].max()))
                floor[a][2].append(float(np.quantile(rel[a][-1][:, un], 0.999)))
        if draw == 0:
            print(
                f"\n=== {stream} {rate:g}: {desc} (draw {mseed}); changed edges {len(changed)}; existing posts "
                f"touched 1-hop {int(touched1.sum())}, 2-hop only {int(touched2.sum())}, untouched {int(untouched.sum())}"
            )
    frac, pred, t1, t2 = (np.stack(v) for v in (frac, pred, t1, t2))  # [draws, n_old]
    err = {a: np.stack(err[a]) for a in AGGRS}  # [draws, ckpt, n_old]
    rel = {a: np.stack(rel[a]) for a in AGGRS}
    print(
        f"changed edges over {len(MUTATION_SEEDS)} draws: {min(n_changed)}-{max(n_changed)}; "
        f"share of existing posts touched 1-hop {t1.mean():.4f}, 2-hop only {t2.mean():.4f}, "
        f"untouched {1 - t1.mean() - t2.mean():.4f}; exact two-hop set {t1.mean() + t2.mean():.4f}"
    )
    for a in AGGRS:
        print(
            f"check [{a}]: error on untouched posts over draws and checkpoints: max {floor[a][0]:.2e}, "
            f"max relative {floor[a][1]:.2e}, 99.9th percentile relative {max(floor[a][2]):.2e}"
        )

    # --- stale fraction by decile, pooled over draws
    print(
        f"{'decile (degree)':<22} {'n':>6} | {'1-hop':>6} {'2-hop':>6} | "
        f"{'s med':>6} {'s q25':>6} {'s q75':>6} {'s mean':>6} {'E[s]':>6} | {'s med 2-hop':>11} {'count med':>9}"
    )
    dd = dec[idx]
    for b in range(10):
        sel = dd == b
        m2 = sel[None, :] & t2
        s_all = frac[:, sel].ravel()
        print(
            f"{b:>2} ({dec_edges[b]:>4}-{dec_edges[b + 1]:<5}) {int(sel.sum()):>6} | "
            f"{t1[:, sel].mean():>6.3f} {t2[:, sel].mean():>6.3f} | "
            f"{med(s_all):>6.3f} {q(s_all, 0.25):>6.3f} {q(s_all, 0.75):>6.3f} {s_all.mean():>6.3f} {pred[:, sel].mean():>6.3f} | "
            f"{med(frac[m2]):>11.3f} {med((frac * deg0[idx][None, :])[m2]):>9.0f}"
        )

    # --- error by decile per aggregation
    summary = {}
    for a in AGGRS:
        e = err[a]
        print(
            f"\n[{a}] median L2 error by decile (pooled over draws and checkpoints); range = across-checkpoint range of the 2-hop-only median"
        )
        print(
            f"{'decile':<8} | {'all':>8} {'1-hop':>8} {'2-hop':>8} {'2-hop min':>9} {'2-hop max':>9} | {'rel all':>8} {'rel 2-hop':>9} | {'n 2-hop':>8}"
        )
        per_ckpt_top_bottom = []
        for b in range(10):
            sel = dd == b
            m1 = sel[None, :] & t1
            m2 = sel[None, :] & t2
            per_c = [med(e[:, c][m2]) for c in range(e.shape[1])]
            print(
                f"{b:<8} | {med(e[:, :, sel]):>8.4f} {med(e.transpose(1, 0, 2)[:, m1]):>8.4f} "
                f"{med(e.transpose(1, 0, 2)[:, m2]):>8.4f} {np.nanmin(per_c):>9.4f} {np.nanmax(per_c):>9.4f} | "
                f"{med(rel[a][:, :, sel]):>8.4f} {med(rel[a].transpose(1, 0, 2)[:, m2]):>9.4f} | {int(m2.sum()):>8}"
            )
            if b in (0, 9):
                per_ckpt_top_bottom.append(np.array(per_c))
        bot, top = per_ckpt_top_bottom
        diff = top - bot
        ratio = top / bot
        half = T95_4DF * diff.std(ddof=1) / np.sqrt(len(diff))
        summary[a] = (bot, top)
        print(
            f"[{a}] top minus bottom decile, median 2-hop-only error, across {len(diff)} checkpoints: "
            f"mean {diff.mean():+.4f} [{diff.mean() - half:+.4f}, {diff.mean() + half:+.4f}]; "
            f"ratio top/bottom {ratio.mean():.3f} ({ratio.min():.3f}-{ratio.max():.3f})"
        )
        # all-posts version (the population A0013 does not restrict)
        per_c_all = np.array(
            [[med(e[:, c][:, dd == b]) for c in range(e.shape[1])] for b in (0, 9)]
        )
        d_all = per_c_all[1] - per_c_all[0]
        h_all = T95_4DF * d_all.std(ddof=1) / np.sqrt(len(d_all))
        print(
            f"[{a}] same on all existing posts of the decile: mean {d_all.mean():+.4f} "
            f"[{d_all.mean() - h_all:+.4f}, {d_all.mean() + h_all:+.4f}]; ratio {np.mean(per_c_all[1] / per_c_all[0]):.3f}"
        )
    r_top = summary["mean"][1] / summary["sum"][1]
    r_bot = summary["mean"][0] / summary["sum"][0]
    print(
        f"mean/sum ratio of the median 2-hop-only error: top decile {np.nanmean(r_top):.4f}, bottom decile {np.nanmean(r_bot):.4f}"
    )

    # --- fixed stale-fraction bins x decile, mean aggregation, 2-hop-only posts
    print(
        "\n[mean] median 2-hop-only L2 error at fixed stale fraction (rows: stale-fraction bin; columns: decile; pooled over draws and checkpoints; n in brackets)"
    )
    e = err["mean"].transpose(1, 0, 2)  # [ckpt, draws, n_old]
    for lo_f, hi_f in zip(FRACTION_BINS[:-1], FRACTION_BINS[1:]):
        cells = []
        for b in range(10):
            m = (dd == b)[None, :] & t2 & (frac >= lo_f) & (frac < hi_f)
            v = e[:, m]
            cells.append(f"{med(v):.4f}({m.sum():d})" if m.sum() >= 20 else f"{'.':>8}")
        print(f"s in [{lo_f:.2f},{min(hi_f, 1):.2f}) " + " ".join(f"{c:>13}" for c in cells))

    # --- tolerance exceedance
    print(
        "\nshare of existing posts (and of the exact two-hop set) whose relative error exceeds tau:"
    )
    exact = (t1 | t2).mean()
    for a in AGGRS:
        line = []
        for tau in TOLERANCES:
            ex = (rel[a] > tau).mean()
            line.append(f"tau={tau:g}: {ex:.4f} ({ex / exact:.3f})")
        print(f"  [{a}] " + "; ".join(line))
    for a in AGGRS:
        tau = 10 * floor[a][1]
        ex = (rel[a] > tau).mean()
        print(
            f"  [{a}] at ten times the measured relative floor (tau={tau:.2e}): {ex:.4f} of existing posts, {ex / exact:.3f} of the exact set"
        )
    print(
        f"  exact two-hop set {exact:.4f} of existing posts; posts with any nonzero error "
        f"{(err['mean'] > 0).mean():.4f} (mean), {(err['sum'] > 0).mean():.4f} (sum)"
    )


def main():
    global dec_edges
    grid = GRID
    if len(sys.argv) > 1:
        grid = tuple((a.split(":")[0], float(a.split(":")[1])) for a in sys.argv[1:])
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
    A0 = sp.coo_matrix(
        (np.ones(2 * len(lo0), np.int8), (np.r_[lo0, hi0], np.r_[hi0, lo0])), shape=(n, n)
    ).tocsr()
    x = torch.from_numpy(data["feature"]).to(torch.float32).to(dev)
    y = torch.from_numpy(label).to(dev)
    train_mask = torch.from_numpy(old & (data["node_types"] == 1)).to(dev)
    adj0 = csr(lo0, hi0, n)
    dec_edges = np.quantile(deg0[old], np.linspace(0, 1, 11)).astype(int)
    dec = np.clip(np.searchsorted(dec_edges, deg0, side="right") - 1, 0, 9)
    print(
        f"starting graph before day {EPISODE_DAY:g}: {int(old.sum())} posts, {len(lo0)} edges; "
        f"degree decile edges {dec_edges.tolist()}; mutation seeds {MUTATION_SEEDS}"
    )
    ckpts = {}
    for a in AGGRS:
        probe_gap.AGGR = a
        ckpts[a] = []
        for seed in SEEDS:
            t = time.time()
            sage, head = train(x, adj0, y, train_mask, seed)
            with torch.no_grad():
                acc = (
                    (head(sage(x, adj0)).argmax(1)[train_mask] == y[train_mask])
                    .float()
                    .mean()
                    .item()
                )
            ckpts[a].append(sage)
            print(
                f"[{a}] seed {seed}: trained {time.time() - t:.0f} s, training accuracy {acc:.4f}",
                flush=True,
            )
            del head
    idx_t = torch.from_numpy(np.flatnonzero(old)).to(dev)
    for a in AGGRS:
        worst = [0.0, 0.0]
        for sage in ckpts[a]:
            z1, z2 = forward(sage, x, adj0)[1][idx_t], forward(sage, x, adj0)[1][idx_t]
            d = (z1 - z2).norm(dim=1)
            worst[0] = max(worst[0], d.max().item())
            worst[1] = max(worst[1], (d / z1.norm(dim=1)).max().item())
            del z1, z2, d
        print(
            f"check [{a}]: same graph twice, existing posts, max |dz| {worst[0]:.2e}, max relative {worst[1]:.2e}"
        )
    for stream, rate in grid:
        t = time.time()
        run(stream, rate, ckpts, x, old, adj0, A0, lo0, hi0, deg0, label, day, lo_all, hi_all, dec)
        print(f"{stream} {rate:g}: {time.time() - t:.0f} s", flush=True)
    print(
        f"\npeak VRAM {torch.cuda.max_memory_allocated() / 2**30:.2f} GiB; total {time.time() - t0:.0f} s"
    )


if __name__ == "__main__":
    sys.exit(main())

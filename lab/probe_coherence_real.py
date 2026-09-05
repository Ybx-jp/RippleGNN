"""lab/015 and lab/016 — the coherence a real mutation induces among stale neighbours, and
the checkpoint's spectral norms.

lab/007 showed on a star graph that mean-aggregation error at a fixed stale fraction sits
between two brackets: the coherent one, where every stale neighbour's delta points the same
way and the centre's aggregated input moves by fraction times delta at every degree, and
the incoherent one, where the deltas are independent and the move falls as the square root
of fraction over degree. Which bracket a real mutation on a real graph sits near was
unmeasured. This probe measures it on lab/013's thirteen arms over the Reddit post graph
before day 20, on the same five trained checkpoints, with the arms' draws reproduced from
the same seed (probe_gap_adversarial.mutate).

For a checkpoint and an arm, the delta of an existing post u is the change in its
first-layer hidden vector (after the ReLU, the vector its neighbours aggregate in the
second layer) between the starting graph and the mutated graph. A post is stale when it is
the endpoint of a changed edge and its delta is non-zero. For every existing post v, its
stale neighbours are the stale posts among its starting-graph neighbours; over those with
two or more:

  cos      the mean pairwise cosine between the stale neighbours' deltas
  R        |sum of deltas| / sum of |delta|: 1 when the deltas agree in direction
  R_inc    sqrt(sum of |delta|^2) / sum of |delta|: what R would be if the deltas were
           orthogonal, about 1/sqrt(k) for k stale neighbours of equal norm

The null band is a shuffle: the deltas are permuted among the stale posts (one draw per
checkpoint), so each post keeps a real delta but of some other stale post; what cos and R
then read is the coherence the delta distribution's anisotropy produces by chance. The
known-positive replaces every stale delta by their common mean (cos must read 1, R must
read 1) and the known-negative replaces them by independent Gaussian vectors of the same
norms (cos must read about 0 and R about R_inc); both are printed once.

For posts touched at two hops only, whose own neighbourhood is unchanged, the second
layer's aggregated input moves by exactly the mean of the neighbours' deltas, and the
output moves by exactly the neighbour weight matrix times that; the probe prints that
move against the coherent bound (sum |delta| / degree), the incoherent prediction
(sqrt(sum |delta|^2) / degree) and the realised gain |output move| / |input move| beside
the spectral norm of the second layer's neighbour matrix.

Spectral norms (largest singular value) of every weight matrix of every checkpoint are
printed first: SAGEConv's neighbour matrix lin_l and root matrix lin_r per layer, and the
head, with the root share |W_r| / (|W_l| + |W_r|) per layer.

    python lab/probe_coherence_real.py [arm:setting ...]

Default: lab/013's full grid.
"""

import sys
import time
from pathlib import Path

import numpy as np
import scipy.sparse as sp
import torch

sys.path.insert(0, str(Path(__file__).resolve().parent))
from probe_gap import EPISODE_DAY, SEEDS, csr, dev, train  # noqa: E402
from probe_gap_adversarial import GRID, MUTATION_SEED, mutate  # noqa: E402

ROOT = Path(__file__).resolve().parents[1] / "data" / "reddit"
SHUFFLE_SEED = 20260905
EPS = 1e-7


def spectral(sage, head):
    rows = []
    for name, conv in (("layer 1", sage.c1), ("layer 2", sage.c2)):
        wl = torch.linalg.matrix_norm(conv.lin_l.weight, 2).item()
        wr = torch.linalg.matrix_norm(conv.lin_r.weight, 2).item()
        rows.append((name, wl, wr, wr / (wl + wr)))
    rows.append(
        ("head", torch.linalg.matrix_norm(head.weight, 2).item(), float("nan"), float("nan"))
    )
    return rows


def coherence(A0, delta, stale):
    """Per centre: k stale neighbours, cos, R, R_inc, sum |delta|, sqrt(sum |delta|^2), sum delta."""
    nrm = np.linalg.norm(delta, axis=1)
    s = stale & (nrm > EPS)
    unit = np.zeros_like(delta)
    unit[s] = delta[s] / nrm[s, None]
    k = A0 @ s.astype(np.float64)
    S = A0 @ unit
    sum_d = A0 @ (delta * s[:, None])
    sum_n = A0 @ (nrm * s)
    sum_n2 = A0 @ (nrm**2 * s)
    with np.errstate(invalid="ignore", divide="ignore"):
        cos = ((S**2).sum(1) - k) / (k * (k - 1))
        R = np.linalg.norm(sum_d, axis=1) / sum_n
        R_inc = np.sqrt(sum_n2) / sum_n
    return k, cos, R, R_inc, sum_n, np.sqrt(sum_n2), sum_d


@torch.no_grad()
def hidden(sage, x, adj):
    h = torch.relu(sage.c1(x, adj))
    return h, sage.c2(h, adj)


def run_arm(arm, f, seeds, x, old, adj0, lo0, hi0, deg0, label, day, lo_all, hi_all, checks):
    n = len(label)
    rng = np.random.default_rng(MUTATION_SEED)
    lo1, hi1, targets, desc = mutate(arm, f, lo0, hi0, label, old, day, lo_all, hi_all, deg0, rng)
    key0 = np.minimum(lo0, hi0).astype(np.int64) * n + np.maximum(lo0, hi0)
    key1 = np.minimum(lo1, hi1).astype(np.int64) * n + np.maximum(lo1, hi1)
    changed = np.setxor1d(key0, key1)
    touched1 = np.zeros(n, bool)
    touched1[changed // n] = True
    touched1[changed % n] = True
    touched1 &= old
    A0 = sp.coo_matrix(
        (np.ones(2 * len(lo0), np.float64), (np.r_[lo0, hi0], np.r_[hi0, lo0])), shape=(n, n)
    ).tocsr()
    touched2 = (A0 @ touched1.astype(np.float64) > 0) & old & ~touched1
    adj1 = csr(lo1, hi1, n)
    print(
        f"\n=== {arm} {f:g}: {desc}; targets {int(targets.sum())}, touched 1-hop {int(touched1.sum())}, "
        f"2-hop only {int(touched2.sum())}"
    )
    per_seed = []
    for si, (sage, head) in enumerate(seeds):
        h0, z0 = hidden(sage, x, adj0)
        h1, z1 = hidden(sage, x, adj1)
        delta = (h1 - h0).cpu().numpy().astype(np.float64)
        dz = (z1 - z0).norm(dim=1).cpu().numpy().astype(np.float64)
        del h0, h1, z0, z1
        nrm = np.linalg.norm(delta, axis=1)
        untouched = old & ~touched1
        stale = touched1 & (nrm > EPS)
        if si == 0:
            print(
                f"check: |delta| on untouched posts max {nrm[untouched].max():.2e}; touched 1-hop posts "
                f"with |delta| <= {EPS:g}: {int((touched1 & ~stale).sum())} of {int(touched1.sum())}"
            )
        k, cos, R, R_inc, sum_n, rt_n2, sum_d = coherence(A0, delta, stale)
        # shuffle null: permute the real deltas among the stale posts
        prng = np.random.default_rng(SHUFFLE_SEED + si)
        idx_s = np.flatnonzero(stale)
        sh = np.zeros_like(delta)
        sh[idx_s] = delta[idx_s[prng.permutation(len(idx_s))]]
        _, cos_sh, R_sh, _, _, _, _ = coherence(A0, sh, stale)
        if checks and si == 0:
            pos = np.zeros_like(delta)
            pos[idx_s] = delta[idx_s].mean(0)
            _, c_pos, R_pos, _, _, _, _ = coherence(A0, pos, stale)
            neg = np.zeros_like(delta)
            g = prng.standard_normal((len(idx_s), delta.shape[1]))
            neg[idx_s] = g / np.linalg.norm(g, axis=1)[:, None] * nrm[idx_s, None]
            _, c_neg, R_neg, Ri_neg, _, _, _ = coherence(A0, neg, stale)
            m = (k >= 2) & old
            print(
                f"check: known-positive (one shared delta) cos {np.nanmean(c_pos[m]):.4f} R {np.nanmean(R_pos[m]):.4f}; "
                f"known-negative (independent directions, real norms) cos {np.nanmean(c_neg[m]):.4f} "
                f"R {np.nanmean(R_neg[m]):.4f} against R_inc {np.nanmean(Ri_neg[m]):.4f}"
            )
        w2 = torch.linalg.matrix_norm(sage.c2.lin_l.weight, 2).item()
        per_seed.append((k, cos, R, R_inc, cos_sh, R_sh, sum_n, rt_n2, sum_d, dz, w2))
        torch.cuda.empty_cache()
    del adj1
    torch.cuda.empty_cache()

    edges = np.quantile(deg0[old], np.linspace(0, 1, 11))
    dec = np.clip(np.searchsorted(edges, deg0, side="right") - 1, 0, 9)
    hubs = targets if arm.startswith("hub") else np.zeros(n, bool)

    def agg(name, m):
        """Mean over seeds of the cell mean over centres with two or more stale neighbours."""
        vals = []
        for k, cos, R, R_inc, cos_sh, R_sh, *_ in per_seed:
            sel = m & old & (k >= 2)
            if sel.sum() == 0:
                return
            vals.append(
                (
                    sel.sum(),
                    k[sel].mean(),
                    (k[sel] / deg0[sel]).mean(),
                    cos[sel].mean(),
                    cos_sh[sel].mean(),
                    R[sel].mean(),
                    R_inc[sel].mean(),
                    R_sh[sel].mean(),
                )
            )
        v = np.array(vals)
        mu = v.mean(0)
        print(
            f"{name:<28} {int(mu[0]):>7} {mu[1]:>7.1f} {mu[2]:>6.3f} | {mu[3]:>7.3f} {mu[4]:>7.3f} | "
            f"{mu[5]:>6.3f} {mu[6]:>6.3f} {mu[7]:>6.3f}   (cos across seeds {v[:, 3].min():.3f}-{v[:, 3].max():.3f})"
        )

    print(
        f"{'cell (centres, k >= 2)':<28} {'n':>7} {'k':>7} {'f':>6} | {'cos':>7} {'cos-sh':>7} | "
        f"{'R':>6} {'R_inc':>6} {'R-sh':>6}"
    )
    for name, m in (
        ("existing, all", old),
        ("touched 1-hop", touched1),
        ("touched 2-hop only", touched2),
        ("hubs (targets)", hubs),
    ):
        agg(name, m)
    for b in range(10):
        agg(f"decile {b} ({int(edges[b])}-{int(edges[b + 1])})", dec == b)
    for b in range(10):
        agg(f"decile {b}, 2-hop only", (dec == b) & touched2)

    # the second layer's input move on 2-hop-only centres, against the two brackets
    print(
        f"\n{'2-hop only, by decile':<28} {'n':>7} | {'|d agg|':>8} {'coherent':>8} {'incoh.':>8} | "
        f"{'gain':>6} {'|W_l2|':>6}"
    )
    for b in range(10):
        vals = []
        for k, *_r in per_seed:
            sum_n, rt_n2, sum_d, dz, w2 = _r[5:]
            sel = touched2 & (dec == b) & (k >= 1)
            if sel.sum() == 0:
                break
            dagg = np.linalg.norm(sum_d[sel], axis=1) / deg0[sel]
            vals.append(
                (
                    sel.sum(),
                    dagg.mean(),
                    (sum_n[sel] / deg0[sel]).mean(),
                    (rt_n2[sel] / deg0[sel]).mean(),
                    (dz[sel] / np.maximum(dagg, 1e-12)).mean(),
                    w2,
                )
            )
        if vals:
            mu = np.array(vals).mean(0)
            print(
                f"decile {b} ({int(edges[b])}-{int(edges[b + 1])}){'':<12} {int(mu[0]):>7} | {mu[1]:>8.5f} {mu[2]:>8.5f} "
                f"{mu[3]:>8.5f} | {mu[4]:>6.3f} {mu[5]:>6.3f}"
            )


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
        f"checkpoints on the graph before day {EPISODE_DAY:g}: {int(old.sum())} posts, {len(lo0)} edges; "
        f"mutation seed {MUTATION_SEED}, shuffle seed {SHUFFLE_SEED}"
    )
    seeds = []
    print(f"\n{'seed':>10} {'matrix':<8} {'|W_l|':>7} {'|W_r|':>7} {'root share':>10}")
    for seed in SEEDS:
        t = time.time()
        sage, head = train(x, adj0, y, train_mask, seed)
        seeds.append((sage, head))
        for name, wl, wr, share in spectral(sage, head):
            print(f"{seed:>10} {name:<8} {wl:>7.3f} {wr:>7.3f} {share:>10.3f}")
        print(f"seed {seed}: trained {time.time() - t:.0f} s", flush=True)
    for i, (arm, f) in enumerate(arms):
        t = time.time()
        run_arm(arm, f, seeds, x, old, adj0, lo0, hi0, deg0, label, day, lo_all, hi_all, i == 0)
        print(f"{arm} {f:g}: {time.time() - t:.0f} s", flush=True)
    print(
        f"\npeak VRAM {torch.cuda.max_memory_allocated() / 2**30:.2f} GiB; total {time.time() - t0:.0f} s"
    )


if __name__ == "__main__":
    sys.exit(main())

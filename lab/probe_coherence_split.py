"""lab/021 — the real stream's coherence split by same- and cross-subreddit arrivals.

lab/015 measured the coherence the real growth stream induces among a post's stale
neighbours' first-layer deltas (cos 0.06–0.08 against a shuffled 0.003; R 2.6 times R_inc
on the top decile) and read the coherent part as the contribution of the cross-subreddit
share of the arriving edges, without splitting the stream. lab/020 measured that share
(a quarter of new-to-old arrivals, U-shaped in degree, dispersed over subreddits on a
hub). This probe makes the split lab/015 did not: the same coherence measurement on
three counterfactual graphs built from the same stream,

  all       the starting graph plus every edge the stream brings (lab/015's growth arm)
  same      the starting graph plus the new posts and only the new-to-old edges whose
            two posts share a subreddit, plus every new-to-new edge
  foreign   the same with only the new-to-old edges that cross subreddits
  matched   a count control: per existing post, a uniform random subset of its
            new-to-old arrivals of the same size as its foreign set (seed 20260913)
  matched-j a sharing control: per new post, a uniform random subset of its
            new-to-old edges of the same size as its foreign set, so the existing
            posts a new post touches still share it (seed 20260913 + 1)

New-to-new edges do not enter an existing post's first-layer vector, so a variant's
delta on an existing post is exactly what its included arrivals do to it.

Per variant, per checkpoint: the post-ReLU first-layer delta of every existing post; a
post is stale when it received an included arrival and its delta is non-zero; per
centre with two or more stale starting-graph neighbours, cos, R and R_inc as lab/015
defines them, with the shuffle null (deltas permuted among stale posts) and the
two-hop-only aggregated-input move against the coherent and incoherent brackets.

Then the delta's own decomposition, per post: over posts stale on both the same and
foreign variants, the cosine of the full delta with each split delta and the norm of
each split delta over the full one, by decile.

Then, inside a post, whether its arrivals push it the same way: the first-layer
pre-activation moves by the mean over arrivals j of p_j = W_l (x_j - m_u), where m_u
is the mean feature of u's starting-graph neighbours (zero for an isolated post), over
the new degree. R_arr = |sum p_j| / sum |p_j| over a post's foreign arrivals, and over
its same arrivals, with R_inc as the orthogonal value, by decile over posts with two
or more arrivals of that kind. Verifier: the mean of p_j over the new degree must
equal the measured pre-activation delta on the all variant.

    python lab/probe_coherence_split.py [days ...]

Default: 1 and 10 days from day 20, on the paper edge set.
"""

import sys
import time
from pathlib import Path

import numpy as np
import scipy.sparse as sp
import torch

sys.path.insert(0, str(Path(__file__).resolve().parent))
from probe_coherence_real import EPS, SHUFFLE_SEED, coherence, hidden  # noqa: E402
from probe_gap import EPISODE_DAY, SEEDS, csr, dev, train  # noqa: E402

ROOT = Path(__file__).resolve().parents[1] / "data" / "reddit"
MATCH_SEED = 20260913
VARIANTS = ("all", "same", "foreign", "matched", "matched-j")


def arrivals(days, old, day, lo_all, hi_all, label, rng):
    """The stream for `days` from day 20: new-to-old edges with their old endpoint, new post,
    foreign flag and matched-random flag; and the new-to-new edges."""
    present = day < EPISODE_DAY + days
    keep = present[lo_all] & present[hi_all] & ~(old[lo_all] & old[hi_all])
    lo, hi = lo_all[keep], hi_all[keep]
    lo_old = old[lo]
    one_old = lo_old ^ old[hi]
    u = np.where(lo_old, lo, hi)[one_old]
    j = np.where(lo_old, hi, lo)[one_old]
    foreign = label[u] != label[j]
    nn_lo, nn_hi = lo[~one_old], hi[~one_old]
    # matched: per old post, a uniform random subset of its arrivals of its foreign count
    n = len(day)
    order = np.lexsort((rng.random(len(u)), u))
    u_s = u[order]
    start = np.searchsorted(u_s, np.arange(n))
    rank = np.arange(len(u_s)) - start[u_s]
    want = np.bincount(u, weights=foreign, minlength=n).astype(np.int64)
    matched = np.zeros(len(u), bool)
    matched[order] = rank < want[u_s]
    matched_j = subset_by(j, foreign, n, np.random.default_rng(MATCH_SEED + 1))
    return u, j, foreign, (matched, matched_j), nn_lo, nn_hi, present & ~old


def subset_by(key, foreign, n, rng):
    """Per key value, a uniform random subset of its edges of the size of its foreign set."""
    order = np.lexsort((rng.random(len(key)), key))
    k_s = key[order]
    start = np.searchsorted(k_s, np.arange(n))
    rank = np.arange(len(k_s)) - start[k_s]
    want = np.bincount(key, weights=foreign, minlength=n).astype(np.int64)
    out = np.zeros(len(key), bool)
    out[order] = rank < want[k_s]
    return out


def variant_edges(v, lo0, hi0, u, j, foreign, matched, nn_lo, nn_hi):
    sel = {
        "all": np.ones(len(u), bool),
        "same": ~foreign,
        "foreign": foreign,
        "matched": matched[0],
        "matched-j": matched[1],
    }[v]
    return np.r_[lo0, u[sel], nn_lo], np.r_[hi0, j[sel], nn_hi], sel


def agg_rows(per_seed, cells, deg0, old):
    print(
        f"{'cell (centres, k >= 2)':<28} {'n':>7} {'k':>7} {'f':>6} | {'cos':>7} {'cos-sh':>7} | "
        f"{'R':>6} {'R_inc':>6} {'R-sh':>6}  R/R_inc"
    )
    for name, m in cells:
        vals = []
        for k, cos, R, R_inc, cos_sh, R_sh, *_ in per_seed:
            s = m & old & (k >= 2)
            if s.sum() == 0:
                break
            vals.append(
                (
                    s.sum(),
                    k[s].mean(),
                    (k[s] / np.maximum(deg0[s], 1)).mean(),
                    cos[s].mean(),
                    cos_sh[s].mean(),
                    R[s].mean(),
                    R_inc[s].mean(),
                    R_sh[s].mean(),
                )
            )
        if not vals:
            continue
        v = np.array(vals)
        mu = v.mean(0)
        print(
            f"{name:<28} {int(mu[0]):>7} {mu[1]:>7.1f} {mu[2]:>6.3f} | {mu[3]:>7.3f} {mu[4]:>7.3f} | "
            f"{mu[5]:>6.3f} {mu[6]:>6.3f} {mu[7]:>6.3f}  {mu[5] / mu[6]:>5.2f}   "
            f"(cos across seeds {v[:, 3].min():.3f}-{v[:, 3].max():.3f})"
        )


def two_hop_rows(per_seed, touched2, dec, edges, deg0):
    print(
        f"\n{'2-hop only, by decile':<28} {'n':>7} | {'|d agg|':>8} {'coherent':>8} {'incoh.':>8} | "
        f"{'gain':>6}"
    )
    for b in range(10):
        vals = []
        for k, *_r in per_seed:
            sum_n, rt_n2, sum_d, dz = _r[5:9]
            s = touched2 & (dec == b) & (k >= 1)
            if s.sum() == 0:
                break
            dagg = np.linalg.norm(sum_d[s], axis=1) / deg0[s]
            vals.append(
                (
                    s.sum(),
                    dagg.mean(),
                    (sum_n[s] / deg0[s]).mean(),
                    (rt_n2[s] / deg0[s]).mean(),
                    (dz[s] / np.maximum(dagg, 1e-12)).mean(),
                )
            )
        if vals:
            mu = np.array(vals).mean(0)
            print(
                f"decile {b} ({int(edges[b])}-{int(edges[b + 1])}){'':<12} {int(mu[0]):>7} | "
                f"{mu[1]:>8.5f} {mu[2]:>8.5f} {mu[3]:>8.5f} | {mu[4]:>6.3f}"
            )


@torch.no_grad()
def pushes(sage, x, adj0, deg0, u, j):
    """p_j = W_l (x_j - m_u) for every new-to-old edge (u, j): [E, 64] on the CPU."""
    W = sage.c1.lin_l.weight  # [64, 602]
    P = x @ W.T  # [n, 64]
    m = torch.sparse.mm(adj0, x) / torch.from_numpy(np.maximum(deg0, 1)).to(dev)[:, None].to(
        x.dtype
    )
    PM = m @ W.T
    out = torch.empty(len(u), P.shape[1], dtype=torch.float64)
    ut, jt = torch.from_numpy(u).to(dev), torch.from_numpy(j).to(dev)
    step = 1 << 20
    for s in range(0, len(u), step):
        out[s : s + step] = (P[jt[s : s + step]] - PM[ut[s : s + step]]).double().cpu()
    del P, m, PM, ut, jt
    return out.numpy()


def within_post(p, u, sel, n):
    """Per post: count, |sum p|, sum |p|, sqrt(sum |p|^2) over the selected arrivals."""
    us = u[sel]
    ps = p[sel]
    k = np.bincount(us, minlength=n).astype(np.float64)
    nrm = np.linalg.norm(ps, axis=1)
    M = sp.csr_matrix((np.ones(len(us)), (us, np.arange(len(us)))), shape=(n, len(us)))
    S = M @ ps
    sum_n = np.bincount(us, weights=nrm, minlength=n)
    sum_n2 = np.bincount(us, weights=nrm**2, minlength=n)
    with np.errstate(invalid="ignore", divide="ignore"):
        R = np.linalg.norm(S, axis=1) / sum_n
        R_inc = np.sqrt(sum_n2) / sum_n
    return k, R, R_inc, S


def run_window(days, seeds, x, old, adj0, lo0, hi0, deg0, label, day, lo_all, hi_all, checks):
    n = len(label)
    rng = np.random.default_rng(MATCH_SEED)
    u, j, foreign, matched, nn_lo, nn_hi, new = arrivals(days, old, day, lo_all, hi_all, label, rng)
    A0 = sp.coo_matrix(
        (np.ones(2 * len(lo0), np.float64), (np.r_[lo0, hi0], np.r_[hi0, lo0])), shape=(n, n)
    ).tocsr()
    edges = np.quantile(deg0[old], np.linspace(0, 1, 11))
    dec = np.clip(np.searchsorted(edges, deg0, side="right") - 1, 0, 9)
    k_for = np.bincount(u, weights=foreign, minlength=n)
    k_same = np.bincount(u, weights=~foreign, minlength=n)
    k_mat = np.bincount(u, weights=matched[0], minlength=n)
    k_matj = np.bincount(u, weights=matched[1], minlength=n)
    print(
        f"\n##### {days:g} days from day {EPISODE_DAY:g}: {int(new.sum())} new posts, "
        f"{len(u)} new-to-old edges of which {int(foreign.sum())} foreign ({foreign.mean():.3f}), "
        f"{len(nn_lo)} new-to-new; matched draws {int(matched[0].sum())} edges, matched-j "
        f"{int(matched[1].sum())} touching {int((k_matj > 0).sum())} existing posts; "
        f"existing posts with a foreign arrival {int((k_for > 0).sum())}, with a same arrival "
        f"{int((k_same > 0).sum())}, with both {int(((k_for > 0) & (k_same > 0)).sum())}"
    )
    assert np.array_equal(k_mat, k_for)

    deltas = {}
    for v in VARIANTS:
        lo1, hi1, sel = variant_edges(v, lo0, hi0, u, j, foreign, matched, nn_lo, nn_hi)
        touched1 = np.zeros(n, bool)
        touched1[u[sel]] = True
        touched2 = (A0 @ touched1.astype(np.float64) > 0) & old & ~touched1
        adj1 = csr(lo1, hi1, n)
        t = time.time()
        print(
            f"\n=== {v}, {days:g} d: {int(sel.sum())} new-to-old edges, touched 1-hop "
            f"{int(touched1.sum())}, 2-hop only {int(touched2.sum())}"
        )
        per_seed = []
        for si, (sage, head) in enumerate(seeds):
            h0, z0 = hidden(sage, x, adj0)
            h1, z1 = hidden(sage, x, adj1)
            delta = (h1 - h0).cpu().numpy().astype(np.float64)
            dz = (z1 - z0).norm(dim=1).cpu().numpy().astype(np.float64)
            del h0, h1, z0, z1
            nrm = np.linalg.norm(delta, axis=1)
            stale = touched1 & (nrm > EPS)
            if si == 0:
                un = old & ~touched1
                print(
                    f"check: |delta| on untouched existing posts max {nrm[un].max():.2e}; touched posts "
                    f"with |delta| <= {EPS:g}: {int((touched1 & ~stale).sum())} of {int(touched1.sum())}"
                )
                deltas[v] = delta[old]
            k, cos, R, R_inc, sum_n, rt_n2, sum_d = coherence(A0, delta, stale)
            prng = np.random.default_rng(SHUFFLE_SEED + si)
            idx_s = np.flatnonzero(stale)
            sh = np.zeros_like(delta)
            sh[idx_s] = delta[idx_s[prng.permutation(len(idx_s))]]
            _, cos_sh, R_sh, _, _, _, _ = coherence(A0, sh, stale)
            if checks and v == "all" and si == 0:
                pos = np.zeros_like(delta)
                pos[idx_s] = delta[idx_s].mean(0)
                _, c_pos, R_pos, _, _, _, _ = coherence(A0, pos, stale)
                neg = np.zeros_like(delta)
                g = prng.standard_normal((len(idx_s), delta.shape[1]))
                neg[idx_s] = g / np.linalg.norm(g, axis=1)[:, None] * nrm[idx_s, None]
                _, c_neg, R_neg, Ri_neg, _, _, _ = coherence(A0, neg, stale)
                m = (k >= 2) & old
                print(
                    f"check: known-positive cos {np.nanmean(c_pos[m]):.4f} R {np.nanmean(R_pos[m]):.4f}; "
                    f"known-negative cos {np.nanmean(c_neg[m]):.4f} R {np.nanmean(R_neg[m]):.4f} "
                    f"against R_inc {np.nanmean(Ri_neg[m]):.4f}"
                )
            per_seed.append((k, cos, R, R_inc, cos_sh, R_sh, sum_n, rt_n2, sum_d, dz))
            torch.cuda.empty_cache()
        del adj1
        torch.cuda.empty_cache()
        cells = [
            ("existing, all", old),
            ("touched 1-hop", touched1),
            ("touched 2-hop only", touched2),
        ]
        cells += [
            (f"decile {b} ({int(edges[b])}-{int(edges[b + 1])})", dec == b) for b in range(10)
        ]
        agg_rows(per_seed, cells, deg0, old)
        two_hop_rows(per_seed, touched2, dec, edges, deg0)
        print(f"{v} {days:g} d: {time.time() - t:.0f} s", flush=True)

    # the delta's own decomposition on posts stale under both splits (first checkpoint)
    both = ((k_for > 0) & (k_same > 0))[old]
    d_all, d_same, d_for = deltas["all"], deltas["same"], deltas["foreign"]
    dec_old = dec[old]

    def cosv(a, b):
        return (a * b).sum(1) / np.maximum(
            np.linalg.norm(a, axis=1) * np.linalg.norm(b, axis=1), 1e-12
        )

    print(
        f"\n{'delta decomposition, seed 1':<28} {'n':>7} | {'|d_same|/|d_all|':>16} {'|d_for|/|d_all|':>15} | "
        f"{'cos(all,same)':>13} {'cos(all,for)':>12} {'cos(same,for)':>13} | "
        f"{'|d_all-d_same-d_for|/|d_all|':>28}"
    )
    for b in list(range(10)) + [None]:
        s = both if b is None else both & (dec_old == b)
        if s.sum() == 0:
            continue
        na = np.linalg.norm(d_all[s], axis=1)
        print(
            f"{'all deciles' if b is None else f'decile {b} ({int(edges[b])}-{int(edges[b + 1])})':<28} "
            f"{int(s.sum()):>7} | {np.median(np.linalg.norm(d_same[s], axis=1) / na):>16.3f} "
            f"{np.median(np.linalg.norm(d_for[s], axis=1) / na):>15.3f} | "
            f"{np.median(cosv(d_all[s], d_same[s])):>13.3f} {np.median(cosv(d_all[s], d_for[s])):>12.3f} "
            f"{np.median(cosv(d_same[s], d_for[s])):>13.3f} | "
            f"{np.median(np.linalg.norm(d_all[s] - d_same[s] - d_for[s], axis=1) / na):>28.3f}"
        )

    # within a post: do its arrivals push it the same way? pre-activation, per checkpoint
    print(
        f"\n{'within-post alignment':<28} {'n':>7} {'k':>6} {'|p|':>6} | {'R_arr':>6} {'R_inc':>6} R/R_inc   "
        f"(mean over seeds; posts with >= 2 arrivals of the kind; |p| the mean push norm per arrival)"
    )
    rows = {}
    opp = {}
    for si, (sage, head) in enumerate(seeds):
        p = pushes(sage, x, adj0, deg0, u, j)
        if si == 0:
            # verifier: mean push over the new degree equals the measured pre-activation delta
            with torch.no_grad():
                lo1, hi1, _ = variant_edges("all", lo0, hi0, u, j, foreign, matched, nn_lo, nn_hi)
                adj1 = csr(lo1, hi1, n)
                pre = (sage.c1(x, adj1) - sage.c1(x, adj0)).double().cpu().numpy()
                del adj1
                torch.cuda.empty_cache()
            _, _, _, S_all = within_post(p, u, np.ones(len(u), bool), n)
            k_all = k_for + k_same
            pred = S_all / np.maximum(deg0 + k_all, 1)[:, None]
            m = old & (k_all > 0)
            err = np.linalg.norm(pred[m] - pre[m], axis=1) / np.maximum(
                np.linalg.norm(pre[m], axis=1), 1e-12
            )
            print(
                f"check: predicted pre-activation delta against measured on {int(m.sum())} touched posts: "
                f"relative error median {np.median(err):.2e}, max {err.max():.2e}"
            )
        nets = {}
        pn = np.linalg.norm(p, axis=1)
        kinds = (
            ("all", np.ones(len(u), bool)),
            ("foreign", foreign),
            ("same", ~foreign),
            ("matched", matched[0]),
            ("matched-j", matched[1]),
        )
        for kind, sel in kinds:
            k, R, R_inc, S = within_post(p, u, sel, n)
            nets[kind] = (k, S)
            mean_pn = np.bincount(u[sel], weights=pn[sel], minlength=n) / np.maximum(k, 1)
            for b in list(range(10)) + [None]:
                s = old & (k >= 2) & (True if b is None else dec == b)
                if s.sum() == 0:
                    continue
                rows.setdefault((kind, b), []).append(
                    (s.sum(), k[s].mean(), mean_pn[s].mean(), R[s].mean(), R_inc[s].mean())
                )
        # the angle between a post's net same push and its net foreign push
        (k_s, S_s), (k_f, S_f) = nets["same"], nets["foreign"]
        c = cosv(S_s, S_f)
        for b in list(range(10)) + [None]:
            s = old & (k_s >= 1) & (k_f >= 1) & (True if b is None else dec == b)
            if s.sum():
                opp.setdefault(b, []).append((s.sum(), np.median(c[s]), (c[s] < 0).mean()))
        del p, pn
    for kind, _ in kinds:
        for b in list(range(10)) + [None]:
            if (kind, b) not in rows:
                continue
            mu = np.array(rows[(kind, b)]).mean(0)
            name = f"{kind}, " + (
                "all deciles" if b is None else f"decile {b} ({int(edges[b])}-{int(edges[b + 1])})"
            )
            print(
                f"{name:<28} {int(mu[0]):>7} {mu[1]:>6.1f} {mu[2]:>6.3f} | {mu[3]:>6.3f} {mu[4]:>6.3f} "
                f"{mu[3] / mu[4]:>7.2f}"
            )
    print(
        f"\n{'net same vs net foreign push':<28} {'n':>7} | {'median cos':>10} {'share < 0':>9}   "
        f"(posts with an arrival of each kind; mean over seeds)"
    )
    for b in list(range(10)) + [None]:
        if b not in opp:
            continue
        mu = np.array(opp[b]).mean(0)
        name = "all deciles" if b is None else f"decile {b} ({int(edges[b])}-{int(edges[b + 1])})"
        print(f"{name:<28} {int(mu[0]):>7} | {mu[1]:>10.3f} {mu[2]:>9.3f}")


def main():
    windows = tuple(float(a) for a in sys.argv[1:]) or (1.0, 10.0)
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
        f"matched-subset seed {MATCH_SEED}, shuffle seed {SHUFFLE_SEED}"
    )
    seeds = []
    for seed in SEEDS:
        t = time.time()
        seeds.append(train(x, adj0, y, train_mask, seed))
        print(f"seed {seed}: trained {time.time() - t:.0f} s", flush=True)
    for i, days in enumerate(windows):
        t = time.time()
        run_window(days, seeds, x, old, adj0, lo0, hi0, deg0, label, day, lo_all, hi_all, i == 0)
        print(f"window {days:g} d: {time.time() - t:.0f} s", flush=True)
    print(
        f"\npeak VRAM {torch.cuda.max_memory_allocated() / 2**30:.2f} GiB; total {time.time() - t0:.0f} s"
    )


if __name__ == "__main__":
    sys.exit(main())

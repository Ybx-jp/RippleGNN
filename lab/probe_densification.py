"""lab/019 — the Reddit post graph's densification exponent and degree assortativity over the thirty days.

The fourth modelling round (lab/018) predicted Leskovec's densification exponent to be 1
for a degree tail exponent above 2, noted that lab/009 had not reported it, and asked
for it and for the degree assortativity over the thirty days before the preregistration.
This probe computes both from the arrival stream lab/009 derived, on both edge sets.

Snapshot at the end of day d: every post with arrival day < d and every edge whose later
endpoint has arrival day < d (an edge exists from the moment its later post exists, as
in lab/009). For d = 1..30 the probe records n(d), e(d), and Newman's degree
assortativity r(d) — the Pearson correlation of the two endpoint degrees over the edges
of the snapshot — and fits log e against log n by least squares to give the
densification exponent a in e ∝ n^a, over all thirty snapshots and over days 10–30.
It also reports the assortativity of the edges that arrive on each day, split by whether
both endpoints are new that day or one is old.

Verifier: the exponent fit is read on two synthetic growth streams with known a (each
new node attaching to a fixed number of existing nodes, a = 1; to a fixed fraction of
them, a = 2). The assortativity is read on the same edge set with one endpoint column
shuffled (the configuration-model-like known negative, r ≈ 0) and with endpoints paired
by degree rank (the known positive, r → 1).

Reads data/reddit/derived/reddit_stream.npz (written by lab/probe_reddit_stream.py).
No model, no GPU. Seed 20260906 for the synthetic streams and the shuffle.
"""

import sys
import time
from pathlib import Path

import numpy as np

DERIVED = Path(__file__).resolve().parents[1] / "data" / "reddit" / "derived"
SEED = 20260906
DAYS = 30


def log(msg):
    print(msg, flush=True)


def assortativity(lo, hi, deg):
    """Newman (2002) degree assortativity over undirected edges (lo, hi): Pearson r of the
    endpoint degrees, symmetrised so that the order of the two endpoints does not matter."""
    if len(lo) < 2:
        return float("nan")
    a = deg[lo].astype(np.float64)
    b = deg[hi].astype(np.float64)
    x = np.concatenate([a, b])
    y = np.concatenate([b, a])
    mx = x.mean()
    vx = ((x - mx) ** 2).mean()
    if vx == 0:
        return float("nan")
    return float(((x - mx) * (y - mx)).mean() / vx)


def fit_exponent(n, e):
    """Least-squares slope of log e on log n."""
    x = np.log(np.asarray(n, dtype=np.float64))
    y = np.log(np.asarray(e, dtype=np.float64))
    a, b = np.polyfit(x, y, 1)
    resid = y - (a * x + b)
    return float(a), float(np.sqrt((resid**2).mean()))


def snapshot_series(lo, hi, eday, day, n_nodes, label):
    log(f"\n=== {label}: {len(lo):,} undirected edges over {n_nodes:,} nodes ===")
    order = np.argsort(eday, kind="stable")
    lo, hi, eday = lo[order], hi[order], eday[order]
    node_days = np.sort(day)
    rows = []
    log(" day   nodes        edges   e/n     r(all)   r(arrive)  r(new-new)  r(new-old)")
    for d in range(1, DAYS + 1):
        n_d = int(np.searchsorted(node_days, d, side="left"))
        m_d = int(np.searchsorted(eday, d, side="left"))
        m_prev = int(np.searchsorted(eday, d - 1, side="left"))
        l_, h_ = lo[:m_d], hi[:m_d]
        deg = np.bincount(l_, minlength=n_nodes) + np.bincount(h_, minlength=n_nodes)
        r_all = assortativity(l_, h_, deg)
        al, ah = lo[m_prev:m_d], hi[m_prev:m_d]
        r_arr = assortativity(al, ah, deg)
        both_new = (day[al] >= d - 1) & (day[ah] >= d - 1)
        r_nn = assortativity(al[both_new], ah[both_new], deg)
        r_no = assortativity(al[~both_new], ah[~both_new], deg)
        rows.append((d, n_d, m_d, r_all, r_arr, r_nn, r_no))
        log(
            f"{d:4d} {n_d:8,} {m_d:12,} {m_d / max(n_d, 1):6.1f}   {r_all:7.4f}   {r_arr:7.4f}    {r_nn:7.4f}     {r_no:7.4f}"
        )
    rows = np.array(rows, dtype=np.float64)
    n, e = rows[:, 1], rows[:, 2]
    a_all, rms_all = fit_exponent(n, e)
    a_late, rms_late = fit_exponent(n[9:], e[9:])
    a_20_30, _ = fit_exponent(n[19:], e[19:])
    log(
        f"densification exponent a (e ∝ n^a): days 1–30 {a_all:.3f} (rms log resid {rms_all:.3f}); "
        f"days 10–30 {a_late:.3f} ({rms_late:.3f}); days 20–30 {a_20_30:.3f}"
    )
    # the same fact as a, in the reader's units: how many edges a new post brings, and how
    # many edges an existing post gains in a day, both against the graph's size that day
    n_arr = np.diff(np.r_[0, n])
    e_arr = np.diff(np.r_[0, e])
    m_new = np.array(
        [
            ((day[lo[m0:m1]] >= d - 1) & (day[hi[m0:m1]] >= d - 1)).sum()
            for d, m0, m1 in zip(
                range(1, DAYS + 1),
                [int(np.searchsorted(eday, d - 1)) for d in range(1, DAYS + 1)],
                [int(np.searchsorted(eday, d)) for d in range(1, DAYS + 1)],
            )
        ],
        dtype=np.float64,
    )
    per_new_post = e_arr / np.maximum(n_arr, 1)
    old_posts = np.r_[0, n[:-1]]
    per_old_post = (e_arr - m_new) / np.maximum(old_posts, 1)
    b_new, _ = fit_exponent(n[9:], per_new_post[9:])
    b_old, _ = fit_exponent(n[9:], per_old_post[9:])
    log(
        "edges a new post brings on its arrival day, days 1/5/10/15/20/25/30: "
        + " ".join(f"{per_new_post[i]:.0f}" for i in (0, 4, 9, 14, 19, 24, 29))
        + f"; log-log slope against n over days 10–30 {b_new:.2f}"
    )
    log(
        "new edges an existing post gains per day, days 2/5/10/15/20/25/30: "
        + " ".join(f"{per_old_post[i]:.2f}" for i in (1, 4, 9, 14, 19, 24, 29))
        + f"; log-log slope against n over days 10–30 {b_old:.2f}"
    )
    log(
        "edges arriving per day / nodes arriving per day (new edges per new post): "
        + " ".join(
            f"d{int(rows[i, 0])}:{(rows[i, 2] - (rows[i - 1, 2] if i else 0)) / max(rows[i, 1] - (rows[i - 1, 1] if i else 0), 1):.0f}"
            for i in range(0, DAYS, 5)
        )
        + f" d30:{(rows[-1, 2] - rows[-2, 2]) / max(rows[-1, 1] - rows[-2, 1], 1):.0f}"
    )
    return rows


def verifier_assortativity(lo, hi, n_nodes, rng, label):
    deg = np.bincount(lo, minlength=n_nodes) + np.bincount(hi, minlength=n_nodes)
    r_obs = assortativity(lo, hi, deg)
    hi_shuf = hi[rng.permutation(len(hi))]
    deg_shuf = np.bincount(lo, minlength=n_nodes) + np.bincount(hi_shuf, minlength=n_nodes)
    r_null = assortativity(lo, hi_shuf, deg_shuf)
    # perfectly assortative pairing: sort both endpoint columns by degree and pair rank to rank
    ends = np.concatenate([lo, hi])
    ends = ends[np.argsort(deg[ends], kind="stable")]
    lo_pos, hi_pos = ends[0::2], ends[1::2]
    r_pos = assortativity(lo_pos, hi_pos, deg)
    log(
        f"verifier on {label} (final graph): observed r {r_obs:.4f}; one endpoint shuffled "
        f"(known negative) {r_null:.4f}; endpoints paired by degree rank (known positive) {r_pos:.4f}"
    )


def verifier_exponent(rng):
    """Two synthetic growth streams with known densification exponent, read through the
    same day-sampling and fit as the real stream."""
    n_total, per_day = 30_000, 1_000
    for name, mode, expect in (
        ("fixed count m=5", "count", 1.0),
        ("fixed fraction 1%", "frac", 2.0),
    ):
        day = np.repeat(np.arange(DAYS), per_day).astype(np.float64)
        lo_l, hi_l = [], []
        for v in range(1, n_total):
            k = 5 if mode == "count" else max(1, int(0.01 * v))
            k = min(k, v)
            targets = rng.choice(v, size=k, replace=False)
            lo_l.append(np.full(k, v))
            hi_l.append(targets)
        lo = np.concatenate(lo_l)
        hi = np.concatenate(hi_l)
        eday = np.maximum(day[lo], day[hi])
        order = np.argsort(eday, kind="stable")
        lo, hi, eday = lo[order], hi[order], eday[order]
        node_days = np.sort(day)
        n = [np.searchsorted(node_days, d) for d in range(1, DAYS + 1)]
        e = [np.searchsorted(eday, d) for d in range(1, DAYS + 1)]
        a, rms = fit_exponent(n, e)
        a_late, _ = fit_exponent(n[9:], e[9:])
        log(
            f"verifier exponent on synthetic '{name}' (expected a = {expect:.0f}): "
            f"days 1–30 {a:.3f} (rms {rms:.3f}), days 10–30 {a_late:.3f}"
        )


def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    z = np.load(DERIVED / "reddit_stream.npz")
    day = z["day"]
    n_nodes = len(day)
    log(f"nodes {n_nodes:,}; arrival days span [{day.min():.2f}, {day.max():.2f}]")
    verifier_exponent(rng)
    results = {}
    for label, key in (("paper (G.json)", "paper"), ("full (PyG/G_full)", "full")):
        lo, hi, eday = z[f"{key}_lo"], z[f"{key}_hi"], z[f"{key}_day"].astype(np.float64)
        verifier_assortativity(lo, hi, n_nodes, rng, label)
        results[key] = snapshot_series(lo, hi, eday, day, n_nodes, label)
    out = DERIVED / "densification.npz"
    np.savez(out, **{f"{k}_rows": v for k, v in results.items()})
    log(f"\nwrote {out}; {time.time() - t0:.0f} s")


if __name__ == "__main__":
    sys.exit(main())

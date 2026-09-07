"""lab/020 — what share of the edges the real stream brings to an existing post come from another subreddit.

lab/015 read the real stream's coherence (cosine 0.05–0.10 among stale neighbours'
deltas, between the deletion and insertion brackets) as the contribution of the
cross-subreddit share of the arriving edges, and did not split the stream by edge type;
lab/018 names that share, unmeasured, as what sets the generator's coherence anchor.
This probe measures the share itself, on the CPU, from the arrival stream lab/009
derived and the subreddit label each post carries.

For every edge that joins a new post to an existing one, "foreign" means the two posts'
subreddit labels differ. The probe reports the foreign share of new-to-old edges by
arrival day, by the existing endpoint's degree decile at day 20 (over days 20–30), and
per existing post as the median and quartiles over posts by decile of the share of its
day-20-to-30 arrivals that are foreign; and the same share for the edges between two
posts arriving the same day and for the graph's existing edges at day 20. The known
negative is the label-shuffled graph, whose foreign share is the chance value 1 minus
the sum of squared label frequencies.

Reads data/reddit/derived/reddit_stream.npz and data/reddit/pyg/raw/reddit_data.npz.
No model, no GPU. Seed 20260906 for the label shuffle.
"""

import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1] / "data" / "reddit"
DERIVED = ROOT / "derived"
PYG = ROOT / "pyg" / "raw"
SEED = 20260906
TRAIN_DAYS = 20


def log(msg):
    print(msg, flush=True)


def deciles(values, mask):
    """Decile index 0–9 of each masked node by its value, ties broken by index; -1 elsewhere."""
    out = np.full(len(values), -1, dtype=np.int64)
    idx = np.flatnonzero(mask)
    ranks = np.empty(len(idx), dtype=np.int64)
    ranks[np.argsort(values[idx], kind="stable")] = np.arange(len(idx))
    out[idx] = np.minimum(ranks * 10 // len(idx), 9)
    return out


def report(label, lo, hi, eday, day, labels, n, rng):
    log(f"\n=== {label}: {len(lo):,} undirected edges ===")
    foreign_edge = labels[lo] != labels[hi]
    old = day < TRAIN_DAYS
    pre = eday < TRAIN_DAYS
    deg20 = np.bincount(lo[pre], minlength=n) + np.bincount(hi[pre], minlength=n)
    dec = deciles(deg20, old)
    edges20 = int(pre.sum())
    log(
        f"existing edges at day 20: {edges20:,}, foreign share {foreign_edge[pre].mean():.3f}; "
        f"chance under a label shuffle {1 - ((np.bincount(labels) / n) ** 2).sum():.3f}"
    )
    # verifier: shuffle labels, the foreign share of every edge class goes to chance
    shuffled = labels[rng.permutation(n)]
    log(
        f"verifier: with labels shuffled the existing-edge foreign share reads "
        f"{(shuffled[lo[pre]] != shuffled[hi[pre]]).mean():.3f}"
    )

    lo_new, hi_new = day[lo] >= TRAIN_DAYS, day[hi] >= TRAIN_DAYS
    one_new = lo_new ^ hi_new
    both_new = lo_new & hi_new
    log(
        f"edges arriving from day 20: new-to-old {one_new.sum():,} foreign share {foreign_edge[one_new].mean():.3f}; "
        f"new-to-new {both_new.sum():,} foreign share {foreign_edge[both_new].mean():.3f}"
    )
    # by arrival day: an edge arriving on day d whose earlier endpoint arrived before
    # day d is a new-to-old edge of that day; the rest join two posts of the same day
    ed = np.clip(eday.astype(int), 0, 30)
    earlier = np.minimum(day[lo], day[hi])
    rows_old, rows_same = [], []
    for d in range(1, 31):
        sel = ed == d
        to_old = sel & (earlier < d)
        same = sel & ~(earlier < d)
        rows_old.append(f"d{d}:{foreign_edge[to_old].mean():.2f}")
        rows_same.append(f"d{d}:{foreign_edge[same].mean():.2f}")
    log("foreign share of the day's new-to-old edges: " + " ".join(rows_old))
    log("foreign share of the day's same-day edges:   " + " ".join(rows_same))

    # by the old endpoint's day-20 degree decile
    old_end = np.where(lo_new, hi, lo)[one_new]
    new_end = np.where(lo_new, lo, hi)[one_new]
    f = (labels[old_end] != labels[new_end]).astype(np.float64)
    d_old = dec[old_end]
    share = [f[d_old == k].mean() for k in range(10)]
    log(
        "foreign share of new-to-old edges by the old endpoint's day-20 degree decile (0 lowest): "
        + " ".join(f"{s:.3f}" for s in share)
    )
    # per existing post: the share of its own arrivals that are foreign, over days 20–30
    arrivals = np.bincount(old_end, minlength=n).astype(np.float64)
    foreign = np.bincount(old_end, weights=f, minlength=n)
    has = old & (arrivals > 0)
    per_post = np.where(has, foreign / np.maximum(arrivals, 1), np.nan)
    log(
        f"existing posts receiving at least one arrival over days 20–30: {has.sum():,} of {old.sum():,} "
        f"({has.mean() / old.mean():.3f}); per-post foreign share of its arrivals, "
        "median (quartiles) by decile: "
        + " ".join(
            f"{np.nanmedian(per_post[has & (dec == k)]):.2f}"
            f"({np.nanpercentile(per_post[has & (dec == k)], 25):.2f}-{np.nanpercentile(per_post[has & (dec == k)], 75):.2f})"
            for k in range(10)
        )
    )
    # how concentrated a post's foreign arrivals are: over posts with at least ten foreign
    # arrivals, the share of them carrying the post's single most common foreign label
    f_mask = f > 0
    keys = old_end[f_mask].astype(np.int64) * 64 + labels[new_end[f_mask]]
    uniq, counts = np.unique(keys, return_counts=True)
    top = np.zeros(n, dtype=np.float64)
    np.maximum.at(top, uniq // 64, counts)
    enough = old & (foreign >= 10)
    conc = top[enough] / foreign[enough]
    log(
        f"posts with at least ten foreign arrivals: {enough.sum():,}; share of a post's foreign arrivals "
        "in its most common foreign subreddit, median (quartiles) by decile: "
        + " ".join(
            (
                f"{np.median(conc[dec[enough] == k]):.2f}"
                f"({np.percentile(conc[dec[enough] == k], 25):.2f}-{np.percentile(conc[dec[enough] == k], 75):.2f})"
                f"[n={int((dec[enough] == k).sum())}]"
            )
            if (dec[enough] == k).any()
            else "-"
            for k in range(10)
        )
    )
    # how the arriving foreign edges are placed: the share of a post's day-20 neighbourhood
    # that is foreign, before and after the ten days, by decile
    f_edge_pre = foreign_edge[pre]
    nb_pre = np.bincount(lo[pre], minlength=n) + np.bincount(hi[pre], minlength=n)
    fb_pre = np.bincount(lo[pre], weights=f_edge_pre, minlength=n) + np.bincount(
        hi[pre], weights=f_edge_pre, minlength=n
    )
    nb_post = nb_pre + arrivals
    fb_post = fb_pre + foreign
    log(
        "median share of a post's neighbourhood that is foreign, day 20 -> day 30, by decile: "
        + " ".join(
            f"{np.median(fb_pre[old & (dec == k)] / np.maximum(nb_pre[old & (dec == k)], 1)):.2f}->"
            f"{np.median(fb_post[old & (dec == k)] / np.maximum(nb_post[old & (dec == k)], 1)):.2f}"
            for k in range(10)
        )
    )


def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    z = np.load(DERIVED / "reddit_stream.npz")
    labels = np.load(PYG / "reddit_data.npz")["label"].astype(np.int64)
    day = z["day"]
    n = len(day)
    log(
        f"nodes {n:,}; labels {labels.max() + 1}; largest label share {np.bincount(labels).max() / n:.3f}"
    )
    for label, key in (("paper (G.json)", "paper"), ("full (PyG/G_full)", "full")):
        report(label, z[f"{key}_lo"], z[f"{key}_hi"], z[f"{key}_day"], day, labels, n, rng)
    log(f"\n{time.time() - t0:.0f} s")


if __name__ == "__main__":
    sys.exit(main())

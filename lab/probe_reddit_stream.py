"""lab/009 — does the Reddit post graph carry an arrival order, and what does its real stream look like?

lab/008's first probe. The PyG copy of Reddit has features, labels, split masks and an
edge list, and nothing that orders nodes in time. The original GraphSAGE release keys
its id map by the post's Reddit id, a base-36 counter that increases with creation.
This probe checks that premise against the data (the published split is "first twenty
days train, the rest val/test", so if ids order posts by creation the split must be a
single id threshold), then characterises the stream the ids imply: insertion rates,
what fraction of the arriving edges land on hubs, how new edges scale with existing
degree, the degree tail, and per-node burstiness.

Two edge sets exist over the same 232,965 nodes: the paper's graph (reddit-G.json,
11.6M undirected edges) and the full graph (reddit-G_full.json, 57.3M), which is the
one the PyG/DGL copy ships. Both are reported.

Inputs: data/reddit/graphsage/reddit/{reddit-id_map.json, reddit-G.json} from the
GraphSAGE release (snap.stanford.edu/graphsage/reddit.zip) and
data/reddit/pyg/raw/{reddit_data.npz, reddit_graph.npz} from the PyG/DGL copy
(data.dgl.ai/dataset/reddit.zip). Writes data/reddit/derived/reddit_stream.npz, which
carries both edge sets with their arrival days, for later probes.
"""

import json
import sys
import time
from pathlib import Path

import numpy as np
import scipy.sparse as sp

ROOT = Path(__file__).resolve().parents[1] / "data" / "reddit"
GS = ROOT / "graphsage" / "reddit"
PYG = ROOT / "pyg" / "raw"
DERIVED = ROOT / "derived"
TRAIN_DAYS = 20  # the published split: first 20 days of September 2014 are train
KEY = 300_000  # > num_nodes; packs an undirected pair into one int64


def log(msg):
    print(msg, flush=True)


def pairs(lo, hi):
    return np.unique(lo.astype(np.int64) * KEY + hi.astype(np.int64))


def unpack(k):
    return (k // KEY).astype(np.int32), (k % KEY).astype(np.int32)


def hill(deg, q):
    """Hill estimator of the power-law tail exponent alpha (p(k) ~ k^-alpha) above the q-quantile."""
    xmin = np.quantile(deg, q)
    tail = deg[deg >= xmin].astype(np.float64)
    if xmin <= 0 or len(tail) < 10:
        return float("nan"), xmin, len(tail)
    return 1 + len(tail) / np.log(tail / xmin).sum(), xmin, len(tail)


def burstiness(edge_time, endpoint, n, min_events=20):
    """Goh–Barabási burstiness B=(s-m)/(s+m) of a node's inter-arrival gaps, over nodes with >= min_events."""
    order = np.lexsort((edge_time, endpoint))
    ep = endpoint[order]
    t = edge_time[order]
    starts = np.flatnonzero(np.r_[True, ep[1:] != ep[:-1]])
    ends = np.r_[starts[1:], len(ep)]
    out = []
    for s, e in zip(starts, ends):
        if e - s < min_events:
            continue
        gaps = np.diff(t[s:e]).astype(np.float64)
        gaps = gaps[gaps > 0]
        if len(gaps) < min_events - 1:
            continue
        m, sd = gaps.mean(), gaps.std()
        out.append((sd - m) / (sd + m))
    return np.array(out)


def main():
    t0 = time.time()
    idmap = json.load(open(GS / "reddit-id_map.json"))
    n = len(idmap)
    post_id = np.zeros(n, dtype=np.int64)
    for k, v in idmap.items():
        post_id[v] = int(k, 36)
    data = np.load(PYG / "reddit_data.npz")
    split = data["node_types"]  # 1 train, 2 val, 3 test
    node_ids = data["node_ids"]
    log(
        f"nodes {n}; PyG node_ids is the identity permutation: {np.array_equal(node_ids, np.arange(n))}"
    )
    log(f"PyG raw arrays: {sorted(data.files)} (no timestamp field)")
    log(
        f"GraphSAGE id_map keys decode as base-36 ints in [{post_id.min()}, {post_id.max()}] "
        f"= [{np.base_repr(post_id.min(), 36).lower()}, {np.base_repr(post_id.max(), 36).lower()}]"
    )

    # --- premise check: is the published temporal split a single post-id threshold? ---
    ids_sorted = np.sort(post_id)
    is_train = split == 1
    thr = post_id[is_train].max()
    non_train_below = (post_id[~is_train] <= thr).sum()
    train_above = (post_id[is_train] > post_id[~is_train].min()).sum()
    log(
        f"split as an id threshold: max train id {thr} ({np.base_repr(thr, 36).lower()}); "
        f"non-train ids at or below it: {non_train_below}; train ids above min non-train id: {train_above}"
    )
    id0 = ids_sorted[0]
    rate = (thr - id0) / TRAIN_DAYS  # id units per day, from the train side only
    test_span_days = (ids_sorted[-1] - thr) / rate
    log(
        f"id-counter rate from the train side: {rate:,.0f} ids/day; "
        f"the ids above the threshold then span {test_span_days:.2f} days "
        f"(a 30-day month predicts {30 - TRAIN_DAYS})"
    )
    day = (post_id - id0) / rate

    # --- edge sets ---
    # reddit-G.json is networkx 1.x node-link data: a link's source/target are positions in
    # the nodes list, not node ids, so they are mapped through the node's id and the id map.
    G = json.load(open(GS / "reddit-G.json"))
    pos2idx = np.array([idmap[nd["id"]] for nd in G["nodes"]])
    gs = pos2idx[np.fromiter((lk["source"] for lk in G["links"]), dtype=np.int64)]
    gt = pos2idx[np.fromiter((lk["target"] for lk in G["links"]), dtype=np.int64)]
    del G
    a = sp.load_npz(PYG / "reddit_graph.npz").tocoo()
    edge_sets = {
        "paper (G.json)": pairs(np.minimum(gs, gt), np.maximum(gs, gt)),
        "full (PyG/G_full)": pairs(np.minimum(a.row, a.col), np.maximum(a.row, a.col)),
    }
    del a
    log(
        f"paper edges are a subset of full edges: {np.isin(edge_sets['paper (G.json)'], edge_sets['full (PyG/G_full)']).all()}"
    )

    # --- node insertion rate ---
    nb = np.bincount(np.clip(day.astype(int), 0, 30), minlength=31)
    log("\nnodes created per day (day index from the earliest post):")
    log(" ".join(f"{i}:{c}" for i, c in enumerate(nb) if c))
    log(
        f"train {is_train.sum()} nodes over {TRAIN_DAYS} days = {is_train.sum() / TRAIN_DAYS:,.0f}/day; "
        f"val+test {(~is_train).sum()} over {test_span_days:.1f} days = {(~is_train).sum() / test_span_days:,.0f}/day"
    )

    out = {"post_id": post_id, "day": day, "split": split}
    for name, k in edge_sets.items():
        lo, hi = unpack(k)
        m = len(k)
        deg = np.bincount(lo, minlength=n) + np.bincount(hi, minlength=n)
        eday = np.maximum(day[lo], day[hi])  # an edge exists once its later post exists
        elo_new = day[lo] >= TRAIN_DAYS
        ehi_new = day[hi] >= TRAIN_DAYS
        new = eday >= TRAIN_DAYS
        log(
            f"\n=== {name}: {m:,} undirected edges, mean degree {2 * m / n:.1f}, max {deg.max()}, isolated {int((deg == 0).sum())} ==="
        )
        eb = np.bincount(np.clip(eday.astype(int), 0, 30), minlength=31)
        log("edges arriving per day: " + " ".join(f"{i}:{c}" for i, c in enumerate(eb) if c))
        log(
            f"edges arriving at day >= {TRAIN_DAYS}: {new.sum():,} ({new.mean():.1%}); "
            f"of those, both endpoints new: {(elo_new & ehi_new)[new].mean():.1%}, exactly one new: {(elo_new ^ ehi_new)[new].mean():.1%}, "
            f"neither new: {(~elo_new & ~ehi_new)[new].sum()} (zero by construction)"
        )

        # degree at the split boundary, over nodes that exist then
        old = day < TRAIN_DAYS
        pre = ~new
        deg20 = np.bincount(lo[pre], minlength=n) + np.bincount(hi[pre], minlength=n)
        gain = deg - deg20
        top_final = deg >= np.quantile(deg[deg > 0], 0.9)
        top20 = np.zeros(n, dtype=bool)
        top20[old] = deg20[old] >= np.quantile(deg20[old], 0.9)
        log(
            f"fraction of arriving edges incident to a top-decile node by final degree: {(top_final[lo] | top_final[hi])[new].mean():.1%}; "
            f"by degree at day {TRAIN_DAYS} (old endpoint only): {(top20[lo] | top20[hi])[new].mean():.1%}"
        )
        # share of new-edge mass landing on old nodes, by old-node degree decile at day 20
        old_end = np.where(elo_new[new], hi[new], lo[new])  # the old endpoint of a one-new edge
        one_new = (elo_new ^ ehi_new)[new]
        old_end = old_end[one_new]
        ranks = np.zeros(n, dtype=np.int64)
        oi = np.flatnonzero(old)
        ranks[oi[np.argsort(deg20[oi])]] = np.arange(len(oi))
        dec = np.minimum(ranks * 10 // len(oi), 9)
        share = np.bincount(dec[old_end], minlength=10) / len(old_end)
        log(
            "share of new old-to-new edges by old endpoint's day-20 degree decile (0=lowest): "
            + " ".join(f"{s:.3f}" for s in share)
        )

        # preferential-attachment exponent: mean gain vs day-20 degree, log-binned
        d20 = deg20[oi]
        g = gain[oi]
        bins = np.unique(np.logspace(0, np.log10(d20.max() + 1), 25).astype(int))
        which = np.digitize(d20, bins)
        xs, ys = [], []
        for b in range(1, len(bins) + 1):
            sel = which == b
            if sel.sum() >= 50 and d20[sel].mean() > 0:
                xs.append(d20[sel].mean())
                ys.append(g[sel].mean())
        xs, ys = np.array(xs), np.array(ys)
        keep = ys > 0
        slope = np.polyfit(np.log(xs[keep]), np.log(ys[keep]), 1)[0]
        log(
            f"activity-vs-degree exponent (log mean new edges vs log day-{TRAIN_DAYS} degree, {keep.sum()} bins): {slope:.2f}"
        )
        log("   degree bin means: " + " ".join(f"{x:.0f}->{y:.1f}" for x, y in zip(xs, ys)))

        for q in (0.90, 0.95, 0.99):
            alpha, xmin, cnt = hill(deg[deg > 0], q)
            log(
                f"Hill tail exponent above q={q:.2f} (k_min={xmin:.0f}, {cnt} nodes): alpha={alpha:.2f}"
            )

        # burstiness of per-node edge arrivals, in id-counter time
        etime = np.maximum(post_id[lo], post_id[hi])
        endpoint = np.concatenate([lo, hi])
        etime2 = np.concatenate([etime, etime])
        B = burstiness(etime2, endpoint, n)
        log(
            f"per-node burstiness B over {len(B)} nodes with >=20 arrivals: median {np.median(B):.3f}, "
            f"IQR [{np.quantile(B, 0.25):.3f}, {np.quantile(B, 0.75):.3f}] (0 = Poisson, 1 = maximally bursty)"
        )

        tag = "paper" if name.startswith("paper") else "full"
        out[f"{tag}_lo"], out[f"{tag}_hi"], out[f"{tag}_day"] = lo, hi, eday.astype(np.float32)

    DERIVED.mkdir(exist_ok=True)
    np.savez(DERIVED / "reddit_stream.npz", **out)
    log(f"\nwrote {DERIVED / 'reddit_stream.npz'}; {time.time() - t0:.0f} s total")


if __name__ == "__main__":
    sys.exit(main())

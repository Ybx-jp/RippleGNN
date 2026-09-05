"""lab/014 — the ogbn-arxiv arrival order, its episode count, and the full recompute on the real graph.

lab/008's probe list asks for the ogbn-arxiv episode count and its full recompute; the
operator moved it ahead of the modelling ruling because arxiv is the plan's one sparse
graph. This probe reads the pinned OGB archive (arxiv.zip, 83,058,288 bytes, sha256
49f85c801589ecdcc52cfaca99693aaea7b8af16a9ac3f41dd85a5f3193fe276) once into
data/arxiv/derived/arxiv.npz, and reports:

  - the clock the dataset carries (a publication year per paper, nothing finer), the
    papers per year, and where the published time split falls;
  - whether the MAG paper id orders papers in time, as the Reddit post id did (lab/009);
  - the stream under the same convention as lab/009: an edge exists from the year its
    later paper exists, so a year's arrivals are the papers of that year and every edge
    with one endpoint among them; the share joining two new papers, a new to an old, and
    two old (zero by construction, checked);
  - the degree distribution of the undirected graph before 2018 and at the end, beside
    the Reddit post graph before day 20, since the operator's hypothesis is about degree;
  - which old papers receive the arriving edges, by degree decile, and the attachment slope;
  - full recompute of a two-layer GraphSAGE on the final undirected graph, edge_index and
    CSR paths, hidden 64 and 128, synchronized, median of five passes.

    uv run python lab/probe_arxiv_stream.py
"""

import gzip
import statistics
import sys
import time
from pathlib import Path

import numpy as np
import torch
from torch_geometric.nn import SAGEConv
from torch_geometric.utils import to_torch_csr_tensor

ROOT = Path(__file__).resolve().parents[1] / "data" / "arxiv"
RAW = ROOT / "arxiv"
DERIVED = ROOT / "derived" / "arxiv.npz"
REDDIT = Path(__file__).resolve().parents[1] / "data" / "reddit"
SPLIT_YEAR = 2018  # the published split: train <= 2017, valid 2018, test >= 2019
SEED = 20260903
REPS = 5
dev = torch.device("cuda")


def read_csv_gz(path, dtype):
    with gzip.open(path, "rt") as f:
        return np.loadtxt(f, delimiter=",", dtype=dtype, ndmin=1)


def build():
    """Parse the OGB CSVs once. Edges are (citing, cited) per the OGB documentation."""
    t = time.time()
    x = read_csv_gz(RAW / "raw" / "node-feat.csv.gz", np.float32)
    y = read_csv_gz(RAW / "raw" / "node-label.csv.gz", np.int64)
    year = read_csv_gz(RAW / "raw" / "node_year.csv.gz", np.int64)
    e = read_csv_gz(RAW / "raw" / "edge.csv.gz", np.int64)
    n = len(y)
    with gzip.open(RAW / "mapping" / "nodeidx2paperid.csv.gz", "rt") as f:
        m = np.loadtxt(f, delimiter=",", dtype=np.int64, skiprows=1)
    assert (m[:, 0] == np.arange(n)).all()
    paper_id = m[:, 1]
    split = np.zeros(n, np.int8)
    for k, name in ((1, "train"), (2, "valid"), (3, "test")):
        split[read_csv_gz(RAW / "split" / "time" / f"{name}.csv.gz", np.int64)] = k
    assert (split > 0).all()
    src, dst = e[:, 0], e[:, 1]
    a, b = np.minimum(src, dst), np.maximum(src, dst)
    keep = a != b
    und = np.unique(np.stack([a[keep], b[keep]], 1), axis=0)
    ROOT.joinpath("derived").mkdir(exist_ok=True)
    np.savez(
        DERIVED,
        x=x,
        y=y,
        year=year,
        paper_id=paper_id,
        split=split,
        src=src,
        dst=dst,
        lo=und[:, 0],
        hi=und[:, 1],
    )
    print(
        f"parsed {n} papers, {len(src)} directed edges ({int((~keep).sum())} self-loops), "
        f"{len(und)} undirected edges, in {time.time() - t:.0f} s -> {DERIVED.relative_to(ROOT.parent.parent)}"
    )


def deciles(deg):
    q = np.quantile(deg, np.linspace(0, 1, 11))
    return ", ".join(f"{int(v)}" for v in q)


def describe_degree(name, deg):
    print(
        f"{name:<34} n {len(deg):>7}  mean {deg.mean():>6.1f}  median {int(np.median(deg)):>4}  "
        f"max {int(deg.max()):>6}  deg<=8 {100 * (deg <= 8).mean():>5.1f}%  deg<=2 {100 * (deg <= 2).mean():>5.1f}%  "
        f"deg=0 {100 * (deg == 0).mean():>5.1f}%"
    )
    print(f"{'':<34} decile edges {deciles(deg)}")


class Sage(torch.nn.Module):
    def __init__(self, d_in, d_h):
        super().__init__()
        self.c1 = SAGEConv(d_in, d_h)
        self.c2 = SAGEConv(d_h, d_h)

    def forward(self, x, adj):
        return self.c2(torch.relu(self.c1(x, adj)), adj)


def timed(model, x, adj):
    torch.cuda.synchronize()
    torch.cuda.empty_cache()
    torch.cuda.reset_peak_memory_stats()
    times = []
    with torch.no_grad():
        for i in range(REPS + 1):
            torch.cuda.synchronize()
            t = time.perf_counter()
            model(x, adj)
            torch.cuda.synchronize()
            if i:
                times.append(time.perf_counter() - t)
    return statistics.median(times), torch.cuda.max_memory_allocated() / 2**30


def main():
    if not DERIVED.exists():
        build()
    d = np.load(DERIVED)
    x, y, year, pid, split = d["x"], d["y"], d["year"], d["paper_id"], d["split"]
    src, dst, lo, hi = d["src"], d["dst"], d["lo"], d["hi"]
    n = len(y)
    print(
        f"\n{n} papers, {x.shape[1]} features, {int(y.max()) + 1} classes, {len(lo)} undirected edges"
    )

    print("\n== the clock: papers per publication year, with the published split")
    ys, cs = np.unique(year, return_counts=True)
    for yv, c in zip(ys, cs):
        s = np.bincount(split[year == yv], minlength=4)[1:]
        print(f"  {yv}: {c:>6} papers  (train {s[0]}, valid {s[1]}, test {s[2]})")
    print(
        f"  years with >= 1,000 papers: {int((cs >= 1000).sum())}; >= 5,000: {int((cs >= 5000).sum())}; "
        f"train years <= {year[split == 1].max()}, valid {year[split == 2].min()}-{year[split == 2].max()}, "
        f"test {year[split == 3].min()}-{year[split == 3].max()}"
    )
    old = year < SPLIT_YEAR
    assert ((split == 1) == old).all(), "the published train split is not exactly year <= 2017"

    print("\n== is the MAG paper id a clock?")
    order = np.argsort(pid, kind="stable")
    yr_by_id = year[order]
    rng = np.random.default_rng(SEED)
    i, j = rng.integers(0, n, 2_000_000), rng.integers(0, n, 2_000_000)
    dif = year[i] != year[j]
    conc = ((pid[i] < pid[j]) == (year[i] < year[j]))[dif].mean()
    print(
        f"  paper id range {pid.min()}-{pid.max()}; Spearman(id, year) {np.corrcoef(np.argsort(np.argsort(pid)), np.argsort(np.argsort(year)))[0, 1]:.3f}; "
        f"concordant pairs across years {100 * conc:.1f}% (50 = no order); "
        f"mean |year(id-sorted) - year(sorted)| {np.abs(yr_by_id - np.sort(year)).mean():.2f} years"
    )

    print("\n== the stream: an edge exists from the year its later paper exists")
    cy, dy = year[src], year[dst]
    print(
        f"  directed edges: citing year > cited {100 * (cy > dy).mean():.1f}%, equal {100 * (cy == dy).mean():.1f}%, "
        f"citing year < cited {100 * (cy < dy).mean():.1f}%"
    )
    e_year = np.maximum(year[lo], year[hi])
    deg_old = np.bincount(np.r_[lo[old[lo] & old[hi]], hi[old[lo] & old[hi]]], minlength=n)
    deg_end = np.bincount(np.r_[lo, hi], minlength=n)
    edges_old = np.quantile(deg_old[old], np.linspace(0, 1, 11))
    dec_old = np.clip(np.searchsorted(edges_old, deg_old, side="right") - 1, 0, 9)
    print(
        f"  {'year':>5} {'papers':>7} {'edges':>8} {'new-new':>8} {'new-old':>8} {'old-old':>8} {'papers %':>9} {'edges %':>8}"
    )
    for yv in ys:
        if yv < 2000:
            continue
        pres = year < yv
        arr = e_year == yv
        new_lo, new_hi = year[lo[arr]] == yv, year[hi[arr]] == yv
        nn_ = int((new_lo & new_hi).sum())
        no = int((new_lo ^ new_hi).sum())
        oo = int((~new_lo & ~new_hi).sum())
        n_pres, e_pres = int(pres.sum()), int((e_year < yv).sum())
        print(
            f"  {yv:>5} {int((year == yv).sum()):>7} {int(arr.sum()):>8} {nn_:>8} {no:>8} {oo:>8} "
            f"{100 * (year == yv).sum() / max(n_pres, 1):>8.1f}% {100 * arr.sum() / max(e_pres, 1):>7.1f}%"
        )
    assert not ((~(year[lo] == e_year)) & (~(year[hi] == e_year))).any()

    print("\n== where the post-2017 arrivals land: old endpoint's pre-2018 degree decile")
    arr = e_year >= SPLIT_YEAR
    o = np.where(old[lo[arr]], lo[arr], np.where(old[hi[arr]], hi[arr], -1))
    o = o[o >= 0]
    share = np.bincount(dec_old[o], minlength=10) / len(o)
    print("  share by decile, lowest to highest: " + ", ".join(f"{100 * s:.1f}" for s in share))
    gained = deg_end - deg_old
    lb = np.floor(np.log2(np.maximum(deg_old[old], 1))).astype(int)
    xs, ys_ = [], []
    for b in np.unique(lb):
        sel = lb == b
        if sel.sum() >= 50 and deg_old[old][sel].mean() > 0:
            xs.append(np.log(deg_old[old][sel].mean()))
            ys_.append(np.log(max(gained[old][sel].mean(), 1e-9)))
    slope = np.polyfit(xs, ys_, 1)[0]
    print(
        f"  mean edges gained 2018-2020 against pre-2018 degree, log-binned: slope {slope:.2f} "
        f"(1 = linear preferential attachment); papers of pre-2018 degree 0: {int((deg_old[old] == 0).sum())}, "
        f"of which gain an edge by 2020: {100 * (gained[old][deg_old[old] == 0] > 0).mean():.1f}%"
    )

    print("\n== degree distributions, undirected")
    describe_degree("arxiv, papers before 2018", deg_old[old])
    describe_degree("arxiv, all papers at the end", deg_end)
    rs = np.load(REDDIT / "derived" / "reddit_stream.npz")
    rday = rs["day"]
    rlo, rhi = rs["paper_lo"].astype(np.int64), rs["paper_hi"].astype(np.int64)
    rold = rday < 20.0
    re_old = rold[rlo] & rold[rhi]
    rdeg = np.bincount(np.r_[rlo[re_old], rhi[re_old]], minlength=len(rday))
    describe_degree("reddit (paper edges), before day 20", rdeg[rold])
    rdeg_end = np.bincount(np.r_[rlo, rhi], minlength=len(rday))
    describe_degree("reddit (paper edges), all posts", rdeg_end)

    print("\n== full recompute on the final undirected graph, untrained, eval, fp32")
    torch.manual_seed(SEED)
    xt = torch.from_numpy(x).to(dev)
    ei = torch.from_numpy(np.stack([np.r_[lo, hi], np.r_[hi, lo]])).to(dev)
    print(f"  {'path':<10} {'hidden':>6} {'ms':>9} {'peak GiB':>9}")
    for path in ("edge_index", "csr"):
        adj = ei if path == "edge_index" else to_torch_csr_tensor(ei, size=(n, n))
        for hidden in (64, 128):
            model = Sage(x.shape[1], hidden).to(dev).eval()
            ms, peak = timed(model, xt, adj)
            print(f"  {path:<10} {hidden:>6} {ms * 1e3:>9.1f} {peak:>9.2f}")
            del model
        del adj
        torch.cuda.empty_cache()


if __name__ == "__main__":
    sys.exit(main())

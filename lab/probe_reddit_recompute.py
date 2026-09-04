"""lab/009 — full recompute on the real Reddit post graph, not a synthetic graph of its shape.

lab/004 and A0010 timed two-layer GraphSAGE on a random graph with Reddit's published node
and edge counts, with the input width equal to the hidden width. The real graph has two
things that shape did not: 602-dim input features, and two candidate edge sets (the
paper's 11.6M and the full 57.3M that PyG ships). The dense message path materialises a
tensor per edge at the input width on the first layer, so 602 x edges, not 64 x edges.
This probe measures peak VRAM and synchronized wall clock for both edge sets, both
paths (edge_index gather, and CSR sparse-matrix aggregation), at hidden 64 and 128,
untrained weights, eval mode, fp32.
"""

import statistics
import sys
import time
from pathlib import Path

import numpy as np
import torch
from torch_geometric.nn import SAGEConv
from torch_geometric.utils import to_torch_csr_tensor

ROOT = Path(__file__).resolve().parents[1] / "data" / "reddit"
SEED = 20260903
REPS = 5
dev = torch.device("cuda")


def load():
    data = np.load(ROOT / "pyg" / "raw" / "reddit_data.npz")
    x = torch.from_numpy(data["feature"]).to(torch.float32)
    n = x.shape[0]
    st = np.load(ROOT / "derived" / "reddit_stream.npz")  # written by probe_reddit_stream.py
    sets = {}
    for tag, name in (("paper", "paper 11.6M"), ("full", "full 57.3M")):
        lo, hi = st[f"{tag}_lo"].astype(np.int64), st[f"{tag}_hi"].astype(np.int64)
        sets[name] = torch.from_numpy(np.stack([np.r_[lo, hi], np.r_[hi, lo]]))
    return x, n, sets


class Sage(torch.nn.Module):
    def __init__(self, d_in, d_h):
        super().__init__()
        self.c1 = SAGEConv(d_in, d_h)
        self.c2 = SAGEConv(d_h, d_h)

    def forward(self, x, adj):
        return self.c2(torch.relu(self.c1(x, adj)), adj)


def run(model, x, adj):
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
            if i:  # first pass is warm-up
                times.append(time.perf_counter() - t)
    return statistics.median(times), torch.cuda.max_memory_allocated() / 2**30


def main():
    torch.manual_seed(SEED)
    x, n, sets = load()
    print(
        f"nodes {n}, input width {x.shape[1]}, fp32, untrained, eval, median of {REPS} synchronized passes"
    )
    print(f"{'edge set':<12} {'path':<10} {'hidden':>6} {'ms':>9} {'peak GiB':>9}")
    x = x.to(dev)
    for name, ei in sets.items():
        ei = ei.to(dev)
        for path in ("edge_index", "csr"):
            adj = ei if path == "edge_index" else to_torch_csr_tensor(ei, size=(n, n))
            for hidden in (64, 128):
                model = Sage(x.shape[1], hidden).to(dev).eval()
                try:
                    ms, peak = run(model, x, adj)
                    print(f"{name:<12} {path:<10} {hidden:>6} {ms * 1e3:>9.1f} {peak:>9.2f}")
                except torch.cuda.OutOfMemoryError:
                    print(f"{name:<12} {path:<10} {hidden:>6} {'OOM':>9} {'-':>9}")
                    torch.cuda.empty_cache()
                del model
            del adj
            torch.cuda.empty_cache()
        del ei
        torch.cuda.empty_cache()


if __name__ == "__main__":
    sys.exit(main())

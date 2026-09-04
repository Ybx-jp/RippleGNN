"""lab/010 — the untrained-weights control on Reddit at 64, against the trained number.

lab/008's second probe. The measurement consultation predicted that task quality on the
Reddit post graph does not survive as an estimand because the label signal is largely
in the 602 features, and that the untrained-weights control would show it in seconds.
This probe measures three things on each edge set, full-batch on the CSR path:

  trained     two-layer GraphSAGE (602 -> 64 -> 64) and a linear head, trained end to end
  untrained   the same GraphSAGE with its random initial weights frozen, a linear head
              trained on its 64-dim output
  features    a linear head on the 602 features alone, and a 602 -> 64 -> 41 MLP

Test micro-F1 (accuracy, since the task is single-label) at the best validation epoch.
Reads data/reddit/derived/reddit_stream.npz written by probe_reddit_stream.py.
"""

import sys
import time
from pathlib import Path

import numpy as np
import torch
from torch_geometric.nn import SAGEConv
from torch_geometric.utils import to_torch_csr_tensor

ROOT = Path(__file__).resolve().parents[1] / "data" / "reddit"
SEEDS = (20260903, 20260904)
EPOCHS = 100
LR = 0.01
HIDDEN = 64
dev = torch.device("cuda")


class Sage(torch.nn.Module):
    def __init__(self, d_in, d_h):
        super().__init__()
        self.c1 = SAGEConv(d_in, d_h)
        self.c2 = SAGEConv(d_h, d_h)

    def forward(self, x, adj):
        return self.c2(torch.relu(self.c1(x, adj)), adj)


def fit(params, forward, y, masks, seed):
    """Full-batch Adam on the train mask; return test accuracy at the best val epoch."""
    torch.manual_seed(seed)
    opt = torch.optim.Adam(params, lr=LR)
    tr, va, te = masks
    best_val, test_at_best = -1.0, float("nan")
    for _ in range(EPOCHS):
        opt.zero_grad()
        out = forward()
        torch.nn.functional.cross_entropy(out[tr], y[tr]).backward()
        opt.step()
        with torch.no_grad():
            pred = forward().argmax(1)
            v = (pred[va] == y[va]).float().mean().item()
            if v > best_val:
                best_val, test_at_best = v, (pred[te] == y[te]).float().mean().item()
    return best_val, test_at_best


def main():
    data = np.load(ROOT / "pyg" / "raw" / "reddit_data.npz")
    x = torch.from_numpy(data["feature"]).to(torch.float32).to(dev)
    y = torch.from_numpy(data["label"]).to(torch.long).to(dev)
    split = torch.from_numpy(data["node_types"]).to(dev)
    masks = tuple(split == s for s in (1, 2, 3))
    n, d_in = x.shape
    n_cls = int(y.max()) + 1
    st = np.load(ROOT / "derived" / "reddit_stream.npz")
    print(
        f"nodes {n}, features {d_in}, classes {n_cls}, train/val/test "
        f"{[int(m.sum()) for m in masks]}, hidden {HIDDEN}, {EPOCHS} full-batch epochs, Adam lr {LR}"
    )
    print(f"{'edge set':<12} {'arm':<22} {'seed':>9} {'val acc':>8} {'test acc':>9} {'s':>6}")

    def row(name, arm, seed, res, t):
        print(f"{name:<12} {arm:<22} {seed:>9} {res[0]:>8.4f} {res[1]:>9.4f} {t:>6.0f}", flush=True)

    # features-only arms do not depend on the graph
    for seed in SEEDS:
        torch.manual_seed(seed)
        head = torch.nn.Linear(d_in, n_cls).to(dev)
        t = time.time()
        row(
            "(none)",
            "features linear",
            seed,
            fit(head.parameters(), lambda: head(x), y, masks, seed),
            time.time() - t,
        )
        torch.manual_seed(seed)
        mlp = torch.nn.Sequential(
            torch.nn.Linear(d_in, HIDDEN), torch.nn.ReLU(), torch.nn.Linear(HIDDEN, n_cls)
        ).to(dev)
        t = time.time()
        row(
            "(none)",
            "features mlp",
            seed,
            fit(mlp.parameters(), lambda: mlp(x), y, masks, seed),
            time.time() - t,
        )

    for tag, name in (("paper", "paper 11.6M"), ("full", "full 57.3M")):
        lo, hi = st[f"{tag}_lo"].astype(np.int64), st[f"{tag}_hi"].astype(np.int64)
        ei = torch.from_numpy(np.stack([np.r_[lo, hi], np.r_[hi, lo]])).to(dev)
        adj = to_torch_csr_tensor(ei, size=(n, n))
        del ei
        for seed in SEEDS:
            torch.manual_seed(seed)
            sage = Sage(d_in, HIDDEN).to(dev)
            head = torch.nn.Linear(HIDDEN, n_cls).to(dev)
            # untrained: the random initial weights, frozen; embed once, train the head
            with torch.no_grad():
                z = sage.eval()(x, adj)
            t = time.time()
            row(
                name,
                "untrained + head",
                seed,
                fit(head.parameters(), lambda: head(z), y, masks, seed),
                time.time() - t,
            )
            z = None
            torch.manual_seed(seed)
            sage = Sage(d_in, HIDDEN).to(dev).train()
            head = torch.nn.Linear(HIDDEN, n_cls).to(dev)
            params = list(sage.parameters()) + list(head.parameters())
            t = time.time()
            try:
                res = fit(params, lambda: head(sage(x, adj)), y, masks, seed)
                row(name, "trained end to end", seed, res, time.time() - t)
            except torch.cuda.OutOfMemoryError:
                print(f"{name:<12} {'trained end to end':<22} {seed:>9} {'OOM':>8}", flush=True)
                torch.cuda.empty_cache()
            sage = head = params = None
            torch.cuda.empty_cache()
        adj = None
        torch.cuda.empty_cache()


if __name__ == "__main__":
    sys.exit(main())

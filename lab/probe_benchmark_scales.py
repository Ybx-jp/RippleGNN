"""Adjudicate the dataset disagreement with a number.

eval-methodology ranks tgbl-wiki (9,227 nodes) as the primary dataset. dl says the
temporal-GNN benchmarks at that scale are three orders of magnitude below the cost floor
and would report scheduling noise. Both are reasoning about the same box; measure it.
"""
import time
import torch
from torch_geometric.nn import SAGEConv

d = torch.device("cuda")
DIM = 128

class SAGE(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.c1, self.c2 = SAGEConv(DIM, DIM), SAGEConv(DIM, 64)
    def forward(self, x, ei):
        return self.c2(self.c1(x, ei).relu(), ei)

m = SAGE().to(d).eval()
# (name, nodes, mean degree) — degrees are the published approximate values.
CASES = [
    ("Cora",            2_708,  4),
    ("CiteSeer",        3_327,  3),
    ("tgbl-wiki",       9_227, 10),
    ("Reddit-JODIE",   11_000, 10),
    ("PubMed",         19_717,  4),
    ("Reddit (full)",  232_965, 99),
    ("ogbn-products", 2_449_029, 50),
]
print(f"{'dataset':<16} {'nodes':>10} {'edges':>12} {'full recompute':>16} {'vs 1 frame @60Hz':>18}")
for name, n, deg in CASES:
    e = n * deg
    try:
        x = torch.randn(n, DIM, device=d)
        ei = torch.randint(0, n, (2, e), device=d)
        with torch.no_grad():
            m(x, ei); torch.cuda.synchronize()
            reps = 20 if n < 100_000 else 3
            t0 = time.perf_counter()
            for _ in range(reps):
                m(x, ei)
            torch.cuda.synchronize()
            secs = (time.perf_counter() - t0) / reps
        print(f"{name:<16} {n:>10,} {e:>12,} {secs*1000:>13.3f} ms {secs/(1/60):>17.4f}")
        del x, ei
        torch.cuda.empty_cache()
    except torch.cuda.OutOfMemoryError:
        print(f"{name:<16} {n:>10,} {e:>12,} {'OOM > 12 GiB':>16}")
        torch.cuda.empty_cache()

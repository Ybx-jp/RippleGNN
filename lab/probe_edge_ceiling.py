"""lab/001 said the ceiling was ~1-2M nodes. That was measured at degree 10, and it is
the wrong variable: full-graph message passing materializes a tensor per EDGE, so the
ceiling is an edge count. Find it, since it decides which datasets are admissible.
"""
import torch
from torch_geometric.nn import SAGEConv

d = torch.device("cuda")

def fits(n_edges, n_nodes=200_000, dim=128):
    torch.cuda.empty_cache(); torch.cuda.reset_peak_memory_stats()
    try:
        x = torch.randn(n_nodes, dim, device=d)
        ei = torch.randint(0, n_nodes, (2, n_edges), device=d)
        m = SAGEConv(dim, dim).to(d)
        with torch.no_grad():
            m(x, ei)
        torch.cuda.synchronize()
        peak = torch.cuda.max_memory_allocated() / 2**30
        del x, ei, m
        return True, peak
    except torch.cuda.OutOfMemoryError:
        torch.cuda.empty_cache()
        return False, None

print("one SAGEConv layer, 128-dim, 200k nodes, varying edge count\n")
print(f"{'edges':>13} {'fits':>6} {'peak GiB':>9}")
lo, hi = 0, 0
for e in (5_000_000, 10_000_000, 15_000_000, 20_000_000, 25_000_000, 40_000_000):
    ok, peak = fits(e)
    print(f"{e:>13,} {str(ok):>6} {(f'{peak:.2f}' if ok else '-'):>9}")
    if ok:
        lo = e
    elif hi == 0:
        hi = e

print(f"\nceiling is between {lo:,} and {hi:,} edges for a single layer at 128-dim.")
print("\nAdmissibility of the datasets the two experts proposed:")
for name, n, deg in [("tgbl-wiki", 9_227, 10), ("tgbl-review", 352_637, 2),
                     ("Reddit (full)", 232_965, 99), ("ogbn-products", 2_449_029, 50),
                     ("ogbn-arxiv", 169_343, 7), ("ogbn-papers100M", 111_059_956, 15)]:
    e = n * deg
    verdict = "fits" if e <= lo else ("marginal" if e < hi else "exceeds ceiling")
    print(f"  {name:<16} {n:>12,} nodes  {e:>13,} edges  -> {verdict}")

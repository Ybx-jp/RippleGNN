"""Is neighborhood sampling really the binding constraint on 4 cores, and at what
graph scale does a full-graph refresh stop fitting the sub-hour budget?"""
import time, os
import torch
from torch_geometric.data import Data
from torch_geometric.loader import NeighborLoader
from torch_geometric.nn import SAGEConv

torch.manual_seed(20260827)
print(f"cores={os.cpu_count()}  torch_threads={torch.get_num_threads()}")

class SAGE(torch.nn.Module):
    def __init__(self, i, h, o):
        super().__init__()
        self.c1, self.c2 = SAGEConv(i, h), SAGEConv(h, o)
    def forward(self, x, ei):
        return self.c2(self.c1(x, ei).relu(), ei)

print(f"\n{'nodes':>9} {'edges':>10} {'full-graph GPU (s)':>19} {'sampled 1 epoch (s)':>20} {'ratio':>7}")
for n, deg in ((10_000, 10), (50_000, 10), (200_000, 10)):
    e = n * deg
    ei = torch.randint(0, n, (2, e))
    x = torch.randn(n, 64)
    data = Data(x=x, edge_index=ei)
    model = SAGE(64, 64, 32)

    # Full-graph inference on GPU, synchronized.
    d = torch.device("cuda")
    m, xg, eig = model.to(d), x.to(d), ei.to(d)
    with torch.no_grad():
        m(xg, eig); torch.cuda.synchronize()
        t0 = time.perf_counter(); m(xg, eig); torch.cuda.synchronize()
        full = time.perf_counter() - t0

    # Mini-batch neighbor sampling: the CPU-side path.
    loader = NeighborLoader(data, num_neighbors=[10, 10], batch_size=512,
                            input_nodes=torch.arange(min(n, 20_000)), num_workers=0)
    t0 = time.perf_counter()
    nb = 0
    for batch in loader:
        nb += 1
        if time.perf_counter() - t0 > 20:  # cap the probe
            break
    elapsed = time.perf_counter() - t0
    per_epoch = elapsed / nb * (min(n, 20_000) / 512)
    print(f"{n:>9,} {e:>10,} {full:>19.4f} {per_epoch:>20.2f} {per_epoch/full:>7.0f}x")

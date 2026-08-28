"""Where does full recomputation stop being cheap on this box?

The manifest's premise is that recomputing every embedding after every change is
expensive enough to be worth avoiding. That premise is a measurable claim, and if it
does not bite until some scale, that scale is where the research question lives.
"""
import time, gc
import torch
from torch_geometric.nn import SAGEConv

d = torch.device("cuda")
DIM, DEG = 128, 10

class SAGE(torch.nn.Module):
    def __init__(self, i, h, o, layers=2):
        super().__init__()
        dims = [i] + [h] * (layers - 1) + [o]
        self.convs = torch.nn.ModuleList(SAGEConv(a, b) for a, b in zip(dims, dims[1:]))
    def forward(self, x, ei):
        for i, c in enumerate(self.convs):
            x = c(x, ei)
            if i + 1 < len(self.convs):
                x = x.relu()
        return x

print(f"{'nodes':>11} {'edges':>12} {'feat GiB':>9} {'full recompute':>15} {'peak VRAM GiB':>14}")
for n in (200_000, 1_000_000, 4_000_000, 10_000_000):
    gc.collect(); torch.cuda.empty_cache(); torch.cuda.reset_peak_memory_stats()
    try:
        x = torch.randn(n, DIM, device=d)
        ei = torch.randint(0, n, (2, n * DEG), device=d)
        m = SAGE(DIM, DIM, 64).to(d)
        with torch.no_grad():
            m(x, ei); torch.cuda.synchronize()
            t0 = time.perf_counter(); m(x, ei); torch.cuda.synchronize()
            secs = time.perf_counter() - t0
        print(f"{n:>11,} {n*DEG:>12,} {n*DIM*4/2**30:>9.2f} {secs:>14.3f}s "
              f"{torch.cuda.max_memory_allocated()/2**30:>13.2f}")
        del x, ei, m
    except torch.cuda.OutOfMemoryError:
        print(f"{n:>11,} {n*DEG:>12,} {n*DIM*4/2**30:>9.2f} {'OOM — exceeds 12 GiB':>15}")
        break

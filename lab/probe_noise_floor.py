"""L1: the seed-variance floor. Two recomputations of an UNCHANGED graph, same weights.

Any refresh-fidelity number is meaningless above this floor. The floor is not one
number: it depends on whether inference is full-graph (deterministic) or minibatch
neighbor-sampled (samples with replacement, so it is not).
"""
import torch
from torch_geometric.data import Data
from torch_geometric.loader import NeighborLoader
from torch_geometric.nn import SAGEConv

N, DEG, DIM, K = 50_000, 10, 64, 20
d = torch.device("cuda")
g = torch.Generator().manual_seed(20260827)
x = torch.randn(N, DIM, generator=g)
ei = torch.randint(0, N, (2, N * DEG), generator=g)
data = Data(x=x, edge_index=ei)

class SAGE(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.c1, self.c2 = SAGEConv(DIM, 64), SAGEConv(64, 32)
    def forward(self, x, ei):
        return self.c2(self.c1(x, ei).relu(), ei)

torch.manual_seed(20260827)
model = SAGE().to(d).eval()

def full_graph():
    with torch.no_grad():
        return model(x.to(d), ei.to(d))

def sampled(seed):
    torch.manual_seed(seed)
    out = torch.zeros(N, 32, device=d)
    loader = NeighborLoader(data, num_neighbors=[10, 10], batch_size=1024,
                            input_nodes=torch.arange(N), shuffle=False)
    with torch.no_grad():
        for b in loader:
            b = b.to(d)
            out[b.n_id[: b.batch_size]] = model(b.x, b.edge_index)[: b.batch_size]
    return out

def compare(a, b, label):
    an, bn = (torch.nn.functional.normalize(t, dim=1) for t in (a, b))
    cos = (an * bn).sum(1)
    # kNN overlap on a sample of query nodes, exact search.
    q = torch.arange(0, N, 25)
    ka = (an[q] @ an.T).topk(K + 1, dim=1).indices[:, 1:]
    kb = (bn[q] @ bn.T).topk(K + 1, dim=1).indices[:, 1:]
    ov = torch.tensor([len(set(r1.tolist()) & set(r2.tolist())) / K for r1, r2 in zip(ka, kb)])
    print(f"{label:<34} cos mean {cos.mean():.6f}  min {cos.min():.6f}  "
          f"| kNN@{K} overlap mean {ov.mean():.4f}  min {ov.min():.4f}")

print(f"N={N:,} edges={N*DEG:,} dim={DIM} K={K}\n")
compare(full_graph(), full_graph(), "full-graph vs full-graph")
compare(sampled(1), sampled(2), "sampled(seed1) vs sampled(seed2)")
compare(full_graph(), sampled(1), "full-graph vs sampled")

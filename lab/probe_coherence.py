"""lab/007 — does the degree invariance in lab/005 survive incoherent staleness?

lab/005 perturbed every stale neighbour by the same vector. Under mean aggregation the
centre's aggregated input then moves by exactly f times that vector at every degree, so
the flat result is an identity of the design. This probe repeats the star-graph sweep
with two arms: coherent (one vector shared by every stale neighbour) and incoherent (an
independent random vector of the same norm per stale neighbour), for mean and sum
aggregation. Untrained weights, eval mode, one layer, 16-dim, as in lab/005.
"""

import math

import torch
from torch_geometric.nn import SAGEConv

SEED = 20260903
DIM = 16
DEGREES = (20, 100, 500, 2000)
FRACTIONS = (0.05, 0.25, 0.50)
NORM = 0.1
DRAWS = 20


def star(deg):
    src = torch.arange(1, deg + 1)
    dst = torch.zeros(deg, dtype=torch.long)
    return torch.stack([src, dst])


def centre_error(conv, x, edge_index, delta):
    with torch.no_grad():
        clean = conv(x, edge_index)[0]
        dirty = conv(x + delta, edge_index)[0]
    return (dirty - clean).norm().item()


def main():
    gen = torch.Generator().manual_seed(SEED)
    torch.manual_seed(SEED)
    convs = {aggr: SAGEConv(DIM, DIM, aggr=aggr).eval() for aggr in ("mean", "sum")}
    shared = torch.randn(DIM, generator=gen)
    shared = shared / shared.norm() * NORM
    print(f"seed {SEED}, dim {DIM}, perturbation norm {NORM}, {DRAWS} incoherent draws")
    print("aggr  deg    f   coherent   incoherent(mean)  pred sqrt(f/d) ratio")
    for aggr, conv in convs.items():
        for deg in DEGREES:
            ei = star(deg)
            x = torch.randn(deg + 1, DIM, generator=gen)
            for f in FRACTIONS:
                k = int(round(f * deg))
                stale = torch.randperm(deg, generator=gen)[:k] + 1
                delta = torch.zeros_like(x)
                delta[stale] = shared
                coh = centre_error(conv, x, ei, delta)
                inc = []
                for _ in range(DRAWS):
                    d = torch.randn(k, DIM, generator=gen)
                    d = d / d.norm(dim=1, keepdim=True) * NORM
                    delta = torch.zeros_like(x)
                    delta[stale] = d
                    inc.append(centre_error(conv, x, ei, delta))
                inc = sum(inc) / len(inc)
                print(
                    f"{aggr:4s} {deg:5d} {f:5.2f}  {coh:.6f}   {inc:.6f}          "
                    f"{inc / coh:.4f}  (sqrt(1/k)={1 / math.sqrt(k):.4f})"
                )


if __name__ == "__main__":
    main()

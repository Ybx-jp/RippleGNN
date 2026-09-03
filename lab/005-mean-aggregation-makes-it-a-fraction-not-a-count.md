# 005 — Mean aggregation makes staleness a fraction, not a count

**Date:** 2026-08-27 · **Component:** refresh error model · **Status:** measured.

> **Corrected in part by lab/007.** The fixed-fraction invariance below is exact because
> the same perturbation vector was applied to every stale neighbour, which makes the mean
> move by the fraction times that vector at any degree by arithmetic. With an independent
> direction per stale neighbour, mean-aggregation error at fixed fraction falls with
> degree as the inverse square root. The contrast with sum aggregation stands; the flat
> line is the coherent special case.

## What was asked

The hand-fed GNNAutoScale span (Section 3, Lemma 1 through Theorem 2, ingested at 100%
anchoring) recovered the L-layer bound that had been mangled in every prior retrieval:

    ‖h̃_v^(L) − h_v^(L)‖ ≤ Σ_{ℓ=1}^{L−1} ε^(ℓ) · k₁^(L−ℓ) · k₂^(L−ℓ) · |N(v)|^(L−ℓ)

The span carries a remark that the |N(v)| factor comes from **sum** aggregation, and that
mean or max admits a much tighter bound. Since the degree factor is what drives the
heavy-tail story in `dl`'s round-2 ranking — R1 measures invalidation-set *size*, and
prediction (a) at 78% says k-hop refresh degenerates on heavy-tailed graphs — the
aggregator matters before anything is pre-registered. GraphSAGE's canonical aggregator is
mean, and `SAGEConv`'s default in PyG is mean.

## Observation

`SAGEConv.__init__` default `aggr='mean'`, instantiating `MeanAggregation()`. A star graph,
one centre with `deg` neighbours, 16-dim, one layer, `eval()` mode. A fixed perturbation of
0.1 is applied to a set of neighbour inputs and the centre's output error is measured.

One stale neighbour, varying degree:

| degree | mean-aggr error | sum-aggr error |
|---|---|---|
| 5 | 0.037569 | 0.187844 |
| 20 | 0.009392 | 0.187845 |
| 100 | 0.001878 | 0.187846 |
| 500 | 0.000376 | 0.187850 |

Holding the stale *fraction* fixed instead, mean aggregation:

| degree | f=5% | f=25% | f=50% |
|---|---|---|---|
| 20 | 0.009392 | 0.046961 | 0.093922 |
| 100 | 0.009392 | 0.046961 | 0.093922 |
| 500 | 0.009392 | 0.046961 | 0.093922 |
| 2000 | 0.009392 | 0.046961 | 0.093922 |

Sum aggregation over the same fractions scales linearly with degree (0.187845 at degree 20,
f=5%, up to 46.961109 at degree 500, f=50%).

Under mean aggregation the error is **exactly degree-invariant at fixed stale fraction**,
to six significant figures across two orders of magnitude of degree.

## Interpretation

**The |N(v)| factor is an aggregator artifact, not a property of message passing.** For a
mean-aggregating GNN the degree term drops out of the Theorem 2 bound, leaving a
degree-free geometric series in the Lipschitz constants. The paper says as much in the
remark; this measures it.

**R1 is measuring the wrong quantity for the model actually in use.** The invalidation-set
*size* distribution is the right object for a sum aggregator. For mean aggregation the
governing quantity is the invalidation set as a *fraction of the neighbourhood*, and a
count-based R1 would rank a hub as maximally endangered when it is in fact the most robust
node per stale neighbour.

**Prediction (a) is threatened, though not refuted.** "k-hop refresh degenerates at k≥2 on
heavy-tailed graphs", held at 78%, rests on hubs being fragile. Per stale neighbour they
are the opposite: a hub dilutes each stale contribution by 1/deg. Whether heavy tails hurt
now reduces to whether hub neighbourhoods acquire a higher stale *fraction* than low-degree
nodes do — an empirical question about mutation locality, not a consequence of the degree
distribution itself. That is a better question and it is not the one R1 currently asks.

**It also makes the project's target claim cleaner, if it survives.** If error is governed
by stale fraction, a refresh policy that bounds the fraction gives a degree-independent
error guarantee. That is a stronger and more portable result than a degree-dependent one.

## Threats

- One layer, one perturbation magnitude, applied uniformly to every stale neighbour. The
  compounding across L layers is not measured here, and Theorem 2's geometric factor in
  the remaining depth is exactly what compounding does.
- GraphSAGE concatenates a root-weight self path, which is unaffected by neighbour
  staleness and therefore dilutes measured error further in a way this star graph
  understates for real graphs.
- A star graph has no structure. Real neighbourhoods are correlated, and stale neighbours
  are unlikely to be a uniform random subset — refresh policies will make them highly
  non-uniform by design, which is the whole point of prioritization.
- Untrained weights again. The Lipschitz constants of a trained model are what the bound
  is stated over.

The mechanism — mean aggregation weights each neighbour by 1/deg — is exact and structural,
so the direction is safe. The magnitudes are not load-bearing.

## Open

This was found after both round-2 rankings closed, and it bears on `dl`'s R1 and R2 and on
prediction (a). It has not been put back to that scope. Whether to spend a round 3 on it is
the operator's call.

Raw probe: reproduced inline in this note's tables; the two scripts are short enough that
the note carries them in full above.

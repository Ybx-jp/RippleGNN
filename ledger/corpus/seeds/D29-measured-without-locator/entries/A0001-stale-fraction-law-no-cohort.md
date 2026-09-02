---
id: A0001-stale-fraction-law-no-cohort
kind: claim
stated: 2026-09-02T08:00:00-07:00
author: main
grade: measured
supersedes: none
verbatim_sha: 4cadf84b96a8c10133aaa89f85641fd62288f9654037228fe44efc66be39f79c
---

## Assertion

Under mean aggregation, per-neighbour staleness error at a node is governed by the stale
fraction of its neighbourhood, not the stale count; at fixed fraction it is degree-
invariant.

## Scope

metric: centre-node output L2 error under fixed-magnitude neighbour perturbation
condition: single layer; uniform perturbation 0.1; stale set uniform-random

## Grounds

- lab: ledger/corpus/fixtures/lab-005.md § "Observation" @corpus

## Warrant

Mean aggregation weights each neighbour by 1/deg, so a fixed perturbation on a fraction
f of neighbours contributes f times the per-neighbour effect regardless of degree. The
sweep confirms the mechanism to three decimals, so the direction is structural.

## Backing

- source: fx-paper-a · §1
  speaker: fixture paper A authors
  quote: "Under mean aggregation the per-neighbour contribution is scaled by 1/deg, so the error induced by a stale fraction f of the neighbourhood is proportional to f and does not grow with degree."

<!-- APPEND BELOW THIS LINE ONLY -->

## Verdicts


## References


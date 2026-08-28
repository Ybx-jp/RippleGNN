# 003 — What round one cost, and what it bought

**Date:** 2026-08-27 · **Component:** research method · **Status:** measured.

## What was asked

Two independent round-1 grounding consultations before any dataset was chosen: `dl` on
the modelling side (ticket modelling consultation, round 1), `eval-methodology` on measurement
(measurement consultation, round 1). Deliberately not shown each other's reasoning.

## Observation

| | dl | eval-methodology |
|---|---|---|
| answer length | 34,144 chars | 44,419 chars |
| validated citations | 34 | 63 |
| documents requested | 6 gaps | 16 papers |

Both scopes disclosed near-total absence of coverage at this surface rather than
producing a literature review from parametric memory. `dl` reported a query returning
literally no matching memories; `eval-methodology` ran four queries at the
embedding-geometry surface and got LLM-as-judge and mutation-testing material back every
time, then labelled its answer "not found in this scope's corpus" instead of ruling.

Procurement that followed: 31 documents, 17 to `dl` (feed `ripple-refresh`), 14 to
`eval-methodology` (feed `ripple-measurement`). Contract check clean, 51,403 vertices /
175,866 edges audited. Roughly $23 of extraction. Five documents anchored between 65% and
80% from equation mangling; no document truncated (digest budget 240,000 chars, largest
document 131,048). Seven items unresolved: paywalled, OpenReview-403, or on hosts not on
the relevant scope's allowlist.

Changes made to the repo before any study exists, all traceable to a round-1 finding:
non-inferiority margin and its derivation required; four estimands replacing one axis;
no-refresh promoted from baseline to falsifier arm; destructive positive control required
for any "local approximates full" comparison; chance-correction against a k>=5
unchanged-graph null; unit of analysis moved from node to mutation episode;
`environment.json` added to the reproducibility triple; `run.py` required to be the
analysis path rather than merely to compute its numbers; preregistration timestamped by
push rather than by local commit date.

## Interpretation

Three things this bought that a general-purpose second opinion would not have.

**Two independent corrections that invalidate obvious experiment designs.** `dl`: exact
k-hop refresh equals global recomputation definitionally, so the manifest's locality
question has no empirical content as posed and the object is the k-hop reverse-reachable
set's size distribution. `eval-methodology`: no-refresh scores perfectly on any pure
stability metric because doing nothing is maximally self-consistent, so it is the
falsifier arm for every probe and any metric it wins is degenerate. The second is
definitionally true once stated and would have been found only after running the
experiment.

**Convergence from two directions on the same threat.** `dl` predicted from NBFNet's
published wall-clock that the baseline might already be cheap enough that there is no
problem to study. lab/001 measured the same thing on this box from the other end. Neither
was told about the other. Agreement between a literature prediction and a local
measurement is worth more than either alone, and it is what makes the dataset-scale
constraint load-bearing rather than a preference.

**A gap disclosed is worth more than an answer confabulated.** Both scopes could have
produced a fluent literature review from parametric memory and it would have read as
authoritative. What they produced instead was a procurement list, which is checkable, and
which turned into 31 documents the next round can actually cite. The cost of that honesty
was one extra round and $23.

## Cost accounting

Round 1 plus procurement: two consultations, one ingest batch, ~$23 extraction, roughly
95 minutes wall-clock including the ingest. Against that, the experiment contract was
rewritten before a single experiment existed, and two experiment designs that would have
produced publishable-looking nonsense were ruled out in advance.

Whether that trade is good is not yet decided by this note. It is decided by whether
round 2's ranking survives contact with the first experiment, and that is unrun.

## Open

- Three unresolved items (Launch and Iterate, RBO, Schonemann) plus the IVM classics and
  DyRep are blocked by host allowlists rather than by not existing. That is an operator
  decision, not a research one, and it is unmade.
- Five weakly-anchored documents need hand-fed sections if their equations become
  load-bearing. GNNAutoScale's Lemma 1 is the one that matters, since it is the paper that
  might already answer the manifest's core question.

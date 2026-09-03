# 006 — Poursafaei et al., read: the threat is to the downstream arm, and it is the saturation objection a second time

**Date:** 2026-09-02 · **Component:** evaluation design · **Status:** measured.

## What was asked

The modelling consultation's second round named Poursafaei, Huang, Pelrine and Rabbany
(2022), *Towards Better Evaluation for Dynamic Link Prediction*, as a threat to the
evaluation design, conditionally: if the evaluation ends up resting on dynamic link
prediction, get the paper before writing the eval script. It also said none of its top
three experiments needed a link-prediction metric, and it had not retrieved the paper
itself. The paper sat unread on the project's list of blockers for the next
preregistration. This note is the reading. Its figures are the authors' own, from the
arXiv v2 text; nothing was rerun.

## Observation

The paper is about evaluating dynamic link prediction on continuous-time interaction
streams: the Wikipedia and Reddit editor–page and user–subreddit graphs of Kumar, Zhang
and Leskovec, MOOC, LastFM, Enron, Social Evo., UCI, and six datasets the authors add.
A test edge is scored against a sampled negative, and the paper's subject is where that
negative comes from.

Three findings.

**Random negatives are saturated, and a method that learns nothing scores near the
ceiling.** The standard protocol keeps a positive edge's source and timestamp and draws
the destination uniformly from all nodes. The authors add EdgeBank, a baseline that
stores every edge it has seen and answers yes to a pair if it is in the store. AU-ROC
under random negatives, Table 3:

| dataset | TGN | CAWN | EdgeBank, all history | EdgeBank, recent window |
|---|---|---|---|---|
| Wikipedia | 0.98 | 0.99 | 0.91 | 0.87 |
| Reddit | 0.99 | 0.99 | 0.95 | 0.91 |

The authors' explanation is that a random node pair is almost never a previously seen
edge, so answering from the edge list is rarely wrong on a negative
(A0008-random-negatives-leave-dynamic-link-prediction-near-ceiling, cites-as-live).

**Historical negatives remove the floor and lower everything.** The authors propose
drawing negatives at each step from edges that were present in the training stream and
are absent at that step, and a second variant from edges first seen at test time. AU-ROC
under historical negatives, Table 6, same rows:

| dataset | TGN | CAWN | EdgeBank, all history | EdgeBank, recent window |
|---|---|---|---|---|
| Wikipedia | 0.84 | 0.84 | 0.49 | 0.77 |
| Reddit | 0.81 | 0.85 | 0.51 | 0.77 |

Across all thirteen datasets the average drop for the learned models is at least ten
points, and the ranking of methods changes between protocols
(A0009-historical-negatives-give-dynamic-link-prediction-headroom, cites-as-live). The
window-limited EdgeBank stays competitive under historical negatives and wins outright
on five datasets, which the authors read as recent edges carrying most of the signal.

**The datasets are small.** The largest of the thirteen by total interactions is Contact
at 2.4M, and by distinct edges Flights at 395k; Reddit has 672k interactions over 78.5k
distinct edges. Every one of them is at least an order of magnitude below the admissible
band lab/004 measured, and the two interaction graphs the project had been discussing
are three orders below it.

## Interpretation

**The threat is real, conditional, and lands on one estimand.** Self-consistency and
rank survival involve no negatives; the protocol problem only reaches the downstream
task estimand, and only if that task is link prediction. The modelling consultation's
condition was the right one.

**Where it lands, it is the saturation objection again on a different graph family.**
The measurement consultation objected that the node-classification tasks on the Reddit
post graph and its relatives score near ceiling, so there is no headroom for a refresh
effect. Poursafaei et al. show the same thing for link prediction on the interaction
graphs under the standard protocol: a stale embedding would score within a few points of
a fresh one because the negatives are separable from the edge list alone. The margin
the experiments README requires is a fraction of the full-recompute-to-no-refresh gap on
the same probe, and on either family, under the standard task, that gap is at most the
few points between a do-nothing baseline and the ceiling. That is the second time the
denominator has come up near zero on a candidate dataset, and for the same reason.

**The constructive part is that headroom exists and it is in the right place.** Under
historical negatives the best model is fifteen to twenty points below the ceiling and
the floor is chance, and the question the task poses, whether a known edge recurs at
this step, is the question a refresh policy is supposed to keep an embedding able to
answer. If a downstream task arm survives at all, it is link prediction with historical
negatives, and EdgeBank belongs beside no-refresh as a baseline: it is the reference for
what needs no embedding, and a refresh policy that cannot beat it is not preserving
anything worth the cost.

**The protocol presupposes a mutation stream with absences.** A historical negative is an
edge that was present and is not. On an insert-only stream, the accumulation of a post
graph as it grows, there are none, and inductive negatives need the same thing at test
time. So the headroom this paper finds is available only on a stream in which edges
recur intermittently, which lab/004 already left as a separate, unmeasured axis. The
dataset question has not been answered by the reading; it has been sharpened to three
axes that have to hold at once: in the band, with an unsaturated task, on a stream where
edges are absent as well as present.

## Open

- Whether the downstream task arm survives, or the fidelity probes carry the result and
  the task is decoration, is the fork lab/004 left, and it is now the question for the
  measurement consultation's next round with this paper in front of it.
- Whether any candidate graph in the band has a mutation stream with absences. The
  interaction graphs do and are far below the band; the post graph is in the band at
  64-dim and its stream has not been characterized.
- Whether EdgeBank joins the baseline set. It is not in the manifest's list, and adding a
  baseline is an evaluation-methodology change to be recorded as one.
- The modelling consultation has not seen this paper; its redesign of the ranking
  experiment should.

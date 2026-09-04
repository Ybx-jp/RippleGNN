# 010 — The label signal is not in the features: the untrained-weights control on Reddit at 64

**Date:** 2026-09-03 · **Component:** experiment design, controls · **Status:** measured.

## What was asked

lab/008's second probe. The measurement consultation's third-round ruling took task
quality off the Reddit post graph on the argument that a 97.0 F1 with a small
generalization gap says the label signal is largely in the 602 features, and that the
untrained-weights control would show it in seconds. This note is that control, on both
edge sets lab/009 found, with a features-only arm beside it. Script:
`lab/probe_reddit_untrained.py`, reading the edge sets `lab/probe_reddit_stream.py`
writes.

## Observation

Full-batch on the CSR path, two-layer GraphSAGE 602 → 64 → 64 with a linear head to
41 classes, Adam at 0.01 for 100 epochs, test accuracy at the best validation epoch
(micro-F1 equals accuracy on a single-label task), seeds 20260903 and 20260904:

| edge set | arm | seed | val | test | s |
|---|---|---|---|---|---|
| none | features, linear head | 20260903 | 0.6833 | 0.6782 | 2 |
| none | features, 602 → 64 → 41 MLP | 20260903 | 0.6939 | 0.6887 | 2 |
| none | features, linear head | 20260904 | 0.6834 | 0.6791 | 1 |
| none | features, 602 → 64 → 41 MLP | 20260904 | 0.6961 | 0.6907 | 2 |
| paper 11.6M | untrained GraphSAGE, trained head | 20260903 | 0.5367 | 0.5303 | 1 |
| paper 11.6M | trained end to end | 20260903 | 0.9558 | 0.9558 | 53 |
| paper 11.6M | untrained GraphSAGE, trained head | 20260904 | 0.5521 | 0.5451 | 1 |
| paper 11.6M | trained end to end | 20260904 | 0.9561 | 0.9543 | 53 |
| full 57.3M | untrained GraphSAGE, trained head | 20260903 | 0.5429 | 0.5371 | 1 |
| full 57.3M | trained end to end | 20260903 | OOM | – | – |
| full 57.3M | untrained GraphSAGE, trained head | 20260904 | 0.5578 | 0.5503 | 1 |
| full 57.3M | trained end to end | 20260904 | 0.9587 | 0.9564 | 229 |

The untrained arm freezes the random initial weights, embeds once, and trains only the
head on the 64-dim output. The out-of-memory on the full graph's first trained run
occurred with the untrained arm's tensors just released on the same device and did not
recur on the second seed, which ran at 229 s; it is an allocator state, not a ceiling.
Validation and test accuracy agree to within 0.2 points on every row.

## Interpretation

**The premise of the ruling does not hold.** Features alone reach 68 to 69 percent;
the trained model reaches 95.4 to 95.6 on either edge set, 27 points above them, and
the untrained-weights control sits at 53 to 55, below features alone, because a random
64-dim projection of a 602-dim input discards signal that the linear head on the raw
features keeps. The label signal is in the graph and the training, not in the
features. An untrained GNN cannot look faithful on this task by preserving feature
smoothing, which is the failure the control exists to catch, so on Reddit the control
is informative rather than a formality.

**What the small gap does say.** Validation equals test on every row, and the test
posts are the last ten days against the first twenty, so the temporal split carries no
distribution shift the task can see. That is the saturation objection in its
defensible form, headroom, and it is untouched here: whether a refresh effect can show
in task quality depends on whether staleness moves a 95.5 percent model, and nothing in
this note measures staleness. What the note removes is the argument that the score
would survive the loss of the learned signal, which it would not.

**The ruling is for the measurement consultation to revisit** with these numbers, not
for this note to reverse. The design keeps behavioural consistency as the downstream
arm and the untrained-weights control on every headline run; whether task quality on
Reddit returns as an estimand is the consultation's question, now that the ground it
was removed on has been measured and found otherwise.

## Open

- Whether task quality on Reddit returns to the design; a question for the
  measurement consultation with this table.
- The trained number at 64 is 95.5 on both edge sets from two seeds and one; the
  pinned checkpoint will need its own seed set and the recorded environment.
- The remaining probes in lab/008's list, from the seed-churn pilot on.

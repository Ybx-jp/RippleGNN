# 008 — What round three settled: the task arm, the dataset, the stream, and what to run before the preregistration

**Date:** 2026-09-02 · **Component:** experiment design · **Status:** measured.

## What was asked

Two third-round consultations were run independently on the same evening, each given
the operator's decisions and the project's own measurements and nothing of the other's
reasoning. The operator had decided for a synthetic, parameterised edit stream over a
large static graph in the admissible band, with the Reddit post graph at 64-dim as the
candidate, and had left to the measurement consultation whether a downstream-task arm
survives. The modelling consultation was asked what lab/005 does to its ranking, and it
answered first with the correction that became lab/007. This note records the rulings
as data, and the design as it stands after them.

## Observation

**From the modelling consultation.** The invalidation-set size is a cost-of-exactness
quantity and is untouched by the aggregator; the prediction that exact k-hop refresh
degenerates to global recomputation on heavy-tailed graphs stands at 78 percent as a
cost statement, with its significance reduced, because under mean aggregation the set
of nodes whose error exceeds a tolerance is predicted to be a small fraction of the
exact set. New prediction on the record: on Reddit at 64-dim under a uniform-random edge
stream, that tolerance-invalidation set at ten times the deterministic-inference noise
floor will be below five percent of the exact two-hop set, median over mutations, at 70
percent. The 60 percent prediction that realised error sits an order of magnitude below
the Lemma 1 bound was withdrawn as trivially true against the sum form, and replaced:
against a fraction-aware mean-aggregation bound with slope estimated from the
checkpoint, realised error under coherent staleness will lie within a factor of ten of
the bound, at 65 percent. The argument that sub-k refresh is lossy on expander-like
graphs was withdrawn in its fidelity half and kept in its cost half. The influence-mass
part of the combinatorics experiment was already the mean-aggregation form; the
experiment is redesigned to report the stale-fraction distribution across degree
deciles per stream model, the influence mass, and a predicted per-node fidelity curve,
with the exact set kept as a reference column, at the same cost. The credence on the
roster hypothesis as it then stood was 0.35; on its restatement as non-increasing under
mean and increasing under sum, about 0.75. Ruling: one preregistration with two arms,
the combinatorics first inside it and the restated hypothesis as the first cell of the
fidelity sweep, on the uniform and the hot-hub streams, with the sum and
untrained-weight controls and deterministic inference. Stream models ranked by how much
they can hurt the target claim: a hot-hub bursty stream first, and the one the design
must include, since it is the only model under which the most-consumed nodes are also
the most endangered and the staleness is coherent; uniform-random edges as the null;
endpoint-uniform as the flattering lower envelope; preferential-attachment insertions
as a drift confound; community shift as a coherence dial. The pushback on the synthetic
decision was not for a real stream but for a calibrated one: measure the activity-vs-
degree exponent, the burst inter-event distribution and the novelty, reoccurrence and
surprise indices on the Reddit interaction graph, which is small enough to process for
free, and use them as the generator's parameters. A memoryless synthetic stream has zero
reoccurrence, so a memorization baseline under it measures the generator. Hand-feed
requested: the GNNAutoScale appendix proof of Lemma 1 and Section 2's Equation 1, to
settle whether the fraction-aware bound is theirs or the project's own lemma.

**From the measurement consultation.** Its round-2 primary is accepted as refuted on
cost. Its saturation objection was aimed at one estimand and kills only that one: the
downstream task splits into behavioural consistency and task quality, and saturation
kills task quality. Task quality does not survive on the Reddit post graph under any
split, because the 97.0 F1 with a small generalization gap says the label signal is
largely in the 602 features, which the untrained-weights control will show in seconds.
Historical-negative link prediction over synthetic deletions measures fidelity under a
task's name, not task quality: under memoryless deletions the task's ceiling is the
generator's entropy, and a memorization baseline scores at chance by construction, so
it is a manipulation check on the generator rather than a baseline. What survives is
behavioural consistency, the disagreement rate of a fixed head between the refreshed and
the fully recomputed space, stratified to the nodes a mutation touched because a
saturated task compresses disagreement too, with full-recompute-versus-full-recompute
churn across seeds as the denominator; the functional-usefulness criterion is then met
by a selection experiment, whether the fidelity probes choose the policy the head-based
oracle would have chosen, and at what worst-case error. The write-up loses the sentence
that a policy preserves task performance. Dataset ruling within the band: the Reddit
post graph at 64-dim is primary for the fidelity study, the one candidate where the
probes can fail for a reason about graphs rather than about the generator, with every
kNN figure stratified by degree band; ogbn-arxiv is the only candidate that keeps task
quality alive with a prescribed time split and 28 points of headroom, blocked on
whether sub-year timestamps exist for enough episodes; Yelp is unranked until its
paper is held; the Cluster SBM is an instrument check, never a fidelity number; Flickr
is below the band. The margin denominator is defensible only under an ordering: the
generator setting pinned to an external anchor before any gap is measured, the
denominator taken as the lower confidence limit of the gap across at least five seeds,
a pre-registered gap-floor eligibility rule with no-headroom cells reported and never
dropped, and a sweep over generator magnitude as sensitivity analysis reporting whether
the policy ranking survives. Pre-registration recovers the commitment a prescribed
protocol gave: generator parameters and seed, split points, negative protocol with a
collision check, the closed mutation grid, the stratification, the gap-floor rule, the
sweep, the seed budget, which the hand-fed variance decomposition puts at episodes over
seeds beyond the five the null needs. It cannot recover disinterest, external
comparability, which is partly recovered by running the reference model once on
ogbn-arxiv's prescribed split against the published table, or external validity to any
real evolution. Its pushback on the synthetic decision: defensible for deletions, and
if the Reddit post graph carries post timestamps the real arrival order should be the
insertion stream and anchor arm with the generator owning only deletions.

## Interpretation

**The two consultations converge on calibration from different sides.** One asks for
the generator's parameters to be measured on the Reddit interaction graph; the other
asks for the post graph's own arrival order if it exists, and for the generator to be
pinned to an external anchor before any gap is measured. The synthetic decision stands
and acquires a condition: the stream is declared, and its parameters are measured
somewhere real before the preregistration names them.

**The design as it stands.** One preregistration, two arms. Arm A is model-free
combinatorics over stream models on the Reddit post graph, with ogbn-arxiv as the
low-expansion control: stale-fraction distribution by degree decile, influence mass
under the lazy row-normalised walk with laziness from the checkpoint, the predicted
tolerance-invalidation set, and the exact set as a reference column. Arm B is the
restated roster hypothesis on the trained Reddit-at-64 checkpoint, uniform and hot-hub
streams, mean against sum, deterministic inference, untrained-weights control, on the
fidelity probes with every kNN figure stratified by degree band. The downstream arm is
behavioural consistency stratified to touched nodes, with seed churn as its
denominator, and the selection experiment. The margin follows the four-part ordering.
Task quality is not claimed on Reddit; whether it is claimed at all depends on
ogbn-arxiv's timestamps.

**Coherence is now a declared property of the stream.** lab/007 made it the second axis
the generator sets; the hot-hub model is the coherent, hub-concentrated corner and the
uniform model the incoherent, degree-neutral one. The two arms of the preregistration
run at both corners.

**What to run before the preregistration is written, in order, all under an hour on
the box.** Characterise the Reddit post graph's real stream: whether posts carry
timestamps in the pinned copy, the per-day insertion rate, the fraction of new edges
incident to top-decile nodes, the tail exponent. The untrained-weights control on
Reddit-at-64 against the trained number. Disagreement compression: full-recompute
churn across five seeds, overall and on touched nodes, on a pilot episode. The gap
pilot at three generator settings across five seeds on every candidate probe, beside
the no-op band. The memorization-baseline check on the generator's deletions. The
ogbn-arxiv episode count and its full recompute on the real graph. Mutation-induced
coherence on a 20k-node Reddit sample, the mean pairwise cosine between stale
neighbours' deltas per degree decile, under a hundred random deletions and under a
hot-hub burst. The spectral norms of the checkpoint's layer matrices, for the slope
and the laziness. The uniform-stream stale-fraction distribution on Reddit at one
percent, as the pilot that sets the margin.

**What to procure.** The GNNAutoScale appendix proof and Equation 1; the GraphSAGE
paper's Reddit section, for the post graph's construction and split; the GraphSAINT
paper for Yelp and Flickr; the benchmarking paper for the Cluster SBM's degree
distribution; the JODIE paper's construction and per-node activity statistics; the
ogbn-arxiv date fields; a temporal-network reference-model paper for a principled
calibrated generator; the two robustness papers on high-degree stability that the
curvature paper cites; the growth-model and burstiness papers a hot-hub generator would
rest on.

## Open

- Whether the Reddit post graph carries timestamps decides whether the insertion stream
  is real or generated. Nothing here is known about it beyond the published split.
- The operator's own credence on the restated hypothesis; the ledger carries the
  consulted expert's.
- Whether ogbn-arxiv joins as the task-quality dataset.
- The GNNAutoScale hand-feed, and whether the fraction-aware bound is attributable or
  is the project's lemma to prove in the preregistration.

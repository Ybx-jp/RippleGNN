# 018 — What round four settled: the real stream is primary, the slope is two numbers, the tolerance is restated, and the fixed-fraction hypothesis splits its condition

**Date:** 2026-09-05 · **Component:** experiment design · **Status:** measured.

## What was asked

Two fourth-round consultations were run on the same evening, each given the operator's
decisions and the project's own measurements (lab/007, lab/009–017, fed to each scope
that evening) and nothing of the other's reasoning. Both had asked in round three for
probes that were then run: the modelling consultation's five (the coherence rerun of
lab/005 as lab/007, mutation-induced coherence as lab/015, the checkpoint's norms as
lab/016, the sum control and the stale-fraction distribution as lab/017) and the
measurement consultation's five (the real stream as lab/009, the untrained-weights
control as lab/010, disagreement compression as lab/011, the gap pilot as lab/012–013,
the ogbn-arxiv clock as lab/014), with the memorization check held back because it
waits on whether synthetic deletions stay at all. What each had asked to be fed was
fed first: the modelling scope received GNNAutoScale's Section 2 and appendix proofs
(hand-fed from the HTML rendering), Kenlay, Thanou and Dong 2021, Leskovec, Kleinberg
and Faloutsos 2007, Barabási and Albert 1999, Holme and Saramäki 2012, Barabási 2005
and JODIE again; the measurement scope received the GraphSAGE paper, JODIE, Holme and
Saramäki and Milani Fard et al. 2016. Zügner and Günnemann 2020 has no open-access copy
and was not fed. This note records the rulings as data, and the design as it stands
after them.

## Observation

**From the modelling consultation.** The round-three synthetic-stream decision is
superseded by the evidence it was made without: the real growth stream is primary and
the anchor for both arms, uniform deletion and uniform insertion are the incoherent and
coherent brackets, and lab/013's hub constructions are the adversarial corner. The
JODIE calibration is withdrawn, since JODIE's Reddit is a bipartite user-to-subreddit
interaction stream carrying no per-node activity exponent and the growth stream's own
slope, tail and burstiness now exist; a generator's remaining roles are deletions, a
coherence dial, rates beyond the ten days the data has, and a hub-concentration sweep
toward arxiv's 72 percent, calibrated to lab/009's and lab/015's numbers and run beside
the real stream. The memorization check on synthetic deletions has no consumer under a
behavioural-consistency task arm and is dropped with that reason. The predicted curve
carries two slopes by name: the spectral product of the neighbour matrices, 10.2 to
12.4, as the bound, and the realised product as the prediction, with the second layer's
realised gain about 1.0 already measured and the first layer's measurable on touched
posts as the ratio of the post's first-layer delta to the move of its aggregated raw
features, bounded by the first neighbour matrix's norm because ReLU is 1-Lipschitz;
predicted at 0.3 to 0.7 of that norm at 65 percent. The laziness is not the
operator-norm root share; it is, per touched post, the norm of the root matrix applied
to the post's own first-layer delta over the norm of the neighbour matrix applied to
its aggregated-input move, predicted above 1 on every decile at 70 percent, and it
drops out of the two-hop-only stratum entirely. The tolerance prediction at ten times
the floor is withdrawn as decided by the floor; restated at consumer tolerances on a
fresh snapshot with pinned checkpoints: at one percent of the norm the share of the
exact two-hop set exceeding is 0.15 to 0.30 under one-percent deletion and 0.40 to
0.65 under one-percent insertion, at 75 percent; at ten percent below 0.01 and 0.12;
insertion above growth above deletion at matched edge count, 70 percent; one day of
the real stream at one percent in 0.35 to 0.80 of the graph, 55 percent. The
fixed-fraction hypothesis conflated which neighbours are stale with how their deltas
align: uniform insertion fixes the fraction at every degree and is coherent, uniform
deletion is incoherent and its fraction rises with degree through the neighbours'
degrees, so the condition splits into a uniform-random stale set at fraction f and a
coherence declared per stream, and the hypothesis reads non-increasing under mean by
two mechanisms, averaging under incoherent staleness and neighbour-degree protection
under coherent, and increasing under sum in absolute L2. Arm B's fixed-fraction cell is
defined on uniform insertion, the harder test, with deletion through fixed-fraction
bins and the real stream at matched arrived fraction. Under relative normalisation the
sum control is predicted to fall with degree too, top over bottom 0.3 to 0.7 under
deletion and 0.1 to 0.3 under insertion at 70 percent, so relative loses the positive
control; absolute rises with top over bottom above 3 at 85 percent. The round-three
prediction that the median stale fraction is flat at the rate was a definitional
mismatch on the median, withdrawn as a prediction about the note's quantity and
restated as the expectation over a post's neighbours of one minus the chance each kept
all its edges, rising with degree under deletion and flat under insertion, at 0.95;
the dispersion half survives. Coherence is a generator parameter, the share of
inserted partners from another community, with the measured cosine and R against
orthogonal by decile as the check the generator hit its anchor; Arm A's influence-mass
bound is declared as the coherent case with the incoherent prediction beside it, and
the top decile's R over orthogonal is predicted monotone in that share, at least 4 at
a share of one, 70 percent. Of the fed papers: Kenlay's bound is per perturbed edge in
the spectral norm of the normalised-Laplacian error, for symmetric normalisation and an
untrained filter on the touched node, so at a fixed fraction its leading term rises as
the root of the node's degree over its neighbours' minimum, and it corroborates
per-neighbour hub safety and nothing about the fixed-fraction direction; the growth
stream is the Barabási–Albert process to two digits, whose stationarity dissolves the
round-three drift objection; Leskovec's densification exponent is predicted to be 1
for a tail exponent above 2 and was not reported in lab/009; the burstiness papers
give a power-law inter-event law that cannot be measured without a wall-clock, so a
bursty arm is dropped or carried unanchored; GAS's Equation 1 places aggregation
between Message and Update and its proof names no norm and no stale-exact split, so the
fraction-aware bound is the project's own two-line lemma. Credence on the restated
hypothesis, absolute L2, fresh snapshot, pinned checkpoints: 0.93 non-increasing under
mean, 0.88 strictly falling below a half, 0.90 sum rising, 0.85 that sum falls under
relative, 0.95 that the mean-to-sum top-decile ratio is under 0.05, 0.80 on the real
stream at matched arrived fraction. Probes asked for: the first layer's realised gain
and the per-post laziness; densification and degree assortativity over the thirty
days; the real stream's coherence split by same- and cross-subreddit arrivals; the CSR
floor on the pinned snapshot; the sum control under relative normalisation on one
insertion arm. Still missing: Kenlay's Section VI looseness, Virmaux and Scaman 2018 on
realised-against-spectral Lipschitz gaps, Zügner 2020 as a citation gap only.

**From the measurement consultation.** Its round-three mechanism for killing task
quality on Reddit, that the label is in the features, is withdrawn against lab/010; the
ruling survives on a measured bound: an arm's accuracy can move by at most the share of
predictions it flips, which the pilot measured at 0.35 percent of existing posts after a
day and 0.2 percent of the top decile after ten days, inside the reference's own
seed-to-seed accuracy spread of 0.4 to 0.6 points, so task quality has no eligible cell
on Reddit at any horizon the stream affords and is written as a screen with a predicted
null and reported as the finding it is. On arxiv the seven-point shortfall against the
published GraphSAGE row is two questions: a reported condition for the fidelity and
behavioural arms, whose reference is the project's own checkpoint, with the recipe
pinned before the eligible cells are written because lab/014 measured that longer
training moves the eligible-cell map; and a required fix for a task-quality claim, whose
whole content is the reference's accuracy, by replicating the published architecture
(three layers, 256 wide, dropout 0.5) beside 71.49 ± 0.27 before the preregistration.
Whether task quality then has headroom on arxiv is unmeasured: 4.7 to 10.3 percent of
predictions flip in a year against a 1.3-point seed spread, but a flip on a 65-percent
model may be a correction. The episode on Reddit is two lengths, hour episodes primary
because the hour is the only length at which touched is a stratum at every degree, day
episodes secondary as the accumulated-staleness regime where the kNN gap is seven times
larger, with touched status and degree decile stratified jointly at both, since lab/011
shows within-decile churn equal and a day's untouched stratum is a degree-zero bin;
about thirty disjoint hours blocked by day and ten disjoint days, some eighty GPU
minutes, with the count declared a budget number until the across-episode spread of the
hour gap is measured. On arxiv fourteen year-episodes are a study for the paired primary
contrast under a rank-based, year-blocked analysis and not for moderator analyses, and
sub-year draws stay labelled constructions. The behavioural arm survives as constructed
and narrowed in domain: the eligible cells are the touched low-degree strata on both
graphs, the hub cells are registered as no-headroom cells and reported as the arm's
finding that a 95.5-percent head is insensitive to hub staleness; not a head chosen to
show a gap, which is the vicious circle with the head in the small sample's place and
which lab/014 shows raises its own band; not a longer episode, since the month has no
longer one; not a full yield to the neighbourhood probe, which carries the hub cells as
primary there but does not replace a decision-level estimand. The selection experiment
runs as designed on the eligible cells, with the eigenspace-instability theorem for a
linear head as its warrant, and inverts on the hubs into a one-sided check of whether a
probe ever chooses a policy the head would reject. The band: the mutated-graph band is
the eligibility denominator, the starting-graph band a second registered quantity, and
their ratio a preregistered outcome named reference instability under the mutation,
because a band that rises with the treatment measures the reference and not the
instrument, and a hub cell made eligible by the starting-graph floor would compare
policies against a reference that disagrees with itself by a third; the synthesis
method, comparator variance in the analysis rather than the margin, is the defensible
alternative and the preregistration names one. The band's rise is a single draw and
replicates across draws before it is written. For the fixed-fraction hypothesis: pin
day 25 with the day-20 pilot as prior and margin source, disclosing that day 25 was
seen under lab/012's different measurement; absolute L2 primary because the linear
head sees absolute moves and the sum control keeps its direction, relative L2 a
registered secondary with its predicted direction, falling under both aggregations,
stated before the run; pin both the ten checkpoints by content hash and the CSR floor
as a measured constant with the untouched stratum as the known negative. The
memorization check is retired with its reason: its consumer, a link-prediction arm,
left in round three, and lab/017's analytic-expectation check on the realised stale
fraction verifies uniformity directly. Of the fed papers: GraphSAGE settles the post
graph's construction and split and makes the project's 95.5 a replication of its
0.950 to 0.954, while its text says fifty communities and an average degree of 492
where the release carries 41 labels and two edge sets, discrepancies the
preregistration names rather than resolves, and it carries no timestamp field, so
lab/009's id clock has no published anchor; JODIE settles that the interaction graph
is a different object with no shared node identity and no deletions, closing the
round-three hope of one source for both; Holme and Saramäki settle the reference-model
vocabulary in which the deletion arms are declared by what they preserve, and carry no
null for growth; Milani Fard settles the churn definition and win-loss arithmetic and
does not carry a seed-only churn floor, so the project's measured 2.0 to 2.2 percent is
the floor and is cited as a measurement. Probes asked for: replicate the published
arxiv row on the CSR path; the task-quality gap on arxiv against the seed spread; the
across-episode spread of the hour gap over twelve disjoint hours; the band's rise over
further mutation draws; the day-25 floor from two passes per pinned checkpoint. Still
missing: the OGB baseline script's epochs and learning rate, the GraphSAGE appendix
and data card, Zügner, Akbarnejad and Günnemann 2018, a seed-only churn source, and a
growth null in the reference-model sense.

## Interpretation

**The two consultations agree without having read each other.** Both supersede the
round-three synthetic decision: the modelling side because the real stream is exact,
free and measured, the measurement side because a generator is now declared by what it
preserves of that stream. Both retire the memorization check for the same reason from
different directions. Both pin day 25 with the day-20 pilot as prior, absolute L2 as
primary with relative registered beside it, and saved checkpoints by hash. The
modelling side predicts the relative sum control loses its direction and the
measurement side writes that prediction into the preregistration before the run.

**The design as it stands.** One preregistration, two arms, on the day-25 snapshot of
the Reddit post graph with ten pinned checkpoints and on ogbn-arxiv with year episodes.
Arm A is the combinatorics and the lazy walk over four streams in declared roles: the
real growth stream as anchor, uniform deletion and uniform insertion as the incoherent
and coherent brackets, the hub constructions as the adversarial corner, each stream
carrying its rate, its degree targeting, its foreign-partner share and its measured
coherence; the predicted curve carries the spectral product as the bound and the
realised product as the prediction, with the first layer's gain and the per-post
laziness measured before the run. Arm B is the restated hypothesis: at a fixed
uniform-random stale fraction, absolute L2 error non-increasing in degree under mean
aggregation under both coherence regimes and increasing under sum, with uniform
insertion as the fixed-fraction cell, deletion through fixed-fraction bins, the real
stream at matched arrived fraction, and relative L2 as a registered secondary predicted
to fall under both. The downstream arm is behavioural consistency on the touched
low-degree strata with the hub cells reported as no-headroom, hour episodes primary
and day episodes secondary on Reddit, years on arxiv, touched status and degree
stratified jointly, the mutated-graph band as denominator and the band ratio as an
outcome. Task quality is a registered null screen on Reddit and conditional on two
probes on arxiv.

**What the round cost.** Two rulings the project had carried since round three fell
this evening on the project's own measurements: the synthetic-stream decision and the
features-carry-the-label mechanism. Neither ruling's conclusion changed; both routes
to it did. The record keeps both routes.

## Open

- The operator's own credence on the restated hypothesis; the ledger carries the
  consulted expert's.
- Which of the ten probes both consultations named run before the preregistration, in
  what order; the two sides name overlapping sets and the union is about a day of work.
- Whether the preregistration names the eligibility form or the synthesis form for the
  band; the measurement side rules for eligibility and names the alternative.
- The real stream's foreign-partner share, unmeasured, which sets the generator's
  coherence anchor.

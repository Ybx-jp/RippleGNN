# 016 — The root path carries about half the operator norm at both layers, and the second layer realises about half its spectral norm on real staleness

**Date:** 2026-09-05 · **Component:** refresh error model, the checkpoint's constants · **Status:** measured.

## What was asked

lab/008's probe list carries the spectral norms of the checkpoint's layer matrices, for
the slope of the fraction-aware bound and the laziness of the row-normalised walk in
Arm A. The restated hypothesis on the roster names, as a threat it cannot price, the
root-weight self path, whose relative norm on a trained checkpoint was unknown and
which could flatten every degree profile for the uninteresting reason that neighbour
staleness barely enters. This note reads the norms off lab/015's five checkpoints and,
from the same run, how much of the second layer's spectral norm a real aggregated-input
move realises. Script: `lab/probe_coherence_real.py`, which prints the norms as it
trains and the realised gain per arm.

## Setup

**The task** is node classification of Reddit posts by subreddit, one of 41, with a
two-layer GraphSAGE with mean aggregation (602 → 64 → 64) and a linear head, trained
full-batch with cross-entropy (Adam at 0.01, 100 epochs) on the training posts of the
starting graph. Five checkpoints, identical except for the seed (20260903–20260907),
lab/013's recipe. Each SAGEConv layer computes a neighbour term, the mean of the
neighbours' inputs through a matrix `W_l` (with bias), plus a root term, the post's own
input through a matrix `W_r`; the head is a 64 × 41 matrix.

**The data and the starting state** are the Reddit post graph before day 20 (153,430
posts, 5,376,616 edges of the paper's 11.6M-edge set); the checkpoints are trained
there and nothing else about the data enters the norms.

**The mutation** enters only the realised gain: lab/013's thirteen arms (uniform
deletion at 1, 5 and 20 percent; uniform insertion at 5 percent; hub bursts and hub
shifts at three settings each; the real stream at 1, 3 and 10 days), single draws,
seed 20260904, described in lab/015.

**What was held fixed.** Everything: the norms are properties of the trained weights,
read once per checkpoint. No retraining.

**What is compared.** The spectral norm (largest singular value) of `W_l` and `W_r` at
each layer and of the head, per checkpoint, and the root share `|W_r| / (|W_l| + |W_r|)`
per layer. The realised gain is, on posts touched at two hops only under an arm (whose
own input to the second layer is unchanged), the norm of the second layer's output move
over the norm of its aggregated-input move; since the move is exactly `W_l` of the
second layer applied to the input move, the gain lies between the smallest and largest
singular values of that matrix by construction, and the number read is where in that
range a real move falls.

**The baseline** for the root share is one half, equal norms on the two paths; for the
gain it is the spectral norm itself, the worst case a bound would use.

**The verifier check.** The gain's algebra is exact on the stratum: the input move was
computed from the first-layer deltas through the starting-graph adjacency, the output
move from the second layer's outputs on the two graphs, and their ratio never exceeded
the spectral norm in any cell, which it could not if the stratum were contaminated by
posts whose own input changed.

## Observation

| seed | layer 1 `|W_l|` | layer 1 `|W_r|` | root share | layer 2 `|W_l|` | layer 2 `|W_r|` | root share | head |
|---|---|---|---|---|---|---|---|
| 20260903 | 5.572 | 5.071 | 0.476 | 1.839 | 1.656 | 0.474 | 1.698 |
| 20260904 | 6.118 | 4.410 | 0.419 | 1.886 | 1.562 | 0.453 | 1.875 |
| 20260905 | 6.373 | 4.484 | 0.413 | 1.944 | 1.550 | 0.444 | 1.795 |
| 20260906 | 6.332 | 4.849 | 0.434 | 1.809 | 1.533 | 0.459 | 1.771 |
| 20260907 | 6.144 | 4.956 | 0.447 | 1.772 | 1.537 | 0.465 | 1.687 |

The product of the neighbour-path norms across the two layers is 10.2 to 12.4; the
product of the root-path norms is 6.9 to 8.4.

The realised gain of the second layer on posts touched at two hops only, mean over the
five checkpoints, by arm and decile: 1.02 to 1.07 on every decile under the deletion
arms, 0.92 to 1.06 under uniform insertion and the hub arms (lowest on the top decile,
0.92 to 0.93 under the bursts), 0.95 to 1.05 under one day of growth, and 0.75 to 1.05
under three and ten days, where deciles 6 to 8 read 0.75 to 0.89. Against a mean
spectral norm of 1.850 the realised gain is 0.41 to 0.58 of it.

## Interpretation

**The self path carries about as much as the neighbour path.** By operator norm the
root matrix is 0.41 to 0.48 of the two at both layers and on every seed, so neighbour
staleness enters a post's output at roughly half weight per layer, not a tenth and not
nine tenths. The threat the roster's hypothesis names, that the self path could
swallow the neighbour term and flatten every degree profile for a reason that says
nothing about aggregation, is priced: it does not. A root share by norm is not the
share of a post's output that comes from itself, which depends on the inputs on the
two paths (features on one, an aggregated hidden vector on the other) and is the
quantity a lazy walk's laziness should be set from; that is the measurement still to
make, on the real graph, as the ratio of the two terms' norms per post.

**A spectral-norm bound overstates the second layer's amplification by about two.** A
real aggregated-input move, whatever arm produced it, is amplified by 0.75 to 1.07
against a largest singular value of 1.77 to 1.94: the moves do not lie along the
matrix's top singular direction. A slope for the fraction-aware bound taken from the
spectral norms is a worst case that this checkpoint's real moves reach about half of,
consistently across arms and deciles; the growth arms at long horizons sit lowest.
Layer 1's realised gain was not measured, because its input move is a change of
neighbourhood rather than of a neighbour's vector and the identity does not hold
there.

**What this does to the design.** Arm A's bound has two constants from the
checkpoint; the slope can be read as the spectral product, 10.2 to 12.4, or as the
realised product, which at layer 2 is 1.0 and at layer 1 is unmeasured, and the
preregistration should say which and why. The laziness is not yet a measured number.

## Threats

- The norms are those of the 100-epoch recipe; a longer-trained checkpoint (lab/014's
  500-epoch control on arxiv) will have different ones, and the roster's hypothesis is
  about a trained checkpoint, not this recipe's.
- Five seeds; the spread across them is 0.06 on the root share and 0.17 on the
  layer-2 neighbour norm.
- The realised gain is on one stratum, posts whose own second-layer input is
  unchanged; on touched posts the output move includes the root term and the ratio is
  not a property of `W_l` alone.

## Open

- The per-post ratio of the root term to the neighbour term on the real graph, as the
  laziness for Arm A.
- The realised gain at layer 1, under a construction that isolates it.

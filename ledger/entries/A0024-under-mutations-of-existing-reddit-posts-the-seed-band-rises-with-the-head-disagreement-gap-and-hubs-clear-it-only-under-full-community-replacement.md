---
id: A0024-under-mutations-of-existing-reddit-posts-the-seed-band-rises-with-the-head-disagreement-gap-and-hubs-clear-it-only-under-full-community-replacement
kind: claim
stated: 2026-09-04T16:20:00-07:00
author: main
grade: measured
supersedes: none
verbatim_sha: cb2608c073e6b6a1eb1a303eccebd4d94396993555774fca4d1c7b60fd3933bc
---

## Assertion

On the Reddit post graph under mean aggregation with a subreddit-classifier head,
mutations that change the existing graph raise the seed-churn band on the hubs
together with the no-refresh gap in head disagreement: the band on the top one
percent of posts by degree is under 1 percent on the unmutated graph and rises to
about 14 percent when each hub's degree is doubled with posts of other subreddits
and to about 33 percent when each hub's same-subreddit edges are all rewired to
other subreddits, while the gap on those hubs is about 12 and 53 percent, so the
gap's lower confidence limit clears the band on the hubs only under complete
community replacement; the lowest-degree decile's touched posts clear it on twelve
of thirteen arms; ten days of the real growth stream, six million edges, move the
head's label on about 0.2 percent of the top decile against a band of about 0.9
percent; and the kNN@20 loss under no refresh is between 0.05 and 0.32 on all
existing posts across the arms and up to 0.69 on the hubs, with its seed band flat at
0.75 to 0.86 on every arm.

## Scope

metric: per existing post, whether one checkpoint's argmax label differs between its run on the starting graph and its run on the mutated graph (the gap), and one minus the overlap of its twenty nearest cosine neighbours among existing posts between the two, averaged per cell and over five seeds with the lower limit of a 95 percent t interval; beside the same quantities between two checkpoints differing only in seed, both on the mutated graph, averaged over the ten seed pairs (the band); cells are the mutation targets, the touched strata, and degree deciles on the starting graph; a cell is eligible when the lower limit exceeds the band
cohort: the paper's 11,606,919-edge Reddit graph restricted to posts before day 20 (153,430 posts, 5,376,616 edges) as the starting graph; checkpoints as in A0021 (two-layer SAGEConv with mean aggregation, 602 to 64 to 64, linear head, Adam at 0.01 for 100 epochs, seeds 20260903 to 20260907, 96.9 to 97.2 percent on their training posts); thirteen arms from one mutation draw (seed 20260904): uniform deletion of 1, 5 and 20 percent of edges (gap on all posts 0.0011, 0.0042, 0.0124 against bands 0.0203, 0.0209, 0.0240), uniform insertion of 5 percent (0.0346 against 0.0390), hub-burst at 0.1, 0.5 and 1.0 of degree on the 1,534 hubs of degree 416 and up (hubs 0.0066, 0.0503, 0.1248 against 0.0357, 0.0771, 0.1402), hub-shift at 0.25, 0.5 and 1.0 (hubs 0.0248, 0.1082, 0.5274 against 0.0537, 0.1128, 0.3317), the real stream for 1, 3 and 10 days (top decile 0.0007, 0.0012, 0.0021 against 0.0084, 0.0087, 0.0089); kNN@20 gap on all posts 0.046 to 0.317, on the hubs 0.534 under hub-burst 1.0 and 0.688 under hub-shift 1.0; RTX 3060, 544 s, 6.0 GiB
condition: nothing is refreshed and no checkpoint is retrained, so the gap is the whole distance a policy could close; the head is the 41-way subreddit classifier whose label the post's own features fix for most posts as in A0019; the mutations are single draws, so variation across draws is not measured, and they are constructions of the note rather than the calibrated generator the design asks for; hub arms pair hubs with uniform random existing posts of another subreddit, which are mostly low-degree posts, so the bottom decile is touched by the hub arms; deterministic full-graph inference on the sparse path, with cosine drift on untouched posts up to 3.6 × 10⁻⁴ on the three arms leaving under a hundred posts untouched; mean aggregation only; the alternative floor of the seed band on the starting graph is named in the note and not applied

## Grounds

- lab: lab/013-the-band-rises-with-the-gap-mutating-existing-posts-moves-the-head-only-where-it-moves-every-seed.md § "Observation" @113bc3e
- entry: A0022-on-the-reddit-growth-stream-the-no-refresh-gap-in-head-disagreement-sits-inside-the-seed-band-except-on-low-degree-touched-posts · cites-as-live
- entry: A0021-full-recomputes-differing-only-in-seed-disagree-on-two-percent-of-reddit-posts-and-under-one-percent-of-hubs · cites-as-live

## Warrant

The two tables of lab/013 are the measurement, gap and band read off one set of five
checkpoints per arm. The rise of the band with the gap is read directly from the
hubs row across the hub arms, where the band moves from 0.036 to 0.332 as the
mutation strengthens while the unmutated band of A0021 is 0.008; the growth arms
reproduce A0022's one-day figures and extend them to ten days. The eligibility
count per arm is the gap-floor rule applied cell by cell with the lower confidence
limit. The untouched stratum is the known negative, with drift at the sparse path's
rounding on every arm. A0021 supplies the reading of the kNN seed band as not this
probe's floor, which is why the kNN gap is reported against zero.

## Backing

none

<!-- APPEND BELOW THIS LINE ONLY -->

## Verdicts


## References

---
id: A0026-at-matched-growth-touched-arxiv-papers-change-label-fourteen-times-as-often-as-reddit-posts-and-at-matched-arrived-fraction-and-degree-their-embeddings-move-no-further
kind: claim
stated: 2026-09-04T21:12:00-07:00
author: main
grade: measured
supersedes: none
verbatim_sha: 38c4779b3ff143ab4bfffcf2043402f50561b6479c0ef2a7983a6bcd59afec98
---

## Assertion

Under no refresh on the real growth stream at matched node growth of 5.6 percent, an
existing ogbn-arxiv paper that received a citation changes predicted label on about
6.3 percent of cases against 0.46 percent for a Reddit post that received an edge,
with relative embedding change 0.082 against 0.032 and kNN@20 loss 0.26 against 0.13,
because a touched paper's arrived fraction averages 0.18 against 0.06; at matched
arrived fraction and degree class the kNN@20 loss is within 0.1 of Reddit's and the
relative L2 change is 0.55 to 0.9 of Reddit's, while head disagreement and its seed
band are both 1.4 to 9 times Reddit's, so the ratio of gap to band rises with the
arrived fraction alike on both graphs. arxiv's median paper, at degree 4, behaves like
Reddit's posts of degree 3 to 5 and not like Reddit's median post; in a real arxiv
year 4.7 percent of all existing papers and 10.3 percent of cited ones change label,
and the eligible cells under the gap-floor rule are the touched papers of degree 0 to
2 on every episode and 3 to 5 on the multi-year ones, with no cell of degree 9 and up
eligible on any episode; training the arxiv head five times longer moves the gap by
under 0.005 and raises the band by 0.02.

## Scope

metric: per existing node, whether one checkpoint's argmax label differs between its run on the starting graph and its run on the post-episode graph (the gap), one minus the overlap of its twenty nearest cosine neighbours among existing nodes between the two, one minus the cosine, and the relative L2 change, averaged per cell over five seeds with the lower limit of a 95 percent t interval; beside the same quantities between two checkpoints differing only in seed, both on the post-episode graph, averaged over the ten pairs (the band); cells are the touched strata, eight absolute starting-degree bins shared by both graphs (0, 1 to 2, 3 to 5, 6 to 8, 9 to 22, 23 to 52, 53 to 151, 152 and up) and five arrived-fraction bins on touched nodes; a cell is eligible when the lower limit exceeds the band
cohort: arxiv as in A0025, starting graph the 90,941 papers before 2018 with 369,033 undirected edges, checkpoints two-layer SAGEConv with mean aggregation, 128 to 64 to 64, linear head, Adam at 0.01 for 100 epochs on every starting paper, seeds 20260903 to 20260907, 63.9 to 65.0 percent on their training papers; episodes the papers of 2018 (29,799 papers, 246,382 edges), 2018 to 2019, 2018 to 2020, and two uniform draws of 5,112 papers of 2018 (seeds 20260904, 20260905; 38,485 and 38,302 edges, 13,255 and 13,254 papers touched); the Reddit anchor the paper edge set before day 20 and one day of the real stream, checkpoints by the same recipe at 602 to 64 to 64 (96.9 to 97.2 percent), reproducing lab/012 within 0.001; a 500-epoch control on arxiv (70.1 to 70.5 percent); RTX 3060, 52 s and 3.0 GiB for arxiv, 113 s and 5.8 GiB for Reddit
condition: nothing is refreshed and no checkpoint is retrained, so the gap is the whole distance a policy could close; the arxiv draws are constructions, since the dataset carries no order inside a year, and the band across draws is two draws only; the arxiv head is a 40-way subject classifier at 65 percent training accuracy, seven points under the published GraphSAGE row on the same split as recalled and not yet read off the pinned paper; mean aggregation only; deterministic full-graph inference on the sparse path with cosine drift on untouched nodes at most 3.0 times ten to the minus seven; the matched-degree comparison is read with each cell's mean arrived fraction, which agrees within 0.03 across graphs in the degree bins from 0 to 22 and differs above them

## Grounds

- lab: lab/014-arxiv-has-a-year-clock-and-at-matched-growth-its-touched-papers-move-fourteen-times-more-than-reddit-posts.md § "Observation" @de77a76
- entry: A0025-ogbn-arxiv-carries-a-year-clock-and-its-stream-is-growth-concentrated-on-the-top-degree-decile · cites-as-live
- entry: A0022-on-the-reddit-growth-stream-the-no-refresh-gap-in-head-disagreement-sits-inside-the-seed-band-except-on-low-degree-touched-posts · cites-as-live

## Warrant

The tables of lab/014 are the measurement: both graphs run through one script, one
recipe and one set of bins, gap and band read off one set of five checkpoints per
graph, so the cross-graph figures are differences between numbers produced the same
way, and the Reddit run reproducing A0022's day-20 figures within 0.001 is the check
that the shared code path is lab/012's. The matched-growth comparison holds the share
of new nodes fixed; the matched-fraction comparison holds the quantity the
mean-aggregation fraction law of A0012 and A0013 says governs the change, and those
entries are named as the explanation of the equal-or-smaller geometric gap and not as
a ground. The head's residual is read from the same cells: the gap and the band rise
together across graphs as they rose together across mutations in A0024, and the
500-epoch control separates the head's fit from the gap by moving one and not the
other. The untouched stratum is the known negative and the degree-zero touched papers
the known positive on both graphs. A0025 supplies the clock and the degree
distribution that make a year the episode and the absolute bins the stratification.

## Backing

none

<!-- APPEND BELOW THIS LINE ONLY -->

## Verdicts


## References


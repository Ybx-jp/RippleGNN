---
id: A0022-on-the-reddit-growth-stream-the-no-refresh-gap-in-head-disagreement-sits-inside-the-seed-band-except-on-low-degree-touched-posts
kind: claim
stated: 2026-09-04T13:05:10-07:00
author: main
grade: measured
supersedes: none
verbatim_sha: fd9243c1e9619b436393b19b53af1fb518d4ebf37a9f7cc2a9f5cba220a2ca38
---

## Assertion

On the Reddit post graph's real growth stream under mean aggregation, the fixed head
changes its label on about 0.35 percent of the existing posts after a day of
insertions, about 0.1 percent after six hours and about 0.02 percent after an hour,
against a seed-churn band of about 2 percent; the ratio of gap to band falls with
degree, from about a half on the second decile of touched posts to about a twelfth on
the top decile; the one cell in forty whose lower confidence limit clears the band is
the lowest-degree decile's one-hop-touched posts at six hours and a day, and that cell
does not clear it on the replication episode; and under sum aggregation the gap rises
about sevenfold and the band about eightfold, so that no cell clears the band, which
leaves a behavioural-consistency arm with seed churn as its denominator no eligible
cell among the hubs on this stream at episodes of a day or shorter.

## Scope

metric: per existing post, whether one checkpoint's argmax label differs between its run on the pre-episode graph and its run on the post-episode graph (the gap), averaged per cell and then over five seeds with the lower limit of a 95 percent t interval, beside the disagreement of two checkpoints' labels on the post-episode graph averaged over the ten seed pairs (the band), per touched stratum and per degree decile on the post-episode graph, with the cell declared eligible when the lower limit exceeds the band
cohort: the paper's 11,606,919-edge Reddit graph with the growth stream of A0018; checkpoints as in A0021 (two-layer SAGEConv, 602 to 64 to 64, linear head, Adam at 0.01 for 100 epochs, seeds 20260903 to 20260907), trained on the graph before the episode; episodes day 20 for one hour (gap 0.0002, band 0.0202), six hours (0.0011, 0.0201) and one day (0.0035, 0.0203; one-hop-touched 0.0046 against 0.0116; deciles 0.0152 to 0.0007 against 0.0981 to 0.0085; the bottom decile's touched posts 0.1131, lower limit 0.1086, band 0.0836) and day 25 for one day (0.0028 against 0.0215; that cell 0.0893, lower limit 0.0837, band 0.0867); sum aggregation on the day-20 episodes (a day: 0.0237 against 0.1567; checkpoints at 79.9 to 88.0 percent on the training posts); RTX 3060, 160 s per run at 5.8 GiB
condition: nothing is refreshed, so the gap is the whole distance a refresh policy could close and not any policy's residual; the head is the 41-way subreddit classifier at 95 percent whose label the post's own features fix for most posts as in A0019, and a head that depends on the neighbourhood is not measured; deterministic full-graph inference on the sparse path, whose run-to-run nondeterminism moved every mean-aggregation figure by under 0.001 and the sum band by about 0.02; the generator's deletions and any synthetic stream are not measured; episodes longer than a day are not measured; the sum checkpoints use the mean recipe unchanged, and their lower accuracy is part of what their band measures

## Grounds

- lab: lab/012-no-refresh-sits-inside-the-seed-band-on-nine-deciles-of-ten.md § "Observation" @98312cb
- entry: A0021-full-recomputes-differing-only-in-seed-disagree-on-two-percent-of-reddit-posts-and-under-one-percent-of-hubs · cites-as-live
- entry: A0020-a-day-of-the-reddit-growth-stream-touches-98-percent-of-existing-posts-within-two-hops · cites-as-live

## Warrant

The tables of lab/012 are the measurement: gap and band computed in one run from one
set of five checkpoints on the same posts, so the comparison is between two figures
read off the same checkpoints and not against A0021's numbers copied across, which the
run reproduces within 0.001. The eligibility rule is the measurement consultation's
gap-floor rule applied cell by cell, with the lower confidence limit as the
consultation's ordering asks. The untouched stratum serves as the known negative: a
post with no arriving edge within two hops has the same two-layer output on both
graphs, and its measured drift is at most 2.4 × 10⁻⁷ on every run, so a gap of zero
there is the instrument reading zero on a case where zero is exact. A0020 supplies the
strata and A0021 the reading of the band as a degree effect; the fall of the gap with
degree among touched posts, seventeenfold in relative L2 from the bottom decile to
the top, is the mean-aggregation fraction law of A0012 and A0013 on a real stream, and
those entries are named here as the explanation and not as a ground.

## Backing

none

<!-- APPEND BELOW THIS LINE ONLY -->

## Verdicts


## References

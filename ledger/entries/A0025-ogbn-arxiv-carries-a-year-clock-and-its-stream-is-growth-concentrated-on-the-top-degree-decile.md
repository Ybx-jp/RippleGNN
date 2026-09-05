---
id: A0025-ogbn-arxiv-carries-a-year-clock-and-its-stream-is-growth-concentrated-on-the-top-degree-decile
kind: claim
stated: 2026-09-04T21:10:00-07:00
author: main
grade: measured
supersedes: none
verbatim_sha: 0de16bda47568700e547bd0d5af2fbb1b286f2ea99fcbb99e889a2c4481badeb
---

## Assertion

The pinned ogbn-arxiv release carries one time field, a publication year per paper,
and its published split is exactly that year: training is every paper of 2017 or
earlier, validation is 2018, test is 2019 and 2020; fourteen years hold at least a
thousand papers and the MAG paper id does not order papers in time. Read as an edge
that exists from the year its later paper exists, the stream is growth with no edge
among existing papers, a year adds about a third of the graph in papers and half to
two thirds in edges, and about 72 percent of the edges joining a new paper to an old
one land on the top decile of the old papers by pre-2018 degree, with mean edges
gained rising with pre-2018 degree at slope 1.2. Before 2018 the undirected graph has
median degree 4 with 74 percent of papers at degree 8 or under, against a median of 49
and 10.5 percent on the Reddit post graph before day 20; full recomputation of a
two-layer GraphSAGE on the final graph takes about 16 ms and a third of a gigabyte on
the sparse path at hidden 64.

## Scope

metric: papers per publication year and the split flag of each; the Spearman correlation of MAG paper id with year and the share of cross-year pairs ordered alike by both; per year, the arriving edges split by whether both, one or neither endpoint is new; the share of new-to-old edges by the old endpoint's pre-2018 degree decile and the log-binned slope of mean edges gained over 2018 to 2020 against pre-2018 degree; degree mean, median and the share at degree 8 or under before 2018 and at the end; wall clock and peak VRAM of a forward pass, median of five synchronized passes after a warm-up
cohort: the OGB arxiv archive as downloaded 2026-09-04 (83,058,288 bytes, sha256 49f85c801589ecdcc52cfaca99693aaea7b8af16a9ac3f41dd85a5f3193fe276, release v1 of 2020-05-04): 169,343 papers, 1,166,243 directed citations collapsing to 1,157,799 undirected edges; 90,941 papers and 369,033 edges before 2018; the Reddit comparison from the paper's 11,606,919-edge set before day 20 (153,430 posts); the forward pass a two-layer SAGEConv with 128-dim input, untrained, eval, fp32, on an RTX 3060, edge_index path 27.8 ms and 1.39 GiB at 64, CSR path 16.4 ms and 0.33 GiB at 64 and 15.4 ms and 0.49 GiB at 128
condition: the year is the only clock, so no order inside a year is known and the 2020 year is partial; the growth reading follows from the convention that an edge exists once both endpoints do, and 1.8 percent of directed citations point forward in year, which is the only place the data could contradict it; degree deciles collapse at the low end (deciles 0 and 1 both end at degree 1), so decile shares below the second are not separable; the citation graph is read undirected; the MAG ids were checked as an order, not as timestamps

## Grounds

- lab: lab/014-arxiv-has-a-year-clock-and-at-matched-growth-its-touched-papers-move-fourteen-times-more-than-reddit-posts.md § "Observation" @de77a76

## Warrant

The clock, the split, the year table, the attachment shares and the degree
distributions are read directly off the pinned archive by the probe, and the split
identity is asserted by the script over every paper. The growth reading is the same
convention lab/009 applied to Reddit, and the 1.8 percent of forward citations is the
measured size of the one place the convention and the data disagree. The recompute
figures follow lab/009's protocol on the same box, synchronized, so the arxiv and
Reddit rows are comparable.

## Backing

none

<!-- APPEND BELOW THIS LINE ONLY -->

## Verdicts


## References


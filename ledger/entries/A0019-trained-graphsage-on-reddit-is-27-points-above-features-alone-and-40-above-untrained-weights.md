---
id: A0019-trained-graphsage-on-reddit-is-27-points-above-features-alone-and-40-above-untrained-weights
kind: claim
stated: 2026-09-03T20:40:00-07:00
author: main
grade: measured
supersedes: none
verbatim_sha: 30b4db38197669178e48740f693e929d7d3b90330eb47f5cac4c47d274ec5596
---

## Assertion

On the Reddit post graph, two-layer GraphSAGE at 64 dimensions trained end to end
full-batch reaches 95.4 to 95.6 percent test accuracy on the published temporal split,
a linear head on the 602 features alone reaches 68 percent and a one-hidden-layer MLP
on them 69, and the same GraphSAGE with its random initial weights frozen and only the
head trained reaches 53 to 55; the label signal is carried by the trained graph model
and not by the features, and validation and test accuracy agree within 0.2 points on
every arm.

## Scope

metric: test accuracy, equal to micro-F1 on this single-label task, at the epoch of best validation accuracy, with the validation accuracy beside it
cohort: the paper's 11,606,919-edge Reddit graph on two seeds, 20260903 and 20260904, and the full 57,307,946-edge graph on one seed for the trained arm and two for the untrained; 602-dim standardized features, 41 classes, the published split of 153,431 train, 23,831 validation and 55,703 test nodes; two-layer SAGEConv with mean aggregation, hidden 64, a linear head, full-batch Adam at learning rate 0.01 for 100 epochs on the CSR sparse path; RTX 3060
condition: no dropout, weight decay or learning-rate schedule, and no tuning of any of them, so the trained number is a floor for the architecture and not its best; the untrained arm embeds once with the initial weights and trains the head alone; one trained run on the full graph failed with an allocator out-of-memory that did not recur on the next seed; nothing here perturbs the graph, so the note measures the standing of the task and not any effect of staleness on it

## Grounds

- lab: lab/010-the-label-signal-is-not-in-the-features.md § "Observation" @7f0ccd6

## Warrant

The twelve rows of lab/010's table are the measurement: the gap between the trained
arm and the features-only arms, 27 points, is what the graph and the training add, and
the untrained arm sitting 14 points below features alone shows that a random 64-dim
projection discards signal the head on the raw features keeps, so the control cannot
score well by feature smoothing on this task. The agreement of validation and test,
the last ten days against the ten before them, is the absence of shift across the
split and is stated as scope rather than explained.

## Backing

none

<!-- APPEND BELOW THIS LINE ONLY -->

## Verdicts


## References


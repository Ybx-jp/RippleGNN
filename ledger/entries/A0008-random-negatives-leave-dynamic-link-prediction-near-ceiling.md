---
id: A0008-random-negatives-leave-dynamic-link-prediction-near-ceiling
kind: claim
stated: 2026-09-02T20:55:00-07:00
author: main
grade: argued
supersedes: none
verbatim_sha: 68c69588bcbd4c4a565122fe07180b6181c376cbaffa61b5dc6deb1c1b917df0
---

## Assertion

Under the standard evaluation for dynamic link prediction, which draws the negative
edges at random from all node pairs, the learned temporal models and a parameter-free
baseline that only memorizes previously seen edges both score near the AU-ROC ceiling on
the Wikipedia and Reddit interaction benchmarks, so a task scored this way leaves little
room in which a degradation of the embeddings could show.

## Scope

metric: test AU-ROC of dynamic link prediction, mean of five runs, with the negative for each positive edge formed by keeping its source and timestamp and drawing the destination uniformly from all nodes
cohort: the Wikipedia and Reddit interaction graphs of Kumar, Zhang and Leskovec, 9,227 and 10,984 nodes; JODIE, DyRep, TGAT, TGN and CAWN, and the EdgeBank memorization baseline in both of its variants
condition: the authors' implementations, hyperparameters and 70-15-15 chronological split, read from their tables and not rerun in this project; the Reddit interaction graph is a different dataset from the Reddit post graph whose full recompute lab/004 timed

## Grounds

- source: poursafaei-2022 · Table 3, the Wikipedia and Reddit rows
- source: poursafaei-2022 · §4, the paragraph beginning At test time, EdgeBank predicts

## Warrant

Table 3 puts TGN at 0.98 and 0.99 and CAWN at 0.99 and 0.99 on Wikipedia and Reddit,
and the baseline that stores every seen edge and answers from that list at 0.91 and
0.95, so a method that learns nothing is within a few points of the best learned model
and both are within a few points of the ceiling. The authors' explanation, quoted in
Backing, is that a randomly drawn node pair is almost never an edge that has been seen
before, so a method that answers from the edge list is rarely wrong on the negatives.
The authors read the near-perfect scores as the evaluation failing to differentiate
methods rather than as the task being solved; that reading is what this entry takes
from them, and the consequence for a refresh comparison is the project's own: an effect
has to fit between a baseline at 0.95 and a ceiling at 1.0.

## Backing

- source: poursafaei-2022 · §5, the opening paragraph
  speaker: Poursafaei, Huang, Pelrine and Rabbany
  quote: "Current SOTA methods for dynamic link prediction often achieve near perfect performance on existing benchmark datasets [18, 38, 42, 28, 40, 37]. Consequently, one can argue that either the existing datasets are too simplistic or the current evaluation process is insufficient to differentiate methods."
- source: poursafaei-2022 · §4, the paragraph beginning At test time, EdgeBank predicts
  speaker: Poursafaei, Huang, Pelrine and Rabbany
  quote: "In the standard random negative sampling evaluation [28, 42, 40], as graphs are often sparse, it is unlikely that an edge observed before will be sampled as a negative edge. Therefore, EdgeBank has strong performance on negative edges in many cases."

<!-- APPEND BELOW THIS LINE ONLY -->

## Verdicts


## References

- lab/006-poursafaei-read-the-threat-is-the-saturation-objection-again.md · record · cites-as-live

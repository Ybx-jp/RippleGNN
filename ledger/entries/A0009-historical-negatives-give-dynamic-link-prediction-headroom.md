---
id: A0009-historical-negatives-give-dynamic-link-prediction-headroom
kind: claim
stated: 2026-09-02T20:57:00-07:00
author: main
grade: argued
supersedes: none
verbatim_sha: 1c2b564ac41e3be03b26965fd255462a832d4ac1ca2962ea4279007ace0cd0ac
---

## Assertion

Scoring dynamic link prediction against historical negatives, edges seen earlier in the
stream but absent at the current step, removes the memorization floor: the baseline that
stores every seen edge falls to about chance on the Wikipedia and Reddit interaction
graphs, and the learned models lose at least ten AU-ROC points on average across the
benchmarks. A task scored this way has headroom that the random-negative task does not,
and what it asks is when a known edge recurs.

## Scope

metric: test AU-ROC of dynamic link prediction, mean of five runs, with the negatives at each step drawn from edges present in the training set and absent at that step, random negatives filling any shortfall
cohort: the thirteen datasets and five learned models of the random-negative results and both EdgeBank variants for the average drop; the Wikipedia and Reddit interaction graphs for the floor figures
condition: the authors' implementations, hyperparameters and 70-15-15 chronological split, read from their tables and not rerun in this project; the average drop is the authors' figure across models and datasets, and the drop on any one dataset differs from it; historical negatives exist only where an edge can be present at one step and absent at a later one

## Grounds

- source: poursafaei-2022 · Table 6, the Wikipedia and Reddit rows, against the same rows of Table 3
- source: poursafaei-2022 · Appendix B.1, the paragraph on Fig. 8
- entry: A0008-random-negatives-leave-dynamic-link-prediction-near-ceiling · cites-as-live

## Warrant

Under historical negatives the negatives are drawn from exactly the set the memorization
baseline answers yes to, so its errors on them go from rare to certain: Table 6 puts the
baseline that stores every seen edge at 0.49 and 0.51 on Wikipedia and Reddit against
0.91 and 0.95 under random negatives, and TGN at 0.84 and 0.81 against 0.98 and 0.99.
The appendix states the average drop across models as at least ten points. Set against
the cited entry, that is the headroom: under random negatives the best baseline and the
best model sit five points apart just under the ceiling, and under historical negatives
the floor is chance and the best model is fifteen to twenty points under the ceiling.
The authors' own statement of the strategy's objective, quoted in Backing, is the source
of the last clause of the assertion.

## Backing

- source: poursafaei-2022 · §5, the paragraph headed Historical Negative Sampling
  speaker: Poursafaei, Huang, Pelrine and Rabbany
  quote: "The objective of this strategy is to evaluate whether a given method is able to predict in which timestamps an edge would reoccur, rather than, for example, naively predicting it always reoccurs whenever it has been seen once."
- source: poursafaei-2022 · Appendix B.1, the paragraph on Fig. 8
  speaker: Poursafaei, Huang, Pelrine and Rabbany
  quote: "In general, the decrease is at least 10 percentage points."
- source: poursafaei-2022 · §6, the paragraph beginning First, we observe that the ranking of models
  speaker: Poursafaei, Huang, Pelrine and Rabbany
  quote: "Third, EdgeBank∞ has a significant drop in performance in both NS strategies. This shows that as the negative edges are sampled from either previously observed edges or unseen edges, naively memorizing all past edges is no longer sufficient."

<!-- APPEND BELOW THIS LINE ONLY -->

## Verdicts


## References

- lab/006-poursafaei-read-the-threat-is-the-saturation-objection-again.md · record · cites-as-live

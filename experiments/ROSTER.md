# Hypothesis roster

One row per hypothesis in the claims ledger whose status is not terminal. This is a
hand-maintained view of the ledger, not a generated one, and it is checked against the
entries before each commit: the first cell of a row cites the entry, the last cell
states its status, and a row that says something the entry does not, or a hypothesis
with no row, fails the check. A preregistration draws its hypothesis from here and
carries the motivating claims and the falsifier with it.

| hypothesis | statement | motivating claims | falsifier | status |
|---|---|---|---|---|
| (A0003-fraction-law-holds-with-trained-weights-and-depth, cites-as-live) | On a real graph with a trained two-layer mean-aggregation checkpoint, error at a fixed uniform-random stale fraction is independent of degree within a preregistered margin | (A0002-stale-fraction-governs-mean-aggregation-error, cites-as-live); (A0001-sageconv-aggregates-by-mean-unless-told-otherwise, cites-as-live) | the spread of error across degree deciles exceeds the margin at the fixed stale fraction | open |

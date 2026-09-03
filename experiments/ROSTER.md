# Hypothesis roster

One row per hypothesis in the claims ledger whose status is not terminal, and below
them the hypotheses that have fallen, kept as history. This is a hand-maintained view
of the ledger, not a generated one, and it is checked against the entries before each
commit: the first cell of a row cites the entry, the last cell states its status, and a
row that says something the entry does not, or an open hypothesis with no row, fails
the check. A preregistration draws its hypothesis from here and carries the motivating
claims and the falsifier with it.

| hypothesis | statement | motivating claims | falsifier | status |
|---|---|---|---|---|
| (A0013-error-at-fixed-stale-fraction-is-non-increasing-in-degree-on-a-trained-model, cites-as-live) | On a real graph with a trained two-layer mean-aggregation checkpoint, error at a fixed uniform-random stale fraction is non-increasing in degree across deciles within a preregistered margin, and increasing under sum aggregation on the same architecture | (A0012-stale-fraction-error-is-non-increasing-in-degree-under-mean-aggregation, cites-as-live); (A0001-sageconv-aggregates-by-mean-unless-told-otherwise, cites-as-live) | the median error in the top degree decile exceeds the bottom decile's by more than the margin under mean aggregation, or fails to exceed it under sum | open |

## Fallen

| hypothesis | statement | motivating claims | falsifier | status |
|---|---|---|---|---|
| (A0006-fraction-law-holds-with-trained-weights-and-depth, cites-as-fallen) | Superseded by the row above after lab/007: the equality it stated is the coherent special case, and a uniform-random stale set is expected to fall with degree instead | (A0005-stale-fraction-governs-mean-aggregation-error, cites-as-fallen) | the spread across deciles exceeds the margin | superseded |
| (A0003-fraction-law-holds-with-trained-weights-and-depth, cites-as-fallen) | Superseded the same day by the row above: its ground was superseded to correct a Backing locator, and a dependent of a fallen entry is restated, not repaired | (A0002-stale-fraction-governs-mean-aggregation-error, cites-as-fallen) | as above | superseded |

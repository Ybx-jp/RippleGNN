# Unscored rankings, preferences, withdrawals and self-refutations

Sixteen statements the consultation channel made that carried no number. Per the ledger
schema a statement with no resolution criterion is a preference, not a prediction, and
cannot be scored — so these are listed rather than given entries.

They are kept because several are load-bearing anyway: two are direct conflicts between
the experts that nobody has adjudicated, two are withdrawals caused by procurement
failure rather than by evidence, and one (A15) is a self-refutation whose pre-correction
form is still what the public contract says.

The asymmetry worth acting on: every numeric confidence in this project came from `dl`.
`eval-methodology` stated rankings, corrections and withdrawals and never a probability.
The fix is to ask for numbers in the ticket, not to impute them here.

| # | Statement | Expert | Ticket | Standing |
|---|---|---|---|---|
| A5 | dl's five ordered experiments: R1 invalidation-set/influence combinatorics > R2 sub-k sweep vs GAS bound > R3 memory-residency cliff > R4 scheduling under budget > R5 mutation-class asymmetry. Ranked on "expected information per CPU-second". | dl | modelling consultation, round 2 §3 | Unrun. lab/005 argues R1 measures the wrong quantity for a mean aggregator (set *size* vs set *fraction*), which if right demotes R1 as specified. |
| A6 | eval-methodology's five ordered experiments: R1 metric qualification grid > R2 non-inferiority study > R3 geometric-drift-predicts-decision-change > R4 dataset-moderator replication > R5 cost-axis measurement. Ranked on "expected validity per CPU-second". | eval-meth | measurement consultation, round 2 §1 | Unrun. Its R1 and dl's R1 are different experiments with the same rank; the collision is unadjudicated. |
| A7 | Dataset tier ranking: ogbn-products and Reddit tier A; ogbn-arxiv, Yelp, Flickr, Cluster tier B; Cora/CiteSeer/PubMed tier C ("scheduling noise wearing a result's clothing"). | dl | modelling consultation, round 2 §4 | **Primary refuted by lab/004** — both tier-A entries OOM at 128-dim. Tier C confirmed by lab/004's sub-millisecond measurements. |
| A8 | Dataset ranking: tgbl-wiki primary, tgbl-review as R4 contrast, OGB link-property as fallback; hard rejection of Cora/CiteSeer/PubMed and of PPI/Reddit/Amazon2M (saturation). | eval-meth | measurement consultation, round 2 §2 | **Primary refuted by lab/004** — tgbl-wiki full recompute is 1.729 ms. The saturation objection to Reddit is *not* refuted and lab/004 explicitly leaves it standing. |
| A9 | Domain ranking: product co-purchase > social/forum > citation (control) > financial fraud (cite as motivation only) > road/infrastructure ("the trivial-success trap"). | dl | modelling consultation, round 2 §4 | Open; downstream of the unresolved dataset decision. |
| A10 | "Do not adopt a CTDG benchmark. Construct your mutation stream over a large static graph." | dl | modelling consultation, round 2 §4 | **Direct conflict with A8**, which ranks tgbl-wiki primary precisely because its split and negative-sampling protocol are prescribed rather than self-designed. Unadjudicated. |
| A11 | Ruling: conduct primary fidelity measurement under full-graph inference; report sampled fidelity as a mandatory second panel; report the difference as a third estimand. | eval-meth | measurement consultation, round 2 §3 | Accepted into `experiments/README.md` only in its first clause. The three-panel decomposition is not in the contract. |
| A12 | "the sharpest threat to your novelty" is GNNAutoScale/VR-GCN historical embeddings — later ruled: "Partial withdrawal. The novelty claim on 'stale neighbour with an error bound' is dead." | dl | R1 §5 G2, ruled in R2 §1 | The withdrawal is itself a scoreable channel event: predicted in R1, confirmed against the fed papers in R2. |
| A13 | R1 withdrawal: "On insert/delete asymmetry I withdraw the round-1 prediction that it is a theorem I can hand you." | dl | modelling consultation, round 2 §3/R5 | Retracted before it could be scored. Cause: the IVM classics never ingested (host allowlist), so the prediction had no source. |
| A14 | R1 withdrawal: "I withdraw the RBO recommendation from round 1 §5 G9 and will not cite it." | eval-meth | measurement consultation, round 2 §0 | Retracted; cause was procurement failure, not evidence. |
| A15 | Self-refutation: "my 'smaller dataset, more replays' advice is partly refuted… the correct form is many episodes on one adequately-sized graph, not many tiny graphs." | eval-meth | measurement consultation, round 2 §0 Correction 2 | **The pre-correction form is still what the public contract says.** See P1. |
| A16 | Self-refutation: "CKA is the wrong primary geometric measure, and this is measured, not argued… Use Orthogonal Procrustes distance instead." | eval-meth | measurement consultation, round 2 §0 Correction 1 | Corroborated by held literature. **Not wired into any repo document.** See B29. |
| A17 | "Your K=20 is defensible but unmotivated; k=10 has measured warrant and is cheaper." | eval-meth | measurement consultation, round 2 §0 | lab/002 used K=20. Unchanged. |
| A18 | "your measured 0.6208 floor is likely an optimistic bound" (because L1 used uniform degree, so hubness cannot arise). | eval-meth | measurement consultation, round 2 §0 Correction 3 | Untested. Directionally agrees with lab/002's own stated threat. |
| A19 | "in deployment, the sampler may contribute as much embedding instability as the entire refresh decision. If that reproduces on graphs, it is the most interesting result this project can produce." | eval-meth | measurement consultation, round 2 §3 | Untested; transferred from a word-embedding result, labelled by the expert as a transfer. |
| A20 | "the modal outcome you should expect": a simple heuristic (recency-ordering, EdgeBank) matches the clever policy, and that counts as the finding. | both | R1 §3c / R2 §2, and dl R4 | Untested. |

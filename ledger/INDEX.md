# Ledger index

Generated from the entries. Do not hand-edit — regenerate.

Backfilled 2026-08-27 from `lab/claims-inventory-draft.md`, which read the four
consultation exchanges in full, `lab/001`-`lab/005`, `MANIFEST.md`,
`experiments/README.md`, `CLAUDE.md` and `README.md`.

Schema: `ledger/README.md`.

## Verdict provenance

26 verdicts name a source · 30 record that a search found nothing ·
5 record a broken chain.

The five broken chains were later resolved by a repair verdict appended to each entry:
four recovered a primary third-party source, one recorded that a search found none. The
original rows stay, so a repaired chain still shows where it broke.

## Claims — 52

By grade: `argued` 32, `asserted` 8, `measured` 12
By status: `contested` 5, `corroborated` 21, `open` 21, `refuted` 3, `superseded` 2

| id | grade | status | statement |
|---|---|---|---|
| `C001-4-cores-not-the-gpu-is-the-binding` | `asserted` | `refuted` | "4 cores, not the GPU, is the binding constraint, because neighborhood sampling and mutation replay are CPU-bound." |
| `C002-vram-caps-full-graph-refresh-at-roughly-1` | `measured` | `superseded` | "VRAM caps full-graph refresh at roughly 1-2M nodes" |
| `C003-the-ceiling-is-an-edge-count-0-51` | `measured` | `corroborated` | "the ceiling is an edge count… ~0.51 GiB per million edges at 128-dim; between 15M and 20M edges" |
| `C004-an-unsynchronized-timing-of-a-knn-kernel-understated` | `measured` | `corroborated` | "an unsynchronized timing of a kNN kernel understated it by 173x, because it timed queue submission rather than compute" |
| `C005-full-recompute-timings-for-named-benchmarks-cora-0` | `measured` | `corroborated` | Full-recompute timings for named benchmarks: Cora 0.504 ms, CiteSeer 0.519 ms, tgbl-wiki 1.729 ms, Reddit-JODIE 2.099 ms, PubMed 2.047 ms; Reddit and … |
| `C006-at-every-scale-that-fits-on-this-box` | `measured` | `contested` | "at every scale that fits on this box, exact nearest-neighbor search is affordable, so no ANN index is needed… Exact search removes a confound rather … |
| `C007-full-recomputation-never-becomes-slow-on-this-hardware` | `measured` | `corroborated` | "Full recomputation never becomes slow on this hardware. It becomes *impossible*." |
| `C008-the-manifest-s-premise-that-recomputing-every-embedding` | `asserted` | `open` | "the manifest's premise… that recomputing every embedding after every change is expensive enough to be worth avoiding" |
| `C009-full-graph-inference-is-bitwise-reproducible-the-floor` | `measured` | `contested` | "Full-graph inference is bitwise reproducible: the floor is exactly zero." |
| `C010-on-an-unchanged-graph-it-loses-37-9` | `measured` | `corroborated` | "on an unchanged graph it loses 37.9% of each node's top-20 neighborhood on average, with a worst case of 19 of 20 neighbors changed" while cosine rea… |
| `C011-the-floor-is-a-property-of-the-inference` | `argued` | `open` | "The floor is a property of the inference path, not of the model or the graph." |
| `C012-rank-based-measures-are-primary-a-geometric-figure` | `measured` | `corroborated` | "Rank-based measures are primary. A geometric figure may accompany one but never substitutes for it." |
| `C013-stability-metrics-are-reported-chance-corrected-p-pnull` | `argued` | `open` | "Stability metrics are reported chance-corrected… κ = (p − p_null)/(1 − p_null)", null from k≥5 unchanged-graph reruns, "also the control for the rota… |
| `C014-no-refresh-scores-perfectly-on-any-pure-stability` | `argued` | `open` | "No-refresh… scores perfectly on any pure stability metric — it is maximally self-consistent because it does nothing. Any metric on which no-refresh w… |
| `C015-local-refresh-approximates-full-recomputation-is-confounded-between` | `argued` | `corroborated` | "'Local refresh approximates full recomputation' is confounded between locality genuinely holding and the mutations being too small to move anything." |
| `C016-an-untrained-gnn-was-already-showing-performance-that` | `argued` | `corroborated` | "an untrained GNN was already showing performance that is competitive with DeepWalk" → every headline run carries an untrained-weights control |
| `C017-cka-requires-deleting-97-of-principal-components-before` | `argued` | `open` | "CKA requires deleting 97% of principal components before registering a detectable dissimilarity… Use Orthogonal Procrustes distance instead." |
| `C018-any-similarity-index-that-is-invariant-to-orthogonal` | `argued` | `open` | "any similarity index that is invariant to orthogonal transformation can be made invariant to invertible linear transformation by orthogonalizing the … |
| `C019-ten-nearest-neighbors-performs-approximately-as-well-as` | `argued` | `open` | "Ten nearest neighbors performs approximately as well as a higher number" / k=5 top-performing as predictor of downstream disagreement |
| `C020-for-a-k-layer-full-neighborhood-message-passing` | `argued` | `open` | "For a k-layer full-neighborhood message-passing model, this never happens, and the answer is not empirical — it is definitional. Exact k-hop refresh … |
| `C021-the-interesting-object-is-the-size-distribution-of` | `argued` | `contested` | "The interesting object is… the size distribution of the k-hop reverse-reachable set… **This is a property of the degree distribution, not of the mode… |
| `C022-theorem-2-hand-fed-at-100-anchoring-h` | `argued` | `corroborated` | Theorem 2, hand-fed at 100% anchoring: `‖h̃_v^(L) − h_v^(L)‖ ≤ Σ ε^(ℓ)·k₁^(L−ℓ)·k₂^(L−ℓ)·\|N(v)\|^(L−ℓ)` |
| `C023-the-n-v-factor-comes-from-sum-aggregation` | `measured` | `corroborated` | "the \|N(v)\| factor comes from **sum** aggregation… mean or max admits a much tighter bound" → measured: "Under mean aggregation the error is **exactly… |
| `C024-sageconv-s-default-in-pyg-is-mean` | `measured` | `corroborated` | "SAGEConv's default in PyG is mean" |
| `C025-the-influence-distribution-ix-for-any-node-x` | `argued` | `corroborated` | "the influence distribution I_x for any node x is equivalent, in expectation, to the k-step random walk distribution" (JKNet Thm 1) |
| `C026-random-walks-starting-inside-an-expander-converge-rapidly` | `argued` | `corroborated` | "Random walks starting inside an expander converge rapidly in O(log\|V\|) steps to an almost-uniform distribution" → on expander-like graphs influence d… |
| `C027-negatively-curved-edges-are-exactly-the-edges-whose` | `argued` | `open` | "negatively-curved edges are exactly the edges whose mutation has the *smallest* reverse-reachable set, and positively-curved ones the largest… a test… |
| `C028-the-minimal-hidden-dimension-to-fit-radius-r` | `argued` | `corroborated` | "the minimal hidden dimension to fit radius r grows exponentially with r; even d = 512 can empirically fit r = 7 at most" → "Real models are shallow b… |
| `C029-your-r-sweep-is-a-one-parameter-family` | `argued` | `corroborated` | "Your r-sweep is a one-parameter family of GAS batches. Lemma 1 already covers it." |
| `C030-the-bound-is-worst-case-and-nobody-measured` | `argued` | `open` | "The bound is worst-case and nobody measured its tightness… Ratio-of-realised-to-bound as a function of r and degree is an unoccupied, cheap, defensib… |
| `C031-their-is-not-your-yours-is-stale-with` | `argued` | `open` | "Their ε is not your ε… Yours is stale with respect to *graph mutation*. Weight drift is global and smooth; mutation drift is sparse and heavy-tailed.… |
| `C032-manifest-line-103-mutation-types-should-not-be` | `asserted` | `open` | MANIFEST line 103: mutation types "should not be assumed equivalent" — insert/delete/feature asymmetry |
| `C033-a-non-inferiority-claim-without-a-pre-specified` | `argued` | `corroborated` | "A non-inferiority claim without a pre-specified margin is unfalsifiable" — with the measured figure that 158/273 (57.9%) of published margins do not … |
| `C034-the-margin-is-expressed-as-a-fraction-of` | `argued` | `contested` | "The margin is expressed as a fraction of the full-recompute-to-no-refresh gap on the same probe, less the measured seed-variance floor for that confi… |
| `C035-on-4-shared-cores-wall-clock-is-a` | `argued` | `open` | "on 4 shared cores, wall-clock is a measurement of your box's scheduler, not of the algorithm. Report FLOPs, nodes-revisited, and messages-passed as t… |
| `C036-more-independent-mutation-episodes-and-more-seeds-buy` | `argued` | `superseded` | "More independent mutation episodes and more seeds buy more validity than more nodes per snapshot. **A smaller graph replayed over many episodes domin… |
| `C037-per-node-across-a-shared-checkpoint-will-be` | `argued` | `open` | "per-node ρ across a shared checkpoint will be far above 0.017" |
| `C038-git-history-is-not-a-timestamp-on-a` | `argued` | `corroborated` | "Git history is not a timestamp on a repo you control" → pre-registration is timestamped by its **push** |
| `C039-ppi-reddit-and-amazon2m-are-saturated-83-65` | `argued` | `contested` | "PPI, Reddit and Amazon2M are saturated — 83%/65%/90% of nodes used for training, an artificially small distribution shift; there is no headroom for a… |
| `C040-inductive-node-ratio-is-your-primary-selection-criterion` | `argued` | `refuted` | "inductive node ratio is your primary selection criterion and the surprise index is your moderator" |
| `C041-degrees-here-are-published-approximate-values-applied-to` | `asserted` | `open` | "Degrees here are published approximate values applied to synthetic random graphs of the right size, not the real datasets loaded. **The memory arithm… |
| `C042-run-py-is-itself-the-analysis-path-an` | `argued` | `corroborated` | "run.py… **is itself the analysis path**. An analysis re-derived beside the production code path is a second implementation that can be wrong on its o… |
| `C043-adequacy-is-claimable-over-the-declared-grid-never` | `argued` | `open` | "Adequacy is claimable over the declared grid, never over the domain of mutations." — with k-MR coverage instantiated as "each mutation type must asso… |
| `C044-faithfulness-is-four-estimands-self-consistency-rank-survival` | `argued` | `corroborated` | Faithfulness is four estimands (self-consistency, rank survival, downstream behavioural consistency, downstream task quality) that must never be colla… |
| `C045-15-of-predictions-on-a-sentiment-analysis-task` | `argued` | `open` | "15% of predictions on a sentiment analysis task can disagree due to training the embeddings on an accumulated dataset with just 1% more data" → full-… |
| `C046-manifest-line-109-at-least-one-comprehensible-applied` | `asserted` | `open` | MANIFEST line 109: "At least one comprehensible applied domain should be used to validate that the mechanism provides practical value, not merely attr… |
| `C047-manifest-line-71-graphsage-is-a-strong-initial` | `asserted` | `open` | MANIFEST line 71: "GraphSAGE is a strong initial candidate… but the project is not defined by GraphSAGE. Model choice is a research decision." |
| `C048-poursafaei-et-al-did-not-land-that-paper` | `asserted` | `open` | "Poursafaei et al. did not land… That paper is a direct threat to your evaluation design and you should read it before you write a single eval script.… |
| `C049-lab-003-s-cost-accounting-34-144-44` | `measured` | `open` | lab/003's cost accounting: 34,144 / 44,419 chars, 34 / 63 validated citations, 31 documents, ~$23, ~95 minutes; "whether that trade is good is not yet… |
| `C050-nothing-may-cite-a-live-dataset-directory-datasets` | `asserted` | `corroborated` | "Nothing may cite a live dataset directory"; `datasets.jsonl` pins the registry, "the bytes are not" committed |
| `C051-more-episodes-and-seeds-buy-more-validity-than-more-nodes` | `argued` | `corroborated` | More independent mutation episodes and more seeds buy more validity than more nodes per snapshot. Power comes from the number of independent episodes,… |
| `C052-a-smaller-graph-replayed-dominates-the-largest-that-fits` | `argued` | `refuted` | A smaller graph replayed over many episodes dominates the largest graph that fits in memory. |

## Predictions — 4

| id | grade | status | credence | statement |
|---|---|---|---|---|
| `P001-l3-kills-exact-k-hop-refresh-and-the-real-result-is-the-curve` | `argued` | `superseded` | 0.65 | my current expectation is that L3 kills exact k-hop local refresh at k>=2 on any heavy-tailed graph, and that the project's real result is the sub-k f… |
| `P002-exact-k-hop-refresh-degenerates-to-global-on-heavy-tailed-graphs` | `argued` | `contested` | 0.78 | Exact k-hop local refresh degenerates to effectively-global recomputation at k >= 2 on any heavy-tailed graph. |
| `P003-the-real-result-is-the-fidelity-curve-not-a-refresh-engine` | `argued` | `contested` | 0.70 | The project's real result is the sub-k fidelity curve plus the cost-blowup characterisation, rather than a refresh engine. |
| `P004-realised-error-an-order-of-magnitude-below-the-lemma-1-bound` | `argued` | `contested` | 0.60 | on ogbn-products and Reddit, realised error at refresh radius r will be more than an order of magnitude below the Lemma-1 bound at every r > 0, and th… |

## Unscored

`unscored-rankings.md` — 16 statements with no resolution criterion.

# Dynamic Graph Embedding Refresh — Research Manifest

## Mission

Investigate how to maintain useful graph representations as a graph evolves without paying the full cost of recomputing every embedding after every change.

The core research question is:

> Given an evolving graph and a trained inductive GNN, what is the cheapest refresh strategy that keeps its embedding space sufficiently faithful for downstream use?

The purpose of this project is discovery first. Research quality, learning, and system design follow from that. The project should not begin by assuming that a production system ought to exist, nor by committing to an architecture before the behavior of the problem is understood.

Run the experiments and see what truth drops out.

## What “cheap” means

Refresh cost is multidimensional.

A useful strategy may trade among:

- latency,
- compute and monetary cost,
- availability,
- consistency,
- tolerated staleness,
- and the fraction of the graph that must be revisited.

There is no presumption that these dimensions collapse cleanly into one scalar objective. The interesting result may be a family of trade-offs rather than a single winner.

## What “faithful” means

Faithfulness is not exact vector identity.

An embedding space may move geometrically while remaining useful if its applied semantics remain stable. The project should treat semantic stability as an empirical property to be characterized, not as a definition chosen in advance.

Relevant questions include:

- whether meaningful localities in representation space remain stable,
- whether neighborhood or ranking relationships survive refresh,
- whether downstream behavior remains consistent,
- whether target structures remain retrievable,
- whether the refreshed representation continues to improve outcomes over baseline,
- and how semantic stability relates to geometric stability or drift.

The intersection between semantics and geometry is itself part of the research surface.

## Research surface

The project is interested in three coupled phenomena.

### Locality

How far should the effect of a graph mutation propagate?

Changes to a node, edge, property, feature, or neighborhood may invalidate more than the directly modified structure. The project should investigate whether the impact of change is meaningfully local, how locality depends on the model and mutation type, and when local refresh ceases to approximate global recomputation.

### Staleness

How long can an embedding remain stale before it becomes materially harmful?

Staleness should be treated as a tunable dimension, not automatically as a defect. Some applications may benefit from knowingly serving stale representations when the expected loss is small relative to the cost or availability benefit.

### Prioritization

When refresh capacity is limited, what should be refreshed first?

A useful strategy may prioritize some regions, nodes, or mutation classes over others. Reactive heuristics, model-aware policies, predictive refresh, and learned prioritization are all legitimate avenues if evidence justifies them.

## Models

GraphSAGE is a strong initial candidate because inductive neighborhood aggregation naturally fits an evolving-graph setting, but the project is not defined by GraphSAGE.

Model choice is a research decision.

Both model-agnostic and model-aware refresh strategies are in scope. There is particular interest in approaches that exploit GNN message-passing structure, but generality should not be assumed or sacrificed without evidence.

## Evaluation

No single downstream task should define success prematurely.

Candidate evaluations include:

- link prediction,
- node classification,
- recommendation,
- retrieval,
- nearest-neighbor stability,
- ranking stability,
- and other applied tasks suggested by the selected domain.

The important criterion is functional usefulness: target structures should be retrieved or represented in ways that consistently improve outcomes over appropriate baselines.

Full recomputation is an important reference point. No refresh and naive/local refresh policies are natural baselines. Additional alternatives should be selected from the literature and from experimental evidence.

The goal is not merely to demonstrate that incremental refresh can work. The goal is to understand where it wins, where it loses, and under what trade-off regime it is useful.

## Data

Dataset selection is itself a research task.

Datasets should be chosen based on their ability to expose the phenomena under study rather than because they are convenient or familiar. Synthetic mutations, naturally temporal graphs, replayable event streams, or combinations of these may all be appropriate.

Mutation type is part of the problem. Edge changes, node changes, feature changes, structural bursts, and other forms of graph evolution may have different effects and should not be assumed equivalent.

## Applied validation

The research should eventually leave benchmark space.

At least one comprehensible applied domain should be used to validate that the mechanism provides practical value, not merely attractive embedding metrics.

The applied system exists to test the research claim. It is not the mission of the project.

## Research discipline

Literature precedes design.

Before committing to a mechanism, establish what is already known about dynamic and temporal graph representation learning, incremental GNN inference, localized recomputation, embedding drift and staleness, caching, refresh scheduling, and related work.

Novelty is a question to investigate, not a premise.

Experiments should preserve epistemic history:

- record hypotheses before evaluating them,
- preserve failed and negative experiments,
- distinguish observations from interpretations,
- keep baselines reproducible,
- do not silently change evaluation methodology,
- document changes that break comparability,
- treat null results as information,
- and prefer evidence that falsifies a favored explanation over evidence that merely decorates it.

When findings conflict with the intended system design, the findings win.

## Scope discipline

This project is not initially an effort to build a distributed production embedding service.

It is not a native vector database project.

It is not a graph infrastructure platform.

It is not an excuse to build orchestration machinery before the underlying phenomenon is understood.

Systems work should be earned by experimental evidence.

Prefer small, interpretable experiments and incrementally larger hypotheses. Scale when scale exposes a research question that cannot be answered otherwise.

## Success

Success is not defined by a predetermined metric threshold or implementation milestone.

The project succeeds when it establishes something useful and defensible about dynamic embedding refresh: a mechanism, trade-off, regime, limitation, or phenomenon that is substantial enough to matter in an applied setting and comprehensible enough to compare against alternatives.

The desired end state is not “we built a refresh engine.”

It is:

> We understand when dynamic graph embedding refresh works, why it works, what it costs, what it preserves, where it fails, and when it is preferable to the alternatives.

Everything else is downstream of that understanding.

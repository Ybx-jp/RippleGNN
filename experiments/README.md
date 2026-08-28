# experiments

The other genre. An experiment is written for a technical reader outside the project,
states what was committed to before the data was seen, and regenerates every number in
it from a pinned dataset state and a seed.

    experiments/
      datasets.jsonl           pinned dataset/mutation-stream registry (committed; the bytes are not)
      NNN-slug/
        preregistration.md     written first, pushed before the first run, never edited after
        run.py                 regenerates results.json; no other inputs
        results.json           every number the writeup shows, machine-readable
        environment.json       captured interpreter, library, driver and determinism state
        findings.md            the writeup

## What is being claimed, and therefore what must be measured

"The cheapest refresh strategy that stays sufficiently faithful" is a **non-inferiority
claim**, not a superiority claim. A non-inferiority claim without a pre-specified margin
is unfalsifiable: any observed difference can be called small after the fact.

So every experiment asserting a strategy is "good enough" states its margin in
`preregistration.md`, **with its derivation**, before the run. The margin is expressed as
a fraction of the full-recompute-to-no-refresh gap on the same probe, less the measured
seed-variance floor for that configuration. A margin chosen without reference to that gap
is a number picked to be passed.

Faithfulness is not one axis. Treat it as at least four estimands with different
baselines and units, and never collapse them into a single score:

1. **Self-consistency** — does the refreshed space agree with itself across seeds.
2. **Rank survival** — do neighborhood and ordering relationships persist.
3. **Downstream behavioral consistency** — does the dependent system make the same calls.
4. **Downstream task quality** — does it still do the job well.

Rank-based measures are primary. A geometric figure (cosine, L2) may accompany one but
never substitutes for it: the two can disagree sharply and in the direction that flatters
the author.

## Baselines, and the one that is a trap

Fixed by the manifest: full recomputation is the reference point; no-refresh and naive
local refresh are baselines. A comparison omitting full recomputation is not a result.

**No-refresh is also the falsifier arm for every probe, not merely a baseline.** It scores
perfectly on any pure stability metric — it is maximally self-consistent because it does
nothing. Any metric on which no-refresh wins is degenerate and must be discarded rather
than reported. Run it against every probe for exactly this reason.

**"Local refresh approximates full recomputation" is confounded** between locality
genuinely holding and the mutations being too small to move anything. Every such
comparison carries a positive control: a deliberately destructive mutation that the probe
must detect. A probe that cannot see the wrecking case has not shown locality holds; it
has shown the probe is blind.

## Controls

Stability metrics are reported **chance-corrected**. The null is not zero and it is not
assumed: train k>=5 seeds on the *unchanged* graph, and that distribution is the null.
Report `kappa = (p - p_null) / (1 - p_null)`.

This is also the control for the rotation and alignment problem. Two runs may produce
spaces related by a transformation that makes naive vector comparison meaningless, and
the defense is structural — a null built from unchanged-graph reruns — rather than a
geometric alignment step chosen after seeing the data.

Where the model's inference path samples neighborhoods, the seed-variance floor is
measured per configuration and pre-registered. Full-graph inference has a floor of zero
and is preferred wherever it fits.

Every headline run carries an **untrained-weights control**. An untrained GNN can be
competitive when node features are informative, so a policy that merely preserves feature
smoothing will look faithful while all learned signal has drifted.

## The unit of analysis is not the node

More independent mutation episodes and more seeds buy more validity than more nodes per
snapshot. The design-effect argument is about the number of independent *episodes*, which
is not the same axis as graph size: the correct form is many episodes on one
adequately-sized graph, not many tiny graphs. Power comes from the number of independent
episodes, and a single snapshot of a huge graph is n=1 however many nodes it has.

Adequately-sized is not a node count. The selection axis is whether the dataset's own
statistics leave room for a refresh effect to exist at all: a benchmark that trains on
83-90% of its nodes has an artificially small distribution shift and no headroom for one
to live in.

## The run.py contract

1. Takes `--dataset`, `--seed`, and nothing that changes a result silently.
2. Reads only pinned state named in `datasets.jsonl`.
3. Writes `results.json` and `environment.json` and nothing else the writeup depends on.
4. Contains no number that is not computed, and — the direction that actually fails —
   **is itself the analysis path**. An analysis re-derived beside the production code
   path is a second implementation that can be wrong on its own, and has been.

## Reproducibility

The triple `(pinned dataset, pinned checkpoint, seed)` is necessary and not sufficient. A
seed reproduces a draw, not a result, and it does not constrain the environment or GPU
nondeterminism. `environment.json` captures interpreter, torch/CUDA/driver versions, and
the determinism flags in force. Where a result depends on deterministic kernels, say so
and set them; where it does not, say that too.

Always synchronize before timing CUDA work. Measured on the development box: an
unsynchronized timing understated a kernel by 173x, because it timed queue submission
rather than compute.

## Pre-registration

`preregistration.md` sections: Question -> What this replaces and why -> Hypothesis ->
Margin and its derivation -> Method -> Baselines and controls -> What would falsify this
-> Threats to validity.

It is committed **and pushed to the public remote** before the first run against real
data, and never edited after. The push is the point: a local commit date is written by
the machine that made it, so on a repo its author controls it is not an independent
timestamp. The remote's record of when it received the commit is.

Negative and null results are kept. A pre-registered hypothesis that fails must be able
to falsify the write-up's own text.

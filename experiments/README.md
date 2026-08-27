# experiments

The other genre. An experiment is written for a technical reader outside the project,
states what was committed to before the data was seen, and regenerates every number in
it from a pinned dataset state and a seed.

    experiments/
      datasets.jsonl           pinned dataset/mutation-stream registry (committed; the bytes are not)
      NNN-slug/
        preregistration.md     written first, committed before the first run, never edited after
        run.py                 regenerates results.json; no other inputs
        results.json           every number the writeup shows, machine-readable
        findings.md            the writeup

## The run.py contract

1. Takes `--dataset`, `--seed`, and nothing that changes a result silently.
2. Reads only pinned state named in `datasets.jsonl`. Never the live working tree of a
   dataset directory, never a checkpoint that is not named by hash.
3. Writes `results.json` and nothing else that the writeup depends on.
4. Contains no number that is not computed. If the narrative says local refresh wins,
   that sentence is generated from the comparison — a pre-registered hypothesis that
   fails must be able to falsify the page's own text.

## Reproducibility

A seed alone is not reproducibility. The triple is `(pinned dataset, pinned model
checkpoint, seed)`. Seeds are date-shaped literals (`SEED = 20260826`) and are threaded
as explicit parameters with local generators — no global `set_seed()` reaching into
library state from three call sites away.

`preregistration.md` sections: Question → What this replaces and why → Hypothesis →
Method → Baselines → What would falsify this → Threats to validity.

The manifest's rule governs: baselines are full recomputation, no refresh, and naive
local refresh. A comparison that omits full recomputation is not a result.

The git history of `preregistration.md` is its pre-registration timestamp. That is why
it is committed before the run and not edited after — an edited prereg is not a prereg,
and there is no way to tell from the file itself.

# The claims ledger

The ledger built on 2026-08-27 is quarantined at `archive/`. A quotation audit run the
same day — every entry whose frozen statement quotes a source, compared against the
source it names — found 23 of 47 quotations faithful and 24 defective. The full audit
is recorded inside the archived entries themselves, as appended verdicts, and the
archive's README states the defect classes and the quarantine rules. The headline rule:
**no new document may cite an entry in `archive/`.** An entry is carried forward only
by re-deriving it from its primary sources, when something needs it.

The failure being designed out is structural: a single frozen statement field fused a
quotation, an observation, the project's own reasoning, and the authority behind it
into one blob, so a faithful quote could continue seamlessly into unsourced inference
and be sealed there by the freeze. The replacement separates the four roles into
Assertion, Grounds, Warrant and Backing, holds every quotation to its source
mechanically, and derives status from an append-only verdict list. Research stays
halted until the first real entries are written against it.

## Layout

    ledger/
      archive/            the quarantined 2026-08 ledger: 56 entries, INDEX, its README,
                          and the two checkers that keep it well-formed as evidence
      corpus/             the red-team corpus: 55 seeds with committed expected outcomes,
                          synthetic fixtures, and run.py, the runner that holds the four
                          checkers to them
      schema.py           the entry parser, normalization, fingerprint and status
                          derivation the four checkers share
      validate.py  resolve.py  references.py  propagate.py
                          the four checkers, one job each (below)
      entries/            the new ledger's entries, `A####-slug.md` — none yet
      sources.jsonl       the source registry — one row per external source cited by an
                          entry: id, type, citation, retrieval date, sha256 of the text.
                          Committed; the bytes are not — none yet
      cache/              the bytes, keyed by sha256; gitignored

## The schema

The schema the seeds and checkers are written against is stated in
`corpus/README.md`, *The schema the seeds are written against*: one file per entry with
nanopublication-style parts (assertion, provenance, publication info), Toulmin's names
for the provenance roles (grounds, warrant, backing), typed pointers for every ground and
every piece of verdict evidence, a fingerprint over the verbatim record, citation acts
between entries, and statuses derived from verdicts and never stored. Where a checker
and that text disagree the checker is wrong, and the corpus is where the disagreement
is caught.

## The checkers

Four programs, each run as `python3 ledger/<name>.py`, each exiting non-zero on a
failure and zero on a flag (a report a human judges):

- `validate.py` — every entry is well-formed: ids, timestamps, the no-quotation-marks
  rule in Assertion, Scope at `measured` and above, grade–grounds consistency, the
  absence-claim rule, the verbatim fingerprint, verdict legality and authorship,
  supersession both ways, and — from git — immutability of the region above the APPEND
  marker and append-only verdicts over the whole history. `--cached` reads staged entries
  from the index, for the pre-commit hook.
- `resolve.py` — every pointer resolves to the artifact that established the fact, and
  every quotation is a contiguous span of the source it names, elisions marked; a
  consultation-type source's speaker is its expert, and a consultation sentence naming
  another registered author is flagged as relayed. A registry or cache miss is a failure
  that says the check could not run, never a silent pass. On a retracted entry the
  defect the verdict states must reproduce.
- `references.py` — citation acts are compatible with the target's current status,
  entry to entry and document to entry; document citations and entries' References
  sections agree both ways; no document cites an archived `C###`/`P###` id.
- `propagate.py` — a dependent of a fallen entry, and the target of a `challenges` act,
  carry the `contested` verdict by `propagation` that records why; `--write` appends the
  missing ones. It is the one place machinery writes into an entry.

They are proven, not trusted: `python3 ledger/corpus/run.py` runs all four over every
seed in `corpus/` and holds them to the committed expectations under the contract in
`corpus/README.md`. A checker is only as good as the seed that exercises it, and a
defect class found in practice gets a seed before it gets a fix. The runner is in the
test suite (`tests/test_corpus.py`), so `uv run pytest` is the pre-push check for the
machinery; the four checkers over the live ledger and the two archive checkers run in
the pre-commit hook and in the pre-push verification set.

What passing the corpus does not show is listed at the end of `corpus/README.md`.

The archive's own checkers stay live under `archive/`:

- `archive/validate.py` — the archived entries stay well-formed against the archived
  schema. The archive is evidence now, and evidence that drifts is worthless.
- `archive/references.py` — no document in the tree carries an unlisted verbatim copy
  of an archived claim, and any standing document still referencing a fallen claim is
  reported as work. A restatement in different words is invisible to it and is on the
  author to avoid.

## Naming, disclosed

`retracted` here means a defect in the making of an entry, not obsolescence without a
successor as in nanopublication usage; a refuted claim nobody replaced is `refuted`, not
`retracted`. `Assertion` is used in the nanopublication sense (the claim); SEPIO uses
the same word for the whole of proposition, agent and occasion. `Scope` is the domain
the claim holds over and is not Toulmin's qualifier, which is `credence`.

# The claims ledger

The ledger built on 2026-08-27 is quarantined at `archive/`. A quotation audit run the
same day — every entry whose frozen statement quotes a source, compared against the
source it names — found 23 of 47 quotations faithful and 24 defective. The full audit
is recorded inside the archived entries themselves, as appended verdicts, and the
archive's README states the defect classes and the quarantine rules. The headline rule:
**no new document may cite an entry in `archive/`.** An entry is carried forward only
by re-deriving it from its primary sources, when something needs it.

A replacement apparatus is being designed against the audit's defect classes. Research
is halted until it is proven; the failure being designed out is structural — a single
frozen statement field that fused a quotation, an observation, the project's own
reasoning, and the authority behind it into one blob, so a faithful quote could
continue seamlessly into unsourced inference and be sealed there by the freeze.

Two checkers remain live and guard the archive:

- `validate.py` — the archived entries stay well-formed against the archived schema.
  The archive is evidence now, and evidence that drifts is worthless.
- `references.py` — no document in the tree carries an unlisted verbatim copy of an
  archived claim, and any standing document still referencing a fallen claim is
  reported as work. This is the mechanical half of the quarantine rule; a restatement
  in different words is invisible to it and is on the author to avoid.

Both exit non-zero on violation and run in the pre-push verification set.

The replacement apparatus is being built test-first. `corpus/` is its proof bar: a
red-team corpus of seeds in the new schema — one or more for every defect class the
audit found, plus known-good seeds for every rule — with committed expected outcomes
the four new checkers must reproduce before anything in the new ledger is trusted.
`corpus/README.md` states the schema the seeds are written against and the runner's
contract. The checkers do not exist yet; the corpus does.

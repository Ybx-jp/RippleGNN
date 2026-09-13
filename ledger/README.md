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
Assertion, Grounds, Warrant and Backing, holds every quotation to its source, and
derives status from an append-only verdict list. The schema is stated in full below;
`claims-ledger` 0.0.1, the package that checks it, is the authority, and the
statement below is this repository's restatement of it.
The first entries were written against it on 2026-09-02, the chain a preregistration
of the stale-fraction law would draw on; the next preregistration is what earns more.

## Layout

    ledger/
      archive/            the quarantined 2026-08 ledger: 56 entries, INDEX, its README,
                          and the two checkers that keep it well-formed as evidence
      entries/            the ledger's entries, one file each, `A####-slug.md`
      sources.jsonl       the source registry — one row per external source an entry
                          cites: id, type, citation, author surnames where the source
                          names authors, retrieval date, sha256 of the text, and the
                          URL and extraction method that regenerate the bytes. Committed;
                          the bytes are not
      cache/              the bytes, keyed by sha256; not committed
      restore-cache.py    rebuilds cache/ from the registry, and names what it cannot
                          rebuild (below)

## How the rules are held

The checkers are `claims-ledger`, installed from PyPI and pinned exactly in this
repository's `dev` extra. It declares no runtime dependencies, so a reader who wants to
verify an entry needs `pip install claims-ledger==0.0.1` and nothing else, and runs the
same check this repository runs:

    claims-ledger check          # or: python3 -m claims_ledger check

The pin is exact rather than floated because a reader who cites an entry should be able
to run the check that held it, and a different checker version is a different check.
Moving the pin is a methodology change and is recorded as one. This repository's local
vocabulary — which documents may cite an entry, which id prefixes are quarantined — is
the `[tool.claims-ledger]` table in `pyproject.toml`.

Five checkers, each exiting non-zero on a failure and zero on a flag (a report a human
judges):

- `validate` — every entry is well-formed: ids, timestamps, the no-quotation-marks
  rule in Assertion, Scope at `measured` and above, grade–grounds consistency, the
  absence-claim rule, the verbatim fingerprint, verdict legality and authorship,
  supersession both ways, and — from git — immutability of the region above the APPEND
  marker and append-only verdicts over the whole history.
- `resolve` — every pointer resolves to the artifact that established the fact, and
  every quotation is a contiguous span of the source it names, elisions marked; a
  consultation-type source's speaker is its expert, and a consultation sentence naming
  another registered author is flagged as relayed. A registry or cache miss is a failure
  that says the check could not run, never a silent pass.
- `references` — citation acts are compatible with the target's current status,
  entry to entry and document to entry; document citations and entries' References
  sections agree both ways; no document cites an archived `C###`/`P###` id.
- `propagate` — a dependent of a fallen entry, and the target of a `challenges` act,
  carry the `contested` verdict by `propagation` that records why; `--write` appends the
  missing ones. It is one of the two places machinery writes into an entry.
- `freshness` — every ground still names the artifact the claim was established on: the
  path is in the tree and the digest of its pinned section matches the anchor, read out
  of the commit a `@<commit>` anchor names. A ground that has moved is flagged and the
  claim is re-judged by a person; `--write` appends the missing `contested` verdicts.

They are proven, not trusted: `claims-ledger corpus` runs all five over a red-team
corpus of 95 seeds with committed expected outcomes — one per defect class the archived
ledger exhibited, plus one per rule the schema creates, plus known-good seeds every
checker must leave alone — and holds them to the contract in the corpus's own README.
The contract is symmetric: a seed passes when every expected failure is produced at the
named place and no checker trips where the seed does not say it should. A run that
checked nothing exits non-zero rather than reporting a clean run over nothing.

Until 2026-09-13 the checkers and a 62-seed corpus were vendored under `ledger/` and run
as `python3 ledger/<name>.py`. They are now the package, whose corpus is a superset of
the vendored one: every one of the 62 seed names is present, with expectations that have
moved in places, and 33 seeds are new. Numbers already in the ledger are unaffected —
all five checkers pass over all 33 entries unchanged — but the corpus is a different
fixture, so a claim about what the checkers catch is a claim about the 95-seed corpus
from this date on.

### A fresh clone has no source bytes

The registry rows are committed and the bytes they name are not, so a fresh clone fails
`resolve` once per quotation until the bytes are back. `python3 ledger/restore-cache.py`
puts back the ones that can be put back, from each row's `url` and `extraction`, and
holds every result to the row's `sha256` before writing it. `--check` reports without
writing. Regenerated bytes whose digest does not match the row are dropped rather than
written: the cache is keyed by that digest, so storing different bytes under it would
make every later check read the wrong source. A mismatch means a toolchain that differs
from the one the row names, and the fix is to match it — a quotation checked against a
different extraction of the same document is a different check.

Three of the six rows regenerate exactly: both arXiv papers, through `pdftotext 24.02.0
(poppler)` in default mode, and the pinned PyTorch Geometric file, read out of the
environment `uv sync --extra dev` installs.

**Three do not, and cannot.** The consultation transcripts `consult-dl-r3`,
`consult-dl-r4` and `consult-eval-r4` were received rather than fetched: they have no
url, and their bytes exist only where they were received. Their text is also not
publishable as it stands — it cites its own working memory by machine identifier
throughout, which this repository does not carry — and the bytes are held to a sha256 by
every quotation that names them, so a redacted copy would be a different source rather
than a censored one. The consequence is stated rather than worked around: **a reader
outside this checkout cannot check the quotations in A0013 and A0030**, and
`restore-cache.py` names those two entries rather than leaving a bare cache miss to be
interpreted. A0013 is superseded; A0030 is open, and is the live entry the limit falls
on. The other 31 entries resolve fully against sources anyone can regenerate.

The archive's own checkers stay live under `archive/`, and are not part of the package:
they hold the quarantined 2026-08 format, which the package does not read.

- `archive/validate.py` — the archived entries stay well-formed against the archived
  schema. The archive is evidence now, and evidence that drifts is worthless.
- `archive/references.py` — no document in the tree carries an unlisted verbatim copy
  of an archived claim, and any standing document still referencing a fallen claim is
  reported as work. A restatement in different words is invisible to it and is on the
  author to avoid.

What a mechanical check does not show is stated at the end of this document.

## The schema

The names are Toulmin's, in Verheij's (2005) formalization: assertion, grounds,
warrant, backing; the three-part split into assertion, provenance and publication info
is the nanopublication model (Kuhn et al. 2021); *challenges* is micropublications'
relation (Clark, Ciccarese and Goble 2014).

**One file per entry**, `entries/A####-slug.md`. Ids are a letter and exactly four
digits; the letter rolls over (`B0001`) when a series is exhausted and skips `C` and `P`,
which are the archived prefixes. A citation of a `C###` or `P###` id anywhere in the
tree is a quarantine breach by prefix alone.

**Frontmatter** (publication info): `id`, `kind` (`claim` | `prediction` |
`hypothesis`), `stated` (ISO 8601 to the second with a UTC offset; a bare date is
malformed), `author` (`main` or an expert scope), `grade` (`asserted` | `argued` |
`measured` | `controlled` | `preregistered`), `credence` and `resolves_when` (required
for predictions and hypotheses, omitted otherwise, never guessed), `supersedes` (`none`
or an id), `verbatim_sha`, and optionally `verbatim_change` with a reason.

**Sections**, in order: Assertion, Scope, Grounds, Warrant, Backing, then the line
`<!-- APPEND BELOW THIS LINE ONLY -->`, then Verdicts and References.

- *Assertion* is the claim in the project's words. **No quotation mark may appear in
  it.** Every fusion of quote and inference in the archived ledger lived inside quotation
  marks in a statement blob; the seam between source words and project words is
  structural here, not typographic.
- *Scope* is three lines, `metric:`, `cohort:`, `condition:`, required at `measured` and
  above. An assertion claims exactly its scope.
- *Grounds* are typed pointers, one per line:
  `lab: <path> § "<section>" @<commit>` · `experiment: <path> @<commit>` ·
  `entry: <id> · <act>` · `source: <registry id> · <locator>` ·
  `search: corpus=…; query="…"; date=…`. An absence claim carries a `search:` ground
  instead of a positive pointer. The citation acts are `cites-as-live` (target open or
  corroborated), `cites-as-contested` (target contested), `cites-as-fallen` (any
  status; the only act legal against a fallen target), and `challenges` (target open,
  corroborated or contested; the citing entry's Warrant names what it attacks). A
  ground is a datum the Warrant uses; an artifact the entry mentions without resting on
  it is named in the Warrant's prose, or cited `cites-as-fallen` if it is an entry, and
  is not a ground. A `measured` or higher grade requires a `lab:` or `experiment:`
  ground, and an `asserted` grade forbids one: the grade is the type of the evidence.
- *Warrant* states the rule by which the grounds support the assertion. Conditions on the
  rule are Scope lines, not Warrant sentences.
- *Backing* holds every verbatim quotation, one block per quote: `source:` (a registry
  id and locator), `speaker:` (the text's author), `quote:`. A consultation-type source
  may back only the expert's own judgment; a result the expert attributes onward resolves
  to the primary source or not at all.
- *Verdicts* append and only append. One row each:

      - <timestamp> · <status> · grade: <grade of the evidence> · author: <main | propagation>
        evidence: <typed pointer, held to the same resolution bar as Grounds>
        note: <optional>

  Verdict evidence adds two pointer forms Grounds do not have: `entry: <id> · fallen`,
  `· challenges` or `· supersedes` names the entry whose fall, challenge or succession
  moved this one; `defect: <description>` is legal only on a `retracted` verdict and
  names the making-defect. Timestamps are non-decreasing down the file and none is
  earlier than `stated`. **Who may write a verdict is checked:** `author:` is `main` or
  `propagation` and nothing else — an expert scope writes none, because a consultation is
  evidence a verdict points at — and a `propagation` verdict must carry `entry:` evidence
  with `· fallen` or `· challenges`, since those are the only two things the machinery
  writes about. An assertion is a proposition made by an agent on an occasion; `author`
  and `stated` are the agent and the occasion, and a verdict under the wrong agent is
  malformed whatever it says.
- *References* lists the documents (not entries) that cite this entry:
  `- <path> · standing | record · <act>`. Entry-to-entry edges are read from Grounds and
  are not repeated here. A document cites an entry inline as `(A0007-slug, cites-as-live)`,
  and the two views are checked against each other both ways, so a status still lives in
  exactly one place: the act a document declares is held to the entry's current status at
  every check, and a copied id cannot go stale silently.

**Hypotheses.** A `kind: hypothesis` entry is a prediction whose `resolves_when` is an
experiment design. It carries at least one `entry:` ground naming the claims motivating
it, and its Warrant states what would falsify it; the falsifier rule is a heuristic on
wording, any word beginning `falsif`, stated so a reader knows what is and is not
caught. Every hypothesis whose status is not terminal has exactly one row in
`experiments/ROSTER.md`, a hand-maintained view a preregistration author reads: the
row's first cell cites the entry and its last cell states its status, and the reference
check holds both to the entry. The roster is not generated, so it is checked.

**The quote grammar.** A `quote:` value is one or more quoted spans separated by `[…]`,
optionally beginning or ending with `[…]`. Each span must be a contiguous substring of
the named source, spans appear in source order, and a span that starts or ends inside a
sentence must have the elision mark on that side. Comparison is made after the same
normalization the fingerprint uses (below); anything that survives it must match.

**`verbatim_sha`** is a fingerprint over the verbatim record: sha256 over the Scope
lines, then a blank line, then one line per Backing block, with the blocks sorted. A
Scope line or a Backing block is normalized before hashing: Unicode NFC, the markdown
emphasis markers `*` and backtick removed, whitespace collapsed to single spaces, blank
Scope lines dropped. A Backing block's line is its `source:`, `speaker:` and `quote:`
values joined by ` | ` — attribution is part of the verbatim record, so a quote moved to
a different source or a different speaker changes the fingerprint. A quote is one line.
Grounds are excluded. The value is recomputed at check time and a declared value that
differs is malformed. Across a supersession chain the value must be equal unless the
successor declares `verbatim_change` with a reason; reordering Backing blocks, changing
emphasis or whitespace, or writing an accented word in another normalization form
changes nothing. Resolution applies the same normalization when it matches spans, so
the two never disagree about what a change is. The fingerprint is not an integrity key;
the integrity key over a whole entry is its git blob at the commit that created it,
which is what the immutability check diffs against. Its job is the inverse of the
fingerprint in Kuhn et al. (2017): there, unequal fingerprints trigger a new version;
here, equal fingerprints are what a chain must preserve.

**Immutability.** The region above the APPEND marker never changes after the commit
that created the entry, and a verdict once committed is never edited or removed. Both
are properties of history, not of a file, and are checked against git over the whole
history, so a commit that bypassed the check is caught by the next run anywhere.

**Statuses** are derived from the last verdict, never stored: `open` (no verdicts),
`corroborated`, `contested`, `refuted`, `superseded`, `retracted`, `non-comparable`. The
last four are terminal, with one exception: `refuted` or `non-comparable` may be
followed by exactly one `superseded`, because reinstatement is supersession. A
corroborating verdict must point at a ground the entry does not already cite. A
`refuted` verdict whose evidence grade differs from the entry's is flagged for a
human, since evidence types are not ranked. `non-comparable` is legal only at
`measured` and above. `retracted` here means a defect in the making, not obsolescence
without a successor as in nanopublication usage. On a retracted entry the defective
quote is not re-reported; instead the `defect:` the verdict states must reproduce, and
a retraction whose stated defect does not is flagged — a retraction for a defect that
is not there is itself the defective act. Supersession is a chain, not a tree: an entry
carries one `superseded` verdict, so a second successor is malformed, and a
`superseded` verdict naming a successor that does not declare `supersedes:` is
malformed too.

**Sources.** Every `source:` pointer names a row in `sources.jsonl`, and the row's
sha256 names the bytes a quotation is checked against. A registry row without its
bytes, or a pointer without its row, is a failure that says the check could not run —
never a silent pass. A consultation-type source's speaker is its expert; a sentence in
such a source that names another registered author is flagged as relayed.

**Propagation** is the one place machinery writes into an entry. When an entry cited
`cites-as-live` falls, or an entry is named by a `challenges` act, a `contested` verdict,
`author: propagation`, is appended to the dependent or challenged entry, and the flag
is reported until a human re-verdicts. A `challenges` act whose target lacks that
verdict, or whose target is fallen, is a failure, and so is a `propagation` verdict
whose named cause does not exist. A dependent flagged because its live-cited ground
fell cannot return to `corroborated`: its Grounds are immutable and still cite the
fallen entry, so the reference check keeps failing until it is superseded; once it has
fallen itself, its Grounds are history, exempt from the act check, and it needs no
further flag, since a verdict after a terminal status is illegal. A document
that cites an entry `cites-as-live` after the entry is superseded or refuted fails the
same way; the filter a reader must apply every time is applied for them at check time.

**Two rules are heuristics**, stated so a reader knows what is and is not caught:

- An Assertion is read as an absence claim, and must carry a `search:` ground, when it
  contains one of the standalone words `nobody`, `no one`, `neither`, `first`, `novel`,
  `unique`, `unprecedented`, the phrase `not found`, or the standalone word `no` followed
  within the sentence by `has`, `have`, `was`, `were`, `report` or `reports`. Words are
  whitespace-delimited: `no-refresh` is a baseline's name and contains no `no`. A
  priority word is an absence claim about everyone else, which is why the project's
  conventions forbid it without a search on record. A false positive costs a `search:`
  line; a false negative is the archived defect. Known miss: an absence stated without any
  of these tokens (`lacks`, `remains open`, `unreported`).
- A quote from a consultation-type source is flagged as relayed third-party material when
  the source sentence containing the span also contains a surname from another registry
  row's `authors` or the token `et al.`. Title words are not used: a consultation about
  mean aggregation would name every paper about mean aggregation. This is a flag for
  review, not a failure; the failure case is a consultation source whose `speaker:` is
  not its expert. Known miss: a relay by pronoun in a sentence that names nobody.

## What a mechanical check does not show

- That a quotation is *true*, or that its source is the right one. Resolution shows a
  span exists in the named artifact and nothing more.
- That a load-bearing elision, an undercut recorded as a refutation, an attack on a
  datum recorded as a refutation, a distortion by reversal, a widened scope, or a chain
  with no empirical base is classified correctly. The machinery can make each of those
  visible; the classification is a human's, recorded as a verdict, and an entry the
  checks pass is not thereby right.
- That a defect class not seeded is caught. The seeded classes are the ones the
  archived ledger actually exhibited plus the ones this schema's own rules create. The
  corpus is the package's now, so a class found in practice here gets its seed upstream
  in `claims-ledger` before it gets a fix there, and this repository picks the fix up by
  moving its pin — which is a methodology change and recorded as one.

## Naming, disclosed

`retracted` here means a defect in the making of an entry, not obsolescence without a
successor as in nanopublication usage; a refuted claim nobody replaced is `refuted`, not
`retracted`. `Assertion` is used in the nanopublication sense (the claim); SEPIO uses
the same word for the whole of proposition, agent and occasion. `Scope` is the domain
the claim holds over and is not Toulmin's qualifier, which is `credence`.

# The red-team corpus

The proof bar for the replacement claims apparatus. Nothing in `ledger/` is trusted to
check anything until it passes this corpus, and the corpus was written before the
checkers existed: the test precedes the thing tested.

Why a corpus and not a sample rebuild: the archived ledger's audit (`../archive/README.md`)
found 24 of 47 quotations defective, in nine classes, and two of the probes written to
audit it were themselves wrong — one exhausted a generator before the check ran and
reported zero matches, another would have reported 11 misattributions where 8 were a
backtick difference. A verifier is trusted only after it has passed a known-positive and
a known-negative, so every defect class here has a seed the checkers must catch, and
every rule has a known-good seed the checkers must not catch.

Seeds and their expected outcomes are committed and re-run on every change to a checker.
A checker change that makes a seed's outcome move is a methodology change and is recorded
as such in the commit that makes it.

## Layout

    corpus/
      fixtures/            synthetic sources the seeds quote: two papers, one consultation,
                           three lab notes. Every fixture says in its first lines that it
                           is synthetic; the authors named in them are fictional.
      sources.jsonl        the registry rows for the fixtures — id, type, citation,
                           retrieval date, sha256 of the bytes, and (only here) the path
                           of the bytes, because fixtures are committed and real sources
                           are not
      seeds/
        K##-slug/          known-good: every checker must pass
        D##-slug/          defect: the named checker must fail or flag at the named place
          expected.json    class, known_good, and the expectation rows
          entries/         the ledger entries of this seed, as they would sit in ledger/entries/
          docs/            any citing documents the seed needs
          commits/01, 02   history seeds only: successive states to apply as commits;
                           a state after 01 may be deliberately tampered

Seeds are independent. Each is checked as if its `entries/` and `docs/` were the whole
ledger, with `sources.jsonl` and `fixtures/` shared from the corpus root. Ids repeat
across seeds (most seeds have an `A0001`) and mean nothing outside their seed.

## What `expected.json` says

    {"class": "unmarked deletion", "known_good": false, "expect": [
      {"checker": "validate", "outcome": "pass", "where": "all", "why": "well-formed"},
      {"checker": "resolve",  "outcome": "fail", "where": "A0001 Backing quote 1",
       "why": "the quote drops the parenthetical (cosine, L2) with no elision mark"}]}

`checker` is one of `validate`, `resolve`, `references`, `propagate` — the four programs
that will live beside this directory — or `review`, which is not a program. `outcome` is
`pass`, `fail`, `flag`, or `judge`. `where` names an entry and a part of it so a runner
can match the checker's report to the row. `why` is for the reader.

The runner's contract, so it is fixed before the runner exists:

- A seed passes when every `fail` and `flag` row is produced by the named checker at the
  named place, **and every checker not named in a non-pass row exits clean.** The second
  half is the known-negative: a defect seed that trips a checker the row does not name is
  a runner failure, not a bonus catch, because either the seed has a defect its author did
  not see or the checker has a false positive. Both are findings.
- `fail` means exit non-zero and a report naming the place. `flag` means exit zero with a
  report naming the place: the checker has made something visible and a human decides.
  `pass` means neither.
- `review` rows carry no obligation for the machinery. They record what the correct human
  verdict is once the machinery has made the defect visible, and they exist so a later
  reader can tell a seed the checkers are meant to *catch* from one they are meant to
  *surface*. The row before a `review` row states the visibility the machinery does owe.
- History seeds (`commits/`) are applied as successive commits in a fresh repository, and
  their rows name the commit they apply to. They are the only way to test immutability,
  since immutability is a property of history and not of a file.

## The schema the seeds are written against

The full schema lands in `../README.md` with the checkers. What follows is what the seeds
depend on, so the corpus is readable on its own. The names are Toulmin's, in Verheij's
(2005) formalization: assertion, grounds, warrant, backing; the three-part split into
assertion, provenance and publication info is the nanopublication model (Kuhn et al.
2021); *challenges* is micropublications' relation (Clark, Ciccarese and Goble 2014).

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
  `search: corpus=…; query="…"; date=…`. In this corpus the pin is `@corpus`, because
  fixtures are not at a commit. An absence claim carries a `search:` ground instead of a
  positive pointer. The citation acts are `cites-as-live` (target open or corroborated),
  `cites-as-contested` (target contested), `cites-as-fallen` (any status; the only act
  legal against a fallen target), and `challenges` (target open, corroborated or
  contested; the citing entry's Warrant names what it attacks).
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
  earlier than `stated`.
- *References* lists the documents (not entries) that cite this entry:
  `- <path> · standing | record · <act>`. Entry-to-entry edges are read from Grounds and
  are not repeated here.

**The quote grammar.** A `quote:` value is one or more quoted spans separated by `[…]`,
optionally beginning or ending with `[…]`. Each span must be a contiguous substring of
the named source, spans appear in source order, and a span that starts or ends inside a
sentence must have the elision mark on that side. Whitespace differences and markdown
emphasis are ignored; everything else is not.

**`verbatim_sha`** is sha256 over: the Scope lines stripped of surrounding whitespace with
blank lines dropped, joined by newlines; then a blank line; then each `quote:` value with
its whitespace collapsed to single spaces, in Backing order, joined by newlines. Grounds
are excluded. `validate.py` recomputes it and a declared value that differs is malformed.
Across a supersession chain the value must be equal unless the successor declares
`verbatim_change`. It is a fingerprint over the verbatim record, not an
integrity key; the integrity key over a whole entry is its git blob at the commit that
created it, which is what the immutability check diffs against.

**Statuses** are derived from the last verdict, never stored: `open` (no verdicts),
`corroborated`, `contested`, `refuted`, `superseded`, `retracted`, `non-comparable`. The
last four are terminal, with one exception: `refuted` or `non-comparable` may be
followed by exactly one `superseded`, because reinstatement is supersession. A
corroborating verdict must point at a ground the entry does not already cite.
`non-comparable` is legal only at `measured` and above. `retracted` here means a defect
in the making, not obsolescence without a successor as in nanopublication usage.

**Propagation** is the one place machinery writes into an entry. When an entry cited
`cites-as-live` falls, or an entry is named by a `challenges` act, `propagate.py` appends
a `contested` verdict, `author: propagation`, to the dependent or challenged entry and
exits non-zero so the flag is seen. A `challenges` act whose target lacks that verdict,
or whose target is fallen, is a failure. A dependent flagged because its live-cited
ground fell cannot return to `corroborated`: its Grounds are immutable and still cite the
fallen entry, so `references.py` keeps failing until it is superseded.

**Two rules the seeds assume are heuristics**, and they are stated here so a checker
author implements what the seeds test rather than something stronger:

- An Assertion is read as an absence claim, and must carry a `search:` ground, when it
  matches a negated-existence pattern: `nobody`, `no one`, `not found`, `neither`, or
  `no <words> (has|have|was|were|report|reports)`. A false positive costs a `search:`
  line; a false negative is the archived defect.
- A quote from a consultation-type source is flagged as relayed third-party material when
  the source sentence containing the span also names another registry row (a surname or a
  title word from its `citation`) or contains `et al.`. This is a flag for review, not a
  failure; the failure case is a consultation source whose `speaker:` is not its expert.

## Coverage

Each archived defect class has at least one seed. The right column is the honest limit:
`catch` means the checker fails; `surface` means it flags and a human judges.

| class | seeds | machinery owes |
|---|---|---|
| unmarked deletion | D01 | catch (span not contiguous) |
| paraphrase inside quotation marks | D02 | catch |
| text no source contains, including reversal | D03 | catch |
| right quote, wrong source | D04 | catch |
| dead pointer | D05 | catch, loudly — a cache or registry miss never passes silently |
| mid-sentence cut without `[…]` | D06 | catch |
| fusion of quote and inference | D07 | catch (no quotation marks in Assertion) |
| grade inversion | D08 | catch (grade–grounds lookup, both directions) |
| absence-scope widening | D09, K04 | catch the missing `search:`; the widening itself is review |
| speaker misidentified | D10 | catch the structural case; surface the relayed case |
| load-bearing elision | D11 | surface — the elision is marked and visible; load is judged |
| refuted on weaker evidence | D12 | surface |
| undercut recorded as refuted | D13 | review only — the corpus records the correct verdict |
| challenge without its flag | D14, K07 | catch |
| act incompatible with target status | D15, D16 | catch |
| verdict after a terminal status | D17, K06 | catch |
| malformed or non-monotonic timestamps | D18 | catch |
| prediction without credence or resolves_when; credence out of range | D19, K02, K03 | catch |
| id width, archived prefix, archived-id citation | D20 | catch |
| verbatim drift across a chain | D21, K05 | catch |
| supersession without the predecessor's final verdict | D22 | catch |
| frozen region edited after creation | D23, K09 | catch (history) |
| verdict line modified | D24 | catch (history) |
| corroborated by its own grounds | D25 | catch |
| non-comparable below measured | D26 | catch |
| references not two-way consistent | D27 | catch |
| challenge against a fallen target | D28 | catch |
| measured claim with an incomplete Scope | D29 | catch |
| declared `verbatim_sha` does not match the content | D30 | catch |

Known-good seeds K01–K09 cover: a measured claim, a prediction, a hypothesis with a
falsifier, an absence claim with its search, a supersession chain, reinstatement by
supersession, a challenge with its propagated flag, an asserted claim on backing alone,
and a verdict appended in history.

## What passing this corpus does not show

- That the checkers catch a defect class not seeded here. The classes are the ones the
  archived ledger actually exhibited plus the ones the schema's own rules create; a new
  class found in practice gets a seed before it gets a fix.
- That a quotation is *true*, or that its source is the right one. Resolution shows a
  span exists in the named artifact and nothing more.
- That the load-bearing elision, the undercut, or the widened absence are classified
  correctly. Those rows say `surface` and `review` because the machinery can only make
  them visible, and a row claiming otherwise would be a fifth thing that says it is
  checked and is not.

# The claims ledger — QUARANTINED 2026-08-28

**This directory is a frozen archive. No new document may cite an entry in it.**

On 2026-08-27 every entry whose frozen statement carries a quotation was compared
against the source it names: of 47 quotations, 23 were faithful and 24 defective —
unmarked deletions, paraphrase inside quotation marks, misidentified speakers, elisions
that removed the condition a sentence depended on, and six statements whose quoted text
appears in no named source. The audit is recorded entry by entry, as appended verdicts;
no statement was rewritten, so the defective text and its correction are both on the
page. A quotation mark in this archive carries no information about faithfulness — the
split is a coin flip — which is why the archive is closed rather than repaired.

The rules for this directory:

- **Nothing here is edited**, including the defective entries. Their defects are ground
  truth for testing the replacement apparatus.
- **No new document may cite or copy an entry here.** `ledger/references.py` enforces
  the verbatim half of this mechanically; restatements in different words are on the
  author.
- **References recorded before the quarantine stay recorded** in each entry's
  References section. They are history, not endorsements.
- An entry is carried forward only by re-deriving it into the replacement ledger from
  its primary sources, when something actually needs it — never by a bulk migration.

The document below is the methodology the archive was written under, kept because the
archive is not readable without it. It describes the archived apparatus, not the
current one.

---

# The claims ledger (archived methodology)

Public. For a discovery project the claims methodology is part of the product, so this
file and the ledger it describes are published with the research. A preregistration still
carries a hand-written digest rather than a pointer, because a prereg has to be readable
without this directory.

Grounded 2026-08-27 in nine documents: ECO, SEPIO, Micropublications, two
nanopublication papers, an argument-mining survey, GRADE, Nosek et al. on
preregistration, and Gneiting & Raftery on proper scoring rules. Quotations below are
from those sources; the working notes that collected them are not published.

## Why this exists

Three statements in this project were written in ordinary declarative voice and later
overturned: that 4 CPU cores rather than VRAM were the binding constraint (never
measured), that the VRAM ceiling was roughly 1-2M nodes (measured, but at mean degree 10,
and it named the wrong variable), and a prediction held at 78% that k-hop refresh
degenerates on heavy-tailed graphs (threatened by mean aggregation making per-neighbour
error degree-invariant).

None of the three was marked as what it was. An unexamined premise and a measurement sat
in the same paragraph in the same voice, and nothing in the format told them apart.

The second case is the instructive one. It *was* measured. What it lacked was a record of
the conditions the measurement held under, so a number true at mean degree 10 was read as
a number about nodes. That is why the evidence locator below is required rather than
encouraged.

## Prior work

**An evidence vocabulary and a claim representation are separate artifacts.** ECO comprises
"two root (upper-level) classes, 'evidence' and 'assertion method'", and states of itself
that "ECO can not be used to make an assertion itself — for that, one would use some other
means" (ECO development site). That kills adopting ECO as the ledger
and is why this design keeps a grade vocabulary distinct from the claim file.

**Separating strength of evidence from strength of conclusion is standard, and failing to
separate them is treated as a defect.** GRADE: "Not all grading systems separate decisions
regarding the quality of evidence from strength of recommendations. Those that fail to do
so create confusion", and "High quality evidence doesn't necessarily imply strong
recommendations, and strong recommendations can arise from low quality evidence"
(Guyatt et al., BMJ 2008). The two-axis decision is a *convergence*
on GRADE, not an extension.

**Grade is set by design and then moved by execution, in that order.** GRADE starts RCTs at
high and observational studies at low, then applies five downgrade factors — one of which
is literally "Study limitations" — and three upgrade factors
(Guyatt et al., BMJ 2008). This answers the open question the
consultation was minted for: the discriminator is not evidence *type* alone, it is design
class first and execution quality second. GRADE also defines its rungs by expected
revision ("Further research is very unlikely to change our confidence in the estimate of
effect"), which transplants directly, and concedes that "some arbitrariness will therefore
be associated with placing particular recommendations in categories".

**Supersession links forward from the replacement, and the superseded version is not
rewritten.** Nanopublication practice: "we can furthermore establish supersedes links to
the respective previous versions … It is important to note that the previous version
remains untouched" (Kuhn et al., ISWC 2017). Immutability there is
cryptographic rather than conventional — content-addressed Trusty URIs mean an edit
necessarily mints a new identifier.

That source also names a hazard this design deliberately diverges from: "by starting from
the URI of the previous version and follow its links, the existence of the new version is
not even noticed." A reader arriving at the old version sees no signal it was replaced.
This ledger writes a final verdict onto the superseded entry for exactly that reason, so
supersession is discoverable backwards as well as forwards.

**Claims, evidence, and the argument between them are separate objects.** The
Micropublications model roots a DAG at a Claim, where "a Representation supports or
challenges other Representations", qualification is a separate mechanism rather than a
third relation, and Attribution distinguishes asserting a claim from formalizing it — with
the caution that "Attribution alone is weak support". This ledger's verdicts are the
`supports`/`challenges` edge, flattened to a list because a single-operator project does
not need the DAG.

**Proper scoring rules are what make a stated credence honest.** "A scoring rule is proper
if the forecaster maximizes the expected score … It is strictly proper if the maximum is
unique" (Gneiting & Raftery, JASA 2007), and the goal is to "maximize the
sharpness … subject to calibration". Skill scores are noted as generally improper, so they
are not used here.

**Not found in this scan:** any prior art attaching a credence to a *persistent claim node*
and scoring it later. Forecasting practice scores predictions; claim registries type
assertions; nothing retrieved joins the two. That join is the part of this design with no
citation behind it, and it is stated as a question rather than a contribution.

## What earns an entry

Two populations, kept separate because they resolve differently.

**Claims** — anything something downstream depends on: a design decision, an experiment
arm, another claim. A statement nothing depends on is not load-bearing and stays as prose
in a lab note. If something comes to depend on it later, that is when it gets an entry.

**Predictions** — every statement an expert consultation made that carried an explicit
confidence, and every pre-run hypothesis of our own.

Note the asymmetry already present: every numeric confidence in this project so far came
from `dl`. Both `eval-methodology` tickets carried rankings and corrections but no
probabilities. A calibration record built today measures one advisor and is blind to the
other, and the fix is to ask for numbers in the ticket, not to impute them afterwards.

## The two axes

Grade and credence are separate fields and are never combined into a score. Well-
established and strongly-believed are different properties, and the failure this ledger
exists to prevent came from a claim that was weakly established and confidently written.

**Grade** — how the claim was established. Ordinal, and a lookup rather than a judgment
call: the grade follows from what was done.

| grade | means |
|---|---|
| `asserted` | stated with no supporting evidence. A postulate. |
| `argued` | reasoned from a mechanism, or cited from literature, but not measured here |
| `measured` | measured on this box, one configuration, no controls |
| `controlled` | measured with the controls the experiment contract requires: falsifier arm, positive control, chance-corrected null, seed-variance floor |
| `preregistered` | produced by a run against a pushed, signed preregistration |

The first two rungs are design class in GRADE's sense — what kind of thing this is before
anyone asks how well it was done. The last three are the same design class (a measurement
on this box) separated by execution quality, which is GRADE's downgrade axis. Five rungs
against GRADE's four is a choice, not a finding; the extra rung exists because
`asserted` and `argued` are the two states the overturned postulates were actually in, and
collapsing them would hide the distinction this ledger was built to draw.

**Credence** — what we would bet, in [0, 1]. Required on predictions and on pre-run
hypotheses. Omitted, not guessed, on claims that are not bets. Frozen at write; a changed
belief is a new entry, not an edit.

## The evidence locator

Every entry at grade `measured` or above carries a locator naming, at minimum:

- **metric** — what was measured, in units
- **cohort** — the dataset, graph, or configuration it was measured on
- **condition** — the parameter values held fixed, especially the ones not being varied

`1-2M nodes` would have been written `metric: peak VRAM at OOM; cohort: synthetic uniform
random graph; condition: mean degree 10, hidden dim 128, 2-layer GraphSAGE` — and the
degree assumption would have been on the page where the next reader could see it.

A locator is not optional at those grades. An entry without one is malformed.

## File format

One file per claim, at `ledger/claims/<id>.md`. Ids are `C###-slug` for claims and
`P###-slug` for predictions, zero-padded, sequential, never renumbered or reused.

```markdown
---
id: C007-vram-ceiling-is-an-edge-count
kind: resource-model
grade: measured
credence:
stated: 2026-08-27
author: main
locator:
  metric: peak VRAM at OOM, GiB
  cohort: synthetic uniform random graphs, one SAGEConv layer
  condition: hidden dim 128; varies edges 5M-20M
supersedes: C003-vram-ceiling-is-a-node-count
---

## Statement

Full-graph message passing materializes a tensor per edge, so the VRAM ceiling is
governed by edges x hidden_dim at ~0.51 GiB per million edges per 128 dims, arriving
between 15M and 20M edges at 128 dims.

### Quotation provenance: the `quotes:` field

Measured 2026-08-27, on the four entries whose broken evidence chains were resolved to a
primary source: **four of four state more than the source they quote.** One dropped the
source's scope qualifier, one transposed the source's structure and pinned a constant the
source does not give, and two quoted exactly and then continued — inside the same pair of
quotation marks — into a consequence the source never draws. A `## Statement` that fuses a
quotation with this project's own inference is sealed by the freeze, and nothing fired at
write time to stop it, because the existing splitting rule fires at verdict time on a
*status* divergence, not at write time on a *provenance* one.

An entry whose statement contains a quotation carries `quotes:` in its frontmatter:

```yaml
quotes: "Grounding Representation Similarity with Statistical Testing" (arXiv 2108.01661)
quotes: unverified: <what has not been checked against the source>
```

`unverified:` is legal and does not fail the check, on exactly the reasoning that makes
`evidence: unresolved:` legal: a recorded gap is traceable and a silent one is the failure
the field exists to prevent. Failing on it would push an honest gap back into a fabricated
citation.

**Existing entries are not migrated.** The frontmatter is inside the frozen region, so
adding the field to the 52 backfilled entries would mean editing text the ledger promises
never to edit, and the promise is worth more than the uniformity. They are unverified by
default and `validate.py` reports how many. An entry gains the field when something else
already requires it to be superseded — supersede on contact, never a sweep. The count is
expected to fall slowly and to stay non-zero for a long time; that is the honest state and
not a defect to be tidied away.

**What this does not fix.** The fusion is authored upstream, where a claim is first
written down, and this field detects it at the last seam rather than preventing it at the
first. It buys a number for how much of the ledger has been checked against its sources —
which was previously unknown and unaskable — and it buys nothing else.

## Depends on this

- experiments/ dataset admissibility band
- lab/004 interpretation

<!-- FROZEN ABOVE. Everything above this line is written once and never edited. -->

## Verdicts
```

Everything above the marker is written once. Nothing edits it, including the author,
including to fix a typo. Everything below appends.

A verdict is one row with three required parts:

```markdown
- **2026-08-27** · `corroborated` · grade `measured`
  - evidence: `lab/004` — peak VRAM at 5/10/15/20M edges, 128 dim
  - read-in: `lab/claims-inventory-draft.md`
  - note: ceiling between 15M and 20M edges.
```

**`evidence` is what bears on the claim. `read-in` is where it was encountered.** They are
different and collapsing them destroys traceability: the first backfill of this ledger had
all 54 verdicts attributing to the inventory they were read in, and one citation chain
degraded across four hops until nothing but an unresolvable identifier remained.

Where the chain genuinely breaks, `evidence: unresolved: <reason>` is legal and does not
fail the check. A recorded broken link is traceable — you know exactly where it broke —
while a silent one is the failure the rule exists to prevent. Failing on it would push an
honest gap back into a fabricated citation or a deletion, which is what happened once.
`evidence: none found: <the search that found nothing>` is a different and legitimate
state: an absence claim, sourced to a search whose scope and date are on record.

The verdict carries the grade of the evidence that moved it. That is the answer to "can a
cheap probe refute a claim": yes, and the record says a probe did it. The risk this leaves
open is a probe-grade refutation later being cited as settled; that is a read-path problem,
and the mitigation is that grade renders wherever status renders, never one without the
other. The cost of not doing that has already been measured in a sibling system of ours:
an effective-trust rule documented in four places and computed nowhere.

## Statuses

Derived from the verdicts, not stored:

| status | means |
|---|---|
| `open` | no verdict yet |
| `corroborated` | evidence consistent with it, and none against |
| `contested` | evidence on both sides, unresolved |
| `refuted` | evidence against it that the author accepts |
| `superseded` | replaced by a new id, which names it in `supersedes:` |
| `retracted` | withdrawn without replacement — the claim should not have been made |
| `non-comparable` | a methodology change broke comparability with this entry's numbers |

`refuted` and `retracted` entries stay. A deleted null result gets re-derived by the next
reader in six weeks, and that rule applies to claims exactly as it applies to lab notes.

`non-comparable` exists because the experiment contract forbids silently changing
evaluation methodology. When a change breaks comparability, prior entries are marked, not
restated.

## Revision

A claim's text is frozen, so a changed claim is a **new file with a new id** carrying
`supersedes: <old-id>`. The old file keeps its text, its original credence, and its
verdicts, and gains one final verdict recording the supersession.

**A conjunction whose halves resolve differently is split, not judged as a whole.** If part
of a claim falls and part survives, the entry is `superseded` and replaced by one entry per
conjunct, each carrying its own status. Marking the whole thing `refuted` kills a claim the
evidence preserved; marking it `corroborated` keeps one the evidence killed. C036 was
backfilled as `refuted` on evidence that touched only its second sentence, and was split
into C051 and C052 — the same retired-by-split error this ledger records against P001, made
one directory over and inside a week.

## Predictions and scoring

A prediction entry additionally carries:

```yaml
credence: 0.78
predicted_by: dl
consultation: modelling consultation, round 2
resolves_when: <the observation that would settle it>
resolved: <date> | null
outcome: true | false | null
```

`resolves_when` is written at the same time as the credence and is frozen with it. A
prediction with no resolution criterion cannot be scored and is not a prediction; it is a
preference, and belongs in the unscored-rankings list instead.

Scoring uses a strictly proper rule, so that reporting the true belief is the unique
optimum. Brier (the quadratic score) is sufficient for binary resolutions. Skill scores
are excluded as generally improper.

## The digest

Each preregistration restates, in its own words, the claims that experiment rests on and
the grade each carried at signing. Written by hand and boundary-safe by authorship — no
ledger ids, no ticket ids, no private paths. If a claim is later refuted or superseded,
that experiment's findings inherit it, and the digest is what makes the inheritance
visible to an outside reader.

## References — the citation invariant

**A claim restated outside the ledger is recorded in that claim's References section.**
Maintenance happens at write time: you write the claim into a document, you append the
location. Verification happens at read time: `ledger/references.py`. When a claim tips to
`refuted` or `superseded`, its References rows are the work list.

**The link runs one way.** The ledger names its references; a referencing document names
no ledger entry. A claim's status lives in exactly one place, and an id copied into a
document is a pointer that goes stale the moment that status changes — silently, because
nothing checks it from that side. The one-way rule keeps the stale copy impossible rather
than merely discouraged.

`references.py` scans published surfaces plus the one unpublished file the public
`.gitignore` already names. A claim restated only on some other unpublished surface is
not found and not recorded; a clean run says nothing about it. The bound is deliberate —
a row here is a public path, so a finding on an undisclosed surface could not be written
down without disclosing it — and it means a restatement written onto such a surface has
to be caught at write time, because nothing catches it at read time.

This also fixes the hazard the nanopublication grounding names: there, supersession is
discoverable only forward, so "by starting from the URI of the previous version and follow
its links, the existence of the new version is not even noticed." A reader at the stale
copy gets no signal. References make it discoverable backward.

Each row carries a genre, because the two genres this project already keeps resolve
differently when a claim falls:

- `record` — a dated lab note. Allowed to be wrong and to stay; that is the genre's
  point, and a superseded note keeps its text under a banner. **Not work.**
- `standing` — a document required to describe current state: the manifest, either
  README, `CLAUDE.md`, a preregistration. **Work, every time.**

Matching is by a frozen `fingerprint` — a distinctive phrase from the statement. That
finds copies. **A restatement in different words is invisible to it**, and no tuning fixes
that; it would need semantic matching, which is a different tool with its own error rate.
Both restatements that motivated this invariant were verbatim, so the checker catches what
actually occurred, and a clean run is not evidence that no uncited restatement exists.

## Known gaps

Stated because they are load-bearing and this document should not be cited past them.

- **Retraction is ungrounded, and this was checked rather than assumed.** A search for
  `retract` across the Kuhn versioning paper, the nanopublications resource paper, the
  Micropublications paper and SEPIO returns three hits, all motivational ("rising levels of
  article retractions"), none defining a construct. Every lifecycle relation in the corpus
  is replacement-shaped. The `retracted` status is designed by analogy with `supersedes`
  and has no citation behind it.
- **ECO's discriminating axis is not quotable from what we ingested.** Only the GitHub
  README landed, seven chunks, and it neither enumerates the top-level evidence categories
  nor states that the hierarchy discriminates on how evidence was obtained. That axis is
  widely attributed to ECO and this design leans on the idea, so it is marked ungrounded
  until the 2022 NAR paper (PMID 34986598) is ingested. ECO's actual second root class is
  `assertion method`, which is the *act* of asserting — human versus machine — not the
  manner of obtaining evidence.
- **The grade ladder's rung count is a choice.** GRADE uses four. Nothing measured says
  five is right here.
- **Nothing here is tested against real use.** The ledger's failure mode is becoming a
  compliance ritual nobody reads, which is attested in this system's own graph — three
  fields written and read by nothing. The backfill is the first test.

## Open decision for the operator

**Narrowed 2026-08-27 by how the signature gate is actually used.** The gate exists so the
operator sits at the desk and reads the proposition and methodology thoroughly — it is a
forcing function for attention, not a fraud control — and signing is immediately followed
by kicking the run off. That closes the pre-run half of the amendment question entirely:
there is no window in which a signed preregistration drifts before it is executed, and the
signature binding to a name and a date rather than to the document's bytes costs nothing.

What remains is smaller and does not threaten the never-edit rule. Nosek et al. are about
deviations discovered *once data exists* — a probe fails, a margin turns out uncomputable —
and they require the deviation to be recorded, not the plan to be editable: "Deviations from
data collection and analysis plans are common, even in the most predictable investigations.
… [the researcher] can transparently report changes that were made and why."

So the preregistration stays immutable, and the deviation record belongs to the **run**,
not to the prereg: three fields — what changed, why, and whether outcomes had been observed
at the time. Where that record lives (`findings.md`, a sibling file, or `results.json`) is
the only thing still unsettled here, and it is a placement question rather than a policy
one.

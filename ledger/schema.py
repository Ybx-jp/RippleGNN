"""The ledger entry as the four checkers read it.

One parser, one normalization, one fingerprint, one status derivation, shared by
validate.py, resolve.py, references.py and propagate.py so that no two checkers can
disagree about what an entry says. The schema itself is stated in corpus/README.md (the
parts the red-team seeds depend on) and is proven by corpus/run.py; nothing here is
trusted beyond what that corpus exercises.

This module is imported by the checkers with the ledger directory on sys.path. It has
no dependencies outside the standard library so the checkers run from a plain
`python3` in a pre-commit hook.
"""

from __future__ import annotations

import dataclasses
import glob
import hashlib
import json
import os
import re
import subprocess
import unicodedata
from datetime import datetime
from pathlib import Path

GRADES = ("asserted", "argued", "measured", "controlled", "preregistered")
MEASURED_AND_ABOVE = ("measured", "controlled", "preregistered")
KINDS = ("claim", "prediction", "hypothesis")
STATUSES = (
    "open",
    "corroborated",
    "contested",
    "refuted",
    "superseded",
    "retracted",
    "non-comparable",
)
TERMINAL = ("refuted", "superseded", "retracted", "non-comparable")
FALLEN = ("refuted", "superseded", "retracted")
ACTS = ("cites-as-live", "cites-as-contested", "cites-as-fallen", "challenges")
# Which target statuses each citation act is legal against.
ACT_ALLOWS = {
    "cites-as-live": {"open", "corroborated"},
    "cites-as-contested": {"contested"},
    "challenges": {"open", "corroborated", "contested"},
    "cites-as-fallen": set(STATUSES),
}
VERDICT_ENTRY_ACTS = ("fallen", "challenges", "supersedes")
GROUND_TYPES = ("lab", "experiment", "entry", "source", "search")
VERDICT_AUTHORS = ("main", "propagation")
ARCHIVED_PREFIXES = ("C", "P")
SECTIONS = ("Assertion", "Scope", "Grounds", "Warrant", "Backing")
TAIL_SECTIONS = ("Verdicts", "References")
SCOPE_KEYS = ("metric", "cohort", "condition")
APPEND = "<!-- APPEND BELOW THIS LINE ONLY -->"

ID_RE = re.compile(r"^([A-Z])(\d{4})-[a-z0-9][a-z0-9-]*$")
PREFIX_RE = re.compile(r"^([A-Z]\d+)")
TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:[+-]\d{2}:\d{2}|Z)$")
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
HEADING_RE = re.compile(r"^## (.+?)\s*$", re.M)
VERDICT_HEAD_RE = re.compile(r"^- (\S+) · (\S+) · grade: (\S+) · author: (\S+)$")
BACKING_BLOCK_RE = re.compile(r"^- source: (.*)\n\s+speaker: (.*)\n\s+quote: (.*)$", re.M)
REFERENCE_RE = re.compile(r"^- (\S+) · (standing|record) · (\S+)$")
# A citation in a document: `(A0007-slug, cites-as-live)`.
CITATION_RE = re.compile(r"\(([A-Z]\d{3,}(?:-[a-z0-9-]+)?),\s*(" + "|".join(ACTS) + r")\)")
# An archived id anywhere in a document is a quarantine breach by prefix alone.
ARCHIVED_ID_RE = re.compile(r"\b[CP]\d{3}\b")

ELISIONS = ("[…]", "[...]")
QUOTE_MARKS = '"“”„«»'


# --- reports -------------------------------------------------------------------------


@dataclasses.dataclass
class Report:
    """One thing a checker has to say. `fail` exits non-zero; `flag` is visible and exits
    zero. `entry` is the id prefix (`A0001`) or None for a document; `part` names the
    place inside it the way corpus/README.md's expectation rows do."""

    outcome: str
    entry: str | None
    part: str
    message: str
    commit: str | None = None

    def place(self):
        return f"{self.entry} {self.part}" if self.entry else self.part

    def line(self):
        return f"{self.outcome.upper():4} {self.place()}: {self.message}"


def exit_code(reports):
    return 1 if any(r.outcome == "fail" for r in reports) else 0


def print_reports(reports, name, quiet_when_clean=False):
    for r in reports:
        print(r.line())
    fails = sum(r.outcome == "fail" for r in reports)
    flags = sum(r.outcome == "flag" for r in reports)
    if fails or flags or not quiet_when_clean:
        print(f"{name}: {fails} failure(s), {flags} flag(s)")


# --- the ledger being checked ----------------------------------------------------


@dataclasses.dataclass
class Ledger:
    """Where a checker looks. The real ledger and a corpus seed are both instances."""

    entries_dir: Path
    registry: Path
    tree: Path  # root that `lab:`/`experiment:` paths and registry `bytes` are relative to
    docs: list  # [(display name, Path)] documents that may cite entries
    repo: Path | None = None  # git repository holding entries_dir, for history checks
    cache: Path | None = None  # source bytes keyed by sha256, when the registry has none


# Documents a claim can be cited or restated in, addressed from the tree root. Only
# published surfaces are scanned, plus the one unpublished file the public .gitignore
# already names; the ledger itself and the inventory it was built from are excluded.
DOC_PATTERNS = ("*.md", "experiments/*.md", "lab/*.md", "src/**/*.py", "tests/**/*.py")
DOC_EXCLUDES = ("/ledger/", "claims-inventory-draft", "ledger-grounding-brief")


def tree_documents(tree):
    paths = []
    for pattern in DOC_PATTERNS:
        paths += glob.glob(os.path.join(tree, pattern), recursive=True)
    docs, seen = [], {}
    for path in sorted(set(paths)):
        norm = path.replace(os.sep, "/")
        if any(x in norm for x in DOC_EXCLUDES):
            continue
        # Keyed by real path: the private surfaces are reachable at more than one
        # address through symlinks, and a document is reported at one location only.
        real = os.path.realpath(path)
        rel = os.path.relpath(path, tree)
        if real in seen and len(seen[real]) <= len(rel):
            continue
        seen[real] = rel
        docs.append((rel, Path(path)))
    return docs


def default_ledger(tree=None):
    tree = Path(tree or Path(__file__).resolve().parent.parent)
    ledger = tree / "ledger"
    return Ledger(
        entries_dir=ledger / "entries",
        registry=ledger / "sources.jsonl",
        tree=tree,
        docs=tree_documents(tree),
        repo=tree if (tree / ".git").exists() else None,
        cache=ledger / "cache",
    )


# --- normalization and the fingerprint ---------------------------------------------


def normalize(text):
    """NFC, markdown emphasis markers removed, whitespace collapsed. The fingerprint and
    the resolver both use this, so they never disagree about what a change is."""
    text = unicodedata.normalize("NFC", text).replace("*", "").replace("`", "")
    return " ".join(text.split())


def normalize_with_map(text):
    """normalize(), plus for every character of the result the index of the character
    in the NFC text it came from. Lets the resolver find a span in normalized text and
    then look at the original around it."""
    nfc = unicodedata.normalize("NFC", text)
    out, idx = [], []
    pending_space = False
    for i, ch in enumerate(nfc):
        if ch in "*`":
            continue
        if ch.isspace():
            pending_space = bool(out)
            continue
        if pending_space:
            out.append(" ")
            idx.append(i)  # the space stands for the whitespace run ending here
            pending_space = False
        out.append(ch)
        idx.append(i)
    return nfc, "".join(out), idx


def fingerprint(scope_text, backing_blocks):
    """sha256 over the normalized Scope lines, a blank line, then one normalized line per
    Backing block (`source | speaker | quote`), blocks sorted. Grounds are excluded."""
    scope = [normalize(ln) for ln in scope_text.splitlines() if ln.strip()]
    lines = sorted(
        f"{normalize(s)} | {normalize(sp)} | {normalize(q)}" for s, sp, q in backing_blocks
    )
    payload = "\n".join(scope) + "\n\n" + "\n".join(lines)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


# --- pointers ------------------------------------------------------------------


@dataclasses.dataclass
class Pointer:
    type: str
    raw: str
    target: str = ""  # path, entry id, registry id
    section: str = ""  # lab: § "section"
    pin: str = ""  # lab:/experiment: @commit
    act: str = ""  # entry: · act
    locator: str = ""  # source: · locator
    fields: dict = dataclasses.field(default_factory=dict)  # search: key=value


LAB_RE = re.compile(r'^lab: (\S+) § "([^"]+)" @(\S+)$')
EXPERIMENT_RE = re.compile(r"^experiment: (\S+) @(\S+)$")
ENTRY_RE = re.compile(r"^entry: (\S+) · (\S+)$")
SOURCE_RE = re.compile(r"^source: (\S+) · (.+)$")
SEARCH_RE = re.compile(r'^search: corpus=(.+?); query="(.*)"; date=(\d{4}-\d{2}-\d{2})$')
DEFECT_RE = re.compile(r"^defect: (.+)$")


def parse_pointer(raw):
    """A typed pointer, or None when the line is none of the forms."""
    raw = raw.strip()
    if m := LAB_RE.match(raw):
        return Pointer("lab", raw, target=m.group(1), section=m.group(2), pin=m.group(3))
    if m := EXPERIMENT_RE.match(raw):
        return Pointer("experiment", raw, target=m.group(1), pin=m.group(2))
    if m := ENTRY_RE.match(raw):
        return Pointer("entry", raw, target=m.group(1), act=m.group(2))
    if m := SOURCE_RE.match(raw):
        return Pointer("source", raw, target=m.group(1), locator=m.group(2).strip())
    if m := SEARCH_RE.match(raw):
        return Pointer(
            "search", raw, fields={"corpus": m.group(1), "query": m.group(2), "date": m.group(3)}
        )
    if m := DEFECT_RE.match(raw):
        return Pointer("defect", raw, target=m.group(1))
    return None


# --- quotes ----------------------------------------------------------------------


@dataclasses.dataclass
class Quote:
    spans: list
    lead_elided: bool
    trail_elided: bool


def parse_quote(value):
    """One or more quoted spans separated by `[…]`, optionally beginning or ending with
    `[…]`. None when the value is anything else."""
    text = value.strip()
    for mark in ELISIONS:
        text = text.replace(mark, "\x00")
    parts = [p.strip() for p in text.split("\x00")]
    if not parts:
        return None
    lead = parts[0] == ""
    trail = len(parts) > 1 and parts[-1] == ""
    inner = parts[1 if lead else 0 : (len(parts) - 1) if trail else len(parts)]
    if not inner:
        return None
    spans = []
    for piece in inner:
        if len(piece) < 2 or piece[0] not in QUOTE_MARKS or piece[-1] not in QUOTE_MARKS:
            return None
        body = piece[1:-1]
        if not body.strip() or any(c in QUOTE_MARKS for c in body):
            return None
        spans.append(body)
    return Quote(spans, lead, trail)


# --- entries ---------------------------------------------------------------------


@dataclasses.dataclass
class Verdict:
    index: int  # 1-based
    raw: str  # the block as written, for the append-only comparison
    timestamp: str = ""
    status: str = ""
    grade: str = ""
    author: str = ""
    evidence: str | None = None
    note: str | None = None
    malformed: str | None = None

    @property
    def pointer(self):
        return parse_pointer(self.evidence) if self.evidence else None


@dataclasses.dataclass
class Backing:
    index: int  # 1-based
    source: str  # `<registry id> · <locator>`
    speaker: str
    quote: str

    @property
    def source_id(self):
        return self.source.split("·", 1)[0].strip()

    @property
    def part(self):
        return f"Backing quote {self.index}"


@dataclasses.dataclass
class Reference:
    path: str
    genre: str
    act: str


@dataclasses.dataclass
class Entry:
    path: Path
    text: str
    front: dict  # frontmatter, key -> value (raw string)
    front_order: list
    sections: dict  # heading -> body, in file order
    section_order: list
    has_append: bool
    frozen: str  # everything above the APPEND marker
    grounds: list  # [(raw line, Pointer | None)]
    backing: list  # [Backing]
    backing_none: bool
    verdicts: list  # [Verdict]
    references: list  # [(raw line, Reference | None)]
    problems: list  # [(part, message)] structural defects found while parsing

    @property
    def id(self):
        return self.front.get("id", "")

    @property
    def prefix(self):
        m = PREFIX_RE.match(self.id or self.path.stem)
        return m.group(1) if m else (self.id or self.path.stem)

    @property
    def grade(self):
        return self.front.get("grade", "")

    @property
    def scope_text(self):
        return self.sections.get("Scope", "")

    @property
    def scope(self):
        out = {}
        for ln in self.scope_text.splitlines():
            if ln.strip():
                key, _, value = ln.partition(":")
                out[key.strip()] = value.strip()
        return out

    @property
    def assertion(self):
        return self.sections.get("Assertion", "").strip()

    @property
    def ground_pointers(self):
        return [p for _, p in self.grounds if p is not None]

    def computed_sha(self):
        return fingerprint(self.scope_text, [(b.source, b.speaker, b.quote) for b in self.backing])

    def status(self):
        return derive_status(self.verdicts)

    def superseded_verdicts(self):
        return [v for v in self.verdicts if v.status == "superseded"]


def _split_sections(body):
    order, sections = [], {}
    matches = list(HEADING_RE.finditer(body))
    for i, m in enumerate(matches):
        name = m.group(1)
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        chunk = body[m.end() : end]
        order.append(name)
        sections[name] = chunk.replace(APPEND, "") if name == "Backing" else chunk
    return order, sections


def _parse_verdicts(text):
    verdicts = []
    blocks = re.split(r"\n(?=- )", "\n" + text.strip("\n"))
    for block in blocks:
        block = block.strip("\n")
        if not block.strip():
            continue
        v = Verdict(index=len(verdicts) + 1, raw=block.rstrip())
        lines = block.splitlines()
        m = VERDICT_HEAD_RE.match(lines[0].rstrip())
        if not m:
            v.malformed = "header is not `- <timestamp> · <status> · grade: <g> · author: <a>`"
        else:
            v.timestamp, v.status, v.grade, v.author = m.groups()
        for ln in lines[1:]:
            fm = re.match(r"^\s+(evidence|note): (.*)$", ln.rstrip())
            if not fm:
                v.malformed = v.malformed or f"unrecognized line {ln.strip()!r}"
                continue
            setattr(v, fm.group(1), fm.group(2).strip())
        verdicts.append(v)
    return verdicts


def parse_entry(path, text=None):
    path = Path(path)
    if text is None:
        text = path.read_text(encoding="utf-8")
    problems = []
    front, front_order = {}, []
    body = text
    if text.startswith("---\n") and "\n---\n" in text[4:]:
        head, body = text[4:].split("\n---\n", 1)
        for ln in head.splitlines():
            if not ln.strip():
                continue
            key, sep, value = ln.partition(":")
            if not sep or not re.match(r"^[a-z_]+$", key):
                problems.append(("frontmatter", f"unparseable line {ln!r}"))
                continue
            if key in front:
                problems.append(("frontmatter", f"duplicate key {key}"))
            front[key] = value.strip()
            front_order.append(key)
    else:
        problems.append(("frontmatter", "no YAML frontmatter"))

    has_append = APPEND in body
    frozen = text.split(APPEND, 1)[0]
    order, sections = _split_sections(body)

    grounds = []
    for ln in sections.get("Grounds", "").splitlines():
        if not ln.strip():
            continue
        if ln.startswith("- "):
            grounds.append((ln[2:].strip(), parse_pointer(ln[2:])))
        else:
            grounds.append((ln.strip(), None))

    backing, backing_none = [], False
    btext = sections.get("Backing", "")
    if btext.strip() == "none":
        backing_none = True
    else:
        consumed = 0
        for i, m in enumerate(BACKING_BLOCK_RE.finditer(btext), start=1):
            backing.append(Backing(i, m.group(1).strip(), m.group(2).strip(), m.group(3).strip()))
            consumed += len(m.group(0).splitlines())
        nonblank = [ln for ln in btext.splitlines() if ln.strip()]
        if len(nonblank) != consumed:
            problems.append(("Backing", "not `none` and not a list of source/speaker/quote blocks"))

    verdicts = _parse_verdicts(sections.get("Verdicts", ""))

    references = []
    for ln in sections.get("References", "").splitlines():
        if not ln.strip():
            continue
        m = REFERENCE_RE.match(ln.strip())
        references.append((ln.strip(), Reference(*m.groups()) if m else None))

    return Entry(
        path=path,
        text=text,
        front=front,
        front_order=front_order,
        sections=sections,
        section_order=order,
        has_append=has_append,
        frozen=frozen,
        grounds=grounds,
        backing=backing,
        backing_none=backing_none,
        verdicts=verdicts,
        references=references,
        problems=problems,
    )


def derive_status(verdicts):
    """The status of the last legal verdict. Terminal statuses stop the walk; a verdict
    appended after one is malformed (validate.py reports it) and does not move the
    status — with the one exception that `refuted` or `non-comparable` may be followed by
    exactly one `superseded`, because reinstatement is supersession."""
    status, terminal, reinstated = "open", False, False
    for v in verdicts:
        if v.malformed or v.status not in STATUSES or v.status == "open":
            continue
        if terminal:
            if (
                status in ("refuted", "non-comparable")
                and v.status == "superseded"
                and not reinstated
            ):
                status, reinstated = "superseded", True
            continue
        status = v.status
        terminal = status in TERMINAL
    return status


def parse_timestamp(value):
    if not value or not TIMESTAMP_RE.match(value):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


# --- loading -------------------------------------------------------------------


def git(repo, *args, check=False):
    """stdout of a git command in `repo`, or None on failure."""
    try:
        out = subprocess.run(
            ["git", "-C", str(repo), *args], capture_output=True, text=True, check=check
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return out.stdout if out.returncode == 0 else None


def load_entries(ledger, cached=False):
    """Every entry under entries_dir, sorted by filename. With `cached`, an entry that is
    in the git index is read from the index instead of the working tree, which is what a
    pre-commit hook wants to check."""
    entries = []
    if not ledger.entries_dir.is_dir():
        return entries
    for path in sorted(ledger.entries_dir.glob("*.md")):
        text = None
        if cached and ledger.repo:
            rel = os.path.relpath(path, ledger.repo)
            text = git(ledger.repo, "show", f":{rel}")
        entries.append(parse_entry(path, text))
    return entries


def by_id(entries):
    return {e.id: e for e in entries if e.id}


def load_registry(path):
    """sources.jsonl as {id: row}. A missing file is an empty registry; a malformed row
    is reported by resolve.py when something points at it."""
    rows = {}
    path = Path(path)
    if not path.is_file():
        return rows
    for ln in path.read_text(encoding="utf-8").splitlines():
        if ln.strip():
            row = json.loads(ln)
            rows[row["id"]] = row
    return rows


def source_bytes(row, ledger):
    """(text, problem). The bytes come from the row's `bytes` path (fixtures) or the
    cache keyed by sha256 (real sources); either way the hash must match the row."""
    if "bytes" in row:
        candidate = ledger.tree / row["bytes"]
    elif ledger.cache:
        candidate = ledger.cache / row["sha256"]
    else:
        return None, f"registry row {row['id']} names no bytes and there is no cache"
    if not candidate.is_file():
        return None, (
            f"bytes for {row['id']} not found at {os.path.relpath(candidate, ledger.tree)}; "
            "the check cannot run"
        )
    data = candidate.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != row.get("sha256"):
        return None, (
            f"bytes for {row['id']} hash to {digest[:12]}…, registry says "
            f"{str(row.get('sha256'))[:12]}…; re-verify everything citing it"
        )
    try:
        return data.decode("utf-8"), None
    except UnicodeDecodeError:
        return None, f"bytes for {row['id']} are not UTF-8 text"


def read_document(path):
    try:
        return Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None

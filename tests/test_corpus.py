"""The red-team corpus under ledger/corpus/ is well-formed against its own README.

These are shape checks on the test fixture, not the checkers the corpus exists to prove:
every seed has expectations a runner can match, known-good seeds expect only passes,
registry hashes match the fixture bytes, and every entry's verbatim_sha follows the
canonicalization the README states. A corpus that drifts from its own description would
prove the wrong thing about the checkers built against it.
"""

import hashlib
import json
import re
import unicodedata
from pathlib import Path

import pytest

CORPUS = Path(__file__).resolve().parents[1] / "ledger" / "corpus"
SEEDS = sorted(p for p in (CORPUS / "seeds").iterdir() if p.is_dir())
CHECKERS = {"validate", "resolve", "references", "propagate", "review"}
OUTCOMES = {"pass", "fail", "flag", "judge"}


def expected(seed):
    return json.loads((seed / "expected.json").read_text(encoding="utf-8"))


def entry_files(seed):
    return sorted(seed.rglob("entries/*.md"))


def test_corpus_has_seeds_of_both_kinds():
    names = [s.name for s in SEEDS]
    assert any(n.startswith("K") for n in names)
    assert any(n.startswith("D") for n in names)


@pytest.mark.parametrize("seed", SEEDS, ids=lambda s: s.name)
def test_expectations_are_matchable(seed):
    exp = expected(seed)
    assert set(exp) >= {"class", "known_good", "expect"}
    assert exp["expect"], "a seed with no expectation rows tests nothing"
    for row in exp["expect"]:
        assert row["checker"] in CHECKERS, row
        assert row["outcome"] in OUTCOMES, row
        assert row["where"] and row["why"], row
        # review is not a program: its rows always judge, and no checker row does.
        assert (row["checker"] == "review") == (row["outcome"] == "judge"), row
    checker_non_pass = [
        r for r in exp["expect"] if r["checker"] != "review" and r["outcome"] != "pass"
    ]
    review_rows = [r for r in exp["expect"] if r["checker"] == "review"]
    if exp["known_good"]:
        assert seed.name.startswith("K") and not checker_non_pass
    else:
        # A defect seed is caught or flagged by a checker, or it is review-only: the
        # machinery passes and the review row is the whole record of what is wrong.
        assert seed.name.startswith("D") and (checker_non_pass or review_rows)
    assert entry_files(seed) or (seed / "commits").is_dir()
    if (seed / "commits").is_dir():
        assert "history" in exp


def test_registry_hashes_match_fixture_bytes():
    rows = [json.loads(line) for line in (CORPUS / "sources.jsonl").read_text().splitlines()]
    assert rows
    for row in rows:
        data = (CORPUS.parents[1] / row["bytes"]).read_bytes()
        assert hashlib.sha256(data).hexdigest() == row["sha256"], row["id"]


def section(text, name):
    m = re.search(rf"^## {name}\n(.*?)(?=^## |^<!-- APPEND|\Z)", text, re.M | re.S)
    assert m, name
    return m.group(1)


def norm(text):
    """The README's normalization: NFC, emphasis markers removed, whitespace collapsed."""
    text = unicodedata.normalize("NFC", text).replace("*", "").replace("`", "")
    return " ".join(text.split())


def canonical_sha(text):
    scope = [norm(ln) for ln in section(text, "Scope").splitlines() if ln.strip()]
    backing = section(text, "Backing")
    blocks = re.findall(r"^- source: (.*)\n\s+speaker: (.*)\n\s+quote: (.*)$", backing, re.M)
    lines = sorted(f"{norm(s)} | {norm(sp)} | {norm(q)}" for s, sp, q in blocks)
    payload = "\n".join(scope) + "\n\n" + "\n".join(lines)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def creation_states(seed):
    """Entries as first written. A history seed's later commit states may be tampered
    on purpose (D23 edits a quote), so only the state a file was created in is held to
    the canonicalization; the one seed whose declared sha is wrong by design is D30."""
    return [p for p in entry_files(seed) if "commits" not in p.parts or p.parents[1].name == "01"]


ENTRIES = [p for s in SEEDS for p in creation_states(s) if not s.name.startswith("D30")]


@pytest.mark.parametrize("path", ENTRIES, ids=lambda p: f"{p.relative_to(CORPUS / 'seeds')}")
def test_verbatim_sha_follows_the_documented_canonicalization(path):
    text = path.read_text(encoding="utf-8")
    declared = re.search(r"^verbatim_sha: ([0-9a-f]{64})$", text, re.M)
    assert declared, "no verbatim_sha"
    assert declared.group(1) == canonical_sha(text)
    assert "<!-- APPEND BELOW THIS LINE ONLY -->" in text


def test_the_mismatch_seed_really_mismatches():
    (path,) = entry_files(CORPUS / "seeds" / "D30-verbatim-sha-mismatch")
    text = path.read_text(encoding="utf-8")
    assert re.search(r"^verbatim_sha: (0{64})$", text, re.M)
    assert canonical_sha(text) != "0" * 64


def test_no_private_surface_is_named():
    for path in CORPUS.rglob("*"):
        if path.is_file():
            body = path.read_text(encoding="utf-8")
            assert "notes/" not in body and "CLAUDE.md" not in body, path

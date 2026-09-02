"""Find restatements of archived ledger claims in the documents, and flag violations.

The ledger was quarantined on 2026-08-28 (see ledger/README.md). This checker now
enforces the verbatim half of the quarantine rule: no new document may copy an archived
claim. A copy at a location an entry's References section does not already list is a
violation -- before the quarantine it meant write-time maintenance was skipped; now it
means the quarantine was breached. References recorded before the quarantine stay
recorded, and a standing document still carrying a fallen claim is still work.

WHAT THIS CANNOT DO. It matches a frozen fingerprint against the tree, so it finds
COPIES. A restatement in different words is invisible to it and no amount of tuning
changes that — it needs semantic matching, which is a different tool with its own error
rate. Both restatements that motivated this invariant were verbatim, so it catches the
cases that actually occurred, and this paragraph is here so nobody reads a clean run as
proof that no uncited restatement exists.

It also does not see unpublished surfaces other than the one the public .gitignore
names. A claim restated only there is not found and not recorded, and a clean run says
nothing about it. That is a real coverage gap, accepted because the alternative is worse:
a finding this checker cannot express without writing an undisclosed path into a public
file. The gap is the reason a claim restated on an unpublished surface has to be caught
when it is written, not here.

Run:  python3 ledger/archive/references.py
Exit 1 if a refuted or superseded claim still has live references, or if a copy is
found at a location the entry does not list.
"""

import glob
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))  # ledger/archive
TREE = os.path.dirname(os.path.dirname(ROOT))

# Documents a claim can be restated in, all addressed from this working tree.
#
# Only published surfaces are scanned, plus the one unpublished file the public
# .gitignore already names. That bound is deliberate and it is not about secrecy: a
# row in this ledger is a public path, so scanning a surface whose paths may not be
# written here would produce a finding that cannot be recorded. See WHAT THIS CANNOT
# DO for the coverage this gives up.
#
# The ledger itself is excluded, and so is the inventory it was built from: the
# inventory is the source of these claims, not a restatement of them.
PATTERNS = (
    "*.md", "experiments/*.md", "lab/*.md", "src/**/*.py", "tests/**/*.py",
)


def documents():
    paths = []
    for pattern in PATTERNS:
        paths += glob.glob(os.path.join(TREE, pattern), recursive=True)
    return [p for p in sorted(set(paths))
            if "/ledger/" not in p.replace(os.sep, "/")
            and "claims-inventory-draft" not in p
            and "ledger-grounding-brief" not in p]


def normalize(text):
    """Collapse whitespace so a fingerprint survives line wrapping in the target."""
    return " ".join(text.split())


def entries():
    for path in sorted(glob.glob(os.path.join(ROOT, "claims", "*.md"))
                       + glob.glob(os.path.join(ROOT, "predictions", "*.md"))):
        text = io.open(path, encoding="utf-8").read()
        fp = re.search(r'^fingerprint:[ \t]*"(.*)"[ \t]*$', text, re.M)
        ident = re.search(r"^id:[ \t]*(.*)$", text, re.M)
        if not fp or not ident:
            continue
        # Bound the region: the References section that follows contains the words
        # "refuted" and "superseded" in its own explanatory text, and an unbounded
        # split read that boilerplate as this entry's latest verdict.
        verdicts = text.split("## Verdicts", 1)[1].split("## References", 1)[0]
        status = None
        for token in re.findall(r"`([a-z-]+)`", verdicts):
            if token in ("open", "corroborated", "contested", "refuted",
                         "superseded", "retracted", "non-comparable"):
                status = token
        listed = set()
        if "## References" in text:
            for line in text.split("## References", 1)[1].splitlines():
                m = re.match(r"\s*-\s+`([^`]+)`\s*·\s*(\w+)", line)
                if m:
                    listed.add((m.group(1), m.group(2)))
        yield ident.group(1).strip(), fp.group(1), status, listed, path


def main():
    # Keyed by real path, because the private surfaces are reachable at more than one
    # address through the symlinks (CLAUDE.md and notes/CLAUDE.md are one file). The
    # shortest relative address wins, so a claim is reported at one location, not two.
    docs, seen = {}, {}
    for path in documents():
        try:
            body = normalize(io.open(path, encoding="utf-8").read())
        except (OSError, UnicodeDecodeError):
            continue
        real = os.path.realpath(path)
        rel = os.path.relpath(path, TREE)
        if real in seen and len(seen[real]) <= len(rel):
            continue
        seen[real] = rel
        docs[real] = body

    unlisted, stale = [], []
    for ident, fp, status, listed, _ in entries():
        needle = normalize(fp)
        if len(needle) < 20:
            continue  # too short to be distinctive; not worth a false positive
        found = set()
        for real, body in docs.items():
            if needle in body:
                found.add(seen[real])
        known = {rel for rel, _ in listed}
        for rel in sorted(found - known):
            unlisted.append((ident, rel, status))
        if status in ("refuted", "superseded", "retracted"):
            # A `record` is a dated lab note: allowed to be wrong and to stay, which
            # is its genre's whole point. Only a `standing` document, required to
            # describe current state, is work when a claim falls.
            for rel, kind in sorted(listed):
                if kind == "standing":
                    stale.append((ident, rel, status))

    if unlisted:
        print("COPIES FOUND AT LOCATIONS THE ENTRY DOES NOT LIST")
        print("  (the archive is quarantined -- a new copy of an archived claim "
              "breaches it)\n")
        for ident, rel, status in unlisted:
            print(f"  {rel}\n      restates `{ident}` (status `{status}`)")
        print()

    if stale:
        print("REFERENCES TO CLAIMS THAT NO LONGER STAND — these are work to do\n")
        for ident, rel, status in stale:
            print(f"  {rel}\n      carries `{ident}`, which is `{status}`")
        print()

    if not unlisted and not stale:
        print("No unlisted copies, and no live references to fallen claims.")
        print("This proves no VERBATIM copy is unaccounted for. It says nothing about "
              "restatements in different words.")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())

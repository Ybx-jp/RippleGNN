"""Check every archived ledger entry against the schema in ledger/archive/README.md.

The ledger was quarantined on 2026-08-28 (see ledger/README.md); the entries under
archive/ are frozen evidence, including their recorded defects, and this keeps them
well-formed against the schema they were written under. Evidence that drifts is
worthless, which is why the checker outlives the apparatus it was built for.

Run from anywhere:  python3 ledger/validate.py
Exit 1 on any violation.
"""

import glob
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
GRADES = ["asserted", "argued", "measured", "controlled", "preregistered"]
STATUSES = ["open", "corroborated", "contested", "refuted", "superseded",
            "retracted", "non-comparable"]
FROZEN = "<!-- FROZEN ABOVE."


def field(text, name):
    # `[ \t]*`, not `\s*`: \s matches the newline, so an empty `credence:` would
    # capture the following line and report it as a malformed value.
    m = re.search(r"^%s:[ \t]*(.*)$" % re.escape(name), text, re.M)
    if not m:
        return None
    return m.group(1).strip() or None


def quotation_state(text):
    """Is this entry's statement a quotation, and has it been checked against the source?

    Returns (carries_quotation, verified, problems). Measured 2026-08-27: of four entries
    whose evidence chains were resolved to a primary source, four of four stated more than
    that source. `quotes:` records which entries have been checked. It is absent from the
    52 backfilled entries by construction -- the frontmatter is inside the frozen region,
    so they gain it on supersession and never by a sweep -- so its absence is reported as
    a count, never as a violation.
    """
    problems = []
    statement = ""
    if "## Statement" in text:
        statement = text.split("## Statement", 1)[1].split("## Depends on this", 1)[0]
    carries = '"' in statement
    # A quotation is also checked when a verdict records the check. The frontmatter is
    # frozen, so a backfilled entry cannot gain `quotes:` without being superseded, and a
    # reader that counted only the field would report zero checked however many had
    # actually been compared against their sources.
    audited = "quotation audit" in text.split("## Verdicts", 1)[-1]
    value = field(text, "quotes")
    if value is None:
        return carries, audited, problems
    if re.match(r"^unverified:\s*$", value):
        problems.append("`quotes: unverified:` with no reason -- name what has not been "
                        "checked against the source")
        return carries, False, problems
    if value.startswith("unverified:"):
        return carries, False, problems
    if not carries:
        problems.append("carries `quotes:` but its statement quotes nothing")
    return carries, True, problems


def check(path):
    problems = []
    text = io.open(path, encoding="utf-8").read()
    name = os.path.relpath(path, ROOT)

    if not text.startswith("---\n"):
        problems.append("no YAML frontmatter")
        return problems
    if FROZEN not in text:
        problems.append("missing the FROZEN marker — nothing separates the immutable "
                        "region from the appendable one")
    if "## Statement" not in text:
        problems.append("no Statement section")
    if "## Verdicts" not in text:
        problems.append("no Verdicts section")

    ident = field(text, "id")
    if not ident:
        problems.append("no id")
    elif ident != os.path.splitext(os.path.basename(path))[0]:
        problems.append(f"id `{ident}` does not match its filename")

    _, _, quote_problems = quotation_state(text)
    problems += quote_problems

    grade = field(text, "grade")
    if grade not in GRADES:
        problems.append(f"grade `{grade}` is not one of {GRADES}")

    # The locator rule: required at `measured` and above, because the postulate this
    # ledger exists to prevent was a real measurement with unrecorded conditions.
    if grade in ("measured", "controlled", "preregistered"):
        head = text.split(FROZEN)[0]
        for part in ("metric", "cohort", "condition"):
            if not re.search(r"^\s+%s:\s*\S" % part, head, re.M):
                problems.append(f"grade `{grade}` requires locator.{part}")

    credence = field(text, "credence")
    if credence:
        try:
            value = float(credence)
            if not 0.0 <= value <= 1.0:
                problems.append(f"credence {value} outside [0, 1]")
        except ValueError:
            problems.append(f"credence `{credence}` is not a number")

    if "/predictions/" in path.replace(os.sep, "/"):
        if not credence:
            problems.append("a prediction with no credence is not a prediction")
        if not field(text, "resolves_when") and "resolves_when: |" not in text:
            problems.append("no resolves_when — nothing can resolve this")

    # Bounded for the same reason as in references.py: the References section
    # mentions statuses in prose.
    verdicts = text.split("## Verdicts", 1)[1].split("## References", 1)[0]
    found = re.findall(r"`([a-z-]+)`", verdicts)
    if not any(f in STATUSES for f in found):
        problems.append("no verdict carries a recognized status")
    for token in found:
        if token in GRADES or token in STATUSES:
            continue
    if re.search(r"`(open|corroborated|contested|refuted|superseded|retracted)`",
                 verdicts) and "grade `" not in verdicts:
        problems.append("a verdict states a status without the grade of the evidence "
                        "that moved it")

    # Verdict provenance. `evidence` is what bears on the claim; `read-in` is where it
    # was encountered. Collapsing them is how a citation degrades to nothing across a
    # chain of secondary sources: every verdict in the first backfill attributed to the
    # inventory it was read in, and one chain broke completely.
    #
    # `unresolved:` is legal and is NOT an error. A recorded broken link is traceable --
    # you know where the chain broke -- while a silent one is the failure this rule
    # exists to prevent. Failing the check on it would push an honest gap back into
    # either a fabricated citation or a deletion, which is what happened once.
    for block in re.split(r"\n(?=- \*\*\d{4}-\d{2}-\d{2}\*\*)", verdicts):
        if not re.match(r"- \*\*\d{4}-\d{2}-\d{2}\*\*", block.strip()):
            continue
        if not re.search(r"^\s+- evidence:\s*\S", block, re.M):
            problems.append("a verdict carries no `evidence:` -- name what bears on the "
                            "claim, or record `unresolved:` with a reason")
        elif re.search(r"^\s+- evidence:\s*unresolved:\s*$", block, re.M):
            problems.append("a verdict says `unresolved:` with no reason")
    return problems


def main():
    paths = sorted(glob.glob(os.path.join(ROOT, "archive", "claims", "*.md"))
                   + glob.glob(os.path.join(ROOT, "archive", "predictions", "*.md")))
    if not paths:
        print("no entries found")
        return 1
    failed = 0
    quoting = verified = 0
    for path in paths:
        text = io.open(path, encoding="utf-8").read()
        carries, ok, _ = quotation_state(text)
        quoting += 1 if carries else 0
        verified += 1 if (carries and ok) else 0
        problems = check(path)
        if problems:
            failed += 1
            print(os.path.relpath(path, ROOT))
            for p in problems:
                print("   ·", p)
    print(f"\n{len(paths) - failed}/{len(paths)} entries valid")
    print(f"{verified}/{quoting} entries whose statement quotes a source have had that "
          f"quotation checked against it")
    if verified < quoting:
        print(f"{quoting - verified} unchecked. That is not a violation, but it is not a "
              "clean bill either: an unchecked quotation is one nobody has compared "
              "against the source it names.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

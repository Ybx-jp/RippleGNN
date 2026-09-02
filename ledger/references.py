"""Citations, both directions, checked.

Entry to entry: every `entry:` ground names an entry that exists and carries an act
compatible with the target's current status — `cites-as-live` needs open or
corroborated, `cites-as-contested` needs contested, `challenges` needs open,
corroborated or contested, `cites-as-fallen` accepts any status and is the only act
legal against a fallen one. The filter a reader must apply every time is applied for
them here.

Document to entry: a document cites an entry inline as `(A0007-slug, cites-as-live)`.
Every cited id exists, the act is compatible with the target's status, and the entry's
References section lists the citing document; every location an entry lists really
cites it. No document may cite an archived `C###`/`P###` id, by prefix alone. A
document that carries an entry's Assertion verbatim without citing it is reported too:
that finds copies, and says nothing about restatements in other words.

Run:  python3 ledger/references.py
Exit 1 on any failure.
Proven against ledger/corpus/ by ledger/corpus/run.py.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from schema import (  # noqa: E402
    ACT_ALLOWS,
    ARCHIVED_ID_RE,
    ARCHIVED_PREFIXES,
    CITATION_RE,
    Report,
    by_id,
    default_ledger,
    exit_code,
    load_entries,
    normalize,
    print_reports,
    read_document,
)


def run(ledger):
    entries = load_entries(ledger)
    index = by_id(entries)
    status = {e.id: e.status() for e in entries}
    reports = []

    for e in entries:
        for raw, p in e.grounds:
            if p is None or p.type != "entry" or p.act not in ACT_ALLOWS:
                continue
            target = index.get(p.target)
            if target is None:
                reports.append(
                    Report("fail", e.prefix, "Grounds", f"cites {p.target}, which does not exist")
                )
            elif status[p.target] not in ACT_ALLOWS[p.act]:
                reports.append(
                    Report(
                        "fail",
                        e.prefix,
                        "Grounds",
                        f"{p.act} against {p.target}, whose status is {status[p.target]}; "
                        f"{p.act} needs {' or '.join(sorted(ACT_ALLOWS[p.act]))}",
                    )
                )

    cited = {}  # doc name -> {(entry id, act)}
    for name, path in ledger.docs:
        body = read_document(path)
        if body is None:
            continue
        cited[name] = set()
        seen_archived = sorted({m.group(0) for m in ARCHIVED_ID_RE.finditer(body)})
        if seen_archived:
            reports.append(
                Report(
                    "fail",
                    None,
                    name,
                    f"cites archived id(s) {', '.join(seen_archived)}; no document may "
                    "cite the archive",
                )
            )
        for m in CITATION_RE.finditer(body):
            ident, act = m.group(1), m.group(2)
            if ident[0] in ARCHIVED_PREFIXES:
                continue  # already reported by prefix
            cited[name].add((ident, act))
            target = index.get(ident)
            if target is None:
                reports.append(Report("fail", None, name, f"cites {ident}, which does not exist"))
                continue
            if status[ident] not in ACT_ALLOWS[act]:
                reports.append(
                    Report(
                        "fail",
                        None,
                        name,
                        f"{act} against {ident}, whose status is {status[ident]}; "
                        f"{act} needs {' or '.join(sorted(ACT_ALLOWS[act]))}",
                    )
                )
            if not any(r and r.path == name and r.act == act for _, r in target.references):
                reports.append(
                    Report(
                        "fail",
                        None,
                        name,
                        f"cites {ident} {act} but {ident}'s References section does not "
                        "list this document",
                    )
                )
        norm_body = normalize(body)
        for e in entries:
            needle = normalize(e.assertion)
            if (
                len(needle) >= 20
                and needle in norm_body
                and not any(i == e.id for i, _ in cited[name])
            ):
                reports.append(
                    Report(
                        "fail",
                        None,
                        name,
                        f"carries the Assertion of {e.id} verbatim without citing it",
                    )
                )

    for e in entries:
        for raw, r in e.references:
            if r is None:
                continue
            if r.path not in cited:
                reports.append(
                    Report(
                        "fail",
                        e.prefix,
                        "References",
                        f"lists {r.path}, which is not a document this checker can see",
                    )
                )
            elif (e.id, r.act) not in cited[r.path]:
                reports.append(
                    Report(
                        "fail",
                        e.prefix,
                        "References",
                        f"lists {r.path} · {r.act}, but that document does not cite "
                        f"{e.id} that way",
                    )
                )
    return reports


def main():
    ledger = default_ledger()
    reports = run(ledger)
    n = len(load_entries(ledger))
    if n == 0:
        print(
            f"no entries under {os.path.relpath(ledger.entries_dir, ledger.tree)}; nothing to check "
            "beyond the archived-id scan of the documents"
        )
    print_reports(reports, f"references ({n} entries, {len(ledger.docs)} documents)")
    return exit_code(reports)


if __name__ == "__main__":
    sys.exit(main())

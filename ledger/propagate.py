"""The one place machinery writes into an entry.

Walks the `entry:` edges. When an entry cited `cites-as-live` has fallen (refuted,
superseded, retracted), the dependent must carry a `contested` verdict by `propagation`
naming the fallen entry; when an entry is named by a `challenges` act, the challenged
entry must carry a `contested` verdict by `propagation` naming the challenger. A
missing verdict is appended with `--write` and is a failure either way, so the flag is
seen. A `challenges` act against a fallen target is reported as illegal and nothing is
appended. A `propagation` verdict whose stated cause does not exist — no such
challenger, no such fall — is an orphan and fails. A dependent that has itself fallen
needs no flag: a verdict after a terminal status is illegal, and its successor is walked.

Run:  python3 ledger/propagate.py [--write]
      Without --write nothing is modified; the missing verdicts are reported. With it
      they are appended, each attributed `author: propagation`, and the run still exits
      non-zero so the change is looked at before it is committed.
Exit 1 on any failure.
Proven against ledger/corpus/ by ledger/corpus/run.py.
"""

from __future__ import annotations

import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from schema import (  # noqa: E402
    FALLEN,
    TERMINAL,
    Report,
    by_id,
    default_ledger,
    exit_code,
    load_entries,
    print_reports,
)


def has_propagated(entry, cause_id, act):
    return any(
        v.author == "propagation"
        and v.status == "contested"
        and v.pointer
        and v.pointer.type == "entry"
        and v.pointer.target == cause_id
        and v.pointer.act == act
        for v in entry.verdicts
    )


def falling_verdict(entry):
    for v in entry.verdicts:
        if v.status in FALLEN:
            return v
    return None


def verdict_block(status_grade, cause_id, act, note):
    stamp = datetime.now().astimezone().isoformat(timespec="seconds")
    return (
        f"- {stamp} · contested · grade: {status_grade} · author: propagation\n"
        f"  evidence: entry: {cause_id} · {act}\n"
        f"  note: {note}\n"
    )


def append_verdict(entry, block):
    text = entry.text
    marker = "\n## References"
    if marker in text:
        head, tail = text.split(marker, 1)
        head = head.rstrip("\n") + "\n"
        if "## Verdicts" in head and head.rstrip().endswith("## Verdicts"):
            head += "\n"
        text = head + block + marker + tail
    else:
        text = text.rstrip("\n") + "\n" + block
    entry.path.write_text(text, encoding="utf-8")


def run(ledger, write=False):
    entries = load_entries(ledger)
    index = by_id(entries)
    status = {e.id: e.status() for e in entries}
    reports = []
    pending = []  # (entry, block)

    for e in entries:
        for _, p in e.grounds:
            if p is None or p.type != "entry" or p.target not in index:
                continue
            target = index[p.target]
            if status[e.id] in FALLEN and p.act == "cites-as-live":
                # A dependent that has itself fallen needs no flag: its status is
                # terminal, a verdict after it is illegal, and its successor is what
                # is walked.
                continue
            if p.act == "cites-as-live" and status[target.id] in FALLEN:
                if not has_propagated(e, target.id, "fallen"):
                    fv = falling_verdict(target)
                    reports.append(
                        Report(
                            "fail",
                            e.prefix,
                            "Verdicts",
                            f"cites {target.id} cites-as-live and {target.id} has fallen to "
                            f"{status[target.id]}, but carries no contested verdict by "
                            "propagation naming it",
                        )
                    )
                    pending.append(
                        (
                            e,
                            verdict_block(
                                fv.grade if fv else target.grade,
                                target.id,
                                "fallen",
                                f"{target.id} {status[target.id]} (verdict {fv.index if fv else '?'}, "
                                f"{fv.timestamp if fv else 'unknown'})",
                            ),
                        )
                    )
            elif p.act == "challenges":
                if status[target.id] in TERMINAL:
                    reports.append(
                        Report(
                            "fail",
                            target.prefix,
                            "Verdicts",
                            f"{e.id} challenges {target.id}, whose status is terminal "
                            f"({status[target.id]}); no contested verdict is appended and the "
                            "act is illegal — a fallen entry is cited cites-as-fallen",
                        )
                    )
                elif not has_propagated(target, e.id, "challenges"):
                    reports.append(
                        Report(
                            "fail",
                            target.prefix,
                            "Verdicts",
                            f"{e.id} cites {target.id} · challenges but {target.id} carries "
                            "no propagated contested verdict naming it",
                        )
                    )
                    pending.append(
                        (
                            target,
                            verdict_block(
                                e.grade,
                                e.id,
                                "challenges",
                                f"propagated from {e.id}'s challenges act",
                            ),
                        )
                    )

    for e in entries:
        for v in e.verdicts:
            p = v.pointer
            if v.author != "propagation" or not p or p.type != "entry":
                continue
            cause = index.get(p.target)
            if p.act == "challenges":
                ok = cause is not None and any(
                    g and g.type == "entry" and g.target == e.id and g.act == "challenges"
                    for _, g in cause.grounds
                )
                why = f"{p.target} carries no challenges act against {e.id}"
            elif p.act == "fallen":
                ok = (
                    cause is not None
                    and status.get(p.target) in FALLEN
                    and any(
                        g
                        and g.type == "entry"
                        and g.target == p.target
                        and g.act == "cites-as-live"
                        for _, g in e.grounds
                    )
                )
                why = (
                    f"{p.target} has not fallen"
                    if cause is not None and status.get(p.target) not in FALLEN
                    else f"{e.id} does not cite {p.target} cites-as-live"
                )
            else:
                continue
            if cause is None:
                why = f"{p.target} does not exist"
            if not ok:
                reports.append(
                    Report(
                        "fail",
                        e.prefix,
                        "Verdicts",
                        f"verdict {v.index} by propagation names {p.target} as its cause, but "
                        f"{why}; a propagated verdict that nothing caused is an orphan",
                    )
                )

    if write:
        for e, block in pending:
            append_verdict(e, block)
            reports.append(
                Report("flag", e.prefix, "Verdicts", "appended a contested verdict by propagation")
            )
    return reports


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    ledger = default_ledger()
    reports = run(ledger, write="--write" in argv)
    n = len(load_entries(ledger))
    if n == 0:
        print(
            f"no entries under {os.path.relpath(ledger.entries_dir, ledger.tree)}; nothing to propagate"
        )
    print_reports(reports, f"propagate ({n} entries)")
    return exit_code(reports)


if __name__ == "__main__":
    sys.exit(main())

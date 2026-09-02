"""Run the four checkers over every seed in ledger/corpus/seeds/ and hold them to
expected.json, under the contract in README.md:

- every `fail` and `flag` row is produced by the named checker at the named place;
- every checker not named in a non-pass row exits clean, and a checker that is named
  produces nothing the rows do not name — an unlisted trip is a finding about the seed
  or the checker, never a bonus catch;
- `review` rows bind nothing;
- history seeds (`commits/`) are applied as successive commits in a fresh repository
  and their rows name the commit they apply to.

Each seed is checked as if its entries/ and docs/ were the whole ledger, with
sources.jsonl and fixtures/ shared from the corpus root and lab: paths resolved against
the repository tree. Entries are copied to a temporary directory first, so a checker
that writes (propagate.py --write) cannot touch the corpus; here propagate runs
read-only.

Run:  python3 ledger/corpus/run.py [-v] [SEED ...]
      LEDGER_CORPUS=<dir> points the runner at another corpus directory (the tests use
      a tampered copy to show the runner can fail).
Exit 1 if any seed fails.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path

LEDGER = Path(__file__).resolve().parent.parent
TREE = LEDGER.parent
# The corpus normally sits beside this file; the tests point the runner at a tampered
# copy to check that the runner can fail.
CORPUS = Path(os.environ.get("LEDGER_CORPUS") or Path(__file__).resolve().parent)
sys.path.insert(0, str(LEDGER))

import propagate  # noqa: E402
import references  # noqa: E402
import resolve  # noqa: E402
import validate  # noqa: E402
from schema import Ledger  # noqa: E402

CHECKERS = {
    "validate": lambda ledger: validate.run(ledger),
    "resolve": lambda ledger: resolve.run(ledger),
    "references": lambda ledger: references.run(ledger),
    "propagate": lambda ledger: propagate.run(ledger, write=False),
}
WHERE_RE = re.compile(r"^(?:commit (\d+),?\s*)?(.*)$")
ENTRY_RE = re.compile(r"^([A-Z]\d+)\s*(.*)$")


def parse_where(where):
    """(commit, entry prefix, part) from an expectation row's `where`."""
    m = WHERE_RE.match(where.strip())
    commit, rest = m.group(1), m.group(2).strip()
    em = ENTRY_RE.match(rest)
    if em:
        return commit, em.group(1), em.group(2).strip()
    return commit, None, rest


def matches(report, commit, entry, part):
    if report.commit != commit or report.entry != entry:
        return False
    rp, qp = report.part.casefold(), part.casefold()
    return rp == qp or rp.startswith(qp + " ")


def seed_ledger(root, repo=None):
    docs = sorted((root / "docs").glob("*.md")) if (root / "docs").is_dir() else []
    return Ledger(
        entries_dir=root / "entries",
        registry=CORPUS / "sources.jsonl",
        tree=TREE,
        docs=[(f"docs/{p.name}", p) for p in docs],
        repo=repo,
        cache=None,
    )


def stage(src, dst):
    for name in ("entries", "docs"):
        if (dst / name).exists():
            shutil.rmtree(dst / name)
        if (src / name).is_dir():
            shutil.copytree(src / name, dst / name)


def git(repo, *args):
    subprocess.run(
        [
            "git",
            "-C",
            str(repo),
            "-c",
            "user.name=corpus",
            "-c",
            "user.email=corpus@example",
            "-c",
            "commit.gpgsign=false",
            *args,
        ],
        check=True,
        capture_output=True,
        text=True,
    )


def run_checkers(ledger, commit=None):
    """{checker: reports | Exception}"""
    produced = {}
    for name, fn in CHECKERS.items():
        try:
            reports = fn(ledger)
            for r in reports:
                r.commit = commit
            produced[name] = reports
        except Exception as exc:  # a crashing checker is a failing checker
            produced[name] = exc
    return produced


def run_seed(seed):
    """(passed, lines) for one seed directory."""
    expected = json.loads((seed / "expected.json").read_text(encoding="utf-8"))
    rows = [
        (r["checker"], r["outcome"], *parse_where(r["where"]), r["why"])
        for r in expected["expect"]
        if r["checker"] in CHECKERS and r["outcome"] in ("fail", "flag")
    ]
    produced = {name: [] for name in CHECKERS}
    crashes = []
    with tempfile.TemporaryDirectory(prefix="corpus-") as tmp:
        tmp = Path(tmp)
        if (seed / "commits").is_dir():
            git(tmp, "init", "-q")
            for state in sorted(p for p in (seed / "commits").iterdir() if p.is_dir()):
                stage(state, tmp)
                git(tmp, "add", "-A")
                git(tmp, "commit", "-qm", state.name)
                for name, result in run_checkers(
                    seed_ledger(tmp, repo=tmp), commit=state.name
                ).items():
                    if isinstance(result, Exception):
                        crashes.append((name, state.name, result))
                    else:
                        produced[name] += result
        else:
            stage(seed, tmp)
            for name, result in run_checkers(seed_ledger(tmp)).items():
                if isinstance(result, Exception):
                    crashes.append((name, None, result))
                else:
                    produced[name] += result

    lines = []
    for name, commit, exc in crashes:
        lines.append(
            f"{name} crashed{' at commit ' + commit if commit else ''}: "
            + "".join(traceback.format_exception(exc)).strip().splitlines()[-1]
        )
    for name in CHECKERS:
        mine = [r for r in rows if r[0] == name]
        reports = produced[name]
        for _, outcome, commit, entry, part, why in mine:
            hits = [r for r in reports if matches(r, commit, entry, part)]
            if not any(r.outcome == outcome for r in hits):
                got = "; ".join(f"{r.outcome} {r.message}" for r in hits) or "nothing there"
                place = f"{'commit ' + commit + ', ' if commit else ''}{entry + ' ' if entry else ''}{part}"
                lines.append(f"expected {name} {outcome} at {place} ({why}) — got {got}")
        for r in reports:
            if not any(
                matches(r, commit, entry, part) and r.outcome == outcome
                for _, outcome, commit, entry, part, _ in mine
            ):
                prefix = f"commit {r.commit}, " if r.commit else ""
                lines.append(f"unexpected {name} {r.outcome} at {prefix}{r.place()}: {r.message}")
    return not lines, lines, produced


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    verbose = "-v" in argv
    names = [a for a in argv if a != "-v"]
    seeds = sorted(p for p in (CORPUS / "seeds").iterdir() if p.is_dir())
    if names:
        seeds = [s for s in seeds if any(s.name.startswith(n) for n in names)]
    passed = 0
    for seed in seeds:
        ok, lines, produced = run_seed(seed)
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} {seed.name}")
        for ln in lines:
            print(f"   · {ln}")
        if verbose:
            for name, reports in produced.items():
                for r in reports:
                    prefix = f"commit {r.commit}, " if r.commit else ""
                    print(f"     {name}: {r.outcome} {prefix}{r.place()}: {r.message}")
    print(f"\n{passed}/{len(seeds)} seeds pass")
    return 0 if passed == len(seeds) else 1


if __name__ == "__main__":
    os.environ.setdefault("GIT_CONFIG_NOSYSTEM", "1")
    sys.exit(main())

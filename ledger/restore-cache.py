"""Rebuild ledger/cache/ from ledger/sources.jsonl, and say what cannot be rebuilt.

A registry row is committed and the bytes it names are not, so a fresh clone has rows
without bytes and `claims-ledger resolve` fails once per quotation until they are back.
This regenerates them from each row's `url` and `extraction` — the record of how the
bytes were produced — and holds every result to the row's `sha256` before it is written.

Run:  python3 ledger/restore-cache.py [--check]
      --check reports what is present, regenerable and unavailable, and writes nothing.

Exit 0 when every row's bytes are present, 1 otherwise.

A regenerated file is written only if its sha256 is the one the row names. A mismatch is
reported and dropped, never written: the cache is keyed by that digest, so a file stored
under it with different bytes would be read as the source by every later check. The
usual cause is a toolchain that differs from the one the row's `extraction` names, and
the fix is to match it rather than to accept the new bytes — a quotation checked against
a different extraction of the same document is a different check.

Not every source can be regenerated. A row with no `url` names something this project
received rather than fetched, and the bytes exist only where they were received. Those
are reported by id, with the entries whose quotations go unchecked without them, because
a reader who cannot check a quotation should be told which one rather than left to read
a cache miss.
"""

import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRY = os.path.join(ROOT, "ledger", "sources.jsonl")
CACHE = os.path.join(ROOT, "ledger", "cache")
ENTRIES = os.path.join(ROOT, "ledger", "entries")

# Recipes are dispatched on the row's `extraction`, which is the record of how the bytes
# were produced. A row whose extraction matches nothing here is reported as unrecognized
# rather than skipped: a source silently passed over is the cache miss this script exists
# to remove, arriving one step earlier.
PDFTOTEXT_RE = re.compile(r"^pdftotext ([0-9][0-9.]*) \(poppler\), default mode")
INSTALLED_FILE_RE = re.compile(r"^(\S+\.py) as it ships in the wheel, byte for byte")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def rows():
    with open(REGISTRY, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError as exc:
                sys.exit(f"ledger/sources.jsonl line {n}: not JSON: {exc}")


def quoting_entries(source_id):
    """The entries whose Grounds or Backing name this source, so an unavailable source
    can be reported as the quotations it leaves unchecked."""
    hits = []
    needle = f"source: {source_id} ·"
    for name in sorted(os.listdir(ENTRIES)):
        if not name.endswith(".md"):
            continue
        with open(os.path.join(ENTRIES, name), encoding="utf-8") as fh:
            if needle in fh.read():
                hits.append(name[: name.index("-")])
    return hits


def fetch(url):
    with urllib.request.urlopen(url, timeout=120) as response:  # noqa: S310 — https, from the registry
        return response.read()


def from_pdftotext(row, version):
    """The row's URL fetched as a PDF and run through pdftotext in default mode."""
    have = subprocess.run(
        ["pdftotext", "-v"], capture_output=True, text=True, check=False
    ).stderr.split("\n")[0]
    if version not in have:
        print(f"  note: row names pdftotext {version}; this box has `{have.strip()}`")
        print("        the digest check below is what decides whether that matters")
    with tempfile.TemporaryDirectory() as tmp:
        pdf = os.path.join(tmp, "source.pdf")
        txt = os.path.join(tmp, "source.txt")
        with open(pdf, "wb") as fh:
            fh.write(fetch(row["url"]))
        subprocess.run(["pdftotext", pdf, txt], check=True, capture_output=True)
        with open(txt, "rb") as fh:
            return fh.read()


def search_path():
    """Where an installed distribution's files might be. `sys.path` covers the case where
    this script was run by the environment's own interpreter; the checkout's `.venv` is
    searched too, because this script is documented as `python3 ledger/restore-cache.py`
    and a bare `python3` from the repository root is not that interpreter."""
    yield from sys.path
    venv = os.environ.get("VIRTUAL_ENV") or os.path.join(ROOT, ".venv")
    lib = os.path.join(venv, "lib")
    if os.path.isdir(lib):
        for version in sorted(os.listdir(lib)):
            yield os.path.join(lib, version, "site-packages")


def from_installed_file(relative):
    """A file as it ships in an installed distribution, read out of the environment this
    checkout syncs. `uv sync --extra dev` is what puts it there."""
    for base in search_path():
        candidate = os.path.join(base, *relative.split("/"))
        if os.path.isfile(candidate):
            with open(candidate, "rb") as fh:
                return fh.read()
    package = relative.split("/")[0]
    raise FileNotFoundError(
        f"{relative} is not in this environment; `uv sync --extra dev` installs {package}"
    )


def regenerate(row):
    """The bytes this row names, or None when the row records no way to produce them."""
    extraction = row.get("extraction", "")
    if m := INSTALLED_FILE_RE.match(extraction):
        return from_installed_file(m.group(1))
    if not row.get("url"):
        return None
    if m := PDFTOTEXT_RE.match(extraction):
        return from_pdftotext(row, m.group(1))
    raise ValueError(f"no recipe for extraction {extraction!r}; add one to this script")


def main(argv):
    check_only = "--check" in argv[1:]
    for arg in argv[1:]:
        if arg != "--check":
            sys.exit(f"usage: python3 ledger/restore-cache.py [--check]\nunknown argument {arg!r}")

    os.makedirs(CACHE, exist_ok=True)
    known, missing, unavailable = set(), [], []

    for row in rows():
        sha, source_id = row["sha256"], row["id"]
        known.add(sha)
        path = os.path.join(CACHE, sha)
        if os.path.isfile(path):
            with open(path, "rb") as fh:
                found = digest(fh.read())
            if found == sha:
                print(f"present      {source_id}")
                continue
            print(f"CORRUPT      {source_id}: cached bytes hash to {found[:12]}…, not {sha[:12]}…")
            os.remove(path)

        try:
            data = regenerate(row)
        except Exception as exc:  # noqa: BLE001 — every failure here is reported, not raised
            print(f"FAILED       {source_id}: {exc}")
            missing.append(source_id)
            continue

        if data is None:
            unavailable.append(source_id)
            print(f"unavailable  {source_id}: no url; received rather than fetched")
            continue

        found = digest(data)
        if found != sha:
            print(
                f"MISMATCH     {source_id}: regenerated bytes hash to {found[:12]}…, not {sha[:12]}…"
            )
            print("             not written. Match the toolchain the row's extraction names.")
            missing.append(source_id)
            continue

        if check_only:
            print(f"regenerable  {source_id}")
        else:
            with open(path, "wb") as fh:
                fh.write(data)
            print(f"restored     {source_id}  ({len(data)} bytes)")

    for stray in sorted(set(os.listdir(CACHE)) - known - {".gitignore"}):
        print(f"orphan       {stray[:12]}…: no registry row names these bytes")

    if unavailable:
        print("\nUnavailable sources, and the entries whose quotations go unchecked without them:")
        for source_id in unavailable:
            entries = quoting_entries(source_id)
            print(f"  {source_id}: {', '.join(entries) if entries else 'no entry quotes it'}")

    blocked = missing + unavailable
    if blocked:
        print(
            f"\n{len(blocked)} source(s) without bytes; `claims-ledger resolve` will fail on them."
        )
        return 1
    print("\nEvery registry row has its bytes.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

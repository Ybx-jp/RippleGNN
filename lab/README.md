# lab

Vibe research. One-page entries in this project's own voice, written for us, recording
what was tried and what broke. An entry is cheap to write and is allowed to be wrong.

Naming: `NNN-slug.md`, zero-padded, sequential, never renumbered.

Every entry opens with the same header line so the sequence can be skimmed:

    **Date:** 2026-08-26 · **Component:** neighborhood sampler · **Status:** measured.

`Status` is one of `measured`, `abandoned`, `open`. `abandoned` entries stay — a
negative result that gets deleted gets re-run by the next reader six weeks later.

An entry that concludes something states the observation and the interpretation in
separate paragraphs, because in this project they have different lifetimes: the
observation survives a change of mind, the interpretation often does not.

This directory is not `experiments/`. Nothing here is a result anyone outside the
project should cite.

Every entry that reports a measurement carries a `## Setup` section before its
`## Observation`, written so that a reader who has opened no other document can
evaluate the result: what the task is, what the data and the starting state are, what
was changed and by what (a generator, a real stream, a hand edit), what was held fixed,
what is compared against what, and what the baseline or noise band is. A pointer to an
earlier note is not a substitute; the earlier note can be named, but the sentences are
repeated here.

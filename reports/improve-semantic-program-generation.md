# Improve semantic-program-generation

Skill: `plugins/bugfinding/skills/semantic-program-generation/`

## Findings

Sources fetched this session: Csmith README and COPYING at commit `0cdc710315cfee9035e22ef4363ca479270d1934`; FuzzTest `doc/domains-reference.md`, `doc/quickstart-bazel.md`, `doc/fuzz-test-macro.md`, `LICENSE` at commit `1b4e4f0e4c446aca4660c43a28ec1b8d893b6510`; SQLite `testing.html` §4.1.3 via WebFetch (page footer "last updated on 2026-04-21"). Csmith paper: paper-reader notes at `C:/Users/Q/code/bugfinding-literature/semantic-program-generation/papers/Yang_2011_FindingCompilerBugs/notes.md` (all 12 page images read by research worker); page images re-read this session for quotes (see below).

1. **sources.yaml:17, :23, :29, :35, :41, :47; SKILL.md:18; tool-choices.md:7, 11, 13, 20; common-mistakes.md:9 — ERROR.** Text cited moving-branch URLs (`/master/`, `/main/`). Source: same files at pinned commits above. Fix: replaced with commit-pinned raw URLs; content re-read at those SHAs.
2. **tool-choices.md:11 — ERROR.** Text: "Restrictive `Filter` predicates waste search". Source says more: "too restrictive filter functions will trigger an abort in the framework" ([domains-reference.md, Filter](https://raw.githubusercontent.com/google/fuzztest/1b4e4f0e4c446aca4660c43a28ec1b8d893b6510/doc/domains-reference.md)). Fix: sentence now states the abort with that quote.
3. **tool-choices.md:20 — WARNING.** Text: "avoid exiting and reset state needed for deterministic replay". Source: "should not `exit()` on any input", "Ideally, it should not use any global state" and "Non-determinism can make fuzzing inefficient" ([fuzz-test-macro.md, The property function](https://raw.githubusercontent.com/google/fuzztest/1b4e4f0e4c446aca4660c43a28ec1b8d893b6510/doc/fuzz-test-macro.md)). "Reset state ... for replay" is not in the source. Fix: reworded to the source's contract with quotes.
4. **tool-choices.md:11 — INFO.** "Recursive domains carry a documented recursion-limit warning" is vague. Source: "Recursion limit for recursive domains is not implemented yet" and initial generation "might \"blow up\", leading to resource exhaustion". Fix: quoted the warning.
5. **tool-choices.md:11 — INFO.** "Check ... overflow boundaries in the domain itself" uncited at sentence level. Source `.good` EvenNumber example comment: "Ensure we don't try to produce a value that causes integer overflow". Fix: added quote. The empty-container half has no source sentence; the doc's own FlatMap example uses `InRange(0, s.size() - 1)`, which the skill's advice guards against; kept as design guidance tied to that example, not claimed as doc text.
6. **tool-choices.md:7 — INFO.** Load-bearing Csmith README claims lacked quotes. Added "might contain infinite loops" / "apply timeout to their executions" and "a bug in Csmith itself" from README "Use Csmith".
7. **SKILL.md:8, semantic-environments.md:34, world-program-replay.md:7 — INFO.** SQLite §4.1.3 claims verified: "mutates both the SQL input and the database file at the same time"; it is a libFuzzer structure-aware mutator, not a generator. Fix: added quotes at SKILL.md:8 and world-program-replay.md:7.

Csmith paper page images re-read this session (paper-reader render, `pngs/page-001..004, 007, 009`); remote PDF sha256 `4381d863...0424` equals the local paper-reader `paper.pdf`, so the cited URL is the document read.

8. **world-program-replay.md:5 — ERROR.** Text: "matched implementation-defined choices" cited to "§§2.2–2.5 and 4". Implementation-defined behavior and target equivalence classes are in §2.6 "Design Trade-offs" (p.5): "we can perform differential testing within an equivalence class but not across classes". Fix: citation now §§2.2–2.6 and 4, with that quote.
9. **SKILL.md:8 — WARNING.** Interleaving claim cited §§2.2–2.5; the sentence stating it is the §2 introduction (p.2): "interleave static analysis with code generation in order to produce meaningful test cases". Fix: citation "§2 introduction and §§2.2–2.5" plus quote.
10. **SKILL.md:24 — WARNING.** "avoid optimizing only syntax variety" cited §§2.2, 3.3, 3.5; the paper's syntax-variety statement is §2.6 (p.5): "source-level diversity that is unlikely to improve". Fix: added §2.6 and quotes, including §3.5 "so small as to be a negative result".
11. **SKILL.md:12, 20, 30; semantic-environments.md:5, 18, 22; world-program-replay.md:19, 23 — INFO.** Load-bearing Csmith claims verified against §§2.2–2.5 and §4 page images; added verbatim fragments ("be well formed and have a single meaning", "loops and function calls threaten to invalidate previously validated code", "The resulting programs are small but useless.", "the new code fragment is committed to the generated program", "are rolled back", "destroy the meaning of a program", "was safe when it was generated", "when a loop is closed by adding its back-edge", "introduce undefined behavior", "are forced to be in bounds using the modulo operator").
12. **references/common-mistakes.md:3-10 — ERROR (audit check 6).** Entries were a two-column table with no WRONG/RIGHT/why structure and one moving URL. House style (`bugfinding-campaign/references/common-mistakes.md`) is `## heading`, `**Wrong:**`, `**Better:**`. Fix: converted the same six entries, unchanged in substance, to Wrong/Better/Why sections; each Why carries a verbatim source fragment; URL pinned.
13. **tool-choices.md:11 — WARNING.** "`Map`/`FlatMap` lack ordinary initial-seed support. Reversible variants require their inverse law." Source: Map/FlatMap "don't support initial seeds"; ReversibleMap requires `f(g(y)) == y`, ReversibleFlatMap requires "`y` is in `f(g(y))`" — the two laws differ. Fix: stated both laws.
14. **tool-choices.md:13 — INFO.** Mode distinction verified; added quotes "for a short time without sanitizer and coverage instrumentation" and "until it finds a crash or it is explicitly terminated by the user". Prerequisites (Linux or macOS experimental, Clang) and C++17 (`build --cxxopt=-std=c++17`) verified.
15. **sources.yaml:6-9, 34-39 — WARNING.** sections_used did not list Csmith §2 intro or §2.6 (now cited) and gave FuzzTest quickstart section names that are not headings. Fix: listed the actual sections/headings used.
16. **Procedural sentences (SKILL.md:12 first three sentences, :26, :32 routing; tool-choices.md:3, :22; world-program-replay.md:29; semantic-environments.md:26-32) — INFO.** These are plugin instructions/routing or an explicitly labelled illustrative design, not factual claims about a source; left uncited, consistent with the foundation skill. No claims cut.

## Pinned URLs

SHAs resolved with `gh api repos/<org>/<repo>/commits/<branch> --jq .sha` on 2026-11-07; content fetched at those SHAs before citing.

- `csmith-project/csmith/master/README.md` -> `.../0cdc710315cfee9035e22ef4363ca479270d1934/README.md`
- `csmith-project/csmith/master/COPYING` -> `.../0cdc710315cfee9035e22ef4363ca479270d1934/COPYING`
- `google/fuzztest/main/doc/domains-reference.md` -> `.../1b4e4f0e4c446aca4660c43a28ec1b8d893b6510/doc/domains-reference.md` (one link keeps `#flat-map`)
- `google/fuzztest/main/doc/quickstart-bazel.md` -> `.../1b4e4f0e4c446aca4660c43a28ec1b8d893b6510/doc/quickstart-bazel.md`
- `google/fuzztest/main/doc/fuzz-test-macro.md` -> `.../1b4e4f0e4c446aca4660c43a28ec1b8d893b6510/doc/fuzz-test-macro.md`
- `google/fuzztest/main/LICENSE` -> `.../1b4e4f0e4c446aca4660c43a28ec1b8d893b6510/LICENSE`

6 distinct URLs pinned (sources.yaml plus every inline occurrence in SKILL.md, tool-choices.md and common-mistakes.md). Not pinnable: `https://www.sqlite.org/testing.html` (no versioned URL published; page footer read this session: "last updated on 2026-04-21"); Csmith PDF is a fixed author preprint (sha256 matched the paper-reader copy).

## Validation

```text
python C:/Users/Q/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/bugfinding/skills/semantic-program-generation
Skill is valid!
--- moving urls
none
--- inline urls not in yaml
ok https://raw.githubusercontent.com/csmith-project/csmith/0cdc710315cfee9035e22ef4363ca479270d1934/COPYING
ok https://raw.githubusercontent.com/csmith-project/csmith/0cdc710315cfee9035e22ef4363ca479270d1934/README.md
ok https://raw.githubusercontent.com/google/fuzztest/1b4e4f0e4c446aca4660c43a28ec1b8d893b6510/LICENSE
ok https://raw.githubusercontent.com/google/fuzztest/1b4e4f0e4c446aca4660c43a28ec1b8d893b6510/doc/domains-reference.md
ok https://raw.githubusercontent.com/google/fuzztest/1b4e4f0e4c446aca4660c43a28ec1b8d893b6510/doc/fuzz-test-macro.md
ok https://raw.githubusercontent.com/google/fuzztest/1b4e4f0e4c446aca4660c43a28ec1b8d893b6510/doc/quickstart-bazel.md
ok https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf
ok https://www.sqlite.org/testing.html
--- yaml urls not cited
--- local links
ok references/semantic-environments.md
ok references/tool-choices.md
ok references/world-program-replay.md
ok references/common-mistakes.md
--- diff check
clean
--- trailing bytes
SKILL.md    .  \n
references/common-mistakes.md    .  \n
references/semantic-environments.md    .  \n
references/sources.yaml    "  \n
references/tool-choices.md    .  \n
references/world-program-replay.md    .  \n
   32 SKILL.md
   51 references/common-mistakes.md
   34 references/semantic-environments.md
   55 references/sources.yaml
   22 references/tool-choices.md
   29 references/world-program-replay.md
python yaml check: 8 sources, all fields name/url/type/accessed/sections_used, accessed 2026-11-07 -> "8 True"
```

Audit checks 1-6: frontmatter valid (validator); description matches body (types/live objects/effects/starting state; world+program shrinking); SKILL.md 32 lines; no local link breaks. No changes needed.

## Unverified

- SQLite testing.html is an unversioned page; quoted §4.1.3 text is as served 2026-11-07 and may change.
- tool-choices.md commands (`bazel test`, `bazel run --config=fuzztest`, `csmith -h/-hh`) were not executed; they match the pinned docs only.
- Empty-container advice in tool-choices.md:11 is the skill's inference from the reference's `InRange(0, s.size() - 1)` example, not a statement in FuzzTest docs; worded as such.
- Csmith pages 6, 8 (index), 11-12 not re-read this session; no claim newly added rests on them (notes and earlier reads cover §§3.1-3.2, 5).

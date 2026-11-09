# Draft: JS/TS (Node) extension of coverage-guided-fuzzing and corpus-evolution

Drafter: group A. Status: complete; validation passed (output below). Not committed.

## Inputs read

- `reports/research-js-fuzzing-corpus.md` (all; decisions, mistakes 1-13, sources S1-S19, unverified list).
- `reports/skill-plan-js-web-bugfinding.md:29-30`.
- `plugins/bugfinding/skills/coverage-guided-fuzzing/`: `SKILL.md`, `references/python-jvm.md`, `references/common-mistakes.md`, `references/sources.yaml` (head and tail, schema).
- `plugins/bugfinding/skills/corpus-evolution/`: `SKILL.md`, all four references, `sources.yaml`.
- `reports/draft-coverage-guided-fuzzing.md` (structure; its link/source probe rejects orphan and unused sources, so every new `sources.yaml` entry must be cited inline and vice versa).

## Source re-check (2026-11-09)

Downloaded the Jazzer.js files at pin `f23bc5aeb7a6d50cd6256cfc3be44b868da5e7b1` to the scratchpad and grepped the exact phrases I quote. Confirmed verbatim: `fuzz-targets.md` command format, includes/excludes default, ESM "Requirements" and "not instrumented", "awaited before", crash files "in the current working directory"; `fuzz-settings.md` "only the first directory", "will not save any inputs other than crashes on exit", `-timeout` "will be ignored", regression "Under the hood ... `-runs=0`", Jest default `"regression"`, "only one fuzz test can be run", "first test it finds", `--sync` note, "It is not possible to change or modify the corpus directories", value-profile wording; `architecture.md` "Out of scope: Other runtimes or browser support", "Once a crash is found it logs it on the console and stops", comparison hooks; `bug-detectors.md` "enabled by default", prototype-pollution shortcoming, SSRF module list, `reportFinding` text. Source: `options.ts:517-518` `SUBPROCESS_FLAGS`, `:488` `-runs=0`, `:495` `-timeout=${inSeconds}`, `:432` handle flags; `core.ts:56-60` exit codes, `:102` "Using generated seed"; `corpus.ts:21,23,60-65`; `fuzz.ts:168` `-artifact_prefix`, `:202-203` `<empty>`; `api.ts:26-29` callback exports; `CMakeLists.txt:117-119`; `sanitizer_symbols.cpp:27`; `packages/fuzzer/README.md:4-12`.

Line drift noted: `architecture.md` lines differ from the research by a few lines (e.g. "stops" is line 49, not 46). The edits cite section names, not line numbers, so this does not matter.

Also confirmed a second doc statement the research did not quote: `fuzz-settings.md:824-827` (Jest fuzzing mode) says crash/timeout inputs "will be saved in the regression directory", consistent with `fuzz.ts:168` putting `-artifact_prefix` on the seed (regression) directory.

## Findings and edits (appended as made)

1. **Added `coverage-guided-fuzzing/references/node-jazzerjs.md`.** Sections: route (CLI vs Jest), instrumentation check (includes/excludes, ESM floors, `--dryRun`, Istanbul `--coverage`), async and per-input reset, oracles (five detectors, `reportFinding`, stop on first crash), limits/seeds/artifacts, native addons, platform/floor/maintenance. Follows research decision 4. Corpus directory roles and merge are pointed to `corpus-evolution` (code exists once). Vitiate and chaosbringer left out (decision 7 allows omission). Every quote re-grepped at the pin; extra verifications: `run-all-tests-pr.yaml:48-49` unit-test note, `fuzz-settings.md:155-175` coverage bounding (`-runs=1`, `-max_total_time=N`, `--mode=regression`), `fuzz-targets.md:96-100` (a transpiled module exporting `fuzz` is accepted), `jest-integration.md:260` `--testNamePattern`, `packages/fuzzer/README.md:31` "CMake and the C++ toolchain", npm registry `@jazzer.js/core@4.0.0` engines `>= 14.0.0` and jest-runner peers `jest >=29.0.0` (fetched 2026-11-09), `release.yaml:16,62` five prebuilt addons. Inferences are labelled in the text: un-awaited async work, Jest `beforeEach` once per campaign, native addon has no sanitizer/coverage. The CLI crash-location doc conflict is stated as unresolved.
2. **`coverage-guided-fuzzing/SKILL.md`.** Description now names "Jazzer.js for Node.js/TypeScript" and states "Browser JavaScript has no coverage-guided route here." Lane table gains the row `Node.js (CJS, ESM, TypeScript via Jest) | Node.js with Jazzer.js`; one sentence after the table quotes the architecture doc's "Other runtimes or browser support" out-of-scope line and routes browser UI exploration to the UI event-sequence skill. The pilot sentence adds the Jazzer.js Jest `"regression"` default (decision 3) with a `fuzz-settings.md` link.
3. **`coverage-guided-fuzzing/references/common-mistakes.md`.** Five rows added (research mistakes 1-5), each with a pinned link. The `beforeEach` row is labelled as inference from source.
4. **`coverage-guided-fuzzing/references/sources.yaml`.** 20 entries appended, one per URL cited (the research grouped several URLs per entry; the existing schema has one `url`, so I split them). Types follow names already used in the repo (`official-documentation`, `source-code`, `package-metadata`, `official-release-notes`). Release-date sentence re-sourced from the npm registry `time` map (verified 2.1.0 = 2023-10-23, 4.0.0 = 2026-04-15) because the release page shows only v4.0.0. The v3-skipped quote re-verified via the GitHub releases API. Jest `beforeEach` quote re-verified at `GlobalAPI.md:140`.
5. **`corpus-evolution/references/tool-recipes.md`: new `## Jazzer.js (Node.js)` section** (research decision 2 for corpus-evolution chose tool-recipes.md, not a new file). Contents: CLI directory roles, regression and listed-file replay commands (composed only from documented forms: `--mode=regression` at `fuzz-settings.md:224`, corpus positional "as the last argument" at `:56-58`, listed files at `:76-78`), crash location with the doc conflict, Jest directory rules (`fuzz-settings.md:80-125` re-read; it also documents that the regression directory is used "to save all crashing inputs"), seed-only regression replay (`corpus.ts:60-65`). **Deviation from research decision 2, stated:** the research proposed showing `npx jazzer <target> -- -merge=1 SELECTED FULL` and a `-minimize_crash` command. I did not print those as command blocks. Reason: no doc, test or example shows them, and I could not confirm from `cli.ts`/`options.ts` how CLI corpus positionals and post-`--` arguments are ordered in the final libFuzzer argv (`cli.ts` declares the positional; the concatenation point was not found in what I read). The text states the source fact (`SUBPROCESS_FLAGS` includes `merge`, `minimize_crash`; wrapper script) and that passing them after `--` is source-supported but unexercised, pilot on copies.
6. **`corpus-evolution/references/selection-and-retention.md`.** One paragraph in "Spend selection compute deliberately": `NODE_V8_COVERAGE` and `v8.takeCoverage()` (quotes re-verified at Node v26.13.0 `cli.md:4517-4523`, `v8.md:568-575`), c8 as reader (`README.md:1,44` at `ae5a0cf`), the per-input replay recipe labelled unexecuted inference, and the distinction from Jazzer.js's Babel counters. One sentence in "Revisit meaning" on the v4.0.0 FDP breaking changes (both quotes re-verified via the GitHub releases API). Research decision 4 (an FDP sentence in `exchange-and-replay.md`) was optional; skipped to keep the change small, since the FDP consume-order point now sits in "Revisit meaning".
7. **`corpus-evolution/SKILL.md`.** Description adds "including Jazzer.js corpora and V8 coverage selection for Node.js"; the recipe list adds "Jazzer.js (Node.js) corpus and regression directories".
8. **`corpus-evolution/references/common-mistakes.md`.** Three sections added (research mistakes 6-8) in the file's Wrong/Better/Why format. Mistake 7 now cites the doc line (`fuzz-settings.md`: regression directory used "to save all crashing inputs") plus the existing libFuzzer merge quote.
9. **`corpus-evolution/references/sources.yaml`.** 10 entries appended in the file's quoted/inline-list style. Research decision 6 listed S5, S11 and S12 too; they are not cited in corpus-evolution, so adding them would create unused inventory entries, which the house probe rejects. Left out.
10. **Research mistakes 9-12 not added as table rows.** Their content is in `node-jazzerjs.md` prose (no-corpus-dir loss, `--timeout` vs `-timeout`, first finding only, published vs root Node floor); the plan asked for mistakes 1-5 in that table. Mistake 13 is the FDP sentence in item 6.

## Files changed

- `plugins/bugfinding/skills/coverage-guided-fuzzing/SKILL.md` (modified; 42 lines)
- `plugins/bugfinding/skills/coverage-guided-fuzzing/references/node-jazzerjs.md` (new; 39 lines)
- `plugins/bugfinding/skills/coverage-guided-fuzzing/references/common-mistakes.md` (modified; +5 rows)
- `plugins/bugfinding/skills/coverage-guided-fuzzing/references/sources.yaml` (modified; +20 entries, 54 total)
- `plugins/bugfinding/skills/corpus-evolution/SKILL.md` (modified)
- `plugins/bugfinding/skills/corpus-evolution/references/tool-recipes.md` (modified; new Jazzer.js section)
- `plugins/bugfinding/skills/corpus-evolution/references/selection-and-retention.md` (modified)
- `plugins/bugfinding/skills/corpus-evolution/references/common-mistakes.md` (modified; +3 sections)
- `plugins/bugfinding/skills/corpus-evolution/references/sources.yaml` (modified; +10 entries, 18 total)
- `reports/draft-js-fuzzing-corpus.md` (this report)

Nothing committed or pushed. No other skill, manifest, README or agent-note touched.

## Validation output

`python quick_validate.py` failed first with the system Python: `ModuleNotFoundError: No module named 'yaml'` (both skills). Re-ran the same script with an ephemeral PyYAML through uv (nothing installed into a system Python):

```text
uv run --no-project --with pyyaml python C:/Users/Q/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/bugfinding/skills/coverage-guided-fuzzing
Skill is valid!
uv run --no-project --with pyyaml python C:/Users/Q/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/bugfinding/skills/corpus-evolution
Skill is valid!
```

Link and source-inventory probe (scratchpad `probe.py`, written with Write; it parses `sources.yaml`, collects every inline `](...)` target in each skill's `.md` files, normalizes fragments, and checks local paths exist):

```text
plugins/bugfinding/skills/coverage-guided-fuzzing
  sources 54 duplicate urls 0
  cited-not-in-inventory []
  inventory-not-cited []
  bad local links []
plugins/bugfinding/skills/corpus-evolution
  sources 18 duplicate urls 0
  cited-not-in-inventory []
  inventory-not-cited []
  bad local links []
```

The only relative link added is `native-runners.md` from `node-jazzerjs.md` and `references/node-jazzerjs.md` from `SKILL.md`; both resolve.

```text
git diff --check -- plugins/bugfinding/skills/coverage-guided-fuzzing plugins/bugfinding/skills/corpus-evolution
[no output, rc=0]
```

`git diff --check` does not cover the untracked `node-jazzerjs.md`; a grep for trailing spaces/tabs in it found none, and it ends in exactly one newline.

## Remaining unverified items

- Nothing was installed or run against a target. Every command is composed from documented forms; none was executed.
- `-merge=1` / `-minimize_crash=1` through Jazzer.js: source recognizes them (`options.ts:517-518`) and builds a wrapper script; no doc, test or run confirms the result, the argv ordering of CLI corpus positionals vs post-`--` flags, or Windows `.bat` behaviour.
- CLI crash-artifact location: `fuzz-targets.md` says cwd, `fuzz-settings.md` CLI mode text says "regression directory". Stated as a conflict in both skills.
- Jest `beforeEach` once per discovery campaign: inference from `fuzz.ts` structure plus Jest docs; labelled inference.
- Un-awaited async work failing under a later input: inference; labelled.
- Native addons get no sanitizer and no coverage from Jazzer.js: inference from build flags and the Babel-only instrumentation; labelled. Whether any UBSan standalone runtime is linked was not checked (`CMakeLists.txt:117-118` comment).
- Per-input `v8.takeCoverage()` replay for selection, and V8 coverage of Babel-instrumented code: unexecuted; labelled.
- npm `@jazzer.js/jest-runner` 4.0.0 on Jest 30.4+: the research's inference from a post-release fix commit. Not stated in the skills beyond "Check the installed version and its Jest compatibility".
- Not included at all (research marks them unverified or optional): Vitiate, chaosbringer, `honggfuzz-node`, Node 14-18 end-of-life status, 2024/2025 commit counts, the Jest `<empty>`-input doc/source mismatch, edge-ID comparability across seeds.


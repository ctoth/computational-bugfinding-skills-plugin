# Improve JS fuzzing and corpus additions (commit 95d71f3)

Scope: sentences added in `git show 95d71f3 -- plugins/` to `coverage-guided-fuzzing` and `corpus-evolution`, checked against the pinned sources they cite.

## Findings

### F1 coverage-guided-fuzzing/references/node-jazzerjs.md:39 — ERROR (claim not in cited source)
- Said: "the monorepo root's `>= 20.11.0` covers developing Jazzer.js ([Jazzer.js PR workflow, unit-test note](…/f23bc5a…/.github/workflows/run-all-tests-pr.yaml))".
- Source: run-all-tests-pr.yaml at f23bc5a contains no `20.11`; its note (lines 48-49) is "Node 14 runtime compatibility is covered by end-to-end tests." / "Unit tests require npm 7+ (workspaces) which Node 14 doesn't ship." The `>= 20.11.0` is in the root package.json (https://raw.githubusercontent.com/CodeIntelligenceTesting/jazzer.js/f23bc5aeb7a6d50cd6256cfc3be44b868da5e7b1/package.json, lines 75-77: `"engines": { "node": ">= 20.11.0", "npm": ">= 7.0.0" }`), while packages/core/package.json says `"node": ">= 14.0.0"`.
- Fix: cite the root package.json for the number, keep the PR workflow for the development framing; added the root package.json to sources.yaml.

### F2 coverage-guided-fuzzing/references/node-jazzerjs.md:25 — WARNING (claim rests on uncited source)
- Said: "A broad `catch` in the target hides ordinary exceptions, though not detector findings", cited only to bug-detectors.md, which states the try/catch escape for `reportFinding` in "Writing Custom Bug Detectors" only.
- Source: built-in detectors call `reportAndThrowFinding` (packages/bug-detectors/internal/command-injection.ts:19,55 at f23bc5a); packages/core/finding.ts:62-93 (https://raw.githubusercontent.com/CodeIntelligenceTesting/jazzer.js/f23bc5aeb7a6d50cd6256cfc3be44b868da5e7b1/packages/core/finding.ts): `reportFinding` "Save the first finding reported by any bug detector" in a global (`setJazzerJsGlobal(firstFinding, cause)`), and `reportAndThrowFinding` "Save the first finding ... and throw it to potentially abort the current execution". The saved global is what survives a catch.
- Fix: added the finding.ts link to the sentence and a sources.yaml entry. No wording change.

### F3 coverage-guided-fuzzing/references/node-jazzerjs.md:39, sources.yaml — INFO (unpinned URLs, left as is)
- `https://registry.npmjs.org/@jazzer.js/core` and `/jest-runner` are the live package documents; values checked 2026-11-09: dist-tags latest 4.0.0, 4.0.0 engines `{'node': '>= 14.0.0', 'npm': '>= 7.0.0'}`, time 2.1.0 `2023-10-23T13:27:32.250Z`, 4.0.0 `2026-04-15T14:10:03.857Z`; jest-runner 4.0.0 peerDependencies `{'@types/jest': '>=29.0.0', 'jest': '>=29.0.0'}`. The publish-date claim needs the full document (`time` is not in the per-version document), so no pinned replacement exists for it; the text already names version 4.0.0 and access date. Not changed.

## Validation (2026-11-09, after fixes)

- `quick_validate.py plugins/bugfinding/skills/coverage-guided-fuzzing`: "Skill is valid!" exit 0.
- `quick_validate.py plugins/bugfinding/skills/corpus-evolution`: "Skill is valid!" exit 0.
- Relative links in every .md of both skills resolve (none broken).
- Cited URLs vs sources.yaml URLs, both directions: corpus-evolution exact match; coverage-guided-fuzzing exact match (the only difference my script printed was `pkg.go.dev/cmd/go@go1.27.3#hdr-Testing_flags`, because the script dropped the fragment on the Markdown side only; go-rust.md:13 and sources.yaml:89 carry the same full URL).
- `git diff --check`: no output, exit 0.

## Files changed

- plugins/bugfinding/skills/coverage-guided-fuzzing/references/node-jazzerjs.md (F1, F2)
- plugins/bugfinding/skills/coverage-guided-fuzzing/references/sources.yaml (two entries added: finding.ts, root package.json)

## Checked and entailed (no change)

All Jazzer.js sources fetched at f23bc5aeb7a6d50cd6256cfc3be44b868da5e7b1 on 2026-11-09.

- docs/fuzz-settings.md: every quote in node-jazzerjs.md, coverage-guided-fuzzing common-mistakes.md rows 1 and 3, SKILL.md mode clause, corpus-evolution tool-recipes.md and common-mistakes.md matches exactly (corpus lines 48-85, 118-124; coverage 159-174; dryRun 420; fuzzerOptions 607-609; JAZZER_FUZZ 759; mode 806-827, 840; sync 885-886; timeout 925).
- docs/fuzz-targets.md: `fuzz`/`Buffer` (30-31), Promise/callback (64-77), TypeScript note (105-108), ESM requirements (117-119) and Jest "Any supported Node.js" (159), crash files in cwd (218-219), command format (224), includes/excludes text (238), `--` forwarding (242), "substantial overhead" (265-266).
- docs/architecture.md: "Other runtimes or browser support" under "Out of scope:" (14-16); Babel counters/comparison hooks (35-37); "Once a crash is found it logs it on the console and stops." (49).
- docs/jest-integration.md "Executing Jest fuzz tests" (258-261): one fuzz test in fuzzing mode, `--testNamePattern`.
- packages/jest-runner/corpus.ts: seed-directory comment (23-24), `.cifuzz-corpus` (21), `inputsPaths()` adds generated directory only when `_coverage` (60-66).
- packages/jest-runner/fuzz.ts: fuzzing mode is one `globals.test` with `-artifact_prefix=` seed directory (163-173); regression is a `describe` with `<empty>` plus one test per `inputsPaths()` entry (186-215).
- packages/core/options.ts: `SUBPROCESS_FLAGS = ["fork", "jobs", "merge", "minimize_crash"]` under "These flags cause libFuzzer to spawn subprocesses." (517-518), wrapper script (504-548), `-runs=0` in regression (486-489), `Math.ceil(timeout / 1000)` (494-495).
- packages/core/core.ts: exit codes 0/77/78 (54-61), `INFO: Using generated seed:` when `-seed=` absent (92-104).
- packages/core/callback.ts: "before or after each fuzz target invocation" (22-23); api.ts re-exports both register functions (27-28).
- docs/bug-detectors.md: "enabled by default", `--disableBugDetectors=<pattern>` (5-7); detector list and modules (13-117); "_Shortcoming:_" (71-73); `reportFinding` try/catch and first-finding text (144-148).
- packages/fuzzer/README.md: "falls back to compilation" (5), "blocks the event loop" (11), "CMake and the C++ toolchain" (31). CMakeLists.txt: `-DCOMPILER_RT_SANITIZERS_TO_BUILD=""` (119), builds only the `fuzzer_no_main` target. sanitizer_symbols.cpp:27 "Suppress libFuzzer warnings about missing sanitizer methods".
- .github/workflows/release.yaml:62 expected five prebuilts (darwin arm64/x64, linux arm64/x64, win32 x64); README.md:131-138 lists Linux x86_64, macOS x86_64/arm64, Windows x86_64 (no Linux arm64).
- v4.0.0 release body (via `gh api .../releases/tags/v4.0.0`): both BREAKING FDP lines (12-13) and "_Releases v3.x.x were used by the commercial version and are therefore skipped._" (23).
- Node v26.13.0 cli.md:4517-4526 (`NODE_V8_COVERAGE=dir`, propagation) and v8.md:559-572 (`v8.takeCoverage()`); c8 README title line 1 and `--temp-directory` default line 44; Jest GlobalAPI.md:138-140 `beforeEach`; LibFuzzer.md:295 "that trigger new code coverage".
- The "like JVM Jazzer `PER_TEST`" analogy matches the skill's own python-jvm.md:29-31 (cited there to Jazzer Lifecycle.java).
- sources.yaml `sections_used` in both skills match what the text uses from each source.
- No paper claims were added in 95d71f3 to these two skills, so no paper-reader notes were needed.

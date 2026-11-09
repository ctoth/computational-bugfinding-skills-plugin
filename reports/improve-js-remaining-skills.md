# Improve pass: JS additions in bf6546b (remaining skills)

Scope: every sentence added under `plugins/` by commit bf6546b ("Add gated ExpoSE, JS reduction and triage evidence, JS lane inventory and no-route notes"), checked against the cited pinned sources.

Status: done. Accessed 2026-11-09. 10 findings (1 ERROR, 7 WARNING, 2 INFO); 9 fixed in place, F10 no edit. Not committed or pushed. `scripts/check_package.py` not run (CI runs it).

## Validation

- `uv run --no-project --quiet --with pyyaml python C:/Users/Q/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/bugfinding/skills/<skill>`: "Skill is valid!" for all ten (symbolic-concolic-execution, failure-reduction, evidence-based-triage, bugfinding-campaign, semantic-program-generation, native-memory-instrumentation, deterministic-simulation, crash-consistency-testing, bounded-model-checking, liveness-testing).
- Relative links: every non-http markdown link in the ten skill directories resolves (script parsed `](...)` targets, resolved against the file's directory): `broken_rel=[]` for all ten.
- Cited URLs vs sources.yaml, both ways: exact match for symbolic-concolic-execution, failure-reduction, native-memory-instrumentation, deterministic-simulation, crash-consistency-testing, bounded-model-checking, liveness-testing. Remaining differences are `#fragment` only, on URLs not added by bf6546b: evidence-based-triage (go.dev/doc/security/fuzz/#..., llvm.org HowToSubmitABug.html#..., LibFuzzer.html#...), bugfinding-campaign (releases.llvm.org/23.1.0/docs/LibFuzzer.html#options), semantic-program-generation (fuzztest domains-reference.md#flat-map); each base URL is in sources.yaml.
- `git diff --check -- plugins/ reports/improve-js-remaining-skills.md`: no output, exit 0.

## Files edited

- plugins/bugfinding/skills/symbolic-concolic-execution/references/expose-javascript.md (F1, F2, F3)
- plugins/bugfinding/skills/symbolic-concolic-execution/references/common-mistakes.md (F3, F4)
- plugins/bugfinding/skills/symbolic-concolic-execution/references/sources.yaml (F2, F3, F4: fork package.json entry; Config.js and Center.js sections_used)
- plugins/bugfinding/skills/failure-reduction/references/tool-recipes.md (F5, F6)
- plugins/bugfinding/skills/failure-reduction/references/common-mistakes.md (F5)
- plugins/bugfinding/skills/failure-reduction/references/sources.yaml (F5: FuzzerDriver.cpp entry)
- plugins/bugfinding/skills/evidence-based-triage/references/maintainer-handoff.md (F7)
- plugins/bugfinding/skills/evidence-based-triage/references/triage-decisions.md (F8)
- plugins/bugfinding/skills/evidence-based-triage/references/common-mistakes.md (F9)
- plugins/bugfinding/skills/evidence-based-triage/references/sources.yaml (F7, F8: trace-viewer line, TestConfig entry)

## Findings

### F1 symbolic-concolic-execution/references/expose-javascript.md:22 — WARNING (misstatement)
- Said: "ExpoSE prints `[!] <error>` and an `expoSE replay` line per error".
- Source: Distributor.js at ec03edf (https://raw.githubusercontent.com/ExpoSEJS/ExpoSE/ec03edf85f883248612b1d498c6a7d9189d16d6f/Distributor/src/Distributor.js) lines 66-75: `item.errors.forEach((error) => console.log(`[!] ${error.error}`)); if (item.errors.length != 0) { console.log(`[!] ${item.replay}`); }` — one replay line per path that has errors, not one per error.
- Fix: "and, for each path with errors, one `expoSE replay` line".

### F2 symbolic-concolic-execution/references/expose-javascript.md:18 — WARNING (units missing; resolves the EXPOSE_MAX_TIME conflict)
- Said: "Set limits explicitly: `EXPOSE_MAX_TIME` defaults to `"2h"`, `EXPOSE_TEST_TIMEOUT` (per test case) to `"40m"`" — no unit for a value the reader is told to set.
- Source: README at ec03edf line 58: "`EXPOSE_MAX_TIME` - The time (in milliseconds) to limit the total execution"; Config.js at ec03edf (https://raw.githubusercontent.com/ExpoSEJS/ExpoSE/ec03edf85f883248612b1d498c6a7d9189d16d6f/Distributor/src/Config.js) lines 23-43, `timeToMS`: suffix `"s"`, `"m"`, `"h"` multiply by 1000/60000/3600000, `else { return Number.parseInt(timeString); }`; lines 47-48 defaults `"2h"` and `"40m"`. No conflict: a bare number is milliseconds (README), a suffixed string is seconds/minutes/hours (Config.js). `EXPOSE_MAX_TIME=300` therefore means 300 ms.
- Fix: one clause: "values take an `s`, `m` or `h` suffix, and a bare number is milliseconds".

### F3 symbolic-concolic-execution/references/expose-javascript.md:12 and common-mistakes.md:17 — WARNING (citation does not entail "Babel 6")
- Said: "runs Babel 6 with the `es2017` and `es2015` presets", cited only to esnstrument.js.
- Source: esnstrument.js at c2961c4 lines 38-41 has `babel.transform(code, { retainLines: true, presets: ['es2017','es2015'] })` and line 1881 `acorn.parse(..., ecmaVersion: 6 })`, but no Babel version. The version is in the fork's package.json (https://raw.githubusercontent.com/ExpoSEJS/jalangi2/c2961c4374fa5f5fb35d114b98621cbe38b5c85f/package.json): `"babel-core": "^6.26.3"`, `"babel-preset-es2015": "^6.24.1"`, `"babel-preset-es2017": "^6.24.1"`, `"acorn": "3.1.0"`. ExpoSE pins that fork commit in Analyser/package.json: `"jalangi2": "git+https://github.com/ExpoSEJS/jalangi2.git#c2961c4374fa5f5fb35d114b98621cbe38b5c85f"`. Claim true; citation incomplete.
- Fix: added the fork package.json link beside the instrumenter link in expose-javascript.md step 2, and a sources.yaml entry.

### F4 symbolic-concolic-execution/references/common-mistakes.md:15 — INFO (imprecise)
- Said: "the exit code is the error count".
- Source: Center.js at ec03edf lines 158-159: `if (errors.length) { this._errors += 1; }`; Distributor.js line 41 passes `this._errors` as `errors` and line 114 `process.exitCode = errors`. The count is paths with at least one error, not individual errors.
- Fix: "the exit code is the number of paths with errors".

### F5 failure-reduction/references/common-mistakes.md:75 and tool-recipes.md:53 — WARNING (claim stronger than source)
- Said: libFuzzer "minimizes the provided crash input" toward any crash" (common-mistakes) and "because the libFuzzer section above minimizes toward any crash" (tool-recipes).
- Source: LibFuzzer.md at 635f308 (https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/llvm/docs/LibFuzzer.md) lines 303-305 say only "If 1, minimizes the provided crash input. Use with -runs=N or -max_total_time=N to limit the number of attempts." — nothing about "any crash". The implementation, FuzzerDriver.cpp at the same commit (https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/compiler-rt/lib/fuzzer/FuzzerDriver.cpp) lines 353-361 and 485-492, compares `DEDUP_TOKEN:` lines from the two runs and stops with "CRASH_MIN: mismatch in dedup tokens (looks like a different bug). Won't minimize further"; when neither run prints a token both are `""` and any crash is accepted. GitHub code search (`gh api search/code`, 2026-11-09) finds no `DEDUP_TOKEN` or `dedup_token` in CodeIntelligenceTesting/jazzer.js, so for Jazzer.js the "any crash" behaviour is an inference, and for libFuzzer in general it is wrong when a sanitizer prints dedup tokens.
- Fix: both sentences now say libFuzzer keeps a smaller input that crashes, comparing only sanitizer `DEDUP_TOKEN` lines, and that no Jazzer.js source emitting one was found (inference), citing FuzzerDriver.cpp; FuzzerDriver.cpp added to sources.yaml.

### F6 failure-reduction/references/tool-recipes.md:59 — WARNING (claim stronger than source)
- Said: "**Shrink Ray** runs `shrinkray is_interesting.sh my-test-case` and has no JavaScript-specific format."
- Source: Shrink Ray README at 5fe6ee1 (https://raw.githubusercontent.com/DRMacIver/shrinkray/5fe6ee135d732e4b7758b3dbe3d91428523018fb/README.md) lines 141-146 list special support for "C and C++", "Python", "JSON", "Dimacs CNF format for SAT problems"; but lines 121-122 say a reduction may download "a tree-sitter grammar for the input's language", so the README does not establish that no JavaScript-aware pass exists. Only the README list is evidence.
- Fix: "and its README's special-format list does not include JavaScript".

### F7 evidence-based-triage/references/maintainer-handoff.md:22 and sources.yaml — ERROR (source is another language's section)
- Said: "A Playwright trace is written to `trace.zip` under `test-results` and opens with `npx playwright show-trace path/to/trace.zip` ([Playwright trace viewer])"; sources.yaml: "trace.zip in test-results (line 147)".
- Source: trace-viewer.md at 95e5dca (https://raw.githubusercontent.com/microsoft/playwright/95e5dca31981bcd0970165853fcc713269d2433a/docs/src/trace-viewer.md) line 147, "This will record the trace and place it into the file named `trace.zip` in your `test-results` directory.", sits under "## Recording a trace / * langs: python" (line 134-135) and describes `pytest --tracing on`. The JS section (lines 74-132) says only "This will produce a `trace.zip` file for each test that was retried" (line 94). The JS location comes from class-testconfig.md at 95e5dca (https://raw.githubusercontent.com/microsoft/playwright/95e5dca31981bcd0970165853fcc713269d2433a/docs/src/test-api/class-testconfig.md) line 324: `outputDir` "Defaults to `<package.json-directory>/test-results`", and line 338: "a unique subdirectory inside the [`property: TestConfig.outputDir`] is created". `show-trace` command (line 25) is correct.
- Fix: the sentence now says `trace.zip` ([trace viewer]) is written in the test's subdirectory of `outputDir`, default `test-results` ([Playwright TestConfig]); sources.yaml trace-viewer entry corrected to line 94 and a TestConfig entry added.

### F8 evidence-based-triage/references/triage-decisions.md:25 — WARNING (citation does not contain the name)
- Said: "the run exits with an error only under `failOnFlakyTests` (CLI `--fail-on-flaky-tests`, "default: false")", cited to test-retries-js.md and test-cli-js.md.
- Source: neither cited file contains `failOnFlakyTests`; test-cli-js.md line 85 has "`--fail-on-flaky-tests` | Fail if any test is flagged as flaky (default: false)". The config property is in class-testconfig.md at 95e5dca lines 113-119: "## property: TestConfig.failOnFlakyTests / * since: v1.52 ... Whether to exit with an error if any tests are marked as flaky." Claim true; citation incomplete.
- Fix: added the TestConfig link to that sentence's citation.

### F9 evidence-based-triage/references/common-mistakes.md:63 — WARNING (claim stronger than source)
- Said: "flaky tests fail the run only with `--fail-on-flaky-tests`".
- Source: class-testconfig.md at 95e5dca lines 113-119: `TestConfig.failOnFlakyTests` "Whether to exit with an error if any tests are marked as flaky. ... Also available in the command line with the `--fail-on-flaky-tests` option." The config property is a second route; "only with" the CLI flag excludes it.
- Fix: "... only with `--fail-on-flaky-tests` ([Playwright CLI]) or the `failOnFlakyTests` config ([Playwright TestConfig])".

### F10 liveness-testing/references/runtime-and-model-routes.md:5 — INFO (no edit)
- Said: "`--process-timeout` exits with code 124 and prints "which resources were keeping the event loop alive"".
- Source: Node cli.md at v26.13.0 (https://raw.githubusercontent.com/nodejs/node/v26.13.0/doc/api/cli.md) lines 2653-2654 confirm the quote; lines 2673-2675 add "If the main thread does not respond within two seconds ... Node.js exits immediately without printing the stack trace and resources." The sentence's conclusion ("observe a process that did not exit, not a progress contract") does not depend on the exception, so no edit.

## Sentences checked and entailed (no finding)

All quotes, flags, versions and line references below were compared against the fetched pinned source in this session.

- symbolic-concolic-execution: ExpoSE README lines 3-8 (description, Jalangi2/Z3, "`node` version v21.7.2 (other versions may work but are not tested)", clang/make/Python 3); commits API: pinned ec03edf is master HEAD, committed 2024-07-02T21:48:12Z; package.json `"node": "^21.7.2"`; .nvmrc `v10.22.0`; `expoSE` shebang `#!/usr/bin/env bash`; Dockerfile `FROM debian:latest`; trees API (not truncated): `tests/async/settimeout.js` only async test, 168 `tests/regex/` entries, `tests/es6/{const,let}.js`, no promise/async-await/ESM test path; tests use `var S$ = require("S$")`; symbols.js `assume` throws `NotAnErrorException`, `symbol`, `pureSymbol`, `assert(value, desc)`; Analyser/src/SymbolicExecution.js lines 65-69 ignore `NotAnErrorException` (path discarded, not an error); Config.js defaults `"2h"`, `"40m"`, CPU count, JSON off; Distributor.js summary line 111 and `process.exitCode = errors` line 114; Center.js "Exit code non-zero" (line 167) and "Error extracting final output - a fatal error must have occured" (line 195); Spawn.js `kill(this._pid, "SIGKILL")` on timeout; scripts/play `--analysis bin/Analyser.js`; Analyser/package.json pins jalangi2 at c2961c4 (matches the cited fork commit). SKILL.md line 12 and the description line are worded as a gate ("if it fails, report that no supported JavaScript backend exists for the target"), a bounded negative.
- failure-reduction: Jazzer.js fuzz-targets.md line 224 CLI shape and line 242 forwarding; options.ts lines 517-518 `SUBPROCESS_FLAGS = ["fork", "jobs", "merge", "minimize_crash"]` with comment "These flags cause libFuzzer to spawn subprocesses", lines 504-515 wrapper script; Jazzer.js docs mention no crash minimization (only "Minimal ESM fuzz target" headings match "minim"); fuzz-settings.md lines 73-78 "run them once and exit"; Perses README line 23 and lines 79-80, line 77 "It should return **0**"; Lithium README lines 22 and 39 quotes exact; Shrink Ray lines 97, 109-112 ("This is enabled by default", "about 2.7GB"), 128 `--no-llm`; Playwright CLI line 104 "Run each test `N` times"; retries line 36 and line 83.
- evidence-based-triage: Playwright retries lines 36, 63, 82-84; CLI lines 85, 104, 106; TestOptions.trace lines 713-732 (`sources` "Defaults to true", `dom` "record network activity", `retain-on-failure` "A failed run's trace is kept even when a later retry passes"); trace table lines 176-184 ("Fails, then passes on retry": `on-first-retry` -> "first retry"); trace-viewer line 25 `npx playwright show-trace path/to/trace.zip`; playwright-trace SKILL.md frontmatter "Inspect Playwright trace files from the command line"; Jest JestObjectAPI lines 1185-1207 `logErrorsBeforeRetry`; Jest CLI lines 345-353 (`--randomize`, seed displayed) and 425 (`--seed=<num>`); Vitest retry.md line 8, test.md lines 152-159 `repeats`, sequence.md lines 15 and 139; Node cli.md `--cpu-prof`/`--heap-prof` "before exit" (lines 921-922, 1779-1780), `--process-timeout` added v26.11.0 and "are still written" (lines 2643, 2670-2671), `--report-uncaught-exception` "Report is not generated if the uncaught exception is handled" (line 2885), `--report-on-fatalerror` (2797-2818), `--test-randomize`/`--test-random-seed` added v26.1.0, "printed in the test summary and can be reused with `--test-random-seed`" (3263, 3277, 3284-3285); report.md lines 499-501 "By default this is not set and the environment variables are included".
- bugfinding-campaign: Jest Configuration.md line 8 `jest.config.js|ts|mjs|mts|cjs|cts|json`, line 140 `"jest"` key, line 1227 `projects`, line 2263 testMatch default (`__tests__` and `spec|test`); Vitest index.md line 13 lookup order and line 15 `test` property; include.md line 8 default; Node test.md lines 731-748 default patterns and `--no-strip-types`; Playwright test-configuration-js.md testDir/retries/trace/projects and testMatch row (lines 19-94); fast-check package names `@fast-check/jest`, `@fast-check/vitest`; Stryker config-file.md lines 62-67, configuration.md line 545 default `'command'` and line 552 "just runs all tests for all mutants"; Jazzer.js jest-integration.md lines 23-70 (`@jazzer.js/jest-runner`, `testMatch` `*.fuzz.js`, `testRunner`); Playwright retries line 83; Jest `jest.retryTimes`; Vitest `retry`. Anchor `#inventorying-a-javascript-or-typescript-project` resolves to campaign-example.md line 41; `ui-state-exploration` skill directory exists.
- crash-consistency-testing: IndexedDB index.bs line 932 "may consider" ... "a persistent storage medium" exact. "No fault tool for browser storage was found" is worded as a bounded negative.
- deterministic-simulation: chronos README title "Deterministic Simulation Testing (DST) Framework for Node.js & TypeScript"; determined README "A deterministic simulation testing (DST) framework for TypeScript"; GitHub API created_at 2025-04-14T18:24:44Z and 2026-03-22T17:32:23Z. "no maintained, adopted route was verified ... they were not evaluated" is a bounded negative.
- native-memory-instrumentation: Node BUILDING.md line 649 "ASan builds are currently only supported on linux", line 658 `./configure --debug --enable-asan && make -j4`. "no recipe ... was verified, so there is no verified JavaScript route here" is a bounded negative.
- semantic-program-generation: Fuzzilli README line 3 and line 114 (REPRL, "the target engine is modified"); Targets listing includes V8, Spidermonkey, JavaScriptCore. "no generator was verified for Node-level program consumers" is a bounded negative.
- bounded-model-checking: "No bounded model checker for JavaScript or TypeScript source was verified (bounded GitHub search, 2026-11-09)" is a bounded negative; no source cited, none needed.
- liveness-testing: Jest CLI.md lines 206-208 "open handles preventing Jest from exiting cleanly"; Node `--process-timeout` see F10. "Node: no progress checker was verified" is a bounded negative.


# Research: JS/TS extension for `coverage-guided-fuzzing` and `corpus-evolution`

Phase 3 per-skill research, group A. Branch `js-web-bugfinding`. Researcher: Opus 5.5 subagent, 2026-11-09.

Status: complete. Findings J1-J17, then decisions for the drafter, common mistakes, sources inventory and the unverified list. The Edit tool was unavailable in this session, so the file was rewritten whole with Write at each append. Nothing was installed or executed. Every behaviour below comes from docs or source at the pinned commits. Lines marked "Inference" are my reasoning, not source statements. No paper was needed; no claim rests on a paper.

## Inputs read

- `reports/skill-plan-js-web-bugfinding.md:29-30` (rows for both skills).
- `reports/skill-research-js-web-bugfinding.md` F1 (lines 26-46), F7 (lines 120-126), existing-skills table (lines 288-297), unverified list (lines 390-399).
- `plugins/bugfinding/skills/coverage-guided-fuzzing/SKILL.md` (39 lines), `references/python-jvm.md`, `references/common-mistakes.md`, `references/reach-reset-feedback.md`, `references/sources.yaml` (first 60 lines; format).
- `plugins/bugfinding/skills/corpus-evolution/SKILL.md`, `references/selection-and-retention.md`, `references/exchange-and-replay.md`, `references/tool-recipes.md`, `references/common-mistakes.md` (first 30 lines), `references/sources.yaml`.

Pin used throughout: `CodeIntelligenceTesting/jazzer.js` main at `f23bc5aeb7a6d50cd6256cfc3be44b868da5e7b1` (commit date 2026-11-02, "style: apply Prettier 3.9 formatting"). This is the same pin as F1. I re-checked on 2026-11-09 that it is still main HEAD (`gh api repos/CodeIntelligenceTesting/jazzer.js/commits/main`). GitHub API: license `Apache-2.0`, `archived: false`. Raw base used below: `https://raw.githubusercontent.com/CodeIntelligenceTesting/jazzer.js/f23bc5aeb7a6d50cd6256cfc3be44b868da5e7b1/` (abbreviated `JZ/`).

Pin versus the published release: `gh api .../compare/v4.0.0...f23bc5ae` reports main is 31 commits ahead of tag `v4.0.0`, 0 behind. Among docs, the only changes are link-text edits in `README.md`, `docs/fuzz-targets.md` and `docs/jest-integration.md`. `packages/core/core.ts` has one formatting change. So the docs cited below describe the npm 4.0.0 release as well as main. The post-release functional commits are Jest-runner fixes: "fix(jest-runner): support ScriptTransformer location of Jest 30.4+" (2026-10-29) and "fix(jest-runner): remove runner frames from error causes" (2026-11-02). Inference: npm `@jazzer.js/jest-runner` 4.0.0 predates the Jest 30.4+ fix, so a project on Jest 30.4+ may need an unreleased build. Not tested.

## Findings

### J1. CLI shape and entry point (verified, docs and source)

- `JZ/docs/fuzz-targets.md:224`: "jazzer <fuzzTarget> <fuzzerFlags> [corpus...] [-- <fuzzingEngineFlags>]".
- A target module "needs to export a function called `fuzz`, which takes a `Buffer` parameter" (`fuzz-targets.md:30-31`). `-f/--fuzzEntryPoint` renames it (line 237).
- `FuzzedDataProvider` provides typed reads from the Buffer (`fuzz-targets.md:34-48`).
- TypeScript: "Directly executing fuzz targets written in TypeScript is **NOT** supported!" Jest fuzz tests written in TypeScript are supported (`fuzz-targets.md:105-108`).
- Arguments after `--` "are forwarded to the internal fuzzing engine (`libFuzzer`)" (`fuzz-targets.md:242`). Exception: "the libFuzzer option `-timeout` ... will be ignored if passed via `fuzzerOptions`"; Jazzer's own `--timeout` (default 5000 ms) is used instead (`JZ/docs/fuzz-settings.md:607-609, 923-930`). Source: `JZ/packages/core/options.ts:494-495` appends `-timeout=${Math.ceil(timeout/1000)}`, i.e. whole seconds rounded up.
- Instrumentation scope: `-i/--includes` and `-e/--excludes`. The default will "include everything outside the `node_modules` directory. If either of these flags are set the default value for the other is ignored" (`fuzz-targets.md:238`). `fuzz-settings.md:715-717`: once `--includes` is non-default, the `excludes` default changes from `["node_modules"]` to `[]`.
- `--dryRun`: "Disable code instrumentation for fuzzing" (`fuzz-settings.md:416-420`). Its stated uses are debugging and regression mode, "where instrumentation is not required" (lines 422-427).
- Configuration precedence (`fuzz-settings.md:22-30`): defaults < `.jazzerjsrc.json`/Jest config < `JAZZER_*` env vars < CLI args < per-Jest-test options.
- Seed reproducibility (source, `JZ/packages/core/core.ts:86-104`): if `-seed=N` is absent (or 0), Jazzer.js generates one, appends `-seed=<n>` and prints "INFO: Using generated seed: <n>", "so both the instrumentation layer and libFuzzer use the same value — making the entire run reproducible from a single seed." Decision relevance: retain that printed seed with the run record.
- Exit codes (source, `core.ts:52-61`): `Ok = 0`, `Finding = 77` ("libFuzzers crash exit code", also used "for uncaught exceptions and bug detector findings"), `UnexpectedError = 78`.
- One finding ends the run. `JZ/docs/architecture.md:46`: "Once a crash is found it logs it on the console and stops." `JZ/docs/bug-detectors.md:146-148`: "`reportFinding` will only report the first finding from any of the bug detectors and all subsequent findings will be ignored."

### J2. Async targets, `--sync`, and per-input reset (verified, docs and source)

- `fuzz-targets.md:59-60`: "Jazzer.js supports asynchronous fuzz targets out of the box".
- `fuzz-targets.md:64-65`: "The resolution of a `Promise`, returned by a fuzz target, is awaited before the next fuzzing input is provided."
- Done-callback form: if the target takes a callback as its second parameter, "the fuzzer will await its invocation"; calling it with an argument "indicates a failure" (`fuzz-targets.md:73-79`). Source: `core.ts:391` dispatches on `originalFuzzFn.length === 1` (one parameter means promise/value form, otherwise callback form).
- `fuzz-targets.md:89-94`: async is "the default mode ... because it works for all fuzz targets"; `--sync` gives "enhanced performance" for "Solely synchronous code". `fuzz-settings.md:885-886`: "don't use this option if the code under test contains asynchronous parts."
- Mechanism (`JZ/packages/fuzzer/README.md`): "In sync mode (`--sync`), the fuzzer runs on the main thread and blocks the event loop. In the default async mode, libFuzzer runs on a separate native thread and communicates with the JS event loop via a thread-safe function."
- Per-input hooks: the public API exports `registerBeforeEachCallback` and `registerAfterEachCallback` (`JZ/packages/core/api.ts:26-28`). `JZ/packages/core/callback.ts` describes them as "executed before or after each fuzz target invocation". `core.ts:400, 418-435` runs them around every invocation, including after the returned promise settles.
- Jest fuzzing mode hosts the whole campaign in one Jest test: `JZ/packages/jest-runner/fuzz.ts:163-173` registers a single `globals.test(name, async () => ... startFuzzingNoInit(...))`. Regression mode registers one Jest test per input file plus an `<empty>` input (`fuzz.ts:201-215`). Jest's `beforeEach` "Runs a function before each of the tests in this file runs" (`jestjs/jest` `docs/GlobalAPI.md:138-140` at `72614448ecb9d16c58d6474b3091247c14a5c090`).
- Inference from the three facts above: in Jest fuzzing mode a Jest `beforeEach` runs once per campaign, not once per input. In regression mode it runs once per input. This is the same discovery/regression lifecycle split the skill already records for JVM Jazzer `PER_TEST`. Per-input reset in fuzzing mode needs `registerBeforeEachCallback` or reset inside the target.
- Inference (not stated by the docs): with `--sync` the event loop is blocked, so callbacks or promises the target schedules cannot run during that input. In async mode, work the target starts but does not return or await (fire-and-forget promises, timers, event emitters) is not awaited before the next input, so its failures can surface under a later input.

### J3. ESM instrumentation floor (verified, docs)

- `fuzz-targets.md:112-115`: ESM is instrumented "via a Node.js loader hook (`module.register`)". `docs/architecture.md:30-32`: "For CJS modules, a `require` hook (via `istanbul-lib-hook`) intercepts loading. For ES modules (Node >= 20.6), a loader hook registered via `module.register()` intercepts `import` statements in a dedicated loader thread."
- `fuzz-targets.md:117-119`: "**Requirements:** Node.js >= 20.6. Function hooks (bug detectors) additionally require Node.js >= 20.11 (for `transferList` support in `module.register`). On older Node versions, ESM loading still works but modules are not instrumented."
- Comparison table (`fuzz-targets.md:156-165`): the direct CLI uses the loader hook ("native ESM stays ESM", Node >= 20.6, function hooks >= 20.11). The Jest route uses a "Babel transform via `jest.config` — ESM is converted to CJS at test time" and works on "Any supported Node.js". The Jest ESM setup needs `.fuzz.cjs` test files plus `babel-jest` and `@babel/plugin-transform-modules-commonjs` (`fuzz-targets.md:174-199`).
- Decision relevance: on Node 20.6-20.10, direct ESM gets coverage but the function-hook bug detectors do not apply to ESM code. Below 20.6, direct ESM gets no coverage, and the run still proceeds.

### J4. Corpus directories, modes and crash artifacts (verified, docs and source)

- Two directory roles (`fuzz-settings.md:51-56`): "_generated corpus directories_ where inputs that generate new coverage during fuzzing runs are saved" and "_regression corpus directory_ that contains all inputs that ever resulted in a crash."
- CLI:
  - Several corpus directories may be given, "however only the first directory will be used as generated corpus directory, whereas the other directories will be used only on fuzzer startup" (`fuzz-settings.md:58-62`).
  - "If no corpus directory is provided, Jazzer.js will start fuzzing from scratch and will not save any inputs other than crashes on exit" (lines 70-71).
  - Mixing directories and individual inputs "is not allowed" (line 49).
  - Individual files: "It is also possible to provide inputs directly. In that case, Jazzer.js will run them once and exit", e.g. `npx jazzer fuzz-file ./crash-abcdef0123456789 ./my-test.txt` (`fuzz-settings.md:73-78`).
  - Crash artifacts: "Inputs triggering issues, like uncaught exceptions, timeouts, etc., are stored in the current working directory with an auto-generated name" (`fuzz-targets.md:218-219`).
  - Source: CLI corpus arguments become positional libFuzzer arguments (`options.ts:469-475` logs each non-flag argument as "INFO: using inputs from:"). Inference: the CLI has no regression directory of its own; crash placement follows libFuzzer defaults, and `-artifact_prefix=` after `--` changes it (the Jest runner uses exactly that flag, see below).
  - Regression mode "runs each input from the seed and regression corpus directories on the fuzz target once, and then stops. Under the hood, this option adds `-runs=0`" (`fuzz-settings.md:813-817`). Source: `options.ts:486-489` appends `-runs=0` after user options ("The last provided option takes precedence"). The CLI default mode is `"fuzzing"` (`fuzz-settings.md:806`; `options.ts:110`).
  - Doc inconsistency: `fuzz-settings.md:808-811` says that in CLI fuzzing mode "Inputs that trigger a crash will be stored in the regression directory". The CLI section names no regression directory, and `fuzz-targets.md:218-219` says cwd. The source supports `fuzz-targets.md`. Not executed.
- Jest (docs and source):
  - The default mode is `"regression"` (`fuzz-settings.md:819`; `options.ts:118`). Directories are automatic, and "It is not possible to change or modify the corpus directories" (`fuzz-settings.md:85`).
  - Regression/seed dir: `<testfile-dir>/<testfile-name-without-ext>/<describe>/<test_name>` with spaces replaced by `_` (`JZ/packages/jest-runner/corpus.ts:82-108, 125-127`), e.g. `./tests/tests.fuzz/Target/fuzz_test_1` (`fuzz-settings.md:112-116`).
  - Generated dir: `<nearest dir with package.json>/.cifuzz-corpus/<testfile-name>/<describe>/<test_name>` (`corpus.ts:21, 95-104, 111-121`).
  - The source comment on the seed dir (`corpus.ts:23-24`): "Directory containing manually generated user seeds and found fuzzer inputs (crash, timeout, ...)". Seeds and crashes share one directory.
  - Fuzzing mode passes `[generated, seed, ...fuzzerOptions, -artifact_prefix=<seed dir>]` (`fuzz.ts:165-168`). So new-coverage inputs go to the generated dir (first positional), the seed dir is read at startup, and crash/timeout artifacts land in the seed dir.
  - Regression mode runs the fuzz function directly, "as no libFuzzer is required" (`fuzz.ts:208`), on an empty buffer (`fuzz.ts:201-206`) and on `corpus.inputsPaths()`. `inputsPaths()` returns only the seed dir, plus the generated dir only when coverage is on (`corpus.ts:57-63`). So a plain Jest regression run does not replay `.cifuzz-corpus`.
  - "In _fuzzing_ mode, only one fuzz test can be run." Select it with `--testNamePattern`, `skip` or `only`; otherwise "Jazzer.js will run the first test it finds" (`fuzz-settings.md:824-848`).
  - Enabling fuzzing: `JAZZER_FUZZ=1 npx jest tests.fuzz.js` (`fuzz-settings.md:755-760`), `"mode": "fuzzing"` in `.jazzerjsrc.json`, or `JAZZER_MODE=fuzzing` (lines 829-874).
  - `JAZZER_LIST_FUZZTEST_NAMES=1` prints the names from which the corpus directories are derived (`fuzz-settings.md:762-783`).
  - `docs/jest-integration.md:332-334`: "If the described directory structure does not contain inputs for a given test, it will be skipped". But the source always registers the `<empty>` input test (`fuzz.ts:201-206`). That is a doc/source mismatch; the source is newer evidence. Not executed.

### J5. Merge, crash minimization, fork and jobs are passed to libFuzzer (verified, source; behaviour unexercised)

- F1 left open whether Jazzer.js exposes libFuzzer's `-merge`/`-minimize_crash`. Source answer: `JZ/packages/core/options.ts:517-518`: "// These flags cause libFuzzer to spawn subprocesses." `const SUBPROCESS_FLAGS = ["fork", "jobs", "merge", "minimize_crash"];`.
- When any of these is set to a non-zero value, `prepareLibFuzzerArg0` (`options.ts:504-515`) writes a wrapper script (`.sh`, or `.bat` on Windows; `options.ts:544-556`) that re-invokes the same Jazzer.js command line. It passes the script as libFuzzer's `argv[0]` because "In the fork mode, the main libFuzzer process uses argv[0] to spawn further processes". It also creates an `--id_sync_file` so child processes share edge IDs (`options.ts:534-542`).
- Inference: `npx jazzer <target> -- -merge=1 OUT IN` and `npx jazzer <target> -- -minimize_crash=1 -runs=N <crash-file>` take libFuzzer's subprocess paths through that wrapper. Neither command is documented. The only checked-in subprocess example is fork mode: `JZ/tests/fork_mode/package.json`: `"fuzz": "jazzer fuzz --sync --disableBugDetectors='.*' -- -fork=3"`. The tree at the pin has no path containing "merge" or "minimi" (`gh api .../git/trees/<pin>?recursive=1`). A reference must call these source-supported and unexercised, and require a pilot on a copy.
- Always-appended libFuzzer flags (`options.ts:430-432`): `-handle_int=0 -handle_term=0 -handle_segv=0`, because libFuzzer's handling "interferes with the Node.js signal handling". `core.ts:244-246`: "SIGSEGV has to be handled by the native addon and directly stops the process."
- The Jest docs offer no merge or minimize command. Inference: in Jest fuzzing mode a `-merge=1` passed through `fuzzerOptions` would merge into the generated dir (first positional, `fuzz.ts:165-167`), not into a destination the user chooses. Corpus selection is therefore a CLI operation.

### J6. Dictionaries, value profile, comparison feedback (verified, docs)

- libFuzzer `-dict=` passes through: `npx jazzer my-fuzz-file -- -use_value_profile=1 -dict=xml.txt` (`fuzz-settings.md:616-618`). In Jest, use `fuzzerOptions` in `.jazzerjsrc.json` or per test (lines 620-639).
- Jest-only `dictionaryEntries` option on `it.fuzz`: it "can only be set directly in the Jest fuzz test" (`fuzz-settings.md:353-374`). Source: `options.ts:428` merges those entries via `useDictionaryByParams`. The API also exports `addDictionary` (`api.ts:30`).
- `fuzz-settings.md:654-658`: "Jazzer.js provides coverage and comparison feedback to the internally used libFuzzer instance. By setting the libFuzzer flag `-use_value_profile=1`, new values in intercepted compares are treated as new coverage ... but may reduce runtime performance significantly."
- `docs/architecture.md:34-37`: Babel inserts "coverage counters so the fuzzer can detect new code paths, and comparison hooks (for `==`, `!=`, etc.) so the fuzzer can mutate input toward specific values." The API also exports `guideTowardsEquality` and `guideTowardsContainment` (`api.ts:38-39`).
- Fork mode: `idSyncFile` exists "to synchronize edge IDs used during fuzzing by multiple processes (e.g. in fork mode by adding `-fork=1`)". It is internal and "will be overwritten internally" (`fuzz-settings.md:692-702`).

### J7. Jazzer.js's own coverage report is Istanbul, separate from the search signal (verified, docs and source)

- `--coverage` generates a report "upon exit". Reporters come from "the istanbul documentation"; the default is `["json", "lcov", "text", "clover"]` (`fuzz-settings.md:155-163, 257-264`). Source: `core.ts:323-340` builds the report from `global.__coverage__` with `istanbul-lib-coverage`/`istanbul-reports` "in fuzzing mode (non-jest)". Under Jest, "The coverage report for the jest-runner is generated by jest internally".
- "If the fuzzer does not finish, no report will be generated. Pressing CTRL-C ... might result in incomplete coverage reports" (`fuzz-settings.md:165-167`). Recommended: `--mode=regression`, or `-runs=1` / `-max_total_time=N` (lines 167-174).
- "It is recommended to disable coverage report generation during fuzzing, because of the substantial overhead that it adds" (`fuzz-targets.md:264-266`).
- Report scope: "Files matched by the flags `--includes` or `--customHooks`, and not matched by the flag `--excludes`" (`fuzz-targets.md:263-264`).
- With coverage on, Jest regression also replays the generated dir (`corpus.ts:59-61`). So `npx jest --coverage` measures seed plus generated inputs, while plain `npx jest` replays only seeds.

### J8. Bug detectors and `reportFinding` (verified, docs and source)

`JZ/docs/bug-detectors.md`:
- Lines 3-9: "Bug detectors (sometimes also called sanitizers) ... Built-in bug detectors are enabled by default". Disable them with `--disableBugDetectors=<pattern>`; `'.*'` disables all.
- Command injection (lines 11-14): "Hooks all functions of the built-in module `child_process` and reports a finding if the fuzzer was able to pass a command".
- Path traversal (lines 23-26): hooks "relevant functions of the built-in modules `fs` and `path`".
- Prototype pollution (lines 35-99):
  - Assignment/declaration instrumentation is off by default because it "drastically reduces the fuzzer's performance" and "might cause false positives because some libraries (e.g. `lodash`) use `__proto__` to store methods" (lines 64-69).
  - Line 71, "_Shortcoming:_": it "will not detect if the prototype of the object in question has new, deleted, or modified functions" (examples at lines 78-86).
- Remote code execution (lines 101-104): hooks `eval` and `Function`.
- SSRF (lines 114-116): reports "outgoing communication that originates from the built-in libraries `net`, `tls`, `http`, `http/2`, `https`, and `dgram`". Permitted connections are configured in a custom-hooks file (lines 118-126).
- Custom detectors (lines 140-148): use custom hooks and `reportFinding`, which "makes sure that the finding escapes all try/catch blocks along the way"; it "will only report the first finding".
- Source: `core.ts:383-389` takes `clearFirstFinding()` before the target's own error, so a detector finding wins over the target's exception ("errors thrown by bug detectors have higher priority", `core.ts:363-364`).
- Decision relevance: a target `try/catch` that swallows exceptions hides ordinary errors but not `reportFinding` findings. The SSRF detector fires on any outgoing connection from the listed modules unless permitted, so a target that legitimately talks to a local test server needs `addPermittedTCPConnection` (inference from lines 114-126).

### J9. Native addons: no sanitizer and no coverage (verified, source; conclusion is inference)

- F1 left open "whether libFuzzer sanitizers apply to native addons."
- `JZ/packages/fuzzer/CMakeLists.txt` builds compiler-rt from `CodeIntelligenceTesting/llvm-project-jazzer` tag `2023-04-25` with `-DCOMPILER_RT_SANITIZERS_TO_BUILD=""` ("No need to build all the sanitizers"). It builds only the `clang_rt.fuzzer_no_main-*` target ("We only need libfuzzer from the compiler-rt project").
- `JZ/packages/fuzzer/shared/sanitizer_symbols.cpp` defines a stub `__sanitizer_acquire_crash_state` and an empty `__sanitizer_print_stack_trace` under the comment "Suppress libFuzzer warnings about missing sanitizer methods".
- Instrumentation is a Babel source transformation of JS only (`docs/architecture.md:34-37, 76-80`).
- `JZ/packages/fuzzer/README.md` says "Loading the addon initializes libFuzzer and the sanitizer runtime". Inference: given the build flags, this means libFuzzer's own common runtime, not ASan/UBSan.
- Conclusion (inference from the above): Jazzer.js does not apply ASan/UBSan to the user's native addons and inserts no coverage counters into them. A crash inside native code stops the process (`core.ts:244-246`). Native addon memory bugs need a separate native lane: `coverage-guided-fuzzing` native runners, with the addon built under `-fsanitize=fuzzer-no-link`. I found no Jazzer.js doc for that combination.

### J10. Platforms and runtime floor (resolved, source and CI)

- Platforms in `JZ/README.md:131-138`: "Linux x86_64; macOS x86_64 and arm64; Windows x86_64". `docs/architecture.md:9-13` repeats that list.
- The v4.0.0 release notes list "feat: add linux arm64 support". The release workflow builds prebuilt addons on `[ubuntu-latest, ubuntu-24.04-arm, macos-latest, windows-latest]` plus a macOS x86_64 cross-compile. It checks for `fuzzer-darwin-arm64.node fuzzer-darwin-x64.node fuzzer-linux-arm64.node fuzzer-linux-x64.node fuzzer-win32-x64.node` (`JZ/.github/workflows/release.yaml:15-22, 62`). Unit tests run on the same four runner types (`run-all-tests-pr.yaml:42-52`).
- Resolution: five prebuilt targets ship (linux x64/arm64, darwin x64/arm64, win32 x64). The README and architecture doc omit Linux arm64; that is doc drift, not missing support. Windows arm64 is not built, and `CMakeLists.txt` maps Windows to the `x86_64` libFuzzer target only.
- Fallback: the addon "tries to download a prebuilt shared object from GitHub but falls back to compilation on the user's machine if there is no suitable binary" (`packages/fuzzer/README.md`). That needs CMake and a C++ toolchain (same README, build step 4).
- Node floor:
  - Published packages: the npm registry shows `@jazzer.js/core@4.0.0` and `@jazzer.js/jest-runner@4.0.0` with `engines: {"node": ">= 14.0.0", "npm": ">= 7.0.0"}` (registry JSON, fetched 2026-11-09). `jest-runner` peer deps: `jest >=29.0.0`, `@types/jest >=29.0.0`.
  - The root `package.json` (`"name": "jazzer.js"`, the monorepo) declares `"node": ">= 20.11.0", "npm": ">= 7.0.0"` (`JZ/package.json:75-77`). The PR workflow notes: "Node 14 runtime compatibility is covered by end-to-end tests. Unit tests require npm 7+ (workspaces) which Node 14 doesn't ship" (`run-all-tests-pr.yaml:48-49`).
  - The end-to-end job runs the packed package's runtime checks on Node 14 (x64 runners only), 16, 18, 20, 22 and 24 (`run-all-tests-pr.yaml:145-197`).
  - Resolution: the root `>= 20.11.0` applies to developing Jazzer.js itself. The published runtime floor is Node 14 for CJS targets, with feature floors: direct ESM instrumentation needs >= 20.6, and ESM bug detectors need >= 20.11 (J3). README: "Node.js LTS versions ... other versions are best effort only". I did not re-verify which of Node 14-18 are end-of-life.

### J11. Maintenance (re-verified)

- Releases (GitHub API): v2.1.0 on 2023-10-23, then v4.0.0 on 2026-04-15. npm `@jazzer.js/core` publish times: 2.1.0 on 2023-10-23, 4.0.0 on 2026-04-15. `latest` is 4.0.0. The v4.0.0 notes say: "_Releases v3.x.x were used by the commercial version and are therefore skipped._"
- The v4.0.0 notes also list "BREAKING fix(FDP): remove the ability to generate printable strings" and "BREAKING fix(FDP): use UTF-8 when consuming strings". Corpus consequence: see J15.
- Commits since v4.0.0 on main (GitHub API, `since=2026-04-15`): 31. Most are dependency bumps. The functional ones are the Jest 30 fixes (2026-10-29 and 2026-11-02) and "ci(end-to-end): test jazzer CLI across node versions" (2026-04-20). Last commit: 2026-11-02.
- F1 recorded 76 commits in 2024, 0 in 2025 and 81 in 2026; I did not recount.
- Inference: open-source work paused through 2025 and resumed in 2026. There has been one release in 2.5 years. A reference should state the gap and tell the agent to check the installed version and Jest compatibility when it selects the tool.

### J12. Browser code: no in-process coverage-guided fuzzer; one coverage-biased UI crawler exists (verified, docs; search bounded)

- Jazzer.js excludes browsers. `JZ/docs/architecture.md:15-17`: "Out of scope: Other runtimes or browser support". Lines 60-61: "**Consequences**: No other runtime can be supported, this includes browsers."
- F1 found the predecessor `fuzzitdev/jsfuzz` archived (last push 2021-04-30). Not re-checked.
- One web search (2026-11-09) found no byte-input coverage-guided fuzzer for browser application code. It did surface one coverage-*biased* browser crawler:
  - `mizchi/chaosbringer` at `5f69d89ef300cc1fb213301d7942ab17f28c82be`, MIT (GitHub API), not archived, 50 stars, last push 2026-11-08. npm `chaosbringer` 0.15.0 (2026-11-02), `engines.node >=20`, 15 versions since 2026-05-01.
  - `packages/chaosbringer/README.md:29`: "**Coverage-guided action selection** — opt-in V8 precise coverage feedback (CDP `Profiler.takePreciseCoverage`) attributes per-action coverage deltas to the target that fired them and biases subsequent action weights toward targets that historically delivered new code paths."
  - Lines 691-728: weights are multiplied by "`1 + boost · log1p(score)`". It is "Chromium-only (the API is Chrome-DevTools-Protocol-specific)". Reproducibility is "`(seed, coverageFeedback)` rather than `seed` alone", and "a coverage-feedback run is reproducible programmatically ... but not from the CLI alone".
  - The extracted collector `@mizchi/playwright-v8-coverage` 0.2.1: npm `engines.node >=20`, but its README says "Requires Node 22+" (mismatch).
  - Assessment (inference): this is UI-action exploration with a coverage-weighted scheduler over a single maintainer's young project. It keeps no input corpus and does no input mutation, so it is not a lane for `coverage-guided-fuzzing`. It is a candidate for whichever skill owns browser UI event-sequence exploration (open question 1 in `skill-research-js-web-bugfinding.md:387`). Only its README was read.

### J13. Alternative Node route: Vitiate (README only; not recommended as primary)

- `mjkoo/vitiate` at `268bb26d4f6c22e85f0a3c394891a733c1d026f5`: MIT, 2 stars, last push 2026-09-24 (GitHub API). npm `vitiate`/`@vitiate/core` 0.3.1 (2026-06-22), `engines.node >= 18`.
- README line 3: "Coverage-guided fuzzing for JavaScript and TypeScript, built as a Vitest plugin." Line 5: it uses "SWC ... for compile-time instrumentation and LibAFL ... for mutation-driven fuzzing". Lines 86-89: edge counters and comparison tracing; "Inputs that cause uncaught exceptions are saved as crash artifacts under `.vitiate/testdata/` and minimized automatically"; cached corpus in `.vitiate/corpus/` (lines 73-74).
- Platforms (lines 91-99): Linux x86_64/aarch64 (glibc, musl)/armv7, macOS aarch64 only, Windows x86_64; "Requires Node.js 18 or later, Vite 6+, and Vitest 3.1+."
- Assessment (inference): it is relevant to Vitest projects, which Jazzer.js's Jest-only integration does not serve. It is pre-1.0, low-adoption and single-maintainer, and only its README was read. At most, a reference can name it as an unverified alternative. Recheck before any use.

### J14. corpus-evolution: how Jazzer.js maps onto the skill's roles (synthesis of J4-J7)

Existing role table: `corpus-evolution/references/selection-and-retention.md:5-10`.

| Skill role | Jazzer.js CLI | Jazzer.js Jest |
|---|---|---|
| Acquired/generated original | Any extra corpus dir after the first, which is read at startup and not written (`fuzz-settings.md:58-62`) | Seeds placed by hand in the seed dir (`jest-integration.md:380-411`) |
| Confirmed regression / unresolved failure | `crash-*` files in cwd, or wherever `-artifact_prefix=` points (J4) | The same seed dir; crashes land there via `-artifact_prefix` (`fuzz.ts:168`) |
| Active discovery input | The first corpus dir, which libFuzzer writes (`fuzz-settings.md:58-62`) | `.cifuzz-corpus/...` (`corpus.ts:21`) |
| Coverage selection | libFuzzer `-merge=1 DEST SRC...` after `--` (source-supported, undocumented, J5) | None documented; use the CLI over the same function exported as a CLI target |
| Replay | `--mode=regression` or listed files (`fuzz-settings.md:73-78, 813-817`) | Default `npx jest` replays the seed dir only; `--coverage` adds the generated dir (`corpus.ts:57-63`) |

Decision-relevant consequences:
- In Jest, seeds and crash regressions share one directory (`corpus.ts:23-24`). The skill's distinction between original evidence and confirmed regression has to be kept by file naming or provenance records, not by directory.
- A coverage merge into the Jest seed dir would mix selection output with regression evidence. Merge into a separate destination with the CLI.
- Plain Jest regression never replays `.cifuzz-corpus`. A claim that "the corpus replays clean" needs the generated inputs replayed explicitly (CLI `--mode=regression` over that dir, or `jest --coverage`).
- Exchange: inputs are raw `Buffer` bytes. A `FuzzedDataProvider` harness gives bytes meaning by its consumption order (`fuzz-targets.md:36-48`). Inference: changing the harness's consume sequence changes what every retained file means, which is the same rule the skill states for Go typed corpora.

### J15. corpus-evolution: a real meaning-change example (FDP in v4.0.0)

- The v4.0.0 release notes: "BREAKING fix(FDP): use UTF-8 when consuming strings" and "BREAKING fix(FDP): remove the ability to generate printable strings".
- Inference: a corpus produced against a v2.x `FuzzedDataProvider` harness that consumes strings can decode to different values under v4.0.0. It must be replayed and re-measured on the receiver, not assumed equivalent. This is a concrete instance of `selection-and-retention.md` "Revisit meaning, not just filenames". Not executed.

### J16. c8 / `NODE_V8_COVERAGE`: independent measurement for coverage-diverse selection (re-verified)

- c8 at `bcoe/c8` `ae5a0cf4349b92cac910cf7275e724ab7a725b9d` (still main HEAD on 2026-11-09; commit 2026-07-14). `package.json`: version 12.0.0, `"license": "ISC"`, `"node": "^20.19.0 || ^22.12.0 || >=23"`. README line 1: "c8 - native V8 code-coverage". Lines 7-8: it uses "Node.js' built in functionality" and is "compatible with Istanbul's reporters". `--temp-directory` defaults to `process.env.NODE_V8_COVERAGE` (line 44). `--all` adds unloaded files at 0% (lines 55-57). c8 handles inline and on-disk source maps (lines 63-69).
- Node v26.13.0 `doc/api/cli.md:4517-4526`: "When set, Node.js will begin outputting V8 JavaScript code coverage and Source Map data to the directory provided ... `NODE_V8_COVERAGE` will automatically propagate to subprocesses".
- Node v26.13.0 `doc/api/v8.md:559-574`, `v8.takeCoverage()` (added v15.1.0, v14.18.0, v12.22.0): it writes coverage "on demand. This method can be invoked multiple times during the lifetime of the process. Each time the execution counter will be reset and a new coverage report will be written". Also: "When the process is about to exit, one last coverage will still be written to disk unless `v8.stopCoverage()` is invoked".
- Decision relevance:
  - Under `NODE_V8_COVERAGE`, a replay script that calls `v8.takeCoverage()` after each input yields one V8 coverage file per input. That gives a per-input coverage set for set-cover selection that does not depend on libFuzzer's edge IDs. Inference; not executed.
  - Why this is not Jazzer's guidance signal: libFuzzer selects on Babel-inserted edge counters and comparison feedback (`docs/architecture.md:34-37`; J6). V8 precise coverage measures the JS engine's own block/function counts. Their units differ, so a V8-diverse subset and a libFuzzer `-merge` subset need not match. Inference: report which measure chose a subset.
  - Inference: measure on an uninstrumented replay (a plain Node script, or Jazzer.js `--dryRun`) so V8 does not count Jazzer's inserted counter code. Whether V8 coverage of Babel-instrumented code remaps cleanly through Jazzer's source maps is not verified.
  - Inference from the "about to exit" wording: a process killed by a native signal may never write its final coverage file. Per-input `takeCoverage()` limits that loss.

### J17. Existing community skills: overlap (bodies read)

- `trancee/skills` `jazzer/SKILL.md` at `69d1eb5911bcfb885f77e1912699e4e85dfb4f72` (repo has no license in the GitHub API). Its description says: "Installs, integrates, runs, and troubleshoots Jazzer coverage-guided JVM fuzzing ... Don't use for Jazzer.js, non-JVM fuzzers". JS overlap: none, by its own exclusion. Its JVM content (PER_TEST lifecycle, regression first, `JAZZER_FUZZ=1`) overlaps this plugin's existing `python-jvm.md`, which is outside this task.
- `bedkillerspacex-boop/codex-skill-library` `javascript-fuzz-targets/SKILL.md` at `eed9fd05579890130b25214473a7970a5b4d776a` (no license in the GitHub API). It is a generic checklist ("Pure function boundary; catch expected errors", "Time-boxed local runs; nightly longer", "Minimize crashes"). Its only command is a commented `npm i -D @jazzer.js/core` plus an `rg` and a fast-check one-liner. It names "honggfuzz-node", which I did not verify. It cites no sources and covers none of: modes, ESM floor, async/`--sync`, corpus directory roles, bug detectors, native-addon limits.
  - Overlap: generic harness hygiene only.
  - Conflict: its "catch expected errors" is fine, but a broad catch would hide ordinary findings (J8). The plugin reference should state the narrower rule and not repeat the checklist.

## Decisions for the drafter

### `coverage-guided-fuzzing`

1. `SKILL.md` description: add Jazzer.js with Node named, e.g. "... cargo-fuzz, Atheris, Jazzer, Jazzer.js (Node.js) or FuzzTest ...". The plan row `skill-plan-js-web-bugfinding.md:29` requires that Node is named.
2. `SKILL.md` "Select the actual lane" table: add the row "Node.js (CJS, ESM, TypeScript via Jest) | [Node.js with Jazzer.js](references/node-jazzerjs.md)". Add one sentence after the table: there is no in-process coverage-guided route for browser code (Jazzer.js puts browsers "Out of scope", J12); browser UI exploration belongs to the skill that owns UI event sequences.
3. `SKILL.md` pilot paragraph: it already lists the regression defaults of Go, Jazzer and FuzzTest. Add Jazzer.js's Jest default (`"regression"`, `fuzz-settings.md:819`) to that sentence rather than a new paragraph.
4. New `references/node-jazzerjs.md`, in the style of `python-jvm.md`, kept to what changes decisions:
   - Two routes: CLI (`jazzer <target> [flags] [corpus...] -- <libFuzzer flags>`) and Jest (`it.fuzz`, `JAZZER_FUZZ=1`, one fuzz test per fuzzing run).
   - Instrumentation check: include/exclude defaults and the `node_modules` rule; ESM floors (20.6 coverage, 20.11 detectors), with uninstrumented ESM below the floor; `--dryRun` means no feedback; TypeScript only through Jest.
   - Async: returned promise or done-callback awaited; `--sync` only for wholly synchronous code; un-awaited work escapes the input.
   - Reset: Jest fuzzing is one Jest test, so Jest `beforeEach` runs once per campaign. Use `registerBeforeEachCallback` or in-target reset (J2).
   - Oracles: uncaught exception or rejection; the five detectors with their limits (prototype-pollution shortcoming, SSRF permitted connections); `reportFinding` escapes `try/catch`; first finding only; exit code 77.
   - Limits: `--timeout` (ms, rounded up to seconds) not `-timeout`; `-max_total_time`/`-runs` after `--`; record the printed `-seed`.
   - Artifacts: CLI crash files in cwd, or `-artifact_prefix`; Jest crash files in the seed dir. Replay a file with `npx jazzer <target> <file>` or plain `npx jest`.
   - Native addons: no sanitizer, no coverage (J9). Route them to the native runners.
   - Platform/floor/maintenance block (J10, J11): five prebuilt targets; published floor Node 14 (CJS); root `>= 20.11` is dev-only; 2025 gap; Jest 30.4+ fix unreleased in 4.0.0.
   - Keep corpus-directory semantics short here and point to `corpus-evolution` for roles and merge (code exists once).
5. `references/common-mistakes.md`: add rows 1-5 below.
6. `references/sources.yaml`: add entries S1-S9 and S11-S13 below.
7. Do not add Vitiate or chaosbringer as lanes (J12, J13). At most, name Vitiate in one line as unverified.

### `corpus-evolution`

1. `SKILL.md` "Run the selected native operation" list: add "Jazzer.js corpus/regression directories" to the recipe list. No description change is needed for selection; optionally add "Jazzer.js" if the drafter wants Node visible.
2. `references/tool-recipes.md`: new `## Jazzer.js` section containing:
   - The J14 table in prose or compact table form.
   - `npx jazzer <target> --mode=regression <dirs>` and listed-file replay.
   - Merge via `npx jazzer <target> -- -merge=1 SELECTED FULL`, stated as source-supported (`options.ts:517-518`), undocumented and unexercised. Pilot on copies and keep originals.
   - Crash minimization via `-minimize_crash=1 -runs=N` on the same footing.
   - Jest constraints: directories cannot be changed; seeds and crashes share the seed dir; plain regression skips `.cifuzz-corpus`.
3. `references/selection-and-retention.md`:
   - Add the V8 measurement route (J16) as the coverage-diverse selection option that is independent of libFuzzer features, and state that it is a different measure from the search signal.
   - Add the FDP v4.0.0 change (J15) as one sentence in "Revisit meaning".
4. `references/exchange-and-replay.md`: add one sentence on the FDP consumption order (J14 last bullet), parallel to the Go typed rule. Optional; the Go paragraph already carries the principle.
5. `references/common-mistakes.md`: add mistakes 6-8 below.
6. `references/sources.yaml`: add S2, S3, S5, S7, S8, S10, S11, S12, S13.

## Common mistakes with evidence

1. **"`npx jest` passed, so the fuzz test fuzzed."** Jest mode defaults to `"regression"` (`fuzz-settings.md:819`). Use `JAZZER_FUZZ=1` with exactly one selected fuzz test (`fuzz-settings.md:824-848`).
2. **"ESM target, Node 18, coverage is growing."** Below Node 20.6, direct ESM "modules are not instrumented" (`fuzz-targets.md:117-119`). Detectors on ESM need 20.11. Either use the Jest/Babel route or upgrade, and check that coverage reaches target modules.
3. **"`--sync` is faster, use it everywhere."** "don't use this option if the code under test contains asynchronous parts" (`fuzz-settings.md:885-886`). In sync mode the fuzzer "blocks the event loop" (`packages/fuzzer/README.md`).
4. **"Jest `beforeEach` resets state for every mutated input."** Fuzzing mode is one Jest test (`fuzz.ts:163-173`); regression is one test per input (`fuzz.ts:201-215`). Use `registerBeforeEachCallback` (`callback.ts`, `api.ts:26-28`) or in-target reset.
5. **"Bug detectors are sanitizers, so native addon memory errors are covered."** The addon build sets `-DCOMPILER_RT_SANITIZERS_TO_BUILD=""` and stubs sanitizer symbols (`CMakeLists.txt`; `sanitizer_symbols.cpp`). Instrumentation is Babel-on-JS (`architecture.md:34-37`).
6. **"Corpus replays clean under `npx jest`."** Plain regression replays only the seed dir (`corpus.ts:57-63`). `.cifuzz-corpus` is included only with coverage on. Replay the generated dir explicitly.
7. **"Run a coverage merge over the Jest seed directory."** That directory holds "manually generated user seeds and found fuzzer inputs (crash, timeout, ...)" (`corpus.ts:23-24`). Merging there can drop crash regressions, because libFuzzer merge keeps inputs that add coverage (existing skill citation). Merge into a separate destination with the CLI.
8. **"The c8 report shows which inputs guided the fuzzer."** c8 reads V8 coverage (`NODE_V8_COVERAGE`); libFuzzer guidance comes from Babel counters and compare hooks (`architecture.md:34-37`). They are different measures. Jazzer.js's own `--coverage` is a third, Istanbul-based report (`fuzz-settings.md:257-264`).
9. **"No corpus dir needed for a quick run."** Without one, Jazzer.js "will not save any inputs other than crashes on exit" (`fuzz-settings.md:70-71`). The discovered corpus is lost.
10. **"`-- -timeout=30` sets the per-input timeout."** It "will be ignored"; use `--timeout` in ms (`fuzz-settings.md:607-609`; `options.ts:494-495`).
11. **"The fuzzer will list every bug it found."** It stops on the first finding (`architecture.md:46`). `reportFinding` reports only the first (`bug-detectors.md:146-148`).
12. **"Root `package.json` says Node >= 20.11, so Jazzer.js needs 20.11."** Published packages declare `>= 14.0.0`, and CI runtime-checks Node 14-24. The root floor is for the monorepo's npm workspaces (`run-all-tests-pr.yaml:48-49`).
13. **"Corpus from a Jazzer.js 2.x FDP harness is still equivalent."** v4.0.0 made FDP string consumption UTF-8 and removed printable-string generation (release notes, both marked BREAKING). Replay and re-measure.

## Sources inventory entries

Format matches the existing `sources.yaml` (`name`, `url`, `type`, `accessed`, `sections_used`). All accessed 2026-11-09.

- S1 `Jazzer.js README` — `JZ/README.md` — official-documentation — Quickstart; Using test framework integration; ESM note; Supported Architectures.
- S2 `Jazzer.js fuzz targets and CLI` — `JZ/docs/fuzz-targets.md` — official-documentation — Creating a fuzz target; Fuzz target execution modes; TypeScript; ESM support (requirements, direct vs Jest table, Jest ESM setup); Running the fuzz target (command format, parameter table); Coverage report generation.
- S3 `Jazzer.js fuzzing settings` — `JZ/docs/fuzz-settings.md` — official-documentation — Configuration options (precedence); corpus; coverage; coverageReporters; dictionaryEntries; disableBugDetectors; dryRun; excludes; fuzzerOptions (`-timeout` note, value profile); idSyncFile; includes; JAZZER_FUZZ; JAZZER_LIST_FUZZTEST_NAMES; mode; sync; timeout.
- S4 `Jazzer.js Jest integration` — `JZ/docs/jest-integration.md` — official-documentation — Executing Jest fuzz tests (fuzzing mode, regression mode); Manually adding regression tests.
- S5 `Jazzer.js bug detectors` — `JZ/docs/bug-detectors.md` — official-documentation — all five detectors; Prototype Pollution shortcoming; Writing Custom Bug Detectors.
- S6 `Jazzer.js architecture` — `JZ/docs/architecture.md` — official-documentation — Constraints (browser out of scope); Components and Interactions (CJS/ESM hooks, Babel counters and compare hooks; stop on first crash); Decisions (no browser runtime).
- S7 `Jazzer.js core options source` — `JZ/packages/core/options.ts` — source-code — `buildFuzzerOption` (always-appended handle flags); `optionDependentParams` (`-runs=0`, `-timeout`); `SUBPROCESS_FLAGS` and wrapper script; defaults (`mode`).
- S8 `Jazzer.js core source` — `JZ/packages/core/core.ts` — source-code — `FuzzingExitCode`; `resolveInstrumentationSeed`; SIGSEGV comment; `processCoverage`; `asFindingAwareFuzzFn`.
- S9 `Jazzer.js callbacks and API source` — `JZ/packages/core/callback.ts`, `JZ/packages/core/api.ts` — source-code — `registerBeforeEachCallback`/`registerAfterEachCallback`; exported API.
- S10 `Jazzer.js Jest runner corpus and modes` — `JZ/packages/jest-runner/corpus.ts`, `JZ/packages/jest-runner/fuzz.ts` — source-code — seed/generated directory derivation; `inputsPaths`; `runInFuzzingMode` (`-artifact_prefix`); `runInRegressionMode` (`<empty>` input).
- S11 `Jazzer.js native addon build` — `JZ/packages/fuzzer/CMakeLists.txt`, `JZ/packages/fuzzer/shared/sanitizer_symbols.cpp`, `JZ/packages/fuzzer/README.md` — source-code — compiler-rt fetch with `COMPILER_RT_SANITIZERS_TO_BUILD=""`; platform libFuzzer targets; sanitizer stubs; sync vs async threading; prebuilt/fallback build.
- S12 `Jazzer.js platform and Node floor evidence` — `JZ/package.json`, `JZ/packages/core/package.json`, `JZ/.github/workflows/release.yaml`, `JZ/.github/workflows/run-all-tests-pr.yaml`, `https://registry.npmjs.org/@jazzer.js/core`, `https://registry.npmjs.org/@jazzer.js/jest-runner` — source-code / package-registry — engines; prebuilt matrix; end-to-end Node 14-24 checks; jest-runner peer deps.
- S13 `Jazzer.js v4.0.0 release` — `https://github.com/CodeIntelligenceTesting/jazzer.js/releases/tag/v4.0.0` — release-notes — What's Changed (ESM, linux arm64, SSRF and eval sanitizers, BREAKING FDP changes); v3 skipped note.
- S14 `Jest Global API beforeEach` — `https://raw.githubusercontent.com/jestjs/jest/72614448ecb9d16c58d6474b3091247c14a5c090/docs/GlobalAPI.md` — official-documentation — `beforeEach(fn, timeout)`.
- S15 `c8 README and package.json` — `https://raw.githubusercontent.com/bcoe/c8/ae5a0cf4349b92cac910cf7275e724ab7a725b9d/README.md` (and `package.json`) — official-documentation — title; CLI options (`--temp-directory`, `--all`); source maps. License ISC; engines.
- S16 `Node.js NODE_V8_COVERAGE` — `https://raw.githubusercontent.com/nodejs/node/v26.13.0/doc/api/cli.md` — official-documentation — `NODE_V8_COVERAGE=dir`; Coverage output; Source map cache.
- S17 `Node.js v8.takeCoverage` — `https://raw.githubusercontent.com/nodejs/node/v26.13.0/doc/api/v8.md` — official-documentation — `v8.takeCoverage()`.
- S18 (only if J12 is cited) `chaosbringer coverage-guided action selection` — `https://raw.githubusercontent.com/mizchi/chaosbringer/5f69d89ef300cc1fb213301d7942ab17f28c82be/packages/chaosbringer/README.md` — official-documentation — feature list line 29; "Coverage-guided action selection" section.
- S19 (only if J13 is cited) `Vitiate README` — `https://raw.githubusercontent.com/mjkoo/vitiate/268bb26d4f6c22e85f0a3c394891a733c1d026f5/README.md` — official-documentation — intro; how it works; Platform Support.

## Unverified list

- Nothing was installed or run. Every command in this report is from docs or source, not execution.
- `-merge=1` and `-minimize_crash=1` through Jazzer.js: source recognizes them and builds a subprocess wrapper (`options.ts:517-556`). No doc, test or execution confirms the result, including on Windows (`.bat` wrapper) or in async mode.
- The CLI crash-artifact location: `fuzz-settings.md:808-811` and `fuzz-targets.md:218-219` disagree. The source reading favours cwd (libFuzzer default). The exact file-name scheme (`crash-<hash>`, `timeout-<hash>`) was not re-read from libFuzzer.
- Whether a Jest regression run with no seed files is skipped (`jest-integration.md:332-334`) or still runs the `<empty>` test (`fuzz.ts:201-206`).
- The Jest `beforeEach`-once-per-campaign conclusion (J2) is an inference from source structure plus Jest docs; not executed.
- Whether the async-mode failure of un-awaited work surfaces under a later input (J2) is an inference.
- `README.md` "initializes libFuzzer and the sanitizer runtime" versus `COMPILER_RT_SANITIZERS_TO_BUILD=""`: I read this as libFuzzer's common runtime only. Whether any UBSan standalone runtime is linked was not verified. The CMake comment mentions "the UBSan standalone runtime is built by default" but the build target is only `clang_rt.fuzzer_no_main-*`.
- Whether the `seed` passed to `Instrumentor` (`core.ts:109-121`) affects edge IDs, and so whether libFuzzer features are comparable across runs. `edgeIdStrategy.ts` was not read.
- V8 coverage of Babel-instrumented code and source-map remapping through Jazzer.js (J16); the per-input `takeCoverage()` replay recipe is not executed.
- Whether npm `@jazzer.js/jest-runner` 4.0.0 fails on Jest 30.4+ (inferred from the post-release fix commit).
- End-of-life status of Node 14-18 was not re-verified.
- Commit counts for 2024/2025 (from F1) were not recounted.
- `fuzzitdev/jsfuzz` archived status (from F1) was not re-checked.
- The browser search was one web query plus primary checks of two hits. "No byte-input coverage-guided browser fuzzer" is bounded, not exhaustive. chaosbringer and Vitiate were assessed from READMEs only; their code and behaviour are unverified.
- "honggfuzz-node", named by the community skill, was not checked.
- Licenses: `trancee/skills` and `bedkillerspacex-boop/codex-skill-library` have no license in the GitHub API. Their content was read only to judge overlap and must not be copied.

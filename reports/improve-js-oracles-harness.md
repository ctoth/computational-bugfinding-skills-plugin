# Improvement pass: JS/TS additions to correctness-oracles and harness-sensitivity

Commit under review: "Add JS observation channels and Node test-harness probes" (branch js-web-bugfinding).

Status: done. 6 findings fixed in place (0 ERROR, 6 WARNING). Sources fetched 2026-11-09 from the pinned raw URLs.

## Findings

### F1 correctness-oracles SKILL.md:23, references/common-mistakes.md:43 and :49, references/javascript-observation-channels.md:9 — WARNING (claim stronger than source)
- Said: with an `uncaughtException` handler installed, Node's process "will exit with 0" (stated unconditionally in four places).
- Source: Node process.md at 18b32a3b (v26.13.0, `src/node_version.h` 26.13.0 release), "Event: 'uncaughtException'" (https://raw.githubusercontent.com/nodejs/node/18b32a3b1552e199a01f1a8d9fd64aa756d3b75b/doc/api/process.md, lines 271-277): "Alternatively, change the [`process.exitCode`][] in the `'uncaughtException'` handler which will result in the process exiting with the provided exit code. Otherwise, in the presence of such handler the process will exit with 0." Exit 0 holds only when the handler leaves `process.exitCode` unset.
- Fix: added "unless the handler sets `process.exitCode`" at each site.

### F2 correctness-oracles references/javascript-observation-channels.md:19 — WARNING (option omitted)
- Said: "With `jest.retryTimes`, "Unhandled rejections owned by a test, `beforeAll`, `beforeEach`, or `afterEach` participate in describe retries""
- Source: Jest 30.5 JestObjectAPI.md at 72614448 (https://raw.githubusercontent.com/jestjs/jest/72614448ecb9d16c58d6474b3091247c14a5c090/website/versioned_docs/version-30.5/JestObjectAPI.md, `jest.retryTimes(numRetries, options?)`): describe retries exist only with the `entireDescribe` option: "`entireDescribe` retries all tests and hooks in the `describe` block where `jest.retryTimes()` is called." The quoted sentence (line 1257) is in that option's paragraph. Plain `jest.retryTimes(n)` "Runs failed tests n-times until they pass", so the "final pass can follow an observed failure" conclusion holds for both, but the quoted rejection rule applies to `entireDescribe` only.
- Fix: sentence now reads "With `jest.retryTimes` a final pass can follow an observed failure, and with its `entireDescribe` option "Unhandled rejections owned by ... participate in describe retries"; read the retry reasons".

### F3 correctness-oracles references/javascript-observation-channels.md:27 — WARNING (wrong identifier)
- Said: "In a development build inside `act`, an uncaught render error is pushed to the act queue and rethrown into the test".
- Source: ReactFiberErrorLogger.js at 61aa00df (= tag v19.3.1, verified via `gh api repos/facebook/react/git/matching-refs/tags/v19.3.1`), `logUncaughtError`: `if (__DEV__ && ReactSharedInternals.actQueue !== null) { // For uncaught errors inside act, we track them on the act and then rethrow them into the test. ReactSharedInternals.thrownErrors.push(error); return; }`. The error goes to `thrownErrors`; `actQueue` is only the condition.
- Fix: "pushed to the act queue" changed to "pushed to `ReactSharedInternals.thrownErrors`".

### F4 correctness-oracles references/sources.yaml (react.dev StrictMode entry) — WARNING (section list incomplete)
- Said: sections_used "Enabling Strict Mode for a part of the app; Fixing bugs found by double rendering in development".
- Source: StrictMode.md at 7594a2b0: the quoted "All of these checks are development-only and do not impact the production build." (line 94) and the list of extra re-render / Effect / ref-callback runs (lines 88-90) are under "Enabling Strict Mode for entire app" (heading line 62), which is not listed.
- Fix: added "Enabling Strict Mode for entire app" to sections_used.

### F5 harness-sensitivity references/control-design.md:15 — WARNING (claim not in cited source)
- Said: BugsJS has "10 server-side Node subjects"; "Limits: Node server code only, no React or browser bugs".
- Source: BugsJS README at 7abbad3e (https://raw.githubusercontent.com/BugsJS/bug-dataset/7abbad3e4df12cd5294110bb5db11b7d5bc758a6/README.md): "This benchmark includes bugs from the following 10 projects: Bower, Eslint, Express, Hessian.js, Hexo, Karma, Mongoose, Node-redis, Pencilblue, Shields". None of the cited files says "server-side"; ESLint (333 of 453 bugs per Projects.csv), Bower and Karma are not server code. The cited Dockerfile (`FROM node:8.16-jessie`) supports "Node.js projects"; "no browser bugs" is not stated anywhere cited.
- Fix: "10 server-side Node subjects" changed to "10 Node.js projects"; limit changed to "the 10 listed Node.js projects only, none of them React".

### F6 harness-sensitivity references/control-design.md:16 — WARNING (overgeneralized from one file; "advisories" overstated)
- Said: the repository "lists 23 vulnerable npm modules with bug reports and advisories"; "Each exploit script runs one crafted input once and prints an execution time, with no assertion or threshold ([test-forwarded.js])".
- Source: README at ccb8d7dc: 23 rows; the Advisory column is "N/A" for 9 of them (14 advisories). All 23 `test-*.js` files at ccb8d7dc were fetched: none contains an assertion, throw, exit or threshold, but test-lodash.js times six inputs, test-content.js and test-string.js two each; utils.js `measureTime` runs `f()` once and prints `"Execution time (hr): %ds %dms"`. "one crafted input" is false for 3 of 23.
- Fix: "with bug reports and advisories" changed to "with bug reports and, for 14 of them, advisories"; "runs one crafted input once and prints an execution time" changed to "runs each crafted input once and prints its execution time".

## Checked and entailed (no change)

- Pins: Node 18b32a3b is v26.13.0 and f7f273a9 is v24.22.2 (`src/node_version.h`, `NODE_VERSION_IS_RELEASE 1`); React 61aa00df is tag v19.3.1 (`packages/react/package.json` 19.3.1; tag ref via gh api); c8 ae5a0cf4 is 12.0.0 with engines `^20.19.0 || ^22.12.0 || >=23`.
- Node: `--unhandled-rejections` modes (cli.md 3660-3687); uncaughtException default "printing the stack trace to `stderr` and exiting with code 1"; uncaughtExceptionMonitor, unhandledRejection "within a turn of the event loop", rejectionHandled "growing-and-shrinking list"; test.md process-isolation exit-code rule, extraneous async activity, randomization (both files and in-file tests, seed print, `--test-random-seed` implies randomization, awaited subtests keep order, not with `--watch`), `--test-isolation=none` text, coverage exclusions and `node:coverage ignore next`; `--test-randomize`/`--test-random-seed` added v26.1.0 and v24.16.0 (CHANGELOG_V24 24.16.0 entry "test_runner: support test order randomization"); `NODE_V8_COVERAGE` "will automatically propagate to subprocesses".
- Jest 30.5: `--waitForUnhandledRejections`, `--randomize` (within a file, jest-circus only), `--seed` suite ordering and rerun tip, `--showSeed`, `--detectOpenHandles` (implies `--runInBand`, `async_hooks`), `--forceExit` caution text, `coverageProvider` (`babel` default or `v8`), `openHandlesTimeout` default 1000.
- Vitest: `dangerouslyIgnoreUnhandledErrors` text and "built-in reporters will still report them"; `onUnhandledError` "no longer affects the result of the test run"; `sequence.shuffle` and `sequence.seed` default `Date.now()` (page says nothing about printing it); coverage V8 provider "Does not work on environments that don't use V8, such as Firefox or Bun", Istanbul "works on any JavaScript runtime".
- React: createRoot callback descriptions and "React will log all errors to the console"; CHANGELOG 19.0.0 introduces `onUncaughtError`/`onCaughtError`, 18.0.0 introduces `onRecoverableError`; `reportGlobalError` branch order; `didWarnUncachedGetSnapshot` module-level guard and the getSnapshot message; `emitPendingHydrationWarnings` is `__DEV__`-only; `throwOnHydrationMismatch` queues the error outside `__DEV__` and `upgradeHydrationErrorsToRecoverable` queues it as recoverable; Component.md boundary exclusions and dev/prod bubbling; StrictMode quotes; useSyncExternalStore quotes.
- Playwright class-page.md: pageerror and console event text, "200 last", default `since-navigation` filter.
- c8 README quotes (`--all`, ignore comments). BugsJS: MIT, 453 bugs, ESLint 333, three revision definitions, Dockerfile `FROM node:8.16-jessie`. ReDoS repo: 23 modules, MIT-style header in scripts, GitHub `license: null`, description "provided for research purpose only".
- Papers (paper-reader notes): Staicu_2018_FreezingWebStudyReDoS/notes.md p.362 "Public benchmark of vulnerabilities and ready-to-use exploits: https://github.com/sola-da/ReDoS-vulnerabilities"; Wang_2017_ComprehensiveStudyRealWorldConcurrency/notes.md: dataset URL on p.2, 404 when checked, references [21]-[42] identify 22 of 57 bugs (p.11). The tcse.cn URL still returned 404 today; the Wayback snapshot contains "Please use the data only for teaching and research purposes" and one `<form>`.
- sources.yaml section names exist as headings in the fetched files (process.md events, createRoot "Error logging in production", class-page.md event/method headings, etc.).

## Validation

- `quick_validate.py plugins/bugfinding/skills/correctness-oracles`: "Skill is valid!" (exit 0).
- `quick_validate.py plugins/bugfinding/skills/harness-sensitivity`: "Skill is valid!" (exit 0).
- Relative links in SKILL.md and references/*.md of both skills: none broken.
- Cited URLs vs sources.yaml `url:` entries (fragments stripped): no URL in the markdown missing from sources.yaml and none in sources.yaml unused, for both skills.
- `git diff --check`: no output, exit 0.
- Not run: scripts/check_package.py (CI runs it). Nothing committed or pushed.


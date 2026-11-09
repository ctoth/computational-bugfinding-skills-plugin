# Research: JS/TS extension of `correctness-oracles` and `harness-sensitivity`

Phase 3 per-skill research, group G. Branch `js-web-bugfinding`. Date 2026-11-09.

## State

- Complete for drafting. Sections: inputs read, findings N1-N9 (Node, test runners, coverage, StrykerJS), R1-R4 (React), P1 (Playwright), K1-K3 (known-defect sources), decisions for the drafter, common mistakes, sources inventory, unverified list.
- The Edit tool was unavailable in this session, so this file was rewritten whole with Write at each append.
- Nothing installed, no tool or test executed, no skills/manifests/README/agent-notes edited, nothing committed or pushed. All facts come from primary documents or source files fetched read-only on 2026-11-09 at the pins stated. Lines marked "Inference" are my reasoning, not source statements.
- No paper was read in this pass. Paper facts come only from the existing paper-reader notes named under Inputs.

## Inputs read

- `reports/skill-plan-js-web-bugfinding.md` lines 36-37 (rows for both skills), 54-58 (Wang 2017 bullet naming the NodeCB dataset and Staicu benchmark as `harness-sensitivity` known-defect sources), 91.
- `reports/skill-research-js-web-bugfinding.md` F7 (lines 120-126), F8 (128-147), F9 (149-169), F10, F11, F14, F15 (233-236).
- `plugins/bugfinding/skills/correctness-oracles/SKILL.md` and `references/{common-mistakes,contract-examples,partial-observations}.md` in full.
- `plugins/bugfinding/skills/harness-sensitivity/SKILL.md` and `references/{common-mistakes,control-design,runtime-integrations}.md` in full. StrykerJS is at `runtime-integrations.md:15-25` (commit `8f24ef0b`, core 10.1.1, Node `>=22.0.0`).
- `reports/research-harness-sensitivity.md` lines 1-40 (evidence-ledger format: URL, access date, quote fragment, finding, decision relevance).
- Paper notes: `C:/Users/Q/code/papers/Wang_2017_ComprehensiveStudyRealWorldConcurrency/notes.md` lines 28, 199 (dataset URL, curl 404 on 2026-11-09, 22 bugs identified by issue URL in refs [21]-[42], p.11); `C:/Users/Q/code/papers/Staicu_2018_FreezingWebStudyReDoS/notes.md` lines 26-29, 43 (benchmark URL; repo contents not checked by the notes).

## Findings

Pin used for all Node quotes: `nodejs/node` tag `v26.13.0` (ref sha `daaa22aeddb87085542376ea1f4854dcea080baf` from the GitHub API), files `doc/api/cli.md`, `doc/api/process.md`, `doc/api/test.md`, `doc/api/globals.md` fetched 2026-11-09 from `raw.githubusercontent.com/nodejs/node/v26.13.0/...`. Where the v24 LTS line matters, tag `v24.22.2` was read.

### N1. `--unhandled-rejections` modes and default (correctness-oracles)

- `doc/api/cli.md:3660-3686`. Default changed to `throw` in v15.0.0 (PR 33021): "Previously, a warning was emitted."
- Modes, quoted:
  - `throw`: "Emit `unhandledRejection`. If this hook is not set, raise the unhandled rejection as an uncaught exception. This is the default."
  - `strict`: "Raise the unhandled rejection as an uncaught exception. If the exception is handled, `unhandledRejection` is emitted."
  - `warn`: "Always trigger a warning, no matter if the `unhandledRejection` hook is set or not".
  - `warn-with-error-code`: "Emit `unhandledRejection`. If this hook is not set, trigger a warning, and set the process exit code to 1."
  - `none`: "Silence all warnings."
  - "If a rejection happens during the command line entry point's ES module static loading phase, it will always raise it as an uncaught exception."
- What it reports: under the default, an unhandled rejection becomes a process crash (exit 1, see N2) only if no `unhandledRejection` listener exists. Under `warn` and `none` nothing fails; under `warn-with-error-code` only the exit code changes.
- What it misses (from the quoted text): in default `throw` mode, any `process.on('unhandledRejection', ...)` listener in the process (application logger, monitoring agent, test runner) replaces the crash with whatever that listener does. "The process did not crash" is therefore not evidence that no rejection went unhandled. The oracle needs the effective mode (flag or `NODE_OPTIONS`) and the installed listeners.
- Timing limit (`doc/api/process.md:175-233`, `rejectionHandled`): `unhandledRejection` fires when no handler is attached "within a turn of the event loop"; a handler attached later emits `rejectionHandled`. The doc calls this "a growing-and-shrinking list of unhandled rejections". The doc's own example (add to a Map on `unhandledRejection`, delete on `rejectionHandled`) keeps only the still-unhandled ones. Jest documents the same hazard from the runner side (N7).

### N2. `uncaughtException`, `uncaughtExceptionMonitor`, `unhandledRejection` listeners (correctness-oracles)

- `doc/api/process.md:249-350`. Default handling is "printing the stack trace to `stderr` and exiting with code 1, overriding any previously set `process.exitCode`." "Adding a handler for the `'uncaughtException'` event overrides this default behavior." "Otherwise, in the presence of such handler the process will exit with 0."
- The `origin` argument is `'uncaughtException'` or `'unhandledRejection'`; the latter when a rejection was raised under `strict` or `throw` (`process.md:258-265`).
- "**It is not safe to resume normal operation after `'uncaughtException'`.**" (warning section, `process.md:325-350`).
- `uncaughtExceptionMonitor` (`process.md:352-397`): emitted before `uncaughtException`; installing it "does not change the behavior"; "The process will still crash if no `'uncaughtException'` listener is installed." This is the documented way to observe without changing the crash outcome. A harness that adds an `uncaughtException` listener just to record errors changes the exit code to 0 and keeps the process running in what the doc calls "an undefined state".
- `unhandledRejection` (`process.md:399-484`): "If an `'unhandledRejection'` event is emitted but not handled it will be raised as an uncaught exception." A no-op `.catch(() => { })` "would prevent the `'unhandledRejection'` event from being emitted". A swallowed rejection therefore leaves no process-level trace; only a state or effect observation can see it.
- Decision relevance: the JS reference should say that exit code 0 means nothing while any `uncaughtException` listener is installed; record through `uncaughtExceptionMonitor` and the `unhandledRejection`/`rejectionHandled` pair; read the effective `--unhandled-rejections` mode before treating a crash or its absence as an outcome.

### N3. node:test: extraneous async activity, isolation, exit-code verdicts (both skills)

- `doc/api/test.md:612-646`: async activity can "outlive the test itself"; the runner "does not delay the reporting of test results in order to accommodate it." A subtest created after its parent finished "is immediately marked as failed". "`uncaughtException` and `unhandledRejection` events originating from a completed test are marked as failed by the `test` module and reported as diagnostic warnings at the top level".
- What it misses (inference from the quoted text): it only sees leaked work that throws, rejects or creates a subtest. A leaked timer or callback that silently mutates shared state after the test finished produces no event, and the next test sees the mutated state. That is order-dependence, which N4 probes.
- Execution model (`doc/api/test.md:852-895`, `doc/api/cli.md:3211-3222`): default `--test-isolation` is `'process'`: "each matching test file is executed in a separate child process", and "If the child process finishes with an exit code of 0, the test is considered passing." With `'none'`, files share one process and "it is possible for tests to interact with each other in ways that are not possible when isolation is enabled".
- Decision relevance: in process-isolation mode a test file's verdict is its exit code, so N1/N2 apply directly: a file that installs an `uncaughtException` listener can exit 0 after an error. For `harness-sensitivity`, cross-file in-memory leakage cannot appear under default isolation; only external state (files, DB, ports) crosses files (inference from the execution-model text).

### N4. Node `--test-randomize` / `--test-random-seed` (harness-sensitivity)

- Versions (correction to the plan row "Node >= 26.1"): `doc/api/cli.md:3260-3290` at v26.13.0 says `added: v26.1.0`; at tag `v24.22.2` the same flags say `added: v24.16.0` (`cli.md:2812-2830`, `test.md:705-708`), and `doc/changelogs/CHANGELOG_V24.md` lists "**test\_runner**: support test order randomization (Pietro Marchini) #61747" under "2026-05-21, Version 24.16.0 'Krypton' (LTS)". The v22.x branch `cli.md` has no `test-randomize` (grep count 0, 2026-11-09). So: Node >= 26.1.0, or 24.16.0 or later on the 24 line; not on 22.
- Behavior (`test.md:760-850`, Stability "1.0 - Early development"): randomizes "both discovered test files and queued tests within each file"; prints "Randomized test order seed: 12345"; `--test-random-seed=<n>` replays "the same randomized order deterministically" and enables randomization by itself; seed is an integer 0 to 4294967295; not supported with `--watch` or `--test-rerun-failures`.
- Documented blind spot: "when subtests are awaited one by one ... the runner keeps declaration order instead of randomizing it." `describe()`/`it()` siblings stay eligible "because sibling tests are enqueued together."
- What a shuffled failure shows: an order-dependent pair, not which test leaked. Keep the failing seed as replay evidence. Inference: combined with N3, under default process isolation file-order shuffling only exposes dependence through external state; in-file order exposes in-memory leakage.

### N5. Coverage from V8: `NODE_V8_COVERAGE`, node:test coverage (harness-sensitivity reachability)

- `doc/api/cli.md:4517-4560`: when `NODE_V8_COVERAGE=dir` is set, Node writes "V8 JavaScript code coverage" and source-map data as JSON files with a `coverage` prefix, an array of `ScriptCoverage` objects under `result`; it "will automatically propagate to subprocesses" and "can be set to an empty string, to prevent propagation."
- node:test coverage (`test.md:897-953`, Stability "1 - Experimental"), flag `--experimental-test-coverage` (`cli.md:1579-1597`): "Node.js core modules and files within `node_modules/` directories are, by default, not included in the coverage report"; test files are excluded by default; `/* node:coverage disable */` and `/* node:coverage ignore next */` comments remove lines from the report. "If no tests are run, a coverage report is not generated."
- What it reports: which functions/blocks V8 executed in this run. What it misses: activation, state change, observation and rejection (the skill's steps 2-5). Reachability inside a dependency is invisible in the node:test report unless `--test-coverage-include` names it, and ignore comments can hide a never-executed producer. A missing report with zero tests run is not "zero coverage".

### N6. c8 (harness-sensitivity reachability)

- Pin: `bcoe/c8` `ae5a0cf4349b92cac910cf7275e724ab7a725b9d` (still main head on 2026-11-09; latest release v12.0.0; npm `latest` 12.0.0 published 2026-07-14). `package.json` engines `"node": "^20.19.0 || ^22.12.0 || >=23"`. The README's "Supported Node.js Versions" section still says "`>= 12`"; the engines field is the stricter, current statement.
- README, "Checking for "full" source coverage using `--all`": "By default v8 will only give us coverage for files that were loaded by the engine." Example: if tests only load `a.js`, "your total coverage could show as `100%` for `a.js` when in fact both `main.js` and `b.js` are uncovered." `--all` (default `false`) loads every file under `--src` that passes include/exclude "with a default of 0% coverage."
- Default `--exclude` is istanbuljs/schema `default-exclude.js` (read at `istanbuljs/schema` master `a9d00f48`): `coverage/**`, `test{,s}/**`, `**/*{.,-}test.{ext}`, `**/__tests__/**`, `**/*.d.ts`, tool config files.
- Ignore comments: `/* c8 ignore next */`, `/* c8 ignore next N */`, `/* c8 ignore start */ ... /* c8 ignore stop */`.
- Decision relevance: c8 answers step 1 (Producer) of the skill's audit only. Without `--all`, a producer file that was never loaded is absent from the report rather than shown at 0%, so a high percentage can hide an unreached producer. Check for ignore comments on the claimed producer. Source maps remap TS/JSX; `--exclude-after-remap` decides whether excludes apply before or after remapping.

### N7. Jest 30.5 (both skills)

- Pin: `jestjs/jest` main `72614448ecb9d16c58d6474b3091247c14a5c090`, docs `website/versioned_docs/version-30.5/{CLI,Configuration,JestObjectAPI}.md`; latest release v30.5.2.
- Order probe: `--randomize` (`CLI.md:345-357`): "Shuffle the order of the tests within a file. The shuffling is based on the seed." Displays the seed; "only supported using the default `jest-circus` test runner." `--seed=<num>` (`CLI.md:425-441`): range `-2147483648` to `2147483647`; "Jest uses the seed internally for shuffling the order in which test suites are run. If the `--randomize` option is used, the seed is also used for shuffling the order of tests within each `describe` block. When dealing with flaky tests, rerunning with the same seed might help reproduce the failure." `--showSeed` prints it. Config `randomize` default `false` (`Configuration.md:1311-1315`).
- Unhandled-rejection reporting: `--waitForUnhandledRejections` / config `waitForUnhandledRejections` (`CLI.md:554-560`, `Configuration.md:2615-2621`): "Gives one event loop turn to handle `rejectionHandled`, `uncaughtException` or `unhandledRejection`. Without this flag Jest may report false-positive errors (e.g. actually handled rejection reported) or not report actually unhandled rejection (or report it for different test case)." "This option may add a noticeable overhead". CHANGELOG line 377: renamed from `--waitNextEventLoopTurnForUnhandledRejectionEvents`.
  - Decision relevance: without this flag, Jest's attribution of an unhandled rejection to a test is documented as unreliable in both directions. An oracle that uses "which Jest test reported the rejection" needs the flag.
- Retries hide flakiness: `jest.retryTimes` (`JestObjectAPI.md:~1235-1259`): "Unhandled rejections owned by a test, `beforeAll`, `beforeEach`, or `afterEach` participate in describe retries." "When test randomization is enabled, each describe block keeps the order selected for its first attempt across all of its retries." Inference: a test that passes on retry had an observed failure that the final status does not show; read the retry reasons, not the pass.
- Leaked handles: `--detectOpenHandles` (`CLI.md:206-208`): "Attempt to collect and print open handles preventing Jest from exiting cleanly." "This implies `--runInBand`, making tests run serially. Implemented using `async_hooks`." "significant performance penalty and should only be used for debugging." `--forceExit` (`CLI.md:243-251`) is "an escape-hatch"; not exiting "means external resources are still being held on to or timers are still pending". `openHandlesTimeout` default `1000` ms prints "a warning indicating that there are probable open handles" (`Configuration.md:1167-1171`).
  - Decision relevance: `--detectOpenHandles` changes the execution (serial, `async_hooks` on), so a flake that disappears under it is not shown fixed. `--forceExit` in a project's config hides leaked handles; read the config before concluding no leak.
- Coverage: `coverageProvider` "Allowed values are `babel` (default) or `v8`" (`Configuration.md:355-357`). Jest's default is Babel instrumentation, not V8; say which provider produced a reachability claim.

### N8. Vitest 5.1 (both skills)

- Pin: `vitest-dev/vitest` main `3a76b87324ecb8d25509cd009aa87fbe56819c39`, latest release v5.1.0; docs under `docs/`.
- Order probe (`docs/config/sequence.md:93-139`): `sequence.shuffle` `boolean | { files?, tests? }`, default `false`, CLI `--sequence.shuffle`; "it may be useful to track tests that accidentally depend on another test run previously." `sequence.shuffle.files` is resolved from the root config only. `sequence.seed` default `Date.now()`, CLI `--sequence.seed=1000`, "Sets the randomization seed, if tests are running in random order." The page does not say the seed is printed; with the `Date.now()` default, a shuffled failure may not be replayable unless the seed was set explicitly (inference; see unverified list).
- Unhandled errors: `dangerouslyIgnoreUnhandledErrors` (default `false`): "Vitest will not fail the test run if there are unhandled errors. Note that built-in reporters will still report them." `onUnhandledError` (since 4.0.0): "When an error is filtered out, it no longer affects the result of the test run." `browser.trackUnhandledErrors` default `true`; disabling it "will completely remove all Vitest error handlers". `docs/guide/common-errors.md:189-191`: an unhandled rejection happens when a promise rejects with no handler "before the microtask queue flushes."
  - Decision relevance: by default Vitest fails the run on unhandled errors. A green run is uninformative about unhandled errors if the config sets `dangerouslyIgnoreUnhandledErrors`, filters in `onUnhandledError`, or disables `browser.trackUnhandledErrors`. Read the config.
- Coverage (`docs/guide/coverage.md:7-121`): providers `v8` (default) and `istanbul`. V8 "requires Javascript runtime that's implemented on top of V8 engine"; "Does not work on environments that don't use V8, such as Firefox or Bun". Since v3.2.0 V8 coverage uses "AST based coverage remapping" said to give reports "identical" to Istanbul. Decision relevance: a reachability check in Vitest browser mode on Firefox or WebKit needs the istanbul provider.

### N9. StrykerJS currency (harness-sensitivity)

- `stryker-mutator/stryker-js`: latest GitHub release `v10.1.1`, published 2026-10-23T19:14:24Z; npm `@stryker-mutator/core` dist-tag `latest` is `10.1.1` (published 2026-10-23T19:18:22Z). Main head on 2026-11-09 is `8f24ef0be3a2119fc44ac48bfce58930ab2c9032` (commit date 2026-10-29), the same commit the existing reference pins.
- Decision: the existing `runtime-integrations.md:15-25` StrykerJS section is current. No change; do not restate it in the JS additions.

### React pins

- Docs: `reactjs/react.dev` main `7594a2b008489121bdf25f97320d11ac0422510e` (still head 2026-11-09), files under `src/content/reference/`. Docs content CC-BY-4.0 per F9.
- Source: `facebook/react` tag `v19.3.1` (`61aa00df822d0eb76d0362eb8b6fdd3527693efe` via `git ls-remote`; `packages/react-dom/package.json` version 19.3.1, license MIT). Files `packages/react-reconciler/src/ReactFiberErrorLogger.js`, `packages/react-reconciler/src/ReactFiberHooks.js`, `packages/shared/reportGlobalError.js`, `CHANGELOG.md`.

### R1. Root error callbacks: `onUncaughtError`, `onCaughtError`, `onRecoverableError` (correctness-oracles)

- Docs (`react-dom/client/createRoot.md:48-50`; same three options on `hydrateRoot.md`, line 46 for `onRecoverableError`): `onCaughtError` is called "when React catches an error in an Error Boundary"; `onUncaughtError` "when an error is thrown and not caught by an Error Boundary"; `onRecoverableError` "when React automatically recovers from errors ... Some recoverable errors may include the original error cause as `error.cause`." `createRoot.md:358`: "By default, React will log all errors to the console."
- Versions (`CHANGELOG.md`): `onRecoverableError` added in 18.0.0 (line 624: "By default, React will use `reportError`, or `console.error` in the older browsers"). 19.0.0 (line 301): "Errors that are not caught by an Error Boundary are now reported to window.reportError. Errors that are caught by an Error Boundary are reported to console.error. We've introduced `onUncaughtError` and `onCaughtError`". So on React 18 only `onRecoverableError` exists.
- Default handlers in source (`ReactFiberErrorLogger.js`, v19.3.1):
  - `defaultOnUncaughtError` calls `reportGlobalError(error)`; in `__DEV__` only, it also `console.warn`s "Consider adding an error boundary to your tree".
  - `defaultOnCaughtError`: in `__DEV__`, `console.error` with "The above error occurred in the <X> component." and "React will try to recreate this component tree from scratch using the error boundary you provided"; in production, `console['error'](error)` with the bare error.
  - `defaultOnRecoverableError` calls `reportGlobalError(error)` only.
  - `logUncaughtError`: `if (__DEV__ && ReactSharedInternals.actQueue !== null)` the error is pushed to `thrownErrors` and returns ("For uncaught errors inside act, we track them on the act and then rethrow them into the test"). So under dev-build `act`, an uncaught render error is rethrown into the test instead of reaching `onUncaughtError`.
  - If a handler throws, the error is rethrown from `setTimeout` (comment cites react issue 13188).
- `reportGlobalError` (`packages/shared/reportGlobalError.js`): uses `reportError` when it is a function ("In modern browsers, reportError will dispatch an error event, emulating an uncaught JavaScript error"); otherwise dispatches a `window.ErrorEvent('error')` if `window.ErrorEvent` exists; otherwise, if `process.emit` exists, `process.emit('uncaughtException', error)` and return; otherwise `console['error'](error)`.
  - `reportError` does not appear in Node's `doc/api/globals.md` at v26.13.0 (grep, no match). Inference, not executed: in plain Node (no jsdom, no browser), React's default uncaught and recoverable handlers take the `process.emit('uncaughtException', error)` branch. That is a plain emit, not a throw, so with no `uncaughtException` listener nothing is printed and the process does not exit. A render error reaching the default handler in plain Node could therefore leave no trace. Needs one executed check before the skill states it.
  - In jsdom, `window.ErrorEvent` exists, so the event is dispatched on the jsdom window (and jsdom's own `reportError`, if any, is unverified).
- What the channel misses: the docs example filters (`if (error.message !== "Known error")`), so a custom handler can drop errors; read the actual handler before trusting silence. Recoverable errors are, by definition, not visible in the rendered UI. Error boundaries do not see errors in "Event handlers", "Server side rendering", "Errors thrown in the error boundary itself", or "Asynchronous code (e.g. `setTimeout` or `requestAnimationFrame` callbacks)" except `startTransition` functions (`react/Component.md:1274-1281`). Those errors take the ordinary JS route (N1/N2 in Node, `pageerror` in the browser).
- Build difference (`react/Component.md:227`): "In development, the errors will bubble up to `window`, which means that any `window.onerror` ... will intercept the errors that have been caught by `componentDidCatch`. In production, instead, the errors will not bubble up". A global error listener therefore sees boundary-caught errors in development builds only.
- Decision relevance: for a React oracle, install all three root callbacks to record (not filter) and keep them in the replay evidence; state the React major (18 has only `onRecoverableError`); say whether the run was a development or production build, because the console text and `window` bubbling differ.

### R2. `console.error` as a channel (correctness-oracles)

- Many React diagnostics are development-only `console.error` calls guarded by `__DEV__`. Verified instances: the `useSyncExternalStore` warnings "The result of getSnapshot should be cached to avoid an infinite loop" and "The result of getServerSnapshot should be cached to avoid an infinite loop" (`ReactFiberHooks.js:1664-1690`, `1763-1769`, inside `if (__DEV__)`); the hydration mismatch warning ("In development mode, React warns about mismatches during hydration", `hydrateRoot.md:58`); the boundary message in `defaultOnCaughtError` (R1).
- These warnings are once per module: `let didWarnUncachedGetSnapshot` is module-level (`ReactFiberHooks.js:186`) and set to `true` after the first warning. Inference: the count of these console errors is not the count of offending components; after the first, the rest are silent for the life of the module.
- In production builds these messages do not exist. A production-build run with a clean console says nothing about these contracts.
- Decision relevance: treat `console.error` as a development-build-only candidate channel; record the build mode; record the first warning, and do not infer "one offender" from one message.

### R3. StrictMode double invocation (correctness-oracles; boundary with schedule-exploration)

- `react/StrictMode.md:87-94`: in development, components "re-render an extra time to find bugs caused by impure rendering", "re-run Effects an extra time to find bugs caused by missing Effect cleanup", "re-run ref callbacks an extra time to find bugs caused by missing ref cleanup", and are checked for deprecated APIs. "**All of these checks are development-only and do not impact the production build.**"
- Scope (`StrictMode.md:123-127`): only the wrapped subtree is checked. "When `StrictMode` is enabled for a part of the app, React will only enable behaviors that are possible in production. For example, if `<StrictMode>` is not enabled at the root of the app, it will not re-run Effects an extra time on initial mount".
- What is double-called (`StrictMode.md:137-141`): component body "(only top-level logic, so this doesn't include code inside event handlers)"; functions passed to `useState`, `set` functions, `useMemo`, `useReducer`; some class methods (`constructor`, `render`, `shouldComponentUpdate`). Effects get "one extra setup+cleanup cycle in development for every Effect" (`StrictMode.md:520`); callback refs the same (`StrictMode.md:842`).
- Observation limit (`StrictMode.md:508`): with React DevTools installed, `console.log` calls in the second render "will appear slightly dimmed", and DevTools offers "a setting (off by default) to suppress them completely." Inference: a log-based oracle can lose second-render output if that setting is on.
- What it misses: event-handler code is not double-invoked; the check is a fixed extra call, not a search over orders; production-only paths (production build, minified names) are outside it.
- Decision relevance: StrictMode is a fixed, development-only oracle for purity and cleanup. A finding needs the observed difference (e.g., duplicated item, connection count not returning to baseline after setup-cleanup-setup). Its absence says nothing about production builds or event handlers.

### R4. `useSyncExternalStore` snapshot contract (correctness-oracles)

- `react/useSyncExternalStore.md:46`: "While the store has not changed, repeated calls to `getSnapshot` must return the same value. If the store changes and the returned value is different (as compared by `Object.is`), React re-renders the component."
- Line 48: `getServerSnapshot` "will be used only during server rendering and during hydration"; "The server snapshot must be the same between the client and the server"; omitting it makes server rendering "throw an error". Source (`ReactFiberHooks.js:1658-1663`): when hydrating without it, React throws "Missing getServerSnapshot, which is required for server-rendered content. Will revert to client rendering."
- Line 56: the snapshot "must be immutable"; for a mutable store "return a new immutable snapshot if the data has changed. Otherwise, return a cached last snapshot."
- Line 60: during a non-blocking Transition, React calls `getSnapshot` "a second time just before applying changes to the DOM. If it returns a different value ... React will restart the update from scratch, this time applying it as a blocking update".
- Line 389: always returning a different value means "you will enter an infinite loop".
- Executable oracle derived from the contract (design, not executed): with the store unchanged, call `getSnapshot()` twice and check `Object.is`; after a store change, check the subscriber callback fired and the new snapshot differs. This checks the contract directly and works in production builds, unlike the dev-only warning (R2), which compares two consecutive calls once per module.

### P1. Playwright `pageerror`, `console`, `weberror` (correctness-oracles)

- Pin: `microsoft/playwright` main `95e5dca31981bcd0970165853fcc713269d2433a` (latest release v1.65.0), `docs/src/api/class-page.md`, `class-browsercontext.md`.
- `page.on('pageerror')` (`class-page.md:396-410`, since v1.9): "Emitted when an uncaught exception happens within the page."
- `page.on('console')` (`class-page.md:165-185`, since v1.8): "Emitted when JavaScript within the page calls one of console API methods".
- `browserContext.on('weberror')` (`class-browsercontext.md:295-299`, since v1.38): "Emitted when exception is unhandled in any of the pages in this context."
- `page.consoleMessages()` and `page.pageErrors()` (`class-page.md:2875-2905`, since v1.56): return "up to (currently) 200 last" messages or errors; `filter` (since v1.59) defaults to `'since-navigation'`, "returns only messages logged after the last committed main-frame navigation".
- What it misses: the polling methods cap at 200 and default to the current navigation, so errors from before a navigation or beyond 200 are dropped unless the event listener records them from the start. Errors caught by application code (or by an error boundary in production, R1) never reach `pageerror`. Whether `pageerror` fires for unhandled promise rejections and for `reportError` calls is not stated on the page (unverified list). Development-only React messages (R2) appear in `console` only against a development build.
- Decision relevance: attach `pageerror` and `console` listeners before the first navigation and keep the full record; do not rely on `pageErrors()` for a multi-navigation scenario.

### K1. NodeCB (Wang 2017) dataset: not live; form-gated when it was (harness-sensitivity controls)

- `http://www.tcse.cn/~wsdou/project/NodeCB` (with and without trailing slash) and `http://www.tcse.cn/~wsdou/` return HTTP 404 (curl, 2026-11-09), matching the paper notes.
- Wayback Machine availability API returns a snapshot `20221207163016`. Its raw HTML (fetched with the `id_` raw modifier) shows: "Our 57 documented concurrency bugs ... We have made the collected bugs available online for future studies. Please use the data only for teaching and research purposes." Download was behind a form: "Please leave your contact information before downloading", `<form ... action="./obtain.php">`. "Last update: Sept 09, 2017." No license file or open download link on the page.
- GitHub repository search for "NodeCB concurrency" returned no repositories.
- Usable remainder: per the paper notes (p.11), references [21]-[42] give GitHub issue URLs for 22 of the 57 bugs; NodeRacer reused 4 of them at reverted revisions (Wang notes line 254). These are issue pointers, not packaged buggy/fixed checkouts or tests.
- Decision relevance: NodeCB cannot be cited as a downloadable control set. A drafter may name the 22 paper-listed issues as candidate historical regressions, each needing its own buggy/fixed revision and a failing test built from the report, per the skill's existing "attributable to the defect" rule.

### K2. sola-da/ReDoS-vulnerabilities (Staicu 2018 benchmark)

- Repo `sola-da/ReDoS-vulnerabilities`, HEAD `ccb8d7dc74fd9cff835b47548bdffb7c010bb60f`, last push 2017-12-06, not archived. GitHub license: `null` (no LICENSE file in the tree). Each `.js` file carries a header "Copyright 2017 Software Lab, TU Darmstadt, Germany" followed by the MIT permission text; the repo description says "The resources in this repository are provided for research purpose only." So licensing is per-file MIT-style headers plus a research-only statement in the description; no repository-level license.
- Contents: `README.md`, `package.json`, `run-all.js`, `utils.js`, and 23 `test-<module>.js` exploit scripts. README table lists 23 modules with bug report, maintainer response and advisory (e.g. forwarded Issue 3, FIXED, advisory 527; lodash Issue 3359, "limiting the size is fine", no advisory). `package.json` pins the vulnerable versions (e.g. `"forwarded":"0.1.0"`, `"moment": "2.18.1"`, `"lodash": "4.17.4"`); it also lists `ua-parser-js` 0.7.13 with no matching test file.
- What an exploit script does (`test-forwarded.js`): builds one string (`"x" + genstr(60000, ' ') + "x"`, comment "progblematic regex: / *, */, in forwarded/index.js"), calls the module once inside `measureTime`, and prints "Execution time (hr)". No assertion, no threshold, one input size, no random-input comparison. README: "For each benchmark, we print an execution time".
- Decision relevance: usable as a known-defect control for a ReDoS oracle in `resource-complexity-testing` / `harness-sensitivity`: the vulnerable version is the faulty case and the advisory's fixed version (where FIXED) is the healthy case. The scripts are not an oracle; Staicu's own decision rule (k=5 sizes, crafted vs random, CIs separate and difference strictly increasing, per notes lines 74-80) must be applied by the harness. Modules marked N/A or not fixed have no healthy counterpart.

### K3. BugsJS benchmark

- Exists. Website `https://bugsjs.github.io/`: "BugsJS is a benchmark of 453 real JavaScript bugs. Collected from 10 popular server-side JavaScript programs and manually validated"; subjects are "Node.js server-side JavaScript programs from GitHub that adopt the Mocha testing framework"; bugs "validated and cleaned to ensure that the bugs and their fixes were relevant, isolated, and reproducible". Crossref: "BugsJS: a Benchmark of JavaScript Bugs", ICST 2019, DOI 10.1109/icst.2019.00019; journal extension "BUGSJS: a benchmark and taxonomy of JavaScript bugs", STVR 2020, DOI 10.1002/stvr.1751 (papers not read).
- `BugsJS/bug-dataset` HEAD `7abbad3e4df12cd5294110bb5db11b7d5bc758a6`, last push 2019-11-27, `LICENSE` "MIT License, Copyright (c) 2018 BugsJS". `Versions.txt`: "Version 1.0 2018-10-15", "Number of Subjects: 10", "Number of Bugs: 453". `Projects.csv` counts: Express 27, Shields 4, Bower 3, Hexo 12, Karma 22, Hessian.js 9, Eslint 333, Node-redis 7, Pencilblue 7, Mongoose 29 (sum 453). Each subject is a fork under the `BugsJS` org.
- README: CLI `python3 main.py -p <Project> -b <n> -t {info,checkout,test,per-test} -v {buggy,fixed-only-test-change,fixed}`. `buggy` is "The parent commit of the revision in which the bug was fixed"; `fixed-only-test-change` is "only the tests introduced in the bug fixing commit, applied to the buggy revision"; `fixed` has "both the cleaned fix and the newly added tests". `Express_bugs.csv` rows give per-bug test counts, coverage and a bug category (e.g. "incorrect feature implementation --> incorrect data processing").
- Runtime: `BugsJS/docker-environment` HEAD `252cf8d7`, MIT, `env/Dockerfile` line 1 `FROM node:8.16-jessie`. Node-redis needs IPv6.
- Decision relevance: BugsJS gives exactly the healthy/faulty pair the skill asks for (`fixed-only-test-change` = faulty + fault-revealing test; `fixed` = healthy + same test), isolated per the site's claim. Limits: server-side Node only, Mocha only, no React/browser bugs, pinned to Node 8 in its Docker image, last updated 2019. Most bugs (333/453) are ESLint. It is a control set for Node oracles, not for React or modern test runners.

## Decisions for the drafter

Which file gets what (proposed; the drafter decides final wording):

- `correctness-oracles/references/javascript-observation-channels.md` (new): N1, N2, R1, R2, R3, R4, P1, plus the runner-side unhandled-error settings from N3, N7, N8. Organize by channel with three fields each: what it reports, in which build/mode/config, what it misses. Keep R4's executable snapshot check as the worked JS contract example (it parallels the existing SQLite examples: contract text, observation, blind spot). Hydration equality itself routes to `semantic-differential-testing` (F9 decision), not here.
- `correctness-oracles/SKILL.md`: one sentence in "Derive the check from the actual boundary" or "Preserve the check's outcome and limits" pointing JS/React targets to the new reference, e.g. a process exit code, test-runner status or clean console is an observation whose meaning depends on effective mode, listeners and build. Do not add channel detail to SKILL.md.
- `correctness-oracles/references/common-mistakes.md`: add the JS mistakes M1-M4 below.
- `harness-sensitivity/references/runtime-integrations.md`: extend (do not repeat StrykerJS) with a "JavaScript/TypeScript: reachability and order probes" section: N5/N6 coverage (c8 `--all`, node:test excludes, Jest `babel` default vs `v8`, Vitest `v8` default and not on Firefox/WebKit); N4/N7/N8 order shuffling with versions and seed replay; Jest `--detectOpenHandles`/`--forceExit` and node:test extraneous activity as leak signals. Place it beside "Optional reachability evidence", since it is the same kind of evidence.
- `harness-sensitivity/references/control-design.md`: add a short "Known-defect sources for JS" paragraph: BugsJS (K3) for Node with its version triple, the Staicu exploits (K2) with "scripts print time; apply the size-family rule", NodeCB (K1) as 22 issue pointers only. State each limit.
- `harness-sensitivity/references/common-mistakes.md`: add M5-M8.
- `harness-sensitivity/SKILL.md`: one clause in "Use the current harness and runner" naming JS coverage and order probes via the reference. No new steps.

Description wording (so JS requests select these skills; keep the existing text, append trigger terms):

- `correctness-oracles`: append something like "including JavaScript/TypeScript and React harnesses that rely on process exit, unhandled rejections, test-runner status, error boundaries or console errors." Terms a user would type: "unhandled rejection", "uncaughtException", "error boundary", "onRecoverableError", "StrictMode", "console.error", "Playwright pageerror".
- `harness-sensitivity`: append something like "including Node/Jest/Vitest coverage (c8, V8) and test-order randomization checks for JavaScript suites." Terms: "c8", "NODE_V8_COVERAGE", "test-randomize", "flaky test order", "detectOpenHandles", "StrykerJS".

## Common mistakes with evidence

- **M1. Treating "no crash" as "no unhandled rejection".** Default `throw` mode only crashes when no `unhandledRejection` listener is set (N1, `cli.md:3660-3686`); any `uncaughtException` listener makes the process "exit with 0" (N2, `process.md`). Use: read effective mode and listeners; record via `uncaughtExceptionMonitor`.
- **M2. Adding an `uncaughtException` listener to "log" errors in the harness.** It overrides the default exit and leaves the process in "an undefined state" (N2). Use `uncaughtExceptionMonitor`, which "does not change the behavior".
- **M3. Reading a clean console in a production build as a passed React contract.** The getSnapshot, hydration and boundary messages are `__DEV__`-only (R1, R2); StrictMode checks "are development-only" (R3). Use: state the build; check the contract directly (R4).
- **M4. Counting React warnings as offenders.** `didWarnUncachedGetSnapshot` is module-level and set after the first warning (R2, `ReactFiberHooks.js:186`). Use: one message means at least one offender.
- **M5. Reading a coverage percentage as producer reachability.** V8/c8 only covers "files that were loaded by the engine" unless `--all` (N6); node:test excludes `node_modules/` by default (N5); ignore comments remove lines. Use: check the specific producer file and function appear and executed.
- **M6. Calling a shuffled pass "no order dependence".** Node keeps declaration order for sequentially awaited subtests (N4); Jest `--randomize` shuffles within a file only and needs jest-circus (N7); default node:test process isolation keeps in-memory state from crossing files (N3). Use: state what was shuffled; keep the seed.
- **M7. Losing the failing shuffle seed.** Node prints it in the summary (N4); Jest needs `--showSeed` or `--randomize` (N7); Vitest defaults to `Date.now()` and printing is not documented (N8). Use: set the seed explicitly for each run you record.
- **M8. Concluding a leak or flake is gone under a diagnostic mode.** Jest `--detectOpenHandles` implies `--runInBand` and enables `async_hooks` (N7). `--forceExit` hides held handles. Use: compare under the original execution mode.
- **M9. Trusting a green test run with unhandled-error suppression configured.** Vitest `dangerouslyIgnoreUnhandledErrors` and `onUnhandledError` filtering stop failures (N8); Jest without `waitForUnhandledRejections` may misattribute or miss rejections (N7). Use: read the runner config before the verdict.

## Sources inventory (all accessed 2026-11-09)

| Source | Pin | Used for |
|---|---|---|
| nodejs/node `doc/api/{cli,process,test,globals}.md` | tag v26.13.0 (`daaa22ae`) | N1-N5, R1 |
| nodejs/node `doc/api/{cli,test}.md`, `doc/changelogs/CHANGELOG_V24.md` | tag v24.22.2; v24.x head `338f67f5`; v22.x branch | N4 versions |
| bcoe/c8 `README.md`, `package.json` | `ae5a0cf4` | N6 |
| istanbuljs/schema `default-exclude.js` | master `a9d00f48` | N6 |
| jestjs/jest `website/versioned_docs/version-30.5/{CLI,Configuration,JestObjectAPI}.md`, `CHANGELOG.md` | `72614448` | N7 |
| vitest-dev/vitest `docs/config/{sequence,dangerouslyignoreunhandlederrors,onunhandlederror,browser/trackunhandlederrors}.md`, `docs/guide/{coverage,common-errors}.md` | `3a76b873` | N8 |
| stryker-mutator/stryker-js releases API; npm registry `@stryker-mutator/core` | `8f24ef0b`, v10.1.1 | N9 |
| reactjs/react.dev `src/content/reference/{react-dom/client/createRoot,react-dom/client/hydrateRoot,react/Component,react/StrictMode,react/useSyncExternalStore}.md` | `7594a2b0` | R1-R4 |
| facebook/react `ReactFiberErrorLogger.js`, `ReactFiberHooks.js`, `shared/reportGlobalError.js`, `CHANGELOG.md` | tag v19.3.1 (`61aa00df`) | R1, R2, R4 |
| microsoft/playwright `docs/src/api/{class-page,class-browsercontext}.md` | `95e5dca3` | P1 |
| www.tcse.cn NodeCB page (404) and Wayback snapshot 20221207163016 | n/a | K1 |
| sola-da/ReDoS-vulnerabilities `README.md`, `package.json`, `utils.js`, `run-all.js`, `test-forwarded.js` | `ccb8d7dc` | K2 |
| BugsJS/bug-dataset `README.md`, `LICENSE`, `Projects.csv`, `Versions.txt`, `Projects/Express/Express_bugs.csv`; BugsJS/docker-environment `README.md`, `env/Dockerfile`; bugsjs.github.io; Crossref | `7abbad3e`; `252cf8d7` | K3 |

## Unverified (explicit)

- Whether Playwright `pageerror` / `weberror` fire for unhandled promise rejections and for `reportError(...)` calls (React 19's default uncaught/recoverable route in browsers). The docs say only "uncaught exception".
- The plain-Node behavior of React's default handlers (R1 inference): that `process.emit('uncaughtException', err)` with no listener leaves no output and no exit. Not executed; Node `events.md` emit semantics not re-read in this pass.
- Whether jsdom provides `reportError`, and therefore which `reportGlobalError` branch runs under Jest/Vitest jsdom environments.
- Whether Vitest prints the shuffle seed when `sequence.shuffle` is on (not stated on `sequence.md`).
- Whether node:test coverage and c8 exclude `node_modules` identically (c8 default excludes come from istanbuljs/schema, which does not list `node_modules`; whether test-exclude adds it implicitly was not read).
- How Jest and node:test report an `uncaughtException` thrown while a test is still running (as opposed to after completion, N3). Not read.
- The full list of `__DEV__`-only React warnings; only the instances cited in R1/R2 were read.
- Whether the BugsJS bugs still build and run on current Node (Docker image is Node 8.16); the "isolated" and "reproducible" claims are the site's, not checked.
- Which of the 22 NodeCB issue URLs still resolve and have identifiable fix commits.
- Whether the Staicu exploit scripts still run on current Node with the pinned vulnerable versions.

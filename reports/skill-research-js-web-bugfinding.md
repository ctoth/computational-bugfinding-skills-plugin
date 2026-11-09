# Skill Research: JavaScript/TypeScript (Node.js and React/Browser) Bugfinding

**Date:** 2026-11-09
**Domain:** Extending the computational-bugfinding plugin's 25 method skills to JS/TS on Node.js services and React/browser applications.

## State

- Status: Phase 1 domain research complete. Sections: repository inputs, tool findings F1-F16, web failure spaces, existing skills/plugins, literature leads, summary (route table, candidate skills, open questions, unverified items).
- The Edit tool was unavailable in this session, so the file was rewritten whole with Write at each append.
- Nothing installed, no campaigns run, no skills/manifests/agent-notes edited, nothing committed or pushed.
- Every paper listed is "not read"; no claim is stated from any paper. Bibliographic data comes from Crossref API records (and the USENIX page for one paper).
- Facts are quoted from primary sources pinned to a commit or tag. Lines marked "Inference" are my reasoning, not source statements.

## Repository inputs read

- `reports/skill-plan-computational-bugfinding.md` in full. Relevant: the runtime table row "JS/TS | fast-check | Deeper API and async sequence guidance required; no verified coverage-guided JS runtime chosen in Phase 1" (line 322). "What Was Excluded" defers "GUI/browser" skill claims as "explicit next research candidates rather than pretend coverage" (line 356).
- `reports/skill-research-computational-bugfinding.md` in full. Its line 127 lists "GUI/browser event sequences" as unresolved.
- All 25 `plugins/bugfinding/skills/*/SKILL.md` frontmatter descriptions, plus the full body of `schedule-exploration/SKILL.md`. That skill owns "schedule choices and their execution model"; its lanes are Loom, Shuttle and Coyote, with a stated boundary for Go synctest.
- Existing JS citations:
  - `plugins/bugfinding/skills/stateful-property-testing/references/runtime-recipes.md:15-21`: fast-check 4.10.2 at commit `5ec2e3ae`, MIT, Node `>=12.17.0`, `asyncModelRun`. It already names `scheduledModelRun` as "a separate controlled-execution concern".
  - `plugins/bugfinding/skills/harness-sensitivity/references/runtime-integrations.md:15-25`: StrykerJS at commit `8f24ef0b`, Apache-2.0, `@stryker-mutator/core` 10.1.1 with `"node": ">=22.0.0"`.
  - I grepped `plugins/bugfinding/skills` for `javascript|node.js|typescript|jazzer.js|fast-check`. Besides the two files above, it found only two incidental mentions: Porcupine's "embedded JavaScript" visualization (`linearizability-checking/references/porcupine-operation.md:37`) and `numerical-oracles/references/tool-routes.md:7` ("No Go, JavaScript or Python binding was verified").

## Tool findings

### F1. Jazzer.js: coverage-guided fuzzer for Node.js (route for `coverage-guided-fuzzing`)

Pinned: `CodeIntelligenceTesting/jazzer.js` main at `f23bc5aeb7a6d50cd6256cfc3be44b868da5e7b1`. License Apache-2.0 (GitHub API). Not archived.

- What it is (README): "a coverage-guided, in-process fuzzer for the Node.js platform ... It is based on libFuzzer".
- Instrumentation:
  - `docs/architecture.md:35-36`: "Both paths use Babel to transform source code, inserting coverage counters so the fuzzer can detect new code paths, and comparison hooks".
  - `docs/fuzz-targets.md:149-150`: without `-i`, "everything outside `node_modules` is instrumented by default".
  - ESM, `docs/fuzz-targets.md:117-119`: "Requirements: Node.js >= 20.6 ... older Node versions, ESM loading still works but modules are not instrumented."
  - Decision relevance: an ESM target on an older Node runs with no coverage feedback. This is exactly the instrumentation check that `coverage-guided-fuzzing` requires.
- Async, `docs/fuzz-targets.md:64-66`: "The resolution of a `Promise`, returned by a fuzz target, is awaited before the next fuzzing input is provided." The `--sync` flag "May only be used for entirely synchronous code" (line 239).
- Oracles beyond uncaught exceptions (`docs/bug-detectors.md`): command injection, path traversal, prototype pollution (with a documented "Shortcoming", line 71), remote code execution, SSRF, and custom detectors via `reportFinding`.
- Test integration: Jest via `@jazzer.js/jest-runner` and `it.fuzz`. Regression/coverage mode: `npx jazzer <fuzzTarget> --mode=regression --coverage <corpus directories>` (`docs/fuzz-targets.md:252`).
- Platforms (README, "Supported Architectures"): "Jazzer.js supports Node.js LTS versions on the following platforms, other versions are best effort only: Linux x86_64; macOS x86_64 and arm64; Windows x86_64". The v4.0.0 release notes add "linux arm64 support". The README and the release notes disagree (open).
- Runtime floor: `packages/core/package.json` (4.0.0) declares `"node": ">= 14.0.0"`, but the root `package.json` declares `"node": ">= 20.11.0"` (mismatch, open).
- Maintenance facts:
  - Releases: v2.1.0 (2023-10-23), then v4.0.0 (2026-04-15). The v4.0.0 release body says: "_Releases v3.x.x were used by the commercial version and are therefore skipped._"
  - Commits per year (GitHub API): 76 in 2024, 0 in 2025, 81 in 2026 so far. Last human commit: 2026-11-02.
  - Inference: open-source work paused through 2025 and resumed in 2026. A reference should state this gap and recheck status when the tool is selected.
- Decision relevance: closes the plan's line-322 gap ("no verified coverage-guided JS runtime") for Node targets. No coverage-guided route for browser code was found.
- Not credible: the predecessor `fuzzitdev/jsfuzz` is archived (GitHub API `archived: true`, last push 2021-04-30).

### F2. fast-check scheduler: controlled promise-resolution order (route for `schedule-exploration`)

Pinned: `dubzzz/fast-check` main at `cd9c1884e8a39fe945600fbcda1ec92d518feaa0`. `packages/fast-check/package.json`: version 4.10.2, `"license": "MIT"`, `"node": ">=12.17.0"`. Source: `website/docs/advanced/race-conditions.md`.

- Purpose: "The `scheduler` arbitrary has been specifically designed for detecting and testing race conditions".
- What it controls:
  - `schedule` wraps a promise: "The newly created promise will resolve when the scheduler decides to resolve it".
  - `scheduleFunction` "is only postponing the resolution of the function. The call to the function itself is started immediately".
  - Code that holds the original promise is "not impacted by the scheduler".
- What it does not control:
  - `waitIdle` "Cannot await tasks triggered by uncontrolled sources like `fetch` or external event emitters."
  - `waitFor`: "having uncontrolled tasks triggering stuff required for `unscheduledTask` might make replay of failures harder as such asynchronous triggers stay out-of-control for fast-check."
- Replay: `fc.schedulerFor(ordering: number[])` defines a hardcoded order. `report()` lists tasks "in the order they get executed by the scheduler".
- Timers ("Scheduling native timers"): timers "require special handling". The documented recipe uses Jest fake timers (`jest.useFakeTimers()`, `jest.advanceTimersToNextTimer()`) inside a custom `act`.
- React ("Wrapping calls automatically using `act`"): "when testing React applications, one cannot perform updates of states outside of `act`."
- Decision relevance:
  - This is a real JS controller. Its boundary fits the "Establish control before allocating search" step in `schedule-exploration`: only wrapped promises are controlled, much as code outside Loom is "invisible" to Loom.
  - The docs describe a random order chosen per property run. I found no documentation of exhaustive or bounded-systematic search (inference from the API docs).
  - It belongs in `schedule-exploration` as a JS reference. Pairing with `stateful-property-testing` goes through `scheduledModelRun`, which `runtime-recipes.md:19` already names.

### F3. Node.fz: libuv event-queue reordering (no credible current route)

Pinned: `SBULeeLab/NodeFz` master at `1ce111e353f423e99b593ca1dfa8643029ae8e37`. GitHub license field `NOASSERTION`. Last commit 2019-07-07.

- README:
  - "a modified version of the popular Node.js JavaScript runtime framework, version 0.12.7".
  - "I probabilistically re-order the event queue, constrained by legal or practical ordering guarantees prescribed by the Node.js and libuv documentation".
  - `UV_SCHEDULER_MODE` supports "RECORD".
  - "The most needed change is porting it up to a more recent version of Node.js (libuv)."
- Decision relevance: the method is a literature lead for `schedule-exploration`. The artifact is an unmaintained Node 0.12.7 fork, so it is no route for current Node. No maintained successor was found (open).

### F4. ExpoSE: dynamic symbolic execution for JavaScript (`symbolic-concolic-execution`, research-grade only)

Pinned: `ExpoSEJS/ExpoSE` master at `ec03edf85f883248612b1d498c6a7d9189d16d6f`. MIT. Last commit 2024-07-02 ("Big general update. Update Node to 21"); last repository push 2025-01-19.

- README:
  - "ExpoSE is a dynamic symbolic execution engine for JavaScript ... supports symbolic execution of Node.js programs and JavaScript in the browser. ExpoSE is based on Jalangi2 and the Z3 SMT solver."
  - Requires "`node` version v21.7.2 (other versions may work but are not tested), `npm`, `clang` (with `clang++`), `gnuplot` ..., `make`, `python`".
  - Browser: "limited support for symbolic execution of webpages through a custom Electron based web browser". The CLI has a `replay` option.
- Decision relevance: a research-grade route behind an explicit applicability check, tested only on Node 21.7.2 (a non-LTS line; inference). No other maintained JS concolic tool was found (open).

### F5. Jalangi2, NodeProf, NodeRacer, EventRacer: JS dynamic analysis and event-race research tools (no credible maintained route)

- Jalangi2, pinned `Samsung/jalangi2` master at `bc879287b1678de6e3c423f5debe63207559525b`, Apache-2.0.
  - README: "a framework for writing dynamic analyses for JavaScript"; "We primarily test Jalangi with the Node LTS version (currently v12)"; "Jalangi2 does not support the record/replay feature of Jalangi1."
  - Two commits in 2026-01 after a gap from 2024-02.
- NodeProf, pinned `Haiyang-Sun/nodeprof.js` master at `5cccefc56dbd144f6a9ff303288dc1f4441f30d4`, Apache-2.0.
  - README: "An efficient instrumentation and profiling framework for Graal.js"; "The latest supported GraalVM JavaScript version is 23.0.1".
  - Last commit 2023-09-12.
- NodeRacer, pinned `andreendo/noderacer` at `2317c673490d3c721abdd91ee93b302c6720a235`, Apache-2.0.
  - README: "A dynamic race detector with guided execution for Node.js applications"; install section says "Node.js ... (version used LTS 10.16.3)".
  - Last commit 2022-12-15.
- EventRacer (`eth-sri/EventRacer`): last push 2015-09-21. README not read.
- Decision relevance: each is pinned to an old runtime (Node 10 or 12) or to GraalJS instead of stock Node, so none is a drop-in for a current service or React app (inference from the documented versions). They are literature leads for event races and the substrate ExpoSE uses.

### F6. memlab: heap-snapshot leak detection for browsers and Node (route for `resource-complexity-testing`)

Pinned: `meta/memlab` main at `8ac1a3c9ed8a9f7076869b4b0abbe7b293986c4d` (the API redirected from `facebook/memlab`). MIT. `packages/core/package.json`: version 2.0.7, `"node": ">= 12.6.0"`.

- README:
  - "an end-to-end testing and analysis framework for identifying JavaScript memory leaks".
  - "Write test scenarios with the Puppeteer API, and memlab will automatically compare JavaScript heap snapshots, filter out memory leaks, and aggregate the results".
  - Works on snapshots "taken from Chromium-based browsers, Node.js, Electron.js, and Hermes".
  - "Memory assertions in Node.js - Enables unit tests or running node.js programs to take a heap snapshot of their own state".
- Scenario and oracle:
  - A scenario has `url`, `action` and `back`.
  - "`leakFilter` will be called for every unreleased heap object (`node`) allocated by the target interaction."
  - `memlab analyze unbound-object` reports objects that keep growing.
- Limit: "To get a readable trace, the website under test needs to serve non-minified code".
- Decision relevance: memlab supplies a client-side retention oracle (objects allocated by the action and still retained after `back`), within the "memory-retention" scope `resource-complexity-testing` already has. A fixed memlab scenario does not search over interaction sequences (inference); that search remains the skill's work.
- memlab also ships a Claude Code/Codex plugin (see Existing skills).

### F7. c8 and `NODE_V8_COVERAGE`: native V8 coverage (supports `harness-sensitivity`, `corpus-evolution`)

- c8, pinned `bcoe/c8` main at `ae5a0cf4349b92cac910cf7275e724ab7a725b9d`. ISC, version 12.0.0, `"node": "^20.19.0 || ^22.12.0 || >=23"`. README: "c8 - native V8 code-coverage". The `--temp-directory` option defaults to `process.env.NODE_V8_COVERAGE`.
- Node, tag v26.13.0, `doc/api/cli.md:4517-4526`: "When set, Node.js will begin outputting V8 JavaScript code coverage and Source Map data to the directory provided"; "`NODE_V8_COVERAGE` will automatically propagate to subprocesses".
- Decision relevance:
  - This is measurement, not search. It answers the reachability check in `harness-sensitivity` and supports coverage-diverse seed selection in `corpus-evolution`.
  - It is not the signal that guides Jazzer.js, which uses Babel-inserted counters (F1). Mixing the two up would misstate what guided a search (inference).

### F8. Node core: heap snapshots, test-order randomization, leaked async work, mock timers

All from `nodejs/node` tag `v26.13.0` (2026-10-28, 'Lithium' LTS). GitHub reports the license as `NOASSERTION` (composite LICENSE file; not resolved further).

- Heap snapshots (`doc/api/v8.md:577-617`, `v8.writeHeapSnapshot`):
  - "The JSON schema is undocumented and specific to the V8 engine, and may change from one version of V8 to the next."
  - "A heap snapshot is specific to a single V8 isolate" (a snapshot of one thread excludes workers).
  - "Creating a heap snapshot requires memory about twice the size of the heap"; it is "a synchronous operation which blocks the event loop".
  - Relevance for `resource-complexity-testing`: taking the measurement perturbs the target, and snapshots are not comparable across V8 versions.
- `--heapsnapshot-near-heap-limit=max_count` (`doc/api/cli.md:1841-1880`; no longer experimental as of v25.4.0, v24.13.1 and v22.22.1): snapshots "can be compared to determine what objects are being allocated during the time consecutive snapshots are taken".
- Test-order randomization (`doc/api/cli.md:3260-3290`, `--test-randomize` and `--test-random-seed`, added in v26.1.0):
  - Randomizes test order, which "can help detect tests that rely on shared state or execution order".
  - "The seed used for randomization is printed in the test summary and can be reused".
  - Relevance: a built-in order-dependence probe for flaky-test work, available only on Node 26.1 and later.
- Leaked async work (`doc/api/test.md:612-646`, "Extraneous asynchronous activity"):
  - "it is possible for the test function to generate asynchronous activity that outlives the test itself".
  - "`uncaughtException` and `unhandledRejection` events originating from a completed test are marked as failed".
  - Relevance: a state-leakage oracle that `harness-sensitivity` should know about.
- Mock timers (`doc/api/test.md:1036-1042`): `mock.timers.enable({ apis: ['setTimeout'] })` and `mock.timers.tick(ms)` simulate timers "without actually waiting". Relevance: this is virtual time, the same boundary `schedule-exploration` already draws for Go synctest. Fake time is not schedule enumeration.
- `--unhandled-rejections=mode` (`doc/api/cli.md:3660-3670`): the default became `throw` in v15.0.0. Relevance: whether a rejected promise acts as a crash oracle depends on this mode.

### F9. React documentation: hydration mismatch, StrictMode, `act`, `useSyncExternalStore`

Pinned: `reactjs/react.dev` main at `7594a2b008489121bdf25f97320d11ac0422510e`. Docs content is CC-BY-4.0 (GitHub API).

- Hydration (`src/content/reference/react-dom/client/hydrateRoot.md`):
  - Lines 57-58: "`hydrateRoot()` expects the rendered content to be identical with the server-rendered content. You should treat mismatches as bugs and fix them." "In development mode, React warns about mismatches during hydration. There are no guarantees that attribute differences will be patched up in case of mismatches."
  - Lines 192-199, common causes: "Using checks like `typeof window !== 'undefined'` in your rendering logic"; "browser-only APIs like `window.matchMedia`"; "Rendering different data on the server and the client". Also: "React recovers from some hydration errors, but **you must fix them like other bugs.** ... in the worst case, event handlers can get attached to the wrong elements."
  - Lines 238-274: `suppressHydrationWarning={true}` "only works one level deep, and is intended to be an escape hatch"; "React will **not** attempt to patch mismatched text content."
  - Line 46: `onRecoverableError` is "Callback called when React automatically recovers from errors". This observation channel does not depend on development-mode warnings.
- StrictMode (`src/content/reference/react/StrictMode.md`):
  - Lines 89-94: components "re-render an extra time to find bugs caused by impure rendering", "re-run Effects an extra time to find bugs caused by missing Effect cleanup", and "re-run ref callbacks an extra time"; "**All of these checks are development-only and do not impact the production build.**"
  - Line 127: React "will only enable behaviors that are possible in production". Line 137: functions that should be pure are called "**twice in development.**"
- `act` (`src/content/reference/react/act.md:53`): "Any updates triggered within the `actFn`, are added to an internal act queue, which are then flushed together". Line 158: `act` "requires setting `global.IS_REACT_ACT_ENVIRONMENT=true`". Line 176: React Testing Library sets this for you.
- `useSyncExternalStore` (`src/content/reference/react/useSyncExternalStore.md`):
  - Line 46: "repeated calls to `getSnapshot` must return the same value".
  - Line 48: "The server snapshot must be the same between the client and the server".
  - Line 389: returning a different value every time means "you will enter an infinite loop".
- Decision relevance:
  - Hydration compares two executions (server render and client initial render) against a documented equality contract. That makes it an instance of `semantic-differential-testing` across execution modes, whose nondeterminism sources (time, randomness, environment checks) that skill already says to control.
  - StrictMode is a fixed, development-only double-invocation oracle for purity and cleanup. It is not schedule search, and production-only behavior lies outside it.
  - Inference: `act` batches updates into one flush, so tests under `act` and RTL do not explore how React would interleave those updates in production. A schedule-search reference must state this limit.

### F10. Playwright and Puppeteer: browser drivers (execution substrate, not generators or oracles)

- Playwright, pinned `microsoft/playwright` main at `95e5dca31981bcd0970165853fcc713269d2433a`. Apache-2.0; `packages/playwright-core/package.json` version `1.66.0-next`, `"node": ">=20"`. README:
  - "It drives Chromium, Firefox, and WebKit with a single API".
  - "Auto-wait and web-first assertions. No artificial timeouts. Playwright waits for elements to be actionable, and assertions automatically retry until conditions are met."
  - The Trace Viewer captures "every action, DOM snapshot, network request, and console message".
- Puppeteer, pinned `puppeteer/puppeteer` main at `8fab4dc965d4d7d9375e7b84dede8e9b80ac5c15`. Apache-2.0; `packages/puppeteer-core/package.json` version 25.16.0, `"node": ">=22.12.0"`. README: drives "Chrome or Firefox over the DevTools Protocol or WebDriver BiDi". memlab scenarios use the Puppeteer API (F6).
- Crawljax (`crawljax/crawljax`, Apache-2.0): last push 2023-09-18. It is Java; README not read. No maintained JS UI-state crawler was verified (open).
- Decision relevance:
  - The drivers execute UI event sequences, and their traces are replay artifacts for `failure-reduction` and `evidence-based-triage`.
  - Inference: assertions that retry automatically can hide a transient wrong state.
  - Neither tool generates event sequences or supplies a correctness oracle. A UI state-space search needs a generator (for example fast-check commands from `stateful-property-testing`) plus a stated contract.
- Cross-browser execution is a `configuration-differential-testing` dimension.

### F11. React Testing Library and MSW: component-level driver and network seam

- React Testing Library, pinned `testing-library/react-testing-library` main at `20ce75f2907ca0e5c5a8ae595c0e9a4e368c7800`. MIT; `"node": ">=18"`; peer dependency `"react": "^18.0.0 || ^19.0.0"`. README lines 94-95: "The more your tests resemble the way your software is used, the more confidence they can give you."
- MSW, pinned `mswjs/msw` main at `9bbfe99cd52beeb952fdaa1cd2901c019e4b858e`. MIT; version 3.0.4, `"node": ">=22.12.0"`. README: "A dedicated layer of requests interception"; responds "with necessary status codes, headers, cookies, delays, or completely custom resolvers."
- Decision relevance:
  - RTL is the component-level driver for `stateful-property-testing` over React components. fast-check's `scheduleSequence` example uses `render` and `rerender`.
  - MSW is the in-process network seam. There, `schedule-exploration` can control response order (fast-check documents a "Scheduling a call to a mocked server" recipe) and tests can inject client-side faults (status codes, delays).
  - MSW faults are application-layer mocks, not the real-deployment faults that `distributed-fault-testing` covers.

### F12. Toxiproxy with a Node client: TCP fault injection (`distributed-fault-testing`, partial route)

- Toxiproxy, pinned `Shopify/toxiproxy` main at `49299d8838525126e09c85ebe0ba89940a3261e5`. MIT. README:
  - "A TCP proxy written in Go".
  - Toxics include `latency`, `down`, `bandwidth`, `timeout`, `reset_peer`, `slicer` and `limit_data`.
  - The client list includes "toxiproxy-node-client".
- `ihsw/toxiproxy-node-client` master at `d7782a4ee344ad30f7030f7dc63a8567f052c5e2`: `package.json` version 4.1.0, `"license": "ISC"`, `"node": ">=18"`. Last commits 2026-04-26. The GitHub repository license field is empty; only package.json declares ISC.
- Decision relevance:
  - Toxiproxy injects network faults between a Node service and its dependencies in a disposable setup.
  - It has no workload generator and no history checker; those still come from F13.
  - It provides no process kills or clock faults.

### F13. History checkers for a Node service: Porcupine, and Elle/Knossos via elle-cli

- Porcupine: `linearizability-checking` already pins it at `97cd067d`; MIT per the GitHub API. It is a Go library, so a Node service history must be exported and checked by a Go model program. I found no JS linearizability checker (`gh search repos "linearizability checker javascript"` returned nothing).
- elle-cli, pinned `ligurio/elle-cli` master at `3c2504815945cd4ab1b5cc0142d2fe206e1ee285`. GitHub license `NOASSERTION` (unresolved). README:
  - "`elle-cli` operates with operations history both in EDN and JSON ... formats and can be successfully used ... with other Jepsen-similar frameworks that produce histories in JSON format".
  - Requires "Java 21 or later".
  - Example: `java -jar target/elle-cli-0.1.11-standalone.jar --model rw-register histories/elle/rw-register.json`.
  - It also wraps Knossos (README line 11). `jepsen-io/knossos` is not archived; last push 2026-07-17.
- Decision relevance:
  - Both history methods apply to Node services unchanged.
  - The JS-specific work is recording invocation and completion in real-time order from an event-loop client, including promises that never settle.
  - The existing skills already cover pending and uncertain operations (plan lines 168 and 179).

### F14. ReDoS detection tools (producers for `resource-complexity-testing`)

- recheck, pinned `makenowjust-labs/recheck` main at `f008739a7470038fa41aa841a648237243cabfb4`. MIT; latest release v4.6.2 (2026-10-26); npm package `recheck`. Its docs site (https://makenowjust-labs.github.io/recheck/) says it "implements the state-of-the-art algorithm to detect ReDoS vulnerability, which contains the fuzzing with static analysis" and supports "backreferences and look-around operations, in JavaScript, Python, Ruby, Java, .NET, Perl and PCRE". That page does not say whether recheck outputs an attack string (open).
- redos-detector, pinned `tjenkinson/redos-detector` main at `db112c6a74361db91f9591df8fa85d4026e9cbe5`. MIT; `"node": ">=16.0.0"`. README:
  - "Supported in the browser, Node and Deno".
  - "If the score is `1` this means no backtracks can occur".
  - It "checks patterns that are expected to run using an engine that implements the ECMA-262 (JS) standard".
- `ota-meshi/eslint-plugin-regexp` (MIT, pushed 2026-11-06) exists; its rules were not read (open).
- `davisjam/vuln-regex-detector` (MIT) was last pushed 2022-01-07: stale, not selected.
- Decision relevance:
  - These tools produce candidate super-linear patterns.
  - `resource-complexity-testing` still requires repeated, matched measurements at the real call site with input-size families before anything counts as a finding. Its rule against "a single slow run treated as a bug" applies.
  - Inference: ReDoS is one producer within that skill, not a separate method.

### F15. StrykerJS currency check

- `stryker-mutator/stryker-js`: not archived, last push 2026-10-30, Apache-2.0 (GitHub API).
- No newer release than the existing reference's pin (`8f24ef0b`, core 10.1.1, Node `>=22.0.0`) was read in this pass. On present evidence the existing route needs no change.

### F16. No JS route verified for native memory, memory-race detection, deterministic simulation, bounded model checking, crash consistency, numerical bindings, or semantic program generation

These are negative results from a bounded pass, not proofs of absence.

- `native-memory-instrumentation`: applies only to native addons inside a Node process. I verified no Node-addon sanitizer recipe. Jazzer.js being "based on libFuzzer" (F1) does not establish sanitizer support for addons.
- `race-detection-campaigns`: its oracle is conflicting shared-memory accesses.
  - Inference, not verified from a primary source in this pass: ordinary JS on one isolate runs its event loop on a single thread, so the detector oracle would apply only to `SharedArrayBuffer`/`Atomics` sharing across workers.
  - No detector for that was found.
  - JS event races are schedule problems (F2, F3, F5), not memory-access races.
- `deterministic-simulation`, `bounded-model-checking`, `crash-consistency-testing`: no JS-specific tool was searched to completion. None found.
- `numerical-oracles`: the existing reference already records no verified JS binding (`numerical-oracles/references/tool-routes.md:7`).
- `semantic-program-generation`: relevant only for Node targets that consume programs (bundlers, template engines, interpreters). No generator was verified in this pass.

## Web-specific failure spaces (question 2)

Each entry gives the search dimension, the oracle, and whether it is distinct from an existing skill's boundary. The distinctness judgments are inferences from the skill descriptions and the sources above.

1. **Event and async races (Node and browser).**
   - Dimension: the order in which promises, callbacks, timers and network responses resolve.
   - Oracle: a state invariant or model comparison after `waitIdle`, or a history checker.
   - Tools: fast-check scheduler (F2); MSW for response order (F11); Node mock timers for virtual time (F8). Runtime-level reordering (Node.fz, F3) and research detectors (NodeRacer, EventRacer, F5) are unmaintained.
   - Distinct? No. It falls inside `schedule-exploration` ("schedule choices"). That skill lacks a JS reference, and its current runtime list (Loom/Shuttle/Coyote/Go) would make an agent wrongly report "no JS controller". Add a JS controller reference there.
2. **UI state-space exploration of React apps.**
   - Dimension: sequences of user events (click, type, navigate) over reachable UI states, with backend responses as part of the state.
   - Oracle: invariants over the rendered DOM or accessibility tree, model comparison, `onRecoverableError`/console-error channels, or retention (memlab).
   - Tools: fast-check commands with RTL (component level) or Playwright (page level). No maintained JS crawler was verified (Crawljax is Java and stale).
   - Distinct? Partly. Operation sequences with preconditions are `stateful-property-testing`'s method. The added obligations are DOM-specific: actionability and auto-wait masking (F10), `act` batching (F9), observation through the accessibility tree, and browser state reset between runs. This is the "GUI/browser event sequences" candidate the plan deferred (plan line 356). Evidence supports a JS/browser reference under `stateful-property-testing`. I found no method-level evidence (beyond those obligations) that would justify a separate skill (see candidates).
3. **SSR/hydration mismatch.**
   - Dimension: inputs, environments (locale, timezone, viewport, `matchMedia`), time and data that make the server render differ from the client's first render.
   - Oracle: React's documented contract that server and first client render are identical (F9). Observe mismatches through development warnings or `onRecoverableError`, or compare server HTML with the client's first render directly.
   - Distinct? No. It is a two-mode comparison under `semantic-differential-testing`, with environment variation from `configuration-differential-testing`. Worth a worked example in a reference because the contract is documented and specific.
4. **Client-side memory leaks.**
   - Dimension: repeated interaction cycles (action, then back).
   - Oracle: retained objects allocated by the action (memlab `leakFilter`), or growth across snapshots.
   - Distinct? No. It sits inside `resource-complexity-testing` ("memory-retention"). Measurement caveats are in F8 (snapshots block the event loop, need about twice the heap, and vary by V8 version). Route mechanics to memlab's own plugin.
5. **ReDoS and algorithmic complexity in Node.**
   - Dimension: input-size families against regexes and parsers on request paths.
   - Oracle: superlinear time growth. Inference: on a single event loop, one slow request also stalls every other request.
   - Distinct? No. It sits inside `resource-complexity-testing`, with ReDoS detectors (F14) as candidate producers.
6. **React concurrent rendering and StrictMode double invocation.**
   - StrictMode is a fixed oracle: purity and cleanup, checked by invoking twice in development only (F9).
   - Concurrent interleaving is not exposed to tests by `act`, which flushes queued updates together (F9). Inference: I found no documented React API that lets a test enumerate concurrent render interleavings.
   - `useSyncExternalStore` documents snapshot-stability contracts that can serve as oracles.
   - Distinct? No skill change justified on present evidence. Note StrictMode under `correctness-oracles` as an existing development-only oracle, and the `act` limit under `schedule-exploration`.
7. **Flaky-test nondeterminism.**
   - Dimension: test order, timing, shared state, leaked async work.
   - Oracle: the same test giving a different verdict under a controlled change.
   - Tools: Node `--test-randomize`/`--test-random-seed` (F8), and the Node test runner's extraneous-async reporting (F8).
   - Distinct? Partly. Diagnosis of flaky replay already appears in `evidence-based-triage` ("investigating flaky replay") and state leakage in `harness-sensitivity`. Searching test orders to find order-dependent tests is a search dimension no skill names. Inference: it fits `harness-sensitivity` (harness defects) better than a new skill, because an order-dependent test is a harness or test defect, not directly a product bug.

## Existing published skills and plugins (question 3)

| Owner | Evidence inspected | Overlap with this plugin |
|---|---|---|
| `dubzzz/fast-check` `skills/javascript-testing-expert/SKILL.md` (official; fast-check repo, commit `cd9c1884`) | Frontmatter, plus a grep of the 406-line body | Description: "Advocates for property-based testing with fast-check and protects against indeterministic code in tests. Does not cover black-box e2e testing." Body lines 249-253, "Guidelines for race conditions": "leverage `fast-check` and its `fc.scheduler()` arbitrary". It overlaps test authoring and basic scheduler use. It is a test-writing style guide (describe/it naming, file layout), not campaign, oracle, replay or reduction method. A JS reference here should not duplicate its authoring advice. |
| `meta/memlab` `plugins/memlab` (official) | README "Claude Code and Codex" section | Skills `memlab-analyze-heap-snapshot`, `memlab-find-web-leaks`, `memlab-capture-heap-snapshots` and `memlab-memory-tests`, plus an MCP server, installed via `claude plugin marketplace add meta/memlab`. Strong overlap with leak capture and analysis. `resource-complexity-testing` should route to it and own the search and confirmation discipline. Skill bodies not read. |
| `microsoft/playwright` (official; commit `95e5dca3`) | Descriptions of the skills shipped in `packages/playwright-core/src/tools/skills/` | `playwright-cli`: "Automate browser interactions, test web pages and work with Playwright tests." `playwright-trace`: "Inspect Playwright trace files from the command line". `playwright-component-testing`: component testing with a story gallery. These cover driver and trace mechanics; no search or oracle method. The repo's `.claude/skills/*` are for Playwright's own development. |
| `anthropics/skills` `skills/webapp-testing` (commit `2c5958ec`) | Frontmatter and opening section | "Toolkit for interacting with and testing local web applications using Playwright"; it uses "native Python Playwright scripts" and a server-lifecycle helper. Covers driving and inspection; no bugfinding search or oracle method. |
| `google/oss-fuzz` `infra/experimental/agent-skills` (commit `0bb38638`) | README contents table | Skills for C/C++, Go, Rust, JVM (Jazzer), Python (Atheris) and OSS-Fuzz infrastructure. No JavaScript or Jazzer.js skill, so no JS overlap. |
| Community SKILL.md files (GitHub code search, 2026-11-09) | Result paths only; bodies not read | Hits include `mizchi/skills stryker-js/SKILL.md`, `trancee/skills jazzer/SKILL.md`, `bedkillerspacex-boop/codex-skill-library javascript-fuzz-targets/SKILL.md`, many React-testing and Playwright skills, and registry mirrors. None inspected; no claim about their content. |

## Literature leads (question 4)

All **not read**; nothing is claimed from them. Metadata comes from Crossref records, except the USENIX paper (from its USENIX presentation page). Read them through the paper-reader pipeline before using them.

| Area | Title | Authors | Year | Venue | DOI / URL | Status |
|---|---|---|---|---|---|---|
| Node event-loop schedule fuzzing | Node.fz: Fuzzing the Server-Side Event-Driven Architecture | James Davis, Arun Thekumparampil, Dongyoon Lee | 2017 | EuroSys | 10.1145/3064176.3064188 | not read |
| Node event races | NodeRacer: Event Race Detection for Node.js Applications | Andre Takeshi Endo, Anders Møller | 2020 | ICST | 10.1109/ICST46399.2020.00022 | not read |
| Node concurrency bug study | A comprehensive study on real world concurrency bugs in Node.js | Jie Wang, Wensheng Dou, Yu Gao, Chushu Gao, Feng Qin, Kang Yin, Jun Wei | 2017 | ASE | 10.1109/ASE.2017.8115663 | not read |
| Node atomicity violations | Detecting Atomicity Violations for Event-Driven Node.js Applications | Xiaoning Chang, Wensheng Dou, Yu Gao, Jie Wang, Jun Wei, Tao Huang | 2019 | ICSE | 10.1109/ICSE.2019.00073 | not read |
| Browser event races | Race detection for web applications | Boris Petrov, Martin Vechev, Manu Sridharan, Julian Dolby | 2012 | PLDI | 10.1145/2254064.2254095 | not read |
| Browser event races | Effective race detection for event-driven programs | Veselin Raychev, Martin Vechev, Manu Sridharan | 2013 | OOPSLA | 10.1145/2509136.2509538 | not read |
| Event-race control | Repairing Event Race Errors by Controlling Nondeterminism | Christoffer Quist Adamsen, Anders Møller, Rezwana Karim, Manu Sridharan, Frank Tip, Koushik Sen | 2017 | ICSE | 10.1109/ICSE.2017.34 | not read |
| Promise semantics | A model for reasoning about JavaScript promises | Magnus Madsen, Ondřej Lhoták, Frank Tip | 2017 | PACMPL (OOPSLA) | 10.1145/3133910 | not read |
| Promise bugs | Finding broken promises in asynchronous JavaScript programs | Saba Alimadadi, Di Zhong, Magnus Madsen, Frank Tip | 2018 | PACMPL (OOPSLA) | 10.1145/3276532 | not read |
| JS symbolic execution | ExpoSE: practical symbolic execution of standalone JavaScript | Blake Loring, Duncan Mitchell, Johannes Kinder | 2017 | SPIN | 10.1145/3092282.3092295 | not read |
| JS symbolic execution (regex) | Sound regular expression semantics for dynamic symbolic execution of JavaScript | Blake Loring, Duncan Mitchell, Johannes Kinder | 2019 | PLDI | 10.1145/3314221.3314645 | not read |
| JS dynamic analysis | Jalangi: a selective record-replay and dynamic analysis framework for JavaScript | Koushik Sen, Swaroop Kalasapur, Tasneem Brutch, Simon Gibbs | 2013 | ESEC/FSE | 10.1145/2491411.2491447 | not read |
| Node dynamic analysis | Efficient dynamic analysis for Node.js | Haiyang Sun, Daniele Bonetta, Christian Humer, Walter Binder | 2018 | CC | 10.1145/3178372.3179527 | not read |
| ReDoS | The impact of regular expression denial of service (ReDoS) in practice: an empirical study at the ecosystem scale | James C. Davis, Christy A. Coghlan, Francisco Servant, Dongyoon Lee | 2018 | ESEC/FSE | 10.1145/3236024.3236027 | not read |
| ReDoS | Freezing the Web: A Study of ReDoS Vulnerabilities in JavaScript-based Web Servers | Cristian-Alexandru Staicu, Michael Pradel | 2018 | USENIX Security | https://www.usenix.org/conference/usenixsecurity18/presentation/staicu (PDF: https://www.usenix.org/system/files/conference/usenixsecurity18/sec18-staicu.pdf) | not read |
| ReDoS | ReScue: crafting regular expression DoS attacks | Yuju Shen, Yanyan Jiang, Chang Xu, Ping Yu, Xiaoxing Ma, Jian Lu | 2018 | ASE | 10.1145/3238147.3238159 | not read |
| ReDoS | Static Detection of DoS Vulnerabilities in Programs that Use Regular Expressions | Valentin Wüstholz, Oswaldo Olivo, Marijn J. H. Heule, Isil Dillig | 2017 | TACAS (LNCS) | 10.1007/978-3-662-54580-5_1 | not read |
| Client memory leaks | BLeak: automatically debugging memory leaks in web applications | John Vilk, Emery D. Berger | 2018 | PLDI (SIGPLAN Notices record) | 10.1145/3296979.3192376 | not read |
| Web UI exploration | Crawling Ajax-Based Web Applications through Dynamic Analysis of User Interface State Changes | Ali Mesbah, Arie van Deursen, Stefan Lenselink | 2012 | ACM TWEB | 10.1145/2109205.2109208 | not read |
| Web app test generation | A framework for automated testing of JavaScript web applications | Shay Artzi, Julian Dolby, Simon Holm Jensen, Anders Møller, Frank Tip | 2011 | ICSE | 10.1145/1985793.1985871 | not read |
| Flaky tests | An empirical analysis of flaky tests | Qingzhou Luo, Farah Hariri, Lamyaa Eloussi, Darko Marinov | 2014 | FSE | 10.1145/2635868.2635920 | not read |
| Flaky tests (JS) | An Empirical Study of Flaky Tests in JavaScript | Negar Hashemi, Amjed Tahir, Shawn Rasheed | 2022 | ICSME | 10.1109/ICSME55016.2022.00011 | not read |
| Node prototype pollution | Detecting Node.js prototype pollution vulnerabilities via object lookup analysis | Song Li, Mingqing Kang, Jianwei Hou, Yinzhi Cao | 2021 | ESEC/FSE | 10.1145/3468264.3468542 | not read |

No paper on SSR/hydration mismatch testing was found (one Crossref query returned only a 2020 book on React SSR). No papers were searched for fast-check, Jazzer.js, memlab or StrictMode.

## Summary

### Per-skill JS route table

"Method-neutral" means the skill's method applies to JS without a JS-specific tool. Routes cite the findings above.

| # | Skill | Node route | Browser/React route | Status |
|---|---|---|---|---|
| 1 | bugfinding-campaign | Method-neutral; inventory existing Jest/Vitest/node:test, fast-check, Stryker, Playwright lanes | Same | Yes, no tool needed |
| 2 | correctness-oracles | `--unhandled-rejections` mode; extraneous async activity (F8) | React `onRecoverableError`; StrictMode dev-only oracle (F9) | Yes; JS observation-channel notes |
| 3 | harness-sensitivity | StrykerJS (existing), c8 reachability (F7), `--test-randomize` order probe (F8) | StrykerJS with a supporting runner (existing) | Yes |
| 4 | stateful-property-testing | fast-check commands (existing) | fast-check + RTL (F11) or Playwright (F10) for UI sequences | Yes; browser reference needed |
| 5 | semantic-program-generation | Only for program-consuming targets; no generator verified (F16) | None | No verified route |
| 6 | coverage-guided-fuzzing | Jazzer.js (F1), with the maintenance gap and floor mismatch noted | None found | Node yes; browser no |
| 7 | corpus-evolution | Jazzer.js libFuzzer corpus dirs and regression mode (F1); c8 (F7) | None | Node partial |
| 8 | semantic-differential-testing | Node versions, modes; method-neutral | SSR vs client hydration (F9) | Yes; hydration example |
| 9 | metamorphic-testing | Method-neutral | Method-neutral | Yes, no tool needed |
| 10 | native-memory-instrumentation | Native addons only; no recipe verified (F16) | None | No credible JS route |
| 11 | race-detection-campaigns | Only SharedArrayBuffer across workers; no detector found (F16) | Same | No credible route; event races go to #12 |
| 12 | schedule-exploration | fast-check scheduler (F2); mock timers are virtual time only (F8); Node.fz/NodeRacer stale (F3, F5) | fast-check scheduler + MSW (F11); `act` limit (F9) | Yes (randomized, promise-level) |
| 13 | linearizability-checking | Export history to Porcupine (Go) or Knossos via elle-cli (F13) | n/a | Yes, via adapter |
| 14 | transactional-history-testing | elle-cli JSON histories, Java 21+ (F13) | n/a | Yes, via adapter |
| 15 | distributed-fault-testing | Toxiproxy + Node client, network faults only (F12) | MSW mocks are not real faults (F11) | Partial |
| 16 | deterministic-simulation | None found (F16) | None | No route found |
| 17 | crash-consistency-testing | None JS-specific found (F16) | None (browser storage not researched) | No route found |
| 18 | symbolic-concolic-execution | ExpoSE, Node 21.7.2 only, research-grade (F4) | ExpoSE Electron mode, "limited" (F4) | Weak |
| 19 | bounded-model-checking | None found (F16) | None | No route found |
| 20 | resource-complexity-testing | Heap snapshots (F8), memlab Node assertions (F6), ReDoS detectors (F14) | memlab scenarios (F6) | Yes |
| 21 | liveness-testing | No JS tool verified | No JS tool verified | Method-neutral only |
| 22 | failure-reduction | fast-check shrinking (existing); Jazzer.js minimization not verified | Playwright traces as replay artifacts (F10) | Partial |
| 23 | evidence-based-triage | Method-neutral | Playwright traces (F10) | Yes |
| 24 | configuration-differential-testing | Node LTS lines, ESM vs CJS (F1 instrumentation difference) | Chromium/Firefox/WebKit (F10); React dev vs prod (F9) | Yes |
| 25 | numerical-oracles | No JS binding verified (existing note) | Same | No route verified |

### Candidate new skills

- **Recommended: no new skill on present evidence.** Every failure space in question 2 maps onto an existing boundary: async races go to `schedule-exploration`, UI sequences to `stateful-property-testing`, hydration to `semantic-differential-testing`, leaks and ReDoS to `resource-complexity-testing`, and flaky order dependence to `harness-sensitivity`. Inference: each needs a JS/browser reference inside its owning skill, not a new method skill.
- **Considered, not justified yet: `ui-state-exploration`** (browser event-sequence search). It would be separate only if UI exploration needs a method the stateful skill cannot carry: state abstraction or merging for DOM states, crawl strategy, and actionability. The two papers in the table (Mesbah et al. 2012, Artzi et al. 2011) are the evidence that could justify it, and both are unread. No maintained JS crawler was verified. Decide after the paper-reader pass.
- **Rejected: a `redos` skill.** It is a producer inside `resource-complexity-testing` with the same measured-growth oracle (F14).
- **Rejected: a `react-strictmode` / concurrent-rendering skill.** StrictMode is a fixed development-only check (F9). No API for searching concurrent interleavings was found.
- **Rejected: a JS event-race detector skill.** Every available tool is unmaintained research code (F3, F5).
- **Rejected: a `flaky-tests` skill.** Covered by `harness-sensitivity` and `evidence-based-triage`, with Node's randomize flags as a tool (F8).

### Proposed reference additions (scope for the plan; not drafted)

- `coverage-guided-fuzzing`: Jazzer.js reference covering Node targets, ESM instrumentation floor, async targets, bug detectors and maintenance gap (F1). Update the plan's line-322 row.
- `schedule-exploration`: JS reference covering the fast-check scheduler's control boundary, `schedulerFor` replay, timers through fake timers, MSW response ordering, the `act` batching limit, and Node mock timers as virtual time (F2, F8, F9, F11).
- `stateful-property-testing`: browser/React subsection covering RTL and Playwright drivers, auto-wait masking, state reset, and DOM/accessibility-tree observation (F10, F11).
- `resource-complexity-testing`: Node heap snapshot caveats, memlab routing and ReDoS producers (F6, F8, F14).
- `semantic-differential-testing`: SSR/hydration worked example (F9).
- `harness-sensitivity`: c8 reachability, `--test-randomize`, extraneous async activity (F7, F8).
- `linearizability-checking` and `transactional-history-testing`: a note on recording histories from a Node client (F13).
- `distributed-fault-testing`: Toxiproxy Node client (F12).

### Open questions for the user

1. Should browser UI event-sequence exploration be a reference inside `stateful-property-testing` (my recommendation on present evidence), or should the deferred GUI/browser candidate get a dedicated skill after the UI-exploration papers are read?
2. Is a research-grade ExpoSE route (Node 21.7.2 only) acceptable in `symbolic-concolic-execution`, or should that skill state that JS has no credible route?

### Unverified or open items

- Jazzer.js: supported platforms (README vs v4.0.0 notes on Linux arm64); real Node floor (core `>= 14.0.0` vs root `>= 20.11.0`); whether libFuzzer sanitizers apply to native addons; input minimization commands.
- recheck: whether it outputs attack strings. eslint-plugin-regexp rules not read.
- memlab plugin skill bodies, community SKILL.md bodies, and the full fast-check `javascript-testing-expert` body were not read beyond the cited lines.
- Licenses unresolved: elle-cli (`NOASSERTION`), Node.fz (`NOASSERTION`), Node core (`NOASSERTION` in the GitHub API); the Toxiproxy Node client declares ISC only in package.json.
- No search was completed for JS deterministic simulation, bounded model checking, crash-consistency or browser-storage tools, Node-addon sanitizer recipes, or semantic JS program generators. "No route found" there is bounded, not exhaustive.
- No maintained JS UI crawler was verified; Crawljax's README was not read.
- The single-threaded-isolate premise behind the `race-detection-campaigns` row (F16) is an inference not verified from a primary source.
- No tool was installed or run. Every behavior stated comes from documentation or source at the pinned commit, not from execution.
- All 23 papers are unread.

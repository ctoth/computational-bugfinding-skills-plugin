# Research: JS/TS schedule exploration (group B)

Skills: `schedule-exploration` (main), boundary note for `race-detection-campaigns`.
Branch: js-web-bugfinding. Researcher: Phase 3 group B. Date: 2026-11-09.

Status: complete for drafting, with the open items listed under "Unverified". No skills, manifests, README or agent-notes were edited. Nothing was installed, run, committed or pushed. No new paper was read (see L2: the paper-reader skill is not available in this agent's tool set).

## Inputs read

- `reports/skill-plan-js-web-bugfinding.md:31-32, 48-58` (schedule-exploration and race-detection rows; batch-2 literature).
- `reports/skill-research-js-web-bugfinding.md` F2 (lines 48-66), F3 (68-77), F5 (89-101), F8 (128-147), F9 (149-169), F11 (185-192), F16 (238-249).
- `plugins/bugfinding/skills/schedule-exploration/SKILL.md` and `references/{controlled-boundaries,common-mistakes,replay-and-reduction}.md`, `references/sources.yaml`; `plugins/bugfinding/skills/race-detection-campaigns/SKILL.md`; `stateful-property-testing/references/runtime-recipes.md:19` and `stateful-property-testing/SKILL.md:26` (existing fast-check mentions).
- `reports/research-schedule-exploration.md` (evidence standard: pinned primary sources, short quote fragments, Decision lines).
- Paper notes (already read via paper-reader by other agents; page numbers are PDF pages as recorded in those notes): Endo 2020 NodeRacer, Davis 2017 Node.fz, Wang 2017 NodeCB, Raychev 2013 EventRacer, Adamsen 2017 EventRaceCommander, all under `C:/Users/Q/code/papers/`.

## Findings

### L1. Literature, from existing paper-reader notes (no re-read)

- NodeRacer (Endo 2020, `C:/Users/Q/code/papers/Endo_2020_NodeRacerEventRaceDetectionNodejs/notes.md`):
  - Observation uses Async Hooks `init` (callback id, running callback id, type Immediate/Timeout/TickObject/Promise/Other, timeout delay), `before`, and `promiseResolve`. Async Hooks does not say which function is the callback, so a function entry/exit tracer (njsTrace) is added, and `Promise.all`/`Promise.race` are monkey-patched (notes p.3-4).
  - Nine happens-before rules: registration, promise settlement, same-tick FIFO for Immediate/nextTick/Promise, cross-tick FIFO, timeouts ordered only when the earlier-registered has delay <= the later, setInterval chain, Promise.all join, Promise.race any-of, nextTick priority (p.4).
  - Guided execution: postpone a ready callback (indegree 0) by default 500 ms with probability 1/2 only if another ready callback exists; each callback postponed at most once; a callback whose predecessors have not run is postponed (p.5).
  - Diagnosis mode postpones exactly one callback per run, a different one each run, to localize the callback tied to the failure (p.6).
  - Oracle is observable failure (crash, hang, test failure), not memory races (p.2). NR-naive (no HB) produced HB-violating runs in 64.1% of runs on average, and more than half of its failures involved an HB violation, so unguided perturbation yields infeasible-schedule false alarms (p.8). Tests with random timeouts break HB inference (objection.js false alarm, p.9).
  - Limits: misses HB from third-party libraries/addons; single process; no worker threads; misses races landing in an external service (p.10). Tool URL brics.dk/noderacer not checked by the notes; the repo pinned in F5 states Node 10.16.3.
- Node.fz (Davis 2017, notes): modified libuv on Node v0.12.7 shuffles/defers timers, ready fds, close events and worker-pool work; keeps libuv timer order and EventEmitter order, so races depending on those are not explored; tests asserting timer precision fail under fuzzing ("race against time") and must be told apart from real races; no replay (notes p.9-13). Racing resources include DB and FS state (p.4-6).
- NodeCB (Wang 2017, notes): 57 bugs; 65% atomicity, 30% order, 5% starvation; 93% need ordering of at most 4 events, 95% one process, 86% one racing resource (p.2, 4-9). Starvation from nextTick/setImmediate priority. Dataset URL returned 404 on 2026-11-09 per the NodeRacer notes; issues are listed as project#issue URLs (p.11).
- EventRacer (Raychev 2013, notes): browser HB over parse/script/timer/network/user event actions; needs instrumented WebKit; predates promises and frameworks (notes p.1-2, 15).
- EventRaceCommander (Adamsen 2017, notes): proxy (mitmproxy) instruments HTML/JS; wraps `setTimeout`, XHR `send`/`onreadystatechange`; root capture-phase listeners; postpones by async re-dispatch, discards via `stopImmediatePropagation`+`preventDefault` (p.7). Replay uses recorded server responses and dynamic URLs break replay (p.9). The paper predates React.
- **Decision:** the JS reference states the method (record causality, perturb only within it, observable-failure oracle, one-postponement diagnosis, start at <= 4 events on one resource including DB/FS) and states that the research tools are pinned to old runtimes. It must not offer NodeRacer or Node.fz as runnable routes.

### S1. fast-check scheduler: API, control boundary, selection policy, replay

Pinned: `dubzzz/fast-check` at `cd9c1884e8a39fe945600fbcda1ec92d518feaa0` (still main HEAD on 2026-11-09, committed 2026-11-09T09:02:12Z; version 4.10.2 per F2). Files read: `website/docs/advanced/race-conditions.md` (312 lines); `packages/fast-check/src/arbitrary/scheduler.ts`; `.../_internals/SchedulerArbitrary.ts`; `.../_internals/helpers/BuildSchedulerFor.ts`; `.../_internals/implementations/SchedulerImplem.ts` (430 lines); `packages/fast-check/src/check/model/commands/ScheduledCommand.ts`. URL base: `https://raw.githubusercontent.com/dubzzz/fast-check/cd9c1884e8a39fe945600fbcda1ec92d518feaa0/`. I also grepped every `website/docs/**/*.md(x)` file at that commit for fake-timer and scheduler mentions.

Note: `stateful-property-testing` pins fast-check at `5ec2e3ac` (`runtime-recipes.md:19`). The drafter should either cite `cd9c1884` for scheduler facts and keep both pins visible, or re-check the scheduler files at `5ec2e3ac`; I did not read them at that commit.

API facts (docs `race-conditions.md`):
- `schedule(task, label?, metadata?, act?)`: "The newly created promise will resolve when the scheduler decides to resolve it" (line 23). "The life-cycle of the wrapped `Promise` will not be altered at all" (line 52). Continuations on the original promise are "not impacted by the scheduler" (lines 82-85).
- `scheduleFunction(fn, act?)`: "only postponing the resolution of the function. The call to the function itself is started immediately" (line 118).
- `scheduleSequence(items, act?)`: "Each operation requires the previous one to be resolved before being started"; while one sequence task runs, "no other scheduled task in the scheduler can be unqueued while this task has not ended", so sequence items must not wait on other scheduled tasks (lines 25, 150).
- Current waiting API is `waitNext(count)`, `waitIdle()`, `waitFor(promise)` (lines 26-28). **`waitOne`, `waitAll` and `count()` are "deprecated since v4.2.0"** (lines 33-35); prefer `waitNext(1)` and `waitIdle`. This corrects the team-lead brief and plan wording, which name `waitOne/waitAll` as current.
- `waitIdle`: "Cannot await tasks triggered by uncontrolled sources like `fetch` or external event emitters" (line 27).
- `waitFor`: uncontrolled triggers "stay out-of-control for fast-check" and "might make replay of failures harder" (line 28).
- `report()`: all tasks scheduled so far with status, output/error string, "in the order they get executed by the scheduler" (line 29).
- `fc.schedulerFor(ordering: number[])` or the template-literal form gives a hardcoded order; task ids start at 1 in scheduling order (line 45; `scheduler.ts:79-80`).
- Mocked-server recipe (lines 210-245): `scheduleFunction` alone means "the mocked-server will always receive the calls in the same order as they were made"; prefixing each call with `s.schedule(Promise.resolve('Server received the call')).then(() => f(...args))` lets the server receive calls in either order, and the second variant also schedules the response.
- React (lines 247-264): `fc.scheduler({ act })` wraps all scheduled tasks; per-call `act` arguments allow finer wrapping; "when testing React applications, one cannot perform updates of states outside of `act`."
- Native timers (lines 266-304): timers "are ordered ... Consequently, they require special handling". The only recipe in the docs uses **Jest** (`jest.useFakeTimers()`, `jest.getTimerCount()`, `jest.advanceTimersToNextTimer()`) inside a custom `act` that schedules one "advance timers" task whenever timers are pending; "it can be modified for other testing frameworks if necessary". No Vitest or `node:test` recipe appears anywhere in the docs tree (grep result).
- `scheduledModelRun` (lines 306-312): model execution is processed through the scheduler; "Neither `check` nor `run` should rely on the completion of other scheduled tasks". Source: each command's `check` and `run` is wrapped as a one-item `scheduleSequence` (`ScheduledCommand.ts:16-58`).

Implementation facts (source):
- Selection policy: `SchedulerArbitrary.ts:13-20` picks `clonedMrng.nextInt(0, scheduledTasks.length - 1)`, a uniform random choice among currently pending scheduled tasks, from the property's random generator. No systematic, bounded or exhaustive enumeration exists in these files (fact for these files; I did not search the whole repo for another enumerator).
- No shrinking of the schedule: `canShrinkWithoutContext` returns false and `shrink` returns `nil`, both commented "Not supported yet" (`SchedulerArbitrary.ts:32-40`). Shrinking a failing property shrinks the other arbitraries; the schedule itself is regenerated from the random stream, not minimized.
- Counterexample printing: `toString()` emits a `schedulerFor()` template literal listing tasks as `[task${id}] <type>::<label> <status> with value ...` (`SchedulerImplem.ts:61-66, 420-429`), which is the format `fc.schedulerFor()` accepts (`scheduler.ts:30-52`).
- `schedulerFor` checks only order: it throws if too many tasks are scheduled or a named task id is not pending (`BuildSchedulerFor.ts:10-16`), and "will neither check that all the referred promises have been scheduled nor that they resolved with the same status and value" (`scheduler.ts:54-57`).
- `cloneMethod` rebuilds the scheduler from the cloned source selector (`SchedulerImplem.ts:54-58`), so fast-check's own seed/path replay regenerates the same choice stream.
- `waitFor`/`waitIdle`/`waitNext` yield `numTicksBeforeScheduling = 50` microtask ticks (`await Promise.resolve()`) before releasing the next task (`SchedulerImplem.ts:12, 268-272`). Inference: work that becomes ready only after a macrotask (I/O, real timers) is not waited for by these ticks.
- Release is serialized: once a task is chosen, the scheduler waits for the wrapped promise before scheduling anything else (docs line 55; `internalWaitOne` at `SchedulerImplem.ts:219-231` triggers one task inside its `act`).

Decisions:
- Control boundary statement for the drafter: fast-check controls only the resolution order of promises passed through `schedule`/`scheduleFunction`/`scheduleSequence`/`scheduledModelRun`; calls start immediately; original-promise continuations, `fetch`, external emitters, real timers and I/O completions are outside it unless the harness routes them through the scheduler. This maps to the existing Loom "invisible" boundary (SKILL.md:12).
- Search policy statement: uniform random choice among pending tasks per step; not systematic, not bounded-exhaustive, no PCT-style depth, no schedule shrinking. A passing run says nothing about orders not sampled.
- Replay statement: keep the fast-check seed and path (property replay) and, for a direct hardcoded replay, the printed `schedulerFor` block. `schedulerFor` replays order only; it does not confirm the same tasks or values, so the drafter must say to check the replayed `report()` against the original.
- Use `waitNext`/`waitIdle`, not the deprecated `waitOne`/`waitAll`.

### S2. Timers: which fake-timer combinations exist, and what each fakes

- fast-check docs show only the Jest combination (S1).
- Jest, pinned `jestjs/jest` main at `72614448ecb9d16c58d6474b3091247c14a5c090` (`packages/jest-cli/package.json` version 30.5.2), `docs/JestObjectAPI.md`:
  - Lines 904-906: fake timers swap out "`Date`, `performance.now()`, `queueMicrotask()`, `setImmediate()`, ... `setTimeout()`, `clearTimeout()`", and in Node also "`process.hrtime`, `process.nextTick()`"; in JSDOM also `requestAnimationFrame()` and `requestIdleCallback()`. Backed by `@sinonjs/fake-timers` (line 902).
  - Line 1088: `advanceTimersToNextTimer(steps)` "Advances all timers by the needed milliseconds so that only the next timeouts/intervals will run." Line 1120: `getTimerCount()` "Returns the number of fake timers still left to run."
  - Inference (not tested): because Jest's default fakes `queueMicrotask` and `process.nextTick`, target code that defers work through them does not run until fake time is advanced, while native promise continuations (which fast-check's own 50-tick wait uses) still run. A drafter should tell the agent to list the faked APIs (`doNotFake`, line 940) in the run record.
- Vitest, pinned `vitest-dev/vitest` main at `3a76b87324ecb8d25509cd009aa87fbe56819c39` (root `package.json` version 5.1.0), `docs/api/vi.md`:
  - `vi.useFakeTimers()` wraps `setTimeout`, `setInterval`, their clears, `setImmediate`, `clearImmediate` and `Date`; it "does not automatically mock `process.nextTick` and `queueMicrotask`" unless `toFake: ['nextTick', 'queueMicrotask']` (lines 1211-1227). Mocking `nextTick` is unsupported under `--pool=forks` (line 1219). Based on `@sinonjs/fake-timers`.
  - `vi.advanceTimersToNextTimer()` "Will call next available timer" (line 1002ff); `vi.getTimerCount()` "Get the number of waiting timers" (line 1058ff).
  - `vi.setTimerTickMode` (since 4.1.0): `manual` is the default; `nextTimerAsync` advances automatically after each macrotask; `interval` advances by a fixed interval.
  - Inference: the fast-check Jest recipe ports to Vitest by replacing `jest.getTimerCount`/`jest.advanceTimersToNextTimer` with `vi.getTimerCount`/`vi.advanceTimersToNextTimer`, in `manual` tick mode. fast-check does not document this port; mark it unverified until run.
- Node `node:test`, tag `v26.13.0`, `doc/api/test.md`:
  - `MockTimers` "is now stable" as of v23.1.0 (lines 2894-2905 YAML).
  - `enable({ apis, now })`: supported values `'setInterval'`, `'setTimeout'`, `'setImmediate'`, `'Date'` (lines 2915-2945); with no arguments it mocks those in `node:timers`, `node:timers/promises` and `globalThis` (lines 2992-2998). `process.nextTick` and `queueMicrotask` are not in the list.
  - Methods documented: `enable`, `reset`, `[Symbol.dispose]`, `tick(ms)` ("Advances time for all mocked timers", line 3037), `runAll()` ("Triggers all pending mocked timers immediately", line 3355), `setTime(ms)` (line 3411). There is **no pending-timer count and no advance-to-next-timer method** in the method list (headings at lines 2915, 3000, 3025, 3029, 3346, 3411).
  - Consequence (inference): the fast-check timer recipe cannot be ported to `node:test` mock timers as written, because it needs a pending-timer count and a next-timer step. An agent on `node:test` either routes the timer callbacks through `s.schedule` by hand or uses `@sinonjs/fake-timers` directly (not read in this pass).
- **Decision:** the drafter writes: fake timers give virtual time; combined with fast-check they make timer firing one more scheduled task, which is still random choice among pending tasks, not timer-order enumeration. The fast-check timer recipe is documented for Jest only; Vitest has the same two methods (port unverified); `node:test` mock timers lack them.

### S3. React `act` and its batching limit

Pinned: `reactjs/react.dev` main at `7594a2b008489121bdf25f97320d11ac0422510e`, `src/content/reference/react/act.md`.
- Line 30: `act()` "makes sure all updates related to these 'units' have been processed and applied to the DOM before you make any assertions."
- Line 45: use `act` with `await` and an async function; the sync version "doesn't work in all cases"; React "will deprecate and remove the sync version".
- Line 53: updates inside `actFn` "are added to an internal act queue, which are then flushed together".
- Line 158: requires `global.IS_REACT_ACT_ENVIRONMENT=true`; line 176: React Testing Library sets it.
- Inference (stated as such): the schedule granularity under `fc.scheduler({ act })` is one scheduled task per `act` flush. Interleavings among React updates queued inside a single flush, and React's own production scheduling of those updates, are not explored. The docs do not describe how the act queue differs from production scheduling beyond "closer to how React works in the browser" (line 15).
- **Decision:** the reference says: wrap scheduled tasks in `act` (via `fc.scheduler({ act })` or per-call `act`), use async `act`, and report that orderings inside one `act` flush are not searched.

### S4. MSW response ordering

Pinned: docs `mswjs/mswjs.io` main at `bda552ebaadde6d75870b4d07de734f9de35fd89`; library per F11 (`mswjs/msw` `9bbfe99c`, version 3.0.4).
- `src/content/docs/http/mocking-responses/response-timing.md:13`: `delay()` "returns a promise that resolves after a certain amount of time"; global delay via a fallthrough `http.all('*', async () => { await delay(500) })` handler or a higher-order resolver (lines 56-90). Imports are `msw/http` and `msw/utils/delay` (lines 16-17).
- `src/content/api/delay.md`: default no delay (line 14); implicit `delay()` is random ~100-400 ms (line 28) and "when testing in Node.js, the implicit delay is negated" (line 44); `delay('infinite')` "indefinitely delays the response, making it pend forever" (line 99).
- MSW docs contain no recipe for controlling the relative order of two responses (searched docs tree for delay/order/race/concurrency page names; only timing pages exist). Delay-based ordering is wall-clock and, for implicit delay, random without a recorded seed.
- The controllable seam is fast-check's "Scheduling a call to a mocked server" recipe (S1) applied inside an MSW resolver: the resolver is an async function, so it can await a promise registered with `s.schedule(...)` before returning the response. Inference from two documented APIs; not shown in either project's docs and not run.
- **Decision:** the reference names response order through MSW as "resolver awaits a scheduler-controlled promise", says delays alone are timing perturbation, not ordered choices, and offers `delay('infinite')` for never-settling responses (useful for history recording of pending operations).

### S5. NodeRacer-style observation on current Node: what `node:async_hooks` and related APIs support

All from `nodejs/node` tag `v26.13.0`, `doc/api/async_hooks.md`, `doc/api/async_context.md`, `doc/api/v8.md`, `doc/api/process.md`, `doc/api/documentation.md`.

Stability, per API:

| API | Stability at v26.13.0 | Source |
|---|---|---|
| `async_hooks.createHook`, `AsyncHook`, `executionAsyncResource` | "Stability: 1 - Experimental. Please migrate away from this API, if you can"; "We strongly discourage the use of the `async_hooks` API" | `async_hooks.md:5-18` |
| `executionAsyncId()`, `triggerAsyncId()` | covered by the module banner (Experimental); no separate marker | `async_hooks.md:5, 756, 810` |
| `AsyncLocalStorage` (class, `run`, `getStore`), `AsyncResource` | "Stability: 2 - Stable" (module banner) | `async_context.md:5` |
| `AsyncLocalStorage.disable`, `enterWith`, `exit`, `withScope`, class `RunScope` | each "Stability: 1 - Experimental" | `async_context.md:218, 258, 358, 395, 533` |
| `v8.promiseHooks` (`onInit`, `onSettled`, `onBefore`, `onAfter`, `createHook`) | no stability marker found in the section or module header; added v17.1.0/v16.14.0 | `v8.md:1-16, 944-1180` |
| `process.getActiveResourcesInfo()` | changed "from Experimental to Stable" in v24.0.0/v22.16.0 | `process.md:2285-2297` |

Definition (`documentation.md:31-34`): Experimental "is not subject to semantic versioning rules. Non-backward compatible changes or removal may occur in any future release."

What a target-specific observer can record (facts from the docs):
- Creation causality: `init(asyncId, type, triggerAsyncId, resource)`; `triggerAsyncId` "shows _why_ a resource was created", while `executionAsyncId()` "only shows _when_" (`async_hooks.md:308-316, 368-373`). This is NodeRacer's Rule 1 input.
- Callback execution boundaries: `before(asyncId)` "just before said callback is executed", 0 to N times per resource; `after(asyncId)` immediately after (`async_hooks.md:589-614`).
- Promise settlement: `promiseResolve(asyncId)` "when the `resolve` function passed to the `Promise` constructor is invoked"; the promise "is not necessarily fulfilled or rejected at this point" if it adopted another promise (`async_hooks.md:631-660`). This is NodeRacer's Rule 2 input.
- Promise tracking: `createHook` has a `trackPromises` option, default `true`, which "Cannot be `false` if `promiseResolve` is set" (`async_hooks.md:159-160`). Without any installed hook, promise callbacks get wrong ids ("eid 1 tid 0"); installing a hook "forces PromiseHooks to be enabled" (`async_hooks.md:847-905`).
- Resource types: values include `Timeout`, `Microtask`, `FSREQCALLBACK`, `TCPWRAP` and `PROMISE`; "The `type` of resources created by Node.js itself can change in any Node.js release" (`async_hooks.md:343-358`).
- `v8.promiseHooks.onInit(promise, parent)` gives the parent promise of a continuation, and `before`/`after` around `then`/`await` resumptions (`v8.md:944-990`).

What it cannot observe or do (facts, with inferences marked):
- Function identity: the `resource` object for Node-created resources is internal, "no API is specified", and may be reused, so it is "not safe to use it as a key in a `WeakMap`" (`async_hooks.md:430-438`). The docs give no way to map an `asyncId` to the JS function that will run; NodeRacer added njsTrace for this (notes p.4).
- Promise `before`/`after` fire "only on chained promises", not on promises not created by `then()`/`catch()` (`async_hooks.md:907-912`).
- Workers: "each thread has an independent `async_hooks` interface, and each thread will use a new set of async IDs" (`async_hooks.md:44-45`), so cross-worker causality is not recorded.
- Context loss: callback-based APIs and custom thenables can lose `AsyncLocalStorage` context unless wrapped in `AsyncResource` (`async_context.md:511-525`). Inference: the same gap breaks causality links for libraries with their own callback queues (matches NodeRacer limit p.10).
- Reordering: every hook is a notification callback; `init`/`before`/`after`/`destroy` "_must not_ be async functions that return promises" (`async_hooks.md:205-208`), and the docs describe no return value or API that delays a callback. Inference: async_hooks can record causality but cannot postpone or reorder anything. Postponement must come from a seam the target already exposes or the harness adds at its own call boundaries (for example wrapping a DB client method with `scheduleFunction`, or the target's own queue), which is exactly what fast-check does for promises.
- Overhead: `destroy` "enables tracking of `Promise` instances via the garbage collector" (`async_hooks.md:624-627`); promise tracking "can cause a significant performance overhead" (`async_hooks.md:916-918`). Inference: observation perturbs timing, so a recorded order is evidence of one run, not of the uninstrumented schedule distribution.
- `AsyncLocalStorage` propagates a store; it exposes no ids or parent links (`async_context.md:9-27`, class API list). Inference: it can tag which logical request a callback belongs to, not the happens-before edge between two callbacks.

Decisions:
- The drafter may describe a NodeRacer-style diagnostic as: record `init`/`before`/`after`/`promiseResolve` with `triggerAsyncId` to see which callbacks were concurrently ready in a failing test, then perturb only at seams the harness controls, keeping orders the recorded causality forbids out of the search (NodeRacer p.5, p.8). It must say `createHook` is Experimental and discouraged by Node, types change across releases, function identity needs separate tracing, and workers are separate.
- No tool is designed or recommended here; the reference should not ship a hook-based scheduler.

### S6. Browser seam: Playwright routing and pre-load actions

Pinned: `microsoft/playwright` main at `95e5dca31981bcd0970165853fcc713269d2433a` (version `1.66.0-next` per F10). Files: `docs/src/api/class-page.md`, `docs/src/api/class-route.md`, `docs/src/api/params.md`, `docs/src/network.md`.
- Holding: `Page.route` (since v1.8): "every request matching the url pattern will stall unless it's continued, fulfilled or aborted" (`class-page.md:3746-3752`). The handler is async in every example (`class-page.md:3860-3890`). Inference: a handler that awaits a harness-controlled promise before calling `route.continue()`/`route.fulfill()` holds that request, and releasing two held routes in a chosen order sets the order in which the page sees them. Not shown as a recipe in the docs; not run.
- Releasing: `Route.continue` "Sends route's request to the network with optional overrides" (`class-route.md:36-44`); `Route.fulfill` "Fulfills route's request with given response" (`class-route.md:568-572`); `Route.fetch` (since v1.29) "Performs the request and fetches result without fulfilling it, so that the response could be modified and then fulfilled" (`class-route.md:442-447`). Inference: `route.fetch()` then a held `route.fulfill({ response })` reorders real server responses without a mock, which is the response-reordering half of EventRaceCommander (Adamsen notes p.3, p.7).
- `Route.fallback` (since v1.23) passes to other matching handlers; multiple matching routes run "in the order opposite to their registration" (`class-route.md:155-165`); page routes take precedence over context routes (`class-page.md:3892-3894`).
- Limits stated in docs: `Page.route` "will not intercept requests intercepted by Service Worker"; recommendation is `serviceWorkers: 'block'` (`class-page.md:3758-3760`). It "will not intercept the first request of a popup page"; use `BrowserContext.route` (`class-page.md:3762-3764`). For redirects "the handler will only be called for the first url" (`class-page.md:3754-3756`). "Enabling routing disables http cache" (`class-page.md:3896-3898`). Inference: disabling the cache changes load timing versus production, and a PWA's service worker must be blocked, which removes its behavior from the test.
- Acting before load: `waitUntil` values are `load` (default), `domcontentloaded`, `networkidle` ("**DISCOURAGED**"), and `commit` ("when network response is received and the document started loading") (`params.md:1-9`). Inference: `page.goto(url, { waitUntil: 'commit' })` returns before scripts finish, and holding script requests with `page.route` keeps them unloaded while the test clicks or types, which is the "user acts before scripts load" assumption (Adamsen notes p.3).
- Pre-page instrumentation: `Page.addInitScript` runs "after the document was created but before any of its scripts were run", for every navigation and child frame (`class-page.md:566-576`); "The order of evaluation of multiple scripts installed via `BrowserContext.addInitScript` and `Page.addInitScript` is not defined" (`class-page.md:617-620`). Inference: an init script can wrap `setTimeout`/`fetch`/`XMLHttpRequest` in the page, the in-page part of EventRaceCommander, without a proxy; the in-page wrapper controls only what it wraps, the same boundary as S1.
- **Decision (verifies the plan's inference at `skill-plan-js-web-bugfinding.md:53`, with corrections):** Playwright supports holding and releasing requests in a chosen order (route handlers stall until continued/fulfilled), returning before load (`waitUntil: 'commit'`), and installing in-page wrappers before page scripts (`addInitScript`). The reference must state: service-worker requests are not intercepted unless workers are blocked; routing disables the HTTP cache; the order of multiple init scripts is undefined; and what the harness does not hold (WebSockets not checked, timers not wrapped, React scheduling) stays uncontrolled. The ordering choices are made by the harness, so replay means recording the release order the harness chose, not a Playwright trace alone.

### S7. `race-detection-campaigns` boundary: single-threaded agents, shared memory only via SharedArrayBuffer/Atomics

ECMAScript, pinned `tc39/ecma262` main at `828d35d00f8584c4a0fbcac7742b57c7b959c3f3`, `spec.html`:
- Line 11883: "At any point in time, there is at most one execution context per agent that is actually executing code."
- Line 12332: "An agent comprises a set of ECMAScript execution contexts, an execution context stack, a running execution context, an Agent Record, and an executing thread."
- Lines 12142-12152 (jobs): a job runs "when there is no running context in the agent for which the job is scheduled and that agent's execution context stack is empty"; "Only one Job may be actively undergoing evaluation at any point in time in an agent." This is the run-to-completion property: a promise job or host task cannot interleave with another inside one agent.
- Line 52687 (memory model): it "specifies the possible orderings of Shared Data Block events, arising via accessing TypedArray instances backed by a SharedArrayBuffer and via methods on the Atomics object"; without data races the ordering "appears as sequentially consistent".
- Lines 53249-53263: "data race" is defined only over events in `SharedDataBlockEventSet(execution)`; a program is "data race free if all its executions are data race free". Shared Data Blocks are created by `CreateSharedByteDataBlock` (used at lines 45900-45904, the SharedArrayBuffer allocation path).
Node, tag `v26.13.0`, `doc/api/worker_threads.md` (Stability: 2 - Stable): "enables the use of threads that execute JavaScript in parallel"; "Unlike `child_process` or `cluster`, `worker_threads` can share memory. They do so by transferring `ArrayBuffer` instances or sharing `SharedArrayBuffer` instances" (lines 35-36); "The `Worker` class represents an independent JavaScript execution thread" (line 1474).

Detector search (bounded, negative): `gh search repos` for "SharedArrayBuffer race detector", "data race detector javascript workers", "Atomics race detection", "javascript shared memory race detection", "tsan javascript worker" returned no repositories; one web search ("data race detector for JavaScript SharedArrayBuffer Atomics web workers tool") returned tutorials and lock libraries, no detector. Not proof of absence.

Inference not verified: native addons and WebAssembly threads can also share memory inside a Node process; those are native-memory questions, not checked here.

- **Decision:** the boundary note says: within one agent (main thread, one worker, one browser page's main thread), JS runs one job at a time to completion, so memory-access race detectors have nothing to report for ordinary JS; event and promise ordering bugs go to `schedule-exploration`. Memory-level data races exist in JS only on SharedArrayBuffer-backed memory accessed from more than one agent (workers); no maintained JS detector was found, so the note says "no verified route". Cite ECMA-262 lines above and the Node worker_threads lines. This verifies the F16 inference (`skill-research-js-web-bugfinding.md:243-245`).

### L2. Literature leads not read, and why

The research-papers `paper-reader` skill is not in this agent's tool set (tools available: Read, Glob, Grep, Bash, WebSearch, WebFetch, Write, SendMessage; no Skill tool). Under the standing rule, a paper not read through paper-reader is "not read", so I state nothing from these papers. Ranked by how much they could change guidance:
1. Chang et al. 2019, NodeAV (atomicity violations in Node.js, ICSE 2019). Most likely to change guidance: it names "supposedly-atomic event pairs" (as summarized in the NodeRacer notes p.10), which could tell an agent where to place scheduler seams first. Atomicity violations are 65% of NodeCB bugs (Wang notes p.2).
2. Loring, Marron, Leijen 2017, Semantics of asynchronous JavaScript (DLS). Could correct queue-priority statements (nextTick vs promise vs setImmediate) that the reference may make; cited by NodeRacer for Rules 1-4 (notes p.4).
3. Madsen et al. 2017 promise graph and Alimadadi et al. 2018 broken promises: likely promise-misuse patterns (oracles) rather than schedule search; lower priority for this skill.
Recommendation: the lead spawns a paper-reader agent for items 1 and 2 before the drafter writes method text that depends on them. The reference can be drafted without them on the evidence above.

## Decisions for the drafter

1. Add `references/javascript-event-loop.md` to `schedule-exploration`; update the description to name Node and browser promises/callbacks (plan row line 31).
2. Route order in the reference: (a) fast-check scheduler as the only maintained JS controller (S1); (b) timers via fake timers, Jest recipe documented, Vitest port unverified, `node:test` lacks the needed methods (S2); (c) React via `act` wrapping with the per-flush granularity limit (S3); (d) response order through an MSW resolver awaiting a scheduled promise, or in a real browser through held Playwright routes (S4, S6); (e) NodeRacer-style causality recording as a diagnostic method only, with Node's Experimental/discouraged status (S5).
3. State the search policy plainly: uniform random choice among pending tasks; no enumeration, no bound, no schedule shrinking (S1). Use NodeCB bounds (<= 4 events, one resource, including DB/FS) to size workloads (L1).
4. Replay bundle: seed + path, printed `schedulerFor` block, the `report()` of the original run, fake-timer configuration (which APIs are faked), and for browser seams the release order the harness chose plus recorded responses (S1, S2, S6; Adamsen notes p.9).
5. Use `waitNext`/`waitIdle`; do not write `waitOne`/`waitAll` (deprecated since v4.2.0).
6. Common-mistakes entries: see next section.
7. `race-detection-campaigns`: one short boundary paragraph per S7, no new reference file.
8. Pin choice: cite fast-check `cd9c1884` for scheduler facts; note `stateful-property-testing` uses `5ec2e3ac`.

## Common mistakes (Wrong / Right / Why), with evidence

- **Wrong:** "fast-check explored the interleavings." **Right:** report sampled orders among wrapped promises, count of runs, and that schedules are not enumerated or shrunk. **Why:** `nextInt(0, scheduledTasks.length - 1)` and "Not supported yet" shrink (`SchedulerArbitrary.ts:13-20, 32-40`).
- **Wrong:** wrap the API with `scheduleFunction` and assume the server sees calls in varied order. **Right:** schedule the arrival too (mocked-server recipe). **Why:** "the mocked-server will always receive the calls in the same order as they were made" (`race-conditions.md:214`).
- **Wrong:** `await s.waitIdle()` and assume `fetch` or emitter work finished. **Right:** route those through the scheduler or wait on them explicitly with `waitFor`, and record what stayed uncontrolled. **Why:** `waitIdle` "Cannot await tasks triggered by uncontrolled sources like `fetch` or external event emitters" (`race-conditions.md:27`).
- **Wrong:** replay with the `schedulerFor` block alone and call it reproduced. **Right:** compare the replayed `report()` with the original. **Why:** it "will neither check that all the referred promises have been scheduled nor that they resolved with the same status and value" (`scheduler.ts:54-57`).
- **Wrong:** "`node:test` mock timers plus fast-check cover timer races." **Right:** mock timers are virtual time; the fast-check timer recipe needs a timer count and next-timer step that `MockTimers` does not document. **Why:** `MockTimers` methods are `enable`, `reset`, `tick`, `runAll`, `setTime` (`test.md:2915-3411`); recipe uses `jest.getTimerCount`/`advanceTimersToNextTimer` (`race-conditions.md:285, 291`).
- **Wrong:** "under `act`, React update interleavings were tested." **Right:** say each `act` flushes its queued updates together; orderings inside one flush are not searched. **Why:** updates "are added to an internal act queue, which are then flushed together" (`act.md:53`). (Limit is inference.)
- **Wrong:** add random delays or `delay()` and call it schedule search. **Right:** use ordered choices at a seam; keep delays as perturbation without replay. **Why:** implicit MSW `delay()` is random and negated in Node (`delay.md:28, 44`); unguided postponement produced HB-violating runs in 64.1% of runs and more than half of failures were infeasible (NodeRacer notes p.8).
- **Wrong:** reorder any two callbacks and report a race. **Right:** keep orders that recorded causality forbids out of the search, and triage failures that needed a forbidden order as false alarms. **Why:** NodeRacer notes p.5, p.8-9 (objection.js random-timeout false alarm).
- **Wrong:** use async_hooks to postpone callbacks or as a stable API. **Right:** use it only to record causality, state it is Experimental and discouraged, and postpone at harness-owned seams. **Why:** `async_hooks.md:5-18, 205-208`.
- **Wrong:** route browser responses with `page.route` on a site with a service worker and assume all requests were held. **Right:** set `serviceWorkers: 'block'` and record that the worker's behavior was removed. **Why:** `class-page.md:3758-3760`.
- **Wrong:** run ThreadSanitizer-style race detection on single-threaded JS. **Right:** route event ordering to `schedule-exploration`; memory races only with SharedArrayBuffer across agents, no verified detector. **Why:** ECMA-262 `spec.html:12142-12152, 53249-53263`.
- **Wrong:** search only in-memory state. **Right:** model DB and file state as the racing resource (findOne then save). **Why:** Wang notes p.4-9; Davis notes p.4-6.

## Sources inventory entries (for `references/sources.yaml`)

```yaml
  - name: "fast-check race conditions guide"
    url: "https://raw.githubusercontent.com/dubzzz/fast-check/cd9c1884e8a39fe945600fbcda1ec92d518feaa0/website/docs/advanced/race-conditions.md"
    type: official-documentation
    accessed: "2026-11-09"
    sections_used:
      - "The scheduler instance (lines 19-45; deprecations lines 31-35); schedule; scheduleFunction; scheduleSequence; Scheduling a call to a mocked server; Wrapping calls automatically using act; Scheduling native timers; Model based testing and race conditions"
  - name: "fast-check scheduler source"
    url: "https://raw.githubusercontent.com/dubzzz/fast-check/cd9c1884e8a39fe945600fbcda1ec92d518feaa0/packages/fast-check/src/arbitrary/_internals/SchedulerArbitrary.ts"
    type: official-source
    accessed: "2026-11-09"
    sections_used:
      - "buildNextTaskIndex lines 13-20; shrink lines 32-40"
  - name: "fast-check schedulerFor and SchedulerImplem"
    url: "https://raw.githubusercontent.com/dubzzz/fast-check/cd9c1884e8a39fe945600fbcda1ec92d518feaa0/packages/fast-check/src/arbitrary/scheduler.ts"
    type: official-source
    accessed: "2026-11-09"
    sections_used:
      - "schedulerFor JSDoc lines 30-88; SchedulerImplem.ts lines 12, 54-58, 219-231, 268-272, 407-429; BuildSchedulerFor.ts lines 5-21; ScheduledCommand.ts lines 16-58"
  - name: "Jest object API (fake timers)"
    url: "https://raw.githubusercontent.com/jestjs/jest/72614448ecb9d16c58d6474b3091247c14a5c090/docs/JestObjectAPI.md"
    type: official-documentation
    accessed: "2026-11-09"
    sections_used:
      - "jest.useFakeTimers (lines 900-940); advanceTimersToNextTimer (1086); getTimerCount (1118)"
  - name: "Vitest vi API (fake timers)"
    url: "https://raw.githubusercontent.com/vitest-dev/vitest/3a76b87324ecb8d25509cd009aa87fbe56819c39/docs/api/vi.md"
    type: official-documentation
    accessed: "2026-11-09"
    sections_used:
      - "vi.useFakeTimers (1211-1240); setTimerTickMode; advanceTimersToNextTimer (1002); getTimerCount (1058)"
  - name: "Node.js v26.13.0 test runner MockTimers"
    url: "https://raw.githubusercontent.com/nodejs/node/v26.13.0/doc/api/test.md"
    type: official-documentation
    accessed: "2026-11-09"
    sections_used:
      - "Timers (1036-1050); Class MockTimers (2894-3420)"
  - name: "Node.js v26.13.0 async_hooks"
    url: "https://raw.githubusercontent.com/nodejs/node/v26.13.0/doc/api/async_hooks.md"
    type: official-documentation
    accessed: "2026-11-09"
    sections_used:
      - "Stability banner (5-18); Terminology (35-45); createHook (147-208); init/type/triggerAsyncId/resource (308-438); before/after/destroy/promiseResolve (589-660); executionAsyncId/triggerAsyncId (756-832); Promise execution tracking (847-946)"
  - name: "Node.js v26.13.0 asynchronous context tracking"
    url: "https://raw.githubusercontent.com/nodejs/node/v26.13.0/doc/api/async_context.md"
    type: official-documentation
    accessed: "2026-11-09"
    sections_used:
      - "Stability (5); per-method Experimental markers (218, 258, 358, 395, 533); Troubleshooting: Context loss (511-525)"
  - name: "Node.js v26.13.0 v8 promiseHooks"
    url: "https://raw.githubusercontent.com/nodejs/node/v26.13.0/doc/api/v8.md"
    type: official-documentation
    accessed: "2026-11-09"
    sections_used:
      - "Promise hooks (944-1180)"
  - name: "Node.js v26.13.0 worker_threads"
    url: "https://raw.githubusercontent.com/nodejs/node/v26.13.0/doc/api/worker_threads.md"
    type: official-documentation
    accessed: "2026-11-09"
    sections_used:
      - "Introduction and stability (1-36); Class Worker (1474)"
  - name: "React act reference"
    url: "https://raw.githubusercontent.com/reactjs/react.dev/7594a2b008489121bdf25f97320d11ac0422510e/src/content/reference/react/act.md"
    type: official-documentation
    accessed: "2026-11-09"
    sections_used:
      - "await act(async actFn) (28-57); Troubleshooting IS_REACT_ACT_ENVIRONMENT (154-178)"
  - name: "MSW response timing and delay"
    url: "https://raw.githubusercontent.com/mswjs/mswjs.io/bda552ebaadde6d75870b4d07de734f9de35fd89/src/content/api/delay.md"
    type: official-documentation
    accessed: "2026-11-09"
    sections_used:
      - "Implicit delay; Explicit delay; Delay modes (infinite); also docs/http/mocking-responses/response-timing.md lines 13-90"
  - name: "Playwright Page and Route API"
    url: "https://raw.githubusercontent.com/microsoft/playwright/95e5dca31981bcd0970165853fcc713269d2433a/docs/src/api/class-page.md"
    type: official-documentation
    accessed: "2026-11-09"
    sections_used:
      - "Page.addInitScript (566-620); Page.route (3746-3898); class-route.md continue (36), fallback (155), fetch (442), fulfill (568); params.md navigation-wait-until (1-9)"
  - name: "ECMA-262 (agents, jobs, memory model)"
    url: "https://raw.githubusercontent.com/tc39/ecma262/828d35d00f8584c4a0fbcac7742b57c7b959c3f3/spec.html"
    type: specification
    accessed: "2026-11-09"
    sections_used:
      - "Execution contexts (line 11883); Jobs and host operations (12142-12152); Agents (12330-12337); Memory model (52687, 53249-53263)"
  - name: "NodeRacer (Endo and Moller, ICST 2020)"
    url: "https://doi.org/10.1109/ICST46399.2020.00022"
    type: research-paper
    accessed: "2026-11-09"
    sections_used:
      - "paper-reader notes pp.2-6, 8-10 (C:/Users/Q/code/papers/Endo_2020_NodeRacerEventRaceDetectionNodejs/notes.md)"
```
Davis 2017, Wang 2017, Raychev 2013 and Adamsen 2017 entries should take their DOI/URL from each notes file's frontmatter; I did not copy those here.

## Unverified (explicit)

- Nothing above was executed. Every recipe composition (Vitest timer port, MSW resolver awaiting a scheduled promise, Playwright held routes released in order, `waitUntil: 'commit'` plus held scripts, init-script wrappers) is an inference from documented APIs.
- Whether any other file in fast-check implements a non-random scheduler (only the five scheduler files were read).
- Behavior of fast-check scheduler at the `5ec2e3ac` pin used by `stateful-property-testing`.
- `@sinonjs/fake-timers` direct use with `node:test`: not read.
- Whether MSW browser-mode resolvers run in the page context, where a fast-check scheduler instance would be reachable: not read.
- Playwright WebSocket routing (`routeWebSocket` or similar): not checked.
- React production scheduling versus the `act` queue: no primary source read beyond `act.md`.
- `v8.promiseHooks` stability: no marker found; I did not check the source or changelog to confirm its status.
- NodeRacer tool URL (brics.dk/noderacer) and EventRaceCommander/EventRacer artifact availability: not checked.
- Detector absence for SharedArrayBuffer races: bounded search only (five GitHub queries, one web search).
- Papers in L2: not read.

# JavaScript event loop and browser async ordering

Within one agent (a Node process's main thread, one worker, one page) "Only one Job may be actively undergoing evaluation at any point in time", so the choices to search are the orders in which callbacks, promise continuations, timers, responses and user events run, not preemption points inside them ([ECMA-262, Jobs](https://raw.githubusercontent.com/tc39/ecma262/828d35d00f8584c4a0fbcac7742b57c7b959c3f3/spec.html)). In 57 real Node bugs the racing resource was a shared variable in 54%, a database in 26% and a file in 14% of cases ([Wang 2017, p.2, p.7](https://doi.org/10.1109/ASE.2017.8115663)).

Nothing on this page was executed for this pack. Recipes combining two documented APIs are marked unexecuted.

## Control boundary of the fast-check scheduler

The maintained controller verified for this pack is fast-check's scheduler (docs and source pinned at fast-check 4.10.2). It orders only the promises routed through it ([race conditions guide](https://raw.githubusercontent.com/dubzzz/fast-check/c77afa8277a67250d798c52e61343b8ed5fd268b/website/docs/advanced/race-conditions.md)):

- `s.schedule(p, label?)` returns a promise that "will resolve when the scheduler decides to resolve it"; continuations on the original promise are "not impacted by the scheduler".
- `s.scheduleFunction(fn)` is "only postponing the resolution of the function. The call to the function itself is started immediately".
- While a `scheduleSequence` item runs, no other scheduled task is released, so sequence items must not wait on other scheduled tasks.
- Wait with `waitNext(n)`, `waitIdle()` or `waitFor(p)`; `waitOne`, `waitAll` and `count()` are "deprecated since v4.2.0". `waitIdle` "Cannot await tasks triggered by uncontrolled sources like `fetch` or external event emitters", and work released by `waitFor` "might make replay of failures harder".
- `scheduledModelRun` runs commands through the scheduler; "Neither `check` nor `run` should rely on the completion of other scheduled tasks". Use `stateful-property-testing` for the command model.

Real timers, I/O completions, `fetch`, event emitters and library-internal queues stay outside the search unless the harness routes them through `s.schedule`; record each one that stayed outside. For a mocked server, `scheduleFunction` alone means "the mocked-server will always receive the calls in the same order as they were made"; the guide's recipe also schedules arrival with `s.schedule(Promise.resolve('Server received the call')).then(() => f(...args))`.

## Search policy and replay

Each step picks `nextInt(0, scheduledTasks.length - 1)`, a uniform random choice among pending tasks, and schedule shrinking is "Not supported yet" ([SchedulerArbitrary.ts](https://raw.githubusercontent.com/dubzzz/fast-check/c77afa8277a67250d798c52e61343b8ed5fd268b/packages/fast-check/src/arbitrary/_internals/SchedulerArbitrary.ts)). Report the search as sampled orders with a run count: no enumeration, bound, depth or reduced schedule. A pass says nothing about orders that were not sampled.

Keep the property seed and path, the printed `schedulerFor` block and the original run's `report()`, which lists tasks "in the order they get executed by the scheduler" ([race conditions guide](https://raw.githubusercontent.com/dubzzz/fast-check/c77afa8277a67250d798c52e61343b8ed5fd268b/website/docs/advanced/race-conditions.md)). `schedulerFor` replays order only: it "will neither check that all the referred promises have been scheduled nor that they resolved with the same status and value", so compare the replayed `report()` with the original before calling the failure reproduced ([scheduler.ts](https://raw.githubusercontent.com/dubzzz/fast-check/c77afa8277a67250d798c52e61343b8ed5fd268b/packages/fast-check/src/arbitrary/scheduler.ts)). Keep the fake-timer configuration with the bundle.

## Timers

Native timers "are ordered" and need special handling; the guide's only recipe is for Jest: a custom `act` schedules one "advance timers" task whenever `jest.getTimerCount()` is non-zero and calls `jest.advanceTimersToNextTimer()` ([race conditions guide, Scheduling native timers](https://raw.githubusercontent.com/dubzzz/fast-check/c77afa8277a67250d798c52e61343b8ed5fd268b/website/docs/advanced/race-conditions.md)). Jest's fake timers also replace `queueMicrotask()` and, in Node, `process.nextTick()`; record the faked APIs and any `doNotFake` list ([Jest fake timers](https://raw.githubusercontent.com/jestjs/jest/72614448ecb9d16c58d6474b3091247c14a5c090/docs/JestObjectAPI.md)).

- Vitest documents `vi.getTimerCount()` and `vi.advanceTimersToNextTimer()`, and `vi.useFakeTimers()` "does not automatically mock `process.nextTick` and `queueMicrotask`" ([Vitest `vi`](https://raw.githubusercontent.com/vitest-dev/vitest/3a76b87324ecb8d25509cd009aa87fbe56819c39/docs/api/vi.md)). Porting the Jest recipe to these two methods is unexecuted and not documented by fast-check.
- `node:test` `MockTimers` documents `enable`, `reset`, `tick`, `runAll` and `setTime`, with no pending-timer count or next-timer step, so the recipe does not port as written ([Node v26.13.0 MockTimers](https://raw.githubusercontent.com/nodejs/node/v26.13.0/doc/api/test.md)).

Fake time makes a timer firing one more scheduled task chosen at random among pending tasks; it is not timer-order enumeration.

## React

`fc.scheduler({ act })` wraps every released task, because "when testing React applications, one cannot perform updates of states outside of `act`" ([race conditions guide](https://raw.githubusercontent.com/dubzzz/fast-check/c77afa8277a67250d798c52e61343b8ed5fd268b/website/docs/advanced/race-conditions.md)). Use async `act`; the sync form "doesn't work in all cases" ([React `act`](https://raw.githubusercontent.com/reactjs/react.dev/7594a2b008489121bdf25f97320d11ac0422510e/src/content/reference/react/act.md)). Updates inside one `act` "are added to an internal act queue, which are then flushed together" (same source), so report one schedule step per flush: orderings inside a flush and React's production scheduling are not searched (inference from that sentence).

## Response order

MSW `delay()` is timing, not an ordered choice: implicit delay is random and "when testing in Node.js, the implicit delay is negated"; `delay('infinite')` makes a response "pend forever", which suits recording operations that never settle ([MSW `delay`](https://raw.githubusercontent.com/mswjs/mswjs.io/bda552ebaadde6d75870b4d07de734f9de35fd89/src/content/api/delay.md)). Unexecuted composition: an MSW resolver awaits a promise registered with `s.schedule(...)` before returning, which puts response order under the scheduler.

In a real browser, a Playwright route makes a matching request "stall unless it's continued, fulfilled or aborted" ([Playwright `Page`](https://raw.githubusercontent.com/microsoft/playwright/95e5dca31981bcd0970165853fcc713269d2433a/docs/src/api/class-page.md)). Unexecuted compositions:

- Hold two routes on harness promises and release `route.continue()`/`route.fulfill()` in a chosen order; `route.fetch()` "Performs the request and fetches result without fulfilling it", so real server responses can be held and released in order ([Playwright `Route`](https://raw.githubusercontent.com/microsoft/playwright/95e5dca31981bcd0970165853fcc713269d2433a/docs/src/api/class-route.md)).
- Act before scripts load: `waitUntil: 'commit'` returns "when network response is received and the document started loading" ([navigation wait](https://raw.githubusercontent.com/microsoft/playwright/95e5dca31981bcd0970165853fcc713269d2433a/docs/src/api/params.md)); hold script requests while the test clicks or types.
- `addInitScript` runs "before any of its scripts were run", so it can wrap `setTimeout`, `fetch` or `XMLHttpRequest`; it controls only what it wraps, and the evaluation order of multiple init scripts "is not defined" ([Playwright `Page`](https://raw.githubusercontent.com/microsoft/playwright/95e5dca31981bcd0970165853fcc713269d2433a/docs/src/api/class-page.md)).

Record the limits: `page.route` "will not intercept requests intercepted by Service Worker" (block service workers and report that their behavior was removed), it misses a popup's first request, redirects call the handler only for the first URL, and "Enabling routing disables http cache" (same source). The harness chooses the release order, so save that order and the recorded responses; a Playwright trace alone does not encode the choice.

## Methods from the literature

The research tools are not runnable routes. NodeRacer's README names Node LTS 10.16.3 and its last commit is 2022-12-15 ([noderacer](https://github.com/andreendo/noderacer/tree/2317c673490d3c721abdd91ee93b302c6720a235)); Node.fz modifies the libuv of Node v0.12.7 ([Davis 2017, p.10](https://doi.org/10.1145/3064176.3064188)) and its last commit is 2019-07-07 ([NodeFz](https://github.com/SBULeeLab/NodeFz/tree/1ce111e353f423e99b593ca1dfa8643029ae8e37)); EventRacer needs an instrumented WebKit ([Raychev 2013, p.2](https://doi.org/10.1145/2509136.2509538)) and its repository was last pushed 2015-09-21 ([EventRacer](https://github.com/eth-sri/EventRacer)). EventRaceCommander's repository state was not checked. Apply their methods at the seams above ([Endo 2020](https://doi.org/10.1109/ICST46399.2020.00022), [Adamsen 2017](https://doi.org/10.1109/icse.2017.34)):

- **Causality before perturbation.** NodeRacer records one run, infers happens-before over callbacks, and postpones a ready callback only when another ready callback exists, at most once per run, also postponing callbacks whose predecessors have not run (Endo 2020, p.5). Its oracle is an observable failure: crash, hang or test failure (p.2). Without the graph, 64.1% of runs on average violated happens-before and more than half of failures involved a violation (p.8). Triage a failure that needed a forbidden order as a false alarm; tests with random timeouts break the inferred order (p.9).
- **One-postponement diagnosis.** Postpone exactly one callback per run, a different one each run; a run that reproduces the failure names that callback (Endo 2020, p.6).
- **Legal orders only.** Node.fz made only scheduling decisions the Node docs allow and kept a completion callback after its task, libuv timer order and EventEmitter registration order, so races that depend on those orders were not explored (Davis 2017, pp.9-11). A test asserting timer precision can fail under perturbation without an event race (pp.12-13). The paper describes no replay; reproduction was a rate over reruns (pp.11-13).
- **Workload size.** 93% of the 57 bugs needed an order among at most 4 events, 95% one process and 86% one racing resource (Wang 2017, pp.7-8); an atomicity example is two requests interleaving `findOne` and `save` on one MongoDB record (p.5). Start with two to four concurrent operations on one resource and include database and file state, not only memory.
- **Where to place seams first.** NodeAV treats two causally ordered events touching the same resource as a pair meant to be atomic, and predicts a violation when a third, causally unordered event touches that resource in a read-write-read, write-write-read, write-read-write or read-write-write pattern ([Chang 2019, pp.6-7](https://doi.org/10.1109/ICSE.2019.00073)). It predicts from one trace without controlling schedules, and of 12 reports 3 were harmful, 8 benign and 1 a false positive where the third event stopped the second from running (p.9); the paper gives no tool artifact. This pack's guidance, not the paper's: treat such triples as candidates and force the ordered pair with the third event between them at a controlled seam to confirm.
- **Browser assumptions to steer toward.** EventRaceCommander names two developer expectations: the user acts only after the page loads, and Ajax responses arrive before further user actions (Adamsen 2017, p.3). It instrumented pages through a proxy, wrapping `setTimeout` and `XMLHttpRequest.prototype.send`, with its controller loaded before any application code (p.7). Postponing one event can require postponing others, such as a script's load event after its execution, and user-event order is preserved (p.4). Whether an order is harmful was left to the user (p.4). Replay relied on recorded server responses and failed where Ajax URLs depended on input, random numbers or timestamps (p.9).

## Recording causality on current Node

`async_hooks.createHook` is "Stability: 1 - Experimental. Please migrate away from this API, if you can" ([Node v26.13.0 async_hooks](https://raw.githubusercontent.com/nodejs/node/v26.13.0/doc/api/async_hooks.md)). Use it only to see which callbacks were ready together in a failing test:

- `init` gives `triggerAsyncId`, which "shows _why_ a resource was created"; `before`, `after` and `promiseResolve` mark callback runs and promise resolution.
- Hooks "_must not_ be async functions that return promises", and the docs describe no way to delay a callback; inference: hooks record order but cannot postpone it, so postponement stays at harness-owned seams.
- Resource `type` values "can change in any Node.js release"; the resource object is not a safe `WeakMap` key; each worker thread has "an independent `async_hooks` interface"; promise tracking "can cause a significant performance overhead", so instrumented timing differs from uninstrumented runs.
- Hooks do not say which function is the callback; NodeRacer added a function entry/exit tracer for that (Endo 2020, p.4).

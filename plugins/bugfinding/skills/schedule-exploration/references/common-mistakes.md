# Common mistakes

Each entry is **Wrong** first, then **Right**, then a one-line **Why**.

## Calling stress runs or fake time schedule enumeration

**Wrong:** "We ran the Go test 10,000 times under `synctest`, so the interleavings are covered."

**Right:** Name the choices a controller actually made; report `synctest` as fake time and quiescence only.

**Why:** synctest documents bubbles, a fake clock and durable blocking, and states "Operations not in the above list are not durably blocking."; it documents no schedule enumeration ([synctest, Time, Blocking](https://pkg.go.dev/testing/synctest@go1.27.3)).

## Trusting a top-level controller over unchanged dependencies

**Wrong:** Wrap the test in `loom::model` while the code under test still uses a dependency built on `std::sync`.

**Right:** Trace the real controlled path and record each dependency whose synchronization stays outside the model.

**Why:** code without replacement types "is invisible to loom", and "certain executions that are possible in the real world won't be modeled" ([Loom, Intrusive Implementation](https://docs.rs/loom/0.7.2/loom/)).

## Treating a Loom alarm as a hardware-valid SeqCst failure

**Wrong:** "Loom failed on a `SeqCst` load, so the code is broken on real hardware."

**Right:** Adjudicate the alarm against Loom's weakened `SeqCst` modeling, and keep its missed load-buffering executions in the report too.

**Why:** `SeqCst` accesses are "regarded as `AcqRel`", causing "false alarms (not complete)", and a bug can exist "even if Loom says there is no bug (not sound)" ([Loom 0.7.2 README, Unsupported features](https://raw.githubusercontent.com/tokio-rs/loom/a7033ee06a97c52eb2f8131c095fbea6c6eecba3/README.md)).

## Setting a checkpoint file on the default Loom dependency

**Wrong:** Set `LOOM_CHECKPOINT_FILE=my_test.json` with `loom` declared without features and expect a saved path.

**Right:** Enable the selected release's `checkpoint` feature and keep the configuration that produced the checkpoint.

**Why:** without the feature, checkpoint load and store call ``panic!("not compiled with `checkpoint` feature")`` ([Loom 0.7.2 `src/model.rs`](https://raw.githubusercontent.com/tokio-rs/loom/a7033ee06a97c52eb2f8131c095fbea6c6eecba3/src/model.rs)).

## Expecting `max_time` to stop a stuck Shuttle iteration

**Wrong:** Rely on `Config::max_time` to end an iteration that spins forever.

**Right:** Bound iterations with `MaxSteps` and keep a separate owned outer limit for the whole run.

**Why:** the time limit "will not abort a currently running test iteration; the limit is only checked between iterations" ([Shuttle `Config`](https://docs.rs/shuttle/0.9.10/shuttle/struct.Config.html)).

## Running Coyote `TestingEngine` on unchanged binaries

**Wrong:** Call `TestingEngine.Create(config, test).Run()` from xUnit against assemblies that were never rewritten, and ignore `TryEmitTraces` output.

**Right:** Rewrite the selected binaries first, assert `TestReport`, and iterate `TryEmitTraces` to write the trace files.

**Why:** "you must first use `coyote rewrite`", and "`TryEmitTraces` is an iterator method" ([Coyote unit-test integration](https://raw.githubusercontent.com/microsoft/coyote/2202e75a861f4e8a63149366c2e41ea21d73ae54/docs/how-to/unit-testing.md)).

## Claiming Coyote systematic testing validated wall-time or weak-memory behavior

**Wrong:** "Coyote passed, so the timeout race and the lock-free reordering are fine."

**Right:** State that finite waits were explored as infinite and that every schedule was sequentially consistent.

**Why:** a finite non-zero timeout "is explored as if it was infinite", and "Every schedule that Coyote explores is sequentially consistent" ([Coyote, How timeouts/memory ordering are modeled](https://raw.githubusercontent.com/microsoft/coyote/2202e75a861f4e8a63149366c2e41ea21d73ae54/docs/concepts/binary-rewriting.md)).

## Keeping only a seed, or shrinking only the source

**Wrong:** Save the random seed and the shrunk test source; drop the initial state and recorded choices.

**Right:** Keep initial state, workload and controlled choices together, and replay them under the same controller.

**Why:** CHESS captures choices to "later reproduce a chosen concurrent execution" but "shifted the onus of generating deterministic inputs to the user" ([CHESS, §§3, 3.1](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/osdi2008-CHESS.pdf)).

## Calling fast-check scheduler runs exhaustive

**Wrong:** "fast-check explored the interleavings of these promises."

**Right:** Report sampled orders among the promises routed through the scheduler, the run count, and that schedules were neither enumerated nor shrunk.

**Why:** each step picks `nextInt(0, scheduledTasks.length - 1)` among pending tasks, and schedule shrinking is "Not supported yet" ([SchedulerArbitrary.ts](https://raw.githubusercontent.com/dubzzz/fast-check/c77afa8277a67250d798c52e61343b8ed5fd268b/packages/fast-check/src/arbitrary/_internals/SchedulerArbitrary.ts)).

## Assuming `waitIdle` covers `fetch` or emitters

**Wrong:** `await s.waitIdle()` and assert, assuming `fetch` and event-emitter work finished in a controlled order.

**Right:** Route those sources through `s.schedule`, or wait on them with `waitFor` and record them as uncontrolled.

**Why:** `waitIdle` "Cannot await tasks triggered by uncontrolled sources like `fetch` or external event emitters" ([fast-check race conditions guide](https://raw.githubusercontent.com/dubzzz/fast-check/c77afa8277a67250d798c52e61343b8ed5fd268b/website/docs/advanced/race-conditions.md)).

## Replaying a `schedulerFor` block alone

**Wrong:** Paste the printed `schedulerFor` block into a test, see it fail, and call the original failure reproduced.

**Right:** Compare the replayed `report()` with the original run's tasks, statuses and values.

**Why:** `schedulerFor` "will neither check that all the referred promises have been scheduled nor that they resolved with the same status and value" ([scheduler.ts](https://raw.githubusercontent.com/dubzzz/fast-check/c77afa8277a67250d798c52e61343b8ed5fd268b/packages/fast-check/src/arbitrary/scheduler.ts)).

## Porting the timer recipe to `node:test` mock timers

**Wrong:** "`node:test` mock timers plus fast-check cover the timer races."

**Right:** Treat mock timers as virtual time; the documented recipe needs a pending-timer count and a next-timer step, which only the Jest recipe shows.

**Why:** `MockTimers` documents `enable`, `reset`, `tick`, `runAll` and `setTime` ([Node v26.13.0 MockTimers](https://raw.githubusercontent.com/nodejs/node/v26.13.0/doc/api/test.md)); the recipe calls `jest.getTimerCount()` and `jest.advanceTimersToNextTimer()` ([fast-check race conditions guide](https://raw.githubusercontent.com/dubzzz/fast-check/c77afa8277a67250d798c52e61343b8ed5fd268b/website/docs/advanced/race-conditions.md)).

## Calling `act`-wrapped runs a search of React update orders

**Wrong:** "Under `act`, the React update interleavings were tested."

**Right:** Report one schedule step per `act` flush; orderings inside one flush were not searched.

**Why:** updates inside `act` "are added to an internal act queue, which are then flushed together" ([React `act`](https://raw.githubusercontent.com/reactjs/react.dev/7594a2b008489121bdf25f97320d11ac0422510e/src/content/reference/react/act.md)).

## Perturbing callbacks without recorded causality

**Wrong:** Add random delays to any callback and report every resulting failure as an event race.

**Right:** Perturb only orders the recorded causality allows, and triage failures that needed a forbidden order as false alarms.

**Why:** unguided postponement violated happens-before in 64.1% of runs on average, and more than half of its failures involved a violation ([Endo 2020, p.8](https://doi.org/10.1109/ICST46399.2020.00022)).

## Holding browser requests on a site with a service worker

**Wrong:** Hold responses with `page.route` on a PWA and assume every request was held.

**Right:** Block service workers, and report that their behavior was removed from the test.

**Why:** `page.route` "will not intercept requests intercepted by Service Worker" ([Playwright `Page`](https://raw.githubusercontent.com/microsoft/playwright/95e5dca31981bcd0970165853fcc713269d2433a/docs/src/api/class-page.md)).

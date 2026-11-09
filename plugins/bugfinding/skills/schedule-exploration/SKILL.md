---
name: schedule-exploration
description: Guides controlled systematic or randomized schedule search with Loom, Shuttle, Coyote, the fast-check scheduler or existing target seams. Use when extending selected interleaving tests, finding logical concurrency failures including Node event-loop, promise, timer and browser or React async-ordering races, or preserving and reducing a replayable scheduling counterexample.
---

# Schedule exploration

Search scheduling choices around a real safety or progress assertion. Capturing a failing execution and exposing alternatives are separate capabilities; retain the scenario's initial state as well as its choices. CHESS captures choices to "later reproduce a chosen concurrent execution", treats exposing them to search as a second goal, and "shifted the onus of generating deterministic inputs to the user" ([CHESS, §§3, 3.1](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/osdi2008-CHESS.pdf)).

## Establish control before allocating search

Read the actual producer, enabled configuration and promised behavior. Identify which relevant tasks, synchronization, callbacks, randomness and external observations the controller can intercept. A wrapper around a test does not establish control of its dependencies: code without Loom's replacement types "is invisible to loom", and Coyote treats un-rewritten DLLs as "pass-through" with methods invoked atomically ([Loom, Intrusive Implementation](https://docs.rs/loom/0.7.2/loom/), [Coyote, Which DLLs to rewrite?](https://raw.githubusercontent.com/microsoft/coyote/2202e75a861f4e8a63149366c2e41ea21d73ae54/docs/concepts/binary-rewriting.md)).

Choose an existing fitting integration and a small meaningful workload. For a target already testing held validation/publication pairs, extend the supported choice space around a documented invariant; do not merely rerun that pair or replace it with sleeps. Inserted sleeps and yields "impede the coverage achieved with CHESS" because its fair scheduler deprioritizes a yielding thread ([CHESS, §§4.5, 5.2](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/osdi2008-CHESS.pdf)). Read [controlled boundaries](references/controlled-boundaries.md) for the worked design and evidence needed.

Use `stateful-property-testing` for dependent workloads, `linearizability-checking` or `transactional-history-testing` for their history oracles, and `race-detection-campaigns` for observed memory conflicts. This skill owns schedule choices and their execution model.

## Select and execute a supported lane

- For Rust replacement-type integrations, read [Rust controllers](references/rust-controllers.md): Loom permutations/checkpoints or Shuttle random/PCT/DFS and encoded replay. Confirm all relevant paths use controlled APIs ([Loom](https://docs.rs/loom/0.7.2/loom/), [Shuttle](https://docs.rs/shuttle/0.9.10/shuttle/)).
- For rewritten .NET task code, or deciding what Go fake time provides, read [.NET and Go boundaries](references/dotnet-and-go.md). Coyote needs rewritten binaries ("you must first use `coyote rewrite`"); synctest documents fake time and durable blocking, not schedule enumeration ([Coyote integration](https://raw.githubusercontent.com/microsoft/coyote/2202e75a861f4e8a63149366c2e41ea21d73ae54/docs/how-to/unit-testing.md), [synctest, Time and Blocking](https://pkg.go.dev/testing/synctest@go1.27.3)).
- For Node, browser or React async ordering, read [JavaScript event loop](references/javascript-event-loop.md): the fast-check scheduler orders only promises routed through it, picking uniformly at random among pending tasks with no schedule shrinking; timers, React `act`, held responses and literature methods are bounded there ([fast-check race conditions](https://raw.githubusercontent.com/dubzzz/fast-check/c77afa8277a67250d798c52e61343b8ed5fd268b/website/docs/advanced/race-conditions.md), [SchedulerArbitrary.ts](https://raw.githubusercontent.com/dubzzz/fast-check/c77afa8277a67250d798c52e61343b8ed5fd268b/packages/fast-check/src/arbitrary/_internals/SchedulerArbitrary.ts)).
- Record policy, actors, steps, preemptions, permutations/iterations, fairness and model omissions separately. A bounded pass is conditional on these choices; fewer interleavings through reduction require valid independence assumptions: CHESS merges executions that "only differ in the order of independent synchronizations operations" ([CHESS, §§4.3–4.4](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/osdi2008-CHESS.pdf)).

Use the actual selected version's limit semantics. Some limits are polled between iterations or checkpoint intervals; they cannot interrupt an arbitrary stuck iteration. Shuttle's `max_time` "is only checked between iterations"; Loom checks `max_permutations` and `max_duration` only when `i % self.checkpoint_interval == 0`. Keep an authorized outer resource envelope and report clipped/unsupported runs separately ([Loom 0.7.2 `Builder::check`](https://raw.githubusercontent.com/tokio-rs/loom/a7033ee06a97c52eb2f8131c095fbea6c6eecba3/src/model.rs), [Shuttle `Config::max_time`](https://docs.rs/shuttle/0.9.10/shuttle/struct.Config.html)).

## Preserve and reduce the execution

Save initial state/setup, workload, source/build/configuration, complete controlled choices, observer and witness. Replay the actual controller artifact; a workload seed does not reconstruct uncontrolled events. Shuttle replay is deterministic only if the test "contains no non-determinism other than that introduced by scheduling". Read [replay and reduction](references/replay-and-reduction.md) for workload-plus-trace handling ([CHESS, §§3.1–4.2](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/osdi2008-CHESS.pdf), [Shuttle replay](https://docs.rs/shuttle/0.9.10/shuttle/fn.replay.html)).

Use `failure-reduction` for minimizer mechanics and `evidence-based-triage` for attribution. Keep alternate failures, unknowns and unrepeatable observations visible. A model alarm must be adjudicated against its documented omissions; Loom documents weakened `SeqCst` accesses "causing Loom to generate false alarms (not complete)" and unexplored load buffering where a bug can exist "even if Loom says there is no bug (not sound)" ([Loom 0.7.2 README, Unsupported features](https://raw.githubusercontent.com/tokio-rs/loom/a7033ee06a97c52eb2f8131c095fbea6c6eecba3/README.md)).

## Completion

Return the tested guarantee and actual control boundary; search policy/bounds and completed scope; resource use; original/replayed/reduced artifact paths; witnessed violations and unresolved evidence. Preserve a no-finding result with its unsearched space. For shortcuts that invalidate these claims, read [common mistakes](references/common-mistakes.md). Invocation preserves existing execution and mutation authority.

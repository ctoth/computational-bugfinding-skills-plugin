---
name: schedule-exploration
description: Guides controlled systematic or randomized schedule search with Loom, Shuttle, Coyote or existing target seams. Use when extending selected interleaving tests, finding logical concurrency failures, or preserving and reducing a replayable scheduling counterexample.
---

# Schedule exploration

Search scheduling choices around a real safety or progress assertion. Capturing a failing execution and exposing alternatives are separate capabilities; retain the scenario's initial state as well as its choices ([CHESS, §§3–4](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/osdi2008-CHESS.pdf)).

## Establish control before allocating search

Read the actual producer, enabled configuration and promised behavior. Identify which relevant tasks, synchronization, callbacks, randomness and external observations the controller can intercept. A wrapper around a test does not establish control of its dependencies ([Loom integration](https://docs.rs/loom/0.7.2/loom/), [Coyote rewriting](https://microsoft.github.io/coyote/concepts/binary-rewriting/)).

Choose an existing fitting integration and a small meaningful workload. For a target already testing held validation/publication pairs, extend the supported choice space around a documented invariant; do not merely rerun that pair or replace it with sleeps. Read [controlled boundaries](references/controlled-boundaries.md) for the worked design and evidence needed ([CHESS, §§3.2, 4.4–4.5](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/osdi2008-CHESS.pdf)).

Use `stateful-property-testing` for dependent workloads, `linearizability-checking` or `transactional-history-testing` for their history oracles, and `race-detection-campaigns` for observed memory conflicts. This skill owns schedule choices and their execution model.

## Select and execute a supported lane

- For Rust replacement-type integrations, read [Rust controllers](references/rust-controllers.md): Loom permutations/checkpoints or Shuttle random/PCT/DFS and encoded replay. Confirm all relevant paths use controlled APIs ([Loom](https://docs.rs/loom/0.7.2/loom/), [Shuttle](https://docs.rs/shuttle/0.9.10/shuttle/)).
- For rewritten .NET task code, or deciding what Go fake time provides, read [.NET and Go boundaries](references/dotnet-and-go.md). Coyote needs rewritten binaries; synctest does not document schedule enumeration ([Coyote integration](https://microsoft.github.io/coyote/how-to/unit-testing/), [synctest](https://pkg.go.dev/testing/synctest)).
- Record policy, actors, steps, preemptions, permutations/iterations, fairness and model omissions separately. A bounded pass is conditional on these choices; fewer interleavings through reduction require valid independence assumptions ([CHESS, §§4.3–4.4](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/osdi2008-CHESS.pdf)).

Use the actual selected version's limit semantics. Some limits are polled between iterations or checkpoint intervals; they cannot interrupt an arbitrary stuck iteration. Keep an authorized outer resource envelope and report clipped/unsupported runs separately ([Loom loop](https://raw.githubusercontent.com/tokio-rs/loom/master/src/model.rs), [Shuttle limits](https://docs.rs/shuttle/0.9.10/shuttle/struct.Config.html)).

## Preserve and reduce the execution

Save initial state/setup, workload, source/build/configuration, complete controlled choices, observer and witness. Replay the actual controller artifact; a workload seed does not reconstruct uncontrolled events. Read [replay and reduction](references/replay-and-reduction.md) for workload-plus-trace handling ([CHESS, §§3.1–4.2](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/osdi2008-CHESS.pdf), [Shuttle replay](https://docs.rs/shuttle/0.9.10/shuttle/fn.replay.html)).

Use `failure-reduction` for minimizer mechanics and `evidence-based-triage` for attribution. Keep alternate failures, unknowns and unrepeatable observations visible. A model alarm must be adjudicated against its documented omissions; Loom explicitly documents both false alarms and missed executions ([Loom unsupported features](https://raw.githubusercontent.com/tokio-rs/loom/master/README.md)).

## Completion

Return the tested guarantee and actual control boundary; search policy/bounds and completed scope; resource use; original/replayed/reduced artifact paths; witnessed violations and unresolved evidence. Preserve a no-finding result with its unsearched space. For shortcuts that invalidate these claims, read [common mistakes](references/common-mistakes.md). Invocation preserves existing execution and mutation authority.

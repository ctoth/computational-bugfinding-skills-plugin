# Rust controllers

These conditional recipes assume an existing compatible test integration and authorized execution. Commands use POSIX environment syntax; use the invoking shell's equivalent. Check the selected release and preserve its dependency/build features.

## Loom

Use Loom synchronization/thread types throughout the tested path, with the existing conditional compilation owner. Other nondeterminism needs a fitting controlled seam. For a configured test: `RUSTFLAGS="--cfg loom" cargo test --test loom_my_struct --release`. A preemption bound selects a smaller space; it does not make an arbitrary scenario complete ([integration and running](https://docs.rs/loom/0.7.2/loom/)).

Record Builder's thread, branch, permutation, duration and preemption settings independently. For checkpoint replay enable the selected dependency's `checkpoint` feature: the inspected source otherwise panics on checkpoint load/store. Duration/permutation checks occur at checkpoint intervals, not as immediate interruption. The inspected crate is 0.7.2, Rust 1.73 minimum, MIT; recheck the chosen release ([Builder](https://docs.rs/loom/latest/loom/model/struct.Builder.html), [actual loop/checkpoint code](https://raw.githubusercontent.com/tokio-rs/loom/master/src/model.rs), [package/features](https://raw.githubusercontent.com/tokio-rs/loom/master/Cargo.toml)).

Retain `LOOM_CHECKPOINT_FILE` and matching configuration; use `LOOM_CHECKPOINT_INTERVAL=1` to isolate the failing permutation before enabling expensive location/log tracing. A checkpoint is not a substitute for the same starting scenario. Fairness-sensitive spins need the documented yielding semantics, not arbitrary sleeps ([debugging and yielding](https://docs.rs/loom/0.7.2/loom/)).

Read the selected memory model before attribution: the README documents weakened SeqCst accesses that can produce false alarms and load-buffering executions that can be missed. A green bounded run cannot exclude those omitted behaviors ([unsupported features](https://raw.githubusercontent.com/tokio-rs/loom/master/README.md)).

## Shuttle

Use its synchronization/thread/random APIs throughout the chosen path. An existing feature-switched integration can run `cargo test --features shuttle`; wrapping unchanged uncontrolled dependencies is insufficient. Official README identifies Apache-2.0; select a consistent release/API set ([crate integration](https://docs.rs/shuttle/0.9.10/shuttle/), [repository setup/license](https://raw.githubusercontent.com/awslabs/shuttle/main/README.md)).

Choose policy intentionally: `check_random(case, iterations)`; `check_pct(case, iterations, depth)`; or `check_dfs(case, Some(max_iterations))`. DFS's optional argument is an iteration count, not depth. PCT parameters are not a general confidence guarantee ([random integration](https://docs.rs/shuttle/0.9.10/shuttle/), [PCT API](https://docs.rs/shuttle/0.9.10/shuttle/fn.check_pct.html), [DFS API](https://docs.rs/shuttle/0.9.10/shuttle/fn.check_dfs.html)).

Configure per-iteration `MaxSteps` separately from total `max_time`: time is checked between iterations and does not abort a running one. `FailAfter` reports a step-bound crossing; `ContinueAfter` starts another iteration. Neither outcome alone proves the target violated a progress guarantee. Keep relevant atomic/lazy-static warnings; hiding them does not improve the model ([Config](https://docs.rs/shuttle/0.9.10/shuttle/struct.Config.html), [steps](https://docs.rs/shuttle/0.9.10/shuttle/enum.MaxSteps.html)).

Preserve the emitted encoded schedule and replay with `shuttle::replay(case, encoded_schedule)`. Deterministic replay requires the case's other nondeterminism to be absent/controlled; retain the workload and setup with the schedule ([replay contract](https://docs.rs/shuttle/0.9.10/shuttle/fn.replay.html)).

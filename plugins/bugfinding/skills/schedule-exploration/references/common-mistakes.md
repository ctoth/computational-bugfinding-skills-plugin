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

# Common mistakes

## Reading a failed unwinding assertion as the product defect

**Wrong:** Kani reports `Failed Checks: unwinding assertion loop 0`, and the run is filed as the buffer-index bug under investigation.

**Right:** Identify the actual failed property and raise the bound first. In the Kani tutorial the unwinding failure is "because this bound is not high enough"; only at unwind 11 does "the actual failure we're trying to find" appear ([Kani loop tutorial](https://raw.githubusercontent.com/model-checking/kani/94253e32fe7ead82c9f1ef842bd9ddc6fae7e8ca/docs/src/tutorial-loop-unwinding.md)).

**Why:** a completeness failure says the bound is too small; it says nothing yet about the product assertion.

## Assuming the expected answer, then counting the green assertion

**Wrong:** The harness assumes `x > 0` and `x < 0`, and the following safety assertion's `SUCCESS` is reported as verified.

**Right:** Establish satisfiable legal setup and check reach with `--cover assume`. The condition must be "actually satisfiable by some nondeterministic choice, otherwise the model checking step will pass vacuously" ([CBMC assumptions, Modeling with Assumptions and Coverage](https://raw.githubusercontent.com/diffblue/cbmc/826c1c739051aa1c2dd8846282e12691db1cee35/doc/cprover-manual/modeling-assumptions.md)).

**Why:** an empty search space makes every later assertion pass without a single execution reaching it.

## Adding `--partial-loops` to finish a loop and calling the path real

**Wrong:** Pass `--partial-loops` so a deep loop stops blocking a later assertion, then report the resulting counterexample as a real execution.

**Right:** Keep unwinding assertions on and investigate the bound. Partial-loop paths "may be spurious, that is, it may not exist in the original program" ([CBMC unwinding, Setting Separate Unwinding Limits](https://raw.githubusercontent.com/diffblue/cbmc/826c1c739051aa1c2dd8846282e12691db1cee35/doc/cprover-manual/cbmc-unwinding.md)).

**Why:** a spurious path is a false alarm; replay of it fails or switches to a different failure.

## Accepting missing Java methods as actual library behavior

**Wrong:** A JBMC trace passes through a library call whose body was never loaded, and its return value is treated as what the JVM would return.

**Right:** Inspect body/stub/model provenance. The frontend provides "a simple stub implementation for any function we don't have a bytecode implementation for" ([JBMC frontend, generate_function_body](https://raw.githubusercontent.com/diffblue/cbmc/826c1c739051aa1c2dd8846282e12691db1cee35/jbmc/src/jbmc/jbmc_parse_options.cpp)).

**Why:** a stub's return value is a model choice, so a red or green result through it may not exist on a real JVM.

## Reading a `SUCCESS` summary as every assertion having executed

**Wrong:** `VERIFICATION:- SUCCESSFUL` is reported as every assertion exercised.

**Right:** Inspect per-property status. A `SUCCESS` property "may hold _vacuously_", `UNREACHABLE` means no trace reaches the check, and `UNDETERMINED` means Kani "was not able to conclude whether the property holds or not" ([Kani verification results, Check results](https://raw.githubusercontent.com/model-checking/kani/94253e32fe7ead82c9f1ef842bd9ddc6fae7e8ca/docs/src/verification-results.md)).

**Why:** a green verdict can include unreachable checks, shown only as a count such as `0 of 786 failed (41 unreachable)`, and vacuous `SUCCESS` checks that are not marked at all.

## Declaring a UB witness disproved because playback did not crash

**Wrong:** Kani reports a failing pointer-validity check, playback produces no failing test, and the finding is closed.

**Right:** Check the supported playback category. Playback "does not generate unit tests for failing non-panic checks (e.g., UB checks)" because "checks would not trigger runtime errors during concrete playback" ([Kani concrete playback, Limitations](https://raw.githubusercontent.com/model-checking/kani/94253e32fe7ead82c9f1ef842bd9ddc6fae7e8ca/docs/src/reference/experimental/concrete-playback.md)). Keep the verifier witness and use another appropriate observer.

**Why:** an absent native crash is the documented behavior for this category, not evidence against the witness.

## Reading an old JSON success after killing the new verifier

**Wrong:** The verifier is killed at the time limit, `kani.json` shows a complete success, and that file is reported.

**Right:** Match run identity and completion. This version "never writes the `INCOMPLETE` marker", and the earlier file "can stay in place and look complete. Compare its `started_at` with the time of your run" ([Kani verification results, JSON output](https://raw.githubusercontent.com/model-checking/kani/94253e32fe7ead82c9f1ef842bd9ddc6fae7e8ca/docs/src/verification-results.md)).

**Why:** the reported success belongs to a different, earlier run.

## Calling an I/O-heavy replacement implementation "the verified target"

**Wrong:** Rewrite a file-reading parser into a pure copy, verify the copy, and report the service as verified.

**Right:** Select an actual supported pure component and state the narrower guarantee. "Kani doesn't model I/O, so if your code depends on behavior like reading/writing to a file, you won't be able to prove anything" ([Kani real-code guide, Where is it easier to start](https://raw.githubusercontent.com/model-checking/kani/94253e32fe7ead82c9f1ef842bd9ddc6fae7e8ca/docs/src/tutorial-real-code.md)).

**Why:** the copy is a different producer; its proof does not cover the code that ships.

# Counterexamples, replay and artifact identity

A solver trace is a candidate tied to its producer, domain and model. The original CBMC paper's trace view allows stepping "also backward, giving the user the ability to determine more easily the causes of the error" ([§3, p.171](https://www.kroening.com/papers/tacas2004.pdf)). Preserve concrete inputs, actual harness/source or bytecode, pre-state, assumptions, ABI/model libraries, tool/solver/compiler options and raw trace before reduction.

## Separate property failure from missing completeness

Inspect which check failed. An unwinding failure requires revisiting the declared bound; it is not interchangeable with an out-of-bounds or user-assertion counterexample. The Kani tutorial explicitly separates those stages ([loop example](https://raw.githubusercontent.com/model-checking/kani/94253e32fe7ead82c9f1ef842bd9ddc6fae7e8ca/docs/src/tutorial-loop-unwinding.md)). Retain model omissions and unfinished properties rather than presenting every red summary as the selected defect.

An accepted partial-loop path "may be spurious, that is, it may not exist in the original program". When `--unwinding-assertions` is also used and the trace "does not include a report of a violated unwinding assertion", the guide says that counterexample "is not impacted by insufficient loop unwinding" ([CBMC unwinding, Setting Separate Unwinding Limits](https://raw.githubusercontent.com/diffblue/cbmc/826c1c739051aa1c2dd8846282e12691db1cee35/doc/cprover-manual/cbmc-unwinding.md)). Reconstruct the concrete operation and required state; reject a replay that switches to a setup failure. Use the existing `failure-reduction` owner for dependent minimization and `evidence-based-triage` for attribution.

## Use actual Kani playback support

For a selected compatible harness, the documented print route avoids an implicit authored-source modification; with `print` "Kani will just print the unit test to stdout", while `inplace` "will automatically copy the unit test into your source code" ([playback, Usage](https://raw.githubusercontent.com/model-checking/kani/94253e32fe7ead82c9f1ef842bd9ddc6fae7e8ca/docs/src/reference/experimental/concrete-playback.md)):

```text
cargo kani --harness HARNESS -Z concrete-playback --concrete-playback=print
cargo kani playback -Z concrete-playback -- GENERATED_TEST_NAME
```

Place the emitted test "into the same module as your proof harness" through the task's editing mechanism. "Any extra compilation option used during verification must be used during playback", with the same Kani version. Playback generates tests "for assertions that failed during verification, as well as cover statements that are reachable", but not for failing non-panic checks such as UB checks, and it does not support "multiple assertion failures within the same harness" ([playback, Usage and Limitations](https://raw.githubusercontent.com/model-checking/kani/94253e32fe7ead82c9f1ef842bd9ddc6fae7e8ca/docs/src/reference/experimental/concrete-playback.md)). Preserve a verifier-only UB witness explicitly and investigate with an appropriate independent observer instead of fabricating a native crash or discarding the candidate.

## Reject stale or vacuous evidence

Kani's result document distinguishes success, unreachable and undetermined checks. Its JSON export format "is unstable and may change between releases", and "If a run is killed, the file from an earlier run can stay in place and look complete"; correlate `started_at`, actual invocation/configuration and process completion ([results and JSON output](https://raw.githubusercontent.com/model-checking/kani/94253e32fe7ead82c9f1ef842bd9ddc6fae7e8ca/docs/src/verification-results.md)). Do not erase the older evidence; identify which run each artifact belongs to.

Illustrative handoff: input domain length0-10; harness calls the real buffer helper; all required bounds complete; a concrete length/index violates the promised buffer assertion; native replay uses that same helper and setup. Contrast with an interrupted run, a contradictory-assumption pass or a missing Java-body stub. These are different evidence states, not alternative descriptions of one completed verification.

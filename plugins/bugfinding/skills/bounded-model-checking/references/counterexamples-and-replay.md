# Counterexamples, replay and artifact identity

A solver trace is a candidate tied to its producer, domain and model. The original CBMC paper's counterexample view allows inspecting earlier states because the failure line need not reveal the cause ([p.171](https://www.kroening.com/papers/tacas2004.pdf)). Preserve concrete inputs, actual harness/source or bytecode, pre-state, assumptions, ABI/model libraries, tool/solver/compiler options and raw trace before reduction.

## Separate property failure from missing completeness

Inspect which check failed. An unwinding failure requires revisiting the declared bound; it is not interchangeable with an out-of-bounds or user-assertion counterexample. The Kani tutorial explicitly separates those stages ([loop example](https://raw.githubusercontent.com/model-checking/kani/94253e32fe7ead82c9f1ef842bd9ddc6fae7e8ca/docs/src/tutorial-loop-unwinding.md)). Retain model omissions and unfinished properties rather than presenting every red summary as the selected defect.

An accepted partial-loop path may not exist in the program ([CBMC unwinding](https://raw.githubusercontent.com/diffblue/cbmc/826c1c739051aa1c2dd8846282e12691db1cee35/doc/cprover-manual/cbmc-unwinding.md)). Reconstruct the concrete operation and required state; reject a replay that switches to a setup failure. Use the existing `failure-reduction` owner for dependent minimization and `evidence-based-triage` for attribution.

## Use actual Kani playback support

For a selected compatible harness, the documented print route avoids an implicit authored-source modification:

```text
cargo kani --harness HARNESS -Z concrete-playback --concrete-playback=print
cargo kani playback -Z concrete-playback -- GENERATED_TEST_NAME
```

Place the emitted test in the actual harness module through the task's editing mechanism. Use the same Kani version and compilation options. Playback supports failed assertions/panics and reached cover cases, but not failing non-panic checks such as all UB reports; generated tests also have multiple-failure limitations ([playback](https://raw.githubusercontent.com/model-checking/kani/94253e32fe7ead82c9f1ef842bd9ddc6fae7e8ca/docs/src/reference/experimental/concrete-playback.md)). Preserve a verifier-only UB witness explicitly and investigate with an appropriate independent observer instead of fabricating a native crash or discarding the candidate.

## Reject stale or vacuous evidence

Kani's result document distinguishes success, unreachable and undetermined checks. Its experimental JSON export can leave an earlier apparently complete file after a killed run; correlate `started_at`, actual invocation/configuration and process completion ([results and JSON output](https://raw.githubusercontent.com/model-checking/kani/94253e32fe7ead82c9f1ef842bd9ddc6fae7e8ca/docs/src/verification-results.md)). Do not erase the older evidence; identify which run each artifact belongs to.

Illustrative handoff: input domain length0-10; harness calls the real buffer helper; all required bounds complete; a concrete length/index violates the promised buffer assertion; native replay uses that same helper and setup. Contrast with an interrupted run, a contradictory-assumption pass or a missing Java-body stub. These are different evidence states, not alternative descriptions of one completed verification.

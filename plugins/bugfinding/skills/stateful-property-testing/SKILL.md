---
name: stateful-property-testing
description: Guides model-based property testing of dependent API and protocol operation sequences. Use when bugs require object lifetimes, permissions, session transitions or setup history, and when shrinking must preserve those dependencies.
---

# Stateful property testing

Search states and operations together. Choose this skill when independent values or syntactically valid programs rarely reach the successful API behavior under investigation. Valid sequences can establish state that direct construction misses ([RapidCheck stateful guide](https://raw.githubusercontent.com/emil-e/rapidcheck/master/doc/state.md)). Program generation belongs to `semantic-program-generation`; controlled interleavings belong to `schedule-exploration`.

## Model the promised behavior

Read the actual public producer, enabled configuration and guarantee. Keep only contract facts in the model: logical identities, live handles, ownership, permissions and session state. Start model and system in equivalent states; do not copy implementation caches or branches into the expected result ([RapidCheck command interface](https://raw.githubusercontent.com/emil-e/rapidcheck/master/include/rapidcheck/state/Command.h), [fast-check model design](https://raw.githubusercontent.com/dubzzz/fast-check/main/website/docs/advanced/model-based-testing.md)).

Preserve state-establishing API calls. In Hughes's storage case, create/close/reopen reached hidden state that a shorter visible-equivalent setup did not; an independent corruption check also exposed failures accepted by return-value checks ([Hughes, pp. 14-16](https://publications.lib.chalmers.se/records/fulltext/232550/local_232550.pdf)). Treat that as a reason to inspect lifecycle paths, not a claim that every target needs reopening. Read [model and sequence design](references/model-and-sequences.md) for a worked object/permission experiment.

## Generate meaningful dependent operations

Select operands from current admissible state, using returned identities rather than random nonexistent handles. Hypothesis bundles carry earlier results; fast-check commands expose admissibility checks and execution separately ([Hypothesis stateful tests](https://hypothesis.readthedocs.io/en/latest/stateful.html), [fast-check commands](https://raw.githubusercontent.com/dubzzz/fast-check/main/website/docs/advanced/model-based-testing.md)).

Make intentional invalid transitions their own operations with documented error-and-effect expectations. Do not count a false command precondition as exercising an invalid API: fast-check skips its execution ([runner source, internalModelRun](https://raw.githubusercontent.com/dubzzz/fast-check/main/packages/fast-check/src/check/model/ModelRunner.ts)). Record admitted calls, successful semantic operations and evaluated properties alongside generated sequence counts. Use `correctness-oracles` for the promised observations and `harness-sensitivity` for representative controls.

## Shrink the state and sequence together

Recompute preconditions from the reduced prefix. A command valid when generated can become invalid after earlier operations are removed; RapidCheck explicitly requires precondition checks during shrinking ([stateful guide, Command](https://raw.githubusercontent.com/emil-e/rapidcheck/master/doc/state.md)). Preserve the same violated guarantee while removing unrelated entities, setup and operations. Delegate general interestingness and minimality mechanics to `failure-reduction`.

Save resolved identities, executed operations, setup and observations as well as framework replay data. fast-check command replay needs `replayPath` plus assertion `seed` and `path`; Rapid fail files have version-sensitive replay handling ([fast-check replay](https://raw.githubusercontent.com/dubzzz/fast-check/main/website/docs/advanced/model-based-testing.md), [Rapid engine](https://raw.githubusercontent.com/flyingmutant/rapid/master/engine.go)). A framework seed does not control an external service or scheduler. Keep sequential modeling separate from concurrency claims.

## Select an existing fitting runtime route

Read only the relevant section of [runtime recipes](references/runtime-recipes.md):

- Python: Hypothesis rules, bundles, invariants and machine lifecycle ([official guide](https://hypothesis.readthedocs.io/en/latest/stateful.html)).
- JS/TS: fast-check commands and the appropriate awaited runner ([runner source](https://raw.githubusercontent.com/dubzzz/fast-check/main/packages/fast-check/src/check/model/ModelRunner.ts)).
- Go: Rapid `T.Repeat` / `StateMachineActions`; optional `MakeFuzz` connects a property to Go fuzzing ([state-machine source](https://raw.githubusercontent.com/flyingmutant/rapid/master/statemachine.go), [engine source](https://raw.githubusercontent.com/flyingmutant/rapid/master/engine.go)).
- C++: RapidCheck `Command<Model,Sut>` where its build integration fits ([stateful guide](https://raw.githubusercontent.com/emil-e/rapidcheck/master/doc/state.md)).

Improve an existing sequence generator rather than port it for a tool name. Return the exercised contract and lifecycle, actual operation/property reach, original and reduced replay artifacts, classifications and limits. Preserve model defects and unresolved comparisons; a mismatch does not identify which side is wrong ([Hughes, pp. 14-17](https://publications.lib.chalmers.se/records/fulltext/232550/local_232550.pdf)). Read [common mistakes](references/common-mistakes.md) for misleading success signals. Campaign allocation and final attribution remain `bugfinding-campaign` and `evidence-based-triage` responsibilities.

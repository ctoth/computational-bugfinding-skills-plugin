# Stateful runtime recipes

These are conditional recipes for an existing fitting integration, not commands executed by this skill's author. Use the project's dependency and test runner conventions. Check the selected release, enabled configuration and actual APIs before changing a target. Mutable `main`, `master` and `latest` sources below were inspected on 2026-11-07.

## Python: Hypothesis

Use `RuleBasedStateMachine.TestCase` with the existing unittest/pytest runner. Bundles pass prior results to later rules; `consumes` removes a selected occurrence, while remaining aliases and permissions still need the target's explicit state model ([stateful guide](https://hypothesis.readthedocs.io/en/latest/stateful.html), [Bundle API](https://hypothesis.readthedocs.io/en/latest/reference/api.html#hypothesis.stateful.Bundle)).

Use `@precondition` for admissibility and `@invariant` for the relevant post-operation property. Independent `@initialize` methods run once in arbitrary order and cannot have preconditions; express dependent initialization explicitly rather than assume declaration order. `stateful_step_count` bounds rule calls per example and multiplies with `max_examples` ([API reference](https://hypothesis.readthedocs.io/en/latest/reference/api.html)).

Reset/clean up through the actual per-machine lifecycle. A function-scoped pytest fixture runs once for the whole test, not per generated input; do not suppress that warning to conceal shared state. The inspected compatibility page supports CPython/PyPy 3.11+ and tests macOS/Windows/Linux/Emscripten; recheck the selected version ([compatibility](https://hypothesis.readthedocs.io/en/latest/compatibility.html)).

Where installation is authorized, the official entrypoint is `pip install hypothesis`; use the project's environment. Run an existing machine test with its normal focused selector, such as `pytest path/to/test_world_state.py` ([quickstart](https://hypothesis.readthedocs.io/en/latest/quickstart.html)). License is MPL-2.0 except explicitly identified inherited code ([license](https://raw.githubusercontent.com/HypothesisWorks/hypothesis/master/LICENSE.txt)).

## JS/TS: fast-check

Implement command `check`, `run` and readable `toString`; generate with `fc.commands`. Use `modelRun` for synchronous operations. For asynchronous operations, await `asyncModelRun` inside the awaited property execution: source awaits both admissibility and the command. A skipped `check` is not a target error ([commands arbitrary](https://raw.githubusercontent.com/dubzzz/fast-check/main/packages/fast-check/src/arbitrary/commands.ts), [ModelRunner source](https://raw.githubusercontent.com/dubzzz/fast-check/main/packages/fast-check/src/check/model/ModelRunner.ts)).

Retain emitted assertion `seed`/`path` and the command arbitrary's `replayPath`. Also save the executed command transcript and resolved identities. Scheduled commands are a separate controlled-execution concern, not an implication of choosing an asynchronous runner ([replay constraint source](https://raw.githubusercontent.com/dubzzz/fast-check/main/packages/fast-check/src/check/model/commands/CommandsContraints.ts), [runner source](https://raw.githubusercontent.com/dubzzz/fast-check/main/packages/fast-check/src/check/model/ModelRunner.ts)).

The inspected package snapshot declares MIT, ESM and Node `>=12.17.0`. That declared floor alone does not validate an application's runner, transpiler or module integration; inspect the selected package/lockfile and use its focused test invocation ([package manifest](https://raw.githubusercontent.com/dubzzz/fast-check/main/packages/fast-check/package.json)).

## Go: Rapid

Use an existing `rapid.Check` property, instantiate matching model/SUT state inside its execution and call `t.Repeat(actions)`. The empty-string action is checked initially and after admitted actions. `rapid.StateMachineActions(machine)` derives actions from eligible exported methods and supplies `Check` as that invariant hook ([state-machine implementation](https://raw.githubusercontent.com/flyingmutant/rapid/master/statemachine.go)).

Select inputs from live model facts. Rapid retries skipped actions and can stop when none is valid; diagnose that as generation/admissibility evidence before blaming the target. Keep deliberate invalid API calls as executable actions with their own oracle ([executeAction](https://raw.githubusercontent.com/flyingmutant/rapid/master/statemachine.go)).

For an existing test integration, replace the selector/path and choose positive counts from actual cost and budget:

```text
go test ./path/to/pkg -run '^TestWorldState$' -args -rapid.checks=COUNT -rapid.steps=STEPS
go test ./path/to/pkg -run '^TestWorldState$' -args -rapid.failfile=PATH
```

`rapid.steps` is an average sequence-length control, not an exact length or hard time ceiling. Preserve the emitted fail file, seed, trace and version; file-format changes can invalidate replay. Shared `rapid.T` draws are not concurrent-safe ([engine flags/replay](https://raw.githubusercontent.com/flyingmutant/rapid/master/engine.go)).

Ordinary Rapid search lacks coverage feedback; `rapid.MakeFuzz` adapts a property to `func(*testing.T, []byte)` for Go's fuzzer. This controls generated choices, not arbitrary goroutine scheduling ([README comparison](https://raw.githubusercontent.com/flyingmutant/rapid/master/README.md), [MakeFuzz source](https://raw.githubusercontent.com/flyingmutant/rapid/master/engine.go)). The inspected module declares Go 1.23; recheck the selected release. Source headers specify MPL-2.0 ([module](https://raw.githubusercontent.com/flyingmutant/rapid/master/go.mod), [state-machine source](https://raw.githubusercontent.com/flyingmutant/rapid/master/statemachine.go)).

## C++: RapidCheck boundary

Where already compatible, `rc::state::Command<Model,Sut>` separates model `apply`, actual `run` and `checkPreconditions`. Recheck every precondition after shrinking and ensure initial states agree. This reference does not establish a current C++ build/platform recipe; inspect the actual selected integration rather than port another target for the framework ([Command interface](https://raw.githubusercontent.com/emil-e/rapidcheck/master/include/rapidcheck/state/Command.h), [stateful guide](https://raw.githubusercontent.com/emil-e/rapidcheck/master/doc/state.md)).

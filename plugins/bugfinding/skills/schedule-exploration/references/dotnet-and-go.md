# .NET and Go boundaries

## Coyote

For an existing Coyote integration, verify the SDK/package/tool host against the assembly's target. The documentation snapshot accessed 2026-11-07 lists .NET 8/10 and .NET Standard 2.0 cross-platform routes, plus Windows Framework 4.6.2; check the selected release instead of upgrading the application to a guessed tool floor. Coyote is MIT ([setup](https://microsoft.github.io/coyote/get-started/install/), [license](https://raw.githubusercontent.com/microsoft/coyote/main/LICENSE)).

Rewrite relevant test/owned production assemblies using the host matching their target major version. Give the existing rewriting configuration a disposable test-output `OutputPath`; omission can overwrite input assemblies. Unsupported/pass-through dependencies narrow control ([rewriting](https://microsoft.github.io/coyote/concepts/binary-rewriting/)).

Conditional command shapes, after checking selected CLI help:

```text
coyote rewrite REWRITING_CONFIG.json
coyote test TEST_ASSEMBLY.dll --iterations N --max-steps S --timeout T
coyote replay TEST_ASSEMBLY.dll FAILURE.trace
```

Choose actual N/S/T from the authorized scenario/budget. Inspect iteration-length output; a step cap and total timeout serve different purposes. Reset static state between iterations. Default invocation may run only one iteration ([CLI execution/replay](https://microsoft.github.io/coyote/get-started/using-coyote/)).

Library `TestingEngine` also needs rewritten binaries. Assert the actual `TestReport` outcome in the hosting test, and iterate `TryEmitTraces` to materialize its lazy outputs ([unit-test integration](https://microsoft.github.io/coyote/how-to/unit-testing/)).

Systematic mode explores sequentially consistent controlled schedules, not processor/JIT weak-memory reorderings. The documented wait APIs model finite nonzero timeouts as infinite; `Lock.TryEnter` instead reports that case unsupported. This does not validate arbitrary wall-clock timeout races. Preserve these limits and distinguish the separate real-thread systematic-fuzzing mode ([time and memory model](https://microsoft.github.io/coyote/concepts/binary-rewriting/)).

## Go

`synctest.Test` supplies isolated bubbles/fake time and `Wait` waits for durable blocking. Mutex acquisition, I/O and syscalls are outside its documented durable-block category. This is useful time/quiescence testing, not documented enumeration of scheduling choices ([synctest](https://pkg.go.dev/testing/synctest)).

For a Go target, inspect existing held-step or scheduler-choice seams and the actual guarantee before proposing additional orders. If no fitting controller exists, state that limitation and select another supported discovery dimension through `bugfinding-campaign`; do not advertise a drop-in Loom/Coyote backend for Go. This is the pack's routing decision grounded in those explicit runtime boundaries.

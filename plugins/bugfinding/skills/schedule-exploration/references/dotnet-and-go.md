# .NET and Go boundaries

## Coyote

For an existing Coyote integration, verify the SDK/package/tool host against the assembly's target. The documentation snapshot accessed 2026-11-07 lists .NET 8/10 and .NET Standard 2.0 cross-platform routes, plus Windows Framework 4.6.2; check the selected release instead of upgrading the application to a guessed tool floor. The LICENSE file is "MIT License" ([Prerequisites](https://raw.githubusercontent.com/microsoft/coyote/2202e75a861f4e8a63149366c2e41ea21d73ae54/docs/get-started/install.md), [license](https://raw.githubusercontent.com/microsoft/coyote/2202e75a861f4e8a63149366c2e41ea21d73ae54/LICENSE)).

Rewrite relevant test/owned production assemblies using the host matching their target major version: "run the host that matches the .NET major version targeted by the assembly". Give the existing rewriting configuration a disposable test-output `OutputPath`; when it is omitted, "the original assemblies will be replaced". Unsupported/pass-through dependencies narrow control ([Choosing the right Coyote host, Configuration, Which DLLs to rewrite?](https://raw.githubusercontent.com/microsoft/coyote/2202e75a861f4e8a63149366c2e41ea21d73ae54/docs/concepts/binary-rewriting.md)).

Conditional command shapes, after checking selected CLI help:

```text
coyote rewrite REWRITING_CONFIG.json
coyote test TEST_ASSEMBLY.dll --iterations N --max-steps S --timeout T
coyote replay TEST_ASSEMBLY.dll FAILURE.trace
```

Choose actual N/S/T from the authorized scenario/budget. Inspect iteration-length output; a step cap and total timeout serve different purposes (`--max-steps` kills one iteration and starts a new one; `--timeout` bounds the run). Reset static state: "the iterations run in shared memory". Without `--iterations`, "the tester will perform 1 iteration by default" ([Testing options, Test entry point, Reproducing and debugging traces](https://raw.githubusercontent.com/microsoft/coyote/2202e75a861f4e8a63149366c2e41ea21d73ae54/docs/get-started/using-coyote.md)).

Library `TestingEngine` also needs rewritten binaries. Assert the actual `TestReport` outcome in the hosting test, and iterate `TryEmitTraces` to materialize its lazy outputs: "`TryEmitTraces` is an iterator method". Replay through `Configuration.Create().WithReproducibleTrace(trace)`, passing the `.trace` contents or `TestingEngine.ReproducibleTrace` ([unit-test integration, Replaying a trace](https://raw.githubusercontent.com/microsoft/coyote/2202e75a861f4e8a63149366c2e41ea21d73ae54/docs/how-to/unit-testing.md)).

Systematic mode explores sequentially consistent controlled schedules, not processor/JIT weak-memory reorderings: "Every schedule that Coyote explores is sequentially consistent". The documented wait APIs explore a finite nonzero timeout "as if it was infinite"; `Lock.TryEnter` instead reports that case unsupported. This does not validate arbitrary wall-clock timeout races. Preserve these limits and distinguish the separate systematic-fuzzing mode, which "executes the program on real threads and in real time" ([How timeouts are modeled, How memory ordering is modeled](https://raw.githubusercontent.com/microsoft/coyote/2202e75a861f4e8a63149366c2e41ea21d73ae54/docs/concepts/binary-rewriting.md)).

## Go

`synctest.Test` supplies isolated bubbles/fake time and `Wait` waits for durable blocking. Mutex acquisition, I/O and syscalls are outside its documented durable-block category: "Operations not in the above list are not durably blocking." This is useful time/quiescence testing, not documented enumeration of scheduling choices ([synctest, Time, Blocking](https://pkg.go.dev/testing/synctest@go1.27.3)).

For a Go target, inspect existing held-step or scheduler-choice seams and the actual guarantee before proposing additional orders. If no fitting controller exists, state that limitation and select another supported discovery dimension through `bugfinding-campaign`; do not advertise a drop-in Loom/Coyote backend for Go. This is the pack's routing decision grounded in those explicit runtime boundaries.

# Runtime and model routes

These are source-read conditional command shapes, not commands executed for the target. Select a compatible existing integration and preserve its actual version/configuration.

## Coyote: controlled .NET obligations

The inspected setup lists .NET 10/8/Standard 2 routes and Windows Framework 4.6.2; recheck the chosen artifact and target framework ([installation prerequisites](https://raw.githubusercontent.com/microsoft/coyote/2202e75a861f4e8a63149366c2e41ea21d73ae54/docs/get-started/install.md)). Existing assemblies require the supported rewriting/test-entry setup; static state is shared between iterations and must reset ([Using Coyote, rewriting and test entry](https://raw.githubusercontent.com/microsoft/coyote/2202e75a861f4e8a63149366c2e41ea21d73ae54/docs/get-started/using-coyote.md)).

```text
coyote rewrite EXISTING_REWRITE_CONFIG.json
coyote test EXISTING_TEST.dll --iterations N --max-steps S
coyote replay EXISTING_TEST.dll FAILURE.trace
```

Substitute actual paths and measured iteration/step choices. The documented test entry carries the systematic-testing attribute; replay consumes the emitted trace ([Using Coyote, Testing options and replay](https://raw.githubusercontent.com/microsoft/coyote/2202e75a861f4e8a63149366c2e41ea21d73ae54/docs/get-started/using-coyote.md)). Unsupported operations need their actual model/replay limits, not an ignored diagnostic.

A hot/cold monitor expresses pending/satisfied progress; the temperature test is a potential-liveness heuristic ([liveness checking](https://raw.githubusercontent.com/microsoft/coyote/2202e75a861f4e8a63149366c2e41ea21d73ae54/docs/how-to/liveness-checking.md)). At the selected source, runtime temperature checks require a fair iteration; the state-monitor counter advances only in hot state with threshold above zero, and cold resets it ([runtime](https://raw.githubusercontent.com/microsoft/coyote/2202e75a861f4e8a63149366c2e41ea21d73ae54/Source/Core/Runtime/CoyoteRuntime.cs), [Monitor](https://raw.githubusercontent.com/microsoft/coyote/2202e75a861f4e8a63149366c2e41ea21d73ae54/Source/Core/Specifications/Monitors/Monitor.cs)). Warm does not advance that counter. Threshold zero disables this counter check, not necessarily every other liveness observation. Preserve threshold, strategy/fairness, step limits, monitor state and trace; do not call threshold exhaustion a wall-time or infinite-execution proof.

## TLC: a temporal model with a real correspondence

The inspected tool README requires Java 11+ and identifies versioned releases; choose the actual existing jar/spec/configuration ([README](https://raw.githubusercontent.com/tlaplus/tlaplus/d8fb231de4e4b5d02c1b2ed1ac759c086f694021/README.md)). Its supported command entry and trace import/export are documented in USE ([command-line and model-based testing](https://raw.githubusercontent.com/tlaplus/tlaplus/d8fb231de4e4b5d02c1b2ed1ac759c086f694021/USE.md)):

```text
java -cp EXISTING_tla2tools.jar tlc2.TLC -config EXISTING.cfg EXISTING.tla
```

The configuration must select the intended behavior, fairness and temporal property. The shipped clock model makes its weak-fairness premise explicit ([LiveHourClock, LSpec](https://raw.githubusercontent.com/tlaplus/tlaplus/d8fb231de4e4b5d02c1b2ed1ac759c086f694021/tlatools/org.lamport.tlatools/test-model/examples/SpecifyingSystems/Liveness/LiveHourClock.tla)). A model result concerns that abstraction; preserve a mapping from actions/state to the actual producer and test the candidate against real behavior instead of copying production code into another implementation.

Do not use TLC symmetry sets for liveness: its documentation warns of missed and nonexistent errors. Distributed TLC does not check liveness, so adding distributed workers cannot fund that check ([symmetry warning](https://raw.githubusercontent.com/tlaplus/tlaplus/d8fb231de4e4b5d02c1b2ed1ac759c086f694021/toolbox/org.lamport.tla.toolbox.doc/html/model/model-values.html), [distributed limitations](https://raw.githubusercontent.com/tlaplus/tlaplus/d8fb231de4e4b5d02c1b2ed1ac759c086f694021/toolbox/org.lamport.tla.toolbox.doc/html/model/distributed-mode.html)). Record state/action constraints because they prune exploration ([Spec Options, constraints](https://raw.githubusercontent.com/tlaplus/tlaplus/d8fb231de4e4b5d02c1b2ed1ac759c086f694021/toolbox/org.lamport.tla.toolbox.doc/html/model/spec-options-page.html)). Graph exploration is followed by final temporal checking; interruption there is incomplete evidence ([ModelChecker, finalCheck](https://raw.githubusercontent.com/tlaplus/tlaplus/d8fb231de4e4b5d02c1b2ed1ac759c086f694021/tlatools/org.lamport.tlatools/src/tlc2/tool/ModelChecker.java)). The CLI's `-deadlock` disables deadlock checking; it is not an enable flag ([TLC parser](https://raw.githubusercontent.com/tlaplus/tlaplus/d8fb231de4e4b5d02c1b2ed1ac759c086f694021/tlatools/org.lamport.tlatools/src/tlc2/TLC.java)).

## Go: fake time and quiescence

Use an existing appropriate synctest test and the project's permitted focused runner. Fake time advances only when bubble goroutines are durably blocked; a CPU loop can prevent that, and mutex/I/O/syscall waiting is outside the documented durable-blocking set ([synctest, Time/Blocking](https://raw.githubusercontent.com/golang/go/dcc06a82727b447270b1a58cc5f86b49736e317c/src/testing/synctest/synctest.go)). An execution-budget timeout protects the run but is not automatically the product's promised deadline. This API does not document schedule enumeration; select `schedule-exploration` for controlled-choice search where actually supported.

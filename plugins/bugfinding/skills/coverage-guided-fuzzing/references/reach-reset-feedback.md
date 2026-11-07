# Reach, reset and feedback

Use a finite pilot on an existing target. This diagnostic order is the pack's decision aid, not a mandatory new instrumentation framework.

| Observation | Next useful investigation |
|---|---|
| Feedback grows in driver parsing but intended library code is untouched | Read actual compile/link/module coverage; instrument the target owner, not only the harness ([LLVM libFuzzer](https://llvm.org/docs/LibFuzzer.html)). |
| Most inputs stop at compression/format checks | Construct mutations in the relevant decoded representation through existing producer/encoder ownership; retain malformed-input checks when they test a separate guarantee ([Google structure-aware fuzzing guide](https://raw.githubusercontent.com/google/fuzzing/master/docs/structure-aware-fuzzing.md)). |
| A stable format reaches a hard comparison barrier | Try a fitting dictionary or matched ordinary/CmpLog build, then measure the changed reach ([AFL++ CmpLog](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation/README.cmplog.md)). |
| A saved input passes alone but fails after a long run | Preserve prior sequence/state and compare real lifecycle/reset boundaries; do not discard evidence after one fresh regression ([Jazzer Lifecycle implementation](https://raw.githubusercontent.com/CodeIntelligenceTesting/jazzer/main/src/main/java/com/code_intelligence/jazzer/junit/Lifecycle.java), [AFL++ persistent mode](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation/README.persistent_mode.md)). |
| Many calls occur but useful operations skip | Track admitted inputs, actual operation/effect and property evaluation separately; coverage reports help identify unvisited paths ([Rust coverage](https://rust-fuzz.github.io/book/cargo-fuzz/coverage.html)). |

## Worked persistent-fixture diagnosis

A JVM fuzz test initializes a world in `@BeforeEach`. Saved-input regression passes; discovery produces a delayed state-dependent failure. Read the actual annotation/lifecycle: default discovery can initialize once, while regression initializes for each input. Preserve the original input sequence and outputs, then establish whether the promised experiment requires isolated inputs or intentional stateful sequences. Use supported lifecycle/reset for the former; represent the sequence explicitly for the latter. Neither outcome by itself decides product versus harness blame ([Jazzer FuzzTest annotation](https://raw.githubusercontent.com/CodeIntelligenceTesting/jazzer/main/src/main/java/com/code_intelligence/jazzer/junit/FuzzTest.java), [Jazzer Lifecycle implementation](https://raw.githubusercontent.com/CodeIntelligenceTesting/jazzer/main/src/main/java/com/code_intelligence/jazzer/junit/Lifecycle.java)).

## Choose one lever against the observed barrier

A custom mutator may unlock a structured decoder but still fail every semantic prerequisite. Keep its representation, trimming and replay contract explicit; `AFL_CUSTOM_MUTATOR_ONLY` changes the search population, and a broken output-buffer contract can fail inside the fuzzer ([AFL++ custom mutators](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/docs/custom_mutators.md)). Use `semantic-program-generation` or `stateful-property-testing` when successful execution needs types, identities, permissions or earlier operations.

A source-only receiving lane and a typed choice-byte generator need deliberate producer-based conversion. Go's corpus preserves argument types/order; relabeling bytes as a source string does not convert the generated program. `corpus-evolution` owns compatible exchange ([Go fuzzing](https://go.dev/doc/security/fuzz/)).

Record the actual discovery mode, target/build differences, counters and omissions with retained artifacts. Use `harness-sensitivity` for representative violations through the same property. Reallocate with `bugfinding-campaign`; repetition of the same blocked lane is not itself a new search dimension.

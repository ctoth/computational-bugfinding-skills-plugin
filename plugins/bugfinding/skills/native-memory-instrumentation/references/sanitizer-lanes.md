# Compatible sanitizer lanes

Use these source-read command shapes only with a fitting installed compiler/runtime and an authorized existing target. Substitute actual source/output paths; the examples were not executed for this skill. LLVM's implementation license is Apache-2.0 with LLVM exceptions ([license](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/LICENSE.TXT)). Verify selected-release support rather than treating a development snapshot as the installed toolchain.

## Addressability and lifetime: ASan

```text
clang++ -O1 -g -fsanitize=address -fno-omit-frame-pointer harness.cc target.cc -o memory_target
```

Instrument relevant code and use the compiler driver for final linking. Retain the first failure and allocation/free context; symbolization needs matching debug files and llvm-symbolizer through PATH or ASAN_SYMBOLIZER_PATH. Stack-return/scope modes and container annotations have distinct coverage. Partially instrumented container code can produce false reports or omissions; investigate the actual annotation/lifetime boundary ([ASan, Usage, Additional Checks and Symbolizing](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/clang/docs/AddressSanitizer.md)).

## Value definedness: MSan

```text
clang++ -O1 -g -fsanitize=memory -fsanitize-memory-track-origins=2 -fno-omit-frame-pointer harness.cc target.cc -o definedness_target
```

Use compatible instrumented dependencies and interceptors, not merely this driver build. Origin tracking adds allocation/store evidence and cost. Assembly, custom syscalls or uninstrumented outputs need actual propagation evidence; blanket unpoisoning can erase the selected violation. Full instrumentation disabling differs from disabling only checks, and can create false reports. The pinned document lists Linux/NetBSD/FreeBSD; verify the chosen release and native dependencies ([MSan, Origin Tracking, Handling external code and Limitations](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/clang/docs/MemorySanitizer.md)).

## Selected undefined behavior: UBSan

```text
clang++ -O1 -g -fno-omit-frame-pointer -fno-sanitize-merge -fsanitize=undefined -fno-sanitize-recover=undefined harness.cc target.cc -o ub_target
```

This fail-fast shape selects the undefined group; recoverable/trap modes produce different evidence and must remain in replay identity. Unsigned overflow, implicit conversion, local bounds and vptr are not all in that group. Select additional checks from the actual language/API guarantee. Symbolized stacks need the supported runtime option and matching symbolizer; a zero exit with a recovered report is still evidence ([UBSan, Usage, Available checks and Stack traces](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/clang/docs/UndefinedBehaviorSanitizer.md)).

## Unreachable allocations: LSan

```text
clang -g -fsanitize=leak target.c -o leak_target
```

Use the compiler driver for final linking; supported ASan integrations can supply leak detection too. Record whether an end-of-process or supported explicit scan completed. Root regions, thread-local disable scopes and ignored objects change the observation. The recoverable explicit scan returns a result without disabling the final scan; LSan-specific runtime flags still use LSAN_OPTIONS under ASan ([LSan, Usage, Programmatic Disabling and Flags](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/clang/docs/LeakSanitizer.md)). Reachable growth needs a separate application resource contract.

## Build compatibility and cost

The inspected driver rejects address with thread/memory, thread with memory, and leak with thread/memory. Use separate fitting builds; integrated leak behavior is not simply independent flags stacked together ([Clang driver, IncompatibleGroups and leak handling](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/clang/lib/Driver/SanitizerArgs.cpp)). Record real resource consumption: sanitizer shadow mappings make virtual-address caps different from RSS, and LLVM ASan/MSan do not support fully static executables ([ASan, Limitations](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/clang/docs/AddressSanitizer.md), [MSan, Limitations](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/clang/docs/MemorySanitizer.md)).

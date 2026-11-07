# Compatible sanitizer lanes

Use these source-read command shapes only with a fitting installed compiler/runtime and an authorized existing target. Substitute actual source/output paths; the examples were not executed for this skill. LLVM's implementation license is Apache-2.0 with LLVM exceptions ([license](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/LICENSE.TXT)). Verify selected-release support rather than treating a development snapshot as the installed toolchain.

## Addressability and lifetime: ASan

```text
clang++ -O1 -g -fsanitize=address -fno-omit-frame-pointer harness.cc target.cc -o memory_target
```

Instrument relevant code and use the compiler driver for final linking ("use `clang` (not `ld`) for the final link step"). "AddressSanitizer exits on the first detected error", so retain that first failure and its allocation/free context. Symbolization needs llvm-symbolizer through PATH or ASAN_SYMBOLIZER_PATH; on macOS, `dsymutil` may be needed for file:line. Stack-return/scope modes and container annotations have distinct coverage. Container checks are "prone to false positives": partial stack poisoning "can cause both false positives and negatives", and a partially instrumented binary can cause false positives; investigate the actual annotation/lifetime boundary ([ASan, Usage, Symbolizing the Reports and Additional Checks](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/clang/docs/AddressSanitizer.md)).

## Value definedness: MSan

```text
clang++ -O1 -g -fsanitize=memory -fsanitize-memory-track-origins=2 -fno-omit-frame-pointer harness.cc target.cc -o definedness_target
```

Use compatible instrumented dependencies and interceptors, not merely this driver build: uninstrumented code "may result in false reports", and inline assembly that writes memory may need replacing. Origin tracking adds allocation/store evidence and slows execution "by a factor of 1.5x-2x on top of the usual MemorySanitizer slowdown". Syscalls or inline assembly that MSan cannot see need explicit checks or actual propagation evidence; blanket unpoisoning can erase the selected violation. `no_sanitize("memory")` disables only checks, while `disable_sanitizer_instrumentation` prevents all instrumentation and "may introduce false positives". The pinned document lists Linux/NetBSD/FreeBSD; verify the chosen release and native dependencies ([MSan, Usage, Origin Tracking, Handling external code and Supported Platforms](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/clang/docs/MemorySanitizer.md)).

## Selected undefined behavior: UBSan

```text
clang++ -O1 -g -fno-omit-frame-pointer -fno-sanitize-merge -fsanitize=undefined -fno-sanitize-recover=undefined harness.cc target.cc -o ub_target
```

This fail-fast shape selects the undefined group; `-fno-sanitize-recover` makes a failed check "print a verbose error report and exit the program", while recoverable/trap modes produce different evidence and must remain in replay identity. The undefined group is "All of the checks listed above other than `float-divide-by-zero`, `unsigned-integer-overflow`, `implicit-conversion`, `local-bounds`, `vptr` and the `nullability-*` group of checks". Select additional checks from the actual language/API guarantee; unsigned overflow "is not undefined behavior". Symbolized stacks need `-g`, `-fno-sanitize-merge`, `-fno-omit-frame-pointer`, `UBSAN_OPTIONS=print_stacktrace=1` and llvm-symbolizer in PATH; a zero exit with a recovered report is still evidence ([UBSan, Usage, Available checks and Stack traces and report symbolization](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/clang/docs/UndefinedBehaviorSanitizer.md)).

## Unreachable allocations: LSan

```text
clang -g -fsanitize=leak target.c -o leak_target
```

Use the compiler driver for final linking. ASan "integrates LeakSanitizer and enables it by default on supported platforms"; ASan's own page says leak detection is on by default on Linux, opt-in via `ASAN_OPTIONS=detect_leaks=1` on macOS and "not yet supported on other platforms". LSan runs "an extra leak detection phase" at the very end of the process, so record whether an end-of-process or supported explicit scan completed. Root regions, thread-local disable scopes and ignored objects change the observation. `__lsan_do_leak_check()` "disables subsequent automatic leak checks at process exit", while `__lsan_do_recoverable_leak_check()` returns a result without "disabling the end-of-process check"; LSan-specific runtime flags still use LSAN_OPTIONS under ASan ([LSan, Introduction, Usage, Runtime Suppressions, Programmatic Disabling and Flags and Options](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/clang/docs/LeakSanitizer.md), [ASan, Memory leak detection and Options Evaluation with Integrated Sanitizers](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/clang/docs/AddressSanitizer.md)). Reachable growth needs a separate application resource contract.

## Build compatibility and cost

The inspected driver rejects address with thread/memory, thread with memory, and leak with thread/memory. Use separate fitting builds; integrated leak behavior is not simply independent flags stacked together, since "-fsanitize=leak is silently ignored in the presence of -fsanitize=address" ([Clang driver, IncompatibleGroups and leak handling](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/clang/lib/Driver/SanitizerArgs.cpp)). Record real resource consumption: ASan and MSan map "(but not reserves)" terabytes of virtual address space, so "tools like `ulimit` may not work as usually expected", and LLVM ASan/MSan do not support static linking ([ASan, Limitations](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/clang/docs/AddressSanitizer.md), [MSan, Limitations](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/clang/docs/MemorySanitizer.md)).

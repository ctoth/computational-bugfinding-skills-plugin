---
name: native-memory-instrumentation
description: Guides native memory bugfinding with ASan, MSan, UBSan, LSan and Valgrind Memcheck. Use when selecting an executable memory-safety observation, instrumenting native or FFI dependencies, or investigating sanitizer reports, leak phases and missing diagnostic coverage.
---

# Native memory instrumentation

Choose a missing memory property on an actual native producer, then search executions that can violate it. ASan addressability, MSan definedness and selected UB checks observe different failures; they are not interchangeable correctness oracles ([ASan, Introduction](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/clang/docs/AddressSanitizer.md), [MSan, Introduction](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/clang/docs/MemorySanitizer.md), [UBSan, Available checks](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/clang/docs/UndefinedBehaviorSanitizer.md)).

## Select the lane and its real boundary

Read the target's allocation, initialization, publication/use and destruction paths, enabled build, native modules and valid-call contract. State which property the lane can refute and where its observation ends. The ASan paper documents addressable wrong-object accesses and allocator reuse as missed cases; more executions alone do not remove those observer limits ([ASan paper, §§3.5 and 5.2](https://www.usenix.org/system/files/conference/atc12/atc12-final39.pdf)).

| Intended observation | Read when selecting or running it |
|---|---|
| Native addressability/lifetime, definedness, selected UB or unreachable allocations | [Compatible sanitizer lanes](references/sanitizer-lanes.md) |
| Existing executable under binary instrumentation, custom pools and leak-error policy | [Memcheck operation](references/memcheck-operation.md) |
| Go/cgo or Windows native/managed boundary | [Native integration boundaries](references/native-boundaries.md) |
| Report, scan completion and replay evidence | [Diagnostics and worked cases](references/diagnostics-and-cases.md) |

These are this pack's responsibility routes. Use `coverage-guided-fuzzing` or the semantic/stateful generators for input search, `race-detection-campaigns` for conflicting-access detection, and `resource-complexity-testing` for retained-growth contracts.

Verify the selected compiler/runtime/platform and loaded objects before execution. MSan requires instrumented program code with fitting interceptors; a driver-only flag is not dependency coverage. Clang's actual incompatibility table also rejects several sanitizer combinations, so choose compatible builds rather than an all-tools binary ([MSan, Handling external code](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/clang/docs/MemorySanitizer.md), [Clang driver, IncompatibleGroups](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/clang/lib/Driver/SanitizerArgs.cpp)).

## Pilot an informative execution

Use an existing fitting build and real workload, or change the existing owner only within the task's authority. Exercise relevant allocation/lifetime sequences and the intended observation; use `harness-sensitivity` for a representative healthy/faulty control. Retain selected instrumentation, allocator and diagnostic settings: redzones and quarantine affect the detection window, while historical overhead is not a forecast for a new target ([ASan paper, §§3.3–3.5 and 4](https://www.usenix.org/system/files/conference/atc12/atc12-final39.pdf)).

Observe raw diagnostics, process status and whether the requested leak phase actually ran. UBSan commonly reports and continues; Memcheck's default error-exit policy preserves application status. A timeout with no completed leak scan is not a clean leak result ([UBSan, Usage](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/clang/docs/UndefinedBehaviorSanitizer.md), [Valgrind core, Error-related options](https://valgrind.org/docs/manual/manual-core.html), [Memcheck, §4.3](https://valgrind.org/docs/manual/mc-manual.html)).

Do not add suppressions or unpoisoning to make an unexplained report green. Preserve any existing omissions: MSan ignorelists treat loads as initialized, and LSan ignored objects can hide reachable descendants ([MSan, Ignorelist](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/clang/docs/MemorySanitizer.md), [LSan, Programmatic Disabling](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/clang/docs/LeakSanitizer.md)). See [common mistakes](references/common-mistakes.md).

## Preserve and hand over the finding

Keep original input/setup/prior sequence, valid-call evidence, actual loaded-module/source/build identity, compiler/runtime/architecture, flags, allocator/root settings, raw diagnostic and status, allocation/free/origin stacks, scan phase and actual replay attempts. ASan symbolization depends on matching debug information and symbolizer; rebuild differences must remain visible ([ASan, Symbolizing the Reports](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/clang/docs/AddressSanitizer.md)).

Return the tested producer/property, actual execution budget, observed coverage and omissions, report/replay paths, supported violations and unresolved cases. Route reduction and attribution to `failure-reduction` and `evidence-based-triage`; a diagnostic does not by itself establish exploitability or every underlying cause. Retain bounded negative results with their observation limits.

Invocation preserves existing scope and runner rules; it does not authorize installing tools, changing targets or publishing findings.

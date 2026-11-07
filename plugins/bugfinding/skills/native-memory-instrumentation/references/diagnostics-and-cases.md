# Diagnostics and worked cases

These are this pack's illustrative investigations, not executed target findings.

## A report with successful process status

A UBSan lane emits a runtime finding, recovery continues and the harness accepts exit zero. Preserve the diagnostic and selected check/recovery mode; make the existing observer consume it or use a supported fail-fast configuration for the same property. Do not reinterpret defined unsigned arithmetic as UB solely because an optional checker warns: for `unsigned-integer-overflow`, "this is not undefined behavior, but it is often unintentional" ([UBSan, Usage and Available checks](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/clang/docs/UndefinedBehaviorSanitizer.md)).

## A missing leak phase

A persistent worker is killed at its timeout. No leak output appeared, but the exit scan never completed. Retain that outcome as incomplete; inspect an existing quiescence/explicit-scan seam, noting that `__lsan_do_leak_check()` "disables subsequent automatic leak checks at process exit" while the recoverable variant does not. LSan root/ignore policies and Memcheck leak-error categories must remain part of the observation ([LSan, Programmatic Disabling](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/clang/docs/LeakSanitizer.md), [Memcheck, §§4.2.10 and 4.3](https://valgrind.org/docs/manual/mc-manual.html)). A reachable cache may violate a separate retention promise without becoming an unreachable-leak report.

## A smaller case changes the failure

A lifetime sequence produces an invalid access, but shrinking removes setup and leaves an illegal API call. Keep the original and require the real valid-call/lifetime preconditions in interestingness. Allocator reuse/quarantine can also change whether the selected addressability observer sees a freed object ("a use-after-free may not be detected" after a large allocate/free burst between the free and the use); keep those settings and the prior sequence ([ASan paper, §3.5](https://www.usenix.org/system/files/conference/atc12/atc12-final39.pdf)). Route bundle reduction to `failure-reduction`.

## Evidence sufficient for the next maintainer

Retain exact input/setup/sequence, loaded target and native-module identities, compiler/runtime/build flags, architecture, allocator/root/suppression settings, raw report/status and scan phase, symbol files, allocation/free/origin stacks and actual replay attempts. ASan reports include "freed by thread T0 here" and "previously allocated by thread T0 here" stacks and rely on llvm-symbolizer; MSan origin tracking "collects both allocation points and all intermediate stores" ([ASan, report example and Symbolizing](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/clang/docs/AddressSanitizer.md), [MSan, Origin Tracking](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/clang/docs/MemorySanitizer.md)).

State the demonstrated access/definedness/UB/leak violation before a proposed cause, severity or fix. A clean finite run covers reached observations, not every native path or semantic guarantee. Preserve missing symbolization, unsupported initialization, suppressed regions and intermittent replay as separate limits. Use `evidence-based-triage` for attribution and causal grouping.

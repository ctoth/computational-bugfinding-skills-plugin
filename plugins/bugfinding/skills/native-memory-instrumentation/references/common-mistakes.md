# Common mistakes

| WRONG | RIGHT | Primary evidence |
|---|---|---|
| Enable every sanitizer in one binary. | Select compatible property-specific builds. | [Clang incompatibility table](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/clang/lib/Driver/SanitizerArgs.cpp) |
| The driver is instrumented, so its prebuilt FFI library is covered. | Verify actual library and shadow-propagation boundaries. | [MSan external code](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/clang/docs/MemorySanitizer.md), [ASan paper §5.2](https://www.usenix.org/system/files/conference/atc12/atc12-final39.pdf) |
| A zero exit means no undefined behavior. | Preserve recovered diagnostics and selected check mode. | [UBSan Usage](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/clang/docs/UndefinedBehaviorSanitizer.md) |
| No leak report before forced termination means no leak. | Record whether the selected scan actually completed. | [LSan scan API](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/clang/docs/LeakSanitizer.md), [Memcheck §4.3](https://valgrind.org/docs/manual/mc-manual.html) |
| All displayed leaks change the exit status. | Record full-scan and selected error-kind policy separately. | [Memcheck §§4.2.10–4.3](https://valgrind.org/docs/manual/mc-manual.html), [core error options](https://valgrind.org/docs/manual/manual-core.html) |
| Add ignore rules until the run is clean. | Keep real synchronization/initialization evidence and explicit omissions. | [MSan Ignorelist](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/clang/docs/MemorySanitizer.md) |
| ASan covers arbitrary managed Windows methods. | Establish native translation-unit/module coverage and mixed-mode lifetime. | [MSVC known issues](https://raw.githubusercontent.com/MicrosoftDocs/cpp-docs/f29e25fb8f05bb38cf0246476b5c1fc92bf33876/docs/sanitizers/asan-known-issues.md) |
| A smaller crash is necessarily the original native defect. | Preserve valid-call state, allocator conditions and selected witness. | [ASan paper §3.5](https://www.usenix.org/system/files/conference/atc12/atc12-final39.pdf) |

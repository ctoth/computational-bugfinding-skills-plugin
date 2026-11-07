# Native integration boundaries

## Go and cgo

The pinned Go build documentation describes ASan/MSan interoperation with OS/architecture/compiler restrictions; inspect the selected toolchain's own help/source, not the union of a development source and older article. The actual builder prepends matching sanitizer flags to cgo C compilation and linking, which does not rebuild arbitrary precompiled libraries ([Go build flags](https://raw.githubusercontent.com/golang/go/dcc06a82727b447270b1a58cc5f86b49736e317c/src/cmd/go/alldocs.go), [actual cgo producer](https://raw.githubusercontent.com/golang/go/dcc06a82727b447270b1a58cc5f86b49736e317c/src/cmd/go/internal/work/exec.go)).

Conditional focused shape for an existing fitting test:
```text
go test -asan ./path/to/pkg -run '^TestNativeBoundary$' -count=1
```

A separate MSan lane also needs its compatible native dependency closure. Preserve actual library/object identities and instrumented/native build differences. These flags do not establish general pure-Go logic or race safety; use this pack's relevant oracle/race owner. The command is an unexecuted example subject to the project's permitted runner ([Go build flags](https://raw.githubusercontent.com/golang/go/dcc06a82727b447270b1a58cc5f86b49736e317c/src/cmd/go/alldocs.go), [MSan external-code contract](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/clang/docs/MemorySanitizer.md)).

## Native Windows

From a compatible existing MSVC developer environment:
```text
cl /fsanitize=address /Zi target.cpp
```

Run the actual produced executable with its workload. The pinned document scopes support to Windows 10+ x86/x64 and lists incompatible edit-and-continue, incremental linking and runtime-check modes. Use an appropriate separate diagnostic configuration, retaining the actual compiler/runtime DLL and debug identity. ASAN_SAVE_DUMPS can retain supported diagnostic dumps ([MSVC ASan, Build integration, Crash dump support and Command prompt](https://raw.githubusercontent.com/MicrosoftDocs/cpp-docs/f29e25fb8f05bb38cf0246476b5c1fc92bf33876/docs/sanitizers/asan.md)).

The implementation has its own boundaries: uninstrumented precompiled headers, allocator overrides, coroutines and mixed-mode loading can hide accesses or create runtime artifacts. C++/CLI support is experimental; managed/JIT methods are not guaranteed instrumented. Inspect the native translation-unit/DLL producer before attributing a shutdown/unload report to application memory corruption. Do not import arbitrary LLVM-only options into MSVC ([MSVC known issues, Incompatible functionality, Allocator overrides and C++/CLI](https://raw.githubusercontent.com/MicrosoftDocs/cpp-docs/f29e25fb8f05bb38cf0246476b5c1fc92bf33876/docs/sanitizers/asan-known-issues.md)).

## A real FFI lane

If a fuzz driver calls a prebuilt native decoder, establish the decoder's actual build/interceptor/allocator coverage. Instrumenting the wrapper alone does not check every library load/store. The historical ASan paper explicitly separates compile-time coverage from closed-library handling; the selected runtime must supply the actual coverage evidence ([ASan paper, §5.2](https://www.usenix.org/system/files/conference/atc12/atc12-final39.pdf)). Use the existing native build owner rather than a copied decoder or universal wrapper.

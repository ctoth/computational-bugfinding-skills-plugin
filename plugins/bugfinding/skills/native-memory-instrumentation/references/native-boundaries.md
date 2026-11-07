# Native integration boundaries

## Go and cgo

The pinned Go build documentation describes `-msan` as "Supported only on linux/amd64, linux/arm64, linux/loong64, freebsd/amd64 and only with Clang/LLVM as the host C compiler" and `-asan` as "Supported only on linux/arm64, linux/amd64, linux/loong64" with GCC/Clang version floors; inspect the selected toolchain's own help/source, not the union of a development source and older article. The actual builder prepends `-fsanitize=memory` or `-fsanitize=address` to the cgo CFLAGS and LDFLAGS, which does not rebuild arbitrary precompiled libraries ([Go build flags](https://raw.githubusercontent.com/golang/go/dcc06a82727b447270b1a58cc5f86b49736e317c/src/cmd/go/alldocs.go), [actual cgo producer](https://raw.githubusercontent.com/golang/go/dcc06a82727b447270b1a58cc5f86b49736e317c/src/cmd/go/internal/work/exec.go)).

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

Run the actual produced executable with its workload. The pinned document states "Support is limited to x86 and x64 on Windows 10 and later" and that `/fsanitize=address` "isn't compatible with" edit-and-continue, incremental linking and `/RTC`. Use an appropriate separate diagnostic configuration, retaining the actual compiler/runtime DLL and debug identity; "Debug information is required for optimal formatting of call stacks". `ASAN_SAVE_DUMPS=MyFileName.dmp` can retain supported diagnostic dumps ([MSVC ASan, Build integration and compatibility, Crash dump support, Use AddressSanitizer and Use AddressSanitizer from a developer command prompt](https://raw.githubusercontent.com/MicrosoftDocs/cpp-docs/f29e25fb8f05bb38cf0246476b5c1fc92bf33876/docs/sanitizers/asan.md)).

The implementation has its own boundaries: precompiled headers built without `/fsanitize=address` are unsupported, coroutines' "resumable functions are exempt from instrumentation", and with other `operator new`/`delete` overrides "ASan might not catch some errors". When an ASan DLL is loaded into partly uninstrumented code and later unloaded, there "may be crashes due to dangling references to intercepted functions". C++/CLI support is experimental: such code "isn't guaranteed to receive ASan load and store instrumentation", and reports during finalization, shutdown or mixed-mode unloading "might not reliably indicate user-code memory bugs". Inspect the native translation-unit/DLL producer before attributing a shutdown/unload report to application memory corruption. Do not import arbitrary LLVM-only options into MSVC; "Special case list" files are unsupported ([MSVC known issues, Incompatible options and functionality, Overriding operator new and delete, Issues with partially sanitized executables and ASan support for C++/CLI is experimental](https://raw.githubusercontent.com/MicrosoftDocs/cpp-docs/f29e25fb8f05bb38cf0246476b5c1fc92bf33876/docs/sanitizers/asan-known-issues.md)).

## A real FFI lane

If a fuzz driver calls a prebuilt native decoder, establish the decoder's actual build/interceptor/allocator coverage. Instrumenting the wrapper alone does not check every library load/store. The historical ASan paper says compile-time instrumentation "does not handle system libraries" apart from some C library functions such as `memset`, and proposes binary translation for closed-source libraries; the selected runtime must supply the actual coverage evidence ([ASan paper, §5.2](https://www.usenix.org/system/files/conference/atc12/atc12-final39.pdf)). Use the existing native build owner rather than a copied decoder or universal wrapper.

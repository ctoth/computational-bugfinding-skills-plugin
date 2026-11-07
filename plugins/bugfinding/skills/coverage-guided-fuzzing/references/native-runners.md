# Native runners

These conditional examples assume an existing compatible harness/build. Paths and numbers are illustrative: select actual project files, owned outputs and limits from the budget. Verify the chosen release rather than installing every mode.

## AFL++

Use the project's build integration with the selected AFL++ compiler wrapper on the actual library and driver. The inspected install snapshot says "We recommend llvm 18 or newer, minimum is 14." and that "`afl-clang-lto`, `afl-gcc-fast` and `qemu_mode` are not working on macOS"; its requirements supersede the older compiler diagram in the depth guide (§1.a still names "clang/clang++ 11+"). Linux source-only and binary-only builds have different needs. Check the selected installation before choosing LTO, GCC-plugin, QEMU or FRIDA ([AFL++ selected-ref install](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/docs/INSTALL.md), [AFL++ Fuzzing in Depth §1.a](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/docs/fuzzing_in_depth.md)).

For an already instrumented file consumer:

```sh
afl-fuzz -i seeds -o out -V 300 -t 1000 -m 1024 -- ./target @@
```

Omit `@@` for stdin. `-t` is the "timeout for each run"; `-V` counts "(fuzz time only!)", while outer wall/CPU/setup accounting remains separate. Binary-only `-Q`/QEMU (compiled in only on Linux) and `-O`/FRIDA require their compatible builds; `-n` means "fuzz without instrumentation (non-instrumented mode)", not equivalent coverage guidance ([AFL++ Fuzzing in Depth §2.b](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/docs/fuzzing_in_depth.md), [AFL++ selected-ref CLI source, usage text](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/src/afl-fuzz.c)).

Check what the memory guard measures. `-m` is a "memory limit for child process" with "0 = no limit [default]", and the depth guide notes "unfortunate trade-offs with ASAN and 64-bit binaries" ([AFL++ selected-ref CLI source, usage text](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/src/afl-fuzz.c), [AFL++ Fuzzing in Depth §3.k](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/docs/fuzzing_in_depth.md)). Sanitizer address-space reservations can make a virtual-memory cap inappropriate: AFL++ ships a cgroups limiter "instead of the traditional setrlimit() API" to "avoid the address space problems", and libFuzzer offers `ulimit -v` only "If running w/o ASAN/MSAN" ([AFL++ asan_cgroups limit_memory.sh](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/utils/asan_cgroups/limit_memory.sh), [LLVM libFuzzer, Options](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/llvm/docs/LibFuzzer.md)). Select a supported sanitizer-compatible limit/containment route through `native-memory-instrumentation`; the illustrative `-m` value is not universal.

Persistent mode needs relevant state/resources reset so that "earlier runs will have no impact on future runs". Compare its stability with nonpersistent execution when diagnosing contamination; if stability drops in persistent mode, "then the fuzz target keeps state". Deferred initialization must precede "Any access to the fuzzed input" and must not follow "The creation of any vital threads or child processes". Repair the existing lifecycle owner rather than masking intermittent evidence ([AFL++ persistent mode](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation/README.persistent_mode.md)).

For a measured comparison barrier, a CmpLog experiment uses two semantically matched builds: ordinary instrumentation and a companion compiled with `AFL_LLVM_CMPLOG=1`; `afl-fuzz -c ./target.cmplog ... -- ./target.afl @@` selects it. Do not accidentally compare different target feature configurations. Revisit the memory limit too: "Be careful with the usage of `-m` because CmpLog can map a lot of pages." ([AFL++ CmpLog](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation/README.cmplog.md)).

Custom mutators use `AFL_CUSTOM_MUTATOR_LIBRARY` or `AFL_PYTHON_MODULE`; with `AFL_CUSTOM_MUTATOR_ONLY` "all mutations will solely be performed with the custom mutator". Verify the selected ABI and trimming, since generic trimming "can easily destroy the structure of complex formats"; C/C++ growth of returned buffers must use `afl_realloc()`, "otherwise afl-fuzz will crash when trying to free your buffers". A mutator crash is not automatically a target failure ([AFL++ custom mutators](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/docs/custom_mutators.md)).

The inspected ref's combined project/`afl-fuzz` license is AGPL-3.0-or-later, with individually marked Apache-2.0 files and separately licensed components; "Each file declares its own license in its `SPDX-License-Identifier` header". Check the actual selected files/release; don't reuse an older blanket Apache label ([AFL++ selected-ref licensing](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/LICENSING.md)).

## libFuzzer

Use matching Clang. Instrument the real target translation units, not just argument decoding; "LibFuzzer requires a matching version of Clang", and "`-fsanitize=fuzzer` links in the libFuzzer's `main()` symbol", so `fuzzer-no-link` separates instrumentation from final driver linking when the project has other mains ([LLVM libFuzzer, Versions and Fuzzer Usage](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/llvm/docs/LibFuzzer.md)). An example for actual source files:

```sh
clang++ -g -O1 -fsanitize=fuzzer,address harness.cc target.cc -o fuzz_target
./fuzz_target corpus -max_total_time=300 -timeout=5 -rss_limit_mb=1024 -artifact_prefix=artifacts/
./fuzz_target saved-case
```

The last command replays without search: given files, libFuzzer "will re-run those files as test inputs but will not perform any fuzzing". The engine "will execute the fuzz target many times with different inputs in the same process", so calls require relevant reset, tolerated malformed input and joined work; "It must not `exit()` on any input." Returning -1 excludes corpus admission "regardless of what coverage it triggers". Treat `cov`, features, corpus size, executions/sec and RSS as different observations. Use dictionaries/value profiles/custom mutation only for fitting barriers. Exact artifact paths must not collide across processes. Status says "please do not expect major new features" beyond bug fixes; this doesn't require migrating a working lane ([LLVM libFuzzer, Fuzz Target, Options, Output, Rejecting unwanted inputs, Status](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/llvm/docs/LibFuzzer.md)).

LLVM's license is Apache-2.0 with LLVM exceptions. Sanitizer choice and its supported build belong to `native-memory-instrumentation`, not a universal combination of every sanitizer ([LLVM license](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/LICENSE.TXT)).

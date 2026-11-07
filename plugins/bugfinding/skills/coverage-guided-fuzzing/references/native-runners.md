# Native runners

These conditional examples assume an existing compatible harness/build. Paths and numbers are illustrative: select actual project files, owned outputs and limits from the budget. Verify the chosen release rather than installing every mode.

## AFL++

Use the project's build integration with the selected AFL++ compiler wrapper on the actual library and driver. The inspected install snapshot requires LLVM 14+, recommends 18+, and documents macOS mode restrictions; its requirements supersede the older compiler diagram. Linux source-only and binary-only builds have different needs. Check the selected installation before choosing LTO, GCC-plugin, QEMU or FRIDA ([AFL++ selected-ref install](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/docs/INSTALL.md), [AFL++ Fuzzing in Depth](https://aflplus.plus/docs/fuzzing_in_depth/)).

For an already instrumented file consumer:

```sh
afl-fuzz -i seeds -o out -V 300 -t 1000 -m 1024 -- ./target @@
```

Omit `@@` for stdin. `-t` is an input limit; `-V` counts fuzz time, while outer wall/CPU/setup accounting remains separate. Binary-only `-Q`/QEMU and `-O`/FRIDA require their compatible builds; `-n` is noninstrumented execution, not equivalent coverage guidance ([AFL++ Fuzzing in Depth](https://aflplus.plus/docs/fuzzing_in_depth/), [AFL++ selected-ref CLI source](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/src/afl-fuzz.c)).

Check what the memory guard measures: sanitizer address-space reservations can make a virtual-memory cap inappropriate. Select a supported sanitizer-compatible limit/containment route through `native-memory-instrumentation`; the illustrative `-m` value is not universal ([AFL++ memory limits](https://aflplus.plus/docs/fuzzing_in_depth/)).

Persistent mode needs relevant state/resources reset. Compare its stability with nonpersistent execution when diagnosing contamination; deferred initialization must precede input reads and avoid invalid forkserver placement after critical threads. Repair the existing lifecycle owner rather than masking intermittent evidence ([AFL++ persistent mode](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation/README.persistent_mode.md)).

For a measured comparison barrier, a CmpLog experiment uses two semantically matched builds: ordinary instrumentation and a companion compiled with `AFL_LLVM_CMPLOG=1`; `afl-fuzz -c ./target.cmplog ... -- ./target.afl @@` selects it. Do not accidentally compare different target feature configurations ([AFL++ CmpLog](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation/README.cmplog.md)).

Custom mutators use `AFL_CUSTOM_MUTATOR_LIBRARY` or `AFL_PYTHON_MODULE`; `AFL_CUSTOM_MUTATOR_ONLY` disables other mutation stages. Verify the selected ABI and trimming; C/C++ growth of returned buffers must use its documented `afl_realloc` contract. A mutator crash is not automatically a target failure ([AFL++ custom mutators](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/docs/custom_mutators.md)).

The inspected ref's combined project/`afl-fuzz` license is AGPL-3.0-or-later, with individually marked Apache-2.0 files and separately licensed components. Check the actual selected files/release; don't reuse an older blanket Apache label ([AFL++ selected-ref licensing](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/LICENSING.md)).

## libFuzzer

Use matching Clang. Instrument the real target translation units, not just argument decoding; `fuzzer-no-link` separates instrumentation from final driver linking when the project has other mains. An example for actual source files:

```sh
clang++ -g -O1 -fsanitize=fuzzer,address harness.cc target.cc -o fuzz_target
./fuzz_target corpus -max_total_time=300 -timeout=5 -rss_limit_mb=1024 -artifact_prefix=artifacts/
./fuzz_target saved-case
```

The last command replays without search. Same-process calls require relevant reset, tolerated malformed input and joined work. Returning -1 excludes corpus admission. Treat `cov`, features, corpus size, executions/sec and RSS as different observations. Use dictionaries/value profiles/custom mutation only for fitting barriers. Exact artifact paths must not collide across processes. Status currently promises important fixes, not major feature work; this doesn't require migrating a working lane ([LLVM libFuzzer](https://llvm.org/docs/LibFuzzer.html)).

LLVM's license is Apache-2.0 with LLVM exceptions. Sanitizer choice and its supported build belong to `native-memory-instrumentation`, not a universal combination of every sanitizer ([LLVM license](https://raw.githubusercontent.com/llvm/llvm-project/main/LICENSE.TXT)).

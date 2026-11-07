# Native race observers

## Clang ThreadSanitizer

Select a supported target/compiler/runtime and instrument the real library as well as its driver. Source-derived, unexecuted build shape:

```text
clang++ -g -O1 -fsanitize=thread harness.cc target.cc -o race_target
```

The pinned docs list supported platforms, debug/optimization guidance and limitations: for code not built with the flag, "TSan may fail to detect races or may report false positives"; ignorelisted functions "are not instrumented at all", unlike `no_sanitize("thread")` functions, so the two remove different evidence. "Libc/libstdc++ static linking is not supported", and TSan "maps (but does not reserve) a lot of virtual address space", so `ulimit`-style caps mislead ([TSan usage/limitations](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/clang/docs/ThreadSanitizer.md)). LLVM's selected license is Apache-2.0 with LLVM exceptions ([LICENSE](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/LICENSE.TXT)). These source pins do not identify an installed runtime.

Keep full symbolized reports and relevant runtime options. `memory_limit_mb` is a "Resident memory limit in MB to aim at" that makes TSan "flush shadow memory"; it is not a hard process cap. `force_seq_cst_atomics` makes atomics "effectively sequentially consistent (seq_cst), regardless of what user actually specified" and is not a production fix. `suppress_equal_stacks` defaults to true, so a repeated stack is not re-reported and report counts are not occurrence counts ([runtime flags](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/compiler-rt/lib/tsan/rtl/tsan_flags.inc)). The documented defaults `exitcode` 66 and `history_size` 0 matter for result classification and for "failed to restore the stack" reports; `ignore_noninstrumented_modules` changes which interceptor calls are observed ([TSan Run-time Flags](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/clang/docs/ThreadSanitizer.md)).

### Optional perturbation in a verified runtime

When actual runtime help/source exposes it and the lifecycle path is reached, pilot this POSIX environment form with chosen outer resource limits:

```text
TSAN_OPTIONS=enable_adaptive_delay=1 ./race_target
```

"Adaptive delay is disabled by default"; it injects delays at synchronization points, atomics and thread lifecycle operations within a time budget, and its aggressiveness "is a tuning parameter; actual overhead varies by workload and platform" ([Adaptive Delay](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/clang/docs/ThreadSanitizer.md), [flags](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/compiler-rt/lib/tsan/rtl/tsan_flags.inc)). Initialization is guarded by `!SANITIZER_GO`; this is not a promised Go `GORACE` feature ([runtime initialization](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/compiler-rt/lib/tsan/rtl/tsan_rtl.cpp)). The implementation seeds from time, so retain workload and actual replay results rather than promise deterministic scheduling ([seed initialization](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/compiler-rt/lib/tsan/rtl/tsan_adaptive_delay.cpp)).

## Helgrind

For an existing compatible pthread binary with debug information, a conditional unexecuted route is:

```text
valgrind --tool=helgrind --history-level=full --error-exitcode=99 --log-file=helgrind.%p.log ./native_target ARGS
```

Helgrind observes pthread synchronization, reports API misuse/races/potential lock-order problems, and "works best when your application uses only the POSIX pthreads API"; custom primitives need the `ANNOTATE_*` macros. `--history-level=full` is the default (the command makes it explicit for the record): it keeps the older conflicting stack but is "expensive in both speed and memory", and old-access stacks live in an LRU cache bounded by `--conflict-cache-size`. For use/free lifecycle races, `--free-is-write=yes` (default `no`, described as experimental) "treats freeing of heap memory as if the memory was written immediately before the free" ([manual §§7.1–7.6](https://valgrind.org/docs/manual/hg-manual.html)). With the default `--error-exitcode=0`, "the return value from Valgrind will always be the return value of the process being simulated"; an explicit nonzero error code and per-process `%p` logs serve a different purpose from the workload oracle. `--trace-children` defaults to `no`, so exec'd children are untraced unless enabled ([core options](https://valgrind.org/docs/manual/manual-core.html)).

Verify selected executable/ISA support rather than assume native Windows or every architecture: the observed "Release 3.28.0 (23 Oct 2026)" platform list names Linux, Android, Solaris, macOS and FreeBSD targets, not Windows, and "macOS is supported up to version 13 Ventura (amd64 only)" ([release notes](https://valgrind.org/docs/manual/dist.news.html)). Valgrind calls itself "a GPL'd system"; no more precise whole-tool license conclusion is established here ([About](https://valgrind.org/info/about.html)).

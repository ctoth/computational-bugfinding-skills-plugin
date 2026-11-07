# Native race observers

## Clang ThreadSanitizer

Select a supported target/compiler/runtime and instrument the real library as well as its driver. Source-derived, unexecuted build shape:

```text
clang++ -g -O1 -fsanitize=thread harness.cc target.cc -o race_target
```

The pinned docs list supported platforms, debug/optimization guidance and limitations: noninstrumented modules can hide races or synchronization; ignorelists and instrumentation-disabling attributes remove different evidence. Static libc/libstdc++ linkage is unsupported, and large shadow mappings make virtual-memory caps misleading ([TSan usage/limitations](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/clang/docs/ThreadSanitizer.md)). LLVM's selected license is Apache-2.0 with LLVM exceptions ([LICENSE](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/LICENSE.TXT)). These source pins do not identify an installed runtime.

Keep full symbolized reports and relevant runtime options. `memory_limit_mb` can flush shadow memory to aim at a target; it is not a hard process cap. `force_seq_cst_atomics` changes effective atomic ordering and is not a production fix ([runtime flags](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/compiler-rt/lib/tsan/rtl/tsan_flags.inc)).

### Optional perturbation in a verified runtime

When actual runtime help/source exposes it and the lifecycle path is reached, pilot this POSIX environment form with chosen outer resource limits:

```text
TSAN_OPTIONS=enable_adaptive_delay=1 ./race_target
```

The inspected feature is off by default and perturbs synchronization/lifecycle timing; its overhead tuning is workload-dependent ([Adaptive Delay](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/clang/docs/ThreadSanitizer.md), [flags](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/compiler-rt/lib/tsan/rtl/tsan_flags.inc)). Initialization is guarded by `!SANITIZER_GO`; this is not a promised Go `GORACE` feature ([runtime initialization](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/compiler-rt/lib/tsan/rtl/tsan_rtl.cpp)). The implementation seeds from time, so retain workload and actual replay results rather than promise deterministic scheduling ([seed initialization](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/compiler-rt/lib/tsan/rtl/tsan_adaptive_delay.cpp)).

## Helgrind

For an existing compatible pthread binary with debug information, a conditional unexecuted route is:

```text
valgrind --tool=helgrind --history-level=full --error-exitcode=99 --log-file=helgrind.%p.log ./native_target ARGS
```

Helgrind observes pthread synchronization, reports API misuse/races/potential lock-order problems, and needs accurate annotations for custom primitives. Full history helps retain the earlier conflicting stack but costs resources and has bounded caches ([manual §§7.1–7.6](https://valgrind.org/docs/manual/hg-manual.html)). Default error exit behavior can preserve target success despite reports; an explicit nonzero error code and per-process logs serve a different purpose from the workload oracle. Check child tracing when relevant ([core options](https://valgrind.org/docs/manual/manual-core.html)).

Verify selected executable/ISA support rather than assume native Windows or every architecture; the observed release notes identify3.28.0,23Oct2026 ([release notes](https://valgrind.org/docs/manual/dist.news.html)). Valgrind declares GPL licensing; no more precise whole-tool license conclusion is established here ([About](https://valgrind.org/info/about.html)).

---
name: race-detection-campaigns
description: Guides race-detector campaigns that search real shared-memory and object-lifecycle interactions. Use when existing race tests miss relevant accesses, designing concurrent workloads, checking instrumentation boundaries, or interpreting Go race, native ThreadSanitizer or Helgrind evidence.
---

# Race-detection campaigns

Choose a real sharing or lifetime interaction, then make a fitting detector observe it. Go's detector covers executed paths ("it can't find races in code paths that are not executed"); the original TSan study shows why initialization, publication and reference-count lifetimes matter beyond a downstream crash ([Go guide, How to Use](https://raw.githubusercontent.com/golang/website/a8b66266e226994e2ead51317bace3ee83cedab9/_content/doc/articles/race_detector.html), [TSan 2009, §§6.3–7.1, pp.67–69](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/35604.pdf)).

## Build an informative lane

Read the actual create/publish/use/reload/cancel/close producer and its enabled configuration. Select a legal sequence that overlaps the relevant accesses to the same live object. Coordinate the test phase without locking the whole target operation: excessive synchronization "may hide real races from data race detectors" ([workload design](references/race-workloads.md), [TSan 2009, §6.5, p.69](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/35604.pdf)). Use `stateful-property-testing` for dependent operations.

Verify the selected executable's instrumentation, build exclusions, native modules, plugins and synchronization model. For uninstrumented code, Clang's docs say "TSan may fail to detect races or may report false positives"; Go's plugin package warns "Even simple race conditions may not be automatically detected" ([Clang TSan, Limitations](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/clang/docs/ThreadSanitizer.md), [Go plugin warnings](https://raw.githubusercontent.com/golang/go/dcc06a82727b447270b1a58cc5f86b49736e317c/src/plugin/plugin.go)). Do not infer end-to-end coverage from a race-enabled driver.

Read only the applicable route:
- [Go runtime](references/go-runtime.md): selected toolchain, ordinary test workloads, plugin/cgo boundaries and diagnostic costs.
- [Native runtime](references/native-runtime.md): Clang TSan, conditional adaptive delay and Helgrind.

JavaScript boundary: within one agent "Only one Job may be actively undergoing evaluation at any point in time", and the memory model's data races are defined only over Shared Data Block events, the memory behind `SharedArrayBuffer` and `Atomics` ([ECMA-262, Jobs and Memory Model](https://raw.githubusercontent.com/tc39/ecma262/828d35d00f8584c4a0fbcac7742b57c7b959c3f3/spec.html)). Node worker threads "can share memory" by "sharing `SharedArrayBuffer` instances" ([Node v26.13.0 worker_threads](https://raw.githubusercontent.com/nodejs/node/v26.13.0/doc/api/worker_threads.md)). Route Node, browser and React event or promise ordering races to `schedule-exploration`. For `SharedArrayBuffer` shared across workers this pack has no verified detector; a bounded search found none.

Use an existing representative faulty and healthy case to establish the claimed access observer through the same producer; `harness-sensitivity` owns control design. A detector "must understand the synchronization mechanisms used by the tested program", not merely a compiled test ([TSan 2009, §5, pp.65–66](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/35604.pdf)).

## Spend compute on an omitted interaction

Pilot a small meaningful lifecycle workload; then vary actors, shared identities, operation sequences and lifecycle phases against measured reach and cost. Repeated test runs and Go `-cpu` settings (a "list of GOMAXPROCS values") vary ordinary execution; they do not enumerate schedules, and "-cpu does not apply to fuzz tests matched by -fuzz" ([Go 1.27.3 testing flags](https://pkg.go.dev/cmd/go@go1.27.3#hdr-Testing_flags)). Use `schedule-exploration` for controlled choices.

For a compatible native runtime, adaptive delay is a separate experiment, not a Go option or a deterministic replay mechanism ([flags](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/compiler-rt/lib/tsan/rtl/tsan_flags.inc), [Go exclusion](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/compiler-rt/lib/tsan/rtl/tsan_rtl.cpp), [time-derived seed](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/compiler-rt/lib/tsan/rtl/tsan_adaptive_delay.cpp)). Preserve actual workload and results rather than promise same-seed replay.

Track completed operations, relevant lifecycle/access contexts, raw reports, unresolved cases and resource cost. Detector memory/history choices change observation; Go's guide puts typical cost at "memory usage may increase by 5-10x and execution time by 2-20x", so diagnose instrumentation overhead separately from target leaks or hangs ([Go overhead](https://raw.githubusercontent.com/golang/website/a8b66266e226994e2ead51317bace3ee83cedab9/_content/doc/articles/race_detector.html), [TSan runtime flags](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/compiler-rt/lib/tsan/rtl/tsan_flags.inc)). Use `bugfinding-campaign` for allocation and `resource-complexity-testing`/`liveness-testing` for those guarantees.

## Preserve the actual finding

Keep both conflicting-access stacks, creation/lifetime context, input/setup/sequence, binary/module/build/runtime/options, raw output and replay attempts. Helgrind reports lock-order cycles as "a potential deadlock" without observing an actual hang; keep those claims separate ([Helgrind, §§7.3–7.4](https://valgrind.org/docs/manual/hg-manual.html)). Read [evidence and model limits](references/evidence-and-limits.md), then use `failure-reduction` and `evidence-based-triage` for their concerns.

Return the reached interaction, instrumentation/model boundaries, actual resources, finding/replay evidence and untested space. A clean run says nothing about unexecuted paths, and a race observer does not judge logic-dependent correctness: in the original study's flag example, "ThreadSanitizer cannot distinguish between these two cases" ([Go guide, How to Use](https://raw.githubusercontent.com/golang/website/a8b66266e226994e2ead51317bace3ee83cedab9/_content/doc/articles/race_detector.html), [TSan 2009, §4.4.1, pp.64–65](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/35604.pdf)). For misleading shortcuts, read [common mistakes](references/common-mistakes.md). Invocation preserves existing task authority; it does not authorize target changes, installations or external publication.

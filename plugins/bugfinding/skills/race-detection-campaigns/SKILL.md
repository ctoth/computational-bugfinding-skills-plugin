---
name: race-detection-campaigns
description: Guides race-detector campaigns that search real shared-memory and object-lifecycle interactions. Use when existing race tests miss relevant accesses, designing concurrent workloads, checking instrumentation boundaries, or interpreting Go race, native ThreadSanitizer or Helgrind evidence.
---

# Race-detection campaigns

Choose a real sharing or lifetime interaction, then make a fitting detector observe it. Go's detector covers executed paths; the original TSan study shows why initialization, publication and reference-count lifetimes matter beyond a downstream crash ([Go guide, How to Use](https://raw.githubusercontent.com/golang/website/a8b66266e226994e2ead51317bace3ee83cedab9/_content/doc/articles/race_detector.html), [TSan 2009, §§6.3–7.1, pp.67–69](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/35604.pdf)).

## Build an informative lane

Read the actual create/publish/use/reload/cancel/close producer and its enabled configuration. Select a legal sequence that overlaps the relevant accesses to the same live object. Coordinate the test phase without locking the whole target operation: excessive synchronization can hide races ([workload design](references/race-workloads.md), [TSan 2009, §6.5, p.69](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/35604.pdf)). Use `stateful-property-testing` for dependent operations.

Verify the selected executable's instrumentation, build exclusions, native modules, plugins and synchronization model. Native TSan documents missed races and false reports when code is uninstrumented; Go's plugin package explicitly warns about missed races ([Clang limitations](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/clang/docs/ThreadSanitizer.md), [Go plugin warnings](https://raw.githubusercontent.com/golang/go/dcc06a82727b447270b1a58cc5f86b49736e317c/src/plugin/plugin.go)). Do not infer end-to-end coverage from a race-enabled driver.

Read only the applicable route:
- [Go runtime](references/go-runtime.md): selected toolchain, ordinary test workloads, plugin/cgo boundaries and diagnostic costs.
- [Native runtime](references/native-runtime.md): Clang TSan, conditional adaptive delay and Helgrind.

Use an existing representative faulty and healthy case to establish the claimed access observer through the same producer; `harness-sensitivity` owns control design. A detector requires knowledge of the program's synchronization, not merely a compiled test ([TSan 2009, §5, pp.65–66](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/35604.pdf)).

## Spend compute on an omitted interaction

Pilot a small meaningful lifecycle workload; then vary actors, shared identities, operation sequences and lifecycle phases against measured reach and cost. Repeated test runs and Go `-cpu` settings vary ordinary execution; they do not enumerate schedules, and `-cpu` does not apply to fuzz discovery ([Go 1.27.3 testing flags](https://pkg.go.dev/cmd/go@go1.27.3#hdr-Testing_flags)). Use `schedule-exploration` for controlled choices.

For a compatible native runtime, adaptive delay is a separate experiment, not a Go option or a deterministic replay mechanism ([flags](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/compiler-rt/lib/tsan/rtl/tsan_flags.inc), [Go exclusion](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/compiler-rt/lib/tsan/rtl/tsan_rtl.cpp), [time-derived seed](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/compiler-rt/lib/tsan/rtl/tsan_adaptive_delay.cpp)). Preserve actual workload and results rather than promise same-seed replay.

Track completed operations, relevant lifecycle/access contexts, raw reports, unresolved cases and resource cost. Detector memory/history choices change observation; diagnose instrumentation overhead separately from target leaks or hangs ([Go overhead](https://raw.githubusercontent.com/golang/website/a8b66266e226994e2ead51317bace3ee83cedab9/_content/doc/articles/race_detector.html), [TSan runtime flags](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/compiler-rt/lib/tsan/rtl/tsan_flags.inc)). Use `bugfinding-campaign` for allocation and `resource-complexity-testing`/`liveness-testing` for those guarantees.

## Preserve the actual finding

Keep both conflicting-access stacks, creation/lifetime context, input/setup/sequence, binary/module/build/runtime/options, raw output and replay attempts. Helgrind can report a potential lock-order deadlock without observing an actual hang; keep those claims separate ([Helgrind, §§7.3–7.4](https://valgrind.org/docs/manual/hg-manual.html)). Read [evidence and model limits](references/evidence-and-limits.md), then use `failure-reduction` and `evidence-based-triage` for their concerns.

Return the reached interaction, instrumentation/model boundaries, actual resources, finding/replay evidence and untested space. A clean run says nothing about unexecuted paths; a race observer does not supply an abstract object-history oracle ([Go guide, How to Use](https://raw.githubusercontent.com/golang/website/a8b66266e226994e2ead51317bace3ee83cedab9/_content/doc/articles/race_detector.html), [TSan 2009, §4.4.1, pp.64–65](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/35604.pdf)). For misleading shortcuts, read [common mistakes](references/common-mistakes.md). Invocation preserves existing task authority; it does not authorize target changes, installations or external publication.

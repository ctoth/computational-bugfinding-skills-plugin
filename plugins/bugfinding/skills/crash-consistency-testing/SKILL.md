---
name: crash-consistency-testing
description: Searches persistence and recovery boundaries for lost acknowledged data, torn state and incorrect error handling. Use when testing durability across crashes, storage faults, flushes, replacement or restart.
---

# Crash consistency testing

Choose a real acknowledgment and a fault model, then test the allowed recovered states. A completed round trip is a different experiment: CrashMonkey records writes, constructs crash images and checks recovered persisted objects: "only files and directories explicitly persisted" at a checkpoint are compared ([Mohan et al., §5.1, pp.7-8](https://www.cs.utexas.edu/~vijay/papers/osdi18-crashmonkey.pdf)).

## Establish the promise and observation

Read the actual caller, enabled durability mode, storage path and recovery entrypoint. Derive which acknowledged effects must survive, which pending effects may survive, and which partial states are forbidden. Linux file sync and directory-entry persistence are separate: `fsync()` "does not necessarily ensure that the entry in the directory" reached disk ([fsync, DESCRIPTION](https://man7.org/linux/man-pages/man2/fsync.2.html)). Atomic replacement is specified against "another process attempting to access newpath", which does not itself specify crash durability ([rename, DESCRIPTION](https://man7.org/linux/man-pages/man2/rename.2.html)). Work through [recovered-state oracles](references/recovered-state-oracles.md).

Select the smallest fitting existing route: a recorded process failure, a compatible filesystem crash harness, an application-facing fault filesystem, or an existing VFS seam. Keep process, kernel-cache, modeled-storage and real-device failure domains distinct; the paper's replayed crash state is not a process termination: "The crash state represents the state of storage" after a completed persistence operation ([Mohan et al., §5.1](https://www.cs.utexas.edu/~vijay/papers/osdi18-crashmonkey.pdf)). Read [fault routes](references/fault-routes.md) or [Pebble VFS operation](references/pebble-vfs.md) only when applicable.

## Search an actual failure boundary

Establish healthy recovery and representative forbidden-state sensitivity through the same producer and oracle; reuse the project's controls and `harness-sensitivity`. Then vary initial state, dependent operation sequences, persistence placement and the selected model's crash/error choices. Ace is "a bounded, and exhaustive workload generator" whose Workload Adapter is separate from generation, so bounded coverage depends on its declared operation and argument space ([Ace, Overview and bounds](https://raw.githubusercontent.com/utsaslab/crashmonkey/27ca57f8cf2760d5d4855e03b8d01f8e5de1628c/docs/Ace.md)).

Retain the requested fault and evidence it actually hit/completed before interpreting recovery. LazyFS exposes a separate completion FIFO so a reader "waits before making any post-fault consistency checks"; Pebble's `MaybeError` "is invoked by an errorfs before an operation is executed", which does not model partial completion ([LazyFS, Running and Injecting faults](https://raw.githubusercontent.com/dsrhaslab/lazyfs/d93e54a7944b28e86506d2af3a97342f5c3eb21f/README.md), [errorfs, Injector](https://raw.githubusercontent.com/cockroachdb/pebble/a995e890c06ef86c583927906e16e7f313083a3f/vfs/errorfs/errorfs.go)). Do not count an injector miss or unsupported setup as a tested durability guarantee.

Recover using the actual startup path, observe the promised data/metadata and perform a meaningful subsequent operation. Mountability or fsck alone misses data-loss cases: fsck "does not detect the loss or corruption of user data", so CrashMonkey runs it only on an unmountable image and checks recovered objects with *read* and *write* checks ([Mohan et al., §§4.3 and 5.1, pp.6-8](https://www.cs.utexas.edu/~vijay/papers/osdi18-crashmonkey.pdf)). Preserve unavailable recovery as unresolved evidence.

## Retain the counterexample

Save acknowledgment/operation order, starting image/state, selected fault boundary and hit evidence, persisted subset or write pieces, exact build/OS/filesystem/model settings, recovery inputs and raw recovered observations. The workload/checkpoint and replay state are explicit parts of CrashMonkey's reproducer: its log holds the recorded block IOs, "the crash states tested and result at each crash state" ([workload interface and Result](https://raw.githubusercontent.com/utsaslab/crashmonkey/27ca57f8cf2760d5d4855e03b8d01f8e5de1628c/docs/workload.md)).

Reduce state, operations and fault choices together while retaining the same forbidden recovered effect; keep the original. Read [worked oracle reductions](references/recovered-state-oracles.md), then use `failure-reduction` and `evidence-based-triage` for their mechanics. Report the tested promise, fault model, real violation or inconclusive outcome, actual resources and unsearched bounds. Bounded crash testing does not cover every crash mechanism; the authors call B3 "sound but incomplete" and exclude mid-operation crashes and I/O reordering ([Mohan et al., §4.4](https://www.cs.utexas.edu/~vijay/papers/osdi18-crashmonkey.pdf)). Read [common mistakes](references/common-mistakes.md) for misleading passes.

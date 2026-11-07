# Common mistakes

Each entry is WRONG first, then RIGHT, then why.

## Treating file sync as directory-entry durability

**Wrong:** Treat a successful `fsync()` on a new or renamed file as proof its directory entry survives a crash.

**Right:** Trace the directory persistence promise and actual call/error path. `fsync()` "does not necessarily ensure that the entry in the directory" has reached disk; that needs "an explicit fsync() on a file descriptor for the directory" ([fsync DESCRIPTION](https://man7.org/linux/man-pages/man2/fsync.2.html)).

**Why:** the file's data can be durable while its name is lost, so the acknowledged file disappears after recovery.

## Treating atomic rename as power-loss-safe replacement

**Wrong:** Claim atomic rename proves power-loss-safe replacement.

**Right:** Separate live visibility from the target's recovery guarantee. rename's atomicity is stated for "another process attempting to access newpath" ([rename DESCRIPTION](https://man7.org/linux/man-pages/man2/rename.2.html)); directory-entry persistence still needs the directory sync above ([fsync DESCRIPTION](https://man7.org/linux/man-pages/man2/fsync.2.html)).

**Why:** a live-process guarantee says nothing about which name a recovered filesystem holds.

## Using mountability or fsck as the data oracle

**Wrong:** Use mountability or fsck as the full data oracle.

**Right:** Check promised persisted objects and continued operations. fsck "does not detect the loss or corruption of user data"; CrashMonkey runs it only when the image is unmountable and otherwise uses *read* and *write* checks ([CrashMonkey paper §5.1, p.8](https://www.cs.utexas.edu/~vijay/papers/osdi18-crashmonkey.pdf)).

**Why:** a mountable, fsck-clean image can still have lost or corrupted acknowledged data.

## Counting a fault command as a completed crash or loss

**Wrong:** Count a fault command written to the FIFO as a completed crash/loss.

**Right:** Retain actual activation and wait for the configured completion event: with `fifo_path_completed`, LazyFS writes `finished::clear-cache` so a reader "waits before making any post-fault consistency checks" ([LazyFS README, Running and Injecting faults](https://raw.githubusercontent.com/dsrhaslab/lazyfs/d93e54a7944b28e86506d2af3a97342f5c3eb21f/README.md)).

**Why:** checks that run before the fault completes test the pre-fault state and report a false pass.

## Building the crash clone from the stale comment

**Wrong:** Build `CrashCloneCfg{Probability: 50}` from the stale `NewCrashableMem` doc comment.

**Right:** Use the real `UnsyncedDataPercent` field; "RNG must be set if UnsyncedDataPercent > 0" ([mem_fs.go CrashCloneCfg](https://raw.githubusercontent.com/cockroachdb/pebble/a995e890c06ef86c583927906e16e7f313083a3f/vfs/mem_fs.go)).

**Why:** the struct has no `Probability` field, so the example does not compile against the inspected source.

## Closing cleanly before capturing the crash state

**Wrong:** Close cleanly, then capture the alleged crash state.

**Right:** Snapshot first, as the real restart caller does: `restartDB` calls `fs.CrashClone(...)` before `db.Close()` ([metamorphic restartDB](https://raw.githubusercontent.com/cockroachdb/pebble/a995e890c06ef86c583927906e16e7f313083a3f/metamorphic/test.go)).

**Why:** `db.Close()` "will finish any ongoing background flushes, compactions", which makes a state captured afterwards stronger than a crash would leave ([mem_fs.go NewCrashableMem](https://raw.githubusercontent.com/cockroachdb/pebble/a995e890c06ef86c583927906e16e7f313083a3f/vfs/mem_fs.go)).

## Reading pre-operation injected errors as partial-write coverage

**Wrong:** Interpret pre-operation injected errors as partial-write coverage.

**Right:** Preserve the actual no-effect injection boundary: `MaybeError` "is invoked by an errorfs before an operation is executed", and an injected `Write` error returns `0, err` without calling the wrapped file ([errorfs Injector](https://raw.githubusercontent.com/cockroachdb/pebble/a995e890c06ef86c583927906e16e7f313083a3f/vfs/errorfs/errorfs.go)).

**Why:** no bytes reach the model, so torn or post-effect failures remain untested.

## Inverting `-P` or copying a host device from an example

**Wrong:** Read `-P` as enabling permutation, or copy `-f /dev/sda` from the [documented example](https://raw.githubusercontent.com/utsaslab/crashmonkey/27ca57f8cf2760d5d4855e03b8d01f8e5de1628c/docs/workload.md).

**Right:** `-P` is `no-permuted-order-replay`; resolve actual owned virtual-device arguments, since `-f` and `-d` default to `/dev/vda` and `/dev/ram0` ([CLI options](https://raw.githubusercontent.com/utsaslab/crashmonkey/27ca57f8cf2760d5d4855e03b8d01f8e5de1628c/code/harness/c_harness.cpp)).

**Why:** the wrong replay mode changes which crash states are tested, and a wrong device argument points the harness at a disk it does not own.

## Calling a bounded workload set every possible crash

**Wrong:** Call a small bounded workload set every possible crash.

**Right:** State operation/argument/fault bounds and omissions. Ace documents that only "sequences of length up to 3 have been tested" ([Ace, Bounds used by Ace](https://raw.githubusercontent.com/utsaslab/crashmonkey/27ca57f8cf2760d5d4855e03b8d01f8e5de1628c/docs/Ace.md)); the paper calls B3 "sound but incomplete" ([paper §4.4](https://www.cs.utexas.edu/~vijay/papers/osdi18-crashmonkey.pdf)).

**Why:** bugs outside the declared bounds, mid-operation crashes and I/O reordering are not searched.

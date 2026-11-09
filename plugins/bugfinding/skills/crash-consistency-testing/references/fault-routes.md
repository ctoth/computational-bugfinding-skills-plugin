# Fault routes

Choose an existing route whose modeled failure matches the promised guarantee. Source pins below identify inspected evidence; verify the selected installed build and its actual help before a run.

JavaScript: a Node service writing files uses the process-failure and LazyFS routes below. No fault tool for browser storage was found, and IndexedDB's `"strict"` durability only says the user agent "may consider" a transaction committed after writing to "a persistent storage medium" ([IndexedDB specification source](https://raw.githubusercontent.com/w3c/IndexedDB/f9f83f196f8501429282ff1747ebcbe35d41381a/index.bs)).

## Process failure

Terminate only the authorized disposable target process at a recorded boundary and reopen through production recovery. Call this process-crash recovery: storage/kernel caches and completed persistence remain distinct, because `fsync()` is what transfers "all modified in-core data" to the device, unlike replaying a selected block image ([fsync DESCRIPTION](https://man7.org/linux/man-pages/man2/fsync.2.html), [CrashMonkey paper §5.1](https://www.cs.utexas.edu/~vijay/papers/osdi18-crashmonkey.pdf)).

## CrashMonkey and Ace

The inspected README lists tested Linux kernels "3.12, 3.13, 3.16, 4.1, 4.4, 4.15, 4.16, 5.5 and 5.6" and recommends "a Ubuntu 16.04 VM"; it does not verify modern-kernel or Windows compatibility. CrashMonkey builds kernel modules and uses test devices ([README, Setup](https://raw.githubusercontent.com/utsaslab/crashmonkey/27ca57f8cf2760d5d4855e03b8d01f8e5de1628c/README.md)). Its selected source carries Apache-2.0 ([LICENSE](https://raw.githubusercontent.com/utsaslab/crashmonkey/27ca57f8cf2760d5d4855e03b8d01f8e5de1628c/LICENSE)).

Use already provisioned owned virtual devices in a disposable compatible VM. For an existing built workload, the documented in-order automatic-check shape is:
```text
./c_harness -v -c -P -f OWNED_FLAG_DEVICE -d OWNED_TEST_DEVICE -t FS_TYPE -e IMAGE_SIZE WORKLOAD.so
```
Substitute actual verified devices/settings. `-P` is `no-permuted-order-replay` and `-c` is `automate_check_test`; without `-P`, `permuted_order_replay = true` by default. The harness falls back to `/dev/vda` and `/dev/ram0` when `-f`/`-d` are omitted. These are device-affecting parameters, not harmless file names ([CLI options](https://raw.githubusercontent.com/utsaslab/crashmonkey/27ca57f8cf2760d5d4855e03b8d01f8e5de1628c/code/harness/c_harness.cpp)). The auto-checker "requires the -P flag to perform in-order replay" ([workload, Test with auto-checker](https://raw.githubusercontent.com/utsaslab/crashmonkey/27ca57f8cf2760d5d4855e03b8d01f8e5de1628c/docs/workload.md)).

In `run`, use the `cm_->Cm*` wrappers (for example `cm_->CmOpen`); CrashMonkey "requires that you wrap `open, close, rename, fsync, fdatasync, sync, msync`" for the auto-checker, and "any persistence operation be followed by a checkpoint"; setup I/O is not recorded ([workload, Interface and Run](https://raw.githubusercontent.com/utsaslab/crashmonkey/27ca57f8cf2760d5d4855e03b8d01f8e5de1628c/docs/workload.md)). For custom checking, set the error on `DataTestResult` "to communicate the bug type and a status string", not only the C++ return value; retain checkpoint, BIO log, recovered state and diff ([workload, Check_Test and Result](https://raw.githubusercontent.com/utsaslab/crashmonkey/27ca57f8cf2760d5d4855e03b8d01f8e5de1628c/docs/workload.md)). Reuse a saved profile with `-r` only "As long as the bio sequence during profiling does not change" ([CrashMonkey.md](https://raw.githubusercontent.com/utsaslab/crashmonkey/27ca57f8cf2760d5d4855e03b8d01f8e5de1628c/docs/CrashMonkey.md)). Ace generates bounded high-level workloads and translates them through a Workload Adapter ([Ace](https://raw.githubusercontent.com/utsaslab/crashmonkey/27ca57f8cf2760d5d4855e03b8d01f8e5de1628c/docs/Ace.md)).

## LazyFS

The selected prototype documents C++17/FUSE3 and was "tested with ext4 (with the default mount options)" on Debian 11 and Ubuntu 20.04; these are evidence limits, not current host compatibility. Configure the relevant application paths through the model and retain cache policy, exact fault occurrence and persisted pieces ([README](https://raw.githubusercontent.com/dsrhaslab/lazyfs/d93e54a7944b28e86506d2af3a97342f5c3eb21f/README.md)). Its LICENSE file says "Licensed under the terms of MIT License" ([LICENSE](https://raw.githubusercontent.com/dsrhaslab/lazyfs/d93e54a7944b28e86506d2af3a97342f5c3eb21f/LICENSE)).

For an existing fitting build and owned mount/backing paths, the script accepts:
```text
./scripts/mount-lazyfs.sh -c CONFIG -m OWNED_MOUNT -r OWNED_BACKING -f -s
```
The script passes `-o allow_other` and unquoted `$MOUNT_DIR`/`$ROOT_DIR` expansions: inspect actual FUSE prerequisites and path handling instead of assuming arbitrary host setup or whitespace-safe arguments ([script](https://raw.githubusercontent.com/dsrhaslab/lazyfs/d93e54a7944b28e86506d2af3a97342f5c3eb21f/lazyfs/scripts/mount-lazyfs.sh)).

For explicit unsynced-loss experiments, record `apply_eviction=false` under `[cache]`; `true` means the cache should "behave like the real page cache" and evict when full. Send the literal `lazyfs::clear-cache` through the existing configured control owner; await `finished::clear-cache` on `fifo_path_completed` before post-fault checks. Torn-sequence and torn-operation modes retain selected writes/pieces, then "LazyFS will crash". Retain the fault acknowledgment, which "is sent to `stdout` or to the `logfile`"; after a LazyFS crash "the mount directory may be left in an undefined state" until `fusermount -uz` ([README, Running and Injecting faults](https://raw.githubusercontent.com/dsrhaslab/lazyfs/d93e54a7944b28e86506d2af3a97342f5c3eb21f/README.md)). The implementation's crash trigger is `kill (lazyfs_pid, SIGKILL)` on its own `getpid ()`; it is not proof the application or hardware also crashed ([trigger_crash_fault](https://raw.githubusercontent.com/dsrhaslab/lazyfs/d93e54a7944b28e86506d2af3a97342f5c3eb21f/lazyfs/src/lazyfs.cpp)). Check bypassed I/O and metadata semantics before extending the claimed fault domain.

# Fault routes

Choose an existing route whose modeled failure matches the promised guarantee. Source pins below identify inspected evidence; verify the selected installed build and its actual help before a run.

## Process failure

Terminate only the authorized disposable target process at a recorded boundary and reopen through production recovery. Call this process-crash recovery: storage/kernel caches and completed persistence remain distinct, unlike replaying a selected block image ([fsync DESCRIPTION](https://man7.org/linux/man-pages/man2/fsync.2.html), [CrashMonkey paper §5.1](https://www.cs.utexas.edu/~vijay/papers/osdi18-crashmonkey.pdf)).

## CrashMonkey and Ace

The inspected README lists tested Linux kernels through 5.6 and an old Ubuntu setup; it does not verify modern-kernel or Windows compatibility. CrashMonkey builds kernel modules and uses test devices ([README, Setup](https://raw.githubusercontent.com/utsaslab/crashmonkey/27ca57f8cf2760d5d4855e03b8d01f8e5de1628c/README.md)). Its selected source carries Apache-2.0 ([LICENSE](https://raw.githubusercontent.com/utsaslab/crashmonkey/27ca57f8cf2760d5d4855e03b8d01f8e5de1628c/LICENSE)).

Use already provisioned owned virtual devices in a disposable compatible VM. For an existing built workload, the documented in-order automatic-check shape is:
```text
./c_harness -v -c -P -f OWNED_FLAG_DEVICE -d OWNED_TEST_DEVICE -t FS_TYPE -e IMAGE_SIZE WORKLOAD.so
```
Substitute actual verified devices/settings. `-P` disables permuted-order replay; `-c` enables automatic checking. These are device-affecting parameters, not harmless file names ([CLI options](https://raw.githubusercontent.com/utsaslab/crashmonkey/27ca57f8cf2760d5d4855e03b8d01f8e5de1628c/code/harness/c_harness.cpp), [workload, Test with auto-checker](https://raw.githubusercontent.com/utsaslab/crashmonkey/27ca57f8cf2760d5d4855e03b8d01f8e5de1628c/docs/workload.md)).

Use the maintained `FsFns` recording calls and checkpoints; setup I/O is excluded. For custom checking, fill `DataTestResult`, not only the C++ return value. Retain checkpoint, BIO log, recovered state and diff; changed underlying workloads invalidate assumptions about old logs ([workload interface and replay](https://raw.githubusercontent.com/utsaslab/crashmonkey/27ca57f8cf2760d5d4855e03b8d01f8e5de1628c/docs/workload.md)). Ace generates bounded operation skeletons and translates them through an adapter; do not copy the filesystem implementation ([Ace](https://raw.githubusercontent.com/utsaslab/crashmonkey/27ca57f8cf2760d5d4855e03b8d01f8e5de1628c/docs/Ace.md)).

## LazyFS

The selected prototype documents C++17/FUSE3 and ext4 tests on Debian11/Ubuntu20.04; these are evidence limits, not current host compatibility. Configure the relevant application paths through the model and retain cache policy, exact fault occurrence and persisted pieces ([README](https://raw.githubusercontent.com/dsrhaslab/lazyfs/d93e54a7944b28e86506d2af3a97342f5c3eb21f/README.md)). Its actual license is MIT ([LICENSE](https://raw.githubusercontent.com/dsrhaslab/lazyfs/d93e54a7944b28e86506d2af3a97342f5c3eb21f/LICENSE)).

For an existing fitting build and owned mount/backing paths, the script accepts:
```text
./scripts/mount-lazyfs.sh -c CONFIG -m OWNED_MOUNT -r OWNED_BACKING -f -s
```
The script uses `allow_other` and unquoted path expansions: inspect actual FUSE prerequisites and path handling instead of assuming arbitrary host setup or whitespace-safe arguments ([script](https://raw.githubusercontent.com/dsrhaslab/lazyfs/d93e54a7944b28e86506d2af3a97342f5c3eb21f/lazyfs/scripts/mount-lazyfs.sh)).

For explicit unsynced-loss experiments, record `cache.apply_eviction=false`. Send the literal `lazyfs::clear-cache` through the existing configured control owner; await `finished::clear-cache` on `fifo_path_completed` before post-fault checks. Torn-sequence and torn-operation modes retain selected writes/pieces, then crash LazyFS ([README, Running and Injecting faults](https://raw.githubusercontent.com/dsrhaslab/lazyfs/d93e54a7944b28e86506d2af3a97342f5c3eb21f/README.md)). The implementation's crash trigger targets its own PID; it is not proof the application or hardware also crashed ([trigger_crash_fault](https://raw.githubusercontent.com/dsrhaslab/lazyfs/d93e54a7944b28e86506d2af3a97342f5c3eb21f/lazyfs/src/lazyfs.cpp)). Check bypassed I/O and metadata semantics before extending the claimed fault domain.

# Common mistakes

| WRONG | RIGHT |
| --- | --- |
| Treat successful file sync as directory-entry durability. | Trace the directory persistence promise and actual call/error path ([fsync DESCRIPTION](https://man7.org/linux/man-pages/man2/fsync.2.html)). |
| Claim atomic rename proves power-loss-safe replacement. | Separate live visibility from the target's recovery guarantee ([rename DESCRIPTION](https://man7.org/linux/man-pages/man2/rename.2.html), [fsync DESCRIPTION](https://man7.org/linux/man-pages/man2/fsync.2.html)). |
| Use mountability or fsck as the full data oracle. | Check promised persisted objects and continued operations ([CrashMonkey paper pp.6-8](https://www.cs.utexas.edu/~vijay/papers/osdi18-crashmonkey.pdf)). |
| Count a fault command as a completed crash/loss. | Retain actual activation and wait for the configured completion event ([LazyFS FIFO contract](https://raw.githubusercontent.com/dsrhaslab/lazyfs/d93e54a7944b28e86506d2af3a97342f5c3eb21f/README.md)). |
| Build `CrashCloneCfg{Probability: 50}` from the stale comment. | Use actual `UnsyncedDataPercent` and required RNG ([CrashCloneCfg](https://raw.githubusercontent.com/cockroachdb/pebble/a995e890c06ef86c583927906e16e7f313083a3f/vfs/mem_fs.go)). |
| Close cleanly, then capture the alleged crash state. | Snapshot first, as the real restart caller does ([restartDB](https://raw.githubusercontent.com/cockroachdb/pebble/a995e890c06ef86c583927906e16e7f313083a3f/metamorphic/test.go)). |
| Interpret pre-operation injected errors as partial-write coverage. | Preserve the actual no-effect injection boundary ([errorfs Injector](https://raw.githubusercontent.com/cockroachdb/pebble/a995e890c06ef86c583927906e16e7f313083a3f/vfs/errorfs/errorfs.go)). |
| Invert `-P` or copy a host device from an example. | `-P` disables permuted replay; resolve actual owned virtual-device arguments ([CLI options](https://raw.githubusercontent.com/utsaslab/crashmonkey/27ca57f8cf2760d5d4855e03b8d01f8e5de1628c/code/harness/c_harness.cpp)). |
| Call a small bounded workload set every possible crash. | State operation/argument/fault bounds and omissions ([Ace bounds](https://raw.githubusercontent.com/utsaslab/crashmonkey/27ca57f8cf2760d5d4855e03b8d01f8e5de1628c/docs/Ace.md), [paper §4.4](https://www.cs.utexas.edu/~vijay/papers/osdi18-crashmonkey.pdf)). |

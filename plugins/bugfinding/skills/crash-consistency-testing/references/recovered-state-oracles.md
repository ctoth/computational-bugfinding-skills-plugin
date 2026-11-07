# Recovered-state oracles

This procedure is the pack's contract-to-experiment design. Trace the public acknowledgment through buffering, persistence and recovery; derive permitted outcomes from the actual stack. Linux `fsync` can report delayed EIO/ENOSPC and does not alone persist a containing directory entry ([DESCRIPTION and ERRORS](https://man7.org/linux/man-pages/man2/fsync.2.html)).

Classify durable acknowledgments, explicitly nondurable responses, rejected operations with their permitted effects, and pending/unknown responses. State required survivors, allowed old/new alternatives, atomic groups and unaffected records. Do not impose total rollback or disappearance of every unacknowledged operation. CrashMonkey's oracle is limited to explicitly persisted objects rather than every precrash observation ([Mohan et al., pp.6-8](https://www.cs.utexas.edu/~vijay/papers/osdi18-crashmonkey.pdf)).

Capture responses outside the crashed domain and confirm the actual fault event. Recover with the real startup configuration; check promised data and relevant namespace/metadata, then continued read/write behavior. CrashMonkey separates crash-image generation, mounted recovery and object checks ([paper, §5.1](https://www.cs.utexas.edu/~vijay/papers/osdi18-crashmonkey.pdf)).

## Worked experiments

These are illustrative designs, not findings about a named product.

| Real guarantee to establish | Experiment and retained witness |
| --- | --- |
| A replacement acknowledgment promises a durable new snapshot | Trace write/sync/rename/directory persistence and errors; enumerate supported cuts; compare allowed logical snapshots plus unaffected data. A live atomic rename is insufficient evidence of the crash promise ([rename DESCRIPTION](https://man7.org/linux/man-pages/man2/rename.2.html), [fsync DESCRIPTION](https://man7.org/linux/man-pages/man2/fsync.2.html)). |
| Durable batch A precedes pending B | Record A's acknowledgment and B's uncertain boundary; recover from an admissible crash state. Require A's promise and B's permitted alternatives. Snapshot before graceful close, as the actual Pebble restart caller does ([restartDB](https://raw.githubusercontent.com/cockroachdb/pebble/a995e890c06ef86c583927906e16e7f313083a3f/metamorphic/test.go)). |
| A flush error must prevent a durability acknowledgment | Inject the actual operation/path and verify the hit and surfaced error. A pre-operation `errorfs` result checks a narrower path than torn/post-effect failure ([Injector and Counter](https://raw.githubusercontent.com/cockroachdb/pebble/a995e890c06ef86c583927906e16e7f313083a3f/vfs/errorfs/errorfs.go)). |

Reduce unrelated setup, operation blocks and fault choices while rechecking the same allowed-state relation. If removing a write changes the selected ordinal, resolve the new event against the actual trace. Retain injection misses, alternate failures and unreproduced originals separately; workload checkpoints tie persistence and replay observations together ([CrashMonkey workload, Interface and Result](https://raw.githubusercontent.com/utsaslab/crashmonkey/27ca57f8cf2760d5d4855e03b8d01f8e5de1628c/docs/workload.md)).

Budget generation, fault execution, recovery, checks and reduction separately. Increase the dimension omitted by the current experiment; Ace exposes independently bounded operations, topology and data ranges ([Ace, Bounds](https://raw.githubusercontent.com/utsaslab/crashmonkey/27ca57f8cf2760d5d4855e03b8d01f8e5de1628c/docs/Ace.md)). Report finite tested bounds rather than claim exhaustive native-storage coverage.

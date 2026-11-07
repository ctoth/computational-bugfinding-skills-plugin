# Pebble VFS operation

Use this route when the real target already has a fitting VFS seam, or an authorized target change establishes the shown need. The inspected module declares `go 1.25.3`; check the selected version instead of treating this as every Go project's environment ([go.mod](https://raw.githubusercontent.com/cockroachdb/pebble/a995e890c06ef86c583927906e16e7f313083a3f/go.mod)). Its license is BSD with three conditions ([LICENSE](https://raw.githubusercontent.com/cockroachdb/pebble/a995e890c06ef86c583927906e16e7f313083a3f/LICENSE)).

`vfs.NewCrashableMem()` creates the model. The real struct field is `UnsyncedDataPercent`: at 0 "the clone will contain exactly the data that was last synced", and "RNG must be set if UnsyncedDataPercent > 0". The `NewCrashableMem` doc comment still shows an obsolete `CrashCloneCfg{Probability: 50, ...}` example: follow the real struct/API ([mem_fs.go, NewCrashableMem and CrashCloneCfg](https://raw.githubusercontent.com/cockroachdb/pebble/a995e890c06ef86c583927906e16e7f313083a3f/vfs/mem_fs.go)).

The existing integration order is significant:
```text
capture crash clone
close the original DB
reopen the DB using the clone
check the promised recovered effects
```
The real `restartDB` caller takes `fs.CrashClone(vfs.CrashCloneCfg{UnsyncedDataPercent: 0})` before `db.Close()`, so graceful/background flushing cannot strengthen that snapshot. It skips the restart when databases "share the same FS", and when strictFS is off, because writes then use `pebble.NoSync` "so we can't restart the database" ([metamorphic restartDB](https://raw.githubusercontent.com/cockroachdb/pebble/a995e890c06ef86c583927906e16e7f313083a3f/metamorphic/test.go)). Preserve acknowledgments externally and choose the allowed recovered-state relation from the target's actual write mode.

Unsynced selection operates on modeled `const blockSize = 4096` blocks and on directory entries; a selected block past the synced length grows the file "leaving 0s for any unsynced blocks past the synced length". Record initial state, percentage, RNG identity/seed and generated clone; neither one seed nor the zero-percent case exhausts real storage failure states ([memNode.CrashClone](https://raw.githubusercontent.com/cockroachdb/pebble/a995e890c06ef86c583927906e16e7f313083a3f/vfs/mem_fs.go)).

For operation-error search, `errorfs.Wrap(fs, injector)` calls `MaybeError`, which "is invoked by an errorfs before an operation is executed"; for two-path operations "the original source path is provided". An injected `Write` error returns `0, err` without calling the wrapped file. `Counter` counts injected errors so a test can check that "the error is surfaced through the user interface"; check `Load()` and `LastError()`. Record operation/path/index and observed propagation; this seam alone does not model partial success followed by an error ([Injector, Counter and Wrap](https://raw.githubusercontent.com/cockroachdb/pebble/a995e890c06ef86c583927906e16e7f313083a3f/vfs/errorfs/errorfs.go)).

Keep modeled findings qualified. A clone can expose a forbidden application recovery effect under its supported semantics; validating native filesystems, delayed device errors or hardware durability needs a fitting independent experiment. The crash-image method itself has explicit selected-bound limitations: B3 "does not make any guarantees about finding" every crash-consistency bug ([CrashMonkey paper §4.4](https://www.cs.utexas.edu/~vijay/papers/osdi18-crashmonkey.pdf)). Use the existing seam, not a universal filesystem facade.

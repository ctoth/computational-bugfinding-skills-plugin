# Pebble VFS operation

Use this route when the real target already has a fitting VFS seam, or an authorized target change establishes the shown need. The inspected module declares Go1.25.3; check the selected version instead of treating this as every Go project's environment ([go.mod](https://raw.githubusercontent.com/cockroachdb/pebble/a995e890c06ef86c583927906e16e7f313083a3f/go.mod)). Its license is BSD with three conditions ([LICENSE](https://raw.githubusercontent.com/cockroachdb/pebble/a995e890c06ef86c583927906e16e7f313083a3f/LICENSE)).

`vfs.NewCrashableMem()` creates the model. The actual configuration is `CrashCloneCfg{UnsyncedDataPercent: 0}`; zero retains synced model state, and a positive percentage needs an RNG. The source comment still contains an obsolete `Probability` example: follow the real struct/API ([mem_fs.go, CrashCloneCfg](https://raw.githubusercontent.com/cockroachdb/pebble/a995e890c06ef86c583927906e16e7f313083a3f/vfs/mem_fs.go)).

The existing integration order is significant:
```text
capture crash clone
close the original DB
reopen the DB using the clone
check the promised recovered effects
```
The real `restartDB` caller snapshots before `Close`, so graceful/background flushing cannot strengthen that snapshot. It excludes the multi-DB/shared-FS case ([metamorphic restartDB](https://raw.githubusercontent.com/cockroachdb/pebble/a995e890c06ef86c583927906e16e7f313083a3f/metamorphic/test.go)). Preserve acknowledgments externally and choose the allowed recovered-state relation from the target's actual write mode.

Unsynced selection operates on modeled 4096-byte blocks and directory entries. Record initial state, percentage, RNG identity/seed and generated clone; neither one seed nor the zero-percent case exhausts real storage failure states ([memNode.CrashClone](https://raw.githubusercontent.com/cockroachdb/pebble/a995e890c06ef86c583927906e16e7f313083a3f/vfs/mem_fs.go)).

For operation-error search, `errorfs.Wrap(fs, injector)` invokes `MaybeError` before the operation; a two-path operation supplies its source path. `Counter` supports verifying injection. Record operation/path/index and observed propagation; this seam alone does not model partial success followed by an error ([Injector, Counter and Wrap](https://raw.githubusercontent.com/cockroachdb/pebble/a995e890c06ef86c583927906e16e7f313083a3f/vfs/errorfs/errorfs.go)).

Keep modeled findings qualified. A clone can expose a forbidden application recovery effect under its supported semantics; validating native filesystems, delayed device errors or hardware durability needs a fitting independent experiment. The crash-image method itself has explicit selected-bound limitations ([CrashMonkey paper §4.4](https://www.cs.utexas.edu/~vijay/papers/osdi18-crashmonkey.pdf)). Use the existing seam, not a universal filesystem facade.

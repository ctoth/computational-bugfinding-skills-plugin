# Improve crash-consistency-testing

## Findings

Paper evidence: CrashMonkey OSDI 2018 paper-reader page images at C:/Users/Q/code/bugfinding-literature/crash-consistency-testing/papers/Mohan_2018_BoundedBlackBoxCrashTesting/pngs/; I re-viewed page-005..007 (printed pp.6-8) this session. Printed p.6 holds §4.1 end, §4.2, §4.3, §4.4; p.7 holds §5 and §5.1 start; p.8 continues §5.1.

1. INFO - man7 fsync/rename (SKILL.md:12, references/common-mistakes.md:5-6, references/recovered-state-oracles.md:3,15, references/fault-routes.md:7). Fetched https://man7.org/linux/man-pages/man2/fsync.2.html and rename.2.html this session (Linux man-pages 6.19; fsync page dated 2026-02-08). fsync DESCRIPTION says "Calling fsync() does not necessarily ensure that the entry in the directory containing the file has also reached disk"; rename DESCRIPTION says "there is no point at which another process attempting to access newpath will find it missing" and has no crash-durability statement. Claims are accurate. Fix: add short verbatim quotes on the load-bearing sentences; record man-pages version in sources.yaml (no immutable URL).
2. WARNING - references/recovered-state-oracles.md:3 said fsync "can report delayed EIO/ENOSPC". fsync ERRORS says EIO "may relate to data written to some other file descriptor on the same file" and that write-back errors are reported to file descriptors; ENOSPC "Disk space was exhausted while synchronizing". "Delayed" is a paraphrase not in the text. Fix: replace with the man page's own wording.
3. WARNING - references/recovered-state-oracles.md:21 said "Ace exposes independently bounded operations, topology and data ranges ([Ace, Bounds])". The pinned docs/Ace.md "Bounds used by Ace" lists Sequence length, File-system operations, File set, Persistence operations, and Fileset for persistence operations; it names no data ranges. Data ranges ("overlapping file ranges") and initial state appear in the paper's §4.2 (printed p.6, page image read). Fix: list Ace.md's actual bounds and cite data ranges to paper §4.2.
4. WARNING - references/fault-routes.md:19 said "Use the maintained `FsFns` recording calls". docs/workload.md at 27ca57f8 says "`open` is replaced by `cm_->CmOpen`" and "CrashMonkey requires that you wrap `open, close, rename, fsync, fdatasync, sync, msync` system calls for the correctness of auto-checker". `FsFns` is the low-level function-pointer class inside code/user_tools/api/wrapper.h (line 27) that `RecordCmFsOps` wraps; workloads call `cm_->Cm*`. Fix: name the documented `cm_->Cm*` wrappers and the wrapped call list.
5. WARNING - references/fault-routes.md:19 "changed underlying workloads invalidate assumptions about old logs" cited workload.md, which does not say it. Primary source found: docs/CrashMonkey.md at 27ca57f8 line 79: "As long as the bio sequence during profiling does not change, it is safe to rerun the tests by loading the saved profile with -r option." Fix: cite and quote CrashMonkey.md; add sources.yaml entry.
6. INFO - references/fault-routes.md:19 "do not copy the filesystem implementation" has no support in docs/Ace.md. Fix: cut the clause (claim cut).
7. INFO - c_harness.cpp long_options at 27ca57f8 verified: `{"automate_check_test", no_argument, NULL, 'c'}`, `{"no-permuted-order-replay", no_argument, NULL, 'P'}`, defaults `permuted_order_replay = true`, `flags_dev("/dev/vda")`, `test_dev("/dev/ram0")`. workload.md: auto-checker "requires the -P flag to perform in-order replay". Skill claims accurate; add quotes.
8. INFO - CrashMonkey README at 27ca57f8 says "tested to work with ext2, ext3, ext4, xfs, F2FS, and btrfs, across Linux kernel versions - 3.12, ... 5.5 and 5.6" and "We recommend spinning up a Ubuntu 16.04 VM". Accurate; add quote.
9. INFO - LazyFS README at d93e54a7 verified: "tested with ext4 (with the default mount options) as the underlying file system", "Debian 11 (bullseye) and Ubuntu 20.04 (focal)", "It is C++17 compliant", `FUSE 3`; `apply_eviction` described as "Whether the cache should behave like the real page cache"; `fifo_path_completed` writes "`finished::clear-cache`" so "users can set up a reader process that waits before making any post-fault consistency checks"; torn-seq/torn-op "LazyFS will crash itself"/"LazyFS will crash". mount-lazyfs.sh passes `-o allow_other` and unquoted `$MOUNT_DIR`, `$ROOT_DIR`, `$CMD_CONFIG`. lazyfs.cpp trigger_crash_fault: `pid_t lazyfs_pid = getpid ();` then `kill (lazyfs_pid, SIGKILL);`. LICENSE: "Licensed under the terms of MIT License". Claims accurate; add quotes.
10. INFO (gap) - LazyFS README "Running and Injecting faults" also states "Fault acknowledgment is sent to `stdout` or to the `logfile`" and "After a LazyFS crash, the mount directory may be left in an undefined state" (recover with `fusermount -uz`). Both bear on the skill's existing "retain hit evidence" and recovery steps. Fix: one sentence in references/fault-routes.md LazyFS section.
11. INFO - Pebble at a995e890 verified: go.mod line 64 `go 1.25.3`; LICENSE "provided that the following conditions are met" with three bullets; mem_fs.go `CrashCloneCfg` doc "If 0, the clone will contain exactly the data that was last synced", "RNG must be set if UnsyncedDataPercent > 0", stale doc example `CrashCloneCfg{Probability: 50, ...}` at line 53, `const blockSize = 4096` in memNode.CrashClone and per-child directory-entry selection; errorfs.go Injector "MaybeError is invoked by an errorfs before an operation is executed" and "the original source path is provided"; `errorFile.Write` returns `0, err` before calling `f.file.Write`; Counter "may be used in tests to ensure that when an error is injected, the error is surfaced through the user interface". Accurate; add quotes.
12. WARNING (gap) - references/pebble-vfs.md:14 said restartDB "excludes the multi-DB/shared-FS case" only. metamorphic/test.go:327-331 at a995e890 also returns without restarting when strictFS is off: "If strictFS is not used, we use pebble.NoSync for writeOpts, so we can't restart the database". This is exactly the write-mode dependency the next sentence tells readers to respect. Fix: add the strictFS/NoSync exclusion with quote.
13. INFO - Paper citations SKILL.md:8,14,22,28 and references/*.md cite "pp.6-8", "§5.1", "§4.4". Page images confirm: §4.3 "Fine-grained correctness checking" and §4.4 "Limitations" on printed p.6; §5.1 "CrashMonkey" on pp.7-8 with "only files and directories explicitly persisted at a given point in the workload are compared", "The crash state represents the state of storage if the system had crashed after a persistence operation completed", "it does not detect the loss or corruption of user data", "fsck is run only if the recovered file system is unmountable"; §4.4 "It is sound but incomplete." Accurate; add section numbers and quotes.
14. ERROR - references/common-mistakes.md was a two-column WRONG/RIGHT table with no "why" line per entry, violating skill-draft Step 3 / task check 6 (WRONG-first-then-RIGHT pairs with a one-line why). Sibling transactional-history-testing uses `## title` / **Wrong:** / **Right:** / **Why:** sections. Fix: convert each row to that form, keeping each row's WRONG/RIGHT text and citation, adding a Why line derived from the cited source.
15. WARNING - references/sources.yaml: entries carry a non-schema `quote` field and the paper's sections_used names pages only. Schema (skill-draft Step 7, task check 5) is name/url/type/accessed/sections_used. Fix: drop `quote` fields (quotes now inline), make sections_used name the sections actually cited, record man-pages 6.19 for the man7 entries, add CrashMonkey.md entry.

16. INFO - Added verbatim 4-10 word quotes on load-bearing sentences across SKILL.md and all references; each quote's source is the first link after its sentence (split multi-source sentences where needed, e.g. fault-routes.md `-P`/auto-checker and fsync/rename in SKILL.md:12). Non-paper quotes machine-checked against curl output of every pinned source this session; paper quotes checked against page images page-004..page-007.

Counts: ERROR 1 (14), WARNING 6 (2, 3, 4, 5, 12, 15), INFO 9 (1, 6, 7, 8, 9, 10, 11, 13, 16). Claims cut: 1 ("do not copy the filesystem implementation"). Sources added: 1 (docs/CrashMonkey.md).

## Pinned URLs

None needed. Every raw.githubusercontent.com URL already used a 40-hex commit (crashmonkey 27ca57f8cf2760d5d4855e03b8d01f8e5de1628c, lazyfs d93e54a7944b28e86506d2af3a97342f5c3eb21f, pebble a995e890c06ef86c583927906e16e7f313083a3f); the new CrashMonkey.md citation uses the same crashmonkey SHA. No /latest/ or /stable/ links. man7.org has no immutable URL; sources.yaml records Linux man-pages 6.19 (fsync page dated 2026-02-08) and access date.

## Validation

```
$ python C:/Users/Q/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/bugfinding/skills/crash-consistency-testing
Skill is valid!
exit=0
$ git diff --check -- plugins/bugfinding/skills/crash-consistency-testing
diffcheck=0
read-only citation/link probe (python -I -c, pathlib+yaml):
cited-not-listed: []
listed-not-cited: []
fields: [('accessed', 'name', 'sections_used', 'type', 'url')]
problems: []          # no moving/unpinned URLs, no unresolved local links, every file ends with exactly one newline
cited: 18 listed: 18
line counts: SKILL.md 28, common-mistakes.md 75, fault-routes.md 31, pebble-vfs.md 20, recovered-state-oracles.md 21, sources.yaml 130
```

Quote probe: all non-paper quotes found in curl output of the pinned sources (Go comment quotes matched after removing `//` line-wrap markers). Paper quotes are absent from that probe by design (PDF excluded) and were checked against page images.

## Unverified

- Paper quotes were checked visually against page images, not by a machine string match.
- No tool was run (no CrashMonkey, LazyFS or Pebble execution); option and behavior claims rest on pinned source and docs only, as the skill itself states.
- The final quote probe ran before two last edits (fault-routes.md "LazyFS will crash", shortened quotes); those strings are substrings of quotes that had matched.

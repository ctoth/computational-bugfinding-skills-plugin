# Improve race-detection campaign skill

## Findings

Paper evidence: TSan 2009 page images `pngs/page-002..007.png` (printed pp.64-69) in C:/Users/Q/code/bugfinding-literature/race-detection-campaigns/papers/Serebryany_2009_ThreadSanitizer, produced by paper-reader in the research step, re-viewed as images this session. Verified: §5 p.65 "Any dynamic race detector must understand the synchronization mechanisms"; §6.3.4/6.3.5 p.67 publication/initialization; §6.4.3 p.69 reference counting; §6.5 p.69 "Excessive synchronization may be just as incorrect as no synchronization at all, but it may hide real races"; §7.1 p.69 "ThreadSanitizer found this data race in a single run", "the failure stack traces were in a different place"; §4.4.1 pp.64-65 "ThreadSanitizer cannot distinguish between these two cases".

- F1 SKILL.md:34, WARNING. Text: "a race observer does not supply an abstract object-history oracle ([TSan 2009, §4.4.1, pp.64–65])". Source §4.4.1 p.65 says, of a flag example whose correctness depends on the flag's initial value, "ThreadSanitizer cannot distinguish between these two cases". The cited text supports "the detector cannot judge logic-dependent correctness", not an "object-history oracle" term the paper never uses. Fix: reworded to the source's claim with quote.
- F2 go-runtime.md:23 and sources.yaml:24, ERROR. Text: "build source, lines3325–3332" for the cgo MSan/ASan flag appends. Source exec.go@dcc06a82 lines 3325-3332 are `gccArchArgs` (`-m32`/`-m64`); the appends are at lines 3553-3560: `if cfg.BuildMSan { cgoCFLAGS = append([]string{"-fsanitize=memory"}, ...` and the same for `cfg.BuildASan`; no race/thread branch there. Fix: line numbers corrected in text and sources.yaml.
- F3 sources.yaml:72, ERROR. Text: "Initialize lines729–731" for `!SANITIZER_GO` guard on adaptive delay. Source tsan_rtl.cpp@635f3089 lines 777-779: `#if !SANITIZER_GO` / `AdaptiveDelay::Init();` / `#endif`; 729-731 guard InitializeAllocator. Fix: corrected.
- F4 sources.yaml:80, ERROR. Text: "InitTls lines243–251; delay operations lines277–307". Source tsan_adaptive_delay.cpp@635f3089: `InitTls` lines 265-273 with `SetRandomSeed(NanoTime());` at 271; delay operations 302-403. Fix: corrected.
- F5 sources.yaml:16, WARNING. Text: "RaceDetectorSupported lines16–32; FuzzInstrumented lines80–90". Source supported.go@dcc06a82: RaceDetectorSupported comment+body lines 18-34; FuzzInstrumented (lines 87+) is not cited by any skill sentence. Fix: lines corrected, unused section dropped.
- F6 sources.yaml (Go guide sections_used), WARNING. Text lists "Usage" but SKILL.md/evidence cite "How to Use"; the article heading is `How To Use` (id How_To_Use) and the overhead heading id is `Runtime_Overheads`. Fix: sections_used names actual headings used.
- F7 native-runtime.md:33, ERROR (content). Text: "Full history helps retain the earlier conflicting stack but costs resources" (framed as opt-in; command passes `--history-level=full`). Source hg-manual §7.6: "--history-level=full (the default)", "expensive in both speed and memory", old stacks in an LRU cache (`--conflict-cache-size`). Fix: states it is the default, the command only makes it explicit.
- F8 native-runtime.md:33, WARNING (gap, in scope: object-lifecycle races). Source hg-manual §7.6: `--free-is-write=no|yes [default: no]` "treats freeing of heap memory as if the memory was written immediately before the free", "regarded as experimental". Fix: one sentence added.
- F9 native-runtime.md:33, WARNING. Text: "Default error exit behavior can preserve target success despite reports"; "Check child tracing". Source manual-core: `--error-exitcode=<number> [default: 0]`, "the return value from Valgrind will always be the return value of the process being simulated"; `--trace-children=<yes|no> [default: no]`; `%p is replaced with the current process ID`. Fix: quoted defaults.
- F10 native-runtime.md:35 and sources.yaml (3 places), WARNING. Mangled text "identify3.28.0,23Oct2026", "release3.28.0", "observed2026-11-07", "Iskhodzhanov,2009". Source dist.news.html: "Release 3.28.0 (23 Oct 2026)", platform list without Windows, "macOS is supported up to version 13 Ventura (amd64 only)". Fix: corrected text and quoted platform statement.
- F11 native-runtime.md:13, WARNING (gap). Source tsan_flags.inc: `suppress_equal_stacks` default true ("Suppress a race report if we've already output another race report with the same stack"); ThreadSanitizer.md Run-time Flags: `exitcode` default 66, `history_size` default 0 / "failed to restore the stack", `ignore_noninstrumented_modules`. Text omitted these result-classification facts. Fix: two sentences added, cited.
- F12 go-runtime.md:19, WARNING (gap). Text named output/first-report/history controls without values. Source Go guide Options: `log_path` -> `log_path.pid`, `exitcode` (default `66`), `history_size` "can avoid a \"failed to restore the stack\" error", `halt_on_error` (default `0`). Fix: values quoted; exit 66 classified separately from workload failures.
- F13 go-runtime.md:5, WARNING (gap). Source Go guide Requirements: Windows "as of Go 1.21 ... requires a C compiler that incorporates version 8 or later of the `mingw-w64` runtime libraries"; older compilers "will just echo the argument". Fix: added.
- F14 go-runtime.md:7, INFO. Text "admits more targets than the pinned website article" unspecific. Source supported.go line 26 admits `riscv64` on linux; article list lacks linux/riscv64. Fix: named it, quoted VMA comment.
- F15 go-runtime.md:23, WARNING. Plugin quote added; the toolchain/tag sameness warning is about runtime crashes (plugin.go lines 49-53), stated as such, not as a race-detection claim.
- F16 evidence-and-limits.md:5, WARNING (uncited). "Its historical Valgrind modes are not modern Go/Clang runtime settings" had no citation. Source TSan 2009 §4.3 n.5 p.64 "--keep-history=[012]"; Clang Run-time Flags list has no such flag. Fix: cited both.
- F17 evidence-and-limits.md:11, WARNING. Timing claim cited only Go overhead and Clang limitations. Added Clang "5x plus 1Mb per each thread" and TSan 2009 §6.5 p.69 "is slow. Do not hard-code any timeout values".
- F18 common-mistakes.md, ERROR (audit check 6/skill-draft Step 3). Table had WRONG/RIGHT but no one-line why; row 7 had mangled "exit0". Fix: added cited Why column to every row; line numbers added to source links; "exit 0".
- F19 SKILL.md:8,12,14,20,24,28,32 and references, INFO. Load-bearing claims lacked verbatim fragments. Fix: 4-15 word quotes added, all from text retrieved this session (curl of the pinned raw URLs/pages; paper from page images).
- F20 SKILL.md:28, INFO. Routes to `resource-complexity-testing`/`liveness-testing`, which do not exist yet under plugins/bugfinding/skills/; agent-notes/computational-bugfinding-marketplace.md:35 says they are being researched. Not changed (planned siblings, also referenced by other skills).

## Pinned URLs

No moving-branch URLs existed. All GitHub pins re-checked against current heads with `gh api .../commits/<branch> --jq .sha`: golang/website master = a8b66266e226994e2ead51317bace3ee83cedab9, golang/go master = dcc06a82727b447270b1a58cc5f86b49736e317c, llvm/llvm-project main = 635f30899dd0914fa89f0b3dc9a9e548e6d0ceec (all equal to the cited pins); content read at those SHAs. pkg.go.dev is version-pinned `@go1.27.3`. Valgrind pages (hg-manual, manual-core, dist.news, about) have no immutable URL; kept with revision "Release 3.28.0 (23 Oct 2026)" / "observed 2026-11-07" in sources.yaml. URLs pinned this session: 0.

## Validation

Fetch method: all 16 source URLs downloaded with curl (read-only) to the session scratchpad and read as raw text; this gives exact text for quotes, which WebFetch's model summary does not.

```
$ python C:/Users/Q/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
Skill is valid!
$ (citation cross-check script: inline http links vs sources.yaml urls, fragments stripped; local links; moving-branch segments; EOF newlines)
cited not listed {'https://pkg.go.dev/cmd/go@go1.27.3'}
listed not cited {'https://pkg.go.dev/cmd/go@go1.27.3#hdr-Testing_flags'}
16 16
```
(The one pair is the same URL; the script stripped the fragment only on the cited side. With fragments ignored both sets match, 16/16. No broken local links, no moving URLs, no EOF problems reported.)
```
$ wc -l SKILL.md
34 SKILL.md
$ git diff --check -- plugins/bugfinding/skills/race-detection-campaigns
diffcheck-clean
$ yaml.safe_load(sources.yaml): 16 entries, all have name/url/type/accessed/sections_used -> True
$ git diff --stat: 7 files changed, 52 insertions(+), 52 deletions(-)
```

## Unverified

- No command in the skill was executed (go test -race, clang -fsanitize=thread, valgrind); they stay labelled unexecuted.
- Paper claims rest on the existing paper-reader page images (re-viewed this session), not a new paper-reader run.
- sources.yaml keeps the pre-existing extra `revision`/`quote` fields; their `quote` values were not all re-checked (spot-checked: "failed to restore", "poorly supported", "-fsanitize=memory", "!SANITIZER_GO", "SetRandomSeed(NanoTime())", "with LLVM Exceptions", "Neither the name", "two stack traces", "GPL'd system", "Release 3.28.0", "DYNAMIC ANNOTATIONS" all present).

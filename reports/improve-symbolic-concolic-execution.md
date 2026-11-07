# Improve: symbolic-concolic-execution

## Findings

Paper evidence: KLEE OSDI 2008 page images read directly this session from the existing paper-reader directory `C:/Users/Q/code/bugfinding-literature/symbolic-concolic-execution/papers/Cadar_2008_KLEE/pngs/` (page-002 = printed p.3, page-006 = p.7, page-007 = p.8, more appended below).

- F1 ERROR — references/target-and-environment.md:5 and references/common-mistakes.md:7. Text cited "KLEE, §§4 and 6" for the paper's target-linked syscall driver. Source: printed p.14 (page-013) puts "5.6 The HiStar OS kernel" and its driver there, and "6 Related Work" starts at the bottom of p.14; printed p.8 §5 intro: "close with results for HiStar (§5.6)" ([KLEE paper](https://www.doc.ic.ac.uk/~cristic/papers/klee-osdi-08.pdf)). Fix: citation changed to §§4 and 5.6, with a quote from §5.6.
- F2 WARNING — references/target-and-environment.md:7 said "Current KLEE has distinct concrete/all/over-approx external policies". Source `enum class ExternalCallPolicy` lists None, Concrete, All, OverApprox, and concrete is "allowed (default)" ([Executor.cpp@2c11e51](https://raw.githubusercontent.com/klee/klee/2c11e515ed83608a0b01b48ffd5865a93b2a0b9f/lib/Core/Executor.cpp), lines 182-209). Fix: list all four, name the default, add quote.
- F3 INFO — SKILL.md:8 claim checked against printed p.3 §2: "bugs in KLEE or its models have produced false positives in practice". Accurate; quote added.
- F4 INFO — Verified at the pinned SHAs: CMakeLists.txt line 117 "KLEE requires LLVM 15 or newer", line 13 `cmake_minimum_required(VERSION 3.16.0)`, line 193 CXX 17, line 20 `3 4-pre`, line 477 `ENABLE_POSIX_RUNTIME ... OFF`, line 509 `ENABLE_KLEE_LIBCXX ... OFF`; LICENSE.TXT "University of Illinois/NCSA"; SolverCmdLine.cpp line 78 "Maximum amount of time for a single SMT query"; main.cpp line 289 watchdog "Use a watchdog process to enforce --max-time"; UserSearcher.cpp default "random-path interleaved with nurs:covnew"; klee-replay.c `main` returns 0 after `waitpid` without reading `status` (lines 396-424), `process_status` `_exit(rc)` in the monitored child only; intrinsics.c line 44 `KLEE_RUN_TEST_ERRORS_NON_FATAL` makes "object name mismatch"/"object sizes differ" nonfatal. Load-bearing quotes added where these claims appear.
- F5 WARNING — Tutorial section labels did not match headings: "tutorial, Compiling and Running" (klee-operation-and-replay.md:7), "tutorial, Replaying" (:22), "KLEE tutorial, Running" (target-and-environment.md:25). Pinned testing-function.md headings are "Compiling to LLVM bitcode", "Running KLEE", "Replaying a test case", "Marking input as symbolic". Fix: labels corrected.
- F6 WARNING (gap) — klee-operation-and-replay.md:16 example `-sym-files 1 64` did not say how the target reaches the file. using-symbolic.md: "the first file is named 'A', the second 'B', and so on", and the tutorial passes `A` as the program argument ([using-symbolic.md@6b3c0bf](https://raw.githubusercontent.com/klee/klee.github.io/6b3c0bff41807b3370655d58a43e91bdee24b3c0/tutorials/using-symbolic.md)). Fix: one sentence added with the quote; also that `-posix-runtime` is required for these options.
- F7 WARNING (gap) — SKILL.md:18 and concolic-hybrid-operation.md mention pruning but not the backend it belongs to. SymCC README FAQ "QSym backend performs pruning": "it isn't sound" and "When building with the simple backend the paths should be found"; symcc-rt CMakeLists line 29 `set(SYMCC_RT_AVAILABLE_BACKENDS "simple" "qsym")`, default `qsym` ([README@522c480](https://raw.githubusercontent.com/eurecom-s3/symcc/522c48070bc312aeb621a631ff130ded71507d6d/README.md), [symcc-rt CMakeLists@892f817](https://raw.githubusercontent.com/eurecom-s3/symcc-rt/892f817f38f5abfa083dd0c1caa7ced821566bf5/CMakeLists.txt)). Fix: sentence added in concolic-hybrid-operation.md with quotes.
- F8 WARNING (gap) — concolic-hybrid-operation.md:13-19 file-input example relies on SYMCC_OUTPUT_DIR. Configuration.txt: SYMCC_OUTPUT_DIR (default "/tmp/output") stores new inputs "(QSYM backend only)". Fix: added to the run paragraph with quote.
- F10 WARNING — SKILL.md:20 quote-placement: the paper citation came third, after two source-code links; SKILL.md:14 citations followed a local reference link instead of the claim. Fix: paper link moved first on :20 (section narrowed to §§3.4 and 5.5; §3.4 "State scheduling" is on printed p.6 and §5.5 says KLEE proves "any condition the programmer expresses as C code", p.13); :14 citation moved directly after the claim with an Executor.cpp quote ("concretizes any symbolic arguments in calls to external functions").
- F11 WARNING — SKILL.md:24 "can return0" (glued digit) and no named nonfatal switch. Source intrinsics.c line 44 reads `KLEE_RUN_TEST_ERRORS_NON_FATAL`. Fix: "return 0", env var named, quote "object name mismatch" added. SKILL.md:26 citation narrowed to §§2 and 4.3 with quote "Our biggest challenge was making system calls fail outside of KLEE" (p.8).
- F12 WARNING — klee-operation-and-replay.md:18 attributed the "older option prose" comparison only to Executor.cpp. Source of "three policies" is options.md "External Call Policy": "KLEE provides three policies" ([options.md@6b3c0bf](https://raw.githubusercontent.com/klee/klee.github.io/6b3c0bff41807b3370655d58a43e91bdee24b3c0/docs/options.md)). Fix: split sentence, options.md cited for that half, Executor.cpp quote "the concretization is ignored after the call" for the other.
- F13 INFO — klee-operation-and-replay.md glued digits "KLEE3.4-pre", "CMake3.16", "LLVM15+", "returns0" fixed; quotes added: tutorial "The bitcode passed to KLEE should not be optimised" / "prevents KLEE from doing its own optimisations"; "-posix-runtime" requirement; replay library "simply replaces the call to `klee_make_symbolic`"; `process_status` strings; paper §4.3 ptrace utility (p.8); default-OFF CMake options.
- F14 INFO — target-and-environment.md quotes added: §4 p.7 "should be reflected in subsequent reads"; §6 p.15 "a concrete external call will do exactly what it did, rather than all things it could potentially do"; intrinsics.md "The remainder of the program's execution will only consider variable values which satisfy _condition_." and "invalid klee_assume call (provably false)"; tutorial "the address of the variable", "its size, and a name"; intrinsics.c "object sizes differ"; §5.5 p.13 "cannot make statements about paths it misses"; tutorial "interrupted (partially completed) paths"; SymCC README "The current symbolic understanding of libc is incomplete."; C++.txt "i.e., we lose track of the corresponding symbolic expressions".
- F15 WARNING — references/common-mistakes.md:5-14 was a two-column "WRONG | RIGHT and why" table; several rows had no separate why (e.g. row 6 "Count generated files..."), against skill-draft Step 3 / task check 6. Fix: table given a third "Why" column with one line per row; each RIGHT cell now carries a verified quote; row 7 "another runtime main" (unclear) reworded to "a symcc-rt checkout other than the parent's submodule"; its why cites Configuration.txt `QSYM_BACKEND=ON/OFF` and `grep -c QSYM_BACKEND` = 0 in both CMake files.
- F16 WARNING — concolic-hybrid-operation.md: glued "LLVM8-18", "AFL2.56b", "a90-second", "kill-after5s" fixed; `symcc`/`sym++` wrapper claim was uncited (only CMake links). Fix: cited C++.txt ("a wrapper "sym++" around clang++") and the runtime submodule pin (gh api contents at 522c480, new sources.yaml entry). Added C++.txt "currently doesn't work with the QSYM backend" for building instrumented libc++; Fuzzing.txt "we've tested with version 2.56b", "just make sure that each has a unique name", "new test cases need to be checked for whether they trigger vulnerabilities"; helper `const TIMEOUT: u32 = 90;`, `timeout -k 5`, linearization `1`; Configuration.txt map "isn't meant to point at a map file that AFL uses too", `SYMCC_MEMORY_INPUT` "Can't be combined with SYMCC_INPUT_FILE".
- F9 INFO — Verified: symcc 522c480 `runtime` is a submodule at 892f817 (gh api contents); compiler CMakeLists warns for LLVM outside 8-17 (line 33) and 8-18 (line 94), `SYMCC_RT_BACKEND "qsym"` (line 19); Configuration.txt line 23 still documents `QSYM_BACKEND=ON/OFF`; README "any version between 8 and 18", Z3 4.5+, C++17, "best effort mode"; Configuration.txt `SYMCC_ENABLE_LINEARIZATION` "enabled automatically by the fuzzing helper", AFL map "updated in place".

- F17 INFO — references/sources.yaml: paper entry renamed to full title, sections_used rewritten to the sections actually cited (§§2, 3.4, 4-4.3, 5.5, 5.6, 6 with printed pages; old text "Sections2-4,5.5,6" omitted 5.6 and mislabelled the HiStar driver as §6); tutorial/options/README/Configuration/C++/Fuzzing/build/main.cpp/SolverCmdLine sections_used corrected to match what the text now cites (e.g. SolverCmdLine "query logging" removed — not used); new entry for the SymCC runtime submodule pin. Existing `quote_fragment` values were each re-checked against fetched text and are exact.

Claims cut: none. Every pre-existing claim was found supported once section labels were fixed.

## Pinned URLs

No moving URLs existed: every raw.githubusercontent.com link was already at a 40-hex SHA (klee 2c11e515…, klee.github.io 6b3c0bff…, symcc 522c4807…, symcc-rt 892f817f…). One new pinned URL added: `https://api.github.com/repos/eurecom-s3/symcc/contents/runtime?ref=522c48070bc312aeb621a631ff130ded71507d6d`. The KLEE paper PDF (author site, no version path) returned HTTP 200 on 2026-11-07. URLs pinned this pass: 0 (none needed).

## Validation

```
$ python C:/Users/Q/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/bugfinding/skills/symbolic-concolic-execution
Skill is valid!
exit=0
--- cited not in yaml:
--- yaml not cited:
--- moving urls:   (grep for /main/, /master/, /HEAD/, /blob/main, /latest/, /stable/: no hits)
raw.githubusercontent.com/eurecom-s3/symcc-rt/892f817f38f5abfa083dd0c1caa7ced821566bf5/
raw.githubusercontent.com/eurecom-s3/symcc/522c48070bc312aeb621a631ff130ded71507d6d/
raw.githubusercontent.com/klee/klee.github.io/6b3c0bff41807b3370655d58a43e91bdee24b3c0/
raw.githubusercontent.com/klee/klee/2c11e515ed83608a0b01b48ffd5865a93b2a0b9f/
--- local links:
ok SKILL.md -> references/target-and-environment.md
ok SKILL.md -> references/klee-operation-and-replay.md
ok SKILL.md -> references/concolic-hybrid-operation.md
ok SKILL.md -> references/common-mistakes.md
diffcheck=0   (git diff --check -- plugins/bugfinding/skills/symbolic-concolic-execution)
file endings (last two bytes): SKILL.md ".\n", common-mistakes.md "|\n", concolic-hybrid-operation.md ".\n", klee-operation-and-replay.md ".\n", sources.yaml "\"\n", target-and-environment.md ".\n"  -> exactly one trailing newline each
SKILL.md: 30 lines (<=500)
```

Audit checks 1-6: frontmatter name matches directory, description third person with trigger; no filler; local links resolve; no ERRORs found beyond F1.

## Unverified

- Quote placement: in a few multi-quote sentences (concolic-hybrid-operation.md run paragraph; target-and-environment.md object-identity sentence) two sources are quoted in one sentence, so only the first quote's source is the first link after it; both sources are linked immediately after.
- KLEE paper: only page images page-002, 005, 006, 007, 012, 013, 014 were viewed this session; other page claims rely on the existing paper-reader read (research report) and none are newly stated.
- No tool was installed or run; flags and behavior are verified from source/docs at the pinned SHAs only.

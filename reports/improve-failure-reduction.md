# Improve failure-reduction: citation and content audit

Skill: `plugins/bugfinding/skills/failure-reduction/`. Accessed 2026-11-07.

## Findings

Sources fetched this session (raw files at pinned SHAs, saved in scratchpad): C-Reduce `creduce/creduce.in`, `INSTALL.md`, `COPYING` at csmith-project/creduce 31e855e290970cba0286e5032971509c0e7c0a80; LLVM `LICENSE.TXT`, `llvm/docs/CommandGuide/llvm-reduce.md`, `llvm/docs/LibFuzzer.md` at llvm/llvm-project 635f30899dd0914fa89f0b3dc9a9e548e6d0ceec.

1. **ERROR — moving URLs.** SKILL.md:29, tool-recipes.md:7,13,15,19,25,35, common-mistakes.md:7,8, sources.yaml cite `/master/`, `/main/`, unversioned `llvm.org/docs/` (built from LLVM main) and Hypothesis `/latest/`. Source: skill-draft Step 5 forbids moving aliases. Fix: repointed to SHA-pinned raw GitHub files (see Pinned URLs).
2. **WARNING — C-Reduce determinism requirement missing.** tool-recipes.md:7 described the test contract (no args, temp dir, exit zero) without the source's determinism requirement. Source `creduce.in` help: "The interestingness test should be deterministic and should not expect any command line arguments." Fix: added the quote.
3. **WARNING — C-Reduce rewrites its inputs in place.** tool-recipes.md:3,7 said to keep an untouched original but did not say C-Reduce itself rewrites the named files. Source `creduce.in` help: files "must be writable"; `--tidy`: "Do not make a backup copy of each file to reduce as file.orig"; lines 1071-1077 copy `${fo}.orig` unless `--tidy`. Fix: added to C-Reduce recipe.
4. **INFO — C-Reduce has a native way to keep a different interesting variant.** interestingness-and-replay.md:14 says preserve a different genuine violation; tool-recipes did not name the native option. Source `creduce.in` `--also-interesting`: "A process exit code ... that, when returned by the interestingness test, will cause C-Reduce to save a copy of the variant"; `delta_test` returns `$res == 0` only (line 322). Fix: one sentence in C-Reduce recipe; no new machinery.
5. **INFO — C-Reduce startup sanity check.** SKILL.md:29 asks to exercise the original through the reducer interface. Source `creduce.in` lines 332-366 `sanity_check` copies files to a fresh temp dir and exits if the test "does not return zero". Fix: cited in tool-recipes as the native original check (healthy/invalid candidates remain the skill's own check).
7. **WARNING — Go minimization preserves any error, not the selected one.** tool-recipes.md:39 described `-fuzzminimizetime` but not what Go's minimizer preserves. Source golang/website `_content/doc/security/fuzz/index.md` (a8b66266e226994e2ead51317bace3ee83cedab9) Failing input: the engine minimizes "to the smallest possible and most human readable value which will still produce an error". Fix: added; replay the minimized entry against the selected predicate (consistent with SKILL.md:14).
8. **WARNING — Go corpus typing claim uncited specifics.** tool-recipes.md:39 "Keep Go corpus argument types and ordering". Source Corpus file format: "These types must match the fuzzing arguments exactly, in that order." Fix: quote added.
9. **WARNING — delta-debugging citations imprecise.** SKILL.md:14 and common-mistakes.md:5 cite `generic_test` for classifying unrelated exceptions. Source debuggingbook `docs/code/DeltaDebugger.py` (uds-se/debuggingbook 35dfb6c7a1932e4d5e9ca9858b4b1e80eb7447a5) lines 311-327: with `expected_exc=None` any exception is `FAIL`; only with an expected exception does a mismatch in type or message become `UNRESOLVED`; notebook text: "The `ddmin` algorithm treats such unresolved outcomes as if they were passing". Fix: SKILL.md and common-mistakes now state the expected-exception condition and quote the ddmin treatment.
10. **INFO — 1-minimal definition.** SKILL.md:39, common-mistakes.md:11. Source notebook: "_1-minimal_, meaning that every character contained is required to produce the error". Fix: quote added.
11. **WARNING — Hypothesis shrink claim lacked its strongest source line.** SKILL.md:35, interestingness-and-replay.md:34. Source hypothesis `hypothesis/docs/tutorial/flaky.rst` (HypothesisWorks/hypothesis 9ab0be61aaaa27396fc1bbf4b34e7925cc68d1e2): non-deterministic strategies leave Hypothesis "unable to shrink to a minimal failing input"; "Only the sequence of calls to Hypothesis APIs like ``draw``" and the pass/fail outcome need be deterministic; sources include "thread scheduling, network timing". Fix: quotes added; claims otherwise accurate.
12. **INFO — Hypothesis replay claims verified.** tool-recipes.md:41, common-mistakes.md:9, SKILL.md:41 against `replaying-failures.rst`: "examples provided using |@example| do not shrink"; "the binary blob is not stable across Hypothesis versions"; database key may change with source. Fix: quote fragments added; no misstatement.
13. **WARNING — Regehr section numbers imprecise.** SKILL.md:8 cited §5.2 for invalid behavior; SKILL.md:12 cited §5.2 for the crash-vs-wrong-code validity split. Page images (paper-reader pngs page-003/004/009, reread this session): §5.1 "The Validity Problem" defines dynamic invalidity; the crash/wrong-code split is §5.2.4 "Validity for Compiler-Crash Inputs": "weaker validity requirements than do the test cases for wrong-code bugs"; §7.5: "naïve reducers tend to introduce problematic undefined" behavior (12 of 41, 29%); §7.7: "wrong-code bugs have no obvious fingerprint" and "Non-deterministic execution of the system under test can cause test-case reduction to fail"; §3: "all test-case minimization work that we are aware of is heuristic"; §4: "removing an argument from a function and simultaneously all its call sites". Fix: section numbers corrected to §§4, 5.1, 7.5, 7.7 and §§5.1, 5.2.4; quotes added at SKILL.md:8,12,16,35,39.
14. **WARNING — llvm-reduce/libFuzzer flags paraphrased loosely.** tool-recipes.md:19,25,35. Source text: `--in-place` "will replace your input file with the reduced version"; `--abort-on-invalid-reduction` "Abort if any reduction results in invalid IR"; `--test-arg` exists; `-merge=1` minimizes "while still preserving the full coverage"; `-reduce_inputs` "while preserving their full feature sets"; `-exact_artifact_path`: "Do not use the same path for several parallel processes." Fix: exact fragments substituted; no claim was wrong.
15. **WARNING — common-mistakes.md was a two-column table, not WRONG-first/RIGHT/why pairs.** common-mistakes.md:3-11. Governing rule: skill-draft Step 3 ("WRONG first, then RIGHT ... a one-line *why*"); house style bugfinding-campaign/references/common-mistakes.md uses Wrong/Better headed entries. Fix: the same seven entries converted to headed Wrong/Right/Why entries, each cited and quoted; closing paragraph unchanged.
16. **WARNING — uncited normative sentences in SKILL.md.** SKILL.md:12 (retain original), :14 (accept only when operation and violation remain), :29 (exercise the original through the interface). Sources: `creduce.in` line 1074 backup comment "is useful when reductions go wrong"; Regehr §6 (page 5) the test "determines if the variant triggers the compiler bug and also, if necessary," checks validity; `creduce.in` help "the interestingness test is flawed". Fix: citations/quotes added. Remaining uncited sentences are routing, authorization, or explicitly labeled pack conventions (SKILL.md:33 last sentence, :35 "no fixed retry count", :39 handoff list; interestingness-and-replay.md convention table; worked-reductions.md, which states it is "this pack's illustrative experiment designs"). Not cut: no primary source contradicts them and they are labeled as pack policy.
6. **WARNING — llvm-reduce exit status detail.** tool-recipes.md:25 said "Normal reducer exit is distinct from final target replay" without the documented code. Source `llvm-reduce.md` EXIT STATUS: "Returns 2 if the interestingness test reported the initial input was not interesting." Fix: added.

## Pinned URLs

SHAs resolved with `gh api repos/<org>/<repo>/commits/<branch> --jq .sha`; every file below was downloaded at that SHA and read before citing. Raw files carry no rendered anchors, so the old `#options` anchor was replaced by the section name in the link text.

| Old | New |
|---|---|
| raw creduce `/master/creduce/creduce.in` | `https://raw.githubusercontent.com/csmith-project/creduce/31e855e290970cba0286e5032971509c0e7c0a80/creduce/creduce.in` |
| raw creduce `/master/INSTALL.md` | `.../creduce/31e855e290970cba0286e5032971509c0e7c0a80/INSTALL.md` |
| raw creduce `/master/COPYING` | `.../creduce/31e855e290970cba0286e5032971509c0e7c0a80/COPYING` |
| raw llvm-project `/main/LICENSE.TXT` | `https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/LICENSE.TXT` |
| `https://llvm.org/docs/CommandGuide/llvm-reduce.html` (built from main) | `.../llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/llvm/docs/CommandGuide/llvm-reduce.md` |
| `https://llvm.org/docs/LibFuzzer.html#options` | `.../llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/llvm/docs/LibFuzzer.md` |
| Hypothesis `/en/latest/tutorial/flaky.html` | `https://raw.githubusercontent.com/HypothesisWorks/hypothesis/9ab0be61aaaa27396fc1bbf4b34e7925cc68d1e2/hypothesis/docs/tutorial/flaky.rst` |
| Hypothesis `/en/latest/tutorial/replaying-failures.html` | `.../hypothesis/9ab0be61aaaa27396fc1bbf4b34e7925cc68d1e2/hypothesis/docs/tutorial/replaying-failures.rst` |
| `https://go.dev/doc/security/fuzz/` | `https://raw.githubusercontent.com/golang/website/a8b66266e226994e2ead51317bace3ee83cedab9/_content/doc/security/fuzz/index.md` |
| `https://www.debuggingbook.org/html/DeltaDebugger.html` | `https://raw.githubusercontent.com/uds-se/debuggingbook/35dfb6c7a1932e4d5e9ca9858b4b1e80eb7447a5/notebooks/DeltaDebugger.ipynb` |

Unchanged: `https://www.cs.utah.edu/~regehr/papers/pldi12-preprint.pdf` (fixed author preprint, not a moving alias). sources.yaml urls and sections_used updated to match.

## Validation

```text
python C:/Users/Q/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/bugfinding/skills/failure-reduction
Skill is valid!

read-only probe (inline cited URLs vs sources.yaml, local links, moving-branch URLs, required fields, file endings):
cited-not-in-yaml []
yaml-not-cited []
errs []
SKILL.md 41 lines ends-ok
common-mistakes.md 61 lines ends-ok
interestingness-and-replay.md 36 lines ends-ok
tool-recipes.md 41 lines ends-ok
worked-reductions.md 25 lines ends-ok
sources.yaml 68 lines ends-ok

git diff --check -- plugins/bugfinding/skills/failure-reduction
[no output] diff-check exit 0
```

Quote probe: every double-quoted fragment from a web source was found verbatim (whitespace-normalized) in the downloaded pinned files. The eight paper fragments (§§3, 4, 5.1, 5.2.4, 6, 6.1, 7.5, 7.7) were checked by reading paper-reader page images page-002, page-003, page-004 and page-009 this session.

## Unverified

- Hypothesis master at the pinned SHA keeps docs under `hypothesis/docs/`; I did not confirm that this tree matches the currently published readthedocs release. Cited text matches the claims either way.
- llvm.org/docs and go.dev are built from the pinned repositories' default branches; that the deployed pages equal these SHAs is assumed, not checked.
- Regehr §6 page 6 (C-Reduce transformation list) was not reread this session; no claim rests only on it (the §§3–4 and 6 citation's quote is from §4, page 3).
- No reducer, command example or interestingness test was executed; recipes remain source-documented, unexecuted.

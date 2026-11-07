# Improve corpus-evolution: citation and content audit

Skill: `plugins/bugfinding/skills/corpus-evolution/`. Accessed 2026-11-07.

## Findings

Raw sources were downloaded read-only at pinned commits into the session scratchpad and grepped/read directly (not via a summarising fetch). Fix status is updated below as each edit lands.

1. **ERROR** `SKILL.md:12,18`, `references/common-mistakes.md:5`, `references/selection-and-retention.md:3`, `references/tool-recipes.md:23`, `references/sources.yaml:18` — cited `https://llvm.org/docs/LibFuzzer.html`, a moving page built from llvm-project `main`. Source read: `https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/llvm/docs/LibFuzzer.md` (the old `LibFuzzer.rst` path 404s at this SHA; the doc is now Markdown). Fix: pin every link to that permalink.
2. **ERROR** every `https://aflplus.plus/docs/fuzzing_in_depth/` link (SKILL.md:18,24; common-mistakes.md:7; exchange-and-replay.md:11,19; selection-and-retention.md:3; tool-recipes.md:7) — moving rendered site. Source read: `https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/docs/fuzzing_in_depth.md` (same SHA as the existing pinned cmin/LICENSING links). Fix: pin.
3. **ERROR** every `https://go.dev/doc/security/fuzz/` link — unversioned page. Source read: `https://raw.githubusercontent.com/golang/website/a8b66266e226994e2ead51317bace3ee83cedab9/_content/doc/security/fuzz/index.md`. Fix: pin.
4. **ERROR** every `https://google.github.io/oss-fuzz/advanced-topics/corpora/` link — built from `master`. Source read: `https://raw.githubusercontent.com/google/oss-fuzz/156f862e5976b3d23828230a0a5b4fef54074d32/docs/advanced-topics/corpora.md`. Fix: pin.
5. **ERROR** `references/tool-recipes.md:7` — "Select coverage inputs into a distinct empty destination" cited only the depth guide §2, which does not mention an empty destination. The requirement is in source: non-merge mode fails with `"Output directory '%s' is not empty"` (`src/afl-cmin.c` at d007072, ~line 3518). Fix: cite the cmin source for the empty-output requirement.
6. **WARNING** `references/tool-recipes.md:13` — said `afl-merge` comes from "the inspected 2026-11-07 source" only. The depth guide §2b at the same SHA documents it: "it only appends inputs that cover something the output corpus does not already cover", plus a positional form. Source usage: "existing output files are never changed or removed". Fix: cite both with quotes.
7. **WARNING** `references/tool-recipes.md:19` — "Check its crash/timeout policy" did not state the policy. Source usage text: `-A` "allow crashes and timeouts (not recommended)"; `-C` "keep crashing inputs, reject everything else". So by default a cmin/merge pass leaves crashing and timing-out inputs out of the selected output: running it over a set that contains failures drops them from the output. Source also says "Only the first %ld bytes of an input are given to the target." with `MAX_FILE` = `1 * 1024 * 1024L` (`include/config.h` at d007072, line 314). Fix: state both.
8. **WARNING** `references/tool-recipes.md:31` — no quotes for load-bearing libFuzzer flags; `-minimize_crash` had no attempt bound. Source: `-reduce_inputs` "Try to reduce the size of inputs while preserving their full feature sets; defaults to 1."; `-minimize_crash` "Use with -runs=N or -max_total_time=N to limit the number of attempts."; resume by "executing the same command"; file list "will not perform any fuzzing". Fix: add quotes and the attempt bound.
9. **WARNING** `references/tool-recipes.md:35` (Go) — left out that Go minimizes before saving: "the fuzzing engine will attempt to minimize the input" then writes it to `testdata/fuzz/...`. So the saved failure is the minimized value, not the original mutated input. Fix: state it, cited.
10. **INFO** `references/exchange-and-replay.md:3` — gap: the Go doc names the documented producer for raw-file import: `file2fuzz` "can be used to convert these binary files to corpus files encoded for `[]byte`". Fix: one sentence; it does not convert to `string` or other argument types.
11. **WARNING** `references/tool-recipes.md:37` — "project contact access is required" was imprecise. Source: "you must be listed as the primary contact or as an auto cc in the project's `project.yaml` file". The corpora are "synthesized by the fuzzing engines" and the bucket path is per engine and target (`.../libFuzzer/expat_parse_fuzzer`). Fix: state it with quotes.
12. **ERROR** `references/exchange-and-replay.md:19` — "A dictionary token is a mutation hint rather than a complete receiving testcase" was cited to the AFL++ guide, which only says "Adding a dictionary is helpful" and shows `-x`. libFuzzer's Dictionaries section supports the claim: "input language keywords or other interesting byte sequences". Fix: add the libFuzzer citation.
13. **WARNING** `SKILL.md:24` — the sentence "The recipes state their predicate and output owner; they do not install a runtime or establish target applicability" describes this skill's own recipes. Its citations (AFL++ preparation, OSS-Fuzz corpora) do not support it. Fix: drop the citations from that sentence.
14. **WARNING** `references/sources.yaml:6` — `sections_used` names "Preparing the campaign", "Dictionaries", "Multiple cores" and "Checking coverage" do not match the guide's headings. The guide has no "Dictionaries" heading; dictionaries are under "3. a) Running afl-fuzz". Fix: use the real headings.
16. **WARNING** `references/selection-and-retention.md:16` — cited §§2.2, 6.2–6.3 for "model seed reduction as set cover over measured blocks". I checked the paper-reader page images `C:/Users/Q/code/bugfinding-literature/corpus-evolution/papers/Rebert_2014_OptimizingSeedSelection/pngs/page-002..005,008,011,012.png` this session. The set-cover formulation is in §2, "Q1: Seed Selection" (p. 863: "This intuition can be formalized as an instance of the set cover problem"). §2.2 is "Specific Research Questions" (the hypotheses, p. 865). §6.1 is "Establishing Ground Truth" (stack-hash uniqueness, p. 868). §6.2.2 asks "Are reduced seed sets better than a full set?" (p. 871). §6.3 is "Are Reduced Sets Reusable Across Programs?" (p. 872). Fix: cite §2 for set cover. The other section citations check out.
15. **WARNING** `references/common-mistakes.md` — a two-column table with no WRONG/RIGHT labels and no one-line why, unlike the house style (`bugfinding-campaign/references/common-mistakes.md`: heading, **Wrong:**, **Better:**). Fix: convert each row to a Wrong/Better/why entry, keeping the same content and citations.

17. **INFO** quote fragments were added across SKILL.md, exchange-and-replay.md, selection-and-retention.md, tool-recipes.md and common-mistakes.md, one per load-bearing claim. Each comes from the pinned raw files fetched this session or from the Rebert page images viewed this session.

**Fix status:** findings 1–17 are all applied. Finding 15 was applied by rewriting the 11-line `common-mistakes.md` with Write, because changing a table into Wrong/Better/Why entries cannot be done as a small Edit. Content and citations were kept; the licensing row also gained a quote. No claims were cut. The one change of that kind: the unsupported citations were removed from SKILL.md:24 (finding 13), and the sentence stays as a statement about this skill's own recipes.

## Pinned URLs

SHAs resolved with `gh api repos/<org>/<repo>/commits/<branch> --jq .sha` on 2026-11-07, and content fetched at that SHA before citing:

- `https://llvm.org/docs/LibFuzzer.html` → `https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/llvm/docs/LibFuzzer.md` (main)
- `https://aflplus.plus/docs/fuzzing_in_depth/` → `https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/docs/fuzzing_in_depth.md` (stable; same SHA as the existing pinned links)
- `https://go.dev/doc/security/fuzz/` → `https://raw.githubusercontent.com/golang/website/a8b66266e226994e2ead51317bace3ee83cedab9/_content/doc/security/fuzz/index.md` (master)
- `https://google.github.io/oss-fuzz/advanced-topics/corpora/` → `https://raw.githubusercontent.com/google/oss-fuzz/156f862e5976b3d23828230a0a5b4fef54074d32/docs/advanced-topics/corpora.md` (master)
- New source: `https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/include/config.h` (`MAX_FILE`)
- Already pinned and re-read: `src/afl-cmin.c` and `LICENSING.md` at d007072. The USENIX PDF is a fixed proceedings URL.

## Validation

```
$ python C:/Users/Q/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/bugfinding/skills/corpus-evolution
Skill is valid!
exit 0

--- moving-branch URLs:
none
--- cited not in yaml:
--- yaml not cited:
--- local links:
ok references/exchange-and-replay.md
ok references/selection-and-retention.md
ok references/tool-recipes.md
ok references/common-mistakes.md
--- line counts / trailing newline:
SKILL.md 32 lines, last2:  . \n
references/common-mistakes.md 43 lines, last2:  . \n
references/exchange-and-replay.md 19 lines, last2:  . \n
references/selection-and-retention.md 24 lines, last2:  . \n
references/sources.yaml 41 lines, last2:  ] \n
references/tool-recipes.md 37 lines, last2:  . \n
--- diff check:
clean

sources.yaml: 8 entries; fields ok: True   (yaml.safe_load; every entry has exactly name/url/type/accessed/sections_used)

HTTP status of every sources.yaml URL:
200 .../AFLplusplus/.../docs/fuzzing_in_depth.md
200 .../AFLplusplus/.../src/afl-cmin.c
200 .../AFLplusplus/.../include/config.h
200 .../AFLplusplus/.../LICENSING.md
200 .../llvm-project/.../llvm/docs/LibFuzzer.md
200 .../golang/website/.../fuzz/index.md
200 .../oss-fuzz/.../corpora.md
000 usenix PDF via curl (curl exit 43); WebFetch returned application/pdf, 368.7KB. That matches the 377,516-byte canonical PDF in the research report.
```

Skill-audit checks 1–6: the frontmatter name matches the directory and the description is 236 characters. The body is 32 lines. Local links resolve. No ERROR remains.

## Unverified

- The Rebert claims rest on the existing paper-reader notes plus the page images I viewed this session (pp. 2–5, 8, 11, 12). I did not view pp. 6–7, 9–10 or 13–15 this session. Nothing new was taken from them; "2,702" and "368 CPU-days" are confirmed on pp. 8 and 12.
- The `afl-cmin.c` line numbers (~1337–1356, ~3518) refer to the d007072 file and will drift on other revisions.
- I did not check whether the installed `afl-cmin` binary links AGPL files. The skill text already limits the license claim to source provenance.
- No commands were executed against a target.

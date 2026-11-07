# Improve: resource-complexity-testing

Skill: `plugins/bugfinding/skills/resource-complexity-testing/`. Accessed 2026-11-07.

## Findings

PerfFuzz paper evidence: page images `C:/Users/Q/code/bugfinding-literature/resource-complexity-testing/papers/Lemieux_2018_PerfFuzz/pngs/page-000,002,003,004,005,006,009.png` (paper-reader render) viewed directly this session. Section map from the images: §1 Introduction (PDF p.1), §2 overview/walkthrough (pp.2-4), §3 Algorithm (pp.4-5), §4 Implementation (p.5), §5 Evaluation (pp.5-9), §6 Threats to Validity (p.10), §7 Related Work (p.10).

1. `SKILL.md:8`, WARNING. Said: execution counts are the search objective, not a wall-time guarantee, cited `§§2–3`. Source: §3 (PDF p.4) takes "the program components to be CFG edges and the values to be their execution counts"; the wall-time limit is stated in §6 (PDF p.10): identified bottlenecks "may not be the points in which the program spends the most time". Fix: cite §§3, 6 with the §6 quote.
2. `SKILL.md:14`, WARNING. Said: improvements kept "even when total work falls", cited `§3`. Source: that statement is §2 (PDF p.4): saves inputs "even if the mutation reduces the total execution path length"; §3 has only Definition 3 (newMax). Fix: cite §§2–3 with the §2 quote.
3. `SKILL.md:28`, ERROR. Said: "PerfFuzz's fixed-size comparisons", cited `§§4–5`. Source: §4 is Implementation (byte mutations, AFL coverage, perf map) and says nothing about fixed sizes; fixed length is §1 (PDF p.1) "given a fixed input length, maximize the execution count" and §5 (500-byte maximum, PDF p.6; §5.1.2 varied "the upper bound on the input size", PDF p.7). Fix: cite §§1, 5.
4. `references/common-mistakes.md:5`, WARNING. Said: scalar local maxima impede search, cited `§3`. Source: §3 has no local-maxima text; §5.1.1 (PDF p.7) "a greedy approach to maximizing total path length is likely to get stuck in local maxima"; §2 has the non-convex example. Fix: cite §§2, 5.1.1 with quote.
5. `references/search-and-confirmation.md:9`, WARNING. Said: execution counts do not establish latency/retention, cited `§§3–5`. Source: the explicit limitation is §6 (PDF p.10). Fix: add §6.
6. `SKILL.md:20` and `references/runtime-recipes.md:14`, ERROR. Said: the count of 10 is only "the upstream example, not a required threshold" / "the source's example count". Source (benchstat main.go doc comment, Usage, https://raw.githubusercontent.com/golang/perf/be2c69fb417e05de5fec05c732911f4c5f172606/cmd/benchstat/main.go): "Each benchmark should be run at least 10 times to gather a statistically significant sample of results." It is a stated minimum for benchstat's statistics, not only an example. Fix: state the usage recommendation with the quote; keep that it is a sampling floor, not a product budget.
7. `references/search-and-confirmation.md:13` and `references/common-mistakes.md:10`, WARNING (gap). Said: significance supplies no application threshold, without the source's own words. Source (benchstat, Example): "\"statistically significant\" is not the same as \"large\"". Fix: add quote.
8. `references/runtime-recipes.md:18`, INFO. Said "exits124" (missing space) and paraphrase. Source (runner.rst, Misc): "pyperf exits with error code 124. There is no time out by default." Fix: corrected spacing, added quote. Same spacing defects fixed at `runtime-recipes.md:27` ("Python>=3.11") and `:31`/`:37` ("Clang3.8", "Clang8", "Apache2.0").
9. `references/runtime-recipes.md:27`, WARNING (gap). Said comparison does not rerun the subject; did not say how compare_to decides significance or what check tests. Source (cli.rst): compare_to "use the first file as the reference" and decides significance with "a Student's two-sample, two-tailed t-test"; check: "Warn if the standard deviation is greater than 10% of the mean". Fix: added both, cited.
10. `references/metrics-and-lifecycle.md:10`, WARNING. Said pyperf track-memory is "Linux private mappings" without saying it is a peak on Linux too. Source (runner.rst, Misc): "--track-memory: get the memory peak usage" then Linux sums `Private_Clean` and `Private_Dirty`. Fix: label both platforms as peak, quote.
11. `references/runtime-recipes.md:37`, INFO. Said afl-showmax sets leak detection off "in its default ASan environment". Source (afl-showmax.c `set_up_environment`): `setenv("ASAN_OPTIONS", ... "detect_leaks=0:" ..., 0)`; the final `0` means it applies only when `ASAN_OPTIONS` is unset. Fix: say "when `ASAN_OPTIONS` is unset" and quote.
12. `references/metrics-and-lifecycle.md:19`, ERROR (uncited normative sentences). "Keep profiler-instrumented and production-cost observations distinct" carried no citation and no pack-rule label. Source: tracemalloc `start()`: "Storing more frames increases the memory and CPU overhead"; pprof `Profile.Add`: value "will not be garbage collected until the corresponding call to [Profile.Remove]". Fix: cited; the remaining lifecycle sentences labeled as this pack's rule (as line 21 already does).
13. `references/common-mistakes.md` (whole file), WARNING. Was a two-column table with no one-line why per entry, unlike the skill-draft Step 3 / sibling `transactional-history-testing` WRONG/RIGHT/Why pairs. Fix: converted each row to Wrong/Right/Why sections, keeping every entry and citation; added quotes.
14. `references/runtime-recipes.md:37`, INFO, not changed. The README says seeds must be "of smaller size than ```num``` bytes", but its own insertion-sort example makes a 64-byte seed (`head -c 64 /dev/zero`) and runs `-N 64`. The skill follows the README's prose rule; no edit beyond quoting it.
15. `references/common-mistakes.md` (B/op entry) and `references/metrics-and-lifecycle.md:7`, WARNING (gap). The claim that allocation deltas include churn rested only on benchmark.go, which shows the deltas but not that TotalAlloc ignores frees. Source (runtime/mstats.go at the same Go SHA, `MemStats.TotalAlloc`, https://raw.githubusercontent.com/golang/go/dcc06a82727b447270b1a58cc5f86b49736e317c/src/runtime/mstats.go): "it does not decrease when objects are freed". Fix: cited with quote; new sources.yaml entry.
16. `references/search-and-confirmation.md:15`, INFO (gap). Said Go's runner "resets counters" before running. Source (benchmark.go `runN`): calls `runtime.GC()` "by clearing garbage from previous runs", `ResetTimer`, `StartTimer`, the benchmark function, `StopTimer`, and defers `b.runCleanup`. Fix: stated GC and cleanup; other state is the benchmark's responsibility.
17. `references/search-and-confirmation.md:23`, INFO (gap). The native-handle case had no Go owner for live handles. Source (pprof.go Profile doc): custom profiles' "most common use is for tracking resources that must be explicitly closed, such as files or network connections". Fix: one cited sentence telling the reader to reuse such an existing owner (no new tool).
18. Quotes added (all from text retrieved this session) to SKILL.md:8, 14, 18, 20, 22, 28; metrics-and-lifecycle rows 7-11 and lines 13, 17; runtime-recipes 14, 18, 27, 31, 37; search-and-confirmation 9, 13, 15, 23. In SKILL.md:22 the two-quote sentence was split so each quote's first following link is its own source.
19. `references/sources.yaml`, WARNING. sections_used were coarse ("sections 2-5", "Run; Interpret") and PerfFuzz's no longer matched the corrected section cites. Fix: sections_used rewritten per entry to the sections actually cited; MemStats entry added.

No claims were cut: every claim found a primary source or is explicitly labeled as this pack's convention.

## Pinned URLs

None needed re-pinning: every GitHub URL was already at a full 40-hex commit SHA (perffuzz f937f370555d0c54f2109e3b1aa5763f8defe337, golang/go dcc06a82727b447270b1a58cc5f86b49736e317c, golang/perf be2c69fb417e05de5fec05c732911f4c5f172606, psf/pyperf 2ed9b9ed4d56448b6a19b6236c7a519a62f6dfe5, python/cpython 0e98aea32593e39c647c2b3d7054ec4e36bf643a). The one added URL (`src/runtime/mstats.go`) uses the same pinned Go SHA. All ten existing URLs plus the new one were fetched with curl this session (all HTTP 200; PDF HEAD 200, 13,443,941 bytes, matching the paper-reader copy). No `/latest/` or `/stable/` links.

## Validation

```
$ python C:/Users/Q/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/bugfinding/skills/resource-complexity-testing
Skill is valid!
exit=0
--- cited URLs not in sources.yaml / yaml not cited
match
--- refs per host/ref
githubusercontent.com/carolemieux/perffuzz/f937f370555d0c54f2109e3b1aa5763f8defe337
githubusercontent.com/golang/go/dcc06a82727b447270b1a58cc5f86b49736e317c
githubusercontent.com/golang/perf/be2c69fb417e05de5fec05c732911f4c5f172606
githubusercontent.com/psf/pyperf/2ed9b9ed4d56448b6a19b6236c7a519a62f6dfe5
githubusercontent.com/python/cpython/0e98aea32593e39c647c2b3d7054ec4e36bf643a
--- moving
none
--- local links
SKILL.md:](references/common-mistakes.md)
SKILL.md:](references/metrics-and-lifecycle.md)
SKILL.md:](references/runtime-recipes.md)
SKILL.md:](references/search-and-confirmation.md)
references/runtime-recipes.md:](metrics-and-lifecycle.md)
(all five targets exist)
--- diff check
diffcheck exit=0
--- trailing (last two bytes of each file)
SKILL.md .\n
references/common-mistakes.md .\n
references/metrics-and-lifecycle.md .\n
references/runtime-recipes.md .\n
references/search-and-confirmation.md .\n
references/sources.yaml "\n
30 SKILL.md
```

Quote check: `grep -F` of each non-paper quote against the fetched files found every fragment; the four that returned 0 (benchstat "should be run at least 10 times", "computes the median and the confidence interval for the median", "each benchmark in the first file to the same benchmark"; pyperf "the peak value of the Commit Charge ...") span a line break with a `//` or indentation prefix in the source and were confirmed by reading the printed source. Paper quotes were checked against the page images listed above.

## Unverified

- The pyperf compare_to quote "a Student's two-sample, two-tailed t-test" is the rendered text of an RST link whose source starts with a backtick before "Student's".
- The README's seed-size rule conflicts with its own example (finding 14); which one the fork's `afl-fuzz` enforces was not checked in its source.
- Nothing was executed against a target; command shapes remain source-read, as the skill already says.

# Improve bugfinding-campaign

Target: `plugins/bugfinding/skills/bugfinding-campaign/` (SKILL.md and references/). Accessed 2026-11-07.

## Findings

Files read: SKILL.md (57 lines), references/campaign-example.md, common-mistakes.md, pilot-diagnosis.md, sources.yaml; skill-draft, skill-audit, skill-improve common-mistakes; reports/research-bugfinding-campaign.md. Elle evidence: `C:/Users/Q/code/papers/Kingsbury_2020_ElleInferringIsolationAnomalies/` (listed in `_reader_done.tsv`, page images in `pngs/`). Fetching every cited URL next.

All 10 cited sources were fetched 2026-11-07 (rendered pages with WebFetch; GitHub-hosted docs also as raw Markdown at the pinned SHA; libFuzzer at releases.llvm.org/23.1.0; Elle page images pp. 3, 7, 12 viewed directly from `pngs/page-002.png`, `page-006.png`, `page-011.png`). Every rendered-page claim below was rechecked by grep against the pinned raw file.

### F1. SKILL.md:8 — WARNING — misstated source
- Text: ClusterFuzz performance cited for "high execution counts alone do not establish useful reach".
- Source: the page says "**Speed** is crucial for fuzzing ... The faster a fuzz target generates testcases, the better", and lists code coverage growth and blocking issues as separate factors ([analyzing-fuzzer-performance.md, Performance factors](https://raw.githubusercontent.com/google/clusterfuzz/77bbad2432fb931906c523786defac928d12afdb/docs/using-clusterfuzz/workflows/analyzing-fuzzer-performance.md)). It does not say high speed fails to establish reach; it says speed is one factor alongside "Code coverage should grow over time".
- Fix: reworded to "speed is one listed factor beside coverage growth and blocking issues", with quote fragments.

### F2. SKILL.md, pilot-diagnosis.md, campaign-example.md, common-mistakes.md — WARNING — moving URLs
- Text: `google.github.io/oss-fuzz/...`, `google.github.io/clusterfuzz/...`, `google.github.io/fuzzbench/...`, `aflplus.plus/docs/...` are rendered from default-branch Markdown (front matter `permalink:` confirmed in each raw file); `llvm.org/docs/LibFuzzer.html` currently renders "LLVM 24.0.0git" (trunk).
- Fix: pinned to raw files at resolved SHAs and to `releases.llvm.org/23.1.0/docs/LibFuzzer.html#options` (latest release tag `llvmorg-23.1.5`; 23.1.0 docs page exists and contains the same option text). See Pinned URLs. sqlite.org/testing.html has no versioned URL; kept (Unverified).

### F3. SKILL.md:14 — WARNING — gap the source exposes
- Text: cites SQLite dbsqlfuzz as a "concrete precedent" without saying it is unavailable.
- Source: "The dbsqlfuzz engine is a proprietary fuzz tester." ([SQLite §2](https://www.sqlite.org/testing.html)); §4.1.3 "mutates both the SQL input and the database file at the same time".
- Fix: added both quote fragments; the precedent is the mechanism, not an installable tool.

### F4. SKILL.md:25 — INFO — load-bearing claim lacked quotes
- Source: Elle p. 3 §3 "blind writes to a register “destroy history”"; p. 7 §4.3 the approach "comes close to guaranteeing completeness" (sound, not complete); p. 12 §9 "Our approach ignores predicates and deals only in individual objects".
- Fix: added quote fragments.

### F5. SKILL.md:53 and pilot-diagnosis.md:12,15 — WARNING — scope omitted
- Source: ClusterFuzz performance "this page only applies to fuzz targets doing coverage guided fuzzing with libFuzzer or AFL"; "If a target finds many new crashes, fixing them is probably more important than analyzing performance."
- Fix: SKILL.md:53 now quotes the crash-first sentence and states the libFuzzer/AFL scope.

### F6. pilot-diagnosis.md:13 — WARNING — overstated fields
- Text: "Reproduction reliability and affected build/platform information".
- Source: triage page lists reliability of reproducing as a filter, "the regression range is often the most useful information for triage", and tracks "which platform issues reproduce on" ([triaging-new-crashes.md](https://raw.githubusercontent.com/google/clusterfuzz/77bbad2432fb931906c523786defac928d12afdb/docs/using-clusterfuzz/workflows/triaging-new-crashes.md)). No "affected build" field.
- Fix: "reproduction reliability, regression revision range and platform".

### F7. pilot-diagnosis.md:11 — INFO — section label
- Text: "AFL++ §1" for comparison-solving instrumentation. Source at SHA: "### b) Selecting instrumentation options" covers laf-intel/COMPCOV and CMPLOG ("usually a better one than laf-intel").
- Fix: cite §1.b with quote "This technique is called laf-intel or COMPCOV".

### F8. pilot-diagnosis.md:31 — WARNING — gap the cited source exposes
- Text: "If the control survives, investigate the oracle or reach".
- Source: SQLite §7.6 "Such branches generate false-positives during mutation testing" (branches that only change speed, not output).
- Fix: added that a surviving mutant can be output-equivalent, so check that before blaming oracle or reach.

### F9. pilot-diagnosis.md:33 — INFO — load-bearing quote
- Source (libFuzzer 23.1.0 Options): `-timeout`/`-rss_limit_mb`: "the process is treated as a failure case"; `-max_total_time`: "maximum total time in seconds to run the fuzzer".
- Fix: added fragment so the runner-limit failure is not read as a product defect without classification.

### F10. common-mistakes.md (all 7 entries) — ERROR — skill-draft Step 3 pattern
- Text: Wrong/Better pairs without the required one-line why.
- Fix: added a cited `**Why:**` line to each entry; kept the existing Wrong/Better labels used across the pack.

### F11. sources.yaml — WARNING — inaccurate sections_used / urls
- `Elle` lists "6. Finding Counterexamples (page 9)" but no file cites §6; removed. OSS-Fuzz Ideal Integration lists "Fuzz Target" (used, "make at least some progress"), "Seed Corpus" (used), "Coverage" (used), "Performance" (not cited anywhere); removed "Performance". AFL++ "Instrumenting the target" kept as "1.b Selecting instrumentation options". Urls updated to pinned forms.

### F12. SKILL.md:39 — INFO — citation attached to pack design
- Text: SQLite §7.6 cited for "Keep this proportional ..., not a recurring approval round", which §7.6 does not say.
- Fix: moved the citation to the control sentence with quote "verifies that the test suite catches the mutation"; the proportionality sentence now stands as the pack's own guidance, uncited.

### Checks with no defect
- Frontmatter: name matches directory, description third person with what/when clauses; quick_validate passes. SKILL.md 57 lines. Local links resolve. No filler phrases found. No claims cut: every existing claim was supported by its source after rewording (F1, F6).

## Pinned URLs

| Was | Now |
|---|---|
| https://aflplus.plus/docs/fuzzing_in_depth/ | https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/docs/fuzzing_in_depth.md (`stable` branch SHA) |
| https://google.github.io/oss-fuzz/advanced-topics/ideal-integration/ | https://raw.githubusercontent.com/google/oss-fuzz/156f862e5976b3d23828230a0a5b4fef54074d32/docs/advanced-topics/ideal_integration.md |
| https://google.github.io/oss-fuzz/advanced-topics/fuzz-introspector/ | .../156f862e.../docs/advanced-topics/fuzz_introspector.md |
| https://google.github.io/oss-fuzz/advanced-topics/reproducing/ | .../156f862e.../docs/advanced-topics/reproducing.md |
| https://google.github.io/clusterfuzz/using-clusterfuzz/workflows/analyzing-fuzzing-performance/ | https://raw.githubusercontent.com/google/clusterfuzz/77bbad2432fb931906c523786defac928d12afdb/docs/using-clusterfuzz/workflows/analyzing-fuzzer-performance.md |
| https://google.github.io/clusterfuzz/using-clusterfuzz/workflows/triaging-new-crashes/ | .../77bbad24.../docs/using-clusterfuzz/workflows/triaging-new-crashes.md |
| https://google.github.io/fuzzbench/reference/report/ | https://raw.githubusercontent.com/google/fuzzbench/3234e151d70f6093272a9b4155e68ee57faf986c/docs/reference/report.md |
| https://llvm.org/docs/LibFuzzer.html#options | https://releases.llvm.org/23.1.0/docs/LibFuzzer.html#options |

Each raw file's front matter `permalink:` equals the rendered path it replaces. SHAs from `gh api repos/<org>/<repo>/commits/HEAD --jq .sha` (AFL++: `commits/stable`), content fetched at that SHA.

## Validation

```
$ python C:/Users/Q/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/bugfinding/skills/bugfinding-campaign
Skill is valid!
--- cited not in yaml
--- yaml not cited
--- moving   (grep for /main/ /master/ /HEAD/ /latest/ /stable/ llvm.org/docs google.github.io aflplus.plus)
--- local links
ok references/pilot-diagnosis.md
ok references/campaign-example.md
ok references/common-mistakes.md
--- diff check
rc=0
SKILL.md last2=.\n ; campaign-example.md .\n ; common-mistakes.md .\n ; pilot-diagnosis.md .\n ; sources.yaml '\n
57 SKILL.md
```

## Unverified
- `https://www.sqlite.org/testing.html` has no versioned URL; kept as is. Quotes checked against the page fetched 2026-11-07.
- Elle (arXiv abs page) was not re-fetched as HTML; claims checked only against page images pp. 3, 7, 12 in the existing collection, which was produced by an earlier run (research report says paper-process --light, plus direct page-image viewing). I viewed those page images myself this session; I did not re-run paper-reader.
- Sibling skills still cite the unpinned `google.github.io`/`aflplus.plus`/`llvm.org/docs` URLs; out of scope for this job.

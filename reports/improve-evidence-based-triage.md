# Improve evidence-based-triage

## Findings

Progress: read all 5 skill files, governing skill-draft/skill-audit/skill-improve, research and draft reports. Viewed Elle page images page-006 (printed p.7), page-008 (p.9), page-011 (p.12) from C:/Users/Q/code/papers/Kingsbury_2020_ElleInferringIsolationAnomalies/pngs/. Elle claims at SKILL.md:19, common-mistakes.md:10, triage-decisions.md:13, maintainer-handoff.md:22 match those pages (§4.3 soundness "anomaly should exist in every interpretation"; §6 "human-readable explanation for the cycle"; §9 "Our approach ignores predicates").

Primary text read this session from version-pinned raw sources (the rendered docs sites are built from these files): ClusterFuzz docs at google/clusterfuzz@77bbad2432fb931906c523786defac928d12afdb (docs/using-clusterfuzz/workflows/triaging-new-crashes.md, docs/reference/glossary.md); OSS-Fuzz docs at google/oss-fuzz@156f862e5976b3d23828230a0a5b4fef54074d32 (docs/advanced-topics/reproducing.md); LLVM docs at llvm/llvm-project@635f30899dd0914fa89f0b3dc9a9e548e6d0ceec (llvm/docs/LibFuzzer.md, llvm/docs/HowToSubmitABug.md); Go docs at golang/website@a8b66266e226994e2ead51317bace3ee83cedab9 (_content/doc/security/fuzz/index.md). Live-page anchors checked with curl: llvm.org LibFuzzer `q-when-libfuzzer-is-not-a-good-solution-for-a-problem`, `fuzz-target`; HowToSubmitABug `miscompilations`, `ai-policy`, `introduction-got-bugs`; go.dev `failing-input`, `corpus-file-format`, `suggestions`.

### F1 — SKILL.md:8 — WARNING (citation does not support sentence)
- Text: "Use the project's existing records rather than introduce a verdict database ([ClusterFuzz triage](...))".
- Source: the triage page says nothing about avoiding a verdict database. It describes per-testcase records filterable by crash type, crash state, fuzzer, job and "[Reliability] of reproducing the crash", and says cause-finding from stacks "is more of an art than an exact science, and there is no one process to follow" (https://raw.githubusercontent.com/google/clusterfuzz/77bbad2432fb931906c523786defac928d12afdb/docs/using-clusterfuzz/workflows/triaging-new-crashes.md, Filtering testcases; Crash stacktrace).
- Fix: keep the instruction; cite only what the page says (reliability recorded separately; no single cause-finding process), with quotes.

### F2 — SKILL.md:14, SKILL.md:27, common-mistakes.md:5, common-mistakes.md:6, triage-decisions.md:17 — ERROR (moving-branch URL)
- Text: `raw.githubusercontent.com/google/oss-fuzz-gen/main/agent/...`.
- Fix: pinned to google/oss-fuzz-gen@c0982c5d40a7e93ce70fd319705804b9a29954d0 after re-reading the files at that SHA (see F-OSSFG findings below); sources.yaml updated.

OSS-Fuzz-Gen at c0982c5d40a7e93ce70fd319705804b9a29954d0 read this session: crash_analyzer.py lines 51-168 (`_initial_prompt`, `_container_handle_conclusion` lines 113-117 set `crash_result.true_bug`, `_container_tool_reaction` lines 137-156 require GDB use and reject hallucinated GDB output); semantic_analyzer.py lines 1-160 (`CRASH_EXCLUSIONS = re.compile(r'.*(slow-unit-|timeout-|leak-|oom-).*')`, `EARLY_FUZZING_ROUND_THRESHOLD = 3`, null-deref/signal/exit/OOM/near-init handling, comment "This is very likely the false positive cases."). Existing claims about this code are accurate.

### F3 — SKILL.md:12 — WARNING (uncited claims, missing quotes, bare-page cite)
- Text: "Link original and reduced artifacts separately" uncited; replay requirement paraphrased; libFuzzer claim paraphrased.
- Source: ClusterFuzz glossary Testcase offers "Minimized Testcase" or "Unminimized Testcase"; OSS-Fuzz reproducing: "built with the appropriate sanitizer", `-timeout=65`/`-rss_limit_mb=2560` for timeout/OOM bugs, "reproducible only in 32 bit mode or only in 64 bit mode"; libFuzzer Fuzz Target "in the same process", FAQ "leads to a crash while testing another input", persistent threads "the fuzzing results will be unreliable".
- Fix: cited and quoted each; added the timeout/memory-limit requirement the OSS-Fuzz page states.

### F4 — SKILL.md:14 and SKILL.md:27 — INFO (quote added)
- Fix: added exact code fragments `crash_result.true_bug = True`, "You MUST use the provided GDB tool", "hallucinated interaction with the GDB tool" from the pinned source; SKILL.md:27 now states the analyzer's own guard against fabricated tool output, which supports "Verify ... actual tool results".

### F5 — SKILL.md:18 — WARNING (uncited claim)
- Text: "Check generated harness preconditions before attributing its failure to the product." uncited.
- Source: semantic_analyzer.py `_parse_libfuzzer_logs`: null-deref "normally indicating inadequate parameter initialization or wrong function usage". LLVM Miscompilations: "make sure it is not using undefined behavior".
- Fix: cited both with quotes.

### F6 — SKILL.md:19, SKILL.md:21 — INFO (quotes added)
- Elle §4.3 p.7 "observations are rarely complete"; §9 p.12 "Our approach ignores predicates". Go Failing input: "A panic occurred in the code or the test"; "may fail due to a deadlock or infinite loop, or from intended behavior in the code".

### F7 — SKILL.md:20 — WARNING (bare URL without section; citation partially supports)
- Text: cited bare `https://llvm.org/docs/LibFuzzer.html` for replay misses; no definition of reproduction reliability.
- Source: libFuzzer FAQ anchor `#q-when-libfuzzer-is-not-a-good-solution-for-a-problem`; ClusterFuzz glossary "consistently crashes with the same crash state"; Go Suggestions "in parallel across multiple workers and in nondeterministic order"; ClusterFuzz triage Crash statistics "For a non-reproducible crash".
- Fix: anchored libFuzzer link; added reliability definition and Go nondeterministic-order fact with citations; named the triage section.

### F8 — SKILL.md:29 — WARNING (claim stronger than source)
- Text: "A stack signature is a grouping aid, not proof that every member has one cause" cited to glossary, which actually defines crash state as used "for deduplication purposes" — ClusterFuzz does use it to dedupe.
- Fix: quoted the definition and stated the factual basis (derived from the stack, not a demonstrated mechanism); quoted Minimization "the same underlying bug".

### F9 — SKILL.md:33 — WARNING (citation covers more than source says)
- Text: "do not invent a successful replay or require a fix before recording evidence ([LLVM reporting])" — LLVM page says neither.
- Source: LLVM Introduction: "All information necessary to reproduce the problem", "The reduced test case that triggers the bug".
- Fix: citation attached only to the invocation/reduced-testcase sentence, with quotes and `#introduction-got-bugs` anchor; the skill's own directive left uncited as a procedure instruction.

### F10 — references/common-mistakes.md:3-12 — ERROR (format: no WRONG/RIGHT pairs with why; bare-page and moving URLs)
- Text: a two-column table with no one-line why; links to `/main/` source and bare libFuzzer/Go pages.
- Fix: converted each row into the house `## heading / **Wrong:** / **Better:** / **Why:**` form used by bugfinding-campaign/references/common-mistakes.md; kept every original correction; pinned source links; anchored libFuzzer FAQ and Go `#failing-input`; added quotes (`crash_result.true_bug = True`, `EARLY_FUZZING_ROUND_THRESHOLD = 3`, "very likely the false positive cases", "from the crash stacktrace for deduplication purposes", "is 1 second", "from intended behavior in the code", "observations are rarely complete", "the same underlying bug").

### F11 — references/common-mistakes.md:12 (old) and references/triage-decisions.md:21 — WARNING (gap the source exposes)
- Text: reducer guidance cited only ClusterFuzz's "same underlying bug" goal.
- Source: Go Failing input: the engine "will attempt to minimize the input to the smallest possible and most human readable value which will still produce an error", and the written "Failing input" is that minimized value (https://raw.githubusercontent.com/golang/website/a8b66266e226994e2ead51317bace3ee83cedab9/_content/doc/security/fuzz/index.md).
- Fix: added that Go's minimizer only keeps "which will still produce an error", so the saved Go file's replay error must be compared with the original log. Inside existing replay/reduction scope; no new machinery.

### F12 — references/triage-decisions.md:13 — WARNING (bare-page cites)
- Fix: anchored Go `#failing-input`, libFuzzer FAQ; named glossary section.

### F13 — references/triage-decisions.md:17 — INFO (quotes added, URL pinned)
- Added "very likely the false positive cases" and "Crashes from incorrect fuzz targets will not be counted finally." from pinned semantic_analyzer.py.

### F14 — references/triage-decisions.md:21 — WARNING (paraphrase of type/order rule)
- Fix: quoted Go Corpus file format "must match the fuzzing arguments exactly, in that order" with `#corpus-file-format`.

### F15 — references/triage-decisions.md:23 — INFO
- Added "need a checkout of OSS-Fuzz" (Cloning OSS-Fuzz) to support "not a generic setup command".

### F16 — references/triage-decisions.md:25 — WARNING (link label misnames section)
- Text: "[ClusterFuzz reliability]" pointed at the triage page, whose relevant content is Crash statistics.
- Fix: relabeled to "ClusterFuzz triage, Crash statistics" with quote "For a non-reproducible crash".

### F17 — references/maintainer-handoff.md:3 — WARNING (gap: LLM-assisted handoff policy)
- Text: LLVM cited only for reproduction details; sources.yaml listed "AI policy" but nothing cited it.
- Source: LLVM AI policy: "You must not post any description you don't understand, and any AI assistance must be noted."; fuzzer/AI testcases "should include a brief description of the framework used to generate them".
- Fix: quoted Introduction requirements and added one sentence directing the agent to check the project's own LLM-assistance policy, citing LLVM AI policy (`#ai-policy`). Directly in description scope ("using an LLM to prepare maintainer findings").

### F18 — references/maintainer-handoff.md:20, :22 — INFO (quotes added)
- ClusterFuzz triage: "Reliability of reproducing the crash", "only available for reliably reproducible crashes", "more of an art than an exact science". Elle §6: "to construct a human-readable explanation for the cycle".

### F19 — references/sources.yaml — WARNING (sections_used inaccurate)
- `_initial_prompt` (crash analyzer), `Running` (libFuzzer) and `Reproduce using local source checkout` (OSS-Fuzz) were listed but cited nowhere; OSS-Fuzz `Cloning OSS-Fuzz` and `Build the image and the fuzzers` are now cited but were missing.
- Fix: removed unused sections; added used ones; pinned the two OSS-Fuzz-Gen URLs.

### F20 — docs-site URLs (google.github.io, llvm.org/docs, go.dev) — INFO (not pinned)
- These render from the repos' default branches, so they move, but they carry no `/main/`-style alias and the house skill (bugfinding-campaign) cites the same rendered pages. Kept for consistency; the exact source revisions read are recorded under Pinned URLs below.

## Pinned URLs

- `https://raw.githubusercontent.com/google/oss-fuzz-gen/main/agent/crash_analyzer.py` -> `https://raw.githubusercontent.com/google/oss-fuzz-gen/c0982c5d40a7e93ce70fd319705804b9a29954d0/agent/crash_analyzer.py` (SHA from `gh api repos/google/oss-fuzz-gen/commits/main --jq .sha`; content re-read at the SHA). Occurrences: SKILL.md (2), common-mistakes.md (1), sources.yaml.
- `https://raw.githubusercontent.com/google/oss-fuzz-gen/main/agent/semantic_analyzer.py` -> `https://raw.githubusercontent.com/google/oss-fuzz-gen/c0982c5d40a7e93ce70fd319705804b9a29954d0/agent/semantic_analyzer.py`. Occurrences: SKILL.md (1, new), common-mistakes.md (1), triage-decisions.md (1), sources.yaml.
- Not repointed (F20): google.github.io/clusterfuzz pages verified against google/clusterfuzz@77bbad2432fb931906c523786defac928d12afdb; google.github.io/oss-fuzz against google/oss-fuzz@156f862e5976b3d23828230a0a5b4fef54074d32; llvm.org/docs against llvm/llvm-project@635f30899dd0914fa89f0b3dc9a9e548e6d0ceec; go.dev against golang/website@a8b66266e226994e2ead51317bace3ee83cedab9.

## Validation

Quote check: every double-quoted fragment of 8+ characters in the skill's Markdown was matched against the concatenated pinned raw sources (markdown links stripped, whitespace collapsed). All matched except the Elle quotes (paper; verified by viewing page images p.7, p.9, p.12) and one semantic_analyzer fragment that spanned a `#` comment break; that quote was shortened to "normally indicating inadequate parameter initialization", which matches.

```text
$ python C:/Users/Q/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/bugfinding/skills/evidence-based-triage
Skill is valid!

$ python -c "<read-only probe: inline URLs vs sources.yaml (ignoring #fragment), local links, /main|master|HEAD|latest|stable/ URLs, single trailing newline>"
sources 9 cited 9
{'SKILL.md': 35, 'references\\common-mistakes.md': 57, 'references\\maintainer-handoff.md': 22, 'references\\sources.yaml': 74, 'references\\triage-decisions.md': 25}
errors []

$ git diff --check -- plugins/bugfinding/skills/evidence-based-triage
diffcheck-exit=0
```

Skill-audit checks 1-6: frontmatter name matches directory, description 300 chars (measured with yaml.safe_load), third person, has when-clause; SKILL.md 35 lines; no filler phrases found; local links (3) resolve; description and body aligned (LLM maintainer-finding preparation now also covers project AI-assistance policy). No ERRORs.

## Unverified

- Elle quotes are from page images viewed this session in C:/Users/Q/code/papers/Kingsbury_2020_ElleInferringIsolationAnomalies/pngs/ (collection produced earlier, per the research report, by paper-process --light, not by a fresh paper-reader run). The lead named these images as existing reads; I did not rerun paper-reader.
- Rendered docs pages were checked through their raw source at the stated SHAs and through live-page anchor ids; the live pages may diverge from those SHAs later (F20).
- No claim was cut; every uncited claim found was citable from a source read this session.

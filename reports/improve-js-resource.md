# Improve pass: JS/TS additions to resource-complexity-testing (commit 3e72bc2)

Skill: `plugins/bugfinding/skills/resource-complexity-testing/`. Accessed 2026-11-09.
Scope: every sentence added under `plugins/` in 3e72bc2, checked against its cited pinned source (all 24 raw URLs fetched this session; both paper PDFs fetched and hashed).

## Findings

### F1 references/common-mistakes.md:79 — ERROR
- Said: "It skips only objects whose retained size never changed and drops non-monotone ones only when `monotonicUnboundGrowthOnly` is set".
- Source: ObjectUnboundGrowthAnalysis.ts at 8ac1a3c (https://raw.githubusercontent.com/meta/memlab/8ac1a3c9ed8a9f7076869b4b0abbe7b293986c4d/packages/heap-analysis/src/plugins/ObjectUnboundGrowthAnalysis.ts) skips more than unchanged-size objects: lines 82-85 track only `node.type === 'object' || node.type === 'closure' || node.type === 'regexp'`; lines 107-109 drop a node whose name or type changed; lines 185-187 skip ids absent from the last snapshot; lines 188-190 `if (item.min === item.max) { continue; }`; lines 192-194 `if (item.history[item.history.length - 1] < config.unboundSizeThreshold) { continue; }`; line 206 `.slice(0, 20)`. "skips only" is false (the sibling text in javascript-memory-and-redos.md:19 itself lists the threshold filter).
- Fix: dropped the first "only" ("It skips objects whose retained size never changed ..."). The second "only" (monotone filter gated on the flag, lines 113-116: `if (config.monotonicUnboundGrowthOnly && n < item.max)`) is correct and kept.

### F2 references/javascript-memory-and-redos.md:52 — ERROR
- Said: "Some sites rejected large headers and most accepted only headers under 10,000 characters".
- Source: Staicu 2018 §4.9, printed p.371 (page image `C:/Users/Q/code/papers/Staicu_2018_FreezingWebStudyReDoS/pngs/page-011.png`, read this session; pinned PDF https://www.usenix.org/system/files/conference/usenixsecurity18/sec18-staicu.pdf has sha256 fd8790397f27865f62cc369d52f176b13bddb2155d07a569eb951bc4bc825971, identical to the read copy): "most websites accept headers that are smaller than 10,000 characters, but only few websites accept headers that are, for instance, 40,000 characters long." The paper says most accept headers below 10,000, not that most accept only those (notes.md also records p.372: "over 15% of sites accepted headers longer than 25,000 chars"; p.372 image not re-read).
- Fix: "most accepted headers under 10,000 characters but few accepted 40,000".

## Checked and entailed (no change)

- SKILL.md description and routing sentence: match the memlab plugin README skill table.
- memlab: how-memlab-works (baseline/target/final, "allocated during the target interaction", "but are still alive when they should have been released"); find-web-leaks (default detached DOM + unmounted Fiber, `--trace-all-objects`, "`back` must really undo `action`", no reloads); scenario-api (`repeat` row exact); capture skill (series recipe, settle quote exact, dev builds quote exact, `memlab anonymize`); analyze skill ("grows at every step", "can still be a bounded cache or work in flight"); memory-tests (`takeNodeMinimalHeap` + `tagObject`); NodeHeap.ts lines 93, 152-160 (`v8.writeHeapSnapshot(file)`, parsed in-process); Config.ts lines 544, 546 (`false`, `10 * 1024`).
- Node v26.13.0: v8.md writeHeapSnapshot quotes exact and section has no GC statement; queryObjects quote exact (default returns count); process.md `external`/`arrayBuffers`/`rss` quotes and glibc note exact; perf_hooks "significantly different results and should not be compared directly" exact; cli.md lists `--expose-gc` under V8 options, "_no stability guarantee_" exact, no regexp option.
- V8 in Node v26.13.0: v8-version.h 14.6.202.34; v8-regexp.h kLinear quote exact; flag-definitions.h `regexp_tier_up` true, tier-up quote exact, `regexp_tier_up_ticks` 1, `regexp_results_cache` true, `DEFINE_EXPERIMENTAL_FEATURE` defaults false, `default_to_experimental_regexp_engine` false, fallback text "on excessive backtracking"; regexp.h RegExpResultsCache comment (global exec and @@split).
- recheck: v4.6.2 `pumps`/`suffix`/`base`, formula and "computed in theoretical" exact; main `pump`/`bias`, "not a final verdict" exact; runtime-attack verification "is off by default" exact. (v4.6.2 has "recall validation", whose `recallLimit` counts characters "read by VM"; the claim that real-engine runtime-attack verification exists only on main stands.)
- redos-detector score definition, `1` = no backtracks, `maxScore` default `200`, "considered unsafe" exact.
- eslint-plugin-regexp: no-super-linear-backtracking in `flat/recommended`/`recommended`, "can only detect very simple cases", `report: "certain"` default; no-super-linear-move "quantifiers that cause quadratic moves", `ignorePartial: true` default.
- BLeak (against notes.md; pinned PDF sha256 1e1e268fd3c78507453a1e94c036f59630345b324cb1eb61999dab3810626b28 equals the read copy, as sources.yaml says): same-state snapshots pp.2, 8; Fig. 4 p.6 strict growth at every consecutive snapshot; paths not identity p.5; default 8 round trips p.5; only false positives threshold/timeout, avoidable with more round trips p.11; loop-scope p.4.
- Staicu (against notes.md): §3.2 definition and data-flow filter pp.364-365; §3.4 oracle, CI separation at all k sizes, d_1 < ... < d_k pp.365-366; n_w=3, n_m=5, k=5 p.366; 100 ms-2 s sizing pp.366, 369; 5 s threshold and 2 s budget p.365; one header made a site unresponsive almost a minute p.365; single-thread blocking p.361; availability experiment p.368.
- sources.yaml: all 24 new entries' `evidence_fragment` strings found verbatim in the fetched sources; `sections_used` match the sections read.

## Validation

- `uv run --no-project --quiet --with pyyaml python C:/Users/Q/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/bugfinding/skills/resource-complexity-testing` → `Skill is valid!` (exit 0).
- Relative links in every `.md` under the skill: none broken.
- Cited URLs in `.md` files vs `sources.yaml` `url:` entries: no URL in either set missing from the other.
- `git diff --check`: no output (exit 0).
- Not committed or pushed.

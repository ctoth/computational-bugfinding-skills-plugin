# Draft: JS/TS resource references (group C, resource-complexity-testing)

Status: draft complete, validation passed. Nothing committed or pushed. No tool run against a target.

## Inputs read

- `reports/research-js-resource.md` (R1-R13, decisions, unverified list).
- `reports/skill-plan-js-web-bugfinding.md` resource row (line 38) and Staicu ReDoS bullet (lines 59-64).
- Skill files: `SKILL.md`, `references/search-and-confirmation.md`, `metrics-and-lifecycle.md`, `common-mistakes.md`, `runtime-recipes.md`, `sources.yaml`.
- `reports/draft-resource-complexity-testing.md` (draft-report shape).
- Paper notes: `C:/Users/Q/code/papers/Vilk_2018_BLeakAutomaticallyDebuggingMemoryLeaks/notes.md` (p.N = PDF page N; growth rule p.6, paths not identity p.5, 8 round trips p.5/p.8/p.10, false positives p.11); `C:/Users/Q/code/papers/Staicu_2018_FreezingWebStudyReDoS/notes.md` (printed pages; oracle p.365-366, sizes p.366/p.369, single loop p.361, live-site freeze p.365, availability p.368-369).

## Findings and changes

1. The strictly-increasing-difference rule is not in the skill. `search-and-confirmation.md` "Confirm an actual violation" requires matched controls and variation but no per-step growth condition; `metrics-and-lifecycle.md:21` preserves the family but sets no step rule. Decision: add it once in `search-and-confirmation.md` under "Confirm an actual violation", citing Staicu p.365-366 and BLeak p.6, and have the JS reference point to it.
2. Re-fetched in this turn (curl, read-only, into the session scratchpad) and checked the lines the draft cites: memlab at `8ac1a3c9ed8a9f7076869b4b0abbe7b293986c4d` (`how-memlab-works.md` candidate formula and Fiber detection; plugin README skill table and install; `memlab-find-web-leaks` default filter and `--trace-all-objects`; `scenario-api.md` `repeat`; `ObjectUnboundGrowthAnalysis.ts` node-id tracking, `min === max` skip, size floor; `Config.ts` defaults `monotonicUnboundGrowthOnly = false`, `unboundSizeThreshold = 10 * 1024`; `memlab-analyze-heap-snapshot` "grows at every step" and bounded-cache warning; `memlab-capture-heap-snapshots` series recipe, dev-build note, `memlab anonymize`). Node `v26.13.0` (`v8.md` writeHeapSnapshot caveats and queryObjects; `process.md` memoryUsage fields and glibc note; `perf_hooks.md` monitorEventLoopDelay sampling-mode warning; `cli.md` V8 options "no stability guarantee", no documented regexp option). V8 in that tree: version 14.6.202.34; `v8-regexp.h` kLinear comment; `flag-definitions.h` experimental-engine flags (DEFINE_EXPERIMENTAL_FEATURE defaults false), `regexp_tier_up` true, ticks 1, results cache true; `regexp.h` results-cache comment. recheck `v4.6.2` diagnostics attack structure and "computed in theoretical"; main `f008739a` diagnostics ("not a final verdict", `pump`/`bias`) and runtime verification "off by default". redos-detector `db112c6a` score definition and `maxScore` 200. eslint-plugin-regexp `0a79e7c0` rule docs ("very simplistic", `report: "certain"` default, `ignorePartial` default true, ">1000 character"). All matched the research report.
3. BLeak citation URL: the notes were read from `plasma-umass/BLeak` `master/paper.pdf`; pinned to commit `2b2db0832ea412fa56683de045420134e3c3aa79` (`git ls-remote` HEAD). sha256 of the pinned download equals the local `paper.pdf` the notes were read from (`1e1e268f...6b28`), so the notes' PDF page numbers apply. Staicu PDF URL from the paper's `metadata.json` returns HTTP 200 `application/pdf`.
4. Written: `references/javascript-memory-and-redos.md` (BLeak oracle; memlab routes by purpose with what each observes; Node v26.13.0 observer table; ReDoS candidate producers; Staicu confirmation at the call site; V8 engine configuration). Wording corrections against sources while drafting: Staicu header limits stated as "some sites rejected large headers; most accepted only < 10,000 chars" (notes p.366, p.371), not "many"; `ignorePartial` stated as "does not check regexes used as fragments" (rule doc text).
5. Written: per-step growth rule added once to `search-and-confirmation.md` "Confirm an actual violation" (Staicu §3.4 pp.365-366; BLeak Fig. 4 p.6, p.11). The JS reference points to it rather than restating it.
6. Written: SKILL.md description now names Node.js, browser and React memory leaks, event-loop blocking and ReDoS; one route line added after the runtime-recipes sentence.
7. Written: five `common-mistakes.md` entries (one memlab run as growth; `unbound-object` as confirmed; detector verdict or one slow request as finding; ignoring V8 engine flags; RSS as JS leak). Left out of common mistakes (already covered in the reference, to keep it small): first-call timing, cross-restart snapshot comparison, attacking shared services.
8. Left out on purpose: `--heapsnapshot-near-heap-limit`, `eventLoopUtilization`, libuv threadpool, `sola-da/ReDoS-vulnerabilities` benchmark (belongs to `harness-sensitivity`), redos-detector/recheck ESLint plugins (unread). Not needed for the plan row.
9. Sources: 28 entries appended to `sources.yaml` in the existing schema (name, url, type, accessed, sections_used, evidence_fragment); 39 total. Every evidence fragment was checked against the fetched file on one line, except the two papers (fragments taken from the paper-reader notes). Synthesis sentences in the new reference are labeled "This pack's synthesis", "Inference" or "This pack's rule".

## Files changed

- `plugins/bugfinding/skills/resource-complexity-testing/SKILL.md` (description; one route line)
- `plugins/bugfinding/skills/resource-complexity-testing/references/javascript-memory-and-redos.md` (new)
- `plugins/bugfinding/skills/resource-complexity-testing/references/search-and-confirmation.md` (per-step growth rule)
- `plugins/bugfinding/skills/resource-complexity-testing/references/common-mistakes.md` (five entries)
- `plugins/bugfinding/skills/resource-complexity-testing/references/sources.yaml` (28 entries)
- `reports/draft-js-resource.md` (this report)

## Validation

Default `python` (Python313) has no PyYAML (`ModuleNotFoundError: No module named 'yaml'`); reran with `C:/Users/Q/scoop/apps/python311/current/python.exe`.

```text
quick_validate.py plugins/bugfinding/skills/resource-complexity-testing
Skill is valid!

check_resource_links.py (scratchpad probe: inventory vs cited URLs, local links, mutable main/master/stable/develop URLs)
sources 39 dups []
cited-not-in-inventory []
inventory-not-cited []
errors []

git diff --check -- plugins/bugfinding/skills/resource-complexity-testing
(no output, exit 0; rerun with the new file intent-to-add, exit 0; intent-to-add reset afterwards)
```

`scripts/check_package.py` (the repo's CI check) was read, not run; its sources rules (non-empty list, name, url) are met by the new entries.

## Remaining unverified

- Whether `v8.writeHeapSnapshot` (so memlab's Node assertions) runs a full GC first: Node docs silent; the reference says not to assume one.
- `memlab_sequence_analysis` implementation (MCP server) not read; its "grows at every step" behavior is cited from the skill doc only, and the reference says so.
- Whether any memlab CLI flag sets `monotonicUnboundGrowthOnly`; whether memlab's browser driver forces GC before each snapshot. Not stated in the reference.
- Whether V8's results cache stores failing matches or affects non-global `exec`/`test`: the reference says "not read".
- recheck v4.6.2 JavaScript-dialect semantics and `l`-flag handling not read; the reference names only the v4.6.2 attack fields.
- V8 linear-engine status after Node v26.13.0 not checked; the reference states only the v26.13.0 tree.
- The BLeak "8 round trips" default and false-positive statements come from paper notes (pp.5, 10-11); the BLeak tool itself was not read.
- No command in the reference was executed.


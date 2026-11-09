# Draft report: JS/TS differential extension (group F)

Skills: `semantic-differential-testing`, `configuration-differential-testing`.

## Progress

- Output file created.
- Read: `reports/research-js-differential.md` (all), plan rows `reports/skill-plan-js-web-bugfinding.md:34-35` and LambdaTester bullet, both skills' SKILL.md and all references, `reports/draft-semantic-differential-testing.md`, paper notes (Selakovic lines 85-95, 148-152, 168-212, 245-248; Arteca lines 198-212, 242-246, 276-281).
- Spot-checked research citations against the raw fetched copies in the session scratchpad `src/`: hydrateRoot.md 44-47, 57-58, 87, 194-196, 240, 251, 274, 280-284; ReactFiberHydrationContext.js 388-412, 907-919, 933-945; ReactDOMComponent.js 3265-3285, 3384-3398; codes.json 418-424; flushSync.md 56; useSyncExternalStore.md 48; renderToString.md 54, 127-130; renderToPipeableStream.md 61, 63, 344, 437; emulation.md 383; browsers.md 590; test-projects-js.md 8, 86; module.md 179-189 (module.register deprecated v25.9.0, runtime DEP0205 v26.0.0); nodejs/Release README 5-15, schedule.json v20 end 2026-04-30; assert.md 608-630; util.md 1848-1872. All matched the research report.
- Fetched and checked (scratchpad `f-draft/`): react.dev `captureOwnerStack.md` 54, 386; react `packages/react/npm/index.js`; jazzer.js `instrument.ts` 330-352, 390-400; node v26.13.0 `deprecations.md` 4574-4597 (DEP0205 runtime v26.0.0, doc-only v25.9.0, "will be removed in a future version"); react.dev `errors/index.md` 3; react `formatProdErrorMessage.js` 23; MDN paths under `files/en-us/` return 200; useId.md 174; ecma262 spec.html 2151, 48015-48017; MDN structured clone 12, 16-23.
- Edited `semantic-differential-testing/SKILL.md`: description; one paragraph on React prod/dev hydration observers under "Observe what the contract promises"; one sentence on reference-as-ground-truth (LambdaTester polyfill-vs-native, Nessie cross-commit) under adjudication.
- Edited `worked-paired-cases.md`: new section "Server HTML versus first client render" (research decision 1), proposed renderToString-vs-renderToString comparator labelled unexecuted; five outcomes kept distinct; sensitivity control.
- Edited `matched-state-and-effects.md`: subsection "JavaScript server and client environments" with the nondeterminism/control table (decision 2). Playwright `colorScheme` checked at emulation.md 8, 589; hydrateRoot whitespace cause at 194.
- Edited `comparison-and-normalization.md`: section "JavaScript values and callbacks" (decision 3): isDeepStrictEqual rules, JSON and structured-clone losses, LambdaTester Def 4.1 observation set, Nessie logging, 10-run set rule, Bug/Bug fix/Upgrade. Corrected Nessie's LT re-implementation citation to p.1499 (Arteca notes line 90). No effectiveness counts adopted.
- Edited semantic `common-mistakes.md`: research mistakes 1-10 added in the existing Wrong/Right/Why format. Dropped the research's Base 0 / Cb-Writes 12/13 counts (evidence standard: no effectiveness counts).
- Edited semantic `sources.yaml`: 2 papers (DOI URLs, read via paper-reader notes) and 17 pinned primary sources.
- Edited `configuration-differential-testing/SKILL.md`: description; one sentence pointing to the JavaScript factor section, citing the Release README.
- Edited `factors-and-coverage.md`: section "JavaScript and React factors" with the PICT model, per-factor control/evidence table, sub-model note, single-valued Load note, Jazzer.js floor and DEP0205 interaction (decision 5). Failure string checked at instrument.ts 396-402.
- Edited config `common-mistakes.md` (research mistakes 11-15) and `sources.yaml` (13 pinned sources).
- Note: module.md shows `deprecated: v25.9.0` (documentation deprecation) with runtime deprecation in v26.0.0; research's "runtime since v26.0.0" agrees.

## Deviations from the research

- Cited Nessie's LambdaTester re-implementation reason at p.1499 (Arteca notes line 90), not p.1503.
- Omitted Next.js (research R5 decision: not needed), `use(browser())`, `process.versions.icu` and ICU build variants (unverified probes), and all effectiveness counts.
- Nessie paper section cited as "RQ3" (the notes' label), not a section number.

## Files changed

- `plugins/bugfinding/skills/semantic-differential-testing/SKILL.md`
- `plugins/bugfinding/skills/semantic-differential-testing/references/worked-paired-cases.md`
- `plugins/bugfinding/skills/semantic-differential-testing/references/matched-state-and-effects.md`
- `plugins/bugfinding/skills/semantic-differential-testing/references/comparison-and-normalization.md`
- `plugins/bugfinding/skills/semantic-differential-testing/references/common-mistakes.md`
- `plugins/bugfinding/skills/semantic-differential-testing/references/sources.yaml`
- `plugins/bugfinding/skills/configuration-differential-testing/SKILL.md`
- `plugins/bugfinding/skills/configuration-differential-testing/references/factors-and-coverage.md`
- `plugins/bugfinding/skills/configuration-differential-testing/references/common-mistakes.md`
- `plugins/bugfinding/skills/configuration-differential-testing/references/sources.yaml`
- `reports/draft-js-differential.md` (this report)

No commit, push, or edits outside these files.

## Validation output

```text
uv run --no-project --with pyyaml python C:/Users/Q/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/bugfinding/skills/semantic-differential-testing
Skill is valid!
uv run --no-project --with pyyaml python C:/Users/Q/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/bugfinding/skills/configuration-differential-testing
Skill is valid!
uv run --no-project --with pyyaml python -I <scratchpad>/f-check/check_links.py <both skill dirs>
semantic-differential-testing: sources=29 cited=29
configuration-differential-testing: sources=21 cited=21
errors: []
git diff --check -- <both skill dirs>
(no output, exit 0)
```

`check_links.py` (scratchpad `f-check/`) resolves every relative Markdown link and compares inline http(s) URLs (fragment stripped) with sources.yaml in both directions. It checks structure, not whether each citation supports its sentence; that was checked by hand against the raw files listed above.

## Remaining unverified

- The in-browser `renderToString` versus Node `renderToString` comparator was not executed; byte-identical output for a deterministic tree is untested (labelled in worked-paired-cases.md).
- `typeof React.captureOwnerStack` as a build probe and Playwright browser-version recording: proposed, not executed (labelled).
- Jazzer.js on Node 26: deprecation warning behavior and whether ESM instrumentation still works were not run (stated in factors-and-coverage.md).
- Which of 422/423 fires for a given tree was not traced.
- LambdaTester and Nessie were not installed or run; paper facts come from paper-reader notes produced by other agents, not from my own reading of page images.
- `emarteca/nessie` being the paper's tool is inferred (not cited in the skills).
- Node dual-package hazard details live in an external repository not read; the skills quote only the packages.md sentence.

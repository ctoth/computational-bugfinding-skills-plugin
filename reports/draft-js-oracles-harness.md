# Draft: JS/Node/React extension of correctness-oracles and harness-sensitivity (group G)

Status: drafted and validated. Not committed or pushed. No other skills, manifests, README or agent-notes edited. Nothing installed or executed except read-only fetches, the validators and `git diff --check`.

## Findings log

### Inputs read (step 1)

- `reports/research-js-oracles-harness.md` in full (N1-N9, R1-R4, P1, K1-K3, M1-M9, sources, unverified).
- `reports/research-js-differential.md` hydration lines 52-98, 153-154, 200-203: production text/structure mismatches reach `onRecoverableError` with minified codes (418, 421-424); attribute-only mismatches are a development-only `console.error` (`ReactFiberHydrationContext.js:933-969`). The oracle reference must say "hydration attribute warnings are dev-only", not "hydration mismatches are dev-only", so it agrees.
- `reports/skill-plan-js-web-bugfinding.md` lines 36-37, 58.
- Both skills' SKILL.md, sources.yaml, common-mistakes.md; harness-sensitivity runtime-integrations.md and control-design.md.
- `reports/draft-correctness-oracles.md` (format example).
- Paper notes: Wang 2017 notes lines 1-40 and summary (dataset URL p.2, 22 issue URLs p.11, NodeRacer reuse); Staicu 2018 notes lines 1-90 (benchmark URL p.362, decision rule p.365-366).

### Plan (file decisions, following research "Decisions for the drafter")

1. correctness-oracles: new `references/javascript-observation-channels.md` (N1, N2, N3/N7/N8 runner settings, R1-R4, P1); one sentence in SKILL.md; description terms; common-mistakes M1-M4 plus M9 (runner suppression is an oracle-channel mistake); sources.yaml.
2. harness-sensitivity: new section in `runtime-integrations.md` (N4-N8 coverage, order probes, leak signals; StrykerJS untouched); known-defect paragraph in `control-design.md` (K1-K3); common-mistakes M5-M8; one clause in SKILL.md; description terms; sources.yaml.
3. Verify every cited URL resolves and every quoted fragment is present in the fetched source; validate; record outputs.

### Source pins re-fetched (step 2)

- Peeled annotated tags via `gh api`: Node v26.13.0 tag object `daaa22ae` -> commit `18b32a3b1552e199a01f1a8d9fd64aa756d3b75b`; v24.22.2 tag object `15227f63` -> commit `f7f273a9bb6445f6f7fb6349105e7532972045fb`. React v19.3.1 ref is a commit `61aa00df822d0eb76d0362eb8b6fdd3527693efe`. BugsJS docker-environment full sha `252cf8d79f0d0ecc9a80afc518f7e7d4b7ae6400`. Skill links use these commit SHAs, not tag names.
- Downloaded 32 raw files (list in scratchpad `urls.txt`); all returned HTTP 200.
- Quote check: every quoted fragment used in the drafts was grepped in the fetched file. Misses on first pass were line-wrap or markdown-link differences, confirmed by reading context. One research fact was NOT found at the pin and is dropped: node:test "If no tests are run, a coverage report is not generated" (not present in `doc/api/test.md` at `18b32a3b`, coverage section lines 897-953).

### correctness-oracles (step 3)

- New `references/javascript-observation-channels.md`: Node process channel (N1, N2), test-runner status (N3, N7, N8), React root callbacks (R1, with reportGlobalError branches read from `packages/shared/reportGlobalError.js` at `61aa00df`), console/build mode (R2, aligned with research-js-differential: attribute warnings dev-only, text/structure mismatches upgraded to recoverable errors), StrictMode (R3), useSyncExternalStore worked contract (R4), Playwright (P1). Each channel: reports / depends on / misses.
- SKILL.md: description terms appended; one paragraph after the candidate-observation convention pointing to the new reference (with the Node exit-0 quote).
- common-mistakes.md: five new entries (research M1, M2, M3, M4, M9). M9 placed here rather than harness-sensitivity because it is about what a runner status observes.
- sources.yaml: 19 entries added (Node cli/process/test, Jest CLI/JestObjectAPI, Vitest two config pages, react.dev four pages, React CHANGELOG and four source files, Playwright page). Section names checked against the fetched headings.

### harness-sensitivity (step 4)

- `runtime-integrations.md`: new section "JavaScript/TypeScript: reachability, order and leak probes" after "Optional reachability evidence" (c8, node:test coverage, NODE_V8_COVERAGE, Jest babel default, Vitest v8 not on Firefox/Bun; node:test/Jest/Vitest order probes with Node v26.1.0 and v24.16.0 versions; node:test extraneous activity, Jest detectOpenHandles/forceExit/openHandlesTimeout). StrykerJS section untouched. The research's `--test-rerun-failures` incompatibility is not stated: at `18b32a3b`, `test.md:846` names only `--watch`.
- `control-design.md`: "Known-defect sources for JavaScript" (BugsJS, sola-da/ReDoS-vulnerabilities, NodeCB) with licenses and limits. NodeCB live URL re-checked: HTTP 404; Wayback `id_` snapshot fetched, phrases "teaching and research purposes", "leave your contact information before downloading" present. sola-da license null and "research purpose only" description re-checked via `gh api repos/sola-da/ReDoS-vulnerabilities`.
- Not stated (unverified in research): plain-Node landing of React's default handler, jsdom `reportError`, Playwright `pageerror` for rejections. The reference says "check which branch runs" instead of claiming one.
- `common-mistakes.md`: four new entries (research M5-M8). SKILL.md: description terms appended; one clause in "Use the current harness and runner" pointing to the new section. No new audit steps.
- `sources.yaml`: 22 entries added (c8 README/package.json; Node test.md, cli.md v26.13.0 and v24.22.2, CHANGELOG_V24; Jest CLI/Configuration; Vitest sequence/coverage; BugsJS README/LICENSE/Versions/Projects/Dockerfile; sola-da README/test-forwarded.js/repo metadata; Staicu and Wang papers; NodeCB Wayback). Paper entries cite pages from the paper-reader notes, not a fresh reading.

## Files changed

- `plugins/bugfinding/skills/correctness-oracles/SKILL.md`
- `plugins/bugfinding/skills/correctness-oracles/references/javascript-observation-channels.md` (new)
- `plugins/bugfinding/skills/correctness-oracles/references/common-mistakes.md`
- `plugins/bugfinding/skills/correctness-oracles/references/sources.yaml`
- `plugins/bugfinding/skills/harness-sensitivity/SKILL.md`
- `plugins/bugfinding/skills/harness-sensitivity/references/runtime-integrations.md`
- `plugins/bugfinding/skills/harness-sensitivity/references/control-design.md`
- `plugins/bugfinding/skills/harness-sensitivity/references/common-mistakes.md`
- `plugins/bugfinding/skills/harness-sensitivity/references/sources.yaml`
- `reports/draft-js-oracles-harness.md` (this report)

## Validation output

```text
uv run --no-project --with pyyaml python C:/Users/Q/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/bugfinding/skills/correctness-oracles
Skill is valid!
uv run --no-project --with pyyaml python C:/Users/Q/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/bugfinding/skills/harness-sensitivity
Skill is valid!

scratchpad check_skill.py (sources.yaml URLs vs inline Markdown URLs, both directions; local links)
== correctness-oracles
cited not listed: []
listed not cited: []
bad local links: []
sources=25 cited=25
== harness-sensitivity
cited not listed: []
listed not cited: []
bad local links: []
sources=34 cited=34

git diff --check -- plugins/bugfinding/skills/correctness-oracles plugins/bugfinding/skills/harness-sensitivity
(no output, exit 0)
grep -nE '[[:blank:]]+$' javascript-observation-channels.md (untracked, not covered by diff --check)
(no output, exit 1 = no trailing whitespace); file ends with a newline

uv run scripts/check_package.py
Package valid: 1 plugin(s), 26 skills
```

URL resolution: the 32 pinned raw files returned HTTP 200 (curl). USENIX page and GitHub API metadata returned 200 (PowerShell). The Wang DOI is registered (doi.org handle API -> `http://ieeexplore.ieee.org/document/8115663/`); the IEEE landing page itself was not fetched (PowerShell redirect error). Late in the session bash curl began failing with exit 43 on every URL; the earlier 200s were obtained before that.

## Remaining unverified items

- Playwright `pageerror`/`weberror` for unhandled promise rejections and `reportError(...)` calls (docs say only "uncaught exception").
- Which `reportGlobalError` branch runs in plain Node and jsdom (whether `reportError` exists there); not executed.
- Whether Vitest prints the shuffle seed (the skill says the page does not state it and recommends setting it).
- Whether c8 (via test-exclude) excludes `node_modules` like node:test does; the skill states only node:test's default.
- How Jest and node:test report an `uncaughtException` thrown while a test is still running.
- The full list of `__DEV__`-only React warnings; only the cited instances were read.
- Whether BugsJS bugs build and run on current Node (image is Node 8.16); the skill tells the user to confirm before use.
- Which of the 22 NodeCB issue URLs still resolve and have identifiable fix commits.
- Whether the sola-da exploit scripts run on current Node with the pinned vulnerable versions.
- Paper facts (Staicu p.362; Wang pp.2, 11) come from the existing paper-reader notes; the papers were not re-read in this pass.


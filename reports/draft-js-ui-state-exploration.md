# Draft report: new skill `ui-state-exploration`

Drafter: group D, JS/TS extension of the `bugfinding` plugin (branch js-web-bugfinding).

## Progress log

- Created this report file. Next: read inputs (research report, skill plan section, house-style skills, paper notes).
- Read: `reports/research-js-ui-state-exploration.md` (all 244 lines), `reports/skill-plan-js-web-bugfinding.md:80-97`, `plugins/bugfinding/skills/stateful-property-testing/SKILL.md`, its `references/sources.yaml` and `references/common-mistakes.md`, `plugins/bugfinding/skills/bugfinding-campaign/SKILL.md`, `reports/draft-stateful-property-testing.md`, the Crawljax notes in full, and grep excerpts of the TSE 2012, Roest 2010 and BLeak notes for every page the draft cites.
- Re-fetched every pinned primary source the draft quotes into the scratchpad (Playwright v1.65.0 docs: aria-snapshots, class-page, class-browsercontext, params, actionability, locators, browser-contexts, auth, network, clock, class-tracing; react.dev at `7594a2b0`: createRoot, Component, act, Suspense, useTransition; chaosbringer at `5f69d89e`: crawler.ts, action-targets.ts, aria-targets.ts, aria-snapshot.ts, README.md, package.json) and printed the cited line ranges. Every quote the research recorded at those lines matched the fetched text. One correction: the Playwright `requestFailed` 404/503 note is at `class-page.md:534-536`, inside the research's `:511-538` range.
- Paper page citations checked against notes: TSE p.38 (Alg. 2 line 11), p.39 (exclusions), p.40 (comparators too permissive; inputs; resolver no guarantee), p.41 (generic invariants, Table 2), p.42 (graph invariants), p.43-44 (reproduction, report), p.46 (TaskFreak), p.48 (silent JS faults, depth 3), p.50 (smoke test; hardest part). Roest p.129-135 as in the research. Crawljax p.5, 8, 9, 10-11, 18-20, 24-27. BLeak p.2, 4, 5, 6, 11 (PDF pages of the extended version).
- BLeak URL: the existing `resource-complexity-testing/references/sources.yaml:107` pins `https://raw.githubusercontent.com/plasma-umass/BLeak/2b2db0832ea412fa56683de045420134e3c3aa79/paper.pdf`; the BLeak notes were read from the `master` copy. I use the pinned URL for consistency; that master and `2b2db08` are the same PDF is unverified.
- Next: write SKILL.md, three references, common-mistakes.md, sources.yaml.
- Verified two more facts before citing: `gh api repos/crawljax/crawljax` returned `Java`, `2023-09-18T07:08:58Z`, `archived: false`; the pinned `playwright-cli` SKILL.md (main `95e5dca3`) has description "Automate browser interactions, test web pages and work with Playwright tests." All six route-target skills named in the boundaries exist under `plugins/bugfinding/skills/`.
- Wrote `SKILL.md` (frontmatter `name`, `description` only; sections: state key, discover/fire/settle, reset/replay, oracles, bound/route/return with six one-line boundaries).
- Wrote `references/playwright-crawl-loop.md` (seven-step loop as prose procedure, no implementation code; candidate discovery and its listener-only blind spot; exclusions and inputs; settle including React Suspense/transition predicates; what auto-wait hides; reset and replay with role+name locators; trace artifacts; chaosbringer section). Header states nothing in it was executed. Checked TSE notes for p.44 (Table 3 `OnUrlLoadPlugin` "reset back-end state"), p.47 (HitList delete exclusion, add-once crawl condition), p.48 (TUDU SQL reset per run).
- Wrote `references/oracles-per-state.md` (generic per-event/per-state checks, React error channels with the boundary limits, invariants with preconditions, graph checks, classification evidence, hand-offs incl. BLeak loop). Removed quote marks where the TSE notes paraphrase rather than quote (p.43 "another browser", p.46 calendar invariant).
- Wrote `references/common-mistakes.md` (15 Wrong/Better bullets, #15 is the URL-level random crawl vs state coverage). Removed quote marks from Crawljax p.19 "not all states are necessarily reached" because the notes record it as a paraphrased conclusion.
- Wrote `references/sources.yaml` (27 entries, house schema name/url/type/accessed/sections_used).
- Validation run; outputs below.
- Wrote `references/state-abstraction.md` (normalizer pipeline with preconditions, planted-difference control, source-level nondeterminism removal, aria snapshot as coarse key, global dedup, worked example labelled "illustration, not executed").

## Decisions

- Reference file names follow the research outline: `state-abstraction.md`, `playwright-crawl-loop.md` (discovery, inputs, settle, reset, replay, artifacts, chaosbringer), `oracles-per-state.md` (oracles plus hand-offs), `common-mistakes.md`, `sources.yaml`.
- The crawl loop is a prose procedure naming only documented Playwright calls (`browser.newContext`, `Page.ariaSnapshot`, `waitForFunction`, `pageerror`/`console`/`webError`, `Tracing.start` `snapshots`, `dispatchEvent`, `force`, `setFixedTime`, `route.fulfill`). No implementation file and no code sketch: the task says not to write a crawler implementation, and a sketch would carry unexecuted API calls.
- For dead clickables the draft says "read HTTP status of finished requests" without naming a Response accessor, because I did not read the Response API page.
- chaosbringer per research X2: named as an optional baseline/oracle harness, not a dependency; common mistake #15 included.
- Boundaries: six one-line route bullets in SKILL.md (stateful-property-testing, resource-complexity-testing, correctness-oracles, failure-reduction/evidence-based-triage, schedule-exploration, Playwright's own skills). Fuller hand-offs (configuration-differential-testing, distributed-fault-testing) are in the references.
- Not done by me (parent's job per the brief): `bugfinding-campaign` routing-table row, manifests and README skill count, the `stateful-property-testing` back-reference (already present at its `SKILL.md:8`).

## Files created

- `C:/Users/Q/code/computational-bugfinding-skills-plugin/plugins/bugfinding/skills/ui-state-exploration/SKILL.md` (39 lines)
- `C:/Users/Q/code/computational-bugfinding-skills-plugin/plugins/bugfinding/skills/ui-state-exploration/references/state-abstraction.md` (36 lines)
- `C:/Users/Q/code/computational-bugfinding-skills-plugin/plugins/bugfinding/skills/ui-state-exploration/references/playwright-crawl-loop.md` (60 lines)
- `C:/Users/Q/code/computational-bugfinding-skills-plugin/plugins/bugfinding/skills/ui-state-exploration/references/oracles-per-state.md` (43 lines)
- `C:/Users/Q/code/computational-bugfinding-skills-plugin/plugins/bugfinding/skills/ui-state-exploration/references/common-mistakes.md` (17 lines, 15 bullets)
- `C:/Users/Q/code/computational-bugfinding-skills-plugin/plugins/bugfinding/skills/ui-state-exploration/references/sources.yaml` (27 sources)
- this report

## Validation output

```text
$ uv run --no-project --with pyyaml python C:/Users/Q/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/bugfinding/skills/ui-state-exploration
Skill is valid!
exit=0
```

Inline `python -I -c` probe (pyyaml, re, pathlib, urllib.parse.urldefrag) over the skill directory: parsed sources.yaml, extracted every Markdown link target, checked relative links resolve, compared cited http URLs with sources.yaml URLs both ways.

```text
SKILL.md 39 lines
references\common-mistakes.md 17 lines
references\oracles-per-state.md 43 lines
references\playwright-crawl-loop.md 60 lines
references\state-abstraction.md 36 lines
sources 27 cited 27
cited not in yaml []
yaml not cited []
link errors []
```

```text
$ git diff --check -- plugins/bugfinding/skills/ui-state-exploration reports/draft-js-ui-state-exploration.md
(no output, exit 0; the paths are untracked so this check covers nothing on its own)
$ grep -rnE '[[:space:]]+$' plugins/bugfinding/skills/ui-state-exploration reports/draft-js-ui-state-exploration.md
(no output, exit 1 = no trailing whitespace, no CR line endings)
$ git status --short ...
?? plugins/bugfinding/skills/ui-state-exploration/
?? reports/draft-js-ui-state-exploration.md
```

These are structural checks. Source entailment was checked by hand: every quoted Playwright, react.dev and chaosbringer line was re-fetched at its pin and printed this session; paper pages were checked against the paper-reader notes (not page images; I did not re-read the PDFs). Nothing was committed or pushed; no target was run.

## Remaining unverified items

1. ICSE 2009 invariant-testing paper not read; only its TSE 2012 extension (via notes).
2. Unhandled promise rejections as `pageerror`: only chaosbringer's source comment (Chromium); Firefox/WebKit unknown. The skill tells the agent to capture `unhandledrejection` too.
3. `cursor` attribute in aria snapshots (chaosbringer `aria-snapshot.ts:170`) is not in the Playwright docs read; marked unverified in the crawl-loop reference.
4. Aria snapshot stability across browsers for the same DOM: not checked; stated as unverified in state-abstraction.md.
5. Inferences labelled in the text, not executed: boundary-caught React errors absent from `pageerror`; event-handler/async errors surfacing as uncaught; no browser-level React idle API; role-based candidate discovery; two-equal-keys stability check; CSS-only differences absent from aria snapshots.
6. BLeak URL pinned at `2b2db08` (same as resource-complexity-testing) while the notes were read from `master`; same PDF assumed, not compared.
7. chaosbringer: `settle.ts`, drivers, setup hook not read; repository Node floor `>=22` vs npm 0.15.0 `>=20` (research J12) unresolved; nothing executed; "no in-page state key" is from the files read, not a full read of `crawler.ts`.
8. Playwright license and Node floor at v1.65.0 not re-read (not cited in the skill).
9. No crawl loop built from this guidance has been run against any target.
